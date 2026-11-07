using System.Collections.Generic;
using Godot;
using Game.Core;

namespace Game.Player;

/// <summary>
/// Quản lý hệ thống đòn đánh, hitbox phát hiện va chạm và hoạt ảnh tấn công cho nhân vật.
/// </summary>
public partial class PlayerCombat : Node
{
	[Signal] public delegate void AttackStartedEventHandler();
	[Signal] public delegate void AttackHitEventHandler(Node3D target, float damage);
	[Signal] public delegate void AttackFinishedEventHandler();

	[ExportGroup("Thông Số Tấn Công")]
	[Export] public float AttackDamage { get; set; } = 25.0f;
	[Export] public float AttackCooldown { get; set; } = 0.45f;
	[Export] public float AttackDuration { get; set; } = 0.35f;

	[ExportGroup("Hitbox & Tầm Đánh")]
	[Export] public Area3D? AttackArea { get; set; }
	[Export] public float HitboxForwardOffset { get; set; } = 1.1f;
	[Export] public float HitboxRadius { get; set; } = 0.9f;

	[ExportGroup("Tham Chiếu Node")]
	[Export] public CharacterBody3D? TargetCharacter { get; set; }
	[Export] public PlayerAnimation? AnimationHandler { get; set; }
	[Export] public AnimationPlayer? AnimPlayer { get; set; }
	[Export] public string AttackAnimName { get; set; } = "Attack";

	public bool IsAttacking => _isAttacking;

	private float _cooldownTimer;
	private float _attackTimer;
	private bool _isAttacking;
	private readonly HashSet<ulong> _hitTargets = new();

	public override void _Ready()
	{
		ResolveReferences();
		SetupAttackArea();
		RegisterDefaultInputs();
	}

	public override void _ExitTree()
	{
		if (AttackArea == null) return;
		AttackArea.BodyEntered -= OnBodyEntered;
		AttackArea.AreaEntered -= OnAreaEntered;
	}

	public override void _Process(double delta)
	{
		float dt = (float)delta;
		UpdateTimers(dt);
		if (CanAttack() && Input.IsActionJustPressed("attack"))
		{
			ExecuteAttack();
		}
	}

	/// <summary>
	/// Kiểm tra điều kiện cho phép thực hiện đòn đánh mới.
	/// </summary>
	public bool CanAttack()
	{
		if (_isAttacking || _cooldownTimer > 0.0f) return false;
		if (CameraFollow.Instance?.IsFreeCamActive == true) return false;
		return true;
	}

	/// <summary>
	/// Kích hoạt đòn đánh, bật hitbox quét mục tiêu và phát hoạt ảnh.
	/// </summary>
	public void ExecuteAttack()
	{
		_isAttacking = true;
		_attackTimer = AttackDuration;
		_cooldownTimer = AttackCooldown;
		_hitTargets.Clear();

		UpdateHitboxTransform();
		if (AttackArea != null) AttackArea.Monitoring = true;
		if (AnimationHandler != null) AnimationHandler.IsAttacking = true;
		if (AnimPlayer != null && AnimPlayer.HasAnimation(AttackAnimName))
		{
			AnimPlayer.Play(AttackAnimName);
		}

		EmitSignal(SignalName.AttackStarted);
	}

	/// <summary>
	/// Kết thúc đòn đánh, tắt hitbox và chuyển lại trạng thái bình thường.
	/// </summary>
	public void FinishAttack()
	{
		_isAttacking = false;
		if (AttackArea != null) AttackArea.Monitoring = false;
		if (AnimationHandler != null) AnimationHandler.IsAttacking = false;
		EmitSignal(SignalName.AttackFinished);
	}

	/// <summary>
	/// Kiểm tra và gây sát thương lên mục tiêu nếu hợp lệ.
	/// </summary>
	public void CheckHitTarget(Node3D target)
	{
		if (target == TargetCharacter || target == null) return;
		ulong id = target.GetInstanceId();
		if (_hitTargets.Contains(id)) return;

		_hitTargets.Add(id);
		if (target is IDamageable damageable)
		{
			damageable.TakeDamage(AttackDamage, TargetCharacter);
		}
		EmitSignal(SignalName.AttackHit, target, AttackDamage);
	}

	/// <summary>
	/// Tự động dò tìm các node thành phần cần thiết nếu chưa kéo thả trong Inspector.
	/// </summary>
	private void ResolveReferences()
	{
		TargetCharacter ??= GetParent() as CharacterBody3D;
		if (TargetCharacter == null) return;
		AnimationHandler ??= TargetCharacter.FindChild("PlayerAnimation") as PlayerAnimation;
		AnimPlayer ??= TargetCharacter.FindChild("AnimationPlayer") as AnimationPlayer;
	}

	/// <summary>
	/// Khởi tạo hoặc cấu hình Area3D làm vùng quét đòn đánh.
	/// </summary>
	private void SetupAttackArea()
	{
		AttackArea ??= TargetCharacter?.GetNodeOrNull<Area3D>("AttackArea") ?? (TargetCharacter?.FindChild("AttackArea", true, false) as Area3D);
		if (AttackArea == null && TargetCharacter != null)
		{
			AttackArea = new Area3D { Name = "AttackArea", Monitoring = false };
			CollisionShape3D shape = new CollisionShape3D
			{
				Shape = new SphereShape3D { Radius = HitboxRadius }
			};
			AttackArea.AddChild(shape);
			TargetCharacter.AddChild(AttackArea);
		}

		if (AttackArea == null) return;
		AttackArea.Monitoring = false;
		AttackArea.BodyEntered += OnBodyEntered;
		AttackArea.AreaEntered += OnAreaEntered;
	}

	/// <summary>
	/// Định vị vị trí hitbox theo hướng nhìn thực tế của nhân vật.
	/// </summary>
	private void UpdateHitboxTransform()
	{
		if (AttackArea == null || TargetCharacter == null) return;
		Node3D visual = TargetCharacter.FindChild("CharacterModel") as Node3D ?? TargetCharacter;
		Vector3 forward = visual.GlobalTransform.Basis.Z.Normalized();
		AttackArea.GlobalPosition = TargetCharacter.GlobalPosition + (forward * HitboxForwardOffset) + new Vector3(0, 0.8f, 0);
	}

	/// <summary>
	/// Cập nhật thời gian hồi chiêu và thời gian tồn tại của đòn đánh.
	/// </summary>
	private void UpdateTimers(float delta)
	{
		if (_cooldownTimer > 0.0f) _cooldownTimer -= delta;
		if (!_isAttacking) return;

		_attackTimer -= delta;
		if (_attackTimer <= 0.0f) FinishAttack();
	}

	/// <summary>
	/// Đăng ký phím tắt tấn công mặc định nếu chưa có trong Project Settings.
	/// </summary>
	private static void RegisterDefaultInputs()
	{
		if (InputMap.HasAction("attack")) return;
		InputMap.AddAction("attack");
		InputMap.ActionAddEvent("attack", new InputEventMouseButton { ButtonIndex = MouseButton.Left });
		InputMap.ActionAddEvent("attack", new InputEventKey { PhysicalKeycode = Key.J });
		InputMap.ActionAddEvent("attack", new InputEventJoypadButton { ButtonIndex = JoyButton.X });
	}

	private void OnBodyEntered(Node3D body) => CheckHitTarget(body);

	private void OnAreaEntered(Area3D area) => CheckHitTarget(area.GetParent() as Node3D ?? area);
}
