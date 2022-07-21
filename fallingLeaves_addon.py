# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name": "Leaf Creator and falling Simulation",
    "author": "Stefan Merdian",
    "version": (1, 0),
    "blender": (3, 1, 0),
    "location": "View3D > UI > Falling Leaves",
    "description": "Creates a customized leaves and can generate a Particlesystem, which imitates falling Leaves.",
    "warning": "",
    "doc_url": "",
    "category": "Add Mesh"
}

import bpy
import bmesh
import math
import mathutils
import random
import string

def map_range(v, from_min, from_max, to_min, to_max):
    """Map a value from an range to another"""
    return to_min + (v - from_min) * (to_max - to_min) / (from_max - from_min)

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class PROPERTY_PG_properties(bpy.types.PropertyGroup):
    NAME: bpy.props.StringProperty(
        name="Name", description="Assign name for Particlesystem", default="Particle_System")
    LEAVE_TEXTURE: bpy.props.StringProperty(
        name="Load Leave Texture", description="Load Texture from device", subtype="FILE_PATH")

class ADDON_PT_main_panel(bpy.types.Panel):
    bl_label = "Falling Leaves"
    bl_idname = "FALLING_LEAVES_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Falling Leaves Addon"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool
        col = layout.column()  
        col.label(text="Create some customized Leaves!")
        col.prop(mytool, "LEAVE_TEXTURE", text="Load Leave Texture")
        layout.operator('leavegenerator.add_leaves', text='Leavegenerator')   
        col = layout.column() 
        col.label(text="Generate and adjust the Particlesystem for falling Leaves")
        col.prop(mytool, "NAME")
        layout.operator(
            'particlesystem.add_particlesystemforfallingparticles', text='Generate System')


