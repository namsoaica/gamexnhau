using Godot;

namespace Game.Core;

/// <summary>
/// Tự động quét và tạo va chạm vật lý (Trimesh Collision) cho các bề mặt địa hình trong Map.
/// </summary>
public partial class MapAutoCollision : Node
{
	[ExportGroup("Cấu hình")]
	[Export] public bool EnableAutoCollision { get; set; } = true;

	public override void _Ready()
	{
		if (!EnableAutoCollision)
		{
			return;
		}

		Node rootNode = GetParent() ?? this;
		ScanAndGenerateCollisions(rootNode);
	}

	/// <summary>
	/// Quét đệ quy toàn bộ cây Node để tìm các MeshInstance3D phù hợp và tạo va chạm.
	/// </summary>
	private void ScanAndGenerateCollisions(Node parentNode)
	{
		foreach (Node child in parentNode.GetChildren())
		{
			if (child is MeshInstance3D meshInstance && IsWalkableSurface(meshInstance.Name))
			{
				CreateCollisionIfMissing(meshInstance);
			}

			if (child.GetChildCount() > 0)
			{
				ScanAndGenerateCollisions(child);
			}
		}
	}

	/// <summary>
	/// Tạo StaticBody3D kèm ConcavePolygonShape3D nếu MeshInstance3D chưa có va chạm.
	/// </summary>
	private void CreateCollisionIfMissing(MeshInstance3D meshInstance)
	{
		if (HasStaticBodyChild(meshInstance))
		{
			return;
		}

		meshInstance.CreateTrimeshCollision();
	}

	/// <summary>
	/// Kiểm tra xem node con đã có StaticBody3D hay chưa để tránh tạo trùng lặp.
	/// </summary>
	private bool HasStaticBodyChild(Node node)
	{
		foreach (Node child in node.GetChildren())
		{
			if (child is StaticBody3D)
			{
				return true;
			}
		}

		return false;
	}

	/// <summary>
	/// Lọc tên các Mesh cần tạo bề mặt va chạm cho nhân vật đi lại.
	/// </summary>
	private bool IsWalkableSurface(string nodeName)
	{
		string lower = nodeName.ToLower();

		return lower.Contains("terrain") ||
		       lower.Contains("stair") ||
		       lower.Contains("path") ||
		       lower.Contains("paver") ||
		       lower.Contains("fence") ||
		       lower.Contains("floor") ||
		       lower.Contains("ground");
	}
}
