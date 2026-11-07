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
	test_dialogue_and_interaction()
	test_physics_floorsnap()
	test_paver_recolor()
	test_paver_stair_gap_and_thickness()
	test_surroundings_mountains()
	test_camera_zoom()
	test_free_camera_mode()
	test_dev_mode_overlay_and_gamepad()
	test_npc_ground_position()
	test_backface_collision()
	test_lighting_and_sky()
	test_staircase_ramp_collision()
	test_plains_recolor()
	test_expanded_platform_and_fence()
	test_clean_grass_texture()
	test_unobstructed_mountains()
	test_shared_materials_loading()
	test_character_shared_materials()
	test_map_shared_materials_applied()
	test_blender_exported_models_and_textures()
	test_player_combat_system()
	test_village_map_and_gameplay()
	print("\n=== SUMMARY: Passed: ", passed, " | Failed: ", failed, " ===")

func test_inputs():
	print("\n-- Testing Input Actions & Gamepad Bindings --")
	var actions = ["move_left", "move_right", "move_forward", "move_backward", "jump", "interact", "attack"]
	for act in actions:
		assert_true(InputMap.has_action(act), "Action '" + act + "' exists in InputMap")
	
	var ev_left = InputMap.action_get_events("move_left")
	assert_true(ev_left.size() >= 3, "move_left has keyboard, joypad motion & joypad button")
	var has_joy_motion_left = false
	var has_joy_btn_left = false
	for ev in ev_left:
		if ev is InputEventJoypadMotion and ev.axis == JOY_AXIS_LEFT_X and is_equal_approx(ev.axis_value, -1.0):
			has_joy_motion_left = true
		if ev is InputEventJoypadButton and ev.button_index == JOY_BUTTON_DPAD_LEFT:
			has_joy_btn_left = true
	assert_true(has_joy_motion_left, "move_left mapped to Joypad LeftStick Left")
	assert_true(has_joy_btn_left, "move_left mapped to Joypad DpadLeft")

	var ev_jump = InputMap.action_get_events("jump")
	var has_joy_jump = false
	for ev in ev_jump:
		if ev is InputEventJoypadButton and ev.button_index == JOY_BUTTON_A:
			has_joy_jump = true
	assert_true(has_joy_jump, "jump mapped to Joypad Button A")

	var ev_interact = InputMap.action_get_events("interact")
	var has_joy_x = false
	var has_joy_y = false
	for ev in ev_interact:
		if ev is InputEventJoypadButton:
			if ev.button_index == JOY_BUTTON_X: has_joy_x = true
			if ev.button_index == JOY_BUTTON_Y: has_joy_y = true
	assert_true(has_joy_x, "interact mapped to Joypad Button X")
	assert_true(has_joy_y, "interact mapped to Joypad Button Y")

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
	
	assert_true(player.global_position.distance_to(original_pos) < 0.5, "Player respawned near safe spawn position")
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
	
	# Model character_25d.glb mặt mặc định hướng +Z, nên hướng mặt thực tế là basis.z
	# Test moving right (+X): Velocity = (6, 0, 0)
	for i in range(10):
		player.velocity = Vector3(6, 0, 0)
		player._physics_process(0.1)
	
	var facing_dir = visual.transform.basis.z
	print("Moving (+X): facing = ", facing_dir)
	assert_true(facing_dir.x > 0.8, "Player faces right (+X) when moving right")

	# Test moving left (-X): Velocity = (-6, 0, 0)
	for i in range(10):
		player.velocity = Vector3(-6, 0, 0)
		player._physics_process(0.1)
	facing_dir = visual.transform.basis.z
	print("Moving (-X): facing = ", facing_dir)
	assert_true(facing_dir.x < -0.8, "Player faces left (-X) when moving left")

	# Test moving forward (-Z): Velocity = (0, 0, -6)
	for i in range(10):
		player.velocity = Vector3(0, 0, -6)
		player._physics_process(0.1)
	facing_dir = visual.transform.basis.z
	print("Moving (-Z): facing = ", facing_dir)
	assert_true(facing_dir.z < -0.8, "Player faces forward (-Z) when moving forward")

	# Test moving backward (+Z): Velocity = (0, 0, 6)
	for i in range(10):
		player.velocity = Vector3(0, 0, 6)
		player._physics_process(0.1)
	facing_dir = visual.transform.basis.z
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

