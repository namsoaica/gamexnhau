using Godot;

namespace Game.Core;

/// <summary>
/// Tự động quét tạo va chạm vật lý (Trimesh Collision) và đồng bộ vật liệu xanh cỏ cho nền gạch trong Map.
/// </summary>
public partial class MapAutoCollision : Node
{
	[ExportGroup("Cấu hình Va Chạm")]
	[Export] public bool EnableAutoCollision { get; set; } = true;

	[ExportGroup("Cấu hình Đổi Màu Nền Gạch")]
	[Export] public bool RecolorPaversToGrass { get; set; } = true;
	[Export] public Color GrassGreenColor { get; set; } = new Color(0.35f, 0.65f, 0.25f);

	private StandardMaterial3D? _cachedPaverMaterial;

	/// <summary>
	/// Bắt đầu quét cây node cha để tự động sinh va chạm vật lý và cập nhật vật liệu.
	/// </summary>
	public override void _Ready()
	{
		if (!EnableAutoCollision) return;
		Node rootNode = GetParent() ?? this;
		ScanAndProcessMeshes(rootNode);
	}

	/// <summary>
	/// Quét đệ quy toàn bộ cây Node để tìm các MeshInstance3D phù hợp.
	/// </summary>
	private void ScanAndProcessMeshes(Node parentNode)
	{
		foreach (Node child in parentNode.GetChildren())
		{
			if (child is MeshInstance3D meshInstance)
			{
				ProcessMeshInstance(meshInstance);
			}

			if (child.GetChildCount() > 0)
			{
				ScanAndProcessMeshes(child);
			}
		}
	}

	/// <summary>
	/// Xử lý từng MeshInstance3D: áp dụng vật liệu nền cỏ và tạo va chạm nếu cần.
	/// </summary>
	private void ProcessMeshInstance(MeshInstance3D meshInstance)
	{
		if (RecolorPaversToGrass && IsPaverSurface(meshInstance.Name))
		{
			ApplyGrassMaterialToPaver(meshInstance);
		}

		if (IsWalkableSurface(meshInstance.Name))
		{
			CreateCollisionIfMissing(meshInstance);
		}
	}

	/// <summary>
	/// Áp dụng vật liệu màu xanh cỏ tươi mát cho các mesh nền gạch để đồng bộ cảnh quan.
	/// </summary>
	private void ApplyGrassMaterialToPaver(MeshInstance3D meshInstance)
	{
		_cachedPaverMaterial ??= new StandardMaterial3D
		{
			AlbedoColor = GrassGreenColor,
			Roughness = 0.85f
		};

		meshInstance.MaterialOverride = _cachedPaverMaterial;
		GD.Print($"[MapAutoCollision] Đã đổi màu xanh cỏ cho nền gạch: {meshInstance.Name}");
	}

	/// <summary>
	/// Tạo StaticBody3D kèm ConcavePolygonShape3D nếu MeshInstance3D chưa có va chạm.
	/// </summary>
	private void CreateCollisionIfMissing(MeshInstance3D meshInstance)
	{
		if (meshInstance.Mesh == null || HasStaticBodyChild(meshInstance)) return;
		meshInstance.CreateTrimeshCollision();
		GD.Print($"[MapAutoCollision] Đã tạo va chạm cho: {meshInstance.Name}");
	}

	/// <summary>
	/// Kiểm tra xem node con đã có StaticBody3D hay chưa để tránh tạo trùng lặp.
	/// </summary>
	private bool HasStaticBodyChild(Node node)
	{
		foreach (Node child in node.GetChildren())
		{
			if (child is StaticBody3D) return true;
		}
		return false;
	}

	/// <summary>
	/// Nhận diện mesh nền gạch (chứa từ khóa paver hoặc tier2_pavers).
	/// </summary>
	private bool IsPaverSurface(string nodeName)
	{
		string lower = nodeName.ToLower();
		return lower.Contains("paver") || lower.Contains("tier2_pavers");
	}

	/// <summary>
	/// Lọc tên các Mesh cần tạo bề mặt va chạm cho nhân vật đi lại hoặc cản trở chuyển động.
	/// </summary>
	private bool IsWalkableSurface(string nodeName)
	{
		string lower = nodeName.ToLower();
		return lower.Contains("terrain") ||
		       lower.Contains("stair") ||
		       lower.Contains("path") ||
		       lower.Contains("paver") ||
		       lower.Contains("fence") ||
		       lower.Contains("floor") ||
		       lower.Contains("ground") ||
		       lower.Contains("rock") ||
		       lower.Contains("mountain") ||
		       lower.Contains("cliff");
	}
}
