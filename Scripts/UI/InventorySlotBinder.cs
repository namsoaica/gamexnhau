using Godot;
using Game.Inventory;

namespace Game.UI;

/// <summary>
/// Lớp trợ giúp hiển thị và liên kết dữ liệu ô vật phẩm trong túi đồ.
/// </summary>
public static class InventorySlotBinder
{
	public static void DisplayItemOnSlot(Button btn, InventoryItem item)
	{
		btn.Text = item.Quantity > 1 ? $"x{item.Quantity}" : string.Empty;
		btn.Alignment = HorizontalAlignment.Right;

		if (string.IsNullOrEmpty(item.IconPath) || !ResourceLoader.Exists(item.IconPath)) return;
		btn.Icon = GD.Load<Texture2D>(item.IconPath);
		btn.IconAlignment = HorizontalAlignment.Center;
		btn.ExpandIcon = true;
	}

	public static void ClearSlotDisplay(Button btn)
	{
		btn.Text = string.Empty;
		btn.Icon = null;
	}

	public static string ResolveTypeName(ItemType type) => type switch
	{
		ItemType.Consumable => "Vật phẩm tiêu hao (Dùng được)",
		ItemType.Material => "Nguyên liệu chế tạo",
		ItemType.KeyItem => "Vật phẩm cốt truyện quan trọng",
		_ => "Vật phẩm"
	};
}
