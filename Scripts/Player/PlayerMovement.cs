using Godot;

namespace Game.Player;

/// <summary>
/// Điều khiển chuyển động vật lý và xoay hướng cho nhân vật (hỗ trợ cả 2.5D Side-Scroller và Isometric/3D).
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

	[ExportGroup("Cấu hình Góc Nhìn")]
	[Export] public bool IsSideScroller { get; set; } = false;
	[Export] public float RotationSpeed { get; set; } = 12.0f;

	[ExportGroup("Tham Chiếu Node")]
	[Export] public Node3D? VisualNode { get; set; }
	[Export] public Camera3D? ReferenceCamera { get; set; }

	private Vector2 _inputDirection = Vector2.Zero;
	private const float MinMoveThreshold = 0.05f;

	public override void _Ready()
	{
		FloorSnapLength = 0.35f;
		FloorConstantSpeed = true;
		FloorMaxAngle = Mathf.DegToRad(50.0f);

		VisualNode ??= (Node3D?)FindChild("Character_Armature") ?? (Node3D?)FindChild("CharacterModel");
	}

	public override void _PhysicsProcess(double delta)
	{
		float dt = (float)delta;

		ApplyGravity(dt);
		ReadInputDirection();
		HandleJump();
		ApplyMovement(dt);
		ApplyRotation(dt);

		MoveAndSlide();
	}

	/// <summary>
	/// Hãm dừng vận tốc di chuyển ngang từ bên ngoài (khi tấn công hoặc choáng).
	/// </summary>
	public void StopHorizontalMovement()
	{
		Vector3 currentVelocity = Velocity;
		currentVelocity.X = 0.0f;
		currentVelocity.Z = 0.0f;
		Velocity = currentVelocity;
	}

	/// <summary>
	/// Áp dụng trọng lực kéo nhân vật rơi xuống khi ở trên không.
	/// </summary>
	private void ApplyGravity(float delta)
	{
		if (IsOnFloor()) return;

		Vector3 currentVelocity = Velocity;
		currentVelocity.Y -= Gravity * delta;
		Velocity = currentVelocity;
	}

	/// <summary>
	/// Đọc vector hướng di chuyển từ bàn phím (WASD hoặc phím mũi tên).
	/// </summary>
	private void ReadInputDirection()
	{
		float horizontal = 0.0f;
		float vertical = 0.0f;

		if (IsActionPressed("move_left", Key.A, Key.Left)) horizontal -= 1.0f;
		if (IsActionPressed("move_right", Key.D, Key.Right)) horizontal += 1.0f;
		if (IsActionPressed("move_forward", Key.W, Key.Up)) vertical -= 1.0f;
		if (IsActionPressed("move_backward", Key.S, Key.Down)) vertical += 1.0f;

		Vector2 rawInput = new Vector2(horizontal, vertical);
		_inputDirection = rawInput.LengthSquared() > 1.0f ? rawInput.Normalized() : rawInput;
	}

	/// <summary>
	/// Thực hiện nhảy khi ấn phím và nhân vật đang ở trên mặt sàn.
	/// </summary>
	private void HandleJump()
	{
		if (!IsOnFloor()) return;

		bool jumpPressed = IsActionPressed("jump", Key.Space, Key.Space);
		if (!jumpPressed) return;

		Vector3 currentVelocity = Velocity;
		currentVelocity.Y = JumpVelocity;
		Velocity = currentVelocity;

		EmitSignal(SignalName.Jumped);
	}

	/// <summary>
	/// Gia tốc vận tốc ngang theo hướng điều khiển.
	/// </summary>
	private void ApplyMovement(float delta)
	{
		Vector3 target = CalculateTargetVelocity();
		Vector3 currentVelocity = Velocity;

		float rate = _inputDirection.LengthSquared() > MinMoveThreshold ? Acceleration : Deceleration;

		currentVelocity.X = Mathf.MoveToward(currentVelocity.X, target.X, rate * delta);
		currentVelocity.Z = Mathf.MoveToward(currentVelocity.Z, target.Z, rate * delta);

		Velocity = currentVelocity;
	}

	/// <summary>
	/// Tính vector vận tốc đích theo góc nhìn màn hình hoặc Camera Isometric.
	/// </summary>
	private Vector3 CalculateTargetVelocity()
	{
		if (IsSideScroller)
		{
			return new Vector3(_inputDirection.X * MoveSpeed, 0.0f, 0.0f);
		}

		Camera3D? cam = ReferenceCamera ?? GetViewport()?.GetCamera3D();
		if (cam == null)
		{
			return new Vector3(_inputDirection.X * MoveSpeed, 0.0f, _inputDirection.Y * MoveSpeed);
		}

		Vector3 camForward = -cam.GlobalTransform.Basis.Z;
		camForward.Y = 0.0f;
		camForward = camForward.Normalized();

		Vector3 camRight = cam.GlobalTransform.Basis.X;
		camRight.Y = 0.0f;
		camRight = camRight.Normalized();

		Vector3 moveDir = (camRight * _inputDirection.X) - (camForward * _inputDirection.Y);
		return moveDir * MoveSpeed;
	}

	/// <summary>
	/// Xoay hướng mặt nhân vật theo hướng chuyển động.
	/// </summary>
	private void ApplyRotation(float delta)
	{
		Node3D? targetNode = VisualNode ?? this;

		if (IsSideScroller)
		{
			RotateSideScroller(targetNode, delta);
			return;
		}

		RotateIsometric(targetNode, delta);
	}

	/// <summary>
	/// Xoay mặt trái/phải theo trục X trong chế độ 2.5D Side-Scroller.
	/// </summary>
	private void RotateSideScroller(Node3D node, float delta)
	{
		if (Mathf.Abs(_inputDirection.X) < MinMoveThreshold) return;

		float targetAngle = _inputDirection.X > 0 ? Mathf.DegToRad(90.0f) : Mathf.DegToRad(-90.0f);
		Vector3 currentRotation = node.Rotation;
		currentRotation.Y = Mathf.LerpAngle(currentRotation.Y, targetAngle, RotationSpeed * delta);
		node.Rotation = currentRotation;
	}

	/// <summary>
	/// Xoay mặt theo hướng vận tốc di chuyển trong chế độ Isometric/3D.
	/// </summary>
	private void RotateIsometric(Node3D node, float delta)
	{
		Vector2 horizontalVel = new Vector2(Velocity.X, Velocity.Z);
		if (horizontalVel.LengthSquared() < MinMoveThreshold) return;

		float targetAngle = Mathf.Atan2(horizontalVel.X, horizontalVel.Y);
		Vector3 currentRotation = node.Rotation;
		currentRotation.Y = Mathf.LerpAngle(currentRotation.Y, targetAngle, RotationSpeed * delta);
		node.Rotation = currentRotation;
	}

	/// <summary>
	/// Kiểm tra hành động từ InputMap hoặc phím vật lý dự phòng.
	/// </summary>
	private bool IsActionPressed(string actionName, Key key1, Key key2)
	{
		if (InputMap.HasAction(actionName) && Input.IsActionPressed(actionName))
		{
			return true;
		}

		return Input.IsKeyPressed(key1) || Input.IsKeyPressed(key2);
	}
}
