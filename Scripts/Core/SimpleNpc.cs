using Godot;

namespace Game.Core;

/// <summary>
/// Điều khiển hành vi NPC mẫu: cho phép tương tác và hiển thị lời thoại đơn giản trên đầu.
/// </summary>
public partial class SimpleNpc : Node3D, IInteractable
{
	[Signal]
	public delegate void DialogueSpokenEventHandler(string speakerName, string message);

	[ExportGroup("Thông Tin NPC")]
	[Export] public string NpcName { get; set; } = "Dân Làng";
	[Export] public string PromptText { get; set; } = "Nói chuyện (E)";
	[Export] public string[] DialogueLines { get; set; } = new string[]
	{
		"Xin chào nhà thám hiểm!",
		"Khu rừng phía trước rất nguy hiểm, hãy cẩn thận!",
		"Chúc bạn một chuyến phiêu lưu may mắn!"
	};

	[ExportGroup("Hiển Thị Thoại")]
	[Export] public Label3D? FloatingLabel { get; set; }

	private int _dialogueIndex = 0;
	private SceneTreeTimer? _hideTimer;
	private bool _isFocused = false;

	public override void _Ready()
	{
		SetupFloatingLabel();
	}

	public override void _ExitTree()
	{
		if (_hideTimer != null)
		{
			_hideTimer.Timeout -= OnDialogueTimeout;
			_hideTimer = null;
		}
	}

	/// <summary>
	/// Kiểm tra xem NPC có đang sẵn sàng trò chuyện hay không.
	/// </summary>
	public bool CanInteract() => IsInsideTree() && Visible;

	/// <summary>
	/// Kích hoạt nói chuyện: chuyển tiếp câu thoại và hiển thị nhãn chữ 3D.
	/// </summary>
	/// <param name="interactor">Node người chơi đang tương tác.</param>
	public void Interact(Node3D interactor)
	{
		if (!CanInteract() || DialogueLines.Length == 0)
		{
			return;
		}

		SpeakNextLine();
	}

	/// <summary>
	/// Hiện lời nhắc tương tác khi người chơi tiến vào phạm vi.
	/// </summary>
	public void OnFocusGained()
	{
		_isFocused = true;
		if (FloatingLabel == null)
		{
			return;
		}

		FloatingLabel.Text = $"[{NpcName}]\n(Ấn E để nói chuyện)";
		FloatingLabel.Visible = true;
	}

	/// <summary>
	/// Ẩn lời nhắc khi người chơi bước ra xa.
	/// </summary>
	public void OnFocusLost()
	{
		_isFocused = false;
		if (FloatingLabel != null)
		{
			FloatingLabel.Visible = false;
		}
	}

	/// <summary>
	/// Khởi tạo hoặc tìm kiếm nhãn Label3D trên đầu NPC nếu chưa được gán sẵn.
	/// </summary>
	private void SetupFloatingLabel()
	{
		FloatingLabel ??= (Label3D?)FindChild("FloatingLabel");

		if (FloatingLabel == null)
		{
			CreateDefaultLabel();
		}

		if (FloatingLabel != null)
		{
			FloatingLabel.Visible = false;
		}
	}

	/// <summary>
	/// Tạo tự động một Label3D billboard trên đầu NPC nếu trong scene chưa có sẵn.
	/// </summary>
	private void CreateDefaultLabel()
	{
		Label3D newLabel = new Label3D();
		newLabel.Name = "FloatingLabel";
		newLabel.Position = new Vector3(0.0f, 2.3f, 0.0f);
		newLabel.Billboard = BaseMaterial3D.BillboardModeEnum.Enabled;
		newLabel.NoDepthTest = true;
		newLabel.FontSize = 36;
		newLabel.OutlineSize = 8;
		newLabel.Modulate = Colors.White;
		newLabel.OutlineModulate = Colors.Black;

		AddChild(newLabel);
		FloatingLabel = newLabel;
	}

	/// <summary>
	/// Đọc câu thoại tiếp theo trong danh sách và cập nhật hiển thị.
	/// </summary>
	public void SpeakNextLine()
	{
		if (DialogueLines.Length == 0) return;
		_dialogueIndex %= DialogueLines.Length;
		string currentMessage = DialogueLines[_dialogueIndex];
		_dialogueIndex = (_dialogueIndex + 1) % DialogueLines.Length;

		DisplayMessage(currentMessage);
		EmitSignal(SignalName.DialogueSpoken, NpcName, currentMessage);
		GD.PrintRich($"[color=green][TƯƠNG TÁC THÀNH CÔNG][/color] [{NpcName}]: {currentMessage}");
	}

	/// <summary>
	/// Hiển thị lời thoại lên nhãn 3D và tự động hẹn giờ ẩn sau 4 giây.
	/// </summary>
	public void DisplayMessage(string message)
	{
		if (FloatingLabel == null)
		{
			return;
		}

		FloatingLabel.Text = $"[{NpcName}]\n\"{message}\"";
		FloatingLabel.Visible = true;

		if (_hideTimer != null)
		{
			_hideTimer.Timeout -= OnDialogueTimeout;
		}

		_hideTimer = GetTree().CreateTimer(4.0);
		_hideTimer.Timeout += OnDialogueTimeout;
	}

	/// <summary>
	/// Hết thời gian thoại: phục hồi lời nhắc tiếp tục nếu người chơi vẫn ở gần, hoặc ẩn đi.
	/// </summary>
	private void OnDialogueTimeout()
	{
		if (FloatingLabel == null || !IsInsideTree())
		{
			return;
		}

		if (_isFocused)
		{
			FloatingLabel.Text = $"[{NpcName}]\n(Ấn E để tiếp tục trò chuyện)";
			FloatingLabel.Visible = true;
			return;
		}

		FloatingLabel.Visible = false;
	}
}
