using Godot;

namespace Game.Inventory;

/// <summary>
/// Phân loại nhóm vật phẩm trong hệ thống túi đồ.
/// </summary>
public enum ItemType
{
	Consumable, // Vật phẩm tiêu hao (bánh mì, dược dịch)
	Material,   // Nguyên vật liệu chế tác (gỗ, quặng sắt, thảo mộc, cá, bắp cải)
	KeyItem     // Vật phẩm nhiệm vụ quan trọng (chìa khóa)
}

/// <summary>
/// Đại diện cho một vật phẩm cụ thể trong túi đồ của người chơi.
/// </summary>
public class InventoryItem
{
	public string Id { get; set; } = string.Empty;
	public string Name { get; set; } = string.Empty;
	public string Description { get; set; } = string.Empty;
	public string IconPath { get; set; } = string.Empty;
	public ItemType Type { get; set; } = ItemType.Material;
	public int Quantity { get; set; } = 1;
	public int MaxStack { get; set; } = 99;

	public InventoryItem Clone(int quantity = 1) => new()
	{
		Id = Id,
		Name = Name,
		Description = Description,
		IconPath = IconPath,
		Type = Type,
		Quantity = quantity,
		MaxStack = MaxStack
	};
}
