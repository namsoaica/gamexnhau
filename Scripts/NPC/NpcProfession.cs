namespace Game.NPC;

/// <summary>
/// Danh sách 8 nghề nghiệp chuyên biệt của dân làng trong Village Map.
/// </summary>
public enum NpcProfession
{
	Blacksmith, // Thợ rèn
	Alchemist,  // Nhà giả kim
	Chef,       // Đầu bếp / Quán ăn
	Farmer,     // Nông dân
	Fisherman,  // Ngư dân
	Miner,      // Thợ mỏ
	Lumberjack, // Tiều phu xẻ gỗ
	Guard       // Lính canh cổng
}

/// <summary>
/// Các hàm tiện ích mở rộng cho nghề nghiệp dân làng.
/// </summary>
public static class NpcProfessionExtensions
{
	public static string GetVietnameseTitle(this NpcProfession profession)
	{
		return profession switch
		{
			NpcProfession.Blacksmith => "Thợ Rèn",
			NpcProfession.Alchemist => "Nhà Giả Kim",
			NpcProfession.Chef => "Đầu Bếp",
			NpcProfession.Farmer => "Nông Dân",
			NpcProfession.Fisherman => "Ngư Dân",
			NpcProfession.Miner => "Thợ Mỏ",
			NpcProfession.Lumberjack => "Tiều Phu",
			NpcProfession.Guard => "Lính Canh",
			_ => "Dân Làng"
		};
	}

	public static string GetDefaultGreeting(this NpcProfession profession)
	{
		return profession switch
		{
			NpcProfession.Blacksmith => "Lò rèn luôn đỏ lửa! Ngươi cần vũ khí sắc bén hay giáp kiên cố?",
			NpcProfession.Alchemist => "Chào mừng tới hiệu thuốc ma pháp. Cẩn thận đừng chạm vào vạc sôi nhé!",
			NpcProfession.Chef => "Mùi bánh mì mới ra lò thơm phức đúng không? Ngồi xuống làm chút gì đi!",
			NpcProfession.Farmer => "Vụ cải bắp năm nay tươi ngon lắm, đất đai phương Nam thật màu mỡ.",
			NpcProfession.Fisherman => "Nước giếng làng hôm nay trong vắt, cá suối tươi rói vừa về đây!",
			NpcProfession.Miner => "Tiếng cuốc gõ trong lòng đá ngân vang suốt ngày đêm. Ngươi cần than hay quặng?",
			NpcProfession.Lumberjack => "Gỗ sồi Tây Bắc đanh chắc số một vùng! Cần gỗ đóng nhà hay làm cán cuốc?",
			NpcProfession.Guard => "Làng ta thái bình yên ổn. Chúc lữ khách một chuyến đi an lành!",
			_ => "Xin chào lữ khách ghé thăm ngôi làng!"
		};
	}
}
