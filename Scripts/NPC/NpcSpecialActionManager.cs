using System;
using System.Collections.Generic;

namespace Game.NPC;

/// <summary>
/// Đại diện cho một hành động tương tác đặc biệt của dân làng.
/// </summary>
public record NpcSpecialAction(string Title, string Description, Func<string> Execute);

/// <summary>
/// Quản lý danh mục hành vi tương tác đặc biệt cho 8 nghề nghiệp trong làng.
/// </summary>
public static class NpcSpecialActionManager
{
	public static List<NpcSpecialAction> GetActions(NpcProfession profession)
	{
		return profession switch
		{
			NpcProfession.Blacksmith => CreateBlacksmithActions(),
			NpcProfession.Alchemist => CreateAlchemistActions(),
			NpcProfession.Chef => CreateChefActions(),
			NpcProfession.Farmer => CreateFarmerActions(),
			NpcProfession.Fisherman => CreateFishermanActions(),
			NpcProfession.Miner => CreateMinerActions(),
			NpcProfession.Lumberjack => CreateLumberjackActions(),
			NpcProfession.Guard => CreateGuardActions(),
			_ => new List<NpcSpecialAction>()
		};
	}

	private static List<NpcSpecialAction> CreateBlacksmithActions() => new()
	{
		new("Cường hóa vũ khí (+1 Công)", "Tôi luyện lưỡi kiếm trên đe sắt rực lửa.",
			() => "Thanh kiếm của bạn được rèn thêm sắc bén! Sức tấn công +1."),
		new("Sửa chữa trang bị", "Mài giũa giáp sắt sáng bóng và gia cố chốt tán.",
			() => "Trang bị của bạn đã được phục hồi độ bền tối đa 100%."),
		new("Hỏi về kim loại", "Tìm hiểu về mỏ quặng phía Đông Bắc bản đồ.",
			() => "Thợ rèn nói: 'Phía Đông Bắc có vách núi quặng sắt rất tốt, nhưng coi chừng đá lở.'")
	};

	private static List<NpcSpecialAction> CreateAlchemistActions() => new()
	{
		new("Mua bình Hồi máu", "Dược dịch thảo mộc đỏ tươi giúp phục hồi sinh lực.",
			() => "Bạn nhận được 1 Bình Máu Đỏ (Hồi phục 50 HP)."),
		new("Mua thuốc Tăng tốc", "Dược dịch ngọc bích giúp bước chân nhẹ như gió.",
			() => "Uống thành công! Tốc độ chạy tăng +30% trong 15 giây."),
		new("Học thuật giả kim", "Hỏi thăm về công thức luyện dược thảo mộc.",
			() => "Nhà giả kim nháy mắt: 'Bí quyết nằm ở chỗ hái cỏ lúc sương sớm chưa tan!'")
	};

	private static List<NpcSpecialAction> CreateChefActions() => new()
	{
		new("Thưởng thức Bánh mì nướng", "Chiếc bánh mì vỏ giòn ruột mềm thơm nức mũi.",
			() => "Ăn một ổ bánh nóng hổi, toàn thân tràn đầy năng lượng ấm áp!"),
		new("Mua lương thực mang đi", "Gói lương khô dinh dưỡng cho hành trình dài.",
			() => "Đã nhận 1 Gói Lương Khô Dã Ngoại."),
		new("Hỏi thực đơn hôm nay", "Tìm hiểu các món ngon đặc sản làng.",
			() => "Đầu bếp cười lớn: 'Hôm nay có súp bắp cải hầm nấm rừng đặc biệt!'")
	};

	private static List<NpcSpecialAction> CreateFarmerActions() => new()
	{
		new("Mua bắp cải tươi", "Những bắp cải xanh mọng nước hái tận vườn.",
			() => "Bạn nhận được 1 Giỏ Bắp Cải Tươi Xanh ngon ngọt."),
		new("Hỏi mùa vụ", "Trao đổi về thời tiết và điều kiện canh tác.",
			() => "Nông dân nói: 'Mảnh đất phù sa ven sông này gieo hạt gì cũng trổ bông mơn mởn!'")
	};

	private static List<NpcSpecialAction> CreateFishermanActions() => new()
	{
		new("Mua cá tươi", "Những chú cá suối ánh bạc tươi rói quẫy đuôi.",
			() => "Bạn nhận được 1 Xâu Cá Suối Tươi Ngon."),
		new("Bí quyết câu cá", "Kinh nghiệm chọn mồi và tìm luồng cá ngược dòng.",
			() => "Ngư dân dặn: 'Cứ lúc mặt trời lặn hãy buông cần, cá đớp mồi rất hăng.'")
	};

	private static List<NpcSpecialAction> CreateMinerActions() => new()
	{
		new("Đổi than đá lấy quặng sắt", "Giao dịch khoáng thô khai thác từ hầm mỏ.",
			() => "Đã đổi 3 Thỏi Than Củi lấy 1 Quặng Sắt Tinh Khiết."),
		new("Tin đồn trong hang mỏ", "Chuyện kỳ bí trong lòng vách đá sâu thẳm.",
			() => "Thợ mỏ hạ giọng: 'Đêm qua ta nghe thấy tiếng tinh thể pha lê reo vang trong hầm...'")
	};

	private static List<NpcSpecialAction> CreateLumberjackActions() => new()
	{
		new("Mua gỗ sồi xẻ", "Khối gỗ chắc nịch thích hợp xây dựng và gia cố đồ vật.",
			() => "Bạn nhận được 1 Bó Gỗ Sồi Cắt Xẻ Chất Lượng Cao."),
		new("Chuyện rừng sâu", "Cảnh giác với những bí mật của cánh rừng Tây Bắc.",
			() => "Tiều phu chia sẻ: 'Cánh rừng này cổ xưa lắm, hãy luôn mang theo rìu phòng thân.'")
	};

	private static List<NpcSpecialAction> CreateGuardActions() => new()
	{
		new("Báo cáo an ninh làng", "Tình hình an ninh khu vực cổng làng và các lối mòn.",
			() => "Lính canh nghiêm trang: 'Khu vực an toàn tuyệt đối, không có quái vật xâm nhập.'"),
		new("Hỏi đường các khu vực", "Chỉ dẫn chi tiết vị trí 8 phân khu trong làng.",
			() => "Cổng Nam -> Đi thẳng đến Chợ, rẽ Trái đến Rèn, rẽ Phải đến Giả Kim & Quán Ăn!")
	};
}
