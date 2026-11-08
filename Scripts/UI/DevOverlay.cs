using Godot;
using Game.Player;
using Game.Core;

namespace Game.UI;

/// <summary>
/// Bảng điều khiển Chế Độ Dev (Debug Overlay HUD) mở rộng hỗ trợ Bàn phím & Tay cầm Gamepad.
/// </summary>
public partial class DevOverlay : CanvasLayer
{
	public static DevOverlay? Instance { get; private set; }
	public bool IsDevModeVisible => MainPanel != null && MainPanel.Visible;

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
	[Export] public DevTeleportTab? TeleportTab { get; set; }
	[Export] public DevNpcSystemTab? NpcSystemTab { get; set; }
	[Export] public DevGraphicsTab? GraphicsTab { get; set; }

	private PlayerMovement? _player;
	private SimpleNpc? _npc;
	private CameraFollow? _camera;

	public override void _Ready()
	{
		Instance = this;
		FindControlsIfNull();
		LocateGameTargets();
		InitializeTabs();
		SetDevModeVisible(false);
	}

	public override void _ExitTree()
	{
		if (Instance == this) Instance = null;
	}

	public override void _UnhandledInput(InputEvent @event)
	{
		if (HandleToggleInput(@event))
		{
			GetViewport().SetInputAsHandled();
			return;
		}

		if (MainPanel != null && MainPanel.Visible)
		{
			if (HandleDevCancelInput(@event)) return;
			if (HandleTabNavigationInput(@event)) GetViewport().SetInputAsHandled();
		}
	}

	private bool HandleDevCancelInput(InputEvent @event)
	{
		if (@event.IsActionPressed("ui_cancel") || (@event is InputEventJoypadButton joy && joy.Pressed && joy.ButtonIndex == JoyButton.B))
		{
			SetDevModeVisible(false);
			GetViewport().SetInputAsHandled();
			return true;
		}
		return false;
	}

	public override void _Process(double delta)
	{
		if (MainPanel == null || !MainPanel.Visible) return;
		WorldTab?.UpdateRealtimeStats();
	}

	public void ToggleDevMode() => SetDevModeVisible(MainPanel == null || !MainPanel.Visible);

	public void SetDevModeVisible(bool isVisible)
	{
		if (MainPanel != null) MainPanel.Visible = isVisible;
		if (isVisible)
		{
			Input.MouseMode = Input.MouseModeEnum.Visible;
			CloseBtn?.GrabFocus();
		}
	}

	private bool HandleToggleInput(InputEvent @event)
	{
		if (@event is InputEventKey key && key.Pressed && !key.Echo)
		{
			if (key.Keycode == ToggleKeyPrimary || key.Keycode == ToggleKeySecondary || key.Keycode == ToggleKeyTertiary)
			{
				ToggleDevMode();
				return true;
			}
		}

		if (@event is InputEventJoypadButton joy && joy.Pressed)
		{
			if (joy.ButtonIndex == JoyButton.Back || joy.ButtonIndex == JoyButton.Start || joy.ButtonIndex == JoyButton.RightStick)
			{
				ToggleDevMode();
				return true;
			}
		}

		return false;
	}

	private bool HandleTabNavigationInput(InputEvent @event)
	{
		if (Tabs == null || @event is not InputEventJoypadButton joy || !joy.Pressed) return false;
		int count = Tabs.GetTabCount();
		if (count <= 1) return false;

		if (joy.ButtonIndex == JoyButton.LeftShoulder)
		{
			Tabs.CurrentTab = (Tabs.CurrentTab - 1 + count) % count;
			return true;
		}
		if (joy.ButtonIndex == JoyButton.RightShoulder)
		{
			Tabs.CurrentTab = (Tabs.CurrentTab + 1) % count;
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
		SetTabTitles();
		PlayerTab?.Setup(_player);
		NpcTab?.Setup(_npc);
		WorldTab?.Setup(_camera, _player);
		TeleportTab?.Setup(_player);
		NpcSystemTab?.Setup(_player);

		if (CloseBtn != null) CloseBtn.Pressed += () => SetDevModeVisible(false);
	}

	private void SetTabTitles()
	{
		if (Tabs == null) return;
		string[] titles = { "🎮 Player", "💬 Thoại", "📷 Camera", "🚀 Teleport", "👥 Dân Làng", "⚙️ Đồ Họa" };
		for (int i = 0; i < titles.Length && i < Tabs.GetTabCount(); i++)
		{
			Tabs.SetTabTitle(i, titles[i]);
		}
	}

	private void FindControlsIfNull()
	{
		MainPanel ??= GetNodeOrNull<Control>("DevPanel");
		CloseBtn ??= GetNodeOrNull<Button>("DevPanel/VBox/HeaderBar/CloseBtn");
		Tabs ??= GetNodeOrNull<TabContainer>("DevPanel/VBox/Tabs");
		PlayerTab ??= GetNodeOrNull<DevPlayerTab>("DevPanel/VBox/Tabs/DevPlayerTab");
		NpcTab ??= GetNodeOrNull<DevNpcTab>("DevPanel/VBox/Tabs/DevNpcTab");
		WorldTab ??= GetNodeOrNull<DevWorldTab>("DevPanel/VBox/Tabs/DevWorldTab");
		TeleportTab ??= GetNodeOrNull<DevTeleportTab>("DevPanel/VBox/Tabs/DevTeleportTab");
		NpcSystemTab ??= GetNodeOrNull<DevNpcSystemTab>("DevPanel/VBox/Tabs/DevNpcSystemTab");
		GraphicsTab ??= GetNodeOrNull<DevGraphicsTab>("DevPanel/VBox/Tabs/DevGraphicsTab");
	}
}
