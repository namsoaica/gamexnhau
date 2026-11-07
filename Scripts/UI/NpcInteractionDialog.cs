using Godot;
using System.Collections.Generic;
using Game.NPC;

namespace Game.UI;

/// <summary>
/// Giao diện hộp thoại và tùy chọn tương tác đặc biệt cho 8 dân làng.
/// </summary>
public partial class NpcInteractionDialog : CanvasLayer
{
	public static NpcInteractionDialog? Instance { get; private set; }

	[ExportGroup("Tham Chiếu Controls")]
	[Export] public Control? DialogPanel { get; set; }
	[Export] public TextureRect? AvatarRect { get; set; }
	[Export] public Label? NameLabel { get; set; }
	[Export] public Label? ProfessionLabel { get; set; }
	[Export] public Label? MessageLabel { get; set; }
	[Export] public VBoxContainer? ActionsContainer { get; set; }
	[Export] public Button? CloseButton { get; set; }

	private NpcBehavior? _currentNpc;

	public override void _Ready()
	{
		Instance = this;
		LocateControls();
		if (CloseButton != null)
		{
			CloseButton.Pressed += CloseDialog;
		}
		SetDialogVisible(false);
	}

	public override void _ExitTree()
	{
		if (Instance == this) Instance = null;
		if (CloseButton != null)
		{
			CloseButton.Pressed -= CloseDialog;
		}
	}

	public override void _UnhandledInput(InputEvent @event)
	{
		if (!Visible || DialogPanel == null || !DialogPanel.Visible) return;
		if (@event is InputEventKey key && key.Pressed && key.Keycode == Key.Escape)
		{
			CloseDialog();
			GetViewport().SetInputAsHandled();
		}
	}

	/// <summary>
	/// Mở hộp thoại tương tác chuyên biệt cho một NPC dân làng cụ thể.
	/// </summary>
	public void OpenForNpc(NpcBehavior npc)
	{
		_currentNpc = npc;
		PopulateNpcInfo(npc);
		PopulateSpecialActions(npc.Profession);
		SetDialogVisible(true);
	}

	/// <summary>
	/// Đóng hộp thoại và giải phóng NPC tiếp tục công việc.
	/// </summary>
	public void CloseDialog()
	{
		SetDialogVisible(false);
		_currentNpc?.FinishInteraction();
		_currentNpc = null;
	}

	private void SetDialogVisible(bool isVisible)
	{
		if (DialogPanel != null) DialogPanel.Visible = isVisible;
		Visible = isVisible;
		if (isVisible)
		{
			Input.MouseMode = Input.MouseModeEnum.Visible;
		}
	}

	private void PopulateNpcInfo(NpcBehavior npc)
	{
		if (AvatarRect != null)
		{
			AvatarRect.Texture = npc.GetAvatarTexture();
			AvatarRect.Visible = AvatarRect.Texture != null;
		}
		if (NameLabel != null) NameLabel.Text = npc.NpcName;
		if (ProfessionLabel != null) ProfessionLabel.Text = $"[{npc.Profession.GetVietnameseTitle()}]";
		if (MessageLabel != null) MessageLabel.Text = npc.Profession.GetDefaultGreeting();
	}

	private void PopulateSpecialActions(NpcProfession profession)
	{
		if (ActionsContainer == null) return;
		ClearOldActionButtons();

		List<NpcSpecialAction> actions = NpcSpecialActionManager.GetActions(profession);
		foreach (NpcSpecialAction action in actions)
		{
			Button btn = CreateActionButton(action);
			ActionsContainer.AddChild(btn);
		}
	}

	private Button CreateActionButton(NpcSpecialAction action)
	{
		Button btn = new Button
		{
			Text = $"▶ {action.Title}",
			CustomMinimumSize = new Vector2(0, 36),
			Alignment = HorizontalAlignment.Left
		};
		btn.Pressed += () =>
		{
			string response = action.Execute();
			if (MessageLabel != null) MessageLabel.Text = response;
		};
		return btn;
	}

	private void ClearOldActionButtons()
	{
		if (ActionsContainer == null) return;
		foreach (Node child in ActionsContainer.GetChildren())
		{
			child.QueueFree();
		}
	}

	private void LocateControls()
	{
		DialogPanel ??= GetNodeOrNull<Control>("PanelContainer");
		AvatarRect ??= GetNodeOrNull<TextureRect>("PanelContainer/VBox/Header/AvatarRect");
		NameLabel ??= GetNodeOrNull<Label>("PanelContainer/VBox/Header/TitleBox/NameLabel");
		ProfessionLabel ??= GetNodeOrNull<Label>("PanelContainer/VBox/Header/TitleBox/ProfLabel");
		MessageLabel ??= GetNodeOrNull<Label>("PanelContainer/VBox/MessageLabel");
		ActionsContainer ??= GetNodeOrNull<VBoxContainer>("PanelContainer/VBox/Scroll/ActionsList");
		CloseButton ??= GetNodeOrNull<Button>("PanelContainer/VBox/CloseButton");
	}
}
