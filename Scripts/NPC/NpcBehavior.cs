using Godot;
using Game.Core;
using Game.UI;

namespace Game.NPC;

/// <summary>
/// Bộ điều khiển trí tuệ nhân tạo (AI Behavior) và tương tác chuyên biệt cho dân làng.
/// </summary>
public partial class NpcBehavior : CharacterBody3D, IInteractable
{
	[Signal] public delegate void StateChangedEventHandler(int newState);

	[ExportGroup("Thông Tin Dân Làng")]
	[Export] public string NpcName { get; set; } = "Dân Làng";
	[Export] public NpcProfession Profession { get; set; } = NpcProfession.Farmer;
	[Export] public NpcState CurrentState { get; set; } = NpcState.Idle;

	[ExportGroup("Di Chuyển & Tuần Tra")]
	[Export] public float MoveSpeed { get; set; } = 2.0f;
	[Export] public Godot.Collections.Array<Vector3> Waypoints { get; set; } = new();

	[ExportGroup("Tham Chiếu Node")]
	[Export] public Node3D? VisualModel { get; set; }
	[Export] public Label3D? OverheadLabel { get; set; }

	public string PromptText => $"Trò chuyện với {NpcName}";

	private NpcState _previousState = NpcState.Idle;
	private int _currentWaypointIndex;
	private float _stateTimer;
	private float _animTime;
	private Vector3 _initialPosition;

	public override void _Ready()
	{
		_initialPosition = GlobalPosition;
		VisualModel ??= GetNodeOrNull<Node3D>("VisualModel") ?? GetNodeOrNull<Node3D>("CharacterModel");
		OverheadLabel ??= GetNodeOrNull<Label3D>("OverheadLabel");
		UpdateOverheadText();
	}

	public override void _PhysicsProcess(double delta)
	{
		float dt = (float)delta;
		_animTime += dt;

		switch (CurrentState)
		{
			case NpcState.Idle:
				ProcessIdleState(dt);
				break;
			case NpcState.Working:
				ProcessWorkingState(dt);
				break;
			case NpcState.Patrolling:
				ProcessPatrollingState(dt);
				break;
			case NpcState.Interacting:
				Velocity = Vector3.Zero;
				break;
		}
	}

	public bool CanInteract() => CurrentState != NpcState.Interacting;

	public void Interact(Node3D interactor)
	{
		if (!CanInteract()) return;
		_previousState = CurrentState;
		SetState(NpcState.Interacting);
		TurnTowards(interactor.GlobalPosition);
		NpcInteractionDialog.Instance?.OpenForNpc(this);
	}

	public void OnFocusGained()
	{
		if (OverheadLabel != null) OverheadLabel.Modulate = new Color(1.0f, 0.9f, 0.3f);
	}

	public void OnFocusLost()
	{
		if (OverheadLabel != null) OverheadLabel.Modulate = Colors.White;
	}

	/// <summary>
	/// Kết thúc trạng thái đối thoại và quay về hành vi chu kỳ trước đó.
	/// </summary>
	public void FinishInteraction()
	{
		SetState(_previousState == NpcState.Interacting ? NpcState.Idle : _previousState);
	}

	public void SetState(NpcState newState)
	{
		if (CurrentState == newState) return;
		CurrentState = newState;
		_stateTimer = 0.0f;
		EmitSignal(SignalName.StateChanged, (int)newState);
	}

	private void ProcessIdleState(float dt)
	{
		Velocity = Vector3.Zero;
		_stateTimer += dt;
		if (_stateTimer > 4.0f)
		{
			SetState(Waypoints.Count > 0 ? NpcState.Patrolling : NpcState.Working);
		}
	}

	private void ProcessWorkingState(float dt)
	{
		Velocity = Vector3.Zero;
		_stateTimer += dt;
		ApplyProceduralWorkMotion();
		if (_stateTimer > 6.0f)
		{
			ResetWorkMotion();
			SetState(NpcState.Idle);
		}
	}

	private void ProcessPatrollingState(float dt)
	{
		if (Waypoints.Count == 0)
		{
			SetState(NpcState.Idle);
			return;
		}

		Vector3 target = Waypoints[_currentWaypointIndex];
		Vector3 diff = target - GlobalPosition;
		diff.Y = 0;

		if (diff.Length() < 0.4f)
		{
			_currentWaypointIndex = (_currentWaypointIndex + 1) % Waypoints.Count;
			SetState(NpcState.Idle);
			return;
		}

		Vector3 dir = diff.Normalized();
		Velocity = new Vector3(dir.X * MoveSpeed, Velocity.Y - 9.8f * dt, dir.Z * MoveSpeed);
		MoveAndSlide();
		TurnTowards(target);
	}

	private void ApplyProceduralWorkMotion()
	{
		if (VisualModel == null) return;
		float bob = Mathf.Sin(_animTime * 4.0f) * 0.04f;
		VisualModel.Position = new Vector3(VisualModel.Position.X, bob, VisualModel.Position.Z);
	}

	private void ResetWorkMotion()
	{
		if (VisualModel == null) return;
		VisualModel.Position = new Vector3(VisualModel.Position.X, 0, VisualModel.Position.Z);
	}

	private void TurnTowards(Vector3 targetPos)
	{
		Vector3 look = targetPos;
		look.Y = GlobalPosition.Y;
		if (GlobalPosition.DistanceSquaredTo(look) > 0.01f)
		{
			LookAt(look, Vector3.Up);
		}
	}

	private void UpdateOverheadText()
	{
		if (OverheadLabel == null) return;
		OverheadLabel.Text = $"[{Profession.GetVietnameseTitle()}]\n{NpcName}";
		OverheadLabel.Billboard = BaseMaterial3D.BillboardModeEnum.Enabled;
		OverheadLabel.NoDepthTest = true;
	}
}
