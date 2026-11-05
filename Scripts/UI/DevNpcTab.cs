using System;
using Godot;
using Game.Core;

namespace Game.UI;

/// <summary>
/// Quản lý giao diện chỉnh sửa trực tiếp lời thoại của NPC trong thời gian thực (Live Dialogue Editor).
/// </summary>
public partial class DevNpcTab : VBoxContainer
{
	[Export] public Label? NpcNameLabel { get; set; }
	[Export] public ItemList? DialogueList { get; set; }
	[Export] public LineEdit? DialogueInput { get; set; }
	[Export] public Button? AddDialogueBtn { get; set; }
	[Export] public Button? SpeakNowBtn { get; set; }
	[Export] public Button? CycleDialogueBtn { get; set; }
	[Export] public Button? DeleteDialogueBtn { get; set; }

	private SimpleNpc? _npc;

	public override void _ExitTree()
	{
		DisconnectEvents();
	}

	/// <summary>
	/// Khởi tạo và liên kết NPC với bảng điều khiển thoại.
	/// </summary>
	public void Setup(SimpleNpc? npc)
	{
		_npc = npc;
		FindNodesIfNull();
		if (_npc == null) return;

		UpdateNpcInfo();
		RefreshDialogueList();
		ConnectEvents();
	}

	/// <summary>
	/// Tự động tìm kiếm các Control con nếu chưa được gán trên Inspector.
	/// </summary>
	private void FindNodesIfNull()
	{
		NpcNameLabel ??= GetNodeOrNull<Label>("NpcNameLabel");
		DialogueList ??= GetNodeOrNull<ItemList>("DialogueList");
		DialogueInput ??= GetNodeOrNull<LineEdit>("DialogueInput");
		AddDialogueBtn ??= GetNodeOrNull<Button>("ActionsRow/AddBtn");
		SpeakNowBtn ??= GetNodeOrNull<Button>("ActionsRow/SpeakNowBtn");
		CycleDialogueBtn ??= GetNodeOrNull<Button>("ActionsRow2/CycleBtn");
		DeleteDialogueBtn ??= GetNodeOrNull<Button>("ActionsRow2/DeleteBtn");
	}

	/// <summary>
	/// Cập nhật hiển thị tên NPC.
	/// </summary>
	private void UpdateNpcInfo()
	{
		if (_npc == null || NpcNameLabel == null) return;
		NpcNameLabel.Text = $"NPC: {_npc.NpcName}";
	}

	/// <summary>
	/// Làm mới danh sách câu thoại hiển thị trong ItemList.
	/// </summary>
	public void RefreshDialogueList()
	{
		if (_npc == null || DialogueList == null) return;
		DialogueList.Clear();

		for (int i = 0; i < _npc.DialogueLines.Length; i++)
		{
			DialogueList.AddItem($"{i + 1}. {_npc.DialogueLines[i]}");
		}
	}

	/// <summary>
	/// Kết nối các sự kiện nút bấm.
	/// </summary>
	private void ConnectEvents()
	{
		if (AddDialogueBtn != null) AddDialogueBtn.Pressed += OnAddDialoguePressed;
		if (SpeakNowBtn != null) SpeakNowBtn.Pressed += OnSpeakNowPressed;
		if (CycleDialogueBtn != null) CycleDialogueBtn.Pressed += OnCycleDialoguePressed;
		if (DeleteDialogueBtn != null) DeleteDialogueBtn.Pressed += OnDeleteDialoguePressed;
	}

	/// <summary>
	/// Hủy kết nối sự kiện an toàn bộ nhớ.
	/// </summary>
	private void DisconnectEvents()
	{
		if (AddDialogueBtn != null) AddDialogueBtn.Pressed -= OnAddDialoguePressed;
		if (SpeakNowBtn != null) SpeakNowBtn.Pressed -= OnSpeakNowPressed;
		if (CycleDialogueBtn != null) CycleDialogueBtn.Pressed -= OnCycleDialoguePressed;
		if (DeleteDialogueBtn != null) DeleteDialogueBtn.Pressed -= OnDeleteDialoguePressed;
	}

	/// <summary>
	/// Thêm câu thoại mới từ ô nhập vào danh sách câu thoại của NPC.
	/// </summary>
	private void OnAddDialoguePressed()
	{
		if (_npc == null || DialogueInput == null) return;
		string text = DialogueInput.Text.Trim();
		if (string.IsNullOrEmpty(text)) return;

		string[] oldArr = _npc.DialogueLines;
		string[] newArr = new string[oldArr.Length + 1];
		Array.Copy(oldArr, newArr, oldArr.Length);
		newArr[^1] = text;

		_npc.DialogueLines = newArr;
		DialogueInput.Text = string.Empty;
		RefreshDialogueList();
	}

	/// <summary>
	/// Bắt NPC phát ngay câu thoại đang gõ trong ô nhập hoặc câu đang chọn.
	/// </summary>
	private void OnSpeakNowPressed()
	{
		if (_npc == null) return;
		string text = DialogueInput?.Text.Trim() ?? string.Empty;

		if (string.IsNullOrEmpty(text) && DialogueList != null)
		{
			int[] selected = DialogueList.GetSelectedItems();
			if (selected.Length > 0 && selected[0] < _npc.DialogueLines.Length)
			{
				text = _npc.DialogueLines[selected[0]];
			}
		}

		if (string.IsNullOrEmpty(text)) return;
		_npc.DisplayMessage(text);
	}

	/// <summary>
	/// Chuyển tiếp và phát câu thoại tiếp theo theo vòng lặp.
	/// </summary>
	private void OnCycleDialoguePressed()
	{
		if (_npc == null) return;
		_npc.SpeakNextLine();
	}

	/// <summary>
	/// Xóa câu thoại được chọn hoặc xóa câu thoại cuối cùng.
	/// </summary>
	private void OnDeleteDialoguePressed()
	{
		if (_npc == null || _npc.DialogueLines.Length == 0) return;
		int targetIndex = _npc.DialogueLines.Length - 1;

		if (DialogueList != null && DialogueList.GetSelectedItems().Length > 0)
		{
			targetIndex = DialogueList.GetSelectedItems()[0];
		}

		string[] oldArr = _npc.DialogueLines;
		string[] newArr = new string[oldArr.Length - 1];
		int dest = 0;
		for (int i = 0; i < oldArr.Length; i++)
		{
			if (i == targetIndex) continue;
			newArr[dest++] = oldArr[i];
		}

		_npc.DialogueLines = newArr;
		RefreshDialogueList();
	}
}
