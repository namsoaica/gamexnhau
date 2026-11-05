using Godot;
using Game.Player;
using Game.Core;

namespace Game.UI;

/// <summary>
/// Bảng điều khiển Chế Độ Dev (Debug Overlay HUD) cho phép tinh chỉnh chỉ số nhân vật, hội thoại NPC và thế giới.
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
	[Export] public DevPlayerTab? PlayerTab { get; set; }
	[Export] public DevNpcTab? NpcTab { get; set; }
	[Export] public HSlider? ZoomSlider { get; set; }
	[Export] public Label? ZoomValLabel { get; set; }
	[Export] public Label? FpsLabel { get; set; }
	[Export] public Label? PosLabel { get; set; }
	[Export] public Button? ReloadBtn { get; set; }

	private PlayerMovement? _player;
	private SimpleNpc? _npc;
	private CameraFollow? _camera;

	public override void _Ready()
	{
		FindControlsIfNull();
		LocateGameTargets();
		InitializeSubTabs();
		SetupWorldControls();
		SetDevModeVisible(false);
	}

	public override void _ExitTree()
	{
		DisconnectWorldEvents();
	}

	public override void _UnhandledInput(InputEvent @event)
	{
		if (@event is not InputEventKey keyEvent || !keyEvent.Pressed || keyEvent.Echo) return;

		if (keyEvent.Keycode == ToggleKeyPrimary ||
			keyEvent.Keycode == ToggleKeySecondary ||
			keyEvent.Keycode == ToggleKeyTertiary)
		{
			ToggleDevMode();
			GetViewport().SetInputAsHandled();
		}
	}

	public override void _Process(double delta)
	{
		if (MainPanel == null || !MainPanel.Visible) return;
		UpdateRealtimeStats();
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

	/// <summary>
	/// Tự động dò tìm các node Gameplay trong Scene hiện tại.
	/// </summary>
	private void LocateGameTargets()
	{
		SceneTree tree = GetTree();
		_player = (PlayerMovement?)tree.GetFirstNodeInGroup("Player") ?? (PlayerMovement?)GetParent()?.FindChild("Player");
		_npc = (SimpleNpc?)tree.GetFirstNodeInGroup("NPC") ?? (SimpleNpc?)GetParent()?.FindChild("NPC");
		_camera = (CameraFollow?)GetParent()?.FindChild("IsometricCamera") ?? (CameraFollow?)tree.Root.FindChild("IsometricCamera", true, false);
	}

	/// <summary>
	/// Khởi tạo và liên kết dữ liệu cho các Tab con.
	/// </summary>
	private void InitializeSubTabs()
	{
		TabContainer? tabs = GetNodeOrNull<TabContainer>("DevPanel/VBox/Tabs");
		if (tabs != null)
		{
			tabs.SetTabTitle(0, "🎮 Nhân Vật");
			tabs.SetTabTitle(1, "💬 Hội Thoại");
			tabs.SetTabTitle(2, "📷 Môi Trường");
		}

		PlayerTab?.Setup(_player);
		NpcTab?.Setup(_npc);
	}

	/// <summary>
	/// Cấu hình giá trị ban đầu và sự kiện cho Tab Camera & Thế giới.
	/// </summary>
	private void SetupWorldControls()
	{
		if (_camera != null && ZoomSlider != null)
		{
			ZoomSlider.MinValue = _camera.MinZoomSize;
			ZoomSlider.MaxValue = _camera.MaxZoomSize;
			ZoomSlider.Value = _camera.Size;
			if (ZoomValLabel != null) ZoomValLabel.Text = $"{_camera.Size:F1}";
			ZoomSlider.ValueChanged += OnZoomChanged;
		}

		if (ReloadBtn != null) ReloadBtn.Pressed += OnReloadPressed;
		if (CloseBtn != null) CloseBtn.Pressed += () => SetDevModeVisible(false);
	}

	/// <summary>
	/// Hủy liên kết sự kiện tab Thế giới.
	/// </summary>
	private void DisconnectWorldEvents()
	{
		if (ZoomSlider != null) ZoomSlider.ValueChanged -= OnZoomChanged;
		if (ReloadBtn != null) ReloadBtn.Pressed -= OnReloadPressed;
	}

	/// <summary>
	/// Cập nhật nhãn hiển thị FPS và tọa độ Player trong thời gian thực.
	/// </summary>
	private void UpdateRealtimeStats()
	{
		if (FpsLabel != null) FpsLabel.Text = $"FPS: {Engine.GetFramesPerSecond()}";
		if (PosLabel == null) return;

		if (_player != null)
		{
			Vector3 p = _player.GlobalPosition;
			PosLabel.Text = $"Player Pos: ({p.X:F1}, {p.Y:F1}, {p.Z:F1})";
		}
		else
		{
			PosLabel.Text = "Player: (Không tìm thấy)";
		}
	}

	private void OnZoomChanged(double val)
	{
		if (_camera == null) return;
		_camera.TargetZoomSize = (float)val;
		if (ZoomValLabel != null) ZoomValLabel.Text = $"{val:F1}";
	}

	private void OnReloadPressed() => GetTree().ReloadCurrentScene();

	/// <summary>
	/// Tự động tìm kiếm các node con nếu chưa gắn trên Godot Inspector.
	/// </summary>
	private void FindControlsIfNull()
	{
		MainPanel ??= GetNodeOrNull<Control>("DevPanel");
		CloseBtn ??= GetNodeOrNull<Button>("DevPanel/VBox/HeaderBar/CloseBtn");
		PlayerTab ??= GetNodeOrNull<DevPlayerTab>("DevPanel/VBox/Tabs/DevPlayerTab");
		NpcTab ??= GetNodeOrNull<DevNpcTab>("DevPanel/VBox/Tabs/DevNpcTab");
		ZoomSlider ??= GetNodeOrNull<HSlider>("DevPanel/VBox/Tabs/DevWorldTab/ZoomRow/ZoomSlider");
		ZoomValLabel ??= GetNodeOrNull<Label>("DevPanel/VBox/Tabs/DevWorldTab/ZoomRow/ZoomVal");
		FpsLabel ??= GetNodeOrNull<Label>("DevPanel/VBox/Tabs/DevWorldTab/StatsBox/FpsLabel");
		PosLabel ??= GetNodeOrNull<Label>("DevPanel/VBox/Tabs/DevWorldTab/StatsBox/PosLabel");
		ReloadBtn ??= GetNodeOrNull<Button>("DevPanel/VBox/Tabs/DevWorldTab/ReloadBtn");
	}
}
