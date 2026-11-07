using Godot;

namespace Game.Core;

/// <summary>
/// Singleton quản lý cấu hình hiển thị, độ phân giải và giới hạn khung hình (FPS).
/// Hỗ trợ lưu trữ bền vững tại user://settings.cfg.
/// </summary>
public partial class DisplaySettingsManager : Node
{
	public static DisplaySettingsManager? Instance { get; private set; }

	private const string SettingsFilePath = "user://settings.cfg";
	private const string SectionDisplay = "Display";

	public static readonly Vector2I[] AvailableResolutions =
	{
		new(1280, 720),
		new(1600, 900),
		new(1920, 1080),
		new(2560, 1440),
		new(3840, 2160)
	};

	public static readonly int[] AvailableFpsLimits = { 30, 60, 120, 144, 0 };

	public Vector2I CurrentResolution { get; private set; } = new(1920, 1080);
	public DisplayServer.WindowMode CurrentWindowMode { get; private set; } = DisplayServer.WindowMode.Windowed;
	public int CurrentMaxFps { get; private set; } = 60;
	public DisplayServer.VSyncMode CurrentVSync { get; private set; } = DisplayServer.VSyncMode.Enabled;

	public override void _Ready()
	{
		Instance = this;
		LoadSettings();
		ApplyAllSettings();
	}

	public override void _ExitTree()
	{
		if (Instance == this) Instance = null;
	}

	public void SetResolution(Vector2I res)
	{
		CurrentResolution = res;
		DisplayServer.WindowSetSize(res);
		CenterWindow();
	}

	public void SetWindowMode(DisplayServer.WindowMode mode)
	{
		CurrentWindowMode = mode;
		DisplayServer.WindowSetMode(mode);
	}

	public void SetMaxFps(int fps)
	{
		CurrentMaxFps = fps;
		Engine.MaxFps = fps;
	}

	public void SetVSync(DisplayServer.VSyncMode vsync)
	{
		CurrentVSync = vsync;
		DisplayServer.WindowSetVsyncMode(vsync);
	}

	public void ApplyAllSettings()
	{
		SetWindowMode(CurrentWindowMode);
		if (CurrentWindowMode == DisplayServer.WindowMode.Windowed)
		{
			SetResolution(CurrentResolution);
		}
		SetMaxFps(CurrentMaxFps);
		SetVSync(CurrentVSync);
	}

	public void SaveSettings()
	{
		ConfigFile config = new();
		config.SetValue(SectionDisplay, "Width", CurrentResolution.X);
		config.SetValue(SectionDisplay, "Height", CurrentResolution.Y);
		config.SetValue(SectionDisplay, "WindowMode", (int)CurrentWindowMode);
		config.SetValue(SectionDisplay, "MaxFps", CurrentMaxFps);
		config.SetValue(SectionDisplay, "VSync", (int)CurrentVSync);
		config.Save(SettingsFilePath);
	}

	public void LoadSettings()
	{
		ConfigFile config = new();
		if (config.Load(SettingsFilePath) != Error.Ok) return;

		int w = (int)config.GetValue(SectionDisplay, "Width", 1920);
		int h = (int)config.GetValue(SectionDisplay, "Height", 1080);
		CurrentResolution = new Vector2I(w, h);

		int mode = (int)config.GetValue(SectionDisplay, "WindowMode", (int)DisplayServer.WindowMode.Windowed);
		CurrentWindowMode = (DisplayServer.WindowMode)mode;

		CurrentMaxFps = (int)config.GetValue(SectionDisplay, "MaxFps", 60);

		int vsync = (int)config.GetValue(SectionDisplay, "VSync", (int)DisplayServer.VSyncMode.Enabled);
		CurrentVSync = (DisplayServer.VSyncMode)vsync;
	}

	private void CenterWindow()
	{
		Vector2I screenSize = DisplayServer.ScreenGetSize();
		Vector2I windowPos = (screenSize - CurrentResolution) / 2;
		if (windowPos.X >= 0 && windowPos.Y >= 0)
		{
			DisplayServer.WindowSetPosition(windowPos);
		}
	}
}
