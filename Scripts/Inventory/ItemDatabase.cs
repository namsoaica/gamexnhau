using System.Collections.Generic;

namespace Game.Inventory;

/// <summary>
/// Cơ sở dữ liệu danh mục vật phẩm chuẩn trong game làng 2.5D.
/// </summary>
public static class ItemDatabase
{
	private const string IconDir = "res://Assets/Textures/Items/";

	private static readonly Dictionary<string, InventoryItem> Items = new()
	{
		["baguette"] = new()
		{
			Id = "baguette",
			Name = "Bánh Mì Baguette",
			Description = "Ổ bánh mì nướng vỏ giòn ruột xốp thơm phức, hồi phục thể lực và sinh lực tức thì.",
			IconPath = $"{IconDir}icon_baguette.png",
			Type = ItemType.Consumable,
			MaxStack = 20
		},
		["potion_health"] = new()
		{
			Id = "potion_health",
			Name = "Bình Máu Đỏ",
			Description = "Dược dịch thảo mộc đỏ tinh luyện, hồi phục ngay 50 Điểm Sinh Lực (HP).",
			IconPath = $"{IconDir}icon_potion_health.png",
			Type = ItemType.Consumable,
			MaxStack = 10
		},
		["potion_speed"] = new()
		{
			Id = "potion_speed",
			Name = "Bình Tăng Tốc",
			Description = "Dược dịch ngọc bích lấp lánh gió bão, tăng +30% tốc độ di chuyển trong 15 giây.",
			IconPath = $"{IconDir}icon_potion_speed.png",
			Type = ItemType.Consumable,
			MaxStack = 10
		},
		["iron_ore"] = new()
		{
			Id = "iron_ore",
			Name = "Quặng Sắt",
			Description = "Khoáng sản quặng sắt thô khai thác từ vách đá mỏ ngầm, dùng để rèn kiếm và khiên.",
			IconPath = $"{IconDir}icon_iron_ore.png",
			Type = ItemType.Material,
			MaxStack = 99
		},
		["wood_log"] = new()
		{
			Id = "wood_log",
			Name = "Gỗ Sồi Cắt Xẻ",
			Description = "Thân cây sồi già đốn từ rừng Tây Bắc, thớ gỗ chắc nịch dùng để gia cố cửa và đồ đạc.",
			IconPath = $"{IconDir}icon_wood_log.png",
			Type = ItemType.Material,
			MaxStack = 99
		},
		["herb"] = new()
		{
			Id = "herb",
			Name = "Thảo Mộc Xanh",
			Description = "Cỏ dược liệu xanh tươi đọng sương sớm, nguyên liệu cốt lõi nấu nước thần.",
			IconPath = $"{IconDir}icon_herb.png",
			Type = ItemType.Material,
			MaxStack = 99
		},
		["cabbage"] = new()
		{
			Id = "cabbage",
			Name = "Bắp Cải Tươi",
			Description = "Bắp cải giòn ngọt vừa hái từ vườn rau George, dùng nấu súp hầm ngon ngọt.",
			IconPath = $"{IconDir}icon_cabbage.png",
			Type = ItemType.Material,
			MaxStack = 50
		},
		["fish"] = new()
		{
			Id = "fish",
			Name = "Cá Suối Tươi",
			Description = "Cá sông vảy bạc tươi rói quẫy đuôi bắt bởi Finn dưới thác nước.",
			IconPath = $"{IconDir}icon_fish.png",
			Type = ItemType.Material,
			MaxStack = 50
		},
		["key"] = new()
		{
			Id = "key",
			Name = "Chìa Khóa Cổ",
			Description = "Chìa khóa chạm khắc hoa văn cổ của Trưởng Làng, dùng mở các cánh cổng khóa kín.",
			IconPath = $"{IconDir}icon_key.png",
			Type = ItemType.KeyItem,
			MaxStack = 1
		}
	};

	/// <summary>
	/// Lấy bản sao của vật phẩm theo mã định danh.
	/// </summary>
	public static InventoryItem? CreateItem(string id, int quantity = 1)
	{
		if (!Items.TryGetValue(id, out InventoryItem? template)) return null;
		return template.Clone(quantity);
	}
}
