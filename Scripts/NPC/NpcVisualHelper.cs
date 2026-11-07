using Godot;

namespace Game.NPC;

/// <summary>
/// Trợ lý quản lý đồ họa 2.5D, Sprite3D và Avatar chân dung cho 8 NPC.
/// Hỗ trợ nạp an toàn cả khi chưa chạy Godot Editor Import (Direct Image Fallback).
/// </summary>
public static class NpcVisualHelper
{
	private const string BaseDir = "res://Assets/Textures/NPCs";

	/// <summary>
	/// Trả về đường dẫn ảnh Sprite 2.5D toàn thân theo nghề nghiệp.
	/// </summary>
	public static string GetSpritePath(NpcProfession profession)
	{
		return profession switch
		{
			NpcProfession.Blacksmith => $"{BaseDir}/sprite_blacksmith.png",
			NpcProfession.Alchemist => $"{BaseDir}/sprite_alchemist.png",
			NpcProfession.Chef => $"{BaseDir}/sprite_chef.png",
			NpcProfession.Farmer => $"{BaseDir}/sprite_farmer.png",
			NpcProfession.Fisherman => $"{BaseDir}/sprite_fisherman.png",
			NpcProfession.Miner => $"{BaseDir}/sprite_miner.png",
			NpcProfession.Lumberjack => $"{BaseDir}/sprite_lumberjack.png",
			NpcProfession.Guard => $"{BaseDir}/sprite_guard.png",
			_ => $"{BaseDir}/sprite_guard.png"
		};
	}

	/// <summary>
	/// Trả về đường dẫn ảnh Avatar chân dung theo nghề nghiệp.
	/// </summary>
	public static string GetAvatarPath(NpcProfession profession)
	{
		return profession switch
		{
			NpcProfession.Blacksmith => $"{BaseDir}/avatar_blacksmith.png",
			NpcProfession.Alchemist => $"{BaseDir}/avatar_alchemist.png",
			NpcProfession.Chef => $"{BaseDir}/avatar_chef.png",
			NpcProfession.Farmer => $"{BaseDir}/avatar_farmer.png",
			NpcProfession.Fisherman => $"{BaseDir}/avatar_fisherman.png",
			NpcProfession.Miner => $"{BaseDir}/avatar_miner.png",
			NpcProfession.Lumberjack => $"{BaseDir}/avatar_lumberjack.png",
			NpcProfession.Guard => $"{BaseDir}/avatar_guard.png",
			_ => $"{BaseDir}/avatar_guard.png"
		};
	}

	/// <summary>
	/// Nạp Texture an toàn (ưu tiên ResourceLoader, fallback Image.LoadFromFile).
	/// </summary>
	public static Texture2D? LoadTextureSafe(string resPath)
	{
		if (ResourceLoader.Exists(resPath))
		{
			var tex = GD.Load<Texture2D>(resPath);
			if (tex != null) return tex;
		}

		string absPath = ProjectSettings.GlobalizePath(resPath);
		if (System.IO.File.Exists(absPath))
		{
			var img = Image.LoadFromFile(absPath);
			if (img != null)
			{
				return ImageTexture.CreateFromImage(img);
			}
		}
		return null;
	}

	/// <summary>
	/// Cấu hình Sprite3D hiển thị chuẩn 2.5D Stylized cao 1.8m từ ảnh vẽ mẫu.
	/// </summary>
	public static void ConfigureSprite(Sprite3D sprite, NpcProfession profession)
	{
		string path = GetSpritePath(profession);
		Texture2D? texture = LoadTextureSafe(path);
		if (texture == null) return;

		sprite.Texture = texture;
		sprite.Billboard = BaseMaterial3D.BillboardModeEnum.FixedY;
		sprite.AlphaCut = SpriteBase3D.AlphaCutMode.OpaquePrepass;
		sprite.CastShadow = GeometryInstance3D.ShadowCastingSetting.DoubleSided;
		sprite.TextureFilter = BaseMaterial3D.TextureFilterEnum.LinearWithMipmaps;

		float texH = Mathf.Max(texture.GetHeight(), 100);
		sprite.PixelSize = 1.80f / texH;
		sprite.Position = new Vector3(0, 0.90f, 0);
	}

	/// <summary>
	/// Nạp Avatar chân dung của NPC.
	/// </summary>
	public static Texture2D? LoadAvatar(NpcProfession profession)
	{
		string path = GetAvatarPath(profession);
		return LoadTextureSafe(path);
	}
}
