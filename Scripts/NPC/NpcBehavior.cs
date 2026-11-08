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

	[Export] public string NpcName { get; set; } = "Dân Làng";
	[Export] public NpcProfession Profession { get; set; } = NpcProfession.Farmer;
	[Export] public NpcState CurrentState { get; set; } = NpcState.Idle;
	[Export] public bool Use3DModel { get; set; } = true;
	[Export] public float MoveSpeed { get; set; } = 1.8f;
	[Export] public Godot.Collections.Array<Vector3> Waypoints { get; set; } = new();
	[Export] public Node3D? VisualModel { get; set; }
	[Export] public Sprite3D? NpcSprite { get; set; }
	[Export] public Label3D? OverheadLabel { get; set; }

	public string PromptText => $"Nhấn E để nói chuyện với {NpcName}";
	public float SocialCooldown { get; set; }

	private NpcState _previousState = NpcState.Idle;
	private int _currentWaypointIndex;
	private float _stateTimer, _animTime, _talkDuration = 4.0f;

	public override void _Ready()
	{
		if (!IsInGroup("VillageNPC")) AddToGroup("VillageNPC");
		VisualModel ??= GetNodeOrNull<Node3D>("VisualModel") ?? GetNodeOrNull<Node3D>("CharacterModel");
		NpcSprite ??= GetNodeOrNull<Sprite3D>("NpcSprite");
		NpcVisualHelper.SetupVisuals(this, Profession, Use3DModel);
		OverheadLabel ??= GetNodeOrNull<Label3D>("OverheadLabel");
		UpdateOverheadText();
	}

	public override void _PhysicsProcess(double delta)
	{
		float dt = (float)delta;
		_animTime += dt;
		UpdateSocialCooldown(dt);

		switch (CurrentState)
		{
			case NpcState.Idle: ProcessIdleState(dt); break;
			case NpcState.Working: ProcessWorkingState(dt); break;
			case NpcState.Patrolling: ProcessPatrollingState(dt); break;
			case NpcState.TalkingWithNpc: ProcessTalkingState(dt); break;
			case NpcState.Interacting: Velocity = Vector3.Zero; break;
		}
	}

	public bool CanInteract() => CurrentState != NpcState.Interacting;

	public void Interact(Node3D interactor)
	{
		if (!CanInteract()) return;
		_previousState = CurrentState == NpcState.TalkingWithNpc ? NpcState.Idle : CurrentState;
		if (CurrentState == NpcState.TalkingWithNpc) FinishTalkingWithNpc();

		SetState(NpcState.Interacting);
		TurnTowards(interactor.GlobalPosition);
		NpcInteractionDialog.Instance?.OpenForNpc(this);
	}

	public void OnFocusGained()
	{
		if (OverheadLabel == null) return;
		OverheadLabel.Modulate = new Color(1.0f, 0.9f, 0.3f);
		OverheadLabel.Text = $"[{Profession.GetVietnameseTitle()}]\n{NpcName}\n(Nhấn E để nói chuyện)";
		LookAtPlayerIfNearby();
	}

	public void OnFocusLost()
	{
		if (OverheadLabel == null || CurrentState == NpcState.TalkingWithNpc) return;
		OverheadLabel.Modulate = Colors.White;
		UpdateOverheadText();
	}

	public void FinishInteraction() => SetState(_previousState == NpcState.Interacting ? NpcState.Idle : _previousState);

	public void SetState(NpcState newState)
	{
		if (CurrentState == newState) return;
		CurrentState = newState;
		_stateTimer = 0.0f;
		EmitSignal(SignalName.StateChanged, (int)newState);
	}

	public Texture2D? GetAvatarTexture() => NpcVisualHelper.LoadAvatar(Profession);

	public void TurnTowards(Vector3 targetPos)
	{
		Vector3 look = targetPos;
		look.Y = GlobalPosition.Y;
		if (GlobalPosition.DistanceSquaredTo(look) > 0.01f) LookAt(look, Vector3.Up);
	}

	public void BeginTalkingWith(NpcBehavior partner, string speechLine)
	{
		TurnTowards(partner.GlobalPosition);
		Velocity = Vector3.Zero;
		SetState(NpcState.TalkingWithNpc);
		_talkDuration = 4.0f;
		if (OverheadLabel == null) return;
		OverheadLabel.Text = $"💬 [{NpcName}]:\n\"{speechLine}\"";
		OverheadLabel.Modulate = new Color(1.0f, 0.95f, 0.45f);
	}

	public void FinishTalkingWithNpc()
	{
		SocialCooldown = 12.0f;
		if (OverheadLabel != null) OverheadLabel.Modulate = Colors.White;
		UpdateOverheadText();
		SetState(Waypoints.Count > 0 ? NpcState.Patrolling : NpcState.Idle);
	}

	private void UpdateSocialCooldown(float dt)
	{
		if (SocialCooldown > 0.0f)
		{
			SocialCooldown -= dt;
			return;
		}

		if (CurrentState == NpcState.Idle || CurrentState == NpcState.Patrolling)
		{
			NpcBehavior? partner = NpcSocialHelper.FindNearbyPartner(this);
			if (partner != null) NpcSocialHelper.StartConversation(this, partner);
		}
	}

	private void ProcessIdleState(float dt)
	{
		Velocity = Vector3.Zero;
		_stateTimer += dt;
		if (_stateTimer > 4.0f) SetState(Waypoints.Count > 0 ? NpcState.Patrolling : NpcState.Working);
	}

	private void ProcessWorkingState(float dt)
	{
		Velocity = Vector3.Zero;
		_stateTimer += dt;
		NpcVisualHelper.ApplyBobbing(VisualModel, NpcSprite, _animTime);
		if (_stateTimer <= 6.0f) return;
		NpcVisualHelper.ResetBobbing(VisualModel, NpcSprite);
		SetState(NpcState.Idle);
	}

	private void ProcessPatrollingState(float dt)
	{
		if (Waypoints.Count == 0) { SetState(NpcState.Idle); return; }
		Vector3 target = Waypoints[_currentWaypointIndex];
		Vector3 diff = new Vector3(target.X - GlobalPosition.X, 0, target.Z - GlobalPosition.Z);
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

	private void ProcessTalkingState(float dt)
	{
		Velocity = Vector3.Zero;
		_stateTimer += dt;
		if (_stateTimer >= _talkDuration) FinishTalkingWithNpc();
	}

	private void LookAtPlayerIfNearby()
	{
		Node3D? player = (Node3D?)GetTree().GetFirstNodeInGroup("Player");
		if (player != null && GlobalPosition.DistanceSquaredTo(player.GlobalPosition) < 25.0f) TurnTowards(player.GlobalPosition);
	}

	private void UpdateOverheadText()
	{
		if (OverheadLabel == null) return;
		OverheadLabel.Text = $"[{Profession.GetVietnameseTitle()}]\n{NpcName}";
		OverheadLabel.Billboard = BaseMaterial3D.BillboardModeEnum.Enabled;
		OverheadLabel.NoDepthTest = true;
	}
}
