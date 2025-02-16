import bpy
import math
from math import radians
import os
import shutil
import glob

# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Import the 3D model
source_path = "/Users/shaunporwal/Documents/Documents - Shaun’s MacBook Air/GitHub/other/blender-llm-testing/media/nft_monkey.glb"
model_path = "/tmp/nft_monkey.glb"

print(f"Current working directory: {os.getcwd()}")
print(f"Source path: {source_path}")
print(f"Target path: {model_path}")

# Copy file to temporary location
try:
    shutil.copy2(source_path, model_path)
    print(f"Successfully copied file to: {model_path}")
except Exception as e:
    print(f"Error copying file: {str(e)}")
    raise

# Try to import the file
try:
    print("Attempting to import GLB file...")
    bpy.ops.import_scene.gltf(filepath=model_path)
    print("GLB import completed")
except Exception as e:
    print(f"Error importing file: {str(e)}")
    raise

# Get the imported object.
# Sometimes the GLB importer doesn't select the imported object, so we search for a mesh in the scene.
monkey = None
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        monkey = obj
        break
if monkey is None:
    raise RuntimeError("No mesh object imported. Please verify your GLB file!")

# Move it to the desired position
monkey.location = (3, 0, 0)

# Add subdivision surface modifier to smooth the monkey
subsurf = monkey.modifiers.new(name="Subdivision", type='SUBSURF')
subsurf.levels = 2  # Viewport subdivision levels
subsurf.render_levels = 2  # Render subdivision levels
subsurf.quality = 3  # Catmull-Clark subdivision

# Add empty object as center point
bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
center = bpy.context.active_object

# Parent monkey to the empty
monkey.parent = center
# Make the monkey face outward and stay upright
monkey.rotation_euler = (0, 0, radians(90))

# Animation settings
frame_start = 1
frame_end = 120  # 5 seconds at 24fps
bpy.context.scene.frame_start = frame_start
bpy.context.scene.frame_end = frame_end
# Set animation to loop
bpy.context.scene.render.fps = 25
bpy.context.scene.frame_current = frame_start
bpy.context.scene.use_preview_range = False
bpy.context.scene.frame_set(frame_start)

# Enable cyclic animation
action = bpy.data.actions.new(name="MonkeyRotation")
center.animation_data_create()
center.animation_data.action = action

# Create the rotation animation
for frame in range(frame_start, frame_end + 1):
    bpy.context.scene.frame_set(frame)
    
    # Calculate rotation angle
    angle = radians((frame - 1) * (360.0 / frame_end))
    
    # Set empty's rotation
    center.rotation_euler.z = angle
    
    # Insert keyframe for rotation
    center.keyframe_insert(data_path="rotation_euler", frame=frame)

# Set up cyclic animation
for fc in center.animation_data.action.fcurves:
    if fc.data_path == "rotation_euler":
        # Set the curve to cycle
        fc.modifiers.new('CYCLES')
        # Make the animation linear
        for kf in fc.keyframe_points:
            kf.interpolation = 'LINEAR'

# Add some basic lighting
bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))

# Add a camera
bpy.ops.object.camera_add(location=(15, 0, 7))
camera = bpy.context.active_object
camera.rotation_euler = (radians(75), 0, radians(90))

# Set the new camera as the active camera
bpy.context.scene.camera = camera

# Optional: Add a simple material to the monkey
material = bpy.data.materials.new(name="MonkeyMaterial")
material.use_nodes = True
monkey.data.materials.append(material)
