using Godot;
using Game.Player;

namespace Game.UI;

/// <summary>
/// Quản lý giao diện tinh chỉnh thông số nhân vật trong Dev Mode (Tốc độ, Nhảy, Trọng lực, Bất tử).
/// </summary>
public partial class DevPlayerTab : VBoxContainer
{
	[Export] public HSlider? SpeedSlider { get; set; }
	[Export] public Label? SpeedValLabel { get; set; }
	[Export] public HSlider? JumpSlider { get; set; }
	[Export] public Label? JumpValLabel { get; set; }
	[Export] public HSlider? GravitySlider { get; set; }
	[Export] public Label? GravityValLabel { get; set; }
	[Export] public CheckBox? InfiniteJumpCheck { get; set; }
	[Export] public Button? RespawnBtn { get; set; }

	private PlayerMovement? _player;

	public override void _ExitTree()
	{
		DisconnectEvents();
	}

	/// <summary>
	/// Khởi tạo và đồng bộ dữ liệu người chơi với các thanh trượt và nút bấm.
	/// </summary>
	public void Setup(PlayerMovement? player)
	{
		_player = player;
		FindNodesIfNull();
		if (_player == null) return;

		SyncPlayerValues();
		ConnectEvents();
	}

	/// <summary>
	/// Tự động tìm kiếm các Control con nếu chưa được gán trên Inspector.
	/// </summary>
	private void FindNodesIfNull()
	{
		SpeedSlider ??= GetNodeOrNull<HSlider>("SpeedRow/SpeedSlider");
		SpeedValLabel ??= GetNodeOrNull<Label>("SpeedRow/SpeedVal");
		JumpSlider ??= GetNodeOrNull<HSlider>("JumpRow/JumpSlider");
		JumpValLabel ??= GetNodeOrNull<Label>("JumpRow/JumpVal");
		GravitySlider ??= GetNodeOrNull<HSlider>("GravityRow/GravitySlider");
		GravityValLabel ??= GetNodeOrNull<Label>("GravityRow/GravityVal");
		InfiniteJumpCheck ??= GetNodeOrNull<CheckBox>("InfiniteJumpCheck");
		RespawnBtn ??= GetNodeOrNull<Button>("RespawnBtn");
	}

	/// <summary>
	/// Đồng bộ giá trị hiện tại của Player lên UI.
	/// </summary>
	private void SyncPlayerValues()
	{
		if (_player == null) return;
		if (SpeedSlider != null) SpeedSlider.Value = _player.MoveSpeed;
		if (SpeedValLabel != null) SpeedValLabel.Text = $"{_player.MoveSpeed:F1}";
		if (JumpSlider != null) JumpSlider.Value = _player.JumpVelocity;
		if (JumpValLabel != null) JumpValLabel.Text = $"{_player.JumpVelocity:F1}";
		if (GravitySlider != null) GravitySlider.Value = _player.Gravity;
		if (GravityValLabel != null) GravityValLabel.Text = $"{_player.Gravity:F1}";
		if (InfiniteJumpCheck != null) InfiniteJumpCheck.ButtonPressed = _player.InfiniteJump;
	}

	/// <summary>
	/// Đăng ký lắng nghe sự kiện thay đổi từ các nút và slider.
	/// </summary>
	private void ConnectEvents()
	{
		if (SpeedSlider != null) SpeedSlider.ValueChanged += OnSpeedChanged;
		if (JumpSlider != null) JumpSlider.ValueChanged += OnJumpChanged;
		if (GravitySlider != null) GravitySlider.ValueChanged += OnGravityChanged;
		if (InfiniteJumpCheck != null) InfiniteJumpCheck.Toggled += OnInfiniteJumpToggled;
		if (RespawnBtn != null) RespawnBtn.Pressed += OnRespawnPressed;
	}

	/// <summary>
	/// Hủy đăng ký sự kiện an toàn bộ nhớ khi tab bị gỡ khỏi cây Scene.
	/// </summary>
	private void DisconnectEvents()
	{
		if (SpeedSlider != null) SpeedSlider.ValueChanged -= OnSpeedChanged;
		if (JumpSlider != null) JumpSlider.ValueChanged -= OnJumpChanged;
		if (GravitySlider != null) GravitySlider.ValueChanged -= OnGravityChanged;
		if (InfiniteJumpCheck != null) InfiniteJumpCheck.Toggled -= OnInfiniteJumpToggled;
		if (RespawnBtn != null) RespawnBtn.Pressed -= OnRespawnPressed;
	}

	private void OnSpeedChanged(double val)
	{
		if (_player == null) return;
		_player.MoveSpeed = (float)val;
		if (SpeedValLabel != null) SpeedValLabel.Text = $"{val:F1}";
	}

	private void OnJumpChanged(double val)
	{
		if (_player == null) return;
		_player.JumpVelocity = (float)val;
		if (JumpValLabel != null) JumpValLabel.Text = $"{val:F1}";
	}

	private void OnGravityChanged(double val)
	{
		if (_player == null) return;
		_player.Gravity = (float)val;
		if (GravityValLabel != null) GravityValLabel.Text = $"{val:F1}";
	}

	private void OnInfiniteJumpToggled(bool enabled)
	{
		if (_player == null) return;
		_player.InfiniteJump = enabled;
	}

	private void OnRespawnPressed()
	{
		if (_player == null) return;
		_player.TeleportTo(_player.SpawnPosition);
	}
}
