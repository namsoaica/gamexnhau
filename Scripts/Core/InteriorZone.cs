using Godot;
using System.Collections.Generic;

namespace Game.Core;

/// <summary>
/// Vùng chuyển đổi nội thất liền mạch (Seamless Interior Transition).
/// Tự động ẩn mái nhà, tường trước và điều chỉnh camera khi người chơi bước vào trong nhà.
/// </summary>
public partial class InteriorZone : Area3D
{
	[ExportGroup("Các Node Kiến Trúc Cần Ẩn")]
	[Export] public Godot.Collections.Array<NodePath> RoofPaths { get; set; } = new();
	[Export] public Godot.Collections.Array<NodePath> WallFrontPaths { get; set; } = new();

	[ExportGroup("Ánh Sáng & Camera Nội Thất")]
	[Export] public OmniLight3D? InteriorLight { get; set; }
	[Export] public float InteriorCameraZoom { get; set; } = 12.5f;
	[Export] public Vector3 RoomCenterOffset { get; set; } = Vector3.Zero;

	private readonly List<Node3D> _visualNodes = new();
	private readonly List<CollisionShape3D> _colliders = new();
	private bool _isPlayerInside;

	public override void _Ready()
	{
		CollisionLayer = 0;
		CollisionMask = 1 << 1; // Layer 2: Player

		CollectArchitectureNodes();
		ConfigureInitialState();

		BodyEntered += OnBodyEntered;
		BodyExited += OnBodyExited;
	}

	public override void _ExitTree()
	{
		BodyEntered -= OnBodyEntered;
		BodyExited -= OnBodyExited;
	}

	private void CollectArchitectureNodes()
	{
		CollectNodesFromPaths(RoofPaths);
		CollectNodesFromPaths(WallFrontPaths);
	}

	private void CollectNodesFromPaths(Godot.Collections.Array<NodePath> paths)
	{
		foreach (NodePath path in paths)
		{
			if (path.IsEmpty) continue;
			Node? node = GetNodeOrNull(path);
			if (node is Node3D node3D)
			{
				_visualNodes.Add(node3D);
				FindChildColliders(node3D);
			}
		}
	}

	private void FindChildColliders(Node parent)
	{
		if (parent is CollisionShape3D col)
		{
			_colliders.Add(col);
		}

		foreach (Node child in parent.GetChildren())
		{
			FindChildColliders(child);
		}
	}

	private void ConfigureInitialState()
	{
		if (InteriorLight != null)
		{
			InteriorLight.Visible = false;
		}
		SetInteriorState(false);
	}

	protected virtual void OnBodyEntered(Node3D body)
	{
		if (!body.IsInGroup("Player") && body.Name != "Player") return;
		_isPlayerInside = true;
		SetInteriorState(true);
	}

	protected virtual void OnBodyExited(Node3D body)
	{
		if (!body.IsInGroup("Player") && body.Name != "Player") return;
		_isPlayerInside = false;
		SetInteriorState(false);
	}

	private void SetInteriorState(bool inside)
	{
		foreach (Node3D visual in _visualNodes)
		{
			visual.Visible = !inside;
		}

		foreach (CollisionShape3D col in _colliders)
		{
			col.SetDeferred(CollisionShape3D.PropertyName.Disabled, inside);
		}

		if (InteriorLight != null)
		{
			InteriorLight.Visible = inside;
		}

		ApplyCameraFocus(inside);
	}

	private void ApplyCameraFocus(bool inside)
	{
		if (CameraFollow.Instance == null) return;

		if (inside)
		{
			Vector3 roomCenter = GlobalPosition + RoomCenterOffset;
			CameraFollow.Instance.SetInteriorFocus(roomCenter, InteriorCameraZoom);
		}
		else
		{
			CameraFollow.Instance.SetInteriorFocus(null, null);
		}
	}
}
