using Godot;

namespace Game.Player;

/// <summary>
/// Quản lý hoạt ảnh nhân vật: ưu tiên AnimationPlayer nếu có track, chuyển procedural nếu chưa có clip.
/// </summary>
public partial class PlayerAnimation : Node
{
	[ExportGroup("Tham Chiếu Node")]
	[Export] public CharacterBody3D? TargetCharacter { get; set; }
	[Export] public AnimationPlayer? AnimPlayer { get; set; }
	[Export] public Node3D? VisualNode { get; set; }

	[ExportGroup("Tên Hoạt Ảnh")]
	[Export] public string IdleAnimName { get; set; } = "Idle";
	[Export] public string WalkAnimName { get; set; } = "Walk";
	[Export] public string JumpAnimName { get; set; } = "Jump";
	[Export] public string AttackAnimName { get; set; } = "Attack";

	[ExportGroup("Chuyển Động Thủ Tục")]
	[Export] public bool ForceProcedural { get; set; } = false;
	[Export] public float LeanAmount { get; set; } = 0.15f;
	[Export] public float BobFrequency { get; set; } = 10.0f;
	[Export] public float BobAmplitude { get; set; } = 0.06f;
	[Export] public float ProceduralSmoothSpeed { get; set; } = 10.0f;

	public bool IsAttacking { get; set; }

	private Vector3 _initialVisualPosition = Vector3.Zero;
	private Vector3 _initialVisualRotation = Vector3.Zero;
	private float _bobTimer;
	private const float MoveThreshold = 0.1f;
	private const float ReferenceSpeed = 6.0f;

	public override void _Ready() => ResolveReferences();
	public override void _Process(double delta) => UpdateAnimation((float)delta);

	private void ResolveReferences()
	{
		TargetCharacter ??= GetParent() as CharacterBody3D;
		if (TargetCharacter == null) return;
		AnimPlayer ??= (AnimationPlayer?)TargetCharacter.FindChild("AnimationPlayer");
		VisualNode ??= (Node3D?)TargetCharacter.FindChild("CharacterModel") ?? (Node3D?)TargetCharacter.FindChild("Character_Armature");
		if (VisualNode == null) return;
		_initialVisualPosition = VisualNode.Position;
		_initialVisualRotation = VisualNode.Rotation;
	}

	private void UpdateAnimation(float delta)
	{
		if (TargetCharacter == null) return;
		if (IsFreeCamActive())
		{
			PlayIdleState(delta);
			return;
		}

		string animName = DetermineCurrentAnimName();
		if (!ForceProcedural && HasPlayableTracks(animName))
		{
			PlayAnimation(animName);
			ResetProcedural(delta);
			return;
		}

		ApplyProceduralAnimation(delta);
	}

	private void PlayIdleState(float delta)
	{
		if (!ForceProcedural && HasPlayableTracks(IdleAnimName)) PlayAnimation(IdleAnimName);
		ResetProcedural(delta);
	}

	private string DetermineCurrentAnimName()
	{
		if (IsAttacking) return AttackAnimName;
		if (!TargetCharacter!.IsOnFloor()) return JumpAnimName;
		Vector2 hVel = new Vector2(TargetCharacter.Velocity.X, TargetCharacter.Velocity.Z);
		return hVel.Length() > MoveThreshold ? WalkAnimName : IdleAnimName;
	}

	private void PlayAnimation(string animName)
	{
		if (AnimPlayer != null && !string.IsNullOrEmpty(animName) && AnimPlayer.CurrentAnimation != animName)
		{
			AnimPlayer.Play(animName);
		}
	}

	private bool HasPlayableTracks(string animName)
	{
		if (AnimPlayer == null || !AnimPlayer.HasAnimation(animName)) return false;
		Animation? anim = AnimPlayer.GetAnimation(animName);
		return anim != null && anim.GetTrackCount() > 0;
	}

	private void ApplyProceduralAnimation(float delta)
	{
		if (VisualNode == null) return;
		if (IsAttacking)
		{
			ResetProcedural(delta);
			return;
		}
		if (!TargetCharacter!.IsOnFloor())
		{
			ApplyProceduralJump(delta);
			return;
		}

		float speed = new Vector2(TargetCharacter.Velocity.X, TargetCharacter.Velocity.Z).Length();
		if (speed > MoveThreshold) ApplyProceduralMove(delta, speed);
		else ApplyProceduralIdle(delta);
	}

	private void ApplyProceduralMove(float delta, float speed)
	{
		_bobTimer += delta * BobFrequency * (speed / ReferenceSpeed);
		float bobY = Mathf.Abs(Mathf.Sin(_bobTimer)) * BobAmplitude;
		Vector3 targetPos = _initialVisualPosition + new Vector3(0.0f, bobY, 0.0f);
		VisualNode!.Position = VisualNode.Position.Lerp(targetPos, ProceduralSmoothSpeed * delta);

		float tilt = Mathf.Clamp(speed / ReferenceSpeed, 0.0f, 1.0f);
		float pitch = _initialVisualRotation.X - (LeanAmount * tilt);
		float roll = _initialVisualRotation.Z + (Mathf.Sin(_bobTimer * 0.5f) * LeanAmount * 0.5f);
		VisualNode.Rotation = new Vector3(
			Mathf.LerpAngle(VisualNode.Rotation.X, pitch, ProceduralSmoothSpeed * delta),
			VisualNode.Rotation.Y,
			Mathf.LerpAngle(VisualNode.Rotation.Z, roll, ProceduralSmoothSpeed * delta));
	}

	private void ApplyProceduralIdle(float delta)
	{
		_bobTimer += delta * 2.0f;
		float idleBob = Mathf.Sin(_bobTimer) * (BobAmplitude * 0.25f);
		Vector3 targetPos = _initialVisualPosition + new Vector3(0.0f, idleBob, 0.0f);
		VisualNode!.Position = VisualNode.Position.Lerp(targetPos, ProceduralSmoothSpeed * delta);
		VisualNode.Rotation = new Vector3(
			Mathf.LerpAngle(VisualNode.Rotation.X, _initialVisualRotation.X, ProceduralSmoothSpeed * delta),
			VisualNode.Rotation.Y,
			Mathf.LerpAngle(VisualNode.Rotation.Z, _initialVisualRotation.Z, ProceduralSmoothSpeed * delta));
	}

	private void ApplyProceduralJump(float delta)
	{
		Vector3 targetPos = _initialVisualPosition + new Vector3(0.0f, BobAmplitude * 0.5f, 0.0f);
		VisualNode!.Position = VisualNode.Position.Lerp(targetPos, ProceduralSmoothSpeed * delta);
		VisualNode.Rotation = new Vector3(
			Mathf.LerpAngle(VisualNode.Rotation.X, _initialVisualRotation.X + (LeanAmount * 0.5f), ProceduralSmoothSpeed * delta),
			VisualNode.Rotation.Y,
			VisualNode.Rotation.Z);
	}

	private void ResetProcedural(float delta)
	{
		if (VisualNode == null) return;
		VisualNode.Position = VisualNode.Position.Lerp(_initialVisualPosition, ProceduralSmoothSpeed * delta);
		VisualNode.Rotation = new Vector3(
			Mathf.LerpAngle(VisualNode.Rotation.X, _initialVisualRotation.X, ProceduralSmoothSpeed * delta),
			VisualNode.Rotation.Y,
			Mathf.LerpAngle(VisualNode.Rotation.Z, _initialVisualRotation.Z, ProceduralSmoothSpeed * delta));
	}

	private static bool IsFreeCamActive() => Game.Core.CameraFollow.Instance?.IsFreeCamActive == true;
}
