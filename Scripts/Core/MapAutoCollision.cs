using Godot;

namespace Game.Core;

/// <summary>
/// Tự động quét gán bộ vật liệu dùng chung (Shared Materials) và tạo va chạm vật lý cho Map & Làng.
/// </summary>
public partial class MapAutoCollision : Node
{
	[ExportGroup("Cấu hình Va Chạm")]
	[Export] public bool EnableAutoCollision { get; set; } = true;

	[ExportGroup("Cấu hình Thư Mục Vật Liệu")]
	[Export] public string GrassTexturePath { get; set; } = "res://Assets/Models_Exported/tex_grass_clean.png";
	[Export] public string SharedMaterialsDir { get; set; } = "res://Assets/Materials_Shared/";

	private StandardMaterial3D? _matGrass;
	private StandardMaterial3D? _matDirt;
	private StandardMaterial3D? _matRock;
	private StandardMaterial3D? _matWood;
	private StandardMaterial3D? _matWoodFence;
	private StandardMaterial3D? _matMetal;
	private StandardMaterial3D? _matRockMountainPurple;
	private StandardMaterial3D? _matRoofRed;
	private StandardMaterial3D? _matRoofTeal;
	private StandardMaterial3D? _matCanopy;
	private StandardMaterial3D? _matMysticCyan;
	private StandardMaterial3D? _matLavaFire;

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
		_matWood = null;
		_matWoodFence = null;
		_matMetal = null;
		_matRockMountainPurple = null;
		_matRoofRed = null;
		_matRoofTeal = null;
		_matCanopy = null;
		_matMysticCyan = null;
		_matLavaFire = null;
	}

	private void LoadSharedMaterials()
	{
		_matGrass = LoadSharedMaterial($"{SharedMaterialsDir}M_Grass.tres");
		_matDirt = LoadSharedMaterial($"{SharedMaterialsDir}M_Dirt.tres");
		_matRock = LoadSharedMaterial($"{SharedMaterialsDir}M_Rock.tres");
		_matWood = LoadSharedMaterial($"{SharedMaterialsDir}M_Wood.tres");
		_matWoodFence = LoadSharedMaterial($"{SharedMaterialsDir}M_Wood_Fence.tres");
		_matMetal = LoadSharedMaterial($"{SharedMaterialsDir}M_Metal.tres");
		_matRockMountainPurple = LoadSharedMaterial($"{SharedMaterialsDir}M_Rock_Mountain_Purple.tres");
		_matRoofRed = LoadSharedMaterial($"{SharedMaterialsDir}M_Roof_Tiles_Red.tres");
		_matRoofTeal = LoadSharedMaterial($"{SharedMaterialsDir}M_Roof_Tiles_Teal.tres");
		_matCanopy = LoadSharedMaterial($"{SharedMaterialsDir}M_Canopy_Striped.tres");
		_matMysticCyan = LoadSharedMaterial($"{SharedMaterialsDir}M_Mystic_Cyan.tres");
		_matLavaFire = LoadSharedMaterial($"{SharedMaterialsDir}M_Lava_Fire.tres");
	}

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

	private void ProcessMeshInstance(MeshInstance3D meshInstance)
	{
		if (MaterialCatalogHelper.IsSkyBackdrop(meshInstance.Name))
		{
			meshInstance.Visible = false;
			meshInstance.QueueFree();
			return;
		}

		if (MaterialCatalogHelper.IsClashingSurroundingProp(meshInstance))
		{
			meshInstance.Visible = false;
			meshInstance.QueueFree();
			return;
		}

		ApplyMaterialIfMatching(meshInstance);

		if (MaterialCatalogHelper.IsWalkableSurface(meshInstance.Name))
		{
			CreateCollisionIfMissing(meshInstance);
		}
	}

	private void ApplyMaterialIfMatching(MeshInstance3D meshInstance)
	{
		string? matType = MaterialCatalogHelper.MatchMaterialType(meshInstance.Name);
		if (matType == null) return;

		StandardMaterial3D? mat = matType switch
		{
			"LavaFire" => _matLavaFire,
			"MysticCyan" => _matMysticCyan,
			"RoofTeal" => _matRoofTeal,
			"RoofRed" => _matRoofRed,
			"Canopy" => _matCanopy,
			"Metal" => _matMetal,
			"WoodFence" => _matWoodFence,
			"Wood" => _matWood,
			"RockPurple" => _matRockMountainPurple,
			"Rock" => _matRock,
			"Dirt" => _matDirt,
			"Grass" => _matGrass,
			_ => null
		};

		if (mat != null) meshInstance.MaterialOverride = mat;
	}

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
	}

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

	private static StandardMaterial3D? LoadSharedMaterial(string path)
	{
		if (string.IsNullOrEmpty(path) || !ResourceLoader.Exists(path)) return null;
		return GD.Load<StandardMaterial3D>(path);
	}

	private static bool HasStaticBodyChild(Node node)
	{
		foreach (Node child in node.GetChildren())
		{
			if (child is StaticBody3D) return true;
		}
		return false;
	}
}
