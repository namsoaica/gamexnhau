using Godot;

namespace Game.Core;

/// <summary>
/// Vùng chuyển đổi nội thất cho từng công trình trong làng (Building Interior Area).
/// Kế thừa InteriorZone để cung cấp cấu hình zoom cận cảnh 9.5f và góc nhìn diorama thông thoáng.
/// </summary>
public partial class BuildingInteriorArea : InteriorZone
{
	[ExportGroup("Cấu hình Tên Tòa Nhà")]
	[Export] public string BuildingName { get; set; } = "Công Trình";

	public override void _Ready()
	{
		InteriorCameraZoom = 9.5f;
		ExteriorCameraZoom = 17.5f;
		base._Ready();
		BuildingInteriorManager.Instance?.RegisterArea(this);
	}

	public override void _ExitTree()
	{
		BuildingInteriorManager.Instance?.UnregisterArea(this);
		base._ExitTree();
	}

	protected override void OnBodyEntered(Node3D body)
	{
		base.OnBodyEntered(body);
		if (!IsPlayerBody(body)) return;
		Vector3 roomCenter = GlobalPosition + RoomCenterOffset;
		CameraFollow.Instance?.SetInteriorFocus(roomCenter, InteriorCameraZoom);
		BuildingInteriorManager.Instance?.NotifyBuildingEntered(this);
	}

	protected override void OnBodyExited(Node3D body)
	{
		base.OnBodyExited(body);
		if (!IsPlayerBody(body)) return;
		CameraFollow.Instance?.SetInteriorFocus(null, null);
		if (CameraFollow.Instance != null && ExteriorCameraZoom > 0f)
		{
			CameraFollow.Instance.TargetZoomSize = ExteriorCameraZoom;
		}
		BuildingInteriorManager.Instance?.NotifyBuildingExited(this);
	}
}
