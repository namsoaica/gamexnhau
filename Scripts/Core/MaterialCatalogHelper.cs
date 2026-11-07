using Godot;

namespace Game.Core;

/// <summary>
/// Lớp trợ giúp tra cứu vật liệu dùng chung và nhận diện mesh địa hình, vật thể va chạm theo TEXTURE_CATALOG.md.
/// </summary>
public static class MaterialCatalogHelper
{
	/// <summary>
	/// Kiểm tra xem mesh có phải là đạo cụ từ Map_Surroundings bị đâm xuyên/chèn vào khu vực làng mới hay không.
	/// </summary>
	public static bool IsClashingSurroundingProp(MeshInstance3D meshInstance)
	{
		if (meshInstance.Name == "Terrain_Plains_Mesh" || meshInstance.Name.ToString().Contains("Mountain")) return false;
		if (meshInstance.FindParent("Map_Surroundings") == null) return false;
		Vector3 pos = meshInstance.GlobalPosition;
		return pos.Z >= 1.0f && pos.Z <= 45.0f && Mathf.Abs(pos.X) <= 22.0f;
	}

	/// <summary>
	/// Tra cứu loại vật liệu phù hợp với tên mesh.
	/// </summary>
	public static string? MatchMaterialType(string nodeName)
	{
		string lower = nodeName.ToLower();

		if (lower.Contains("foliage") || lower.Contains("leaves")) return "Grass";
		if (lower.Contains("fire") || lower.Contains("lava") || lower.Contains("furnace_fire")) return "LavaFire";
		if (lower.Contains("mystic") || lower.Contains("potion") || lower.Contains("smoke") || lower.Contains("cauldron")) return "MysticCyan";
		if (lower.Contains("roof_alchemist") || lower.Contains("teal")) return "RoofTeal";
		if (lower.Contains("roof") || lower.Contains("mattress")) return "RoofRed";
		if (lower.Contains("cobble") || lower.Contains("chimney") || lower.Contains("furnace") || lower.Contains("oven") || lower.Contains("well_stone") || lower.Contains("hearth")) return "Cobble";
		if (lower.Contains("canopy") || lower.Contains("rug") || lower.Contains("striped")) return "Canopy";
		if (lower.Contains("metal") || lower.Contains("rail") || lower.Contains("minecart") || lower.Contains("anvil") || lower.Contains("blade") || lower.Contains("iron") || lower.Contains("sword") || lower.Contains("spear") || lower.Contains("armor")) return "Metal";
		if (lower.Contains("fence") || lower.Contains("wardrobe") || lower.Contains("chest") || lower.Contains("bookshelf")) return "WoodFence";
		if (lower.Contains("wood") || lower.Contains("log") || lower.Contains("table") || lower.Contains("bench") || lower.Contains("cart") || lower.Contains("shed") || lower.Contains("gate") || lower.Contains("beam") || lower.Contains("post") || lower.Contains("crate") || lower.Contains("barrel") || lower.Contains("bed_frame") || lower.Contains("rack") || lower.Contains("floor_house") || lower.Contains("floor_chef")) return "Wood";
		if (lower.Contains("mountains_background")) return "RockPurple";
		if (lower.Contains("rock") || lower.Contains("stone") || lower.Contains("wall") || lower.Contains("chimney") || lower.Contains("well") || lower.Contains("mine") || lower.Contains("cliff") || lower.Contains("floor") || lower.Contains("forge") || lower.Contains("oven") || lower.Contains("hearth")) return "Rock";
		if (lower.Contains("dirt") || lower.Contains("path")) return "Dirt";
		if (lower.Contains("paver") || lower.Contains("plains") || lower.Contains("grass") || lower.Contains("cabbage") || lower.Contains("vegetable") || lower.Contains("foliage") || lower.Contains("herb") || lower.Contains("bread") || lower.Contains("wheat") || lower.Contains("straw")) return "Grass";

		return null;
	}

	/// <summary>
	/// Kiểm tra mesh có phải phông nền trời cũ cần xóa hay không.
	/// </summary>
	public static bool IsSkyBackdrop(string nodeName)
	{
		string lower = nodeName.ToLower();
		return lower.Contains("sky_backdrop") || lower.Contains("backdrop") || lower.Contains("sky_plane");
	}

	/// <summary>
	/// Kiểm tra mesh có phải bề mặt đi lại hoặc chướng ngại vật cần sinh va chạm vật lý hay không.
	/// </summary>
	public static bool IsWalkableSurface(string nodeName)
	{
		string lower = nodeName.ToLower();
		return lower.Contains("terrain") || lower.Contains("stair") || lower.Contains("path") ||
		       lower.Contains("paver") || lower.Contains("fence") || lower.Contains("floor") ||
		       lower.Contains("ground") || lower.Contains("rock") || lower.Contains("mountain") ||
		       lower.Contains("cliff") || lower.Contains("overlook") || lower.Contains("gate") ||
		       lower.Contains("shed") || lower.Contains("cart") || lower.Contains("wall") ||
		       lower.Contains("chimney") || lower.Contains("well") || lower.Contains("trunk") ||
		       lower.Contains("anvil") || lower.Contains("table") || lower.Contains("furnace") ||
		       lower.Contains("oven") || lower.Contains("wardrobe") || lower.Contains("chest") ||
		       lower.Contains("barrel") || lower.Contains("crate") || lower.Contains("minecart");
	}
}