func test_dialogue_and_interaction():
	print("\n-- Testing Dialogue & Interaction Bug Fixes --")
	var npc = test_map.find_child("NPC")
	assert_true(npc != null, "NPC exists in WorldMap")

	var interact_area = npc.find_child("InteractableArea")
	assert_true(interact_area != null, "InteractableArea exists under NPC")
	assert_true(interact_area.collision_layer == ((1 << 2) | (1 << 3)), "InteractableArea has Layer 3 & 4 (12)")

	var player = test_map.find_child("Player")
	var player_interactor = player.find_child("PlayerInteractor")
	assert_true(player_interactor != null, "PlayerInteractor exists under Player")
	assert_true(player_interactor.collision_mask == ((1 << 2) | (1 << 3)), "PlayerInteractor scans Layer 3 & 4 (12)")

	# Test Dialogue timeout refocus
	npc.OnFocusGained()
	var label = npc.FloatingLabel
	assert_true(label != null and label.visible, "FloatingLabel visible on focus gained")
	assert_true(label.text.contains("Ấn E để nói chuyện"), "Prompt displayed on focus gained")

	npc.Interact(player)
	assert_true(label.text.contains("Xin chào nhà thám hiểm"), "Dialogue text shown on interact")

	# Simulate timeout while focused
	npc.call("OnDialogueTimeout")
	assert_true(label.visible, "FloatingLabel still visible after timeout while focused")
	assert_true(label.text.contains("Ấn E để tiếp tục trò chuyện"), "Prompt updated to continue dialogue after timeout")

func test_physics_floorsnap():
	print("\n-- Testing Physics FloorSnap Bug Fixes --")
	var player = test_map.find_child("Player")
	
	# When jumping upwards (Velocity.Y > 0), FloorSnapLength must be 0
	player.velocity = Vector3(0, 9, 0)
	player._physics_process(0.016)
	assert_true(player.floor_snap_length == 0.0, "FloorSnapLength is 0.0 when jumping upwards")

	# When landing on floor with Velocity.Y <= 0, FloorSnapLength restores
	player.velocity = Vector3(0, 0, 0)
	# Force on floor by setting position and moving
	player._physics_process(0.016)
	if player.is_on_floor():
		assert_true(player.floor_snap_length > 0.0, "FloorSnapLength restored to DefaultFloorSnap on floor")
	else:
		assert_true(player.floor_snap_length == 0.0, "FloorSnapLength is 0.0 when in air")

func test_paver_recolor():
	print("\n-- Testing Paver Recolor To Grass --")
	var map_25d = test_map.find_child("Map_25D")
	assert_true(map_25d != null, "Map_25D exists in WorldMap")

	var paver_mesh = map_25d.find_child("SM_Tier2_Pavers")
	assert_true(paver_mesh != null, "SM_Tier2_Pavers exists in Map_25D")
	assert_true(paver_mesh.material_override != null, "Paver mesh has grass MaterialOverride applied")

func test_paver_stair_gap_and_thickness():
	print("\n-- Testing Paver Gap Elimination and 3D Extrusion --")
	var map_25d = test_map.find_child("Map_25D")
	var paver = map_25d.find_child("SM_Tier2_Pavers") as MeshInstance3D
	var stair = map_25d.find_child("SM_Staircase_02") as MeshInstance3D
	assert_true(paver != null and stair != null, "Paver and Staircase_02 exist in Map_25D")

	var paver_aabb = paver.get_aabb()
	var stair_aabb = stair.get_aabb()
	print("Paver AABB: ", paver_aabb)
	print("Stair AABB: ", stair_aabb)

	assert_true(paver_aabb.size.y >= 0.40, "Paver extruded thickness >= 0.40m (solid 3D block)")

	var paver_front_z = paver_aabb.position.z + paver_aabb.size.z
	var stair_end_z = stair_aabb.position.z
	print("Stair end Z: ", stair_end_z, " | Paver front Z: ", paver_front_z)
	assert_true(paver_front_z >= stair_end_z, "Paver overlaps Staircase_02 (0 gap, no clipping seam)")

func test_surroundings_mountains():
	print("\n-- Testing Surroundings Mountains & Plains --")
	var map_surr = test_map.find_child("Map_Surroundings")
	assert_true(map_surr != null, "Map_Surroundings exists in WorldMap")

	var north_mt = map_surr.find_child("Mountain_Mesh_North")
	assert_true(north_mt != null, "Mountain_Mesh_North exists as single majestic background mountain")

	var south_mt = map_surr.find_child("Mountain_Mesh_South")
	assert_true(south_mt == null, "Mountain_Mesh_South has been removed")

	var west_mt = map_surr.find_child("Mountain_Mesh_West")
	assert_true(west_mt == null, "Mountain_Mesh_West has been removed")

	var east_mt = map_surr.find_child("Mountain_Mesh_East")
	assert_true(east_mt == null, "Mountain_Mesh_East has been removed")

	var plains = map_surr.find_child("Terrain_Plains_Mesh")
	assert_true(plains != null, "Terrain_Plains_Mesh exists and connects island to surroundings")