class FALLINGPARTICLES_OT_add_particlesystemforfallingparticles(bpy.types.Operator):
    bl_label = "Particlesystem"
    bl_idname = "particlesystem.add_particlesystemforfallingparticles"
    bl_description = "Add a particlesystem of falling particles"
    bl_options = {"REGISTER", "UNDO"}

    SCALE: bpy.props.FloatProperty(
        name="SCALE", default=1)
    POSTION_PARTICLESYS_X: bpy.props.FloatProperty(
        name="Position X", default=0)
    POSTION_PARTICLESYS_Y: bpy.props.FloatProperty(
        name="Position Y", default=0)
    POSTION_PARTICLESYS_Z: bpy.props.FloatProperty(
        name="Position Z", default=4)

    STRENGTH: bpy.props.FloatProperty(
        name="Wind Strength", default=3)
    FLOAT_FACTOR: bpy.props.FloatProperty(
        name="Float Factor", default=1, min=0, max=10)
    NOISE_AMOUNT: bpy.props.FloatProperty(
        name="Noise Amount", default=6, min=0, max=10)

    
    LIFETIME: bpy.props.FloatProperty(
        name="Lifetime", default=100, min=0)
    NUMBER_PARTICLES: bpy.props.IntProperty(
        name="Number of Particles", default=100, min=0)
    ROTATION: bpy.props.BoolProperty(
        name="Leave Rotation", default=True)
    DYNAMIC_ROTATION: bpy.props.BoolProperty(
        name="Dynamic Rotation", default=True)
    SHOW_VIEWPORT: bpy.props.BoolProperty(
        name="Show in Viewport", default=True)
    PARTICLE_SCALE: bpy.props.FloatProperty(
        name="Object Scale", default=0.5, min=0.1)
    SCALE_RANDOMNESS: bpy.props.FloatProperty(
        name="Object Scale Randomness", default=0, min=0, max=1)
    PARTCILE_MASS: bpy.props.FloatProperty(
        name="Mass", default=0.2, min=0)
    BROWNIAN: bpy.props.FloatProperty(
        name="Brownian", default=0.8, min=0, max=1)
    ANGULAR_VELOICTY: bpy.props.FloatProperty(
        name="Angular Veloicty", default=3.7, min=0, max=15)
    EMIT_FROM: bpy.props.EnumProperty(items=[('FACE', 'FACE', ''),
                                             ('VERT', 'VERT', ''), (('VOLUME', 'VOLUME', ''))])

    SCALE_X: bpy.props.FloatProperty(
        name="Scale X", default=20)
    SCALE_Y: bpy.props.FloatProperty(
        name="Scale Y", default=10)
    STICKNESS_LEVEL: bpy.props.FloatProperty(
        name="Stickness Level", default=10, min=0, max=15)
    DAMPING_FACTOR: bpy.props.FloatProperty(
        name="Damping Factor", default=0.95, min=0, max=1)

    def draw(self, context):
        
        layout = self.layout
        col = layout.column()
        col.label(text="Adjust your system")
        col.label(text="Transformation System")
        col.prop(self,"SCALE")
        col.prop(self, "POSTION_PARTICLESYS_X")
        col.prop(self, "POSTION_PARTICLESYS_Y")
        col.prop(self, "POSTION_PARTICLESYS_Z")

        col.label(text="Windsettings")
        col.prop(self, "STRENGTH")
        col.prop(self, "FLOAT_FACTOR")
        col.prop(self, "NOISE_AMOUNT")

       
        col.label(text="Groundsettings")
        col.prop(self, "SCALE_X")
        col.prop(self, "SCALE_Y")
        col.prop(self, "STICKNESS_LEVEL")
        col.prop(self, "DAMPING_FACTOR")

        col.label(text="Particlesettings")
        col.prop(self, "NUMBER_PARTICLES")
        col.prop(self, "LIFETIME")
        col.prop(self, "PARTICLE_SCALE")
        col.prop(self, "SCALE_RANDOMNESS")
        col.prop(self, "PARTCILE_MASS")
        col.prop(self, "EMIT_FROM", text="Emit from")
        col.prop(self, "BROWNIAN")
        col.prop(self, "ROTATION")
        col.prop(self, "DYNAMIC_ROTATION")
        col.prop(self, "ANGULAR_VELOICTY")
        col.prop(self, "SHOW_VIEWPORT")

    def add_particelSystem(self, _particlesys_name) -> bpy.types.Object:
        bpy.ops.mesh.primitive_cube_add()
        my_obj = bpy.context.active_object
        my_obj.name = _particlesys_name
        my_obj.scale =(self.SCALE, self.SCALE, self.SCALE)
        my_obj.location[0] = self.POSTION_PARTICLESYS_X
        my_obj.location[1] = self.POSTION_PARTICLESYS_Y
        my_obj.location[2] = self.POSTION_PARTICLESYS_Z
        if len(my_obj.particle_systems) == 0:
            my_obj.modifiers.new("leaveParticle", type='PARTICLE_SYSTEM')
            partical_sys = my_obj.particle_systems[0]
            settings = partical_sys.settings
            settings.emit_from = 'FACE'
            settings.render_type = 'COLLECTION'
            settings.instance_collection = bpy.data.collections["Leaves"]
            settings.normal_factor = 5
            settings.factor_random = 2
            settings.rotation_factor_random = 0.5
            settings.angular_velocity_mode = 'VELOCITY'
            settings.use_collection_pick_random = True
            settings.use_rotation_instance = True
            settings.use_scale_instance = True
            settings.lifetime = self.LIFETIME
            settings.emit_from = self.EMIT_FROM
            settings.count = self.NUMBER_PARTICLES
            settings.mass = self.PARTCILE_MASS
            settings.use_rotations = self.ROTATION
            settings.use_dynamic_rotation = self.DYNAMIC_ROTATION
            settings.brownian_factor = self.BROWNIAN
            settings.angular_velocity_factor = self.ANGULAR_VELOICTY
            settings.particle_size = self.PARTICLE_SCALE
            settings.size_random = self.SCALE_RANDOMNESS
            bpy.data.objects[_particlesys_name].show_instancer_for_viewport = self.SHOW_VIEWPORT
        return my_obj

    def add_ground(self) -> bpy.types.Object:
        bpy.ops.mesh.primitive_plane_add()
        my_obj = bpy.context.active_object
        my_obj.scale[0] = self.SCALE_X
        my_obj.scale[1] = self.SCALE_Y
        my_obj.modifiers.new("collisonGround", type='COLLISION')
        settings = my_obj.collision
        settings.friction_factor = 0.1
        settings.stickiness = self.STICKNESS_LEVEL
        settings.damping_factor = self.DAMPING_FACTOR
        return my_obj

    def add_wind(self, _particlesys_name) -> bpy.types.Object:
        particle_sys = bpy.context.scene.objects[_particlesys_name]
        bpy.ops.object.effector_add(type='WIND')
        my_obj = bpy.context.active_object
        my_obj.parent = particle_sys
        my_obj.location[0] = particle_sys.location[0] - 5
        my_obj.rotation_euler[1] = math.pi / 2
        my_obj.field.strength = self.STRENGTH
        my_obj.field.flow = self.FLOAT_FACTOR
        my_obj.field.noise = self.NOISE_AMOUNT
        return my_obj

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        particlesys_name: string
        my_tool = context.scene.my_tool
        temporary_string = my_tool.NAME
        for obj in bpy.context.scene.objects:
            if temporary_string == obj.name:
                context.scene.my_tool.NAME = ""
                self.report(
                    {'ERROR'}, f'{temporary_string} is already assigned')
                return {'CANCELLED'}
        if temporary_string == "":
            context.scene.my_tool.NAME = ""
            self.report({'ERROR'}, f'Name is empty')
            return {'CANCELLED'}
        else:
            particlesys_name = temporary_string
            context.scene.my_tool.STRING_NAME = ""
        self.add_particelSystem(particlesys_name)
        self.add_ground()
        self.add_wind(particlesys_name)
        return {"FINISHED"}


