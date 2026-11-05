using Godot;

namespace Game.Player;

/// <summary>
/// Quản lý hoạt ảnh nhân vật: ưu tiên AnimationPlayer nếu có track, tự chuyển sang procedural lean/bob nếu chưa có clip.
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

	[ExportGroup("Chuyển Động Thủ Tục (Procedural)")]
	[Export] public bool ForceProcedural { get; set; } = false;
	[Export] public float LeanAmount { get; set; } = 0.15f;
	[Export] public float BobFrequency { get; set; } = 10.0f;
	[Export] public float BobAmplitude { get; set; } = 0.06f;
	[Export] public float ProceduralSmoothSpeed { get; set; } = 10.0f;

	private Vector3 _initialVisualPosition = Vector3.Zero;
	private Vector3 _initialVisualRotation = Vector3.Zero;
	private float _bobTimer;
	private const float MoveThreshold = 0.1f;
	private const float ReferenceSpeed = 6.0f;

	public override void _Ready()
	{
		ResolveReferences();
		StoreInitialVisualTransform();
	}

	public override void _Process(double delta) => UpdateAnimation((float)delta);

	/// <summary>
	/// Tự động tìm kiếm các thành phần cần thiết nếu chưa cấu hình trên Inspector.
	/// </summary>
	private void ResolveReferences()
	{
		TargetCharacter ??= GetParent() as CharacterBody3D;
		if (TargetCharacter == null) return;
		AnimPlayer ??= (AnimationPlayer?)TargetCharacter.FindChild("AnimationPlayer");
		VisualNode ??= (Node3D?)TargetCharacter.FindChild("CharacterModel") ?? (Node3D?)TargetCharacter.FindChild("Character_Armature");
	}

	/// <summary>
	/// Lưu lại vị trí và góc xoay gốc của model để làm mốc chuyển động thủ tục.
	/// </summary>
	private void StoreInitialVisualTransform()
	{
		if (VisualNode == null) return;
		_initialVisualPosition = VisualNode.Position;
		_initialVisualRotation = VisualNode.Rotation;
	}

	/// <summary>
	/// Điều phối phát animation clip có sẵn hoặc chuyển sang hoạt ảnh thủ tục.
	/// </summary>
	private void UpdateAnimation(float delta)
	{
		if (TargetCharacter == null) return;

		string animName = DetermineCurrentAnimName();
		if (!ForceProcedural && HasPlayableTracks(animName))
		{
			PlayAnimation(animName);
			ResetProcedural(delta);
			return;
		}

		ApplyProceduralAnimation(delta);
	}

	/// <summary>
	/// Xác định tên hoạt ảnh clip theo trạng thái nhân vật.
	/// </summary>
	private string DetermineCurrentAnimName()
	{
		if (!TargetCharacter!.IsOnFloor()) return JumpAnimName;
		Vector2 hVel = new Vector2(TargetCharacter.Velocity.X, TargetCharacter.Velocity.Z);
		return hVel.Length() > MoveThreshold ? WalkAnimName : IdleAnimName;
	}

	/// <summary>
	/// Phát clip hoạt ảnh qua AnimationPlayer nếu clip chưa phát.
	/// </summary>
	private void PlayAnimation(string animName)
	{
		if (AnimPlayer == null || string.IsNullOrEmpty(animName)) return;
		if (AnimPlayer.CurrentAnimation != animName) AnimPlayer.Play(animName);
	}

	/// <summary>
	/// Kiểm tra AnimationPlayer có chứa clip và có ít nhất 1 track dữ liệu hợp lệ.
	/// </summary>
	private bool HasPlayableTracks(string animName)
	{
		if (AnimPlayer == null || !AnimPlayer.HasAnimation(animName)) return false;
		Animation? anim = AnimPlayer.GetAnimation(animName);
		return anim != null && anim.GetTrackCount() > 0;
	}

	/// <summary>
	/// Áp dụng độ nghiêng (lean) và nhấp nhô (bobbing) khi chưa có track animation.
	/// </summary>
	private void ApplyProceduralAnimation(float delta)
	{
		if (VisualNode == null) return;
		Vector2 hVel = new Vector2(TargetCharacter!.Velocity.X, TargetCharacter.Velocity.Z);
		float speed = hVel.Length();

		if (!TargetCharacter.IsOnFloor())
		{
			ApplyProceduralJump(delta);
			return;
		}

		if (speed > MoveThreshold)
		{
			ApplyProceduralMove(delta, speed);
			return;
		}

		ApplyProceduralIdle(delta);
	}

	/// <summary>
	/// Hiệu ứng nghiêng mình về phía trước và nhấp nhô nhịp nhàng khi chạy.
	/// </summary>
	private void ApplyProceduralMove(float delta, float speed)
	{
		_bobTimer += delta * BobFrequency * (speed / ReferenceSpeed);
		float bobY = Mathf.Abs(Mathf.Sin(_bobTimer)) * BobAmplitude;
		Vector3 targetPos = _initialVisualPosition + new Vector3(0.0f, bobY, 0.0f);
		VisualNode!.Position = VisualNode.Position.Lerp(targetPos, ProceduralSmoothSpeed * delta);

		float tiltFactor = Mathf.Clamp(speed / ReferenceSpeed, 0.0f, 1.0f);
		float pitch = _initialVisualRotation.X - (LeanAmount * tiltFactor);
		float roll = _initialVisualRotation.Z + (Mathf.Sin(_bobTimer * 0.5f) * LeanAmount * 0.5f);

		Vector3 targetRot = VisualNode.Rotation;
		targetRot.X = Mathf.LerpAngle(targetRot.X, pitch, ProceduralSmoothSpeed * delta);
		targetRot.Z = Mathf.LerpAngle(targetRot.Z, roll, ProceduralSmoothSpeed * delta);
		VisualNode.Rotation = targetRot;
	}

	/// <summary>
	/// Hiệu ứng thở nhẹ tại chỗ khi nhân vật đứng yên.
	/// </summary>
	private void ApplyProceduralIdle(float delta)
	{
		_bobTimer += delta * 2.0f;
		float idleBob = Mathf.Sin(_bobTimer) * (BobAmplitude * 0.25f);
		Vector3 targetPos = _initialVisualPosition + new Vector3(0.0f, idleBob, 0.0f);
		VisualNode!.Position = VisualNode.Position.Lerp(targetPos, ProceduralSmoothSpeed * delta);

		Vector3 rot = VisualNode.Rotation;
		rot.X = Mathf.LerpAngle(rot.X, _initialVisualRotation.X, ProceduralSmoothSpeed * delta);
		rot.Z = Mathf.LerpAngle(rot.Z, _initialVisualRotation.Z, ProceduralSmoothSpeed * delta);
		VisualNode.Rotation = rot;
	}

	/// <summary>
	/// Hiệu ứng ngả nhẹ về phía sau khi nhảy lên không.
	/// </summary>
	private void ApplyProceduralJump(float delta)
	{
		Vector3 targetPos = _initialVisualPosition + new Vector3(0.0f, BobAmplitude * 0.5f, 0.0f);
		VisualNode!.Position = VisualNode.Position.Lerp(targetPos, ProceduralSmoothSpeed * delta);

		Vector3 rot = VisualNode.Rotation;
		rot.X = Mathf.LerpAngle(rot.X, _initialVisualRotation.X + (LeanAmount * 0.5f), ProceduralSmoothSpeed * delta);
		VisualNode.Rotation = rot;
	}

	/// <summary>
	/// Trả model về trạng thái chuẩn mượt mà khi phát Animation clip.
	/// </summary>
	private void ResetProcedural(float delta)
	{
		if (VisualNode == null) return;
		VisualNode.Position = VisualNode.Position.Lerp(_initialVisualPosition, ProceduralSmoothSpeed * delta);
		Vector3 rot = VisualNode.Rotation;
		rot.X = Mathf.LerpAngle(rot.X, _initialVisualRotation.X, ProceduralSmoothSpeed * delta);
		rot.Z = Mathf.LerpAngle(rot.Z, _initialVisualRotation.Z, ProceduralSmoothSpeed * delta);
		VisualNode.Rotation = rot;
	}
}
