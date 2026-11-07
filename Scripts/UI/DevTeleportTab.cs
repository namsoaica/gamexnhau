using Godot;
using Game.Player;

namespace Game.UI;

/// <summary>
/// Tab dịch chuyển tức thời (Teleport) tới các phân khu Đảo Đá, Làng Liền Kề và Nội Thất.
/// </summary>
public partial class DevTeleportTab : VBoxContainer
{
	private record TeleportSpot(string Name, Vector3 Position);

	private static readonly TeleportSpot[] Spots =
	{
		new("🏝️ Đảo Đá (Spawn)", new Vector3(6.0f, 2.5f, -6.0f)),
		new("🏰 Đài Vọng Cảnh Tầng 2", new Vector3(6.0f, 2.6f, 8.0f)),
		new("🚪 Cổng Làng", new Vector3(0.0f, 0.5f, 17.5f)),
		new("🥬 Vườn Rau Cải", new Vector3(-4.5f, 0.5f, 20.0f)),
		new("🥖 Quán Ăn / Bếp", new Vector3(7.0f, 0.5f, 24.0f)),
		new("🏠 Trong Quán Ăn", new Vector3(10.0f, 0.5f, 24.0f)),
		new("🏡 Sân Nhà Dân", new Vector3(-6.0f, 0.5f, 24.0f)),
		new("🏠 Trong Nhà Dân", new Vector3(-10.0f, 0.5f, 24.0f)),
		new("🏪 Chợ Trung Tâm", new Vector3(0.0f, 0.5f, 31.0f)),
		new("🔨 Sân Nhà Rèn", new Vector3(-6.5f, 0.5f, 35.0f)),
		new("🏠 Trong Nhà Rèn", new Vector3(-11.0f, 0.5f, 36.0f)),
		new("🧪 Hiên Giả Kim", new Vector3(7.5f, 0.5f, 35.0f)),
		new("🏠 Trong Nhà Giả Kim", new Vector3(11.0f, 0.5f, 36.0f)),
		new("🪓 Khu Lâm Nghiệp", new Vector3(-14.0f, 0.5f, 43.5f)),
		new("⛏️ Khu Mỏ Đá", new Vector3(14.0f, 0.5f, 42.5f))
	};

	private PlayerMovement? _player;
	private GridContainer? _grid;

	public override void _Ready()
	{
		BuildTeleportButtons();
	}

	public void Setup(PlayerMovement? player)
	{
		_player = player;
	}

	private void BuildTeleportButtons()
	{
		_grid = GetNodeOrNull<GridContainer>("Scroll/Grid");
		if (_grid == null)
		{
			ScrollContainer scroll = new() { SizeFlagsVertical = SizeFlags.ExpandFill };
			_grid = new GridContainer { Columns = 2, SizeFlagsHorizontal = SizeFlags.ExpandFill };
			scroll.AddChild(_grid);
			AddChild(scroll);
		}

		foreach (TeleportSpot spot in Spots)
		{
			Button btn = new()
			{
				Text = spot.Name,
				CustomMinimumSize = new Vector2(160, 34),
				SizeFlagsHorizontal = SizeFlags.ExpandFill
			};
			btn.Pressed += () => TeleportPlayerTo(spot.Position);
			_grid.AddChild(btn);
		}
	}

	private void TeleportPlayerTo(Vector3 target)
	{
		_player?.TeleportTo(target);
	}
}
