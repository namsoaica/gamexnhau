extends SceneTree

var passed = 0
var failed = 0
var frame_count = 0
var test_map = null

func assert_true(cond: bool, msg: String):
	if cond:
		passed += 1
		print("[PASS] ", msg)
	else:
		failed += 1
		print("[FAIL] ", msg)

func _init():
	print("=== INITIALIZING VERIFICATION SUITE ===")

func _process(delta: float) -> bool:
	frame_count += 1
	if frame_count == 1:
		var map_res = load("res://Scenes/Levels/WorldMap.tscn")
		test_map = map_res.instantiate()
		root.add_child(test_map)
		return false
	
	if frame_count == 2:
		# At frame 2, all _Ready() methods have executed
		run_suite()
		test_map.queue_free()
		quit(0 if failed == 0 else 1)
		return true

	return false

func run_suite():
	print("\n=== RUNNING VERIFICATION SUITE ===")
	test_inputs()
	test_layers()
	test_world_map()
	test_player_scripts()
	test_player_facing_direction()
	test_procedural_tilt_direction()
	print("\n=== SUMMARY: Passed: ", passed, " | Failed: ", failed, " ===")

func test_inputs():
	print("\n-- Testing Input Actions --")
	var actions = ["move_left", "move_right", "move_forward", "move_backward", "jump", "interact"]
	for act in actions:
		assert_true(InputMap.has_action(act), "Action '" + act + "' exists in InputMap")
	
	var ev_left = InputMap.action_get_events("move_left")
	assert_true(ev_left.size() >= 2, "move_left has at least 2 events")

	var ev_jump = InputMap.action_get_events("jump")
	assert_true(ev_jump.size() >= 1, "jump has at least 1 event")

	var ev_interact = InputMap.action_get_events("interact")
	assert_true(ev_interact.size() >= 1, "interact has at least 1 event")

func test_layers():
	print("\n-- Testing 3D Physics Layers --")
	assert_true(ProjectSettings.get_setting("layer_names/3d_physics/layer_1") == "World", "Layer 1 is World")
	assert_true(ProjectSettings.get_setting("layer_names/3d_physics/layer_2") == "Player", "Layer 2 is Player")
	assert_true(ProjectSettings.get_setting("layer_names/3d_physics/layer_3") == "NPC", "Layer 3 is NPC")
	assert_true(ProjectSettings.get_setting("layer_names/3d_physics/layer_4") == "Interactable", "Layer 4 is Interactable")
	assert_true(ProjectSettings.get_setting("layer_names/3d_physics/layer_5") == "Hazard/KillZone", "Layer 5 is Hazard/KillZone")

func test_world_map():
	print("\n-- Testing WorldMap.tscn Structure --")
	var void_zone = test_map.find_child("VoidKillZone")
	assert_true(void_zone != null, "VoidKillZone node exists in WorldMap")
	assert_true(void_zone is Area3D, "VoidKillZone is Area3D")
	
	var player = test_map.find_child("Player")
	assert_true(player != null, "Player node exists in WorldMap")

	# Test void kill zone respawn logic
	print("\n-- Testing VoidKillZone Respawn Interaction --")
	var original_pos = player.global_position
	print("Initial player position: ", original_pos)
	
	player.global_position = Vector3(100, -20, 100) # fallen in void
	player.velocity = Vector3(0, -50, 0) # fast falling speed
	
	# Simulate entering void kill zone body_entered
	void_zone.emit_signal("body_entered", player)
	
	print("Post-respawn player position: ", player.global_position)
	print("Post-respawn player velocity: ", player.velocity)
	
	assert_true(player.global_position.distance_to(original_pos) < 0.2, "Player respawned near safe spawn position")
	assert_true(player.velocity == Vector3.ZERO, "Player velocity zeroed after respawn")

func test_player_scripts():
	print("\n-- Testing Player Scripts and Properties --")
	var player = test_map.find_child("Player")
	
	# PlayerMovement checks
	assert_true(player.get("IsSideScroller") == null, "IsSideScroller flag removed")
	assert_true(player.get("CoyoteTime") != null, "CoyoteTime property exists")
	assert_true(player.get("JumpBufferTime") != null, "JumpBufferTime property exists")
	assert_true(player.get("MoveSpeed") != null, "MoveSpeed property exists")
	
	# PlayerAnimation checks
	var anim_node = player.find_child("PlayerAnimation")
	assert_true(anim_node != null, "PlayerAnimation node exists")
	assert_true(anim_node.get("LeanAmount") != null, "LeanAmount property exists")
	assert_true(anim_node.get("BobFrequency") != null, "BobFrequency property exists")
	assert_true(anim_node.get("BobAmplitude") != null, "BobAmplitude property exists")

func test_player_facing_direction():
	print("\n-- Testing Player Movement Facing Direction (Anti-Moonwalk) --")
	var player = test_map.find_child("Player")
	var visual = player.get("VisualNode")
	if visual == null:
		visual = player
	
	# Test moving right (+X): Velocity = (6, 0, 0)
	player.velocity = Vector3(6, 0, 0)
	# Call 10 physics frames of rotation
	for i in range(10):
		player._physics_process(0.1)
	
	var facing_dir = -visual.transform.basis.z
	print("Moving (+X): facing = ", facing_dir)
	assert_true(facing_dir.x > 0.8, "Player faces right (+X) when moving right")

	# Test moving left (-X): Velocity = (-6, 0, 0)
	player.velocity = Vector3(-6, 0, 0)
	for i in range(10):
		player._physics_process(0.1)
	facing_dir = -visual.transform.basis.z
	print("Moving (-X): facing = ", facing_dir)
	assert_true(facing_dir.x < -0.8, "Player faces left (-X) when moving left")

	# Test moving forward (-Z): Velocity = (0, 0, -6)
	player.velocity = Vector3(0, 0, -6)
	for i in range(10):
		player._physics_process(0.1)
	facing_dir = -visual.transform.basis.z
	print("Moving (-Z): facing = ", facing_dir)
	assert_true(facing_dir.z < -0.8, "Player faces forward (-Z) when moving forward")

	# Test moving backward (+Z): Velocity = (0, 0, 6)
	player.velocity = Vector3(0, 0, 6)
	for i in range(10):
		player._physics_process(0.1)
	facing_dir = -visual.transform.basis.z
	print("Moving (+Z): facing = ", facing_dir)
	assert_true(facing_dir.z > 0.8, "Player faces backward (+Z) when moving backward")

func test_procedural_tilt_direction():
	print("\n-- Testing Procedural Lean Direction --")
	var player = test_map.find_child("Player")
	var anim_node = player.find_child("PlayerAnimation")
	var visual = player.get("VisualNode")
	if anim_node != null and visual != null:
		anim_node.set("ForceProcedural", true)
		player.velocity = Vector3(0, 0, -6) # moving forward
		# Run 5 process frames
		for i in range(5):
			anim_node._process(0.05)
		print("Procedural moving rotation X (pitch): ", visual.rotation.x)
		assert_true(visual.rotation.x < 0.0, "Player leans forward (negative pitch X) when moving")
