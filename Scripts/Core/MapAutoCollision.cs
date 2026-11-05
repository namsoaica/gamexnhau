using Godot;

namespace Game.Core;

/// <summary>
/// Tự động quét tạo va chạm vật lý (Trimesh / Stair Ramp), loại bỏ phông trắng và đồng bộ cỏ xanh cho Map.
/// </summary>
public partial class MapAutoCollision : Node
{
	[ExportGroup("Cấu hình Va Chạm")]
	[Export] public bool EnableAutoCollision { get; set; } = true;

	[ExportGroup("Cấu hình Đổi Màu Nền Cỏ")]
	[Export] public bool RecolorPaversToGrass { get; set; } = true;
	[Export] public Color PaverAlbedoColor { get; set; } = Colors.White;
	[Export] public string GrassTexturePath { get; set; } = "res://Assets/Models_Exported/tex_grass_grid.png";

	private StandardMaterial3D? _cachedPaverMaterial;

	public override void _Ready()
	{
		if (!EnableAutoCollision) return;
		Node rootNode = GetParent() ?? this;
		ScanAndProcessMeshes(rootNode);
	}

	public override void _ExitTree()
	{
		_cachedPaverMaterial = null;
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
	/// Xử lý từng MeshInstance3D: xóa phông nền trắng, phủ vật liệu cỏ và tạo va chạm nếu cần.
	/// </summary>
	private void ProcessMeshInstance(MeshInstance3D meshInstance)
	{
		if (IsSkyBackdrop(meshInstance.Name))
		{
			meshInstance.Visible = false;
			meshInstance.QueueFree();
			return;
		}

		if (RecolorPaversToGrass && ShouldRecolorToGrass(meshInstance.Name))
		{
			ApplyGrassMaterial(meshInstance);
		}

		if (IsWalkableSurface(meshInstance.Name))
		{
			CreateCollisionIfMissing(meshInstance);
		}
	}

	/// <summary>
	/// Áp dụng vật liệu cỏ đồng bộ texture cho các mesh nền gạch và đồng bằng.
	/// </summary>
	private void ApplyGrassMaterial(MeshInstance3D meshInstance)
	{
		meshInstance.MaterialOverride = GetOrCreatePaverMaterial();
		GD.Print($"[MapAutoCollision] Đã đồng bộ texture cỏ cho: {meshInstance.Name}");
	}

	/// <summary>
	/// Tạo hoặc trả về vật liệu cỏ với texture đồng bộ cho nền đất và gạch.
	/// </summary>
	private StandardMaterial3D GetOrCreatePaverMaterial()
	{
		if (_cachedPaverMaterial != null) return _cachedPaverMaterial;

		Texture2D? grassTex = LoadGrassTexture();
		_cachedPaverMaterial = new StandardMaterial3D
		{
			AlbedoColor = PaverAlbedoColor,
			AlbedoTexture = grassTex,
			TextureFilter = BaseMaterial3D.TextureFilterEnum.LinearWithMipmaps,
			Roughness = 0.85f
		};
		return _cachedPaverMaterial;
	}

	/// <summary>
	/// Tải texture cỏ từ đường dẫn cấu hình hoặc texture dự phòng.
	/// </summary>
	private Texture2D? LoadGrassTexture()
	{
		if (ResourceLoader.Exists(GrassTexturePath)) return GD.Load<Texture2D>(GrassTexturePath);
		const string fallback = "res://Assets/Models_Exported/map_25d_Tex_Grass_Grid.png";
		return ResourceLoader.Exists(fallback) ? GD.Load<Texture2D>(fallback) : null;
	}

	/// <summary>
	/// Tạo va chạm phù hợp: dốc phẳng trơn cho cầu thang, hoặc Trimesh cho địa hình.
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
	/// Bật BackfaceCollision cho ConcavePolygonShape3D để chống lọt mép, rìa bậc thềm.
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
	/// Kiểm tra xem node con đã có StaticBody3D hay chưa để tránh tạo trùng lặp.
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
	/// Nhận diện mesh phông nền trắng cần xóa bỏ để lộ bầu trời xanh ProceduralSky.
	/// </summary>
	private static bool IsSkyBackdrop(string nodeName)
	{
		string lower = nodeName.ToLower();
		return lower.Contains("sky_backdrop") || lower.Contains("backdrop") || lower.Contains("sky_plane");
	}

	/// <summary>
	/// Nhận diện mesh cần đổi sang cỏ xanh (gạch paver hoặc cánh đồng plains).
	/// </summary>
	private static bool ShouldRecolorToGrass(string nodeName)
	{
		string lower = nodeName.ToLower();
		return lower.Contains("paver") || lower.Contains("tier2_pavers") || lower.Contains("plains");
	}

	/// <summary>
	/// Lọc tên các Mesh cần tạo bề mặt va chạm cho nhân vật đi lại hoặc cản trở chuyển động.
	/// </summary>
	private static bool IsWalkableSurface(string nodeName)
	{
		string lower = nodeName.ToLower();
		return lower.Contains("terrain") || lower.Contains("stair") || lower.Contains("path") ||
		       lower.Contains("paver") || lower.Contains("fence") || lower.Contains("floor") ||
		       lower.Contains("ground") || lower.Contains("rock") || lower.Contains("mountain") ||
		       lower.Contains("cliff");
	}
}