func test_camera_zoom():
	print("\n-- Testing Isometric Camera Zoom Feature --")
	var cam = test_map.find_child("IsometricCamera")
	assert_true(cam != null, "IsometricCamera exists in WorldMap")
	assert_true(cam.get("MinZoomSize") != null, "MinZoomSize property exists")
	assert_true(cam.get("MaxZoomSize") != null, "MaxZoomSize property exists")
	assert_true(cam.get("ZoomSpeed") != null, "ZoomSpeed property exists")
	assert_true(cam.get("ZoomSmoothness") != null, "ZoomSmoothness property exists")

func test_npc_ground_position():
	print("\n-- Testing NPC Ground Placement --")
	var npc = test_map.find_child("NPC")
	assert_true(npc != null, "NPC exists in WorldMap")
	print("NPC Position: ", npc.position)
	assert_true(npc.position.y <= 1.0, "NPC placed on ground level (Y <= 1.0m)")
	assert_true(is_equal_approx(npc.position.x, 5.0), "NPC X coordinate is near player main pathway")

func test_backface_collision():
	print("\n-- Testing BackfaceCollision on Trimesh Surfaces --")
	var map_25d = test_map.find_child("Map_25D")
	var terrain = map_25d.find_child("SM_Terrain_Chunk") if map_25d else null
	assert_true(terrain != null, "SM_Terrain_Chunk exists in Map_25D")
	var found_concave_backface = false
	for child in terrain.get_children():
		if child is StaticBody3D:
			for sub_child in child.get_children():
				if sub_child is CollisionShape3D and sub_child.shape is ConcavePolygonShape3D:
					if sub_child.shape.backface_collision:
						found_concave_backface = true
	assert_true(found_concave_backface, "ConcavePolygonShape3D has BackfaceCollision enabled")

func test_lighting_and_sky():
	print("\n-- Testing Lighting, Shadows & Sky Environment --")
	var world_env = test_map.find_child("WorldEnvironment") as WorldEnvironment
	assert_true(world_env != null, "WorldEnvironment node exists in WorldMap")
	var env = world_env.environment
	assert_true(env != null, "Environment resource assigned")
	assert_true(env.background_mode == Environment.BG_SKY, "Background mode is Sky (2)")
	assert_true(env.ambient_light_source == Environment.AMBIENT_SOURCE_SKY, "Ambient light source is Sky (3)")
	assert_true(is_equal_approx(env.ambient_light_energy, 0.45), "Ambient light energy is 0.45")
	assert_true(env.tonemap_mode == Environment.TONE_MAPPER_ACES, "Tonemap mode is ACES (3)")
	assert_true(is_equal_approx(env.tonemap_exposure, 1.0), "Tonemap exposure is 1.0")
	assert_true(env.ssao_enabled == true, "SSAO is enabled")

	assert_true(env.sky != null, "Sky resource exists")
	var sky_mat = env.sky.sky_material as ProceduralSkyMaterial
	assert_true(sky_mat != null, "Sky material is ProceduralSkyMaterial")
	assert_true(sky_mat.sky_top_color.is_equal_approx(Color(0.35, 0.62, 0.95)), "Sky top color is soft sky blue")

	var light = test_map.find_child("DirectionalLight3D") as DirectionalLight3D
	assert_true(light != null, "DirectionalLight3D node exists in WorldMap")
	assert_true(is_equal_approx(light.light_energy, 1.15), "Light energy is 1.15")
	assert_true(light.shadow_enabled == true, "Shadows enabled")
	assert_true(is_equal_approx(light.shadow_bias, 0.04), "Shadow bias is 0.04")
	assert_true(is_equal_approx(light.shadow_blur, 1.6), "Shadow blur is 1.6")
	assert_true(light.directional_shadow_mode == DirectionalLight3D.SHADOW_PARALLEL_4_SPLITS, "Directional shadow mode is PSSM 4 splits (2)")
	assert_true(is_equal_approx(light.directional_shadow_max_distance, 70.0), "Directional shadow max distance is 70.0")

	var map_25d = test_map.find_child("Map_25D")
	var sky_plane = map_25d.find_child("SM_Sky_Backdrop_Plane") if map_25d != null else null
	assert_true(sky_plane == null, "SM_Sky_Backdrop_Plane removed (sky is clear and unobstructed)")

