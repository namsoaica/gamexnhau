using Godot;
using Game.Core;
using Game.Player;

namespace Game.UI;

/// <summary>
/// Tab điều khiển Môi trường, Thu phóng Camera, Chế độ Camera Tự Do (Free Cam) và Thống kê.
/// </summary>
public partial class DevWorldTab : VBoxContainer
{
	[ExportGroup("Controls Thu Phóng")]
	[Export] public HSlider? ZoomSlider { get; set; }
	[Export] public Label? ZoomValLabel { get; set; }

	[ExportGroup("Controls Camera Tự Do")]
	[Export] public CheckBox? FreeCamCheck { get; set; }
	[Export] public HSlider? FreeCamSpeedSlider { get; set; }
	[Export] public Label? FreeCamSpeedValLabel { get; set; }
	[Export] public Button? ResetCameraBtn { get; set; }
	[Export] public Label? FreeCamStatusLabel { get; set; }

	[ExportGroup("Controls Thống Kê & Nút")]
	[Export] public Label? FpsLabel { get; set; }
	[Export] public Label? PosLabel { get; set; }
	[Export] public Button? ReloadBtn { get; set; }

	private CameraFollow? _camera;
	private PlayerMovement? _player;

	public void Setup(CameraFollow? camera, PlayerMovement? player)
	{
		_camera = camera;
		_player = player;
		FindControlsIfNull();
		BindCameraValues();
		ConnectEvents();
	}

	public override void _ExitTree()
	{
		DisconnectEvents();
	}

	public void UpdateRealtimeStats()
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

		UpdateFreeCamStatusDisplay();
	}

	private void FindControlsIfNull()
	{
		ZoomSlider ??= GetNodeOrNull<HSlider>("ZoomRow/ZoomSlider");
		ZoomValLabel ??= GetNodeOrNull<Label>("ZoomRow/ZoomVal");
		FreeCamCheck ??= GetNodeOrNull<CheckBox>("FreeCamCheck");
		FreeCamSpeedSlider ??= GetNodeOrNull<HSlider>("FreeCamSpeedRow/SpeedSlider");
		FreeCamSpeedValLabel ??= GetNodeOrNull<Label>("FreeCamSpeedRow/SpeedVal");
		ResetCameraBtn ??= GetNodeOrNull<Button>("ResetCameraBtn");
		FreeCamStatusLabel ??= GetNodeOrNull<Label>("FreeCamStatusLabel");
		FpsLabel ??= GetNodeOrNull<Label>("StatsBox/FpsLabel");
		PosLabel ??= GetNodeOrNull<Label>("StatsBox/PosLabel");
		ReloadBtn ??= GetNodeOrNull<Button>("ReloadBtn");
	}

	private void BindCameraValues()
	{
		if (_camera == null) return;

		if (ZoomSlider != null)
		{
			ZoomSlider.MinValue = _camera.MinZoomSize;
			ZoomSlider.MaxValue = _camera.MaxZoomSize;
			ZoomSlider.Value = _camera.Size;
			if (ZoomValLabel != null) ZoomValLabel.Text = $"{_camera.Size:F1}";
		}

		if (FreeCamCheck != null) FreeCamCheck.ButtonPressed = _camera.IsFreeCamActive;
		if (FreeCamSpeedSlider != null)
		{
			FreeCamSpeedSlider.MinValue = 5.0f;
			FreeCamSpeedSlider.MaxValue = 50.0f;
			FreeCamSpeedSlider.Value = _camera.FreeCamSpeed;
			if (FreeCamSpeedValLabel != null) FreeCamSpeedValLabel.Text = $"{_camera.FreeCamSpeed:F1}";
		}
	}

	private void ConnectEvents()
	{
		if (ZoomSlider != null) ZoomSlider.ValueChanged += OnZoomChanged;
		if (FreeCamCheck != null) FreeCamCheck.Toggled += OnFreeCamToggled;
		if (FreeCamSpeedSlider != null) FreeCamSpeedSlider.ValueChanged += OnFreeCamSpeedChanged;
		if (ResetCameraBtn != null) ResetCameraBtn.Pressed += OnResetCameraPressed;
		if (ReloadBtn != null) ReloadBtn.Pressed += OnReloadPressed;
	}

	private void DisconnectEvents()
	{
		if (ZoomSlider != null) ZoomSlider.ValueChanged -= OnZoomChanged;
		if (FreeCamCheck != null) FreeCamCheck.Toggled -= OnFreeCamToggled;
		if (FreeCamSpeedSlider != null) FreeCamSpeedSlider.ValueChanged -= OnFreeCamSpeedChanged;
		if (ResetCameraBtn != null) ResetCameraBtn.Pressed -= OnResetCameraPressed;
		if (ReloadBtn != null) ReloadBtn.Pressed -= OnReloadPressed;
	}

	private void OnZoomChanged(double val)
	{
		if (_camera == null) return;
		_camera.TargetZoomSize = (float)val;
		if (ZoomValLabel != null) ZoomValLabel.Text = $"{val:F1}";
	}

	private void OnFreeCamToggled(bool active)
	{
		_camera?.SetFreeCamActive(active);
		UpdateFreeCamStatusDisplay();
	}

	private void OnFreeCamSpeedChanged(double val)
	{
		if (_camera == null) return;
		_camera.FreeCamSpeed = (float)val;
		if (FreeCamSpeedValLabel != null) FreeCamSpeedValLabel.Text = $"{val:F1}";
	}

	private void OnResetCameraPressed()
	{
		_camera?.ResetToPlayer();
		if (FreeCamCheck != null) FreeCamCheck.ButtonPressed = false;
		if (ZoomSlider != null && _camera != null) ZoomSlider.Value = _camera.Size;
		UpdateFreeCamStatusDisplay();
	}

	private void OnReloadPressed() => GetTree().ReloadCurrentScene();

	private void UpdateFreeCamStatusDisplay()
	{
		if (FreeCamStatusLabel == null || _camera == null) return;
		if (_camera.IsFreeCamActive)
		{
			FreeCamStatusLabel.Text = "Trạng thái: 🎥 Free Cam (Bay tự do 6-DOF)";
			FreeCamStatusLabel.Modulate = new Color(0.3f, 1.0f, 0.5f);
		}
		else
		{
			FreeCamStatusLabel.Text = "Trạng thái: 🎯 Khóa góc nhìn Isometric";
			FreeCamStatusLabel.Modulate = new Color(0.7f, 0.8f, 1.0f);
		}
	}
}
