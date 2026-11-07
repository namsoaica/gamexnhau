using Godot;
using Game.Core;

namespace Game.UI;

/// <summary>
/// Trợ lý đồng bộ và ánh xạ các tùy chọn hiển thị giữa giao diện SettingsMenu và DisplaySettingsManager.
/// </summary>
public static class SettingsMenuBinder
{
	/// <summary>
	/// Nạp danh sách tùy chọn vào các OptionButton trên giao diện.
	/// </summary>
	public static void PopulateOptions(OptionButton? resOpt, OptionButton? winOpt, OptionButton? fpsOpt, OptionButton? vsyncOpt)
	{
		PopulateResolutions(resOpt);
		PopulateWindowModes(winOpt);
		PopulateFpsLimits(fpsOpt);
		PopulateVsyncModes(vsyncOpt);
	}

	/// <summary>
	/// Đồng bộ lựa chọn hiện tại trên giao diện theo cấu hình thực tế từ DisplaySettingsManager.
	/// </summary>
	public static void SyncFromSettings(OptionButton? resOpt, OptionButton? winOpt, OptionButton? fpsOpt, OptionButton? vsyncOpt, DisplaySettingsManager mgr)
	{
		SyncResolution(resOpt, mgr);
		SyncWindowMode(winOpt, mgr);
		SyncFps(fpsOpt, mgr);
		SyncVsync(vsyncOpt, mgr);
	}

	/// <summary>
	/// Đọc các giá trị đang chọn trên UI và áp dụng vào DisplaySettingsManager.
	/// </summary>
	public static void ApplyToSettings(OptionButton? resOpt, OptionButton? winOpt, OptionButton? fpsOpt, OptionButton? vsyncOpt, DisplaySettingsManager mgr)
	{
		ApplyResolution(resOpt, mgr);
		ApplyWindowMode(winOpt, mgr);
		ApplyFps(fpsOpt, mgr);
		ApplyVsync(vsyncOpt, mgr);
	}

	private static void PopulateResolutions(OptionButton? opt)
	{
		if (opt == null) return;
		opt.Clear();
		for (int i = 0; i < DisplaySettingsManager.AvailableResolutions.Length; i++)
		{
			Vector2I r = DisplaySettingsManager.AvailableResolutions[i];
			opt.AddItem($"{r.X} x {r.Y}", i);
		}
	}

	private static void PopulateWindowModes(OptionButton? opt)
	{
		if (opt == null) return;
		opt.Clear();
		opt.AddItem("Cửa sổ (Windowed)", 0);
		opt.AddItem("Không viền (Borderless)", 1);
		opt.AddItem("Toàn màn hình (Fullscreen)", 2);
	}

	private static void PopulateFpsLimits(OptionButton? opt)
	{
		if (opt == null) return;
		opt.Clear();
		for (int i = 0; i < DisplaySettingsManager.AvailableFpsLimits.Length; i++)
		{
			int f = DisplaySettingsManager.AvailableFpsLimits[i];
			opt.AddItem(f == 0 ? "Không giới hạn" : $"{f} FPS", i);
		}
	}

	private static void PopulateVsyncModes(OptionButton? opt)
	{
		if (opt == null) return;
		opt.Clear();
		opt.AddItem("Tắt VSync", 0);
		opt.AddItem("Bật VSync", 1);
	}

	private static void SyncResolution(OptionButton? opt, DisplaySettingsManager mgr)
	{
		for (int i = 0; i < DisplaySettingsManager.AvailableResolutions.Length; i++)
		{
			if (DisplaySettingsManager.AvailableResolutions[i] == mgr.CurrentResolution)
			{
				opt?.Select(i);
				break;
			}
		}
	}

	private static void SyncWindowMode(OptionButton? opt, DisplaySettingsManager mgr)
	{
		int idx = mgr.CurrentWindowMode == DisplayServer.WindowMode.ExclusiveFullscreen ? 2 : (mgr.CurrentWindowMode == DisplayServer.WindowMode.Fullscreen ? 1 : 0);
		opt?.Select(idx);
	}

	private static void SyncFps(OptionButton? opt, DisplaySettingsManager mgr)
	{
		for (int i = 0; i < DisplaySettingsManager.AvailableFpsLimits.Length; i++)
		{
			if (DisplaySettingsManager.AvailableFpsLimits[i] == mgr.CurrentMaxFps)
			{
				opt?.Select(i);
				break;
			}
		}
	}

	private static void SyncVsync(OptionButton? opt, DisplaySettingsManager mgr)
	{
		int idx = mgr.CurrentVSync == DisplayServer.VSyncMode.Disabled ? 0 : 1;
		opt?.Select(idx);
	}

	private static void ApplyResolution(OptionButton? opt, DisplaySettingsManager mgr)
	{
		int idx = opt?.Selected ?? 0;
		if (idx >= 0 && idx < DisplaySettingsManager.AvailableResolutions.Length)
		{
			mgr.SetResolution(DisplaySettingsManager.AvailableResolutions[idx]);
		}
	}

	private static void ApplyWindowMode(OptionButton? opt, DisplaySettingsManager mgr)
	{
		int idx = opt?.Selected ?? 0;
		var mode = idx switch
		{
			1 => DisplayServer.WindowMode.Fullscreen,
			2 => DisplayServer.WindowMode.ExclusiveFullscreen,
			_ => DisplayServer.WindowMode.Windowed
		};
		mgr.SetWindowMode(mode);
	}

	private static void ApplyFps(OptionButton? opt, DisplaySettingsManager mgr)
	{
		int idx = opt?.Selected ?? 1;
		if (idx >= 0 && idx < DisplaySettingsManager.AvailableFpsLimits.Length)
		{
			mgr.SetMaxFps(DisplaySettingsManager.AvailableFpsLimits[idx]);
		}
	}

	private static void ApplyVsync(OptionButton? opt, DisplaySettingsManager mgr)
	{
		int idx = opt?.Selected ?? 1;
		mgr.SetVSync(idx == 0 ? DisplayServer.VSyncMode.Disabled : DisplayServer.VSyncMode.Enabled);
	}
}
