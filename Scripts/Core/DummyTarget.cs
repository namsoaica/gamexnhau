using Godot;

namespace Game.Core;

/// <summary>
/// Bia tập đánh (Training Dummy) triển khai IDamageable để kiểm thử hệ thống chiến đấu.
/// </summary>
public partial class DummyTarget : CharacterBody3D, IDamageable
{
	[Signal] public delegate void DamagedEventHandler(float currentHealth, float damageTaken);
	[Signal] public delegate void DefeatedEventHandler();

	[Export] public float MaxHealth { get; set; } = 100.0f;
	[Export] public float ResetDelay { get; set; } = 2.0f;

	public float CurrentHealth { get; private set; }
	public bool IsAlive => CurrentHealth > 0.0f;

	private float _resetTimer;
	private Vector3 _originalScale = Vector3.One;

	public override void _Ready()
	{
		CurrentHealth = MaxHealth;
		_originalScale = Scale;
		if (!IsInGroup("Enemy")) AddToGroup("Enemy");
	}

	public override void _Process(double delta)
	{
		if (IsAlive) return;
		_resetTimer -= (float)delta;
		if (_resetTimer <= 0.0f) ResetHealth();
	}

	/// <summary>
	/// Xử lý khi bị trúng đòn: trừ máu, phát hiệu ứng giật nhẹ và phát tín hiệu.
	/// </summary>
	public void TakeDamage(float amount, Node3D? attacker = null)
	{
		if (!IsAlive) return;
		CurrentHealth = Mathf.Max(0.0f, CurrentHealth - amount);
		EmitSignal(SignalName.Damaged, CurrentHealth, amount);

		PlayHitFlinch();
		if (CurrentHealth <= 0.0f)
		{
			_resetTimer = ResetDelay;
			EmitSignal(SignalName.Defeated);
		}
	}

	/// <summary>
	/// Hồi máu đầy lại sau khoảng thời gian đếm ngược.
	/// </summary>
	public void ResetHealth()
	{
		CurrentHealth = MaxHealth;
		Scale = _originalScale;
	}

	/// <summary>
	/// Hiệu ứng giật scale nhẹ khi bị đánh trúng.
	/// </summary>
	private void PlayHitFlinch()
	{
		Tween tween = CreateTween();
		tween.TweenProperty(this, "scale", _originalScale * 1.15f, 0.05);
		tween.TweenProperty(this, "scale", _originalScale, 0.1);
	}
}
