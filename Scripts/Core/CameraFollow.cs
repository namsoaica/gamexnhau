using Godot;

namespace Game.Core;

/// <summary>
/// Camera điều khiển góc nhìn Isometric bám theo nhân vật và hỗ trợ Chế Độ Tự Do (Free Cam).
/// </summary>
public partial class CameraFollow : Camera3D
{
	[ExportGroup("Mục Tiêu & Khoảng Cách")]
	[Export] public Node3D? Target { get; set; }
	[Export] public Vector3 Offset { get; set; } = new Vector3(-28.0f, 23.0f, 28.0f);
	[Export] public float SmoothSpeed { get; set; } = 8.0f;
	[Export] public Vector3 LookAtOffset { get; set; } = new Vector3(0.0f, 1.0f, 0.0f);

	[ExportGroup("Thu Phóng (Zoom)")]
	[Export] public float MinZoomSize { get; set; } = 8.0f;
	[Export] public float MaxZoomSize { get; set; } = 35.0f;
	[Export] public float ZoomSpeed { get; set; } = 1.5f;
	[Export] public float ZoomSmoothness { get; set; } = 10.0f;

	[ExportGroup("Camera Tự Do (Free Cam)")]
	[Export] public bool IsFreeCamActive { get; set; }
	[Export] public float FreeCamSpeed { get => _freeCam.Speed; set => _freeCam.Speed = value; }
	[Export] public float FreeCamLookSensitivity { get => _freeCam.LookSensitivity; set => _freeCam.LookSensitivity = value; }

	public static CameraFollow? Instance { get; private set; }

	public float TargetZoomSize
	{
		get => _targetZoomSize;
		set => _targetZoomSize = Mathf.Clamp(value, MinZoomSize, MaxZoomSize);
	}

	private readonly FreeCameraController _freeCam = new();
	private float _targetZoomSize;
	private ProjectionType _savedProjection = ProjectionType.Orthogonal;

	public override void _Ready()
	{
		Instance = this;
		Current = true;
		_targetZoomSize = Size;
		_savedProjection = Projection;
		LocatePlayerTarget();
		SnapToTarget();
	}

	public override void _ExitTree()
	{
		if (Instance == this) Instance = null;
	}

	public override void _UnhandledInput(InputEvent @event)
	{
		if (IsFreeCamActive)
		{
			_freeCam.HandleInput(@event);
			return;
		}

		if (@event is InputEventMouseButton mouseBtn && mouseBtn.Pressed)
		{
			HandleIsometricZoomInput(mouseBtn.ButtonIndex);
		}
	}

	public override void _Process(double delta)
	{
		float dt = (float)delta;
		if (IsFreeCamActive)
		{
			_freeCam.Update(this, dt);
			return;
		}

		UpdateIsometricZoom(dt);
	}

	public override void _PhysicsProcess(double delta)
	{
		if (IsFreeCamActive || Target == null) return;

		float dt = (float)delta;
		Vector3 targetPos = Target.GlobalPosition + Offset;
		GlobalPosition = GlobalPosition.Lerp(targetPos, SmoothSpeed * dt);
		LookAt(Target.GlobalPosition + LookAtOffset, Vector3.Up);
	}

	/// <summary>
	/// Bật hoặc tắt Chế Độ Camera Tự Do (Free Cam).
	/// </summary>
	public void SetFreeCamActive(bool active)
	{
		if (IsFreeCamActive == active) return;
		IsFreeCamActive = active;

		if (active)
		{
			_savedProjection = Projection;
			Projection = ProjectionType.Perspective;
			Fov = 75.0f;
			_freeCam.Initialize(this);
		}
		else
		{
			Projection = _savedProjection;
			Size = _targetZoomSize;
			ResetToPlayer();
		}
	}

	/// <summary>
	/// Đưa Camera quay lại bám theo nhân vật chính ở góc nhìn mặc định.
	/// </summary>
	public void ResetToPlayer()
	{
		if (IsFreeCamActive) SetFreeCamActive(false);
		SnapToTarget();
	}

	private void LocatePlayerTarget()
	{
		Target ??= (Node3D?)GetTree().GetFirstNodeInGroup("Player") ?? (Node3D?)GetParent()?.FindChild("Player");
	}

	private void SnapToTarget()
	{
		if (Target == null) return;
		GlobalPosition = Target.GlobalPosition + Offset;
		LookAt(Target.GlobalPosition + LookAtOffset, Vector3.Up);
	}

	private void UpdateIsometricZoom(float dt)
	{
		HandleGamepadZoom(dt);
		if (Projection == ProjectionType.Orthogonal)
		{
			Size = Mathf.Lerp(Size, _targetZoomSize, ZoomSmoothness * dt);
		}
	}

	private void HandleIsometricZoomInput(MouseButton buttonIndex)
	{
		if (buttonIndex == MouseButton.WheelUp)
		{
			TargetZoomSize -= ZoomSpeed;
		}
		else if (buttonIndex == MouseButton.WheelDown)
		{
			TargetZoomSize += ZoomSpeed;
		}
	}

	private void HandleGamepadZoom(float dt)
	{
		float rightY = Input.GetJoyAxis(0, JoyAxis.RightY);
		if (Mathf.Abs(rightY) > 0.25f)
		{
			TargetZoomSize += rightY * ZoomSpeed * 4.0f * dt;
		}
	}
}
