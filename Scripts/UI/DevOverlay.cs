using Godot;
using Game.Player;
using Game.Core;

namespace Game.UI;

/// <summary>
/// Bảng điều khiển Chế Độ Dev (Debug Overlay HUD) hỗ trợ Bàn phím & Tay cầm Gamepad.
/// </summary>
public partial class DevOverlay : CanvasLayer
{
	[ExportGroup("Cấu Hình Phím Tắt")]
	[Export] public Key ToggleKeyPrimary { get; set; } = Key.F1;
	[Export] public Key ToggleKeySecondary { get; set; } = Key.Quoteleft;
	[Export] public Key ToggleKeyTertiary { get; set; } = Key.F3;

	[ExportGroup("Tham Chiếu Controls")]
	[Export] public Control? MainPanel { get; set; }
	[Export] public Button? CloseBtn { get; set; }
	[Export] public TabContainer? Tabs { get; set; }
	[Export] public DevPlayerTab? PlayerTab { get; set; }
	[Export] public DevNpcTab? NpcTab { get; set; }
	[Export] public DevWorldTab? WorldTab { get; set; }

	private PlayerMovement? _player;
	private SimpleNpc? _npc;
	private CameraFollow? _camera;

	public override void _Ready()
	{
		FindControlsIfNull();
		LocateGameTargets();
		InitializeTabs();
		SetDevModeVisible(false);
	}

	public override void _UnhandledInput(InputEvent @event)
	{
		if (HandleToggleInput(@event))
		{
			GetViewport().SetInputAsHandled();
			return;
		}

		if (MainPanel != null && MainPanel.Visible && HandleTabNavigationInput(@event))
		{
			GetViewport().SetInputAsHandled();
		}
	}

	public override void _Process(double delta)
	{
		if (MainPanel == null || !MainPanel.Visible) return;
		WorldTab?.UpdateRealtimeStats();
	}

	/// <summary>
	/// Bật / tắt bảng HUD Dev Mode và mở khóa chuột khi kích hoạt.
	/// </summary>
	public void ToggleDevMode() => SetDevModeVisible(MainPanel == null || !MainPanel.Visible);

	/// <summary>
	/// Đặt trạng thái ẩn hiện của bảng Dev.
	/// </summary>
	public void SetDevModeVisible(bool isVisible)
	{
		if (MainPanel != null) MainPanel.Visible = isVisible;
		if (isVisible) Input.MouseMode = Input.MouseModeEnum.Visible;
	}

	private bool HandleToggleInput(InputEvent @event)
	{
		if (@event is InputEventKey keyEvent && keyEvent.Pressed && !keyEvent.Echo)
		{
			if (keyEvent.Keycode == ToggleKeyPrimary ||
			    keyEvent.Keycode == ToggleKeySecondary ||
			    keyEvent.Keycode == ToggleKeyTertiary)
			{
				ToggleDevMode();
				return true;
			}
		}

		if (@event is InputEventJoypadButton joyBtn && joyBtn.Pressed)
		{
			if (joyBtn.ButtonIndex == JoyButton.Back ||
			    joyBtn.ButtonIndex == JoyButton.Start ||
			    joyBtn.ButtonIndex == JoyButton.RightStick)
			{
				ToggleDevMode();
				return true;
			}
		}

		return false;
	}

	private bool HandleTabNavigationInput(InputEvent @event)
	{
		if (Tabs == null || @event is not InputEventJoypadButton joyBtn || !joyBtn.Pressed) return false;

		int tabCount = Tabs.GetTabCount();
		if (tabCount <= 1) return false;

		if (joyBtn.ButtonIndex == JoyButton.LeftShoulder)
		{
			Tabs.CurrentTab = (Tabs.CurrentTab - 1 + tabCount) % tabCount;
			return true;
		}

		if (joyBtn.ButtonIndex == JoyButton.RightShoulder)
		{
			Tabs.CurrentTab = (Tabs.CurrentTab + 1) % tabCount;
			return true;
		}

		return false;
	}

	private void LocateGameTargets()
	{
		SceneTree tree = GetTree();
		_player = (PlayerMovement?)tree.GetFirstNodeInGroup("Player") ?? (PlayerMovement?)GetParent()?.FindChild("Player");
		_npc = (SimpleNpc?)tree.GetFirstNodeInGroup("NPC") ?? (SimpleNpc?)GetParent()?.FindChild("NPC");
		_camera = (CameraFollow?)GetParent()?.FindChild("IsometricCamera") ?? (CameraFollow?)tree.Root.FindChild("IsometricCamera", true, false);
	}

	private void InitializeTabs()
	{
		if (Tabs != null)
		{
			Tabs.SetTabTitle(0, "🎮 Nhân Vật");
			Tabs.SetTabTitle(1, "💬 Hội Thoại");
			Tabs.SetTabTitle(2, "📷 Môi Trường");
		}

		PlayerTab?.Setup(_player);
		NpcTab?.Setup(_npc);
		WorldTab?.Setup(_camera, _player);

		if (CloseBtn != null) CloseBtn.Pressed += () => SetDevModeVisible(false);
	}

	private void FindControlsIfNull()
	{
		MainPanel ??= GetNodeOrNull<Control>("DevPanel");
		CloseBtn ??= GetNodeOrNull<Button>("DevPanel/VBox/HeaderBar/CloseBtn");
		Tabs ??= GetNodeOrNull<TabContainer>("DevPanel/VBox/Tabs");
		PlayerTab ??= GetNodeOrNull<DevPlayerTab>("DevPanel/VBox/Tabs/DevPlayerTab");
		NpcTab ??= GetNodeOrNull<DevNpcTab>("DevPanel/VBox/Tabs/DevNpcTab");
		WorldTab ??= GetNodeOrNull<DevWorldTab>("DevPanel/VBox/Tabs/DevWorldTab");
	}
}