class LEAVEGENERATOR_OT_add_leaves(bpy.types.Operator):

    bl_label = "Leaves"
    bl_idname = "leavegenerator.add_leaves"
    bl_description = "Add a collection of random Leaves for use in particle systems"
    bl_options = {"REGISTER", "UNDO"}

    SPREAD: bpy.props.IntProperty(name="Leave Spread", default=1, min=1)
    LEAVE_NUMBER: bpy.props.IntProperty(
        name="Leave Numbers", default=1, min=1, max=100)
    LEAVE_RESOLUTION: bpy.props.IntProperty(
        name="Resolution", default=30, min=10, max=100)
    SMOOTHING: bpy.props.IntProperty(name="Smoothing", default=0, min=0, max=3)
    WIDTH_BASE: bpy.props.FloatProperty(
        name="Leave Width", default=0.2, min=0.15, max=0.5)
    WIDTH_TIP: bpy.props.FloatProperty(
        name="Tip Width", default=0.01, min=0.01, max=0.1)
    HEIGHT: bpy.props.FloatProperty(name="Height", default=2, min=1, max=5)
    ROTATION_FALLOFF: bpy.props.FloatProperty(
        name="Angle tip-over", default=1, min=0, max=10)
    ROTATION_X: bpy.props.IntProperty(
        name="Rotation X", default=10, min=-100, max=100)
    ROTATION_Y: bpy.props.IntProperty(
        name="Rotation Y", default=0, min=-100, max=100)

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.label(text="Customize your Leaves")
        col.prop(self, "SPREAD")
        col.prop(self, "LEAVE_NUMBER")
        col.prop(self, "LEAVE_RESOLUTION")
        col.prop(self, "SMOOTHING")
        col.prop(self, "WIDTH_BASE")
        col.prop(self, "WIDTH_TIP")
        col.prop(self, "HEIGHT")
        col.prop(self, "ROTATION_FALLOFF")
        col.prop(self, "ROTATION_X")
        col.prop(self, "ROTATION_Y")
        col.prop(self, "my_string")


    def create_material(self, _leaveTexture) -> bpy.types.Material:
        mat_name = "Leaf Material" + id_generator()
        hue_value = random.uniform(0.35, 0.55)
        hue_value = round(hue_value, 2)
        leaf_material: bpy.types.Material = bpy.data.materials.new(mat_name)
        leaf_material.use_nodes = True
        node_tree: bpy.types.NodeTree = leaf_material.node_tree
        nodes: typing.List[bpy.types.Node] = leaf_material.node_tree.nodes
        nd_txtImage = nodes.new("ShaderNodeTexImage")
        nd_txtCoord = nodes.new("ShaderNodeTexCoord")
        nd_hueSaturation = nodes.new("ShaderNodeHueSaturation")
        bpy.data.materials[mat_name].node_tree.nodes["Hue Saturation Value"].inputs[0].default_value = hue_value
        if _leaveTexture != "":
            nd_txtImage.image = bpy.data.images.load(_leaveTexture)
        node_tree.links.new(nd_hueSaturation.outputs[0], node_tree.nodes["Principled BSDF"].inputs[0])
        node_tree.links.new(nd_txtImage.outputs[0], nd_hueSaturation.inputs[4])
        node_tree.links.new(nd_txtCoord.outputs[0], nd_txtImage.inputs[0])
        return leaf_material

    def generate_leaves(self) -> bpy.types.Object:
        leaf_mesh = bpy.data.meshes.new("leaf_mesh")
        leaf_object = bpy.data.objects.new("leaf_object", leaf_mesh)

        bm = bmesh.new()
        bm.from_mesh(leaf_mesh)

        periode = 2 / self.LEAVE_RESOLUTION
        time = 0
        flag = True
        height = self.HEIGHT / self.LEAVE_RESOLUTION

        for i in range(self.LEAVE_RESOLUTION):
            time = periode * i
            shape = (2 * math.sin(1 * time + ((0 / 180) * math.pi)) +
                     2 * math.sin(2.1 * time + ((7.2 / 180) * math.pi))) * 1
            progress = i / (self.LEAVE_RESOLUTION - 1)
            width = map_range(shape, 0, 1, random.uniform(
                self.WIDTH_BASE, self.WIDTH_BASE + (self.SMOOTHING / 100)), self.WIDTH_TIP)
            if i == 0:
                print(i)
                last_vert1 = bm.verts.new((-0.02, 0, 0))
                last_vert2 = bm.verts.new((0.02, 0, 0))
                vert1 = bm.verts.new((0.02, 0, height * i))
                vert2 = bm.verts.new((-0.02, 0, height * i))
                face = bm.faces.new((last_vert1, last_vert2, vert2, vert1))
                progress = i / (self.LEAVE_RESOLUTION - 1)
            elif width < 0.0001:
                if flag:
                    width = -0.02
                flag = False
                vert1 = bm.verts.new((-width, 0, height * i))
                vert2 = bm.verts.new((width, 0, height * i))
                face = bm.faces.new((last_vert1, last_vert2, vert2, vert1))
            elif i > self.LEAVE_RESOLUTION / 2 and self.LEAVE_RESOLUTION >= 25:
                break
            elif i > self.LEAVE_RESOLUTION / 2 and self.LEAVE_RESOLUTION <= 25:
                vert1 = bm.verts.new((0, 0, (height * i) - 0.02))
                vert2 = bm.verts.new((0, 0, (height * i)-0.02))
                face = bm.faces.new((last_vert1, last_vert2, vert2, vert1))
                progress = i / (self.LEAVE_RESOLUTION)
                rot_angle_X = map_range(math.pow(
                    progress, self.ROTATION_FALLOFF), 0, 1, 0, math.radians(self.ROTATION_X))
                rot_matrix_X = mathutils.Matrix.Rotation(rot_angle_X, 4, "X")
                bmesh.ops.rotate(bm, cent=(0, 0, 0), matrix=rot_matrix_X, verts=[vert1, vert2])
                rot_angle_Y = map_range(math.pow(
                    progress, self.ROTATION_FALLOFF), 0, 1, 0,  math.radians(self.ROTATION_Y))
                rot_matrix_Y = mathutils.Matrix.Rotation(rot_angle_Y, 4, "Y")
                bmesh.ops.rotate(bm, cent=(0, 0, 0),
                                 matrix=rot_matrix_Y, verts=[vert1, vert2])
                break
            last_vert1 = vert1
            last_vert2 = vert2
            rot_angle_X = map_range(math.pow(
                progress, self.ROTATION_FALLOFF), 0, 1, 0, math.radians(self.ROTATION_X))
            rot_matrix_X = mathutils.Matrix.Rotation(rot_angle_X, 4, "X")
            bmesh.ops.rotate(bm, cent=(0, 0, 0),
                             matrix=rot_matrix_X, verts=[vert1, vert2])
            rot_angle_Y = map_range(math.pow(
                progress, self.ROTATION_FALLOFF), 0, 1, 0,  math.radians(self.ROTATION_Y))
            rot_matrix_Y = mathutils.Matrix.Rotation(rot_angle_Y, 4, "Y")
            bmesh.ops.rotate(bm, cent=(0, 0, 0),
                             matrix=rot_matrix_Y, verts=[vert1, vert2])
        bm.to_mesh(leaf_mesh)
        bm.free()
        return leaf_object

    @classmethod
    def poll(cls, context):
        return context.mode == "OBJECT"

    def execute(self, context):
        leaveTexture: string
        leave_collection: bpy.types.Collection
        my_tool = context.scene.my_tool
        temporary_filepath = my_tool.LEAVE_TEXTURE

        if temporary_filepath.lower().endswith(('.png', '.jpg', '.jpeg')):
            leaveTexture = temporary_filepath
        elif temporary_filepath == "":
            leaveTexture = ""
            self.report(
                    {'WARNING'}, 'No Texture was loaded. No texture will assigned!')
        else:
            self.report(
                   {'ERROR_INVALID_INPUT'}, f'{temporary_filepath} is not readable!')
            return {'CANCELLED'}
  
        if "Leaves" in bpy.data.collections:
            leave_collection = bpy.data.collections["Leaves"]
        else:
            leave_collection = bpy.data.collections.new("Leaves")
        try:
            bpy.context.scene.collection.children.link(leave_collection)
        except:
            ...  # collction already linked
        for i in range(self.LEAVE_NUMBER):
            leave: bpy.types.Object = self.generate_leaves()
            leave.data.materials.append(self.create_material(leaveTexture))
            leave_collection.objects.link(leave)
            bpy.context.view_layer.objects.active = leave
            if self.SPREAD > 1:
                for obj in bpy.data.collections['Leaves'].all_objects:
                    if bpy.context.active_object == obj:
                        leave_offset: mathutils.Vector = mathutils.Vector(
                            (random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-1, 1)))
                        leave_offset = leave_offset.normalized() * random.uniform(0, self.SPREAD)
                        leave.location = 1 * leave_offset
        return {"FINISHED"}

def menu_func(self, context):
    self.layout.operator(
        LEAVEGENERATOR_OT_add_leaves.bl_idname, icon='OUTLINER_OB_HAIR')
    self.layout.operator(
        FALLINGPARTICLES_OT_add_particlesystemforfallingparticles.bl_idname, icon='OUTLINER_OB_HAIR')

classes = [PROPERTY_PG_properties, ADDON_PT_main_panel, LEAVEGENERATOR_OT_add_leaves,
           FALLINGPARTICLES_OT_add_particlesystemforfallingparticles]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        bpy.types.Scene.my_tool = bpy.props.PointerProperty(
            type=PROPERTY_PG_properties)
        bpy.types.VIEW3D_MT_mesh_add.append(menu_func)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)
        del bpy.types.Scene.my_tool
