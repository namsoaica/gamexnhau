using Godot;

namespace Game.Core;

/// <summary>
/// Giao diện chuẩn cho mọi thực thể có thể tương tác trong thế giới game (NPC, rương, cửa).
/// </summary>
public interface IInteractable
{
	/// <summary>
	/// Nội dung hiển thị hướng dẫn khi người chơi tiếp cận (ví dụ: "Nói chuyện", "Mở rương").
	/// </summary>
	string PromptText { get; }

	/// <summary>
	/// Kiểm tra xem thực thể hiện tại có đang cho phép tương tác hay không.
	/// </summary>
	bool CanInteract();

	/// <summary>
	/// Kích hoạt hành động tương tác chính khi người chơi bấm nút tương tác.
	/// </summary>
	/// <param name="interactor">Node người chơi thực hiện tương tác.</param>
	void Interact(Node3D interactor);

	/// <summary>
	/// Được gọi khi người chơi tiến vào phạm vi và nhắm trúng mục tiêu này.
	/// </summary>
	void OnFocusGained() { }

	/// <summary>
	/// Được gọi khi người chơi rời khỏi phạm vi hoặc chuyển sang mục tiêu khác.
	/// </summary>
	void OnFocusLost() { }
}
