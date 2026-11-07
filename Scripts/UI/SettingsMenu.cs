using Godot;
using Game.Core;

namespace Game.UI;

/// <summary>
/// Giao diện Menu Cài Đặt Game (Settings Menu) hỗ trợ điều chỉnh đồ họa, phân giải, FPS, VSync.
/// Tự động đồng bộ và lưu trữ cấu hình qua DisplaySettingsManager.
/// </summary>
public partial class SettingsMenu : CanvasLayer
{
	public static SettingsMenu? Instance { get; private set; }

	[ExportGroup("Tham Chiếu Giao Diện")]
	[Export] public PanelContainer? MainPanel { get; set; }
	[Export] public OptionButton? ResolutionOption { get; set; }
	[Export] public OptionButton? WindowModeOption { get; set; }
	[Export] public OptionButton? FpsOption { get; set; }
	[Export] public OptionButton? VsyncOption { get; set; }
	[Export] public Button? ApplyButton { get; set; }
	[Export] public Button? CloseButton { get; set; }
	[Export] public Button? HudSettingsButton { get; set; }
	[Export] public Label? StatusLabel { get; set; }

	public bool IsMenuOpen => MainPanel?.Visible ?? false;

	public override void _Ready()
	{
		Instance = this;
		LocateControls();
		PopulateOptions();
		SyncFromSettings();
		BindEvents();
		SetMenuOpen(false);
	}

	public override void _ExitTree()
	{
		if (Instance == this) Instance = null;
		UnbindEvents();
	}

	public override void _UnhandledInput(InputEvent @event)
	{
		if (@event is InputEventKey keyEvent && keyEvent.Pressed && !keyEvent.Echo)
		{
			if (keyEvent.Keycode == Key.Escape)
			{
				ToggleMenu();
				GetViewport().SetInputAsHandled();
			}
		}
	}

	public void ToggleMenu() => SetMenuOpen(!IsMenuOpen);

	public void SetMenuOpen(bool open)
	{
		if (MainPanel != null) MainPanel.Visible = open;
		if (open)
		{
			SyncFromSettings();
			Input.MouseMode = Input.MouseModeEnum.Visible;
		}
	}

	public void ApplyAndSaveSettings()
	{
		DisplaySettingsManager? mgr = DisplaySettingsManager.Instance;
		if (mgr == null) return;

		ApplySelectedResolution(mgr);
		ApplySelectedWindowMode(mgr);
		ApplySelectedFps(mgr);
		ApplySelectedVsync(mgr);

		mgr.SaveSettings();
		if (StatusLabel != null) StatusLabel.Text = "Đã lưu cài đặt thành công!";
	}

	private void LocateControls()
	{
		MainPanel ??= GetNodeOrNull<PanelContainer>("MainPanel");
		HudSettingsButton ??= GetNodeOrNull<Button>("HudSettingsButton");
		ResolutionOption ??= GetNodeOrNull<OptionButton>("MainPanel/Margin/VBox/Grid/ResolutionOption");
		WindowModeOption ??= GetNodeOrNull<OptionButton>("MainPanel/Margin/VBox/Grid/WindowModeOption");
		FpsOption ??= GetNodeOrNull<OptionButton>("MainPanel/Margin/VBox/Grid/FpsOption");
		VsyncOption ??= GetNodeOrNull<OptionButton>("MainPanel/Margin/VBox/Grid/VsyncOption");
		ApplyButton ??= GetNodeOrNull<Button>("MainPanel/Margin/VBox/ActionsBox/ApplyBtn");
		CloseButton ??= GetNodeOrNull<Button>("MainPanel/Margin/VBox/ActionsBox/CloseBtn");
		StatusLabel ??= GetNodeOrNull<Label>("MainPanel/Margin/VBox/StatusLabel");
	}

	private void PopulateOptions()
	{
		PopulateResolutions();
		PopulateWindowModes();
		PopulateFpsLimits();
		PopulateVsyncModes();
	}

	private void PopulateResolutions()
	{
		if (ResolutionOption == null) return;
		ResolutionOption.Clear();
		for (int i = 0; i < DisplaySettingsManager.AvailableResolutions.Length; i++)
		{
			Vector2I r = DisplaySettingsManager.AvailableResolutions[i];
			ResolutionOption.AddItem($"{r.X} x {r.Y}", i);
		}
	}

	private void PopulateWindowModes()
	{
		if (WindowModeOption == null) return;
		WindowModeOption.Clear();
		WindowModeOption.AddItem("Cửa sổ (Windowed)", 0);
		WindowModeOption.AddItem("Không viền (Borderless)", 1);
		WindowModeOption.AddItem("Toàn màn hình (Fullscreen)", 2);
	}

