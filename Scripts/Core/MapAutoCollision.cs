using Godot;

namespace Game.Core;

/// <summary>
/// Tự động quét gán bộ vật liệu dùng chung (Shared Materials) và tạo va chạm vật lý cho Map.
/// </summary>
public partial class MapAutoCollision : Node
{
	[ExportGroup("Cấu hình Va Chạm")]
	[Export] public bool EnableAutoCollision { get; set; } = true;

	[ExportGroup("Cấu hình Vật Liệu Dùng Chung")]
	[Export] public bool RecolorPaversToGrass { get; set; } = true;
	[Export] public string GrassTexturePath { get; set; } = "res://Assets/Models_Exported/tex_grass_clean.png";
	[Export] public string SharedMaterialsDir { get; set; } = "res://Assets/Materials_Shared/";

	private StandardMaterial3D? _matGrass;
	private StandardMaterial3D? _matDirt;
	private StandardMaterial3D? _matRock;
	private StandardMaterial3D? _matWoodFence;
	private StandardMaterial3D? _matRockMountainPurple;

	public override void _Ready()
	{
		LoadSharedMaterials();
		if (!EnableAutoCollision) return;

		Node rootNode = GetParent() ?? this;
		ScanAndProcessMeshes(rootNode);
	}

	public override void _ExitTree()
	{
		_matGrass = null;
		_matDirt = null;
		_matRock = null;
		_matWoodFence = null;
		_matRockMountainPurple = null;
	}

	/// <summary>
	/// Tải sẵn các vật liệu chuẩn dùng chung từ thư mục Assets/Materials_Shared/.
	/// </summary>
	private void LoadSharedMaterials()
	{
		_matGrass = LoadSharedMaterial($"{SharedMaterialsDir}M_Grass.tres");
		_matDirt = LoadSharedMaterial($"{SharedMaterialsDir}M_Dirt.tres");
		_matRock = LoadSharedMaterial($"{SharedMaterialsDir}M_Rock.tres");
		_matWoodFence = LoadSharedMaterial($"{SharedMaterialsDir}M_Wood_Fence.tres");
		_matRockMountainPurple = LoadSharedMaterial($"{SharedMaterialsDir}M_Rock_Mountain_Purple.tres");
	}

	/// <summary>
	/// Quét đệ quy toàn bộ cây Node để tìm và xử lý các MeshInstance3D.
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
	/// Xử lý từng mesh: xóa phông nền trời, gán vật liệu dùng chung và tạo va chạm.
	/// </summary>
	private void ProcessMeshInstance(MeshInstance3D meshInstance)
	{
		if (IsSkyBackdrop(meshInstance.Name))
		{
			meshInstance.Visible = false;
			meshInstance.QueueFree();
			return;
		}

		ApplyMaterialIfMatching(meshInstance);

		if (IsWalkableSurface(meshInstance.Name))
		{
			CreateCollisionIfMissing(meshInstance);
		}
	}

	/// <summary>
	/// Gán vật liệu dùng chung tương ứng theo phân loại tên Mesh.
	/// </summary>
	private void ApplyMaterialIfMatching(MeshInstance3D meshInstance)
	{
		StandardMaterial3D? mat = GetSharedMaterialForMesh(meshInstance.Name);
		if (mat == null) return;

		meshInstance.MaterialOverride = mat;
		GD.Print($"[MapAutoCollision] Đã gán vật liệu dùng chung cho: {meshInstance.Name}");
	}

	/// <summary>
	/// Xác định vật liệu phù hợp cho từng mesh theo quy chuẩn thư mục Shared Materials.
	/// </summary>
	private StandardMaterial3D? GetSharedMaterialForMesh(string nodeName)
	{
		string lower = nodeName.ToLower();
		if (lower.Contains("paver") || lower.Contains("plains")) return _matGrass;
		if (lower.Contains("dirt_path")) return _matDirt;
		if (lower.Contains("fence")) return _matWoodFence;
		if (lower.Contains("mountains_background")) return _matRockMountainPurple;
		if (lower.Contains("rock_boulder") || lower.Contains("rock_mesh")) return _matRock;
		return null;
	}

	/// <summary>
	/// Tạo va chạm dốc trơn cho cầu thang hoặc Trimesh có bật BackfaceCollision cho địa hình.
	/// </summary>
	private void CreateCollisionIfMissing(MeshInstance3D meshInstance)
	{
		if (meshInstance.Mesh == null || HasStaticBodyChild(meshInstance)) return;

		if (StairRampBuilder.IsStaircase(meshInstance.Name))
		{
			StairRampBuilder.BuildStairRamp(meshInstance);
			return;
		}

		meshInstance.CreateTrimeshCollision();
		EnableBackfaceCollision(meshInstance);
		GD.Print($"[MapAutoCollision] Đã tạo va chạm (BackfaceCollision bật) cho: {meshInstance.Name}");
	}

	/// <summary>
	/// Kích hoạt BackfaceCollision cho ConcavePolygonShape3D để chống rơi xuyên địa hình.
	/// </summary>
	private void EnableBackfaceCollision(Node parentNode)
	{
		foreach (Node child in parentNode.GetChildren())
		{
			if (child is CollisionShape3D colShape && colShape.Shape is ConcavePolygonShape3D concave)
			{
				concave.BackfaceCollision = true;
			}
			else if (child.GetChildCount() > 0)
			{
				EnableBackfaceCollision(child);
			}
		}
	}

	/// <summary>
	/// Tải an toàn tài nguyên StandardMaterial3D từ đường dẫn.
	/// </summary>
	private static StandardMaterial3D? LoadSharedMaterial(string path)
	{
		if (string.IsNullOrEmpty(path) || !ResourceLoader.Exists(path)) return null;
		return GD.Load<StandardMaterial3D>(path);
	}

	/// <summary>
	/// Kiểm tra Node con đã có StaticBody3D hay chưa.
	/// </summary>
	private static bool HasStaticBodyChild(Node node)
	{
		foreach (Node child in node.GetChildren())
		{
			if (child is StaticBody3D) return true;
		}
		return false;
	}

	/// <summary>
	/// Nhận diện mesh phông nền trắng cần xóa bỏ.
	/// </summary>
	private static bool IsSkyBackdrop(string nodeName)
	{
		string lower = nodeName.ToLower();
		return lower.Contains("sky_backdrop") || lower.Contains("backdrop") || lower.Contains("sky_plane");
	}

	/// <summary>
	/// Lọc tên các Mesh cần tạo va chạm tương tác cho nhân vật.
	/// </summary>
	private static bool IsWalkableSurface(string nodeName)
	{
		string lower = nodeName.ToLower();
		return lower.Contains("terrain") || lower.Contains("stair") || lower.Contains("path") ||
		       lower.Contains("paver") || lower.Contains("fence") || lower.Contains("floor") ||
		       lower.Contains("ground") || lower.Contains("rock") || lower.Contains("mountain") ||
		       lower.Contains("cliff") || lower.Contains("overlook");
	}
}