func test_staircase_ramp_collision():
	print("\n-- Testing Staircase Ramp Collision (Smooth Climbing) --")
	var map_25d = test_map.find_child("Map_25D")
	var stair1 = map_25d.find_child("SM_Staircase_01") as MeshInstance3D
	var stair2 = map_25d.find_child("SM_Staircase_02") as MeshInstance3D
	assert_true(stair1 != null and stair2 != null, "Both staircases exist in Map_25D")

	var has_convex_ramp_1 = false
	for child in stair1.get_children():
		if child is StaticBody3D:
			for col in child.get_children():
				if col is CollisionShape3D and col.shape is ConvexPolygonShape3D:
					has_convex_ramp_1 = true
	assert_true(has_convex_ramp_1, "SM_Staircase_01 has ConvexPolygonShape3D ramp collision")

	var has_convex_ramp_2 = false
	for child in stair2.get_children():
		if child is StaticBody3D:
			for col in child.get_children():
				if col is CollisionShape3D and col.shape is ConvexPolygonShape3D:
					has_convex_ramp_2 = true
	assert_true(has_convex_ramp_2, "SM_Staircase_02 has ConvexPolygonShape3D ramp collision")

	var player = test_map.find_child("Player") as CharacterBody3D
	assert_true(player != null, "Player exists")
	print("Player FloorMaxAngle (deg): ", rad_to_deg(player.floor_max_angle))
	assert_true(player.floor_max_angle >= deg_to_rad(57.5), "Player FloorMaxAngle >= 57.5 deg (supports 58 deg)")

func test_plains_recolor():
	print("\n-- Testing Terrain Plains Recolor To Grass --")
	var map_surr = test_map.find_child("Map_Surroundings")
	var plains = map_surr.find_child("Terrain_Plains_Mesh") as MeshInstance3D
	assert_true(plains != null, "Terrain_Plains_Mesh exists")
	assert_true(plains.material_override != null, "Terrain_Plains_Mesh has grass MaterialOverride applied (no white terrain)")

func test_free_camera_mode():
	print("\n-- Testing Free Camera Mode (6-DOF) --")
	var cam = test_map.find_child("IsometricCamera") as Camera3D
	assert_true(cam != null, "IsometricCamera exists")
	assert_true(cam.get("IsFreeCamActive") != null, "IsFreeCamActive property exists")
	assert_true(cam.get("FreeCamSpeed") != null, "FreeCamSpeed property exists")
	assert_true(cam.get("FreeCamLookSensitivity") != null, "FreeCamLookSensitivity property exists")
	assert_true(cam.get("IsFreeCamActive") == false, "IsFreeCamActive defaults to false")

	# Test switching to FreeCam
	cam.call("SetFreeCamActive", true)
	assert_true(cam.get("IsFreeCamActive") == true, "IsFreeCamActive is true after SetFreeCamActive(true)")
	assert_true(cam.projection == Camera3D.PROJECTION_PERSPECTIVE, "Camera switches to Perspective mode in FreeCam")
	assert_true(is_equal_approx(cam.fov, 75.0), "Camera FOV set to 75 deg in FreeCam")

	# Test switching back to Isometric
	cam.call("SetFreeCamActive", false)
	assert_true(cam.get("IsFreeCamActive") == false, "IsFreeCamActive is false after SetFreeCamActive(false)")
	assert_true(cam.projection == Camera3D.PROJECTION_ORTHOGONAL, "Camera restored to Orthogonal in Isometric mode")

	# Test ResetToPlayer
	cam.call("SetFreeCamActive", true)
	cam.call("ResetToPlayer")
	assert_true(cam.get("IsFreeCamActive") == false, "ResetToPlayer disables FreeCam mode")
	assert_true(cam.projection == Camera3D.PROJECTION_ORTHOGONAL, "ResetToPlayer restores Orthogonal projection")

	# Test Player Immobility during FreeCam mode
	var player = test_map.find_child("Player") as CharacterBody3D
	assert_true(player != null, "Player exists in WorldMap")

	cam.call("SetFreeCamActive", true)
	player.velocity = Vector3(6.0, 0.0, 6.0)
	player._physics_process(0.016)
	print("Player velocity during FreeCam: ", player.velocity)
	assert_true(is_equal_approx(player.velocity.x, 0.0) and is_equal_approx(player.velocity.z, 0.0),
		"Player stands still (horizontal velocity = 0) when FreeCam is active")

	# Test Player regains movement when FreeCam is deactivated
	cam.call("SetFreeCamActive", false)
	player.velocity = Vector3(6.0, 0.0, 0.0)
	player._physics_process(0.016)
	assert_true(abs(player.velocity.x) > 0.1,
		"Player regains normal movement when FreeCam is deactivated")

