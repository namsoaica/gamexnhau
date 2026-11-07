namespace Game.NPC;

/// <summary>
/// Trạng thái hành vi của trí tuệ nhân tạo (AI State Machine) cho dân làng.
/// </summary>
public enum NpcState
{
	Idle,        // Đứng yên quan sát, nghỉ ngơi
	Working,     // Thực hiện công việc nghề nghiệp
	Patrolling,  // Đi tuần tra giữa các điểm Waypoints
	Interacting  // Đang nói chuyện, tương tác với người chơi
}
