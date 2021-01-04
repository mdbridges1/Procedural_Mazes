## Unity Export Script v2.1
## (C)Michael Bridges 2020 www.canopy.games

## This Script will do the following:
# + SAVE the Current Blend file
# + Convert each object to a Mesh, this will apply ALL modifiers
# + Export all mesh objects placed in the collection defined in the varible "col_name" below.
# + Center objects in the scene each piece before export and return them it to its original location.
# + Export using settings to solve the scale and rotation issues that exist.
# + Exported files will be in a sub folder in the same direction the .blend file is located.
# + FBX with textures is disabled in this script, update with the following:
#    + path_mode='COPY', 
#    + embed_textures=True, 
# + Revert the file back to how it was prior to running the script.

import bpy
from math import *
from mathutils import *
import os

bpy.ops.wm.save_mainfile()

########EDIT HERE#########
col_name = 'Pieces.001'
########EDIT HERE#########

unity_dir = '.\FBX_Unity'                                       # Save Directory

blend_file_path = bpy.data.filepath
directory = os.path.dirname(blend_file_path)
 
if os.path.isdir(directory + unity_dir) == False:               # Makes directort if one doesn't exist already
    os.makedirs(directory + unity_dir) 

bpy.ops.object.mode_set(mode='OBJECT')                          # Switches into Object mode.
bpy.ops.object.select_all(action='DESELECT')                    # Makes sure nothing is selected

i = 0    
for i in range(len(bpy.data.collections[col_name].objects)):    # Iterate through each object of the named collection
    
    obj = bpy.data.collections[col_name].objects[i]
    
#    if obj.type != 'MESH':                                      # Exclude anything that isn't a Mesh object
#        
#        print(str(i) + obj.name  + " is not a MESH")
#        i += 1
#        continue
    
    if obj.parent != None:                                      # Exlcude any Mesh object that is a child
        
        print(str(i) + obj.name + " is a CHILD")
        i += 1
        continue
    else:                                                       # Export Parent and Children as a single FBX with Parents name
        bpy.ops.object.select_all(action='DESELECT') 
        
        obj.select_set(True)
    
        for child in range(len(obj.children)):
            bpy.data.objects[obj.children[child].name].select_set(True)
        
        obj.to_mesh
        target_file_fbx = os.path.join(directory + unity_dir, obj.name + '.fbx')

        bpy.data.objects[obj.name].location = (0,0,0) # move object to world origin
        
        bpy.ops.export_scene.fbx(
            filepath=target_file_fbx, 
            check_existing=False, 
            filter_glob="*.fbx", 
            use_selection=True, 
            use_active_collection=False, 
            global_scale=1, 
            apply_unit_scale=True, 
            apply_scale_options='FBX_SCALE_UNITS', 
            bake_space_transform=True, 
            object_types={'MESH', 'LIGHT'}, 
            use_mesh_modifiers=True, 
            use_mesh_modifiers_render=True, 
            mesh_smooth_type='FACE', 
            use_subsurf=False, 
            use_mesh_edges=False, 
            use_tspace=False, 
            use_custom_props=False, 
            add_leaf_bones=True, 
            primary_bone_axis='Y', 
            secondary_bone_axis='X', 
            use_armature_deform_only=False, 
            armature_nodetype='NULL', 
            bake_anim=True, 
            bake_anim_use_all_bones=True, 
            bake_anim_use_nla_strips=True, 
            bake_anim_use_all_actions=True, 
            bake_anim_force_startend_keying=True, 
            bake_anim_step=1, 
            bake_anim_simplify_factor=1, 
            path_mode='AUTO', 
            embed_textures=False, 
            batch_mode='OFF', 
            use_batch_own_dir=True, 
            use_metadata=True, 
            axis_forward='-Z', 
            axis_up='Y')

        bpy.ops.object.select_all(action='DESELECT')   
        print(str(i) + obj.name  + " is EXPORTED")
        i += 1
        
bpy.ops.wm.revert_mainfile()