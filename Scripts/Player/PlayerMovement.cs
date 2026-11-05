using Godot;

namespace Game.Player;

/// <summary>
/// Điều khiển chuyển động vật lý, nhảy mượt (Coyote/Buffer) và xoay hướng cho nhân vật góc nhìn Isometric.
/// </summary>
public partial class PlayerMovement : CharacterBody3D
{
	[Signal]
	public delegate void JumpedEventHandler();

	[ExportGroup("Thông số Vận Tốc")]
	[Export] public float MoveSpeed { get; set; } = 6.0f;
	[Export] public float Acceleration { get; set; } = 25.0f;
	[Export] public float Deceleration { get; set; } = 30.0f;
	[Export] public float JumpVelocity { get; set; } = 9.0f;
	[Export] public float Gravity { get; set; } = 20.0f;

	[ExportGroup("Hỗ Trợ Nhảy")]
	[Export] public float CoyoteTime { get; set; } = 0.15f;
	[Export] public float JumpBufferTime { get; set; } = 0.15f;

	[ExportGroup("Xoay Hướng")]
	[Export] public float RotationSpeed { get; set; } = 12.0f;

	[ExportGroup("Tham Chiếu Node")]
	[Export] public Node3D? VisualNode { get; set; }
	[Export] public Camera3D? ReferenceCamera { get; set; }

	private Vector2 _inputVector = Vector2.Zero;
	private float _coyoteTimer;
	private float _jumpBufferTimer;

	private const float MinMoveThreshold = 0.05f;
	private const float DefaultFloorSnap = 0.35f;
	private const float DefaultMaxFloorAngle = 50.0f;

	public override void _Ready()
	{
		FloorSnapLength = DefaultFloorSnap;
		FloorConstantSpeed = true;
		FloorMaxAngle = Mathf.DegToRad(DefaultMaxFloorAngle);
		if (!IsInGroup("Player")) AddToGroup("Player");
		VisualNode ??= (Node3D?)FindChild("Character_Armature") ?? (Node3D?)FindChild("CharacterModel");
	}

	public override void _PhysicsProcess(double delta)
	{
		float dt = (float)delta;
		UpdateTimers(dt);
		ApplyGravity(dt);
		ReadInput();
		HandleJump();
		ApplyMovement(dt);
		ApplyRotation(dt);
		MoveAndSlide();
	}

	/// <summary>
	/// Hãm dừng vận tốc ngang ngay lập tức khi vào trạng thái đặc biệt.
	/// </summary>
	public void StopHorizontalMovement()
	{
		Vector3 currentVelocity = Velocity;
		currentVelocity.X = 0.0f;
		currentVelocity.Z = 0.0f;
		Velocity = currentVelocity;
	}

	/// <summary>
	/// Dịch chuyển nhân vật đến vị trí chỉ định và triệt tiêu toàn bộ vận tốc rơi.
	/// </summary>
	public void TeleportTo(Vector3 position)
	{
		Velocity = Vector3.Zero;
		GlobalPosition = position;
		ResetPhysicsInterpolation();
	}

	/// <summary>
	/// Cập nhật bộ đếm thời gian cho Coyote Time và Jump Buffer.
	/// </summary>
	private void UpdateTimers(float delta)
	{
		_coyoteTimer = IsOnFloor() ? CoyoteTime : _coyoteTimer - delta;
		if (Input.IsActionJustPressed("jump"))
		{
			_jumpBufferTimer = JumpBufferTime;
		}
		else if (_jumpBufferTimer > 0.0f)
		{
			_jumpBufferTimer -= delta;
		}
	}

	/// <summary>
	/// Áp dụng lực hút trọng trường khi nhân vật đang rơi trên không.
	/// </summary>
	private void ApplyGravity(float delta)
	{
		if (IsOnFloor()) return;
		Vector3 currentVelocity = Velocity;
		currentVelocity.Y -= Gravity * delta;
		Velocity = currentVelocity;
	}

	/// <summary>
	/// Đọc vector hướng di chuyển WASD / Phím mũi tên chuẩn hóa.
	/// </summary>
	private void ReadInput()
	{
		_inputVector = Input.GetVector("move_left", "move_right", "move_forward", "move_backward");
	}

	/// <summary>
	/// Kích hoạt nhảy khi thỏa mãn cả Jump Buffer và Coyote Time.
	/// </summary>
	private void HandleJump()
	{
		if (_jumpBufferTimer <= 0.0f || _coyoteTimer <= 0.0f) return;
		_jumpBufferTimer = 0.0f;
		_coyoteTimer = 0.0f;

		Vector3 currentVelocity = Velocity;
		currentVelocity.Y = JumpVelocity;
		Velocity = currentVelocity;
		EmitSignal(SignalName.Jumped);
	}

	/// <summary>
	/// Tính toán vận tốc mục tiêu dựa theo góc chiếu của Camera Isometric.
	/// </summary>
	private Vector3 CalculateTargetVelocity()
	{
		Camera3D? cam = ReferenceCamera ?? GetViewport()?.GetCamera3D();
		if (cam == null)
		{
			return new Vector3(_inputVector.X * MoveSpeed, 0.0f, _inputVector.Y * MoveSpeed);
		}

		Vector3 camForward = -cam.GlobalTransform.Basis.Z;
		camForward.Y = 0.0f;
		camForward = camForward.Normalized();

		Vector3 camRight = cam.GlobalTransform.Basis.X;
		camRight.Y = 0.0f;
		camRight = camRight.Normalized();

		Vector3 moveDirection = (camRight * _inputVector.X) - (camForward * _inputVector.Y);
		return moveDirection * MoveSpeed;
	}

	/// <summary>
	/// Tăng giảm tốc độ di chuyển ngang mượt mà.
	/// </summary>
	private void ApplyMovement(float delta)
	{
		Vector3 target = CalculateTargetVelocity();
		Vector3 currentVelocity = Velocity;
		float rate = _inputVector.LengthSquared() > MinMoveThreshold ? Acceleration : Deceleration;

		currentVelocity.X = Mathf.MoveToward(currentVelocity.X, target.X, rate * delta);
		currentVelocity.Z = Mathf.MoveToward(currentVelocity.Z, target.Z, rate * delta);
		Velocity = currentVelocity;
	}

	/// <summary>
	/// Xoay hướng mặt của nhân vật mượt mà theo vector vận tốc thực tế.
	/// </summary>
	private void ApplyRotation(float delta)
	{
		Vector2 horizontalVelocity = new Vector2(Velocity.X, Velocity.Z);
		if (horizontalVelocity.LengthSquared() < MinMoveThreshold) return;

		Node3D targetNode = VisualNode ?? this;
		float targetAngle = Mathf.Atan2(-horizontalVelocity.X, -horizontalVelocity.Y);
		Vector3 currentRotation = targetNode.Rotation;

		currentRotation.Y = Mathf.LerpAngle(currentRotation.Y, targetAngle, RotationSpeed * delta);
		targetNode.Rotation = currentRotation;
	}
}
