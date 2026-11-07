#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/supervisor_gate.py
Công cụ giám sát tự động (C# Inspector Gatekeeper) cho dự án Godot 4 .NET 8.
Thực thi kiểm tra Clean Code, an toàn bộ nhớ, Input Action và dotnet build.
Trả về exit code 0 nếu PASS, 1 nếu vi phạm.
"""

import os
import re
import sys
import subprocess
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = WORKSPACE_ROOT / "Scripts"
PROJECT_GODOT = WORKSPACE_ROOT / "project.godot"
CSPROJ_FILE = WORKSPACE_ROOT / "Dự án Trò chơi Mới.csproj"

MAX_FILE_LINES = 200
MAX_METHOD_LINES = 25

class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    RESET = "\033[0m"

def print_header(text):
    print(f"\n{Colors.CYAN}{'='*60}\n[GATEKEEPER] {text}\n{'='*60}{Colors.RESET}")

def print_pass(text):
    print(f"{Colors.GREEN}  [PASS] {text}{Colors.RESET}")

def print_fail(text):
    print(f"{Colors.RED}  [FAIL] {text}{Colors.RESET}")

def print_warn(text):
    print(f"{Colors.YELLOW}  [WARN] {text}{Colors.RESET}")

def inspect_cs_files():
    """Kiểm tra độ dài file, độ dài hàm và an toàn bộ nhớ trong Scripts/."""
    violations = []
    
    if not SCRIPTS_DIR.exists():
        return violations

    for cs_file in SCRIPTS_DIR.rglob("*.cs"):
        try:
            with open(cs_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except Exception as e:
            violations.append(f"{cs_file.name}: Không đọc được file ({e})")
            continue

        file_len = len(lines)
        rel_path = cs_file.relative_to(WORKSPACE_ROOT)

        # 1. Kiểm tra độ dài file (< 200 dòng)
        if file_len >= MAX_FILE_LINES:
            violations.append(f"{rel_path}: File dài {file_len} dòng (Giới hạn < {MAX_FILE_LINES} dòng)")

        # 2. Kiểm tra độ dài hàm (< 25 dòng)
        method_pattern = re.compile(
            r'^\s*(?:public|private|protected|internal|static|async|override|virtual)?\s+'
            r'(?:[a-zA-Z0-9_<>,\s]+)\s+([a-zA-Z0-9_]+)\s*\([^\)]*\)\s*$'
        )

        brace_depth = 0
        current_method = None
        method_start_line = 0

        for idx, line in enumerate(lines, start=1):
            stripped = line.strip()

            # Phát hiện chữ ký hàm sơ bộ
            if brace_depth == 1 and method_pattern.match(line):
                match = method_pattern.match(line)
                name = match.group(1) if match else "Unknown"
                if name not in ["if", "for", "while", "switch", "catch", "using"]:
                    current_method = name
                    method_start_line = idx

            # Đếm dấu ngoặc nhọn
            brace_depth += line.count('{') - line.count('}')

            if current_method and brace_depth == 1 and '}' in line:
                method_len = idx - method_start_line + 1
                if method_len >= MAX_METHOD_LINES:
                    violations.append(
                        f"{rel_path}:{method_start_line}: Hàm '{current_method}' dài {method_len} dòng (Giới hạn < {MAX_METHOD_LINES} dòng)"
                    )
                current_method = None

        # 3. Kiểm tra an toàn bộ nhớ (+= phải có -= tương ứng)
        file_text = "".join(lines)
        plus_events = re.findall(r'(\w+)\s*\+=\s*(\w+);', file_text)
        minus_events = re.findall(r'(\w+)\s*-=\s*(\w+);', file_text)
        
        # Nếu có BodyEntered/Pressed/ValueChanged mà không có ExitTree
        dangerous_events = [ev for ev in plus_events if ev[0] in ["BodyEntered", "BodyExited", "Pressed", "ValueChanged", "Timeout"]]
        if dangerous_events and "_ExitTree" not in file_text:
            violations.append(f"{rel_path}: Có đăng ký sự kiện {dangerous_events} nhưng thiếu phương thức _ExitTree() để hủy -= !")

    return violations

def inspect_input_actions():
    """Kiểm tra mọi Input Action dùng trong C# đã được đăng ký trong project.godot."""
    violations = []
    if not PROJECT_GODOT.exists():
        violations.append("Không tìm thấy file project.godot!")
        return violations

    with open(PROJECT_GODOT, "r", encoding="utf-8") as f:
        godot_content = f.read()

    # Tìm các action trong project.godot
    declared_actions = set(re.findall(r'^([a-zA-Z0-9_]+)=\{\s*"deadzone"', godot_content, re.MULTILINE))

    # Tìm các action được gọi trong C#
    used_actions = set()
    for cs_file in SCRIPTS_DIR.rglob("*.cs"):
        with open(cs_file, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        matches = re.findall(r'Input\.(?:IsActionPressed|IsActionJustPressed|IsActionJustReleased|GetVector|GetAxis|GetActionStrength)\(\s*"([^"]+)"', content)
        for m in matches:
            used_actions.add((m, cs_file.relative_to(WORKSPACE_ROOT)))

    for action, source_file in used_actions:
        # Bỏ qua built-in ui_* actions của Godot
        if action.startswith("ui_"):
            continue
        if action not in declared_actions:
            violations.append(f"{source_file}: Input Action \"{action}\" chưa được khai báo trong project.godot!")

    return violations

def check_dotnet_build():
    """Chạy dotnet build và xác nhận 0 Warning, 0 Error."""
    if not CSPROJ_FILE.exists():
        return False, "Không tìm thấy file .csproj!"

    try:
        res = subprocess.run(
            ["dotnet", "build", str(CSPROJ_FILE), "--nologo"],
            capture_output=True,
            text=True,
            check=False
        )
        if res.returncode != 0:
            return False, res.stdout + "\n" + res.stderr
        if "Warning(s)" in res.stdout and "0 Warning(s)" not in res.stdout:
            return False, f"Cảnh báo biên dịch:\n{res.stdout}"
        return True, "0 Warning(s), 0 Error(s)"
    except Exception as e:
        return False, f"Lỗi chạy dotnet build: {e}"

def main():
    print_header("RÀ SOÁT CHẤT LƯỢNG MÃ NGUỒN C# & QUY CHUẨN DỰ ÁN")
    all_passed = True

    # 1. Static Clean Code Analysis
    print("\n[1/3] Rà soát Clean Code (<25 dòng/hàm, <200 dòng/file, Memory Leak)...")
    code_violations = inspect_cs_files()
    if code_violations:
        all_passed = False
        for v in code_violations:
            print_fail(v)
    else:
        print_pass("100% tệp C# < 200 dòng, hàm < 25 dòng, an toàn bộ nhớ.")

    # 2. Input Action Validation
    print("\n[2/3] Kiểm tra đăng ký Input Action trong project.godot...")
    input_violations = inspect_input_actions()
    if input_violations:
        all_passed = False
        for v in input_violations:
            print_fail(v)
    else:
        print_pass("Mọi Input Action gọi trong C# đều được đăng ký đầy đủ.")

    # 3. Dotnet Build
    print("\n[3/3] Kiểm tra biên dịch dotnet build...")
    build_ok, build_msg = check_dotnet_build()
    if not build_ok:
        all_passed = False
        print_fail(build_msg)
    else:
        print_pass("Biên dịch .NET 8 thành công: 0 Cảnh báo, 0 Lỗi.")

    print_header("KẾT QUẢ NGHIỆM THU GATEKEEPER")
    if all_passed:
        print(f"{Colors.GREEN}>>> CHUẨN XÁC 100% - ĐỦ ĐIỀU KIỆN CHUYỂN GIAO LÊN @chief-supervisor <<<{Colors.RESET}\n")
        sys.exit(0)
    else:
        print(f"{Colors.RED}>>> THẤT BẠI - BẮT BUỘC @csharp-coder PHẢI REFACTOR LẠI NGAY LẬP TỨC <<<{Colors.RESET}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
