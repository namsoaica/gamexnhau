using Godot;

namespace Game.Core;

/// <summary>
/// Giao diện chuẩn cho các thực thể có thể nhận sát thương (quái vật, nhân vật, vật thể phá hủy).
/// </summary>
public interface IDamageable
{
	/// <summary>
	/// Lượng máu hiện tại của thực thể.
	/// </summary>
	float CurrentHealth { get; }

	/// <summary>
	/// Lượng máu tối đa của thực thể.
	/// </summary>
	float MaxHealth { get; }

	/// <summary>
	/// Kiểm tra thực thể còn sống hay không.
	/// </summary>
	bool IsAlive { get; }

	/// <summary>
	/// Xử lý nhận sát thương từ nguồn tấn công.
	/// </summary>
	/// <param name="amount">Lượng sát thương gây ra.</param>
	/// <param name="attacker">Node gây ra đòn đánh.</param>
	void TakeDamage(float amount, Node3D? attacker = null);
}
