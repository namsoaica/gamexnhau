using System.Collections.Generic;
using Godot;
using Game.Core;

namespace Game.Player;

/// <summary>
/// Quản lý việc dò tìm và kích hoạt các thực thể IInteractable xung quanh nhân vật người chơi.
/// </summary>
public partial class PlayerInteractor : Area3D
{
	[Signal] public delegate void FocusedTargetChangedEventHandler(Node3D? targetNode, string promptText);
	[Signal] public delegate void InteractionTriggeredEventHandler(Node3D targetNode);

	[ExportGroup("Cấu hình")]
	[Export] public string ActionName { get; set; } = "interact";
	[Export] public float ScanRadius { get; set; } = 3.0f;

	private readonly List<IInteractable> _availableInteractables = new();
	private IInteractable? _currentFocus;
	private ulong _lastInteractFrame;
	private const uint InteractMask = (1 << 2) | (1 << 3); // NPC (layer 3) + Interactable (layer 4)

	public override void _Ready()
	{
		Monitoring = true;
		Monitorable = false;
		CollisionLayer = 0;
		CollisionMask = InteractMask;

		EnsureCollisionShape();
		AreaEntered += OnAreaEntered;
		AreaExited += OnAreaExited;
	}

	public override void _ExitTree()
	{
		AreaEntered -= OnAreaEntered;
		AreaExited -= OnAreaExited;
	}

	public override void _PhysicsProcess(double delta)
	{
		PollOverlappingAreas();
		CheckPhysicalInteractInput();
	}

	public override void _UnhandledInput(InputEvent @event)
	{
		if (!IsInteractTriggered(@event)) return;
		TryExecuteInteraction();
	}

	/// <summary>
	/// Lấy mục tiêu tương tác đang được chọn ưu tiên hiện tại.
	/// </summary>
	public IInteractable? GetCurrentFocus() => _currentFocus;

	/// <summary>
	/// Kiểm tra phím tương tác trong vòng lặp vật lý để phản hồi tức thì, không nuốt phím.
	/// </summary>
	private void CheckPhysicalInteractInput()
	{
		if (InputMap.HasAction(ActionName) && Input.IsActionJustPressed(ActionName))
		{
			TryExecuteInteraction();
		}
	}

	/// <summary>
	/// Xử lý khi có vùng Area3D mới tiến vào phạm vi tương tác của người chơi.
	/// </summary>
	private void OnAreaEntered(Area3D area)
	{
		IInteractable? interactable = ResolveInteractable(area);
		if (interactable == null || _availableInteractables.Contains(interactable)) return;

		_availableInteractables.Add(interactable);
		UpdateCurrentFocus();
	}

	/// <summary>
	/// Xử lý khi vùng Area3D rời khỏi phạm vi tương tác của người chơi.
	/// </summary>
	private void OnAreaExited(Area3D area)
	{
		IInteractable? interactable = ResolveInteractable(area);
		if (interactable == null) return;

		_availableInteractables.Remove(interactable);
		UpdateCurrentFocus();
	}

	/// <summary>
	/// Quét bù các Area đang chồng lấn nếu sự kiện AreaEntered bị trễ khi khởi tạo.
	/// </summary>
	private void PollOverlappingAreas()
	{
		if (_availableInteractables.Count > 0) return;
		foreach (Area3D area in GetOverlappingAreas()) OnAreaEntered(area);
	}

	/// <summary>
	/// Tìm kiếm giao diện IInteractable, ưu tiên Node cha của Area3D.
	/// </summary>
	private IInteractable? ResolveInteractable(Area3D area) => area.GetParent() as IInteractable ?? area as IInteractable;

	/// <summary>
	/// Cập nhật mục tiêu gần nhất và phát tín hiệu cho UI.
	/// </summary>
	private void UpdateCurrentFocus()
	{
		IInteractable? bestTarget = FindBestTarget();
		if (ReferenceEquals(bestTarget, _currentFocus)) return;

		_currentFocus?.OnFocusLost();
		_currentFocus = bestTarget;
		_currentFocus?.OnFocusGained();

		Node3D? targetNode = _currentFocus as Node3D;
		string prompt = _currentFocus?.PromptText ?? string.Empty;
		Variant targetVariant = targetNode != null ? Variant.From(targetNode) : new Variant();
		EmitSignal(SignalName.FocusedTargetChanged, targetVariant, prompt);
	}

	/// <summary>
	/// Tìm mục tiêu tương tác có khoảng cách gần người chơi nhất.
	/// </summary>
	private IInteractable? FindBestTarget()
	{
		IInteractable? closest = null;
		float minDistanceSquared = float.MaxValue;
		Vector3 playerPos = GlobalPosition;

		foreach (IInteractable candidate in _availableInteractables)
		{
			if (!candidate.CanInteract() || candidate is not Node3D candidateNode) continue;
			float distSq = playerPos.DistanceSquaredTo(candidateNode.GlobalPosition);
			if (distSq < minDistanceSquared)
			{
				minDistanceSquared = distSq;
				closest = candidate;
			}
		}

		return closest;
	}

	/// <summary>
	/// Kiểm tra sự kiện bấm phím tương tác từ Input Map hoặc phím E dự phòng.
	/// </summary>
	private bool IsInteractTriggered(InputEvent @event)
	{
		if (InputMap.HasAction(ActionName) && @event.IsActionPressed(ActionName)) return true;
		return @event is InputEventKey key && key.Pressed && !key.Echo && (key.Keycode == Key.E || key.PhysicalKeycode == Key.E);
	}

	/// <summary>
	/// Thực thi tương tác trên mục tiêu đang được chọn ưu tiên (chống kích hoạt kép).
	/// </summary>
	private void TryExecuteInteraction()
	{
		ulong currentFrame = Engine.GetProcessFrames();
		if (currentFrame == _lastInteractFrame) return;
		_lastInteractFrame = currentFrame;

		if (PlayerUIBlocker.IsUIBlocking()) return;
		if (_currentFocus == null || !_currentFocus.CanInteract()) return;
		if (_currentFocus is Node3D targetNode) EmitSignal(SignalName.InteractionTriggered, targetNode);
		_currentFocus.Interact(this);
	}

	/// <summary>
	/// Tự động sinh CollisionShape3D hình cầu nếu trong Editor chưa tạo sẵn.
	/// </summary>
	private void EnsureCollisionShape()
	{
		foreach (Node child in GetChildren())
		{
			if (child is CollisionShape3D) return;
		}

		CollisionShape3D shapeNode = new CollisionShape3D
		{
			Position = new Vector3(0.0f, 1.0f, 0.0f),
			Shape = new SphereShape3D { Radius = ScanRadius }
		};
		AddChild(shapeNode);
	}
}
