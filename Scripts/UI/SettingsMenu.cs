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
		SettingsMenuBinder.PopulateOptions(ResolutionOption, WindowModeOption, FpsOption, VsyncOption);
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
		if (!IsMenuOpen) return;
		if (@event.IsActionPressed("ui_cancel") || IsCancelTriggered(@event))
		{
			ToggleMenu();
			GetViewport().SetInputAsHandled();
		}
	}

	private static bool IsCancelTriggered(InputEvent @event)
	{
		if (@event is InputEventKey key && key.Pressed && !key.Echo && key.Keycode == Key.Escape) return true;
		return @event is InputEventJoypadButton joy && joy.Pressed && joy.ButtonIndex == JoyButton.B;
	}

	public void ToggleMenu() => SetMenuOpen(!IsMenuOpen);

	public void SetMenuOpen(bool open)
	{
		if (MainPanel != null) MainPanel.Visible = open;
		if (open)
		{
			SyncFromSettings();
			Input.MouseMode = Input.MouseModeEnum.Visible;
			(ResolutionOption ?? (Control?)CloseButton)?.GrabFocus();
		}
	}

	public void ApplyAndSaveSettings()
	{
		DisplaySettingsManager? mgr = DisplaySettingsManager.Instance;
		if (mgr == null) return;

		SettingsMenuBinder.ApplyToSettings(ResolutionOption, WindowModeOption, FpsOption, VsyncOption, mgr);
		mgr.SaveSettings();
		if (StatusLabel != null) StatusLabel.Text = "Đã lưu cài đặt thành công!";
	}

	private void LocateControls()
	{
		MainPanel ??= GetNodeOrNull<PanelContainer>("MainPanel");
		HudSettingsButton ??= GetNodeOrNull<Button>("HudSettingsButton");
		if (HudSettingsButton != null) HudSettingsButton.FocusMode = Control.FocusModeEnum.None;
		ResolutionOption ??= GetNodeOrNull<OptionButton>("MainPanel/Margin/VBox/Grid/ResolutionOption");
		WindowModeOption ??= GetNodeOrNull<OptionButton>("MainPanel/Margin/VBox/Grid/WindowModeOption");
		FpsOption ??= GetNodeOrNull<OptionButton>("MainPanel/Margin/VBox/Grid/FpsOption");
		VsyncOption ??= GetNodeOrNull<OptionButton>("MainPanel/Margin/VBox/Grid/VsyncOption");
		ApplyButton ??= GetNodeOrNull<Button>("MainPanel/Margin/VBox/ActionsBox/ApplyBtn");
		CloseButton ??= GetNodeOrNull<Button>("MainPanel/Margin/VBox/ActionsBox/CloseBtn");
		StatusLabel ??= GetNodeOrNull<Label>("MainPanel/Margin/VBox/StatusLabel");
	}

	private void SyncFromSettings()
	{
		DisplaySettingsManager? mgr = DisplaySettingsManager.Instance;
		if (mgr == null) return;
		SettingsMenuBinder.SyncFromSettings(ResolutionOption, WindowModeOption, FpsOption, VsyncOption, mgr);
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