func test_dev_mode_overlay_and_gamepad():
	print("\n-- Testing Dev Mode Overlay & Gamepad Support --")
	var overlay = test_map.find_child("DevOverlay")
	assert_true(overlay != null, "DevOverlay node exists in WorldMap")

	var world_tab = overlay.find_child("DevWorldTab")
	assert_true(world_tab != null, "DevWorldTab exists in DevOverlay")

	var freecam_check = world_tab.find_child("FreeCamCheck")
	assert_true(freecam_check != null, "FreeCamCheck checkbox exists in DevWorldTab")

	var speed_slider = world_tab.find_child("SpeedSlider")
	assert_true(speed_slider != null, "FreeCam SpeedSlider exists in DevWorldTab")

	var reset_cam_btn = world_tab.find_child("ResetCameraBtn")
	assert_true(reset_cam_btn != null, "ResetCameraBtn exists in DevWorldTab")

	var status_label = world_tab.find_child("FreeCamStatusLabel")
	assert_true(status_label != null, "FreeCamStatusLabel exists in DevWorldTab")

	# Test Dev Mode Toggle
	var panel = overlay.find_child("DevPanel") as Control
	assert_true(panel != null, "DevPanel exists")
	assert_true(panel.visible == false, "DevPanel initially hidden")
	overlay.call("ToggleDevMode")
	assert_true(panel.visible == true, "DevPanel visible after ToggleDevMode()")
	overlay.call("ToggleDevMode")
	assert_true(panel.visible == false, "DevPanel hidden after second ToggleDevMode()")

func test_expanded_platform_and_fence():
	print("\n-- Testing Expanded Tier 2 Platform & Overlook Fence --")
	var map_25d = test_map.find_child("Map_25D")
	var paver = map_25d.find_child("SM_Tier2_Pavers") as MeshInstance3D
	assert_true(paver != null, "SM_Tier2_Pavers exists in Map_25D")
	var aabb = paver.get_aabb()
	print("Expanded Paver AABB: ", aabb)
	assert_true(aabb.size.x >= 2.5, "Tier 2 platform width >= 2.5m (expanded 2.6m)")
	assert_true(aabb.size.z >= 2.2, "Tier 2 platform length >= 2.2m (expanded 2.41m)")

	var fence = map_25d.find_child("SM_Fence_Wood_Overlook") as MeshInstance3D
	assert_true(fence != null, "SM_Fence_Wood_Overlook exists in Map_25D")
	var fence_aabb = fence.get_aabb()
	print("Expanded Fence AABB: ", fence_aabb)
	assert_true(fence_aabb.size.x >= 2.4, "Fence perimeter width >= 2.4m")
	assert_true(fence_aabb.size.z >= 2.2, "Fence perimeter length >= 2.2m")

func test_clean_grass_texture():
	print("\n-- Testing Clean Grass Texture (No Grid Lines) --")
	var auto_col = test_map.find_child("MapAutoCollision")
	assert_true(auto_col != null, "MapAutoCollision node exists")
	var tex_path = auto_col.get("GrassTexturePath") as String
	print("Current GrassTexturePath: ", tex_path)
	assert_true(tex_path.contains("tex_grass_clean.png"), "GrassTexturePath points to tex_grass_clean.png")
	assert_true(ResourceLoader.exists(tex_path), "tex_grass_clean.png resource exists and loaded in Godot")

func test_unobstructed_mountains():
	print("\n-- Testing Unobstructed Mountains (Removed Crowded Peaks) --")
	var map_25d = test_map.find_child("Map_25D")
	var mountains = map_25d.find_child("SM_Mountains_Background") as MeshInstance3D
	assert_true(mountains != null, "SM_Mountains_Background exists in Map_25D")
	var m_aabb = mountains.get_aabb()
	print("Mountains AABB: ", m_aabb)
	assert_true(m_aabb.position.z <= -7.5, "Mountains background pushed back, clear sky behind overlook deck")

