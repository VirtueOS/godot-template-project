## customized version of https://gist.github.com/TheDuriel/4507f6f81ebe4ed0bc082c0e3c220049
@tool
extends EditorScript

var _tree: SceneTree

func _run() -> void:
	_tree = Engine.get_main_loop() as SceneTree
	if not _tree:
		print("SceneTree is missing!")
		return
	
	if ProjectSettings.get_setting("virtueos/godot_setup_script", false):
		print("godot_setup_script: already ran, skipping")
		return
	ProjectSettings.set_setting("virtueos/godot_setup_script", true)
	ProjectSettings.save()
	
	# HACK: Keep this script alive so that await functions
	_tree.root.set_meta("godot_setup_script", self)
	
	print(_get_time_str(), ": godot_setup_script: started")
	print(_get_time_str(), ": godot_setup_script: starting create_file_structure")
	_create_file_structure()
	print(_get_time_str(), ": godot_setup_script: finished create_file_structure")
	print(_get_time_str(), ": godot_setup_script: starting configure_project_settings")
	_configure_project_settings()
	print(_get_time_str(), ": godot_setup_script: finished configure_project_settings")
	
	# HACK: Clean up after ourselves
	_tree.root.remove_meta("godot_setup_script")
	print(_get_time_str(), ": godot_setup_script: finished")

func _get_time_str() -> String:
	var time : Dictionary = Time.get_time_dict_from_system()
	return str(time.hour, ":", time.minute, ":", time.second)


func _create_file_structure() -> void:
	_make_folder("res://App/")
	_make_folder("res://Config/")
	_make_folder("res://Content/")
	_make_folder("res://Game/")
	_make_folder("res://Interface/")


func _configure_project_settings() -> void:
	ProjectSettings.set_setting("application/run/main_scene", "res://App/Boot/Boot.tscn")
	ProjectSettings.set_setting("run/main_scene", "res://boot.tscn")
	
	# exclude_addons -> no such setting
	ProjectSettings.set_setting("debug/gdscript/warnings/exclude_addons", false)
	ProjectSettings.set_setting("debug/gdscript/warnings/untyped_declaration", 1)
	ProjectSettings.set_setting("debug/gdscript/warnings/inferred_declaration", 1)
	
	ProjectSettings.set_setting("window/size/viewport_width", 1920)
	ProjectSettings.set_setting("window/size/viewport_height", 1080)
	ProjectSettings.set_setting("window/size/window_width_override", 1600)
	ProjectSettings.set_setting("window/size/window_height_override", 900)
	ProjectSettings.set_setting("window/stretch/mode", "canvas_items")
	ProjectSettings.set_setting("window/stretch/aspect", "expand")
	
	ProjectSettings.set_setting("editor/naming/node_name_num_separator", 2)
	ProjectSettings.set_setting("editor/naming/node_name_casing", 2)
	ProjectSettings.set_setting("editor/naming/scene_name_casing", 2)
	ProjectSettings.set_setting("editor/naming/script_name_casing", 2)
	ProjectSettings.set_setting("editor/naming/default_signal_callback_name", "_handle_{signal_name}")
	ProjectSettings.set_setting("editor/naming/default_signal_callback_to_self_name", "_handle_{signal_name}")
	
	ProjectSettings.set_setting("filesystem/import/blender/enabled", true)
	ProjectSettings.set_setting("gui/timers/tooltip_delay_sec", 0.1)
	ProjectSettings.save()


func _add_autoloads() -> void:
	# This order matters
	_add_autoload("Content", "res://App/Core/Content.gd")
	_add_autoload("App", "res://App/Core/App.gd")
	_add_autoload("Game", "res://App/Core/Game.gd")
	_add_autoload("Interface", "res://App/Core/Interface.gd")
	_add_autoload("Nylon", "res://Nylon/Nylon.gd")


func _add_autoload(autoload_name: String, path: String) -> void:
	if not FileAccess.file_exists(path):
		return
	var e: EditorPlugin = EditorPlugin.new()
	e.add_autoload_singleton(autoload_name, path)


func _make_folder(path: String) -> void:
	if DirAccess.dir_exists_absolute(ProjectSettings.globalize_path(path)):
		return
	else:
		DirAccess.make_dir_recursive_absolute(ProjectSettings.globalize_path(path))
		print("DurielsTemplate: Create Folder - %s" % path)
