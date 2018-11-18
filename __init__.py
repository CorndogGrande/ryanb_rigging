import sys 
import mathutils
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
        layout.prop_search(scene, "armatureSlave_name", bpy.data, "objects")
        layout.prop_search(scene, "armatureMaster_name", bpy.data, "objects")       
        layout.operator("button.getbones",text="Get List of Bones")

def scene_armature_poll(self, object):
    return object.type == 'OBJECT'

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
        for bone in bpy.data.objects[armatureName].pose.bones:
            boneArray.append(bone)
    return boneArray

def GetBiggestDotProduct(boneSlave, boneMaster, axis):
    dotX = 0
    dotY = 0
    dotZ = 0
    if (boneSlave is not None and boneMaster is not None):
        boneSlaveAxis = getattr(boneSlave, axis)
        dotX = boneSlaveAxis.dot(boneMaster.x_axis)
        dotY = boneSlaveAxis.dot(boneMaster.y_axis)
        dotZ = boneSlaveAxis.dot(boneMaster.z_axis)
    listOfAbsDotProducts = [abs(dotX),abs(dotY),abs(dotZ)]
    listOfDotProducts = [dotX, dotY, dotZ]
    indexOfBiggest = listOfAbsDotProducts.index(max(listOfAbsDotProducts))   
    if (listOfDotProducts[indexOfBiggest] < 0):
        signOfDot = -1
    else:
        signOfDot = 1
    return indexOfBiggest, signOfDot
                    
def AddTransformationConstraints(armSlave, armMaster):
    axisList = ["X","Y","Z"]
    if armSlave is not None and armMaster is not None:
        for boneSlave in bpy.data.objects[armSlave].pose.bones:
            for boneMaster in bpy.data.objects[armMaster].pose.bones:
                if boneSlave.name == boneMaster.name:
                    crc = boneSlave.constraints.new(type='TRANSFORM')
                    crc.target = bpy.data.objects[armMaster]
                    crc.subtarget = boneMaster.name
                    biggestDotProductX, signOfX = GetBiggestDotProduct(boneSlave, boneMaster, "x_axis")                   
                    biggestDotProductY, signOfY = GetBiggestDotProduct(boneSlave, boneMaster, "y_axis")
                    biggestDotProductZ, signOfZ = GetBiggestDotProduct(boneSlave, boneMaster, "z_axis")
                    crc.map_to_x_from = axisList[biggestDotProductX]
                    crc.map_to_y_from = axisList[biggestDotProductY]
                    crc.map_to_z_from = axisList[biggestDotProductZ]
                    crc.map_from = "ROTATION"
                    crc.map_to = "ROTATION"
                    crc.owner_space = "LOCAL"
                    crc.target_space = "LOCAL"
                    crc.from_min_x_rot = -6.283185
                    crc.from_max_x_rot = 6.283185
                    crc.from_min_y_rot = -6.283185
                    crc.from_max_y_rot = 6.283185
                    crc.from_min_z_rot = -6.283185
                    crc.from_max_z_rot = 6.283185
                    crc.to_min_x_rot = -6.283185 * signOfX
                    crc.to_max_x_rot = 6.283185 * signOfX
                    crc.to_min_y_rot = -6.283185 * signOfY
                    crc.to_max_y_rot = 6.283185 * signOfY
                    crc.to_min_z_rot = -6.283185 * signOfZ
                    crc.to_max_z_rot = 6.283185 * signOfZ
                                 
    return None

class buttonGetBones(bpy.types.Operator):
    bl_idname = "button.getbones" # translates to C-name BUTTON_OT_explode
    bl_label = "Button text"

    def execute(self, context):
        boneSlaveArray = GetBonesFromArmature(context.scene.armatureSlave_name)
        boneMasterArray = GetBonesFromArmature(context.scene.armatureMaster_name)
        AddTransformationConstraints(context.scene.armatureSlave_name, context.scene.armatureMaster_name)
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
