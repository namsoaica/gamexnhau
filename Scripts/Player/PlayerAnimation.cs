using Godot;

namespace Game.Player;

/// <summary>
/// Quản lý phát hoạt ảnh cho nhân vật dựa trên trạng thái di chuyển của CharacterBody3D.
/// </summary>
public partial class PlayerAnimation : Node
{
	// =========================================================================
	// 1. EXPORT PROPERTIES
	// =========================================================================

	[ExportGroup("Tham Chiếu Node")]
	[Export] public CharacterBody3D? TargetCharacter { get; set; }
	[Export] public AnimationPlayer? AnimPlayer { get; set; }

	[ExportGroup("Tên Hoạt Ảnh")]
	[Export] public string IdleAnimName { get; set; } = "Idle";
	[Export] public string WalkAnimName { get; set; } = "Walk";
	[Export] public string JumpAnimName { get; set; } = "Jump";

	// =========================================================================
	// 2. CONSTANTS
	// =========================================================================

	private const float MoveThreshold = 0.2f;

	// =========================================================================
	// 3. VÒNG ĐỜI GODOT
	// =========================================================================

	public override void _Ready()
	{
		ResolveReferences();
	}

	public override void _Process(double delta)
	{
		UpdateAnimation();
	}

	// =========================================================================
	// 4. PRIVATE METHODS
	// =========================================================================

	/// <summary>
	/// Tự động tìm kiếm CharacterBody3D và AnimationPlayer nếu chưa được kéo thả.
	/// </summary>
	private void ResolveReferences()
	{
		if (TargetCharacter == null && GetParent() is CharacterBody3D parentChar)
		{
			TargetCharacter = parentChar;
		}

		if (AnimPlayer == null && TargetCharacter != null)
		{
			AnimPlayer = (AnimationPlayer?)TargetCharacter.FindChild("AnimationPlayer");
		}
	}

	/// <summary>
	/// Kiểm tra trạng thái rơi, đi bộ hoặc đứng yên để chuyển hoạt ảnh phù hợp.
	/// </summary>
	private void UpdateAnimation()
	{
		if (AnimPlayer == null || TargetCharacter == null)
		{
			return;
		}

		if (!TargetCharacter.IsOnFloor())
		{
			PlayAnimation(JumpAnimName);
			return;
		}

		float horizontalSpeed = new Vector2(TargetCharacter.Velocity.X, TargetCharacter.Velocity.Z).Length();
		if (horizontalSpeed > MoveThreshold)
		{
			PlayAnimation(WalkAnimName);
			return;
		}

		PlayAnimation(IdleAnimName);
	}

	/// <summary>
	/// Phát hoạt ảnh an toàn nếu tồn tại trên AnimationPlayer.
	/// </summary>
	private void PlayAnimation(string animName)
	{
		if (string.IsNullOrEmpty(animName))
		{
			return;
		}

		if (!AnimPlayer!.HasAnimation(animName))
		{
			return;
		}

		if (AnimPlayer.CurrentAnimation != animName)
		{
			AnimPlayer.Play(animName);
		}
	}
}
