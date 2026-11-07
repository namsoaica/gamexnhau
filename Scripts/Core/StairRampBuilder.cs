using Godot;

namespace Game.Core;

/// <summary>
/// Hỗ trợ tính toán và tự động tạo mặt dốc va chạm phẳng dạng ConvexPolygonShape3D cho cầu thang.
/// Giúp nhân vật di chuyển êm ru lên xuống mà không bị cản trở bởi góc 90 độ của bậc thang.
/// </summary>
public static class StairRampBuilder
{
	private const float SlopeExtension = 0.05f;
	private const float HeightThreshold = 0.15f;

	/// <summary>
	/// Nhận diện xem tên Node có phải là cầu thang hay không.
	/// </summary>
	public static bool IsStaircase(string nodeName)
	{
		string lower = nodeName.ToLower();
		return lower.Contains("stair") || lower.Contains("staircase");
	}

	/// <summary>
	/// Tạo StaticBody3D chứa ConvexPolygonShape3D dạng hình nêm lăng trụ che phủ toàn bộ bậc thang.
	/// </summary>
	public static void BuildStairRamp(MeshInstance3D meshInstance)
	{
		if (meshInstance.Mesh == null) return;

		Aabb aabb = meshInstance.GetAabb();
		Vector3[] points = CalculateRampPoints(meshInstance, aabb);
		if (points.Length == 0) return;

		var convexShape = new ConvexPolygonShape3D { Points = points };
		var colShape = new CollisionShape3D { Name = "StairRampShape", Shape = convexShape };
		var staticBody = new StaticBody3D { Name = $"{meshInstance.Name}_RampBody" };

		staticBody.AddChild(colShape);
		meshInstance.AddChild(staticBody);
		GD.Print($"[StairRampBuilder] Đã tạo dốc nghiêng phẳng ConvexPolygonShape3D cho: {meshInstance.Name}");
	}

	/// <summary>
	/// Tính toán 6 đỉnh của lăng trụ tam giác (hình nêm) theo hướng dốc của cầu thang.
	/// </summary>
	private static Vector3[] CalculateRampPoints(MeshInstance3D meshInstance, Aabb aabb)
	{
		bool isZAxis = true;
		bool topIsMin = true;
		if (!TryDetectStairSlope(meshInstance, aabb, out isZAxis, out topIsMin))
		{
			isZAxis = aabb.Size.Z >= aabb.Size.X;
			topIsMin = true;
		}

		return isZAxis
			? BuildZRampPoints(aabb, topIsMin)
			: BuildXRampPoints(aabb, topIsMin);
	}

	/// <summary>
	/// Xây dựng các đỉnh cho dốc chạy dọc theo trục Z.
	/// </summary>
	private static Vector3[] BuildZRampPoints(Aabb aabb, bool topIsMin)
	{
		float minX = aabb.Position.X;
		float maxX = aabb.End.X;
		float minY = aabb.Position.Y;
		float maxY = aabb.End.Y;

		float topZ = topIsMin ? aabb.Position.Z - SlopeExtension : aabb.End.Z + SlopeExtension;
		float botZ = topIsMin ? aabb.End.Z + SlopeExtension : aabb.Position.Z - SlopeExtension;

		return new[]
		{
			new Vector3(minX, minY, botZ),
			new Vector3(maxX, minY, botZ),
			new Vector3(minX, maxY, topZ),
			new Vector3(maxX, maxY, topZ),
			new Vector3(minX, minY, topZ),
			new Vector3(maxX, minY, topZ)
		};
	}

	/// <summary>
	/// Xây dựng các đỉnh cho dốc chạy dọc theo trục X.
	/// </summary>
	private static Vector3[] BuildXRampPoints(Aabb aabb, bool topIsMin)
	{
		float minZ = aabb.Position.Z;
		float maxZ = aabb.End.Z;
		float minY = aabb.Position.Y;
		float maxY = aabb.End.Y;

		float topX = topIsMin ? aabb.Position.X - SlopeExtension : aabb.End.X + SlopeExtension;
		float botX = topIsMin ? aabb.End.X + SlopeExtension : aabb.Position.X - SlopeExtension;

		return new[]
		{
			new Vector3(botX, minY, minZ),
			new Vector3(botX, minY, maxZ),
			new Vector3(topX, maxY, minZ),
			new Vector3(topX, maxY, maxZ),
			new Vector3(topX, minY, minZ),
			new Vector3(topX, minY, maxZ)
		};
	}

	/// <summary>
	/// Quét mảng đỉnh của Mesh để phát hiện hướng dốc từ chân lên đỉnh.
	/// </summary>
	private static bool TryDetectStairSlope(MeshInstance3D meshInstance, Aabb aabb, out bool isZAxis, out bool topIsMin)
	{
		isZAxis = true;
		topIsMin = true;
		if (meshInstance.Mesh is not ArrayMesh arrayMesh || arrayMesh.GetSurfaceCount() == 0) return false;

		Vector3[] verts = (Vector3[])arrayMesh.SurfaceGetArrays(0)[(int)Mesh.ArrayType.Vertex];
		if (verts.Length == 0) return false;

		if (!CalculateSlopeDelta(verts, aabb, out Vector3 delta)) return false;
		isZAxis = Mathf.Abs(delta.Z) >= Mathf.Abs(delta.X);
		topIsMin = isZAxis ? delta.Z < 0.0f : delta.X < 0.0f;
		return true;
	}

	private static bool CalculateSlopeDelta(Vector3[] verts, Aabb aabb, out Vector3 delta)
	{
		Vector3 topSum = Vector3.Zero, botSum = Vector3.Zero;
		int topCount = 0, botCount = 0;
		float topThresh = aabb.End.Y - HeightThreshold, botThresh = aabb.Position.Y + HeightThreshold;

		foreach (var v in verts)
		{
			if (v.Y >= topThresh) { topSum += v; topCount++; }
			if (v.Y <= botThresh) { botSum += v; botCount++; }
		}

		delta = (topCount > 0 && botCount > 0) ? (topSum / topCount) - (botSum / botCount) : Vector3.Zero;
		return topCount > 0 && botCount > 0;
	}
}
