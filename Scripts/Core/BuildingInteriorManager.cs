using Godot;
using System.Collections.Generic;

namespace Game.Core;

/// <summary>
/// Quản lý tập trung hệ thống chuyển đổi góc nhìn nội thất liền mạch trong làng (Seamless Interior Transition Manager).
/// Hiển thị Banner/Toast thông báo chuyển vùng thị giác trực quan cho người chơi.
/// </summary>
public partial class BuildingInteriorManager : Node
{
	public static BuildingInteriorManager? Instance { get; private set; }

	[Signal] public delegate void BuildingEnteredEventHandler(string buildingName);
	[Signal] public delegate void BuildingExitedEventHandler(string buildingName);

	public BuildingInteriorArea? ActiveArea { get; private set; }
	public bool IsInsideAnyBuilding => ActiveArea != null;

	private readonly List<BuildingInteriorArea> _registeredAreas = new();
	private CanvasLayer? _toastCanvas;
	private PanelContainer? _toastPanel;
	private Label? _toastLabel;
	private StyleBoxFlat? _panelStyle;
	private Tween? _toastTween;

	public override void _Ready()
	{
		Instance = this;
		SetupToastUi();
		ScanSceneForAreas();
	}

	public override void _ExitTree()
	{
		_toastTween?.Kill();
		_registeredAreas.Clear();
		if (Instance == this) Instance = null;
	}

	public void RegisterArea(BuildingInteriorArea area)
	{
		if (!_registeredAreas.Contains(area)) _registeredAreas.Add(area);
	}

	public void UnregisterArea(BuildingInteriorArea area)
	{
		_registeredAreas.Remove(area);
		if (ActiveArea == area) ActiveArea = null;
	}

	public void NotifyBuildingEntered(BuildingInteriorArea area)
	{
		ActiveArea = area;
		EmitSignal(SignalName.BuildingEntered, area.BuildingName);
		ShowToast($"🏠 Đã bước vào {area.BuildingName} - Góc nhìn nội thất", new Color(1.0f, 0.85f, 0.45f));
	}

	public void NotifyBuildingExited(BuildingInteriorArea area)
	{
		if (ActiveArea != area) return;
		ActiveArea = null;
		EmitSignal(SignalName.BuildingExited, area.BuildingName);
		ShowToast($"🌿 Đã rời khỏi {area.BuildingName} - Góc nhìn toàn cảnh", new Color(0.45f, 0.95f, 0.6f));
	}

	public void ShowToast(string message, Color accentColor)
	{
		if (_toastPanel == null || _toastLabel == null || _panelStyle == null) return;
		_toastLabel.Text = message;
		_panelStyle.BorderColor = accentColor;
		AnimateToast();
	}

	private void AnimateToast()
	{
		_toastTween?.Kill();
		_toastTween = CreateTween();
		if (_toastTween == null || _toastPanel == null) return;

		_toastPanel.Modulate = new Color(1f, 1f, 1f, 0f);
		_toastTween.TweenProperty(_toastPanel, "modulate:a", 1.0f, 0.25f);
		_toastTween.TweenInterval(2.2f);
		_toastTween.TweenProperty(_toastPanel, "modulate:a", 0.0f, 0.45f);
	}

	private void SetupToastUi()
	{
		_toastCanvas = new CanvasLayer { Layer = 15 };
		AddChild(_toastCanvas);

		_panelStyle = new StyleBoxFlat
		{
			BgColor = new Color(0.08f, 0.09f, 0.14f, 0.88f),
			BorderWidthLeft = 2, BorderWidthRight = 2,
			BorderWidthTop = 2, BorderWidthBottom = 2,
			CornerRadiusBottomLeft = 8, CornerRadiusBottomRight = 8,
			CornerRadiusTopLeft = 8, CornerRadiusTopRight = 8,
			ContentMarginLeft = 18, ContentMarginRight = 18,
			ContentMarginTop = 8, ContentMarginBottom = 8
		};

		CreateToastNodes();
	}

	private void CreateToastNodes()
	{
		if (_toastCanvas == null) return;

		_toastPanel = new PanelContainer
		{
			Modulate = new Color(1f, 1f, 1f, 0f),
			MouseFilter = Control.MouseFilterEnum.Ignore
		};
		_toastPanel.AddThemeStyleboxOverride("panel", _panelStyle);

		_toastLabel = new Label
		{
			HorizontalAlignment = HorizontalAlignment.Center,
			VerticalAlignment = VerticalAlignment.Center
		};
		_toastLabel.AddThemeFontSizeOverride("font_size", 15);
		_toastPanel.AddChild(_toastLabel);

		SetupPanelLayout();
		_toastCanvas.AddChild(_toastPanel);
	}

	private void SetupPanelLayout()
	{
		if (_toastPanel == null) return;
		_toastPanel.AnchorTop = 0.0f;
		_toastPanel.AnchorBottom = 0.0f;
		_toastPanel.AnchorLeft = 0.5f;
		_toastPanel.AnchorRight = 0.5f;
		_toastPanel.GrowHorizontal = Control.GrowDirection.Both;
		_toastPanel.Position = new Vector2(-180.0f, 24.0f);
	}

	private void ScanSceneForAreas()
	{
		Node? root = GetTree().CurrentScene ?? GetParent();
		if (root != null) CollectAreasRecursive(root);
	}

	private void CollectAreasRecursive(Node parent)
	{
		if (parent is BuildingInteriorArea area) RegisterArea(area);
		foreach (Node child in parent.GetChildren())
		{
			CollectAreasRecursive(child);
		}
	}
}
