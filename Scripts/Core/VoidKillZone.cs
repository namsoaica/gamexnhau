using Godot;
using Game.Player;

namespace Game.Core;

/// <summary>
/// Vùng ranh giới vực sâu bên dưới đảo bay, tự động đưa nhân vật trở lại điểm an toàn khi rơi ra ngoài.
/// </summary>
public partial class VoidKillZone : Area3D
{
	[Signal]
	public delegate void PlayerRespawnedEventHandler(Node3D player, Vector3 respawnPoint);

	[ExportGroup("Cấu hình Hồi sinh")]
	[Export] public Node3D? SpawnTarget { get; set; }
	[Export] public Vector3 DefaultSpawnPosition { get; set; } = new Vector3(6.0f, 2.5f, -6.0f);
	[Export] public bool AutoRecordInitialPosition { get; set; } = true;

	[ExportGroup("Kích Thước Vùng Va Chạm")]
	[Export] public Vector3 ZoneSize { get; set; } = new Vector3(400.0f, 10.0f, 400.0f);

	private Vector3? _recordedSpawnPosition;
	private const uint HazardLayerBit = 1 << 4;
	private const uint AllCollisionMask = 0x7FFFFFFF;

	public override void _Ready()
	{
		CollisionLayer = HazardLayerBit;
		CollisionMask = AllCollisionMask;
		Monitoring = true;

		EnsureCollisionShape();
		RecordInitialPlayerPosition();
		BodyEntered += OnBodyEntered;
	}

	/// <summary>
	/// Xử lý sự kiện khi có vật thể rơi vào vùng vực thẳm.
	/// </summary>
	private void OnBodyEntered(Node3D body)
	{
		if (body is PlayerMovement playerMovement)
		{
			RespawnPlayer(playerMovement);
			return;
		}

		if (body is CharacterBody3D character && body.Name.ToString().Contains("Player"))
		{
			RespawnCharacter(character);
		}
	}

	/// <summary>
	/// Hồi sinh PlayerMovement về vị trí an toàn và triệt tiêu vận tốc rơi.
	/// </summary>
	private void RespawnPlayer(PlayerMovement player)
	{
		Vector3 respawnPos = GetRespawnLocation();
		player.TeleportTo(respawnPos);
		EmitSignal(SignalName.PlayerRespawned, player, respawnPos);
	}

	/// <summary>
	/// Hồi sinh CharacterBody3D tổng quát về điểm xuất phát.
	/// </summary>
	private void RespawnCharacter(CharacterBody3D character)
	{
		Vector3 respawnPos = GetRespawnLocation();
		character.Velocity = Vector3.Zero;
		character.GlobalPosition = respawnPos;
		character.ResetPhysicsInterpolation();
		EmitSignal(SignalName.PlayerRespawned, character, respawnPos);
	}

	/// <summary>
	/// Xác định tọa độ hồi sinh ưu tiên theo thứ tự cấu hình.
	/// </summary>
	private Vector3 GetRespawnLocation()
	{
		if (SpawnTarget != null)
		{
			return SpawnTarget.GlobalPosition;
		}

		if (AutoRecordInitialPosition && _recordedSpawnPosition.HasValue)
		{
			return _recordedSpawnPosition.Value;
		}

		return DefaultSpawnPosition;
	}

	/// <summary>
	/// Ghi nhớ tọa độ ban đầu của nhân vật Player trong bản đồ khi khởi tạo game.
	/// </summary>
	private void RecordInitialPlayerPosition()
	{
		if (!AutoRecordInitialPosition || SpawnTarget != null) return;

		Node3D? player = (Node3D?)GetTree().GetFirstNodeInGroup("Player") ?? (Node3D?)GetParent()?.FindChild("Player");
		if (player != null)
		{
			_recordedSpawnPosition = player.GlobalPosition;
		}
	}

	/// <summary>
	/// Đảm bảo luôn có CollisionShape3D bao phủ phạm vi vực sâu nếu chưa được thêm trong scene.
	/// </summary>
	private void EnsureCollisionShape()
	{
		foreach (Node child in GetChildren())
		{
			if (child is CollisionShape3D) return;
		}

		CollisionShape3D shapeNode = new CollisionShape3D();
		BoxShape3D boxShape = new BoxShape3D();
		boxShape.Size = ZoneSize;
		shapeNode.Shape = boxShape;
		AddChild(shapeNode);
	}
}
