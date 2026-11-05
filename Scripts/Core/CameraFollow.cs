using Godot;

namespace Game.Core;

/// <summary>
/// Điều khiển Camera Isometric luôn bám theo và ngắm nhìn nhân vật chính (Player).
/// </summary>
public partial class CameraFollow : Camera3D
{
	[ExportGroup("Mục Tiêu & Khoảng Cách")]
	[Export] public Node3D? Target { get; set; }
	[Export] public Vector3 Offset { get; set; } = new Vector3(-28.0f, 23.0f, 28.0f);
	[Export] public float SmoothSpeed { get; set; } = 8.0f;
	[Export] public Vector3 LookAtOffset { get; set; } = new Vector3(0.0f, 1.0f, 0.0f);

	public override void _Ready()
	{
		Current = true;
		Target ??= (Node3D?)GetTree().GetFirstNodeInGroup("Player") ?? (Node3D?)GetParent()?.FindChild("Player");

		if (Target != null)
		{
			GlobalPosition = Target.GlobalPosition + Offset;
			LookAt(Target.GlobalPosition + LookAtOffset, Vector3.Up);
		}
	}

	public override void _PhysicsProcess(double delta)
	{
		if (Target == null)
		{
			return;
		}

		float dt = (float)delta;
		Vector3 targetPos = Target.GlobalPosition + Offset;
		GlobalPosition = GlobalPosition.Lerp(targetPos, SmoothSpeed * dt);
		LookAt(Target.GlobalPosition + LookAtOffset, Vector3.Up);
	}
}
