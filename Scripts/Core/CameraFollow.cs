using Godot;

namespace Game.Core;

/// <summary>
/// Điều khiển Camera Isometric luôn bám theo nhân vật chính và hỗ trợ thu phóng mượt mà bằng con lăn chuột.
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

	/// <summary>
	/// Kích thước phóng to mục tiêu của camera (Orthographic Size).
	/// </summary>
	public float TargetZoomSize
	{
		get => _targetZoomSize;
		set => _targetZoomSize = Mathf.Clamp(value, MinZoomSize, MaxZoomSize);
	}

	private float _targetZoomSize;

	/// <summary>
	/// Khởi tạo camera, gán kích thước zoom ban đầu và tìm kiếm mục tiêu nếu cần.
	/// </summary>
	public override void _Ready()
	{
		Current = true;
		_targetZoomSize = Size;
		Target ??= (Node3D?)GetTree().GetFirstNodeInGroup("Player") ?? (Node3D?)GetParent()?.FindChild("Player");

		if (Target != null)
		{
			GlobalPosition = Target.GlobalPosition + Offset;
			LookAt(Target.GlobalPosition + LookAtOffset, Vector3.Up);
		}
	}

	/// <summary>
	/// Bắt sự kiện con lăn chuột để điều chỉnh kích thước phóng to / thu nhỏ.
	/// </summary>
	public override void _UnhandledInput(InputEvent @event)
	{
		if (@event is InputEventMouseButton mouseBtn && mouseBtn.Pressed)
		{
			HandleZoomInput(mouseBtn.ButtonIndex);
		}
	}

	/// <summary>
	/// Nội suy mượt mà kích thước phóng to / thu nhỏ theo từng khung hình hiển thị.
	/// </summary>
	public override void _Process(double delta)
	{
		if (Projection == ProjectionType.Orthogonal)
		{
			Size = Mathf.Lerp(Size, _targetZoomSize, ZoomSmoothness * (float)delta);
		}
	}

	/// <summary>
	/// Cập nhật vị trí camera mượt mà bám theo mục tiêu trong vòng lặp vật lý.
	/// </summary>
	public override void _PhysicsProcess(double delta)
	{
		if (Target == null) return;

		float dt = (float)delta;
		Vector3 targetPos = Target.GlobalPosition + Offset;
		GlobalPosition = GlobalPosition.Lerp(targetPos, SmoothSpeed * dt);
		LookAt(Target.GlobalPosition + LookAtOffset, Vector3.Up);
	}

	/// <summary>
	/// Tính toán độ phóng to mục tiêu khi cuộn con lăn chuột.
	/// </summary>
	private void HandleZoomInput(MouseButton buttonIndex)
	{
		if (buttonIndex == MouseButton.WheelUp)
		{
			_targetZoomSize = Mathf.Clamp(_targetZoomSize - ZoomSpeed, MinZoomSize, MaxZoomSize);
		}
		else if (buttonIndex == MouseButton.WheelDown)
		{
			_targetZoomSize = Mathf.Clamp(_targetZoomSize + ZoomSpeed, MinZoomSize, MaxZoomSize);
		}
	}
}
