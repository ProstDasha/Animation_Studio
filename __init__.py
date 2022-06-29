bl_info = {
    'name': 'Create Camera360',
    'author': 'Igor Yazev',
    'version': (0, 0, 1),
    'blender': (3, 1, 0),
    "location": "View3D > UI > Camera360",
    'description': 'This addon adds a camera to the selected object and creates a flyby around it'
}

import bpy
import math
from bpy.types import Operator, Panel, PropertyGroup
from bpy.utils import register_class, unregister_class
from bpy.props import FloatProperty, BoolProperty, PointerProperty

class CameraProps(PropertyGroup):

    camera_radius : FloatProperty(
        name = 'radius',
        default = 1,
        soft_min = .1,
        soft_max = 50,
        subtype = 'FACTOR'
    )
    
    
class Camera360(Operator):
 
    bl_idname = "object.camera"
    bl_label = "Camera360"
    bl_category = 'Camera360'
    camera_radius = None     
    def structure(self,context):
        props = context.object.rand
        self.camera_radius = props.camera_radius    
    
    def execute(self, context) -> set:
        self.structure(context)
        bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(self.camera_radius, 0, 5), rotation=(1.13446, 0, 1.5708), scale=(1, 1, 1))
        obj_camera = bpy.context.object
        
        bpy.ops.object.empty_add(type='PLAIN_AXES',radius = self.camera_radius, align='WORLD', location=(0, 0, 0), scale=(0.1, 0.1, 0.1))
        obj = bpy.context.object
        bpy.context.scene.frame_set(1)
        bpy.ops.anim.keyframe_insert_menu(type='Rotation')
        bpy.context.scene.frame_set(250)
        obj.rotation_euler = [0,0, math.radians(360)]
        bpy.ops.anim.keyframe_insert_menu(type='Rotation')
        bpy.context.scene.frame_set(1)
        
        obj_camera.select_set(state=True)
        bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)

        return {'FINISHED'}

class OBJECT_PT_CameraPanel(Panel):
    bl_label = "Camera360"
    bl_space_type = "VIEW_3D"    
    bl_region_type = "UI"
    bl_category = 'Camera360'
    
    def draw(self,context):
        layout = self.layout
        props = context.object.rand
        col = layout.column()
        col.prop(props, "camera_radius")
        
        row = layout.row()
        row.operator('object.camera')
        
        

classes = [
    CameraProps, 
    Camera360, 
    OBJECT_PT_CameraPanel
]

def register():
    for cl in classes:
        register_class(cl)
    bpy.types.Object.rand = PointerProperty(type = CameraProps)

def unregister():
    for cl in reversed(classes):
        unregister_class(cl)


if __name__ == "__main__":
    register()