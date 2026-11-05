using Godot;

namespace Game.Core;

/// <summary>
/// Bộ điều khiển Camera Tự Do (6-DOF Free Cam) hỗ trợ bay tự do bằng Bàn phím, Chuột và Tay cầm Gamepad.
/// </summary>
public partial class FreeCameraController
{
	public float Speed { get; set; } = 15.0f;
	public float LookSensitivity { get; set; } = 0.003f;

	private float _pitch;
	private float _yaw;
	private bool _isRightMouseDown;

	public void Initialize(Camera3D camera)
	{
		_yaw = camera.Rotation.Y;
		_pitch = Mathf.Clamp(camera.Rotation.X, -Mathf.DegToRad(89.0f), Mathf.DegToRad(89.0f));
	}

	/// <summary>
	/// Xử lý sự kiện chuột cho chế độ FreeCam (giữ chuột phải để xoay góc nhìn, cuộn chuột đổi tốc độ).
	/// </summary>
	public void HandleInput(InputEvent @event)
	{
		if (@event is InputEventMouseButton mouseBtn)
		{
			HandleMouseButton(mouseBtn);
			return;
		}

		if (@event is InputEventMouseMotion mouseMotion && _isRightMouseDown)
		{
			RotateFromMouseMotion(mouseMotion);
		}
	}

	/// <summary>
	/// Cập nhật vị trí và góc quay của camera theo thời gian thực (Bàn phím, Chuột, Tay cầm).
	/// </summary>
	public void Update(Camera3D camera, float dt)
	{
		UpdateRotationFromGamepad(camera, dt);
		UpdatePosition(camera, dt);
		ApplyRotation(camera);
	}

	private void HandleMouseButton(InputEventMouseButton mouseBtn)
	{
		if (mouseBtn.ButtonIndex == MouseButton.Right)
		{
			_isRightMouseDown = mouseBtn.Pressed;
		}
		else if (mouseBtn.Pressed && mouseBtn.ButtonIndex == MouseButton.WheelUp)
		{
			Speed = Mathf.Clamp(Speed + 2.0f, 5.0f, 50.0f);
		}
		else if (mouseBtn.Pressed && mouseBtn.ButtonIndex == MouseButton.WheelDown)
		{
			Speed = Mathf.Clamp(Speed - 2.0f, 5.0f, 50.0f);
		}
	}

	private void RotateFromMouseMotion(InputEventMouseMotion motion)
	{
		_yaw -= motion.Relative.X * LookSensitivity;
		_pitch -= motion.Relative.Y * LookSensitivity;
		_pitch = Mathf.Clamp(_pitch, -Mathf.DegToRad(89.0f), Mathf.DegToRad(89.0f));
	}

	private void UpdateRotationFromGamepad(Camera3D camera, float dt)
	{
		float rightX = Input.GetJoyAxis(0, JoyAxis.RightX);
		float rightY = Input.GetJoyAxis(0, JoyAxis.RightY);

		if (Mathf.Abs(rightX) > 0.15f)
		{
			_yaw -= rightX * LookSensitivity * 400.0f * dt;
		}
		if (Mathf.Abs(rightY) > 0.15f)
		{
			_pitch -= rightY * LookSensitivity * 400.0f * dt;
			_pitch = Mathf.Clamp(_pitch, -Mathf.DegToRad(89.0f), Mathf.DegToRad(89.0f));
		}
	}

	private void UpdatePosition(Camera3D camera, float dt)
	{
		Vector3 moveDir = CalculateMoveDirection(camera);
		if (moveDir.LengthSquared() > 0.001f)
		{
			camera.GlobalPosition += moveDir.Normalized() * Speed * dt;
		}
	}

	private Vector3 CalculateMoveDirection(Camera3D camera)
	{
		Vector3 moveDir = Vector3.Zero;
		Transform3D transform = camera.GlobalTransform;

		float inputX = GetHorizontalInput();
		float inputZ = GetForwardInput();
		float inputY = GetVerticalInput();

		moveDir += -transform.Basis.Z * inputZ;
		moveDir += transform.Basis.X * inputX;
		moveDir += Vector3.Up * inputY;
		return moveDir;
	}

	private static float GetHorizontalInput()
	{
		float val = 0.0f;
		if (Input.IsKeyPressed(Key.D)) val += 1.0f;
		if (Input.IsKeyPressed(Key.A)) val -= 1.0f;

		float stickX = Input.GetJoyAxis(0, JoyAxis.LeftX);
		if (Mathf.Abs(stickX) > 0.15f) val += stickX;
		return Mathf.Clamp(val, -1.0f, 1.0f);
	}

	private static float GetForwardInput()
	{
		float val = 0.0f;
		if (Input.IsKeyPressed(Key.W)) val += 1.0f;
		if (Input.IsKeyPressed(Key.S)) val -= 1.0f;

		float stickY = -Input.GetJoyAxis(0, JoyAxis.LeftY);
		if (Mathf.Abs(stickY) > 0.15f) val += stickY;
		return Mathf.Clamp(val, -1.0f, 1.0f);
	}

	private static float GetVerticalInput()
	{
		float val = 0.0f;
		if (Input.IsKeyPressed(Key.Space) || Input.IsKeyPressed(Key.E)) val += 1.0f;
		if (Input.IsKeyPressed(Key.Ctrl) || Input.IsKeyPressed(Key.Q)) val -= 1.0f;

		if (Input.IsJoyButtonPressed(0, JoyButton.RightShoulder)) val += 1.0f;
		if (Input.IsJoyButtonPressed(0, JoyButton.LeftShoulder)) val -= 1.0f;

		float triggerR = Input.GetJoyAxis(0, JoyAxis.TriggerRight);
		float triggerL = Input.GetJoyAxis(0, JoyAxis.TriggerLeft);
		if (triggerR > 0.2f) val += triggerR;
		if (triggerL > 0.2f) val -= triggerL;

		return Mathf.Clamp(val, -1.0f, 1.0f);
	}

	private void ApplyRotation(Camera3D camera)
	{
		camera.Rotation = new Vector3(_pitch, _yaw, 0.0f);
	}
}
