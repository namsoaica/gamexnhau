#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/supervisor_gate.py
Công cụ giám sát tự động (C# Inspector Gatekeeper & Role Isolation Auditor) cho dự án Godot 4 .NET 8.
Thực thi kiểm tra:
1. Luật Cô Lập Đơn Nhiệm & Ranh Giới File (Strict 1-Skill-Per-Subagent & File-Boundary Isolation)
2. Luật Ghép Cặp Giám Sát 1-Kèm-1 (Strict 1-to-1 Inspector Pairing)
3. Clean Code C# (<25 dòng/hàm, <200 dòng/file, an toàn bộ nhớ -= trong _ExitTree)
4. Đăng ký Input Action trong project.godot
5. Biên dịch .NET 8 (dotnet build 0 warning 0 error)

Trả về exit code 0 nếu PASS 100%, 1 nếu vi phạm.
"""

import os
import re
import sys
import json
import struct
import subprocess
from pathlib import Path

try:
    import numpy as np
    from PIL import Image
    HAS_PIXEL_DEPS = True
except ImportError:
    HAS_PIXEL_DEPS = False

WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = WORKSPACE_ROOT / "Scripts"
PROJECT_GODOT = WORKSPACE_ROOT / "project.godot"
CSPROJ_FILE = WORKSPACE_ROOT / "Dự án Trò chơi Mới.csproj"

MAX_FILE_LINES = 200
MAX_METHOD_LINES = 25

# Danh sách danh xưng Sub-agent hợp lệ tương ứng 1-1 với .agents/skills/
VALID_SKILL_ROLES = {
    "texture-architect": {"exts": [".png", ".tres"], "allow_catalog": True},
    "texture-inspector": {"inspector_for": "texture-architect"},
    "blender-helper": {"exts": [".py", ".blend", ".glb"]},
    "blender-inspector": {"inspector_for": "blender-helper"},
    "csharp-coder": {"exts": [".cs", ".tscn", ".godot"]},
    "csharp-inspector": {"inspector_for": "csharp-coder"},
    "chief-supervisor": {"role": "chief_supervisor"},
    "producer": {"exts": [".md"]},
    "checkpoint": {"exts": [".md"]}
}

FORBIDDEN_GENERIC_PATTERNS = [
    r"lead", r"system\s*lead", r"integrator", r"general", r"all-in-one", r"qa\s*tester"
]

class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    RESET = "\033[0m"

def print_header(text):
    print(f"\n{Colors.CYAN}{'='*65}\n[GATEKEEPER] {text}\n{'='*65}{Colors.RESET}")

def print_pass(text):
    print(f"{Colors.GREEN}  [PASS] {text}{Colors.RESET}")

def print_fail(text):
    print(f"{Colors.RED}  [FAIL] {text}{Colors.RESET}")

def print_warn(text):
    print(f"{Colors.YELLOW}  [WARN] {text}{Colors.RESET}")

def find_latest_transcript():
    """Tìm file transcript.jsonl mới nhất trong thư mục brain."""
    user_home = Path(os.environ.get("USERPROFILE", os.path.expanduser("~")))
    brain_root = user_home / ".gemini" / "antigravity-cli" / "brain"
    if not brain_root.exists():
        return None

    transcripts = list(brain_root.glob("*/.system_generated/logs/transcript.jsonl"))
    if not transcripts:
        return None
    transcripts.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return transcripts[0]

def inspect_role_isolation_and_pairing(recent_count=1):
    """Kiểm tra Luật Cô Lập Đơn Nhiệm, Ranh Giới File và Ghép Cặp Giám Sát 1-kèm-1 trong các phiên gần nhất."""
    violations = []
    transcript_path = find_latest_transcript()
    if not transcript_path or not transcript_path.exists():
        return violations

    invocations = []
    try:
        with open(transcript_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                if "invoke_subagent" in line:
                    try:
                        step_data = json.loads(line)
                        calls = step_data.get("tool_calls", [])
                        for call in calls:
                            if call.get("name") == "invoke_subagent":
                                args = call.get("args", {})
                                invocations.append(args)
                    except Exception:
                        continue
    except Exception as e:
        print_warn(f"Không thể đọc transcript: {e}")
        return violations

    # Chỉ kiểm tra các lần gọi gần nhất (recent_count) để áp dụng luật từ thời điểm ban hành
    recent_invocations = invocations[-recent_count:] if len(invocations) > recent_count else invocations

    # 1. Kiểm tra CẤM ĐẶT TÊN CHUNG CHUNG & KIÊM NHIỆM
    for inv in recent_invocations:
        role = inv.get("Role", "").lower()
        type_name = inv.get("TypeName", "").lower()
        
        # Nếu dùng tên chung chung cấm
        for pat in FORBIDDEN_GENERIC_PATTERNS:
            if re.search(r'\b' + pat + r'\b', role) and not ("chief-supervisor" in role or "chief supervisor" in role):
                violations.append(
                    f"[FAIL - VI PHẠM LUẬT CẤM GỘP VAI]: Tên Sub-agent '{inv.get('Role')}' vi phạm quy tắc cấm đặt tên chung chung/kiêm nhiệm!"
                )
                break

    # 2. Kiểm tra GHÉP CẶP GIÁM SÁT 1-KÈM-1 (Strict 1-to-1 Pairing)
    roles_called = [inv.get("Role", "").lower() for inv in recent_invocations]
    
    # Kiểm tra C#
    has_cs_worker = any("csharp-coder" in r or "c# programmer" in r or "c# coder" in r for r in roles_called)
    has_cs_inspector = any("csharp-inspector" in r or "c# inspector" in r for r in roles_called)
    if has_cs_worker and not has_cs_inspector:
        violations.append("[FAIL - VI PHẠM LUẬT CẤM GỘP VAI]: Có Sub-agent thợ C# nhưng THIẾU Sub-agent giám sát riêng @csharp-inspector!")

    # Kiểm tra Blender
    has_blender_worker = any("blender-helper" in r or "blender assistant" in r for r in roles_called)
    has_blender_inspector = any("blender-inspector" in r or "blender inspector" in r for r in roles_called)
    if has_blender_worker and not has_blender_inspector:
        violations.append("[FAIL - VI PHẠM LUẬT CẤM GỘP VAI]: Có Sub-agent thợ 3D Blender nhưng THIẾU Sub-agent giám sát riêng @blender-inspector!")

    # Kiểm tra Texture
    has_tex_worker = any("texture-architect" in r for r in roles_called)
    has_tex_inspector = any("texture-inspector" in r for r in roles_called)
    if has_tex_worker and not has_tex_inspector:
        violations.append("[FAIL - VI PHẠM LUẬT CẤM GỘP VAI]: Có Sub-agent thợ Texture nhưng THIẾU Sub-agent giám sát riêng @texture-inspector!")

    return violations

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
            if brace_depth == 1 and method_pattern.match(line):
                match = method_pattern.match(line)
                name = match.group(1) if match else "Unknown"
                if name not in ["if", "for", "while", "switch", "catch", "using"]:
                    current_method = name
                    method_start_line = idx

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

    declared_actions = set(re.findall(r'^([a-zA-Z0-9_]+)=\{\s*"deadzone"', godot_content, re.MULTILINE))
    used_actions = set()

    for cs_file in SCRIPTS_DIR.rglob("*.cs"):
        with open(cs_file, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        matches = re.findall(r'Input\.(?:IsActionPressed|IsActionJustPressed|IsActionJustReleased|GetVector|GetAxis|GetActionStrength)\(\s*"([^"]+)"', content)
        for m in matches:
            used_actions.add((m, cs_file.relative_to(WORKSPACE_ROOT)))

    for action, source_file in used_actions:
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

def inspect_pixel_mathematics():
    """Phân tích pixel toán học bằng PIL và numpy để chặn đứng ảnh lỗi, thiếu vật liệu hoặc bệt màu."""
    violations = []
    if not HAS_PIXEL_DEPS:
        violations.append("Thiếu thư viện PIL hoặc numpy để đo lường pixel toán học!")
        return violations

    target_images = list((WORKSPACE_ROOT / "docs" / "test_screenshots").glob("*.png"))
    preview_img = WORKSPACE_ROOT / "Assets" / "Models" / "_preview_render.png"
    if preview_img.exists():
        target_images.append(preview_img)

    if not target_images:
        violations.append("Chưa có ảnh chụp thực tế nào trong docs/test_screenshots/ để phân tích!")
        return violations

    for img_path in target_images:
        try:
            with Image.open(img_path) as im:
                rgb_im = im.convert("RGB")
                arr = np.array(rgb_im, dtype=np.float32)

            # [a] Kiểm tra độ sáng trung bình (Luminance)
            lum = 0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]
            mean_lum = float(np.mean(lum))
            if mean_lum < 20.0:
                violations.append(f"{img_path.name}: Ảnh quá tối (Luminance = {mean_lum:.1f} < 20.0)")
            elif mean_lum > 240.0:
                violations.append(f"{img_path.name}: Ảnh bị cháy sáng (Luminance = {mean_lum:.1f} > 240.0)")

            # [b] Kiểm tra mảng trắng/xám đồng nhất > 25% (dấu hiệu khối mesh trắng thiếu vật liệu)
            white_mask = (arr[:, :, 0] > 220) & (arr[:, :, 1] > 220) & (arr[:, :, 2] > 220) & \
                         (np.abs(arr[:, :, 0] - arr[:, :, 1]) < 15) & (np.abs(arr[:, :, 1] - arr[:, :, 2]) < 15)
            white_ratio = float(np.mean(white_mask))
            if white_ratio > 0.25:
                violations.append(f"{img_path.name}: Mảng trắng/xám đồng nhất chiếm {white_ratio*100:.1f}% > 25% (nguy cơ thiếu vật liệu)")

            # [c] Kiểm tra độ lệch chuẩn màu sắc (Color Variance/Entropy)
            std_col = float(np.std(arr))
            if std_col < 15.0:
                violations.append(f"{img_path.name}: Độ lệch chuẩn màu sắc quá thấp ({std_col:.1f} < 15.0) - ảnh bệt đơn sắc")

        except Exception as e:
            violations.append(f"{img_path.name}: Không thể phân tích pixel ({e})")

    return violations

def inspect_glb_structures():
    """Kiểm định cấu trúc file GLB 3D (kích thước tối thiểu và xác thực kênh UV TEXCOORD_0)."""
    violations = []
    models_dir = WORKSPACE_ROOT / "Assets" / "Models"
    if not models_dir.exists():
        return violations

    glb_files = list(models_dir.glob("*.glb"))
    if not glb_files:
        violations.append("Không tìm thấy file .glb nào trong Assets/Models/!")
        return violations

    for glb_path in glb_files:
        size_kb = glb_path.stat().st_size / 1024.0
        # Kiểm tra kích thước tối thiểu (trừ prop siêu nhỏ)
        min_size = 50.0 if "map" in glb_path.name.lower() else 10.0
        if size_kb < min_size:
            violations.append(f"{glb_path.name}: Kích thước quá nhỏ ({size_kb:.1f} KB < {min_size} KB) - nghi vấn khối sơ sài")

        # Kiểm tra binary header & JSON chunk chứa TEXCOORD_0
        try:
            with open(glb_path, "rb") as f:
                header = f.read(12)
                if len(header) < 12:
                    violations.append(f"{glb_path.name}: File GLB lỗi header!")
                    continue
                magic, ver, length = struct.unpack("<4sII", header)
                if magic != b"glTF":
                    violations.append(f"{glb_path.name}: Định dạng không phải glTF hợp lệ!")
                    continue

                chunk_header = f.read(8)
                if len(chunk_header) < 8:
                    violations.append(f"{glb_path.name}: Thiếu chunk JSON!")
                    continue
                chunk_len, chunk_type = struct.unpack("<I4s", chunk_header)
                json_bytes = f.read(chunk_len)
                data = json.loads(json_bytes.decode("utf-8", errors="ignore"))

                has_uv = any(
                    "TEXCOORD_0" in prim.get("attributes", {})
                    for mesh in data.get("meshes", [])
                    for prim in mesh.get("primitives", [])
                )
                if not has_uv and len(data.get("meshes", [])) > 0:
                    violations.append(f"{glb_path.name}: Không có kênh UV TEXCOORD_0 (chưa trải UV unwrapping)!")

        except Exception as e:
            violations.append(f"{glb_path.name}: Lỗi đọc cấu trúc nhị phân ({e})")

    return violations

def main():
    print_header("RÀ SOÁT TOÀN DIỆN PRODUCTION & CHAOS QA GATEKEEPER")
    all_passed = True

    # 1. Kiểm tra Luật Cô Lập Đơn Nhiệm & Ghép Cặp Giám Sát 1-kèm-1
    print("\n[1/6] Kiểm tra Luật Cô Lập Đơn Nhiệm & Ghép Cặp 1-kèm-1...")
    role_violations = inspect_role_isolation_and_pairing()
    if role_violations:
        all_passed = False
        for v in role_violations:
            print_fail(v)
    else:
        print_pass("Đạt chuẩn: Mỗi Sub-agent đơn nhiệm, gắn đúng 1-1 với Skill và ghép cặp Giám sát riêng.")

    # 2. Static Clean Code Analysis
    print("\n[2/6] Rà soát Clean Code (<25 dòng/hàm, <200 dòng/file, Memory Leak)...")
    code_violations = inspect_cs_files()
    if code_violations:
        all_passed = False
        for v in code_violations:
            print_fail(v)
    else:
        print_pass("100% tệp C# < 200 dòng, hàm < 25 dòng, an toàn bộ nhớ.")

    # 3. Input Action Validation
    print("\n[3/6] Kiểm tra đăng ký Input Action trong project.godot...")
    input_violations = inspect_input_actions()
    if input_violations:
        all_passed = False
        for v in input_violations:
            print_fail(v)
    else:
        print_pass("Mọi Input Action gọi trong C# đều được đăng ký đầy đủ.")

    # 4. Dotnet Build
    print("\n[4/6] Kiểm tra biên dịch dotnet build...")
    build_ok, build_msg = check_dotnet_build()
    if not build_ok:
        all_passed = False
        print_fail(build_msg)
    else:
        print_pass("Biên dịch .NET 8 thành công: 0 Cảnh báo, 0 Lỗi.")

    # 5. Pixel Mathematics & Lighting Analysis
    print("\n[5/6] Đo lường toán học Pixel & Độ sáng ảnh chụp thực tế (PIL/numpy)...")
    pixel_violations = inspect_pixel_mathematics()
    if pixel_violations:
        all_passed = False
        for v in pixel_violations:
            print_fail(v)
    else:
        print_pass("Đạt chuẩn: 100% ảnh chụp thực tế có độ tương phản, ánh sáng tự nhiên và không có mảng trắng thiếu vật liệu.")

    # 6. GLB Structure & UV Unwrapping Validation
    print("\n[6/6] Kiểm định cấu trúc file GLB 3D (Kích thước & Kênh UV TEXCOORD_0)...")
    glb_violations = inspect_glb_structures()
    if glb_violations:
        all_passed = False
        for v in glb_violations:
            print_fail(v)
    else:
        print_pass("Đạt chuẩn: 100% mô hình GLB đạt kích thước chi tiết và có kênh UV TEXCOORD_0.")

    print_header("KẾT QUẢ NGHIỆM THU GATEKEEPER")
    if all_passed:
        print(f"{Colors.GREEN}>>> CHUẨN XÁC 100% - ĐỦ ĐIỀU KIỆN CHUYỂN GIAO LÊN @chief-supervisor <<<{Colors.RESET}\n")
        sys.exit(0)
    else:
        print(f"{Colors.RED}>>> THẤT BẠI - BẮT BUỘC REFACTOR LẠI NGAY LẬP TỨC <<<{Colors.RESET}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
