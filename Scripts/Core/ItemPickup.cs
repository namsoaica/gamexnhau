using Godot;
using Game.Inventory;

namespace Game.Core;

/// <summary>
/// Thực thể vật phẩm rơi trên bản đồ cho phép người chơi tương tác nhặt vào túi đồ.
/// </summary>
public partial class ItemPickup : Area3D, IInteractable
{
	[ExportGroup("Cấu hình Vật Phẩm")]
	[Export] public string ItemId { get; set; } = "iron_ore";
	[Export] public int Quantity { get; set; } = 1;
	[Export] public string CustomName { get; set; } = string.Empty;
	[Export] public float RotationSpeed { get; set; } = 1.8f;
	[Export] public float BobHeight { get; set; } = 0.12f;
	[Export] public float BobSpeed { get; set; } = 2.5f;

	[ExportGroup("Tham Chiếu Visual")]
	[Export] public Node3D? VisualNode { get; set; }
	[Export] public Label3D? HoverLabel { get; set; }

	public string PromptText => $"Nhấn E để Nhặt {ResolveDisplayName()} (x{Quantity})";

	private float _timeAccumulator;
	private Vector3 _initialLocalPos = Vector3.Zero;
	private const uint InteractMask = (1 << 2) | (1 << 3);

	public override void _Ready()
	{
		Monitoring = false;
		Monitorable = true;
		CollisionLayer = InteractMask;
		CollisionMask = 0;

		VisualNode ??= GetNodeOrNull<Node3D>("Visual");
		HoverLabel ??= GetNodeOrNull<Label3D>("HoverLabel");
		if (VisualNode != null) _initialLocalPos = VisualNode.Position;

		EnsureCollisionShape();
		UpdateHoverText();
	}

	public override void _Process(double delta)
	{
		float dt = (float)delta;
		_timeAccumulator += dt;
		AnimateFloating(dt);
	}

	public bool CanInteract() => IsInsideTree() && !IsQueuedForDeletion();

	public void Interact(Node3D interactor)
	{
		if (!CanInteract()) return;
		InventoryManager? inv = InventoryManager.Instance;
		if (inv == null) return;

		bool added = inv.AddItem(ItemId, Quantity);
		if (!added) return;

		NotifyPickup();
		QueueFree();
	}

	public void OnFocusGained()
	{
		if (HoverLabel != null) HoverLabel.Visible = true;
	}

	public void OnFocusLost()
	{
		if (HoverLabel != null) HoverLabel.Visible = false;
	}

	private void AnimateFloating(float dt)
	{
		if (VisualNode == null) return;
		VisualNode.RotateY(RotationSpeed * dt);
		float yOffset = Mathf.Sin(_timeAccumulator * BobSpeed) * BobHeight;
		VisualNode.Position = _initialLocalPos + new Vector3(0, yOffset, 0);
	}

	private string ResolveDisplayName()
	{
		if (!string.IsNullOrEmpty(CustomName)) return CustomName;
		InventoryItem? item = ItemDatabase.CreateItem(ItemId, 1);
		return item?.Name ?? ItemId;
	}

	private void NotifyPickup()
	{
		string msg = $"✨ Đã nhặt được: {ResolveDisplayName()} x{Quantity}!";
		BuildingInteriorManager.Instance?.ShowToast(msg, new Color(1.0f, 0.85f, 0.3f));
	}

	private void UpdateHoverText()
	{
		if (HoverLabel == null) return;
		HoverLabel.Text = $"{ResolveDisplayName()} (x{Quantity})\n[E / Gamepad X]";
		HoverLabel.Visible = false;
	}

	private void EnsureCollisionShape()
	{
		foreach (Node child in GetChildren())
		{
			if (child is CollisionShape3D) return;
		}

		CollisionShape3D col = new CollisionShape3D
		{
			Shape = new SphereShape3D { Radius = 1.2f },
			Position = new Vector3(0, 0.4f, 0)
		};
		AddChild(col);
	}
}
