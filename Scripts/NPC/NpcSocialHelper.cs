using Godot;

namespace Game.NPC;

/// <summary>
/// Trợ lý xử lý tương tác xã hội, tìm kiếm bạn trò chuyện và câu thoại giữa các NPC.
/// </summary>
public static class NpcSocialHelper
{
	private const float ConversationDistance = 2.5f;

	/// <summary>
	/// Quét tìm một NPC gần nhất đủ điều kiện để bắt đầu trò chuyện.
	/// </summary>
	public static NpcBehavior? FindNearbyPartner(NpcBehavior self)
	{
		SceneTree tree = self.GetTree();
		if (tree == null) return null;

		Godot.Collections.Array<Node> npcs = tree.GetNodesInGroup("VillageNPC");
		Vector3 myPos = self.GlobalPosition;

		foreach (Node node in npcs)
		{
			if (node is not NpcBehavior other || other == self) continue;
			if (!IsEligibleForChat(other)) continue;

			float dist = myPos.DistanceTo(other.GlobalPosition);
			if (dist <= ConversationDistance)
			{
				return other;
			}
		}

		return null;
	}

	/// <summary>
	/// Kiểm tra điều kiện để một NPC có thể tham gia trò chuyện.
	/// </summary>
	public static bool IsEligibleForChat(NpcBehavior npc)
	{
		if (npc.CurrentState == NpcState.Interacting) return false;
		if (npc.CurrentState == NpcState.TalkingWithNpc) return false;
		return npc.SocialCooldown <= 0.0f;
	}

	/// <summary>
	/// Kích hoạt cuộc hội thoại qua lại giữa 2 NPC.
	/// </summary>
	public static void StartConversation(NpcBehavior npcA, NpcBehavior npcB)
	{
		var (lineA, lineB) = GetDialogueLines(npcA.Profession, npcB.Profession);
		npcA.BeginTalkingWith(npcB, lineA);
		npcB.BeginTalkingWith(npcA, lineB);
	}

	/// <summary>
	/// Lấy cặp câu thoại phù hợp theo nghề nghiệp của 2 NPC.
	/// </summary>
	public static (string lineA, string lineB) GetDialogueLines(NpcProfession profA, NpcProfession profB)
	{
		if (MatchesPair(profA, profB, NpcProfession.Blacksmith, NpcProfession.Chef))
		{
			return profA == NpcProfession.Blacksmith
				? ("Chào Gusteau! Mùi bánh mì nướng thơm lừng cả xóm rèn!", "Chào Vulcan! Hôm nay thợ rèn có đắt khách không?")
				: ("Chào Vulcan! Hôm nay thợ rèn có đắt khách không?", "Chào Gusteau! Mùi bánh mì nướng thơm lừng cả xóm rèn!");
		}

		if (MatchesPair(profA, profB, NpcProfession.Blacksmith, NpcProfession.Alchemist))
		{
			return profA == NpcProfession.Blacksmith
				? ("Chào Aria! Bình dịch xanh hôm trước giữ nhiệt lò rèn rất tốt!", "Cảm ơn Vulcan! Lò rèn cần chất tôi kim loại cứ bảo ta nhé!")
				: ("Chào Vulcan! Lò rèn cần chất tôi kim loại cứ bảo ta nhé!", "Chào Aria! Bình dịch xanh hôm trước giữ nhiệt lò rèn rất tốt!");
		}

		if (MatchesPair(profA, profB, NpcProfession.Chef, NpcProfession.Fisherman))
		{
			return profA == NpcProfession.Chef
				? ("Chào Finn! Cá tươi vừa câu được trông ngon mắt quá!", "Chào Gusteau! Để lại cho quán chú cá to nhất trưa nay nhé!")
				: ("Chào Gusteau! Để lại cho quán chú cá to nhất trưa nay nhé!", "Chào Finn! Cá tươi vừa câu được trông ngon mắt quá!");
		}

		if (MatchesPair(profA, profB, NpcProfession.Farmer, NpcProfession.Guard))
		{
			return profA == NpcProfession.Farmer
				? ("Chào lính canh! Cổng làng hôm nay an ninh yên bình chứ?", "Yên tâm bác George! Mọi ngả đường đều an toàn cho bà con!")
				: ("Yên tâm bác George! Mọi ngả đường đều an toàn cho bà con!", "Chào lính canh! Cổng làng hôm nay an ninh yên bình chứ?");
		}

		if (profA == NpcProfession.Guard && profB == NpcProfession.Guard)
		{
			return ("Ca trực hôm nay thế nào rồi đồng đội?", "Mọi thứ đều ổn định, không có quái vật nào bén mảng!");
		}

		return GetSecondaryDialogueLines(profA, profB);
	}

	private static (string lineA, string lineB) GetSecondaryDialogueLines(NpcProfession profA, NpcProfession profB)
	{
		if (MatchesPair(profA, profB, NpcProfession.Lumberjack, NpcProfession.Blacksmith))
		{
			return profA == NpcProfession.Lumberjack
				? ("Chào Vulcan! Gỗ sồi đốt lò rèn chuyến này cháy đượm chứ?", "Rất tuyệt Grover! Than gỗ đanh và giữ nhiệt cực kỳ đều!")
				: ("Chào Grover! Than gỗ đanh và giữ nhiệt cực kỳ đều!", "Chào Vulcan! Gỗ sồi đốt lò rèn chuyến này cháy đượm chứ?");
		}

		if (MatchesPair(profA, profB, NpcProfession.Miner, NpcProfession.Blacksmith))
		{
			return profA == NpcProfession.Miner
				? ("Chào Vulcan! Quặng sắt tinh luyện từ vách đá Đông Bắc đây!", "Cảm ơn Brock! Quặng chất lượng cao rèn kiếm bén lắm!")
				: ("Cảm ơn Brock! Quặng chất lượng cao rèn kiếm bén lắm!", "Chào Vulcan! Quặng sắt tinh luyện từ vách đá Đông Bắc đây!");
		}

		return ("Chào người anh em! Hôm nay trong làng thật rộn ràng!", "Đúng vậy! Chúc bạn một ngày làm việc tràn đầy niềm vui!");
	}

	private static bool MatchesPair(NpcProfession pA, NpcProfession pB, NpcProfession target1, NpcProfession target2)
	{
		return (pA == target1 && pB == target2) || (pA == target2 && pB == target1);
	}
}
