import sys 
sys.path.append('c:/Python37-32/Lib/site-packages')
import bpy
from bpy.types import Panel

bl_info = {
    "name": "RyanB Rigging Tools",
    "author": "Ryan Blanchard",
    "version": (0, 0, 1),
    "blender": (2, 79, 0),
    "location": "View3D > Tools > RyanB Rigging Tools",
    "description": "Tools for rigging",
    "warning": "",
    "wiki_url": "https://wiki.blender.org/index.php/Extensions:2.6/Py/"
                "Scripts/3D_interaction/Oscurart_Tools",
    "category": "Rigging",
    }

#Class for the panel, derived by panel
class SimpleToolPanel(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = 'Tools Tab Label'
    bl_context = 'objectmode'
    bl_category = 'RyanB'
        
    #Add UI elements here
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.prop_search(scene, "armatureSlave_name", bpy.data, "armatures")
        layout.prop_search(scene, "armatureMaster_name", bpy.data, "armatures")       
        layout.operator("button.getbones",text="Get List of Bones")

def scene_armature_poll(self, object):
    return object.type == 'ARMATURE'

def RegisterArmatures():
    bpy.types.Scene.armatureSlave_name = bpy.props.StringProperty()
    bpy.types.Scene.armatureMaster_name = bpy.props.StringProperty()
    
def DeleteArmatures():
    del bpy.types.Scene.armatureSlave_name
    del bpy.types.Scene.armatureMaster_name
    
def GetBones(context):   
    bone_names = []
    if context.scene.armatureSlave_name is not None:
        #print(context.scene.armatureSlave_name)
        for bone in bpy.data.objects[context.scene.armatureSlave_name].data.bones:
            bone_names.append(bone.name)
    #for i in bone_names:
    #    print(i)
  
def GetBonesFromArmature(armatureName):   
    boneArray = []
    if armatureName is not None:
        for bone in bpy.data.armatures[armatureName].bones:
            boneArray.append(bone)
    return boneArray

def AddTransformationConstraints(armSlave, armMaster):
    if armSlave is not None and armMaster is not None:
        for boneSlave in bpy.data.armatures[armSlave].bones:
            for boneMaster in bpy.data.armatures[armMaster].bones:
                if boneSlave.name == boneMaster.name:
                    crc = boneSlave.constraints.new('TRANSFORM')
                    crc.target = boneMaster             
    return None

class buttonGetBones(bpy.types.Operator):
    bl_idname = "button.getbones" # translates to C-name BUTTON_OT_explode
    bl_label = "Button text"

    def execute(self, context):
        boneSlaveArray = GetBonesFromArmature(context.scene.armatureSlave_name)
        boneMasterArray = GetBonesFromArmature(context.scene.armatureMaster_name)
        return {'FINISHED'}

def register():
    bpy.utils.register_module(__name__)
    RegisterArmatures()

def unregister():
    bpy.utils.unregister_module(__name__)
    DeleteArmatures()
    
#Needed to run script in Text Editor
if __name__ == '__main__':
    register()