func test_shared_materials_loading():
	print("\n-- Testing Shared Materials Loading (.tres) --")
	var mat_files = [
		"M_Grass.tres",
		"M_Grass_Dry.tres",
		"M_Dirt.tres",
		"M_Dirt_RedClay.tres",
		"M_Rock.tres",
		"M_Rock_Mountain_Purple.tres",
		"M_Wood.tres",
		"M_Wood_Fence.tres",
		"M_Metal.tres",
		"M_Metal_DarkIron.tres",
		"M_Palette_Stylized.tres",
		"M_Character_Body.tres",
		"M_Character_Face.tres"
	]
	var base_path = "res://Assets/Materials_Shared/"
	for file_name in mat_files:
		var path = base_path + file_name
		assert_true(ResourceLoader.exists(path), "File exists: " + file_name)
		var mat = ResourceLoader.load(path)
		assert_true(mat != null, "Successfully loaded: " + file_name)
		assert_true(mat is StandardMaterial3D, file_name + " is StandardMaterial3D")

func test_character_shared_materials():
	print("\n-- Testing Character Shared Materials Properties --")
	var body_mat = ResourceLoader.load("res://Assets/Materials_Shared/M_Character_Body.tres") as StandardMaterial3D
	assert_true(body_mat != null, "M_Character_Body.tres is valid")
	assert_true(body_mat.albedo_texture != null, "M_Character_Body has albedo_texture assigned")
	assert_true(is_equal_approx(body_mat.roughness, 0.6), "M_Character_Body roughness is 0.60")

	var face_mat = ResourceLoader.load("res://Assets/Materials_Shared/M_Character_Face.tres") as StandardMaterial3D
	assert_true(face_mat != null, "M_Character_Face.tres is valid")
	assert_true(face_mat.albedo_texture != null, "M_Character_Face has albedo_texture assigned")
	assert_true(is_equal_approx(face_mat.roughness, 0.6), "M_Character_Face roughness is 0.60")

func test_map_shared_materials_applied():
	print("\n-- Testing Map Shared Materials Applied on Meshes --")
	var map_25d = test_map.find_child("Map_25D")
	var map_surr = test_map.find_child("Map_Surroundings")
	assert_true(map_25d != null and map_surr != null, "Map nodes exist")

	# 1. Nền gạch & Plains -> M_Grass.tres
	var paver = map_25d.find_child("SM_Tier2_Pavers") as MeshInstance3D
	assert_true(paver != null and paver.material_override != null, "Paver has material override")
	assert_true(paver.material_override.resource_path.ends_with("M_Grass.tres"), "Paver uses M_Grass.tres")

	var plains = map_surr.find_child("Terrain_Plains_Mesh") as MeshInstance3D
	assert_true(plains != null and plains.material_override != null, "Plains has material override")
	assert_true(plains.material_override.resource_path.ends_with("M_Grass.tres"), "Plains uses M_Grass.tres")

	# 2. Đường đất -> M_Dirt.tres
	var dirt_path = map_25d.find_child("SM_Dirt_Path_Main") as MeshInstance3D
	assert_true(dirt_path != null and dirt_path.material_override != null, "SM_Dirt_Path_Main has material override")
	assert_true(dirt_path.material_override.resource_path.ends_with("M_Dirt.tres"), "SM_Dirt_Path_Main uses M_Dirt.tres")

	var dirt_tier1 = map_25d.find_child("SM_Dirt_Path_Tier1") as MeshInstance3D
	assert_true(dirt_tier1 != null and dirt_tier1.material_override != null, "SM_Dirt_Path_Tier1 has material override")
	assert_true(dirt_tier1.material_override.resource_path.ends_with("M_Dirt.tres"), "SM_Dirt_Path_Tier1 uses M_Dirt.tres")

	# 3. Hàng rào gỗ -> M_Wood_Fence.tres
	var fence = map_25d.find_child("SM_Fence_Wood_Overlook") as MeshInstance3D
	assert_true(fence != null and fence.material_override != null, "SM_Fence_Wood_Overlook has material override")
	assert_true(fence.material_override.resource_path.ends_with("M_Wood_Fence.tres"), "SM_Fence_Wood_Overlook uses M_Wood_Fence.tres")

	# 4. Núi tím viễn cảnh -> M_Rock_Mountain_Purple.tres
	var mountains = map_25d.find_child("SM_Mountains_Background") as MeshInstance3D
	assert_true(mountains != null and mountains.material_override != null, "SM_Mountains_Background has material override")
	assert_true(mountains.material_override.resource_path.ends_with("M_Rock_Mountain_Purple.tres"), "SM_Mountains_Background uses M_Rock_Mountain_Purple.tres")

	# 5. Tảng đá -> M_Rock.tres
	var boulder = map_25d.find_child("SM_Rock_Boulder_01") as MeshInstance3D
	assert_true(boulder != null and boulder.material_override != null, "SM_Rock_Boulder_01 has material override")
	assert_true(boulder.material_override.resource_path.ends_with("M_Rock.tres"), "SM_Rock_Boulder_01 uses M_Rock.tres")

	var rock_mesh = map_surr.find_child("Rock_Mesh_001") as MeshInstance3D
	assert_true(rock_mesh != null and rock_mesh.material_override != null, "Rock_Mesh_001 has material override")
	assert_true(rock_mesh.material_override.resource_path.ends_with("M_Rock.tres"), "Rock_Mesh_001 uses M_Rock.tres")

