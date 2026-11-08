using Godot;
using System.Collections.Generic;

namespace Game.Core;

/// <summary>
/// Vùng chuyển đổi nội thất liền mạch (Seamless Interior Transition).
/// Tự động ẩn mái nhà, tường trước và điều chỉnh camera khi người chơi bước vào trong nhà.
/// Cấm triệt để tắt collider tường chu vi để ngăn chặn lỗi xuyên tường ra ngoài.
/// </summary>
public partial class InteriorZone : Area3D
{
	[ExportGroup("Các Node Kiến Trúc Cần Ẩn")]
	[Export] public Godot.Collections.Array<NodePath> RoofPaths { get; set; } = new();
	[Export] public Godot.Collections.Array<NodePath> WallFrontPaths { get; set; } = new();

	[ExportGroup("Ánh Sáng & Camera Nội Thất")]
	[Export] public OmniLight3D? InteriorLight { get; set; }
	[Export] public float InteriorCameraZoom { get; set; } = 9.5f;
	[Export] public float ExteriorCameraZoom { get; set; } = 17.5f;
	[Export] public Vector3 RoomCenterOffset { get; set; } = Vector3.Zero;

	private readonly List<Node3D> _visualNodes = new();
	private readonly List<CollisionShape3D> _roofColliders = new();
	private bool _isPlayerInside;

	public override void _Ready()
	{
		CollisionLayer = 0;
		CollisionMask = (1 << 0) | (1 << 1);

		CollectArchitectureNodes();
		ConfigureInitialState();

		BodyEntered += OnBodyEntered;
		BodyExited += OnBodyExited;
	}

	public override void _ExitTree()
	{
		BodyEntered -= OnBodyEntered;
		BodyExited -= OnBodyExited;
		_visualNodes.Clear();
		_roofColliders.Clear();
	}

	private void CollectArchitectureNodes()
	{
		CollectVisualAndColliders(RoofPaths, allowDisableCollider: true);
		CollectVisualAndColliders(WallFrontPaths, allowDisableCollider: false);
	}

	private void CollectVisualAndColliders(Godot.Collections.Array<NodePath> paths, bool allowDisableCollider)
	{
		foreach (NodePath path in paths)
		{
			if (path.IsEmpty) continue;
			Node? node = ResolveArchNode(path);
			if (node is not Node3D node3D) continue;

			_visualNodes.Add(node3D);
			if (allowDisableCollider) FindRoofColliders(node3D);
			else EnsureWallCollidersActive(node3D);
		}
	}

	private Node? ResolveArchNode(NodePath path)
	{
		Node? node = GetNodeOrNull(path);
		if (node != null) return node;
		string s = path.ToString();
		return GetNodeOrNull(s + "-col") ?? GetNodeOrNull(s + "_col");
	}

	private void FindRoofColliders(Node parent)
	{
		if (IsPerimeterWall(parent.Name)) return;

		if (parent is CollisionShape3D col) _roofColliders.Add(col);
		foreach (Node child in parent.GetChildren()) FindRoofColliders(child);
	}

	private static void EnsureWallCollidersActive(Node parent)
	{
		if (parent is CollisionShape3D col)
		{
			col.SetDeferred(CollisionShape3D.PropertyName.Disabled, false);
		}
		foreach (Node child in parent.GetChildren()) EnsureWallCollidersActive(child);
	}

	private static bool IsPerimeterWall(string nodeName)
	{
		string lower = nodeName.ToLower();
		return lower.Contains("wall") || lower.Contains("tuong");
	}

	private void ConfigureInitialState()
	{
		if (InteriorLight != null) InteriorLight.Visible = false;
		SetInteriorState(false);
	}

	protected virtual void OnBodyEntered(Node3D body)
	{
		if (!IsPlayerBody(body)) return;
		_isPlayerInside = true;
		SetInteriorState(true);
	}

	protected virtual void OnBodyExited(Node3D body)
	{
		if (!IsPlayerBody(body)) return;
		_isPlayerInside = false;
		SetInteriorState(false);
	}

	protected static bool IsPlayerBody(Node3D body) => body.IsInGroup("Player") || body.Name == "Player";

	public void SetInteriorState(bool inside)
	{
		foreach (Node3D visual in _visualNodes)
		{
			visual.Visible = !inside;
		}

		foreach (CollisionShape3D col in _roofColliders)
		{
			col.SetDeferred(CollisionShape3D.PropertyName.Disabled, inside);
		}

		if (InteriorLight != null) InteriorLight.Visible = inside;
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
			if (ExteriorCameraZoom > 0f) CameraFollow.Instance.TargetZoomSize = ExteriorCameraZoom;
		}
	}
}
