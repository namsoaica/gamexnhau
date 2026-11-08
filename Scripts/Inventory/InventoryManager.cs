using Godot;
using System.Collections.Generic;
using Game.Player;

namespace Game.Inventory;

/// <summary>
/// Quản trị trung tâm hệ thống Túi đồ (Inventory Manager) cho người chơi.
/// </summary>
public partial class InventoryManager : Node
{
	public static InventoryManager? Instance { get; private set; }

	[Signal] public delegate void InventoryChangedEventHandler();
	[Signal] public delegate void ItemUsedEventHandler(string itemId, string message);

	public const int MaxSlots = 16;
	private readonly List<InventoryItem> _items = new();

	public override void _Ready()
	{
		Instance = this;
		InitializeStarterItems();
	}

	public override void _ExitTree()
	{
		if (Instance == this) Instance = null;
		_items.Clear();
	}

	public IReadOnlyList<InventoryItem> GetItems() => _items;
	public int GetItemCount() => _items.Count;
	public bool HasItem(string id) => _items.Exists(it => it.Id == id);

	public bool AddItem(string id, int count = 1)
	{
		if (count <= 0) return false;
		InventoryItem? existing = _items.Find(it => it.Id == id && it.Quantity < it.MaxStack);

		if (existing != null)
		{
			existing.Quantity = Mathf.Min(existing.Quantity + count, existing.MaxStack);
			EmitSignal(SignalName.InventoryChanged);
			return true;
		}

		if (_items.Count >= MaxSlots) return false;
		InventoryItem? newItem = ItemDatabase.CreateItem(id, count);
		if (newItem == null) return false;

		_items.Add(newItem);
		EmitSignal(SignalName.InventoryChanged);
		return true;
	}

	public bool RemoveItem(string id, int count = 1)
	{
		InventoryItem? existing = _items.Find(it => it.Id == id);
		if (existing == null || existing.Quantity < count) return false;

		existing.Quantity -= count;
		if (existing.Quantity <= 0) _items.Remove(existing);
		EmitSignal(SignalName.InventoryChanged);
		return true;
	}

	public bool UseItem(int slotIndex)
	{
		if (slotIndex < 0 || slotIndex >= _items.Count) return false;
		InventoryItem item = _items[slotIndex];
		if (item.Type != ItemType.Consumable) return false;

		string message = ApplyItemEffect(item.Id);
		item.Quantity--;
		if (item.Quantity <= 0) _items.RemoveAt(slotIndex);

		EmitSignal(SignalName.InventoryChanged);
		EmitSignal(SignalName.ItemUsed, item.Id, message);
		return true;
	}

	private string ApplyItemEffect(string id) => id switch
	{
		"baguette" => "Đã thưởng thức bánh mì baguette giòn rụm! Phục hồi toàn bộ thể lực.",
		"potion_health" => "Đã uống Bình Máu Đỏ! Phục hồi tức thì 50 HP.",
		"potion_speed" => ApplySpeedBoost(),
		_ => "Đã sử dụng vật phẩm thành công."
	};

	private string ApplySpeedBoost()
	{
		PlayerMovement? player = (PlayerMovement?)GetTree().GetFirstNodeInGroup("Player");
		if (player == null) return "Không tìm thấy người chơi để tăng tốc.";

		float origSpeed = player.MoveSpeed;
		player.MoveSpeed = origSpeed * 1.35f;

		SceneTreeTimer timer = GetTree().CreateTimer(15.0);
		timer.Timeout += () => { if (GodotObject.IsInstanceValid(player)) player.MoveSpeed = origSpeed; };
		return "Gió lốc bao bọc! Tốc độ di chuyển tăng +35% trong 15 giây.";
	}

	private void InitializeStarterItems()
	{
		AddItem("baguette", 2);
		AddItem("potion_health", 1);
		AddItem("potion_speed", 1);
		AddItem("wood_log", 3);
		AddItem("iron_ore", 2);
		AddItem("key", 1);
	}
}