	private void PopulateFpsLimits()
	{
		if (FpsOption == null) return;
		FpsOption.Clear();
		for (int i = 0; i < DisplaySettingsManager.AvailableFpsLimits.Length; i++)
		{
			int f = DisplaySettingsManager.AvailableFpsLimits[i];
			FpsOption.AddItem(f == 0 ? "Không giới hạn" : $"{f} FPS", i);
		}
	}

	private void PopulateVsyncModes()
	{
		if (VsyncOption == null) return;
		VsyncOption.Clear();
		VsyncOption.AddItem("Tắt VSync", 0);
		VsyncOption.AddItem("Bật VSync", 1);
	}

	private void SyncFromSettings()
	{
		DisplaySettingsManager? mgr = DisplaySettingsManager.Instance;
		if (mgr == null) return;

		SyncResolutionSelection(mgr);
		SyncWindowModeSelection(mgr);
		SyncFpsSelection(mgr);
		SyncVsyncSelection(mgr);
	}

	private void SyncResolutionSelection(DisplaySettingsManager mgr)
	{
		for (int i = 0; i < DisplaySettingsManager.AvailableResolutions.Length; i++)
		{
			if (DisplaySettingsManager.AvailableResolutions[i] == mgr.CurrentResolution)
			{
				ResolutionOption?.Select(i);
				break;
			}
		}
	}

	private void SyncWindowModeSelection(DisplaySettingsManager mgr)
	{
		int idx = mgr.CurrentWindowMode == DisplayServer.WindowMode.ExclusiveFullscreen ? 2 : (mgr.CurrentWindowMode == DisplayServer.WindowMode.Fullscreen ? 1 : 0);
		WindowModeOption?.Select(idx);
	}

	private void SyncFpsSelection(DisplaySettingsManager mgr)
	{
		for (int i = 0; i < DisplaySettingsManager.AvailableFpsLimits.Length; i++)
		{
			if (DisplaySettingsManager.AvailableFpsLimits[i] == mgr.CurrentMaxFps)
			{
				FpsOption?.Select(i);
				break;
			}
		}
	}

	private void SyncVsyncSelection(DisplaySettingsManager mgr)
	{
		int idx = mgr.CurrentVSync == DisplayServer.VSyncMode.Disabled ? 0 : 1;
		VsyncOption?.Select(idx);
	}

	private void ApplySelectedResolution(DisplaySettingsManager mgr)
	{
		int idx = ResolutionOption?.Selected ?? 0;
		if (idx >= 0 && idx < DisplaySettingsManager.AvailableResolutions.Length)
		{
			mgr.SetResolution(DisplaySettingsManager.AvailableResolutions[idx]);
		}
	}

	private void ApplySelectedWindowMode(DisplaySettingsManager mgr)
	{
		int idx = WindowModeOption?.Selected ?? 0;
		var mode = idx switch
		{
			1 => DisplayServer.WindowMode.Fullscreen,
			2 => DisplayServer.WindowMode.ExclusiveFullscreen,
			_ => DisplayServer.WindowMode.Windowed
		};
		mgr.SetWindowMode(mode);
	}

	private void ApplySelectedFps(DisplaySettingsManager mgr)
	{
		int idx = FpsOption?.Selected ?? 1;
		if (idx >= 0 && idx < DisplaySettingsManager.AvailableFpsLimits.Length)
		{
			mgr.SetMaxFps(DisplaySettingsManager.AvailableFpsLimits[idx]);
		}
	}

	private void ApplySelectedVsync(DisplaySettingsManager mgr)
	{
		int idx = VsyncOption?.Selected ?? 1;
		mgr.SetVSync(idx == 0 ? DisplayServer.VSyncMode.Disabled : DisplayServer.VSyncMode.Enabled);
	}

	private void BindEvents()
	{
		if (ApplyButton != null) ApplyButton.Pressed += ApplyAndSaveSettings;
		if (CloseButton != null) CloseButton.Pressed += OnClosePressed;
		if (HudSettingsButton != null) HudSettingsButton.Pressed += OnHudSettingsPressed;
	}

	private void UnbindEvents()
	{
		if (ApplyButton != null) ApplyButton.Pressed -= ApplyAndSaveSettings;
		if (CloseButton != null) CloseButton.Pressed -= OnClosePressed;
		if (HudSettingsButton != null) HudSettingsButton.Pressed -= OnHudSettingsPressed;
	}

	private void OnClosePressed() => SetMenuOpen(false);
	private void OnHudSettingsPressed() => ToggleMenu();
}