func test_blender_exported_models_and_textures():
	print("\n-- Testing Blender Exported Models & Seamless Textures Pipeline --")
	# Check GLB models exist and load
	var map_glb = ResourceLoader.load("res://Assets/Models_Exported/map_25d.glb")
	assert_true(map_glb != null, "map_25d.glb loaded successfully as PackedScene")

	var surr_glb = ResourceLoader.load("res://Assets/Models_Exported/map_surroundings.glb")
	assert_true(surr_glb != null, "map_surroundings.glb loaded successfully as PackedScene")

	# Check Blender source files
	assert_true(FileAccess.file_exists("res://Assets/Blender_Source/map_25d.blend"), "Original map_25d.blend preserved")
	assert_true(FileAccess.file_exists("res://Assets/Blender_Source/map_25d_fixed.blend"), "Safe map_25d_fixed.blend exists")
	assert_true(FileAccess.file_exists("res://Assets/Blender_Source/map_surroundings.blend"), "Safe map_surroundings.blend exists")

	# Check Tileable Textures
	var textures = [
		"res://Assets/Textures/Tileable/tex_grass_seamless.png",
		"res://Assets/Textures/Tileable/tex_dirt_seamless.png",
		"res://Assets/Textures/Tileable/tex_rock_seamless.png",
		"res://Assets/Textures/Tileable/tex_wood_seamless.png",
		"res://Assets/Textures/Tileable/tex_metal_seamless.png"
	]
	for tex_path in textures:
		var tex = ResourceLoader.load(tex_path)
		assert_true(tex != null and tex is Texture2D, "Texture exists and is Texture2D: " + tex_path)

func test_player_combat_system():
	print("\n-- Testing Player Combat System (PlayerCombat & IDamageable) --")
	var player = test_map.find_child("Player")
	assert_true(player != null, "Player node exists in scene")

	var combat = player.find_child("PlayerCombat")
	assert_true(combat != null, "PlayerCombat node exists under Player")
	assert_true(is_equal_approx(combat.get("AttackDamage"), 25.0), "Default AttackDamage is 25.0")
	assert_true(is_equal_approx(combat.get("AttackCooldown"), 0.45), "Default AttackCooldown is 0.45s")
	assert_true(is_equal_approx(combat.get("AttackDuration"), 0.35), "Default AttackDuration is 0.35s")
	assert_true(combat.get("AttackAnimName") == "Attack", "AttackAnimName is 'Attack'")

	var attack_area = player.find_child("AttackArea", true, false)
	assert_true(attack_area != null, "AttackArea exists under Player")
	assert_true(attack_area.monitoring == false, "AttackArea monitoring is disabled initially")

	var anim = player.find_child("PlayerAnimation", true, false)
	assert_true(anim != null, "PlayerAnimation exists")

	# Test executing attack
	assert_true(combat.CanAttack(), "CanAttack returns true initially")
	combat.ExecuteAttack()
	assert_true(combat.IsAttacking, "IsAttacking is true after ExecuteAttack")
	assert_true(attack_area.monitoring == true, "AttackArea monitoring enabled during attack")
	assert_true(anim.IsAttacking == true, "PlayerAnimation.IsAttacking is true during attack")

	# Test Damage to a DummyTarget
	var dummy_script = load("res://Scripts/Core/DummyTarget.cs")
	var dummy = dummy_script.new()
	test_map.add_child(dummy)
	dummy.global_position = player.global_position + Vector3(0, 0, 1.0)
	var initial_hp = dummy.CurrentHealth
	assert_true(dummy.IsAlive, "Dummy is initially alive with 100 HP")

	combat.CheckHitTarget(dummy)
	assert_true(dummy.CurrentHealth < initial_hp, "Dummy took damage from attack")
	assert_true(is_equal_approx(dummy.CurrentHealth, initial_hp - 25.0), "Dummy took exactly 25 damage")

	# Test Finishing attack
	combat.FinishAttack()
	assert_true(combat.IsAttacking == false, "IsAttacking is false after FinishAttack")
	assert_true(attack_area.monitoring == false, "AttackArea monitoring disabled after attack")
	assert_true(anim.IsAttacking == false, "PlayerAnimation.IsAttacking is false after FinishAttack")
	dummy.queue_free()

