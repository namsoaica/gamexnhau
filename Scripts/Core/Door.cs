using Godot;

namespace Game.Core;

/// <summary>
/// Chế độ hoạt động đóng/mở của cánh cửa làng.
/// </summary>
public enum DoorMode
{
	Manual,    // Chỉ mở/đóng thủ công qua tương tác (phím E / Gamepad X)
	Automatic, // Tự động mở khi lại gần (2m) và tự đóng sau 1.5s khi rời đi
	Hybrid     // Kết hợp cả hai: tự động mở/đóng và cho phép bấm nút điều khiển
}

/// <summary>
/// Thực thể cánh cửa đóng mở mượt mà bằng Tween và xoay quanh bản lề Pivot X=0.
/// </summary>
public partial class Door : Node3D, IInteractable
{
	[Signal] public delegate void DoorStateChangedEventHandler(bool isOpen);

	[ExportGroup("Cấu hình Cửa")]
	[Export] public DoorMode Mode { get; set; } = DoorMode.Hybrid;
	[Export] public float OpenAngleDegrees { get; set; } = 90.0f;
	[Export] public bool InvertOpenDirection { get; set; } = false;
	[Export] public float AnimationDuration { get; set; } = 0.55f;
	[Export] public float AutoCloseDelay { get; set; } = 1.5f;

	[ExportGroup("Tham Chiếu Nodes")]
	[Export] public Node3D? DoorHinge { get; set; }
	[Export] public Area3D? DetectionArea { get; set; }
	[Export] public Label3D? OverheadLabel { get; set; }

	public bool IsOpen { get; private set; }
	public bool IsAnimating { get; private set; }
	public string PromptText => IsOpen ? "Nhấn E để Đóng Cửa" : "Nhấn E để Mở Cửa";

	private int _playerOverlapCount;
	private Tween? _tween;

	public override void _Ready()
	{
		LocateNodesIfNull();
		BindDetectionEvents();
		UpdateLabelPrompt();
	}

	public override void _ExitTree()
	{
		_tween?.Kill();
		UnbindDetectionEvents();
	}

	public bool CanInteract() => Mode != DoorMode.Automatic && !IsAnimating;

	public void Interact(Node3D interactor)
	{
		if (!CanInteract()) return;
		ToggleDoor();
	}

	public void OnFocusGained()
	{
		if (OverheadLabel != null && Mode != DoorMode.Automatic) OverheadLabel.Visible = true;
	}

	public void OnFocusLost()
	{
		if (OverheadLabel != null) OverheadLabel.Visible = false;
	}

	public void ToggleDoor()
	{
		if (IsOpen) CloseDoor();
		else OpenDoor();
	}

	public void OpenDoor()
	{
		if (IsOpen || IsAnimating || DoorHinge == null) return;
		float targetAngle = InvertOpenDirection ? -OpenAngleDegrees : OpenAngleDegrees;
		AnimateRotation(Mathf.DegToRad(targetAngle), true);
	}

	public void CloseDoor()
	{
		if (!IsOpen || IsAnimating || DoorHinge == null) return;
		AnimateRotation(0.0f, false);
	}

	private void AnimateRotation(float targetAngleRad, bool targetState)
	{
		if (DoorHinge == null) return;
		_tween?.Kill();
		IsAnimating = true;

		_tween = CreateTween().SetEase(Tween.EaseType.Out).SetTrans(Tween.TransitionType.Cubic);
		_tween.TweenProperty(DoorHinge, "rotation:y", targetAngleRad, AnimationDuration);
		_tween.TweenCallback(Callable.From(() =>
		{
			IsOpen = targetState;
			IsAnimating = false;
			UpdateLabelPrompt();
			EmitSignal(SignalName.DoorStateChanged, IsOpen);
		}));
	}

	private void OnDetectionBodyEntered(Node3D body)
	{
		if (!IsPlayer(body)) return;
		_playerOverlapCount++;
		if (Mode == DoorMode.Manual) return;
		OpenDoor();
	}

	private void OnDetectionBodyExited(Node3D body)
	{
		if (!IsPlayer(body)) return;
		_playerOverlapCount = Mathf.Max(0, _playerOverlapCount - 1);
		if (_playerOverlapCount > 0 || Mode == DoorMode.Manual) return;

		SceneTreeTimer timer = GetTree().CreateTimer(AutoCloseDelay);
		timer.Timeout += () =>
		{
			if (_playerOverlapCount == 0 && IsOpen) CloseDoor();
		};
	}

	private static bool IsPlayer(Node3D body) => body.IsInGroup("Player") || body.Name == "Player";

	private void UpdateLabelPrompt()
	{
		if (OverheadLabel == null) return;
		OverheadLabel.Text = PromptText;
	}

	private void BindDetectionEvents()
	{
		if (DetectionArea == null) return;
		DetectionArea.BodyEntered += OnDetectionBodyEntered;
		DetectionArea.BodyExited += OnDetectionBodyExited;
	}

	private void UnbindDetectionEvents()
	{
		if (DetectionArea == null) return;
		DetectionArea.BodyEntered -= OnDetectionBodyEntered;
		DetectionArea.BodyExited -= OnDetectionBodyExited;
	}

	private void LocateNodesIfNull()
	{
		DoorHinge ??= GetNodeOrNull<Node3D>("DoorHinge");
		DetectionArea ??= GetNodeOrNull<Area3D>("DetectionArea");
		OverheadLabel ??= GetNodeOrNull<Label3D>("OverheadLabel");
	}
}
