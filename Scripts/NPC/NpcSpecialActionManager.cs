using System;
using System.Collections.Generic;
using Game.Inventory;

namespace Game.NPC;

/// <summary>
/// Đại diện cho một hành động tương tác đặc biệt của dân làng.
/// </summary>
public record NpcSpecialAction(string Title, string Description, Func<string> Execute);

/// <summary>
/// Quản lý danh mục hành vi tương tác đặc biệt và trao đổi vật phẩm cho 8 nghề nghiệp trong làng.
/// </summary>
public static class NpcSpecialActionManager
{
	public static List<NpcSpecialAction> GetActions(NpcProfession profession) => profession switch
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

	private static List<NpcSpecialAction> CreateBlacksmithActions() => new()
	{
		new("Cường hóa vũ khí (+1 Công)", "Tôi luyện lưỡi kiếm trên đe sắt rực lửa.", () =>
		{
			InventoryManager.Instance?.AddItem("iron_ore", 1);
			return "Thanh kiếm được rèn thêm sắc bén (+1 Sát thương)! Thợ rèn tặng thêm 1 Quặng Sắt dự phòng.";
		}),
		new("Sửa chữa trang bị", "Mài giũa giáp sắt sáng bóng và gia cố chốt tán.",
			() => "Trang bị của bạn đã được phục hồi độ bền tối đa 100%."),
		new("Hỏi về kim loại", "Tìm hiểu về mỏ quặng phía Đông Bắc bản đồ.",
			() => "Thợ rèn nói: 'Phía Đông Bắc có vách núi quặng sắt rất tốt, hãy thu thập mang về đây!'")
	};

	private static List<NpcSpecialAction> CreateAlchemistActions() => new()
	{
		new("Mua bình Hồi máu", "Dược dịch thảo mộc đỏ tươi giúp phục hồi sinh lực.", () =>
		{
			InventoryManager.Instance?.AddItem("potion_health", 1);
			return "Đã nhận 1 Bình Máu Đỏ (Hồi phục 50 HP) bỏ vào túi đồ!";
		}),
		new("Mua thuốc Tăng tốc", "Dược dịch ngọc bích giúp bước chân nhẹ như gió.", () =>
		{
			InventoryManager.Instance?.AddItem("potion_speed", 1);
			return "Đã nhận 1 Bình Tăng Tốc (Tăng tốc độ +30%) bỏ vào túi đồ!";
		}),
		new("Học thuật giả kim", "Hỏi thăm về công thức luyện dược thảo mộc.", () =>
		{
			InventoryManager.Instance?.AddItem("herb", 1);
			return "Nhà giả kim tặng bạn 1 Cành Thảo Mộc Xanh và dặn: 'Hãy hái lúc sương sớm chưa tan!'";
		})
	};

	private static List<NpcSpecialAction> CreateChefActions() => new()
	{
		new("Thưởng thức Bánh mì nướng", "Chiếc bánh mì vỏ giòn ruột mềm thơm nức mũi.", () =>
		{
			InventoryManager.Instance?.AddItem("baguette", 1);
			return "Đầu bếp Gusteau tặng bạn 1 ổ Bánh Mì Baguette nóng hổi bỏ vào túi đồ!";
		}),
		new("Mua lương thực mang đi", "Gói lương khô dinh dưỡng cho hành trình dài.", () =>
		{
			InventoryManager.Instance?.AddItem("baguette", 2);
			return "Đã nhận 2 Ổ Bánh Mì Baguette Dã Ngoại vào túi đồ.";
		}),
		new("Hỏi thực đơn hôm nay", "Tìm hiểu các món ngon đặc sản làng.",
			() => "Đầu bếp cười lớn: 'Hôm nay có món súp bắp cải hầm cá suối nướng thơm phức!'")
	};

	private static List<NpcSpecialAction> CreateFarmerActions() => new()
	{
		new("Mua bắp cải tươi", "Những bắp cải xanh mọng nước hái tận vườn.", () =>
		{
			InventoryManager.Instance?.AddItem("cabbage", 2);
			return "Bác George tặng bạn 2 Bắp Cải Tươi Xanh ngon ngọt bỏ vào túi đồ!";
		}),
		new("Hỏi mùa vụ", "Trao đổi về thời tiết và điều kiện canh tác.",
			() => "Nông dân nói: 'Mảnh đất phù sa ven sông này gieo hạt gì cũng trổ bông mơn mởn!'")
	};

	private static List<NpcSpecialAction> CreateFishermanActions() => new()
	{
		new("Mua cá tươi", "Những chú cá suối ánh bạc tươi rói quẫy đuôi.", () =>
		{
			InventoryManager.Instance?.AddItem("fish", 2);
			return "Finn câu được 2 Chú Cá Suối Tươi Rói và trao vào túi đồ của bạn!";
		}),
		new("Bí quyết câu cá", "Kinh nghiệm chọn mồi và tìm luồng cá ngược dòng.",
			() => "Ngư dân dặn: 'Cứ lúc hoàng hôn hãy buông cần, cá đớp mồi rất hăng.'")
	};

	private static List<NpcSpecialAction> CreateMinerActions() => new()
	{
		new("Khai thác quặng sắt", "Giao dịch khoáng thô khai thác từ vách hang ngầm.", () =>
		{
			InventoryManager.Instance?.AddItem("iron_ore", 2);
			return "Brock trao cho bạn 2 Quặng Sắt Tinh Khiết khai thác dưới lòng đất!";
		}),
		new("Tin đồn trong hang mỏ", "Chuyện kỳ bí trong lòng vách đá sâu thẳm.",
			() => "Thợ mỏ hạ giọng: 'Đêm qua ta nghe thấy tiếng tinh thể pha lê reo vang trong hầm...'")
	};

	private static List<NpcSpecialAction> CreateLumberjackActions() => new()
	{
		new("Mua gỗ sồi xẻ", "Khối gỗ chắc nịch thích hợp gia cố đồ đạc.", () =>
		{
			InventoryManager.Instance?.AddItem("wood_log", 2);
			return "Grover trao tặng bạn 2 Bó Gỗ Sồi Cắt Xẻ Chất Lượng Cao vào túi đồ!";
		}),
		new("Chuyện rừng sâu", "Cảnh giác với những bí mật của cánh rừng Tây Bắc.",
			() => "Tiều phu chia sẻ: 'Cánh rừng này cổ xưa lắm, hãy luôn mang theo rìu phòng thân.'")
	};

	private static List<NpcSpecialAction> CreateGuardActions() => new()
	{
		new("Xin Chìa Khóa Cổng Làng", "Nhận chìa khóa an ninh để bảo vệ làng.", () =>
		{
			InventoryManager.Instance?.AddItem("key", 1);
			return "Lính canh trao cho bạn 1 Chìa Khóa Cổ Làng để mở cánh cổng chính!";
		}),
		new("Báo cáo an ninh làng", "Tình hình an ninh khu vực cổng làng và các lối mòn.",
			() => "Lính canh nghiêm trang: 'Khu vực an toàn tuyệt đối, không có quái vật xâm nhập.'")
	};
}