func test_village_map_and_gameplay():
	print("\n-- Testing Village Map & 4 Gameplay Subsystems --")
	var vlg_res = load("res://Scenes/Levels/VillageMap.tscn")
	assert_true(vlg_res != null, "VillageMap.tscn loaded successfully")
	if vlg_res == null:
		return
		
	var vlg = vlg_res.instantiate()
	test_map.add_child(vlg)

	# 1. Test Seamless Interior Zones
	var zones = ["InteriorZone_Smith", "InteriorZone_Alchemist", "InteriorZone_Chef", "InteriorZone_House"]
	for zn in zones:
		var z_node = vlg.find_child(zn, true, false)
		assert_true(z_node != null, "Interior zone '" + zn + "' exists")
		if z_node != null:
			var light = z_node.get("InteriorLight")
			assert_true(light != null, zn + " has InteriorLight configured")
			var zoom = z_node.get("InteriorCameraZoom")
			assert_true(zoom != null and zoom > 5.0, zn + " has InteriorCameraZoom > 5.0")

	# 2. Test 8 NPCs
	var npcs = [
		"Npc_Blacksmith", "Npc_Alchemist", "Npc_Chef", "Npc_Farmer",
		"Npc_Fisherman", "Npc_Miner", "Npc_Lumberjack", "Npc_Guard"
	]
	for npc_name in npcs:
		var npc_node = vlg.find_child(npc_name, true, false)
		assert_true(npc_node != null, "NPC '" + npc_name + "' exists in VillageMap")
		if npc_node != null:
			assert_true(npc_node.is_in_group("VillageNPC"), npc_name + " is in group VillageNPC")
			assert_true(npc_node.get("Profession") != null, npc_name + " has Profession assigned")
			assert_true(npc_node.CanInteract(), npc_name + " CanInteract returns true initially")

	# 3. Test Dev Overlay 6 Tabs
	var dev = vlg.find_child("DevOverlay", true, false)
	assert_true(dev != null, "DevOverlay exists in VillageMap")
	if dev != null:
		var tabs = dev.find_child("Tabs", true, false)
		assert_true(tabs != null, "Tabs container exists in DevOverlay")
		if tabs != null:
			assert_true(tabs.get_tab_count() >= 6, "DevOverlay has at least 6 tabs (found: " + str(tabs.get_tab_count()) + ")")
		var tp_tab = dev.find_child("DevTeleportTab", true, false)
		assert_true(tp_tab != null, "DevTeleportTab exists in DevOverlay")
		var npc_tab = dev.find_child("DevNpcSystemTab", true, false)
		assert_true(npc_tab != null, "DevNpcSystemTab exists in DevOverlay")
		var gfx_tab = dev.find_child("DevGraphicsTab", true, false)
		assert_true(gfx_tab != null, "DevGraphicsTab exists in DevOverlay")

	# 4. Test Display Settings Manager
	var disp_mgr = vlg.find_child("DisplaySettingsManager", true, false)
	assert_true(disp_mgr != null, "DisplaySettingsManager node exists in VillageMap")
	if disp_mgr != null:
		var max_fps = disp_mgr.get("CurrentMaxFps")
		assert_true(max_fps != null, "DisplaySettingsManager has CurrentMaxFps")

	# 5. Test NPC Interaction Dialog
	var dialog = vlg.find_child("NpcInteractionDialog", true, false)
	assert_true(dialog != null, "NpcInteractionDialog exists in VillageMap")

	# 6. Test CameraFollow Interior Focus
	var cam = vlg.find_child("IsometricCamera", true, false)
	assert_true(cam != null, "IsometricCamera exists in VillageMap")
	if cam != null:
		cam.SetInteriorFocus(Vector3(10, 2, 10), 12.0)
		assert_true(is_equal_approx(cam.TargetZoomSize, 12.0), "Camera TargetZoomSize changed to 12.0 on interior focus")
		cam.ResetInteriorFocus()

	vlg.queue_free()









