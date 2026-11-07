using Godot;
using Game.Core;

namespace Game.UI;

/// <summary>
/// Tab tinh chỉnh cấu hình đồ họa, độ phân giải, FPS và VSync trong Dev HUD.
/// </summary>
public partial class DevGraphicsTab : VBoxContainer
{
	[Export] public OptionButton? ResolutionOption { get; set; }
	[Export] public OptionButton? WindowModeOption { get; set; }
	[Export] public OptionButton? FpsOption { get; set; }
	[Export] public OptionButton? VsyncOption { get; set; }
	[Export] public Button? SaveBtn { get; set; }
	[Export] public Label? StatusLabel { get; set; }

	public override void _Ready()
	{
		LocateControls();
		PopulateAllOptions();
		SyncFromCurrentSettings();
		BindEvents();
	}

	public override void _ExitTree() => UnbindEvents();

	private void PopulateAllOptions()
	{
		if (ResolutionOption != null)
		{
			ResolutionOption.Clear();
			for (int i = 0; i < DisplaySettingsManager.AvailableResolutions.Length; i++)
			{
				Vector2I r = DisplaySettingsManager.AvailableResolutions[i];
				ResolutionOption.AddItem($"{r.X} x {r.Y}", i);
			}
		}

		if (WindowModeOption != null)
		{
			WindowModeOption.Clear();
			WindowModeOption.AddItem("Cửa sổ (Windowed)", 0);
			WindowModeOption.AddItem("Không viền (Borderless)", 1);
			WindowModeOption.AddItem("Toàn màn hình (Fullscreen)", 2);
		}

		if (FpsOption != null)
		{
			FpsOption.Clear();
			for (int i = 0; i < DisplaySettingsManager.AvailableFpsLimits.Length; i++)
			{
				int f = DisplaySettingsManager.AvailableFpsLimits[i];
				FpsOption.AddItem(f == 0 ? "Không giới hạn" : $"{f} FPS", i);
			}
		}

		if (VsyncOption != null)
		{
			VsyncOption.Clear();
			VsyncOption.AddItem("Tắt VSync", 0);
			VsyncOption.AddItem("Bật VSync", 1);
			VsyncOption.AddItem("Thích ứng (Adaptive)", 2);
		}
	}

	private void SyncFromCurrentSettings()
	{
		DisplaySettingsManager? mgr = DisplaySettingsManager.Instance;
		if (mgr == null) return;

		for (int i = 0; i < DisplaySettingsManager.AvailableResolutions.Length; i++)
		{
			if (DisplaySettingsManager.AvailableResolutions[i] == mgr.CurrentResolution)
			{
				ResolutionOption?.Select(i);
				break;
			}
		}

		int modeIdx = mgr.CurrentWindowMode == DisplayServer.WindowMode.ExclusiveFullscreen ? 2 : (mgr.CurrentWindowMode == DisplayServer.WindowMode.Fullscreen ? 1 : 0);
		WindowModeOption?.Select(modeIdx);

		for (int i = 0; i < DisplaySettingsManager.AvailableFpsLimits.Length; i++)
		{
			if (DisplaySettingsManager.AvailableFpsLimits[i] == mgr.CurrentMaxFps)
			{
				FpsOption?.Select(i);
				break;
			}
		}

		int vsyncIdx = mgr.CurrentVSync == DisplayServer.VSyncMode.Adaptive ? 2 : (mgr.CurrentVSync == DisplayServer.VSyncMode.Enabled ? 1 : 0);
		VsyncOption?.Select(vsyncIdx);
	}

	private void BindEvents()
	{
		if (ResolutionOption != null) ResolutionOption.ItemSelected += OnResolutionSelected;
		if (WindowModeOption != null) WindowModeOption.ItemSelected += OnWindowModeSelected;
		if (FpsOption != null) FpsOption.ItemSelected += OnFpsSelected;
		if (VsyncOption != null) VsyncOption.ItemSelected += OnVsyncSelected;
		if (SaveBtn != null) SaveBtn.Pressed += OnSavePressed;
	}

	private void UnbindEvents()
	{
		if (ResolutionOption != null) ResolutionOption.ItemSelected -= OnResolutionSelected;
		if (WindowModeOption != null) WindowModeOption.ItemSelected -= OnWindowModeSelected;
		if (FpsOption != null) FpsOption.ItemSelected -= OnFpsSelected;
		if (VsyncOption != null) VsyncOption.ItemSelected -= OnVsyncSelected;
		if (SaveBtn != null) SaveBtn.Pressed -= OnSavePressed;
	}

	private void OnResolutionSelected(long idx)
	{
		if (idx < 0 || idx >= DisplaySettingsManager.AvailableResolutions.Length) return;
		DisplaySettingsManager.Instance?.SetResolution(DisplaySettingsManager.AvailableResolutions[(int)idx]);
		SetStatus("Đã đổi độ phân giải!");
	}

	private void OnWindowModeSelected(long idx)
	{
		DisplayServer.WindowMode mode = idx switch
		{
			1 => DisplayServer.WindowMode.Fullscreen,
			2 => DisplayServer.WindowMode.ExclusiveFullscreen,
			_ => DisplayServer.WindowMode.Windowed
		};
		DisplaySettingsManager.Instance?.SetWindowMode(mode);
		SetStatus("Đã đổi chế độ cửa sổ!");
	}

	private void OnFpsSelected(long idx)
	{
		if (idx < 0 || idx >= DisplaySettingsManager.AvailableFpsLimits.Length) return;
		int fps = DisplaySettingsManager.AvailableFpsLimits[(int)idx];
		DisplaySettingsManager.Instance?.SetMaxFps(fps);
		SetStatus($"Đã đặt giới hạn: {(fps == 0 ? "Vô hạn" : $"{fps} FPS")}");
	}

	private void OnVsyncSelected(long idx)
	{
		DisplayServer.VSyncMode vsync = idx switch
		{
			1 => DisplayServer.VSyncMode.Enabled,
			2 => DisplayServer.VSyncMode.Adaptive,
			_ => DisplayServer.VSyncMode.Disabled
		};
		DisplaySettingsManager.Instance?.SetVSync(vsync);
		SetStatus("Đã cập nhật VSync!");
	}

	private void OnSavePressed()
	{
		DisplaySettingsManager.Instance?.SaveSettings();
		SetStatus("💾 Đã lưu cấu hình vào user://settings.cfg!");
	}

	private void SetStatus(string msg)
	{
		if (StatusLabel != null) StatusLabel.Text = msg;
	}

	private void LocateControls()
	{
		ResolutionOption ??= GetNodeOrNull<OptionButton>("ResRow/ResOption");
		WindowModeOption ??= GetNodeOrNull<OptionButton>("ModeRow/ModeOption");
		FpsOption ??= GetNodeOrNull<OptionButton>("FpsRow/FpsOption");
		VsyncOption ??= GetNodeOrNull<OptionButton>("VsyncRow/VsyncOption");
		SaveBtn ??= GetNodeOrNull<Button>("SaveBtn");
		StatusLabel ??= GetNodeOrNull<Label>("StatusLabel");
	}
}
