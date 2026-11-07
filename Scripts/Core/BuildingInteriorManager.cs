using Godot;
using System.Collections.Generic;

namespace Game.Core;

/// <summary>
/// Quản lý tập trung hệ thống chuyển đổi góc nhìn nội thất liền mạch trong làng (Seamless Interior Transition Manager).
/// </summary>
public partial class BuildingInteriorManager : Node
{
	public static BuildingInteriorManager? Instance { get; private set; }

	[Signal] public delegate void BuildingEnteredEventHandler(string buildingName);
	[Signal] public delegate void BuildingExitedEventHandler(string buildingName);

	public BuildingInteriorArea? ActiveArea { get; private set; }
	public bool IsInsideAnyBuilding => ActiveArea != null;

	private readonly List<BuildingInteriorArea> _registeredAreas = new();

	public override void _Ready()
	{
		Instance = this;
	}

	public override void _ExitTree()
	{
		if (Instance == this) Instance = null;
		_registeredAreas.Clear();
	}

	public void RegisterArea(BuildingInteriorArea area)
	{
		if (!_registeredAreas.Contains(area))
		{
			_registeredAreas.Add(area);
		}
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
	}

	public void NotifyBuildingExited(BuildingInteriorArea area)
	{
		if (ActiveArea == area)
		{
			ActiveArea = null;
			EmitSignal(SignalName.BuildingExited, area.BuildingName);
		}
	}
}
