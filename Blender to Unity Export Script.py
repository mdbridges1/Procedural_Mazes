## Unity Export Script v2
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

#####################
col_name = 'Pieces'
#####################

unity_dir = '.\FBX_Unity'  

blend_file_path = bpy.data.filepath
directory = os.path.dirname(blend_file_path)
 
bpy.ops.object.select_all(action='DESELECT') 

if os.path.isdir(directory + unity_dir) == False:
    os.makedirs(directory + unity_dir) 

i = 0    
for i in range(len(bpy.data.collections[col_name].objects)):
    if bpy.data.collections[col_name].objects[i].type != 'MESH':
         i += 1
    else:    
        obj_name = bpy.data.collections[col_name].objects[i].name
        bpy.data.objects[obj_name].select_set(True)
        bpy.data.objects[obj_name].to_mesh
        target_file_fbx = os.path.join(directory + unity_dir, obj_name + '.fbx')

#        bpy.data.collections[col_name].objects[i].rotation_euler[0] = radians(-90)
#        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
#        bpy.data.collections[col_name].objects[i].rotation_euler[0] = radians(90)

#        obj_loc = bpy.data.objects[obj_name].location.copy() # copy location
        bpy.data.objects[obj_name].location = (0,0,0) # move object to world origin
        
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
            object_types={'EMPTY', 'CAMERA', 'LIGHT', 'ARMATURE', 'MESH', 'OTHER'}, 
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

#        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
#        
#        bpy.data.objects[obj_name].location = obj_loc # set object back to it's original location
        bpy.ops.object.select_all(action='DESELECT')   
        i =+ 1

bpy.ops.wm.revert_mainfile()