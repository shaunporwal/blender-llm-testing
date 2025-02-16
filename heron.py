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
source_path = "/Users/shaunporwal/Documents/Documents - Shaun’s MacBook Air/GitHub/other/blender-llm-testing/media/heron.glb"
model_path = "/tmp/heron.glb"

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
heron = None
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        heron = obj
        break
if heron is None:
    raise RuntimeError("No mesh object imported. Please verify your GLB file!")

# Move it to the desired position
heron.location = (3, 0, 0)

# Add subdivision surface modifier to smooth the heron
subsurf = heron.modifiers.new(name="Subdivision", type='SUBSURF')
subsurf.levels = 2  # Viewport subdivision levels
subsurf.render_levels = 2  # Render subdivision levels
subsurf.quality = 3  # Catmull-Clark subdivision

# Unparent the heron so that it can rotate in place (remove empty influence)
heron.parent = None

# Material creation and coloration code removed per request

# Add some basic lighting
bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))

# Add a camera
bpy.ops.object.camera_add(location=(15, 0, 7))
camera = bpy.context.active_object
camera.rotation_euler = (radians(75), 0, radians(90))

# Set the new camera as the active camera
bpy.context.scene.camera = camera
