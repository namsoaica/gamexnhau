using Godot;
using Game.Player;

namespace Game.UI;

/// <summary>
/// Tab dịch chuyển tức thời (Teleport) tới 8 phân khu và 4 phòng nội thất trên bản đồ làng.
/// </summary>
public partial class DevTeleportTab : VBoxContainer
{
	private record TeleportSpot(string Name, Vector3 Position);

	private static readonly TeleportSpot[] Spots =
	{
		new("🚪 Cổng Làng", new Vector3(0.0f, 0.5f, 17.5f)),
		new("🏪 Chợ Trung Tâm", new Vector3(0.0f, 0.5f, 2.0f)),
		new("🔨 Sân Nhà Rèn", new Vector3(-7.0f, 0.5f, 1.0f)),
		new("🏠 Trong Nhà Rèn", new Vector3(-10.0f, 0.5f, -2.0f)),
		new("🧪 Hiên Giả Kim", new Vector3(11.5f, 0.5f, 0.0f)),
		new("🏠 Trong Nhà Giả Kim", new Vector3(11.5f, 0.5f, -3.5f)),
		new("🥖 Quán Ăn / Bếp", new Vector3(10.0f, 0.5f, 8.0f)),
		new("🏠 Trong Quán Ăn", new Vector3(13.0f, 0.5f, 10.5f)),
		new("🏡 Sân Nhà Dân", new Vector3(-4.5f, 0.5f, 12.0f)),
		new("🏠 Trong Nhà Dân", new Vector3(-6.0f, 0.5f, 11.5f)),
		new("🪓 Khu Lâm Nghiệp", new Vector3(-12.0f, 0.5f, -13.0f)),
		new("⛏️ Khu Mỏ Đá", new Vector3(13.5f, 0.5f, -9.0f)),
		new("🥬 Vườn Rau Cải", new Vector3(-5.5f, 0.5f, 16.5f))
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
