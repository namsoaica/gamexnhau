using Godot;
using Game.Player;
using Game.Inventory;

namespace Game.Core;

/// <summary>
/// Các phân loại đồ dùng nội thất có tính năng tương tác trong làng.
/// </summary>
public enum FurnitureType
{
	ForgeAndAnvil,    // Lò rèn & Đe sắt: Cường hóa vũ khí
	CauldronAlchemy,  // Vạc ma thuật & Bàn thí nghiệm: Pha chế độc dược
	OvenAndDining,    // Lò nướng & Bàn ăn: Nướng bánh hồi phục sinh lực
	BedAndStorage     // Giường ngủ & Tủ đồ: Nghỉ ngơi, lưu game và rương đồ
}

/// <summary>
/// Vùng tương tác nội thất đa năng, ban chức năng sử dụng cho các trang bị trong nhà.
/// </summary>
public partial class FurnitureInteractionArea : Area3D, IInteractable
{
	[Signal] public delegate void FurnitureUsedEventHandler(string title, string message);

	[ExportGroup("Cấu hình Nội Thất")]
	[Export] public FurnitureType Type { get; set; } = FurnitureType.ForgeAndAnvil;
	[Export] public string FurnitureTitle { get; set; } = "Nội Thất";
	[Export] public string CustomPrompt { get; set; } = string.Empty;
	[Export] public float InteractionRadius { get; set; } = 2.2f;
	[Export] public bool IsEnabled { get; set; } = true;

	[ExportGroup("Hiển Thị 3D")]
	[Export] public Label3D? OverheadLabel { get; set; }

	public string PromptText => !string.IsNullOrEmpty(CustomPrompt) ? CustomPrompt : GetDefaultPrompt();

	private const uint InteractableLayer = (1 << 2) | (1 << 3);
	private float _feedbackTimer;
	private bool _isShowingFeedback;

	public override void _Ready()
	{
		Monitoring = false;
		Monitorable = true;
		CollisionLayer = InteractableLayer;
		CollisionMask = 0;

		EnsureCollisionShape();
		EnsureOverheadLabel();
	}

	public override void _PhysicsProcess(double delta)
	{
		if (!_isShowingFeedback) return;
		_feedbackTimer -= (float)delta;
		if (_feedbackTimer <= 0.0f)
		{
			_isShowingFeedback = false;
			ResetOverheadDisplay();
		}
	}

	public bool CanInteract() => IsEnabled && IsInsideTree();

	public void Interact(Node3D interactor)
	{
		if (!CanInteract()) return;
		string response = ExecuteAction(interactor);
		ShowFeedback(response);
		EmitSignal(SignalName.FurnitureUsed, FurnitureTitle, response);
	}

	public void OnFocusGained()
	{
		if (OverheadLabel == null || _isShowingFeedback) return;
		OverheadLabel.Text = $"[{FurnitureTitle}]\n({PromptText})";
		OverheadLabel.Modulate = new Color(1.0f, 0.9f, 0.3f);
		OverheadLabel.Visible = true;
	}

	public void OnFocusLost()
	{
		if (OverheadLabel == null || _isShowingFeedback) return;
		OverheadLabel.Visible = false;
	}

	private string ExecuteAction(Node3D interactor) => Type switch
	{
		FurnitureType.ForgeAndAnvil => ExecuteForge(interactor),
		FurnitureType.CauldronAlchemy => ExecuteAlchemy(interactor),
		FurnitureType.OvenAndDining => ExecuteCooking(),
		FurnitureType.BedAndStorage => ExecuteRest(),
		_ => "Đã hoàn tất tương tác."
	};

	private string ExecuteForge(Node3D interactor)
	{
		PlayerCombat? combat = interactor.GetNodeOrNull<PlayerCombat>("PlayerCombat")
			?? (PlayerCombat?)GetTree().GetFirstNodeInGroup("Player")?.FindChild("PlayerCombat");

		if (combat != null) combat.AttackDamage += 2.0f;
		InventoryManager.Instance?.AddItem("iron_ore", 1);
		return "Đã cường hóa vũ khí (+2 Công) và tôi luyện thêm 1 Quặng Sắt!";
	}

	private string ExecuteAlchemy(Node3D interactor)
	{
		InventoryManager.Instance?.AddItem("potion_health", 1);
		return "Đã nấu thành công 1 Bình Máu Đỏ ma thuật bỏ vào túi đồ!";
	}

	private static string ExecuteCooking()
	{
		InventoryManager.Instance?.AddItem("baguette", 1);
		return "Đã nướng xong 1 Ổ Bánh Mì Baguette giòn thơm và bỏ vào túi đồ!";
	}

	private static string ExecuteRest()
	{
		ConfigFile save = new ConfigFile();
		save.SetValue("GameState", "LastRestTime", Time.GetUnixTimeFromSystem());
		save.Save("user://savegame.cfg");
		return "Đã nghỉ ngơi hồi phục thể lực, lưu dữ liệu game và sắp xếp rương đồ an toàn.";
	}

	private void ShowFeedback(string message)
	{
		if (OverheadLabel == null) return;
		OverheadLabel.Text = $"✨ [{FurnitureTitle}] ✨\n{message}";
		OverheadLabel.Modulate = new Color(0.4f, 1.0f, 0.6f);
		OverheadLabel.Visible = true;
		_isShowingFeedback = true;
		_feedbackTimer = 3.5f;
	}

	private void ResetOverheadDisplay()
	{
		if (OverheadLabel == null) return;
		OverheadLabel.Modulate = Colors.White;
		OverheadLabel.Visible = false;
	}

	private string GetDefaultPrompt() => Type switch
	{
		FurnitureType.ForgeAndAnvil => "Nhấn E để Rèn & Cường hóa vũ khí",
		FurnitureType.CauldronAlchemy => "Nhấn E để Pha chế độc dược ma thuật",
		FurnitureType.OvenAndDining => "Nhấn E để Nướng bánh & Thưởng thức",
		FurnitureType.BedAndStorage => "Nhấn E để Nghỉ ngơi & Mở rương",
		_ => "Nhấn E để tương tác"
	};

	private void EnsureCollisionShape()
	{
		foreach (Node child in GetChildren())
		{
			if (child is CollisionShape3D) return;
		}

		CollisionShape3D shape = new CollisionShape3D
		{
			Shape = new SphereShape3D { Radius = InteractionRadius },
			Position = new Vector3(0.0f, 0.5f, 0.0f)
		};
		AddChild(shape);
	}

	private void EnsureOverheadLabel()
	{
		OverheadLabel ??= (Label3D?)FindChild("OverheadLabel");
		if (OverheadLabel != null) return;

		Label3D lbl = new Label3D
		{
			Name = "OverheadLabel",
			Position = new Vector3(0.0f, 1.4f, 0.0f),
			Billboard = BaseMaterial3D.BillboardModeEnum.Enabled,
			NoDepthTest = true,
			FontSize = 30,
			OutlineSize = 6,
			OutlineModulate = new Color(0, 0, 0, 0.85f),
			Visible = false
		};
		AddChild(lbl);
		OverheadLabel = lbl;
	}
}
