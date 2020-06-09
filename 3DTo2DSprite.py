import bpy, math, mathutils

_end_frame_offset = 1;
_pi = 3.14159265359
_start_angle = 0
_end_angle = _pi * 2
_zero = 0;
_45_degree_rot = _pi/4

scene = bpy.context.scene

print("start")

# ====================Render Settings====================
project_name = "2DRougelike"
armature_name = "Human" # Armature to render on
mesh_name = "Human" # Name of rendered file
# animations_to_render = ["Idle", "Jump", "Dodge", "Run", "Tpose", "Walk"]
animations_to_render = ["All"]
part_to_render = "" # Optional part to render, ex: head, body, legs (WIP, needs to be set manually in editor)
scene.render.resolution_x = 120
scene.render.resolution_y = 120
directions_to_render = 8 ## (WIP, set manually in script)
starting_tirection = 0 # (WIP, set manually in script)
new_anim_len = 12 # Number of frames for new animation, 0 will render all frames
perspective_angle = 45 # angle to view sprite from
# =====================================================

if "All" in animations_to_render[0]:
    for act in bpy.data.actions:
        animations_to_render.append(act.name)
    animations_to_render.pop(0)
        
for name in animations_to_render:
    print(name)

for animation_name in animations_to_render:
    thing_to_anim = bpy.data.objects[armature_name]
    current_anim = bpy.data.actions[animation_name]

    thing_to_anim.animation_data.action = current_anim

    _first_frame = scene.frame_start;
    _last_frame = current_anim.frame_range.y
    scene.render.filepath = "C:\Blender\Renders"

    if new_anim_len <= 0:
        frames_to_render = [0]
    else:
       # Calculate frames to render
        frame_var = _last_frame / new_anim_len

        add_to_render = frame_var

        frames_to_render = [round(add_to_render)]

        while add_to_render <= (_last_frame + frame_var):
            add_to_render += frame_var
            frames_to_render.extend([round(add_to_render)])  


      

    # set up filepath
    fp = scene.render.filepath + str("/" + project_name + "/" + mesh_name + "/")
    
    # If rendering in parts
    if part_to_render != "":
        fp = fp + str(part_to_render + "/"  + animation_name + "/")
    else:
        fp = fp + str(animation_name + "/")
        
    
    # render as png
    scene.render.image_settings.file_format = 'PNG' # set output format to .png

    #directions to render
    directions = ["Down", "DownLeft", "Left", "UpLeft", "Up", "UpRight", "Right", "DownRight"]
    # directions = ["DL"]

    # rotate_by = (end_angle / len(directions))

    rotate_to = _start_angle

    # Setup Camera Rig
    camera = bpy.data.objects["CameraRig"]
    # Set Z rotation to 0 to change other axis
    camera.rotation_euler[2] = 0
    
    # Set X rotation (Perspective)
    camera.rotation_euler[0] = -(perspective_angle * _pi/180)
    
    # Starting Z rotation
    camera.rotation_euler[2] = 0

    # for each direction in the list of directions
    for idx, dir in enumerate(directions):
        dir_fp =fp + str("/" + dir + "/") 
        current_frame = int(_first_frame)
        
        
        if idx != _zero:
            rotate_to += _45_degree_rot    
            
        camera.rotation_euler[2] = rotate_to
               
        for frame in range(_first_frame, int(_last_frame + round(frame_var))):
                    if _zero in frames_to_render or frame in frames_to_render:
                        bpy.context.scene.frame_current = frame
                        scene.render.filepath = dir_fp + str(current_frame)
                        current_frame += 1
                        bpy.ops.render.render(write_still=True) # render still



    # restore the filepath
    scene.render.filepath = "C:\Blender\Renders"

print("end")