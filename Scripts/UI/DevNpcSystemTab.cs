using Godot;
using System.Collections.Generic;
using Game.NPC;
using Game.Player;

namespace Game.UI;

/// <summary>
/// Tab giám sát và điều khiển trạng thái 8 NPC trong hệ thống làng.
/// </summary>
public partial class DevNpcSystemTab : VBoxContainer
{
	[Export] public OptionButton? NpcDropdown { get; set; }
	[Export] public Label? StateLabel { get; set; }
	[Export] public Button? TeleportToNpcBtn { get; set; }
	[Export] public Button? SummonNpcBtn { get; set; }
	[Export] public Button? ForceIdleBtn { get; set; }
	[Export] public Button? ForceWorkBtn { get; set; }
	[Export] public Button? ForcePatrolBtn { get; set; }

	private readonly List<NpcBehavior> _npcs = new();
	private PlayerMovement? _player;
	private NpcBehavior? _selectedNpc;

	public override void _Ready()
	{
		LocateControls();
		ScanAllNpcs();
		BindEvents();
	}

	public override void _ExitTree()
	{
		UnbindEvents();
	}

	public void Setup(PlayerMovement? player)
	{
		_player = player;
	}

	public override void _Process(double delta)
	{
		UpdateStatusDisplay();
	}

	private void ScanAllNpcs()
	{
		_npcs.Clear();
		if (NpcDropdown != null) NpcDropdown.Clear();

		foreach (Node node in GetTree().GetNodesInGroup("VillageNPC"))
		{
			if (node is NpcBehavior npc) _npcs.Add(npc);
		}

		if (_npcs.Count == 0)
		{
			FindNpcsRecursive(GetTree().Root);
		}

		PopulateDropdown();
	}

	private void FindNpcsRecursive(Node parent)
	{
		if (parent is NpcBehavior npc && !_npcs.Contains(npc)) _npcs.Add(npc);
		foreach (Node child in parent.GetChildren())
		{
			FindNpcsRecursive(child);
		}
	}

	private void PopulateDropdown()
	{
		if (NpcDropdown == null) return;
		for (int i = 0; i < _npcs.Count; i++)
		{
			NpcBehavior n = _npcs[i];
			NpcDropdown.AddItem($"[{n.Profession.GetVietnameseTitle()}] {n.NpcName}", i);
		}

		if (_npcs.Count > 0)
		{
			NpcDropdown.Select(0);
			_selectedNpc = _npcs[0];
		}
	}

	private void BindEvents()
	{
		if (NpcDropdown != null) NpcDropdown.ItemSelected += OnNpcSelected;
		if (TeleportToNpcBtn != null) TeleportToNpcBtn.Pressed += OnTeleportToNpc;
		if (SummonNpcBtn != null) SummonNpcBtn.Pressed += OnSummonNpc;
		if (ForceIdleBtn != null) ForceIdleBtn.Pressed += () => _selectedNpc?.SetState(NpcState.Idle);
		if (ForceWorkBtn != null) ForceWorkBtn.Pressed += () => _selectedNpc?.SetState(NpcState.Working);
		if (ForcePatrolBtn != null) ForcePatrolBtn.Pressed += () => _selectedNpc?.SetState(NpcState.Patrolling);
	}

	private void UnbindEvents()
	{
		if (NpcDropdown != null) NpcDropdown.ItemSelected -= OnNpcSelected;
		if (TeleportToNpcBtn != null) TeleportToNpcBtn.Pressed -= OnTeleportToNpc;
		if (SummonNpcBtn != null) SummonNpcBtn.Pressed -= OnSummonNpc;
	}

	private void OnNpcSelected(long index)
	{
		if (index >= 0 && index < _npcs.Count)
		{
			_selectedNpc = _npcs[(int)index];
		}
	}

	private void OnTeleportToNpc()
	{
		if (_selectedNpc == null || _player == null) return;
		_player.TeleportTo(_selectedNpc.GlobalPosition + new Vector3(1.2f, 0.1f, 1.2f));
	}

	private void OnSummonNpc()
	{
		if (_selectedNpc == null || _player == null) return;
		_selectedNpc.GlobalPosition = _player.GlobalPosition + new Vector3(1.2f, 0.1f, 1.2f);
	}

	private void UpdateStatusDisplay()
	{
		if (StateLabel == null || _selectedNpc == null) return;
		Vector3 pos = _selectedNpc.GlobalPosition;
		StateLabel.Text = $"Trạng thái: {_selectedNpc.CurrentState}\nVị trí: ({pos.X:F1}, {pos.Y:F1}, {pos.Z:F1})";
	}

	private void LocateControls()
	{
		NpcDropdown ??= GetNodeOrNull<OptionButton>("DropdownRow/NpcDropdown");
		StateLabel ??= GetNodeOrNull<Label>("StateLabel");
		TeleportToNpcBtn ??= GetNodeOrNull<Button>("Actions/TeleportToNpcBtn");
		SummonNpcBtn ??= GetNodeOrNull<Button>("Actions/SummonNpcBtn");
		ForceIdleBtn ??= GetNodeOrNull<Button>("ForceStateRow/ForceIdleBtn");
		ForceWorkBtn ??= GetNodeOrNull<Button>("ForceStateRow/ForceWorkBtn");
		ForcePatrolBtn ??= GetNodeOrNull<Button>("ForceStateRow/ForcePatrolBtn");
	}
}
