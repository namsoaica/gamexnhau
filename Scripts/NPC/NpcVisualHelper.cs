using Godot;

namespace Game.NPC;

/// <summary>
/// Trợ lý quản lý đồ họa 2.5D, mô hình 3D và Avatar chân dung cho 8 NPC.
/// </summary>
public static class NpcVisualHelper
{
	private const string BaseTexDir = "res://Assets/Textures/NPCs";
	private const string BaseModelDir = "res://Assets/Models/NPCs";

	public static string GetSpritePath(NpcProfession profession) => profession switch
	{
		NpcProfession.Blacksmith => $"{BaseTexDir}/sprite_blacksmith.png",
		NpcProfession.Alchemist => $"{BaseTexDir}/sprite_alchemist.png",
		NpcProfession.Chef => $"{BaseTexDir}/sprite_chef.png",
		NpcProfession.Farmer => $"{BaseTexDir}/sprite_farmer.png",
		NpcProfession.Fisherman => $"{BaseTexDir}/sprite_fisherman.png",
		NpcProfession.Miner => $"{BaseTexDir}/sprite_miner.png",
		NpcProfession.Lumberjack => $"{BaseTexDir}/sprite_lumberjack.png",
		_ => $"{BaseTexDir}/sprite_guard.png"
	};

	public static string GetAvatarPath(NpcProfession profession) => profession switch
	{
		NpcProfession.Blacksmith => $"{BaseTexDir}/avatar_blacksmith.png",
		NpcProfession.Alchemist => $"{BaseTexDir}/avatar_alchemist.png",
		NpcProfession.Chef => $"{BaseTexDir}/avatar_chef.png",
		NpcProfession.Farmer => $"{BaseTexDir}/avatar_farmer.png",
		NpcProfession.Fisherman => $"{BaseTexDir}/avatar_fisherman.png",
		NpcProfession.Miner => $"{BaseTexDir}/avatar_miner.png",
		NpcProfession.Lumberjack => $"{BaseTexDir}/avatar_lumberjack.png",
		_ => $"{BaseTexDir}/avatar_guard.png"
	};

	public static string GetModelPath(NpcProfession profession) => profession switch
	{
		NpcProfession.Blacksmith => $"{BaseModelDir}/npc_blacksmith.glb",
		NpcProfession.Alchemist => $"{BaseModelDir}/npc_alchemist.glb",
		NpcProfession.Chef => $"{BaseModelDir}/npc_chef.glb",
		NpcProfession.Farmer => $"{BaseModelDir}/npc_farmer.glb",
		NpcProfession.Fisherman => $"{BaseModelDir}/npc_fisherman.glb",
		NpcProfession.Miner => $"{BaseModelDir}/npc_miner.glb",
		NpcProfession.Lumberjack => $"{BaseModelDir}/npc_lumberjack.glb",
		_ => $"{BaseModelDir}/npc_guard.glb"
	};

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
			if (img != null) return ImageTexture.CreateFromImage(img);
		}
		return null;
	}

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

	public static Texture2D? LoadAvatar(NpcProfession profession) => LoadTextureSafe(GetAvatarPath(profession));

	public static PackedScene? LoadModel(NpcProfession profession)
	{
		string path = GetModelPath(profession);
		return ResourceLoader.Exists(path) ? GD.Load<PackedScene>(path) : null;
	}

	public static void SetupVisuals(NpcBehavior npc, NpcProfession profession, bool use3DModel)
	{
		if (npc.VisualModel == null)
		{
			PackedScene? scene = LoadModel(profession);
			if (scene != null)
			{
				Node3D instance = scene.Instantiate<Node3D>();
				instance.Name = "VisualModel";
				npc.AddChild(instance);
				npc.VisualModel = instance;
			}
		}

		if (npc.NpcSprite != null) ConfigureSprite(npc.NpcSprite, profession);
		if (npc.VisualModel != null) npc.VisualModel.Visible = use3DModel;
		if (npc.NpcSprite != null) npc.NpcSprite.Visible = !use3DModel;
	}

	public static void ApplyBobbing(Node3D? model, Sprite3D? sprite, float time)
	{
		float bob = Mathf.Sin(time * 4.0f) * 0.04f;
		if (model != null) model.Position = new Vector3(model.Position.X, bob, model.Position.Z);
		if (sprite != null) sprite.Position = new Vector3(0, 0.90f + bob, 0);
	}

	public static void ResetBobbing(Node3D? model, Sprite3D? sprite)
	{
		if (model != null) model.Position = new Vector3(model.Position.X, 0, model.Position.Z);
		if (sprite != null) sprite.Position = new Vector3(0, 0.90f, 0);
	}
}
