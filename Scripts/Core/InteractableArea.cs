using Godot;

namespace Game.Core;

/// <summary>
/// Vùng va chạm tương tác 3D dùng chung, gắn vào bất kỳ vật thể hoặc NPC nào trong màn chơi.
/// </summary>
public partial class InteractableArea : Area3D, IInteractable
{
	[Signal]
	public delegate void InteractedEventHandler(Node3D interactor);

	[ExportGroup("Cấu hình Tương tác")]
	[Export] public string PromptText { get; set; } = "Tương tác";
	[Export] public bool IsEnabled { get; set; } = true;
	[Export] public float InteractionRadius { get; set; } = 3.0f;

	private const uint InteractableLayer = (1 << 2) | (1 << 3); // Layer 3 (NPC) & Layer 4 (Interactable)

	public override void _Ready()
	{
		Monitoring = false;
		Monitorable = true;
		CollisionLayer = InteractableLayer;
		CollisionMask = 0;
		EnsureCollisionShape();
	}

	/// <summary>
	/// Kiểm tra trạng thái sẵn sàng tương tác của vùng này.
	/// </summary>
	public bool CanInteract()
	{
		return IsEnabled && IsInsideTree();
	}

	/// <summary>
	/// Kích hoạt tương tác, phát tín hiệu và ủy quyền cho Node cha nếu có.
	/// </summary>
	/// <param name="interactor">Node người chơi kích hoạt tương tác.</param>
	public void Interact(Node3D interactor)
	{
		if (!CanInteract())
		{
			return;
		}

		EmitSignal(SignalName.Interacted, interactor);

		if (GetParent() is IInteractable parentInteractable)
		{
			parentInteractable.Interact(interactor);
		}
	}

	/// <summary>
	/// Chuyển tiếp sự kiện được nhắm tới cho Node cha nếu có.
	/// </summary>
	public void OnFocusGained()
	{
		if (GetParent() is IInteractable parent)
		{
			parent.OnFocusGained();
		}
	}

	/// <summary>
	/// Chuyển tiếp sự kiện mất tiêu điểm cho Node cha nếu có.
	/// </summary>
	public void OnFocusLost()
	{
		if (GetParent() is IInteractable parent)
		{
			parent.OnFocusLost();
		}
	}

	/// <summary>
	/// Tự động sinh CollisionShape3D hình cầu nếu trong Editor chưa tạo sẵn.
	/// </summary>
	private void EnsureCollisionShape()
	{
		foreach (Node child in GetChildren())
		{
			if (child is CollisionShape3D)
			{
				return;
			}
		}

		CollisionShape3D shapeNode = new CollisionShape3D();
		shapeNode.Position = new Vector3(0.0f, 1.0f, 0.0f);
		SphereShape3D sphere = new SphereShape3D();
		sphere.Radius = InteractionRadius;
		shapeNode.Shape = sphere;
		AddChild(shapeNode);
	}
}
