using Godot;
using System.Collections.Generic;
using Game.Inventory;

namespace Game.UI;

/// <summary>
/// Giao diện lưới túi đồ 4x4 hỗ trợ chuột, bàn phím và tay cầm gamepad 100%.
/// </summary>
public partial class InventoryUI : CanvasLayer
{
	public static InventoryUI? Instance { get; private set; }

	[ExportGroup("Tham Chiếu Controls")]
	[Export] public Control? MainPanel { get; set; }
	[Export] public GridContainer? SlotsGrid { get; set; }
	[Export] public Label? ItemNameLabel { get; set; }
	[Export] public Label? ItemTypeLabel { get; set; }
	[Export] public Label? ItemDescLabel { get; set; }
	[Export] public Button? CloseButton { get; set; }
	[Export] public Label? StatusFeedbackLabel { get; set; }

	private readonly List<Button> _slotButtons = new();
	private int _focusedSlotIndex = -1;

	public bool IsOpen => MainPanel?.Visible ?? false;

	public override void _Ready()
	{
		Instance = this;
		LocateControls();
		CreateSlotButtons();
		BindEvents();
		SetInventoryOpen(false);
	}

	public override void _ExitTree()
	{
		if (Instance == this) Instance = null;
		UnbindEvents();
		_slotButtons.Clear();
	}

	public override void _UnhandledInput(InputEvent @event)
	{
		if (HandleToggleInput(@event)) return;
		if (!IsOpen) return;

		if (@event.IsActionPressed("ui_cancel") || IsGamepadCancel(@event))
		{
			SetInventoryOpen(false);
			GetViewport().SetInputAsHandled();
		}
	}

	public void ToggleInventory() => SetInventoryOpen(!IsOpen);

	public void SetInventoryOpen(bool open)
	{
		if (MainPanel != null) MainPanel.Visible = open;
		if (!open) return;

		Input.MouseMode = Input.MouseModeEnum.Visible;
		RefreshSlots();
		FocusInitialSlot();
	}

	private void CreateSlotButtons()
	{
		if (SlotsGrid == null) return;
		_slotButtons.Clear();

		for (int i = 0; i < InventoryManager.MaxSlots; i++)
		{
			int slotIndex = i;
			Button slotBtn = BuildSlotButton(slotIndex);
			SlotsGrid.AddChild(slotBtn);
			_slotButtons.Add(slotBtn);
		}
	}

	private Button BuildSlotButton(int slotIndex)
	{
		Button btn = new Button
		{
			CustomMinimumSize = new Vector2(68, 68),
			FocusMode = Control.FocusModeEnum.All
		};
		btn.Pressed += () => OnSlotPressed(slotIndex);
		btn.FocusEntered += () => OnSlotFocused(slotIndex);
		return btn;
	}

	private void RefreshSlots()
	{
		IReadOnlyList<InventoryItem>? items = InventoryManager.Instance?.GetItems();
		int count = items?.Count ?? 0;

		for (int i = 0; i < _slotButtons.Count; i++)
		{
			Button btn = _slotButtons[i];
			if (items != null && i < count) InventorySlotBinder.DisplayItemOnSlot(btn, items[i]);
			else InventorySlotBinder.ClearSlotDisplay(btn);
		}
		UpdateItemDetails(_focusedSlotIndex);
	}

	private void OnSlotPressed(int slotIndex)
	{
		InventoryManager? mgr = InventoryManager.Instance;
		if (mgr == null) return;

		bool success = mgr.UseItem(slotIndex);
		if (success && StatusFeedbackLabel != null) StatusFeedbackLabel.Text = "Đã dùng vật phẩm!";
		RefreshSlots();
	}

	private void OnSlotFocused(int slotIndex)
	{
		_focusedSlotIndex = slotIndex;
		UpdateItemDetails(slotIndex);
	}

	private void UpdateItemDetails(int slotIndex)
	{
		IReadOnlyList<InventoryItem>? items = InventoryManager.Instance?.GetItems();
		if (items == null || slotIndex < 0 || slotIndex >= items.Count)
		{
			SetDetailsText("Ô trống", "Chưa có đồ", "Hãy khám phá làng để thu thập vật phẩm.");
			return;
		}

		InventoryItem item = items[slotIndex];
		SetDetailsText(item.Name, InventorySlotBinder.ResolveTypeName(item.Type), item.Description);
	}

	private void SetDetailsText(string name, string type, string desc)
	{
		if (ItemNameLabel != null) ItemNameLabel.Text = name;
		if (ItemTypeLabel != null) ItemTypeLabel.Text = $"[{type}]";
		if (ItemDescLabel != null) ItemDescLabel.Text = desc;
	}

	private void FocusInitialSlot()
	{
		if (_slotButtons.Count > 0)
		{
			_slotButtons[0].GrabFocus();
			_focusedSlotIndex = 0;
			UpdateItemDetails(0);
		}
	}

	private bool HandleToggleInput(InputEvent @event)
	{
		if (@event.IsActionPressed("inventory"))
		{
			ToggleInventory();
			GetViewport().SetInputAsHandled();
			return true;
		}
		return false;
	}

	private static bool IsGamepadCancel(InputEvent @event)
	{
		return @event is InputEventJoypadButton joy && joy.Pressed && joy.ButtonIndex == JoyButton.B;
	}

	private void BindEvents()
	{
		if (CloseButton != null) CloseButton.Pressed += OnCloseButtonPressed;
		if (InventoryManager.Instance != null) InventoryManager.Instance.InventoryChanged += RefreshSlots;
	}

	private void UnbindEvents()
	{
		if (CloseButton != null) CloseButton.Pressed -= OnCloseButtonPressed;
		if (InventoryManager.Instance != null) InventoryManager.Instance.InventoryChanged -= RefreshSlots;
	}

	private void OnCloseButtonPressed() => SetInventoryOpen(false);

	private void LocateControls()
	{
		MainPanel ??= GetNodeOrNull<Control>("MainPanel");
		SlotsGrid ??= GetNodeOrNull<GridContainer>("MainPanel/Margin/HBox/LeftBox/SlotsGrid");
		ItemNameLabel ??= GetNodeOrNull<Label>("MainPanel/Margin/HBox/RightBox/ItemNameLabel");
		ItemTypeLabel ??= GetNodeOrNull<Label>("MainPanel/Margin/HBox/RightBox/ItemTypeLabel");
		ItemDescLabel ??= GetNodeOrNull<Label>("MainPanel/Margin/HBox/RightBox/ItemDescLabel");
		CloseButton ??= GetNodeOrNull<Button>("MainPanel/Margin/HBox/RightBox/CloseBtn");
		StatusFeedbackLabel ??= GetNodeOrNull<Label>("MainPanel/Margin/HBox/RightBox/FeedbackLabel");
	}
}
