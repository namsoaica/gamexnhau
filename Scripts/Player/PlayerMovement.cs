using Godot;

namespace Game.Player;

/// <summary>
/// Điều khiển chuyển động vật lý, nhảy mượt (Coyote/Buffer) và xoay hướng cho nhân vật góc nhìn Isometric.
/// </summary>
public partial class PlayerMovement : CharacterBody3D
{
	[Signal] public delegate void JumpedEventHandler();

	[ExportGroup("Thông số Vận Tốc")]
	[Export] public float MoveSpeed { get; set; } = 6.0f;
	[Export] public float Acceleration { get; set; } = 25.0f;
	[Export] public float Deceleration { get; set; } = 30.0f;
	[Export] public float JumpVelocity { get; set; } = 9.0f;
	[Export] public float Gravity { get; set; } = 20.0f;

	[ExportGroup("Hỗ Trợ Nhảy")]
	[Export] public float CoyoteTime { get; set; } = 0.15f;
	[Export] public float JumpBufferTime { get; set; } = 0.15f;
	[Export] public bool InfiniteJump { get; set; } = false;

	[ExportGroup("Xoay Hướng & Node")]
	[Export] public float RotationSpeed { get; set; } = 12.0f;
	[Export] public Node3D? VisualNode { get; set; }
	[Export] public Camera3D? ReferenceCamera { get; set; }

	public Vector3 SpawnPosition { get; private set; }

	private Vector2 _inputVector = Vector2.Zero;
	private float _coyoteTimer;
	private float _jumpBufferTimer;

	private const float MinMoveThreshold = 0.05f;
	private const float DefaultFloorSnap = 0.40f;
	private const float DefaultMaxFloorAngle = 58.0f;

	public override void _Ready()
	{
		FloorSnapLength = DefaultFloorSnap;
		FloorConstantSpeed = true;
		FloorStopOnSlope = true;
		FloorBlockOnWall = true;
		FloorMaxAngle = Mathf.DegToRad(DefaultMaxFloorAngle);
		SafeMargin = 0.08f;
		MaxSlides = 6;
		WallMinSlideAngle = Mathf.DegToRad(15.0f);
		if (!IsInGroup("Player")) AddToGroup("Player");
		VisualNode ??= (Node3D?)FindChild("Character_Armature") ?? (Node3D?)FindChild("CharacterModel");
		SpawnPosition = GlobalPosition;
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
		UpdateFloorSnap();
		MoveAndSlide();
	}

	/// <summary>
	/// Hãm dừng vận tốc ngang ngay lập tức khi vào trạng thái đặc biệt.
	/// </summary>
	public void StopHorizontalMovement() => Velocity = new Vector3(0.0f, Velocity.Y, 0.0f);

	/// <summary>
	/// Dịch chuyển nhân vật đến vị trí chỉ định và triệt tiêu toàn bộ vận tốc rơi.
	/// </summary>
	public void TeleportTo(Vector3 position)
	{
		FloorSnapLength = 0.0f;
		Velocity = Vector3.Zero;
		GlobalPosition = position;
		ResetPhysicsInterpolation();
	}

	/// <summary>
	/// Cập nhật bộ đếm thời gian cho Coyote Time và Jump Buffer.
	/// </summary>
	private void UpdateTimers(float delta)
	{
		_coyoteTimer = (IsOnFloor() || InfiniteJump) ? CoyoteTime : _coyoteTimer - delta;
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
	/// Áp dụng trọng lực mượt mà, ổn định vận tốc khi tiếp đất trên dốc.
	/// </summary>
	private void ApplyGravity(float delta)
	{
		if (IsOnFloor())
		{
			if (Velocity.Y < 0.0f) Velocity = new Vector3(Velocity.X, -0.1f, Velocity.Z);
			return;
		}

		Velocity = new Vector3(Velocity.X, Velocity.Y - (Gravity * delta), Velocity.Z);
	}

	/// <summary>
	/// Đọc vector hướng di chuyển WASD / Phím mũi tên chuẩn hóa.
	/// </summary>
	private void ReadInput() => _inputVector = Input.GetVector("move_left", "move_right", "move_forward", "move_backward");

	/// <summary>
	/// Kích hoạt nhảy khi thỏa mãn Jump Buffer và Coyote Time (tắt snap sàn tức thì).
	/// </summary>
	private void HandleJump()
	{
		if (_jumpBufferTimer <= 0.0f || _coyoteTimer <= 0.0f) return;
		_jumpBufferTimer = 0.0f;
		_coyoteTimer = 0.0f;
		FloorSnapLength = 0.0f;

		Velocity = new Vector3(Velocity.X, JumpVelocity, Velocity.Z);
		EmitSignal(SignalName.Jumped);
	}

	/// <summary>
	/// Quản lý độ bám sàn: tắt snap khi nhảy và ở trên không để tránh giật dính sàn.
	/// </summary>
	private void UpdateFloorSnap()
	{
		FloorSnapLength = (!IsOnFloor() || Velocity.Y > 0.0f) ? 0.0f : DefaultFloorSnap;
	}

	/// <summary>
	/// Tính toán vận tốc mục tiêu dựa theo góc chiếu của Camera Isometric.
	/// </summary>
	private Vector3 CalculateTargetVelocity()
	{
		Camera3D? cam = ReferenceCamera ?? GetViewport()?.GetCamera3D();
		if (cam == null) return new Vector3(_inputVector.X * MoveSpeed, 0.0f, _inputVector.Y * MoveSpeed);

		Vector3 camFwd = new Vector3(-cam.GlobalTransform.Basis.Z.X, 0.0f, -cam.GlobalTransform.Basis.Z.Z).Normalized();
		Vector3 camRight = new Vector3(cam.GlobalTransform.Basis.X.X, 0.0f, cam.GlobalTransform.Basis.X.Z).Normalized();
		return ((camRight * _inputVector.X) - (camFwd * _inputVector.Y)) * MoveSpeed;
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
		float targetAngle = Mathf.Atan2(horizontalVelocity.X, horizontalVelocity.Y);
		Vector3 currentRotation = targetNode.Rotation;

		currentRotation.Y = Mathf.LerpAngle(currentRotation.Y, targetAngle, RotationSpeed * delta);
		targetNode.Rotation = currentRotation;
	}
}
