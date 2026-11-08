namespace Game.Player;

/// <summary>
/// Kiểm tra các trạng thái giao diện modal (Túi đồ, Menu cài đặt, Hộp thoại NPC, DevTools)
/// để khóa điều khiển chuyển động và phím bấm vật lý của nhân vật.
/// </summary>
public static class PlayerUIBlocker
{
	public static bool IsUIBlocking()
	{
		if (Game.UI.InventoryUI.Instance?.IsOpen == true) return true;
		if (Game.UI.NpcInteractionDialog.Instance?.IsOpen == true) return true;
		if (Game.UI.SettingsMenu.Instance?.IsMenuOpen == true) return true;
		if (Game.UI.DevOverlay.Instance?.IsDevModeVisible == true) return true;
		return false;
	}
}
