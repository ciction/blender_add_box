from mathutils import Vector
from bpy_extras.object_utils import AddObjectHelper, object_data_add
from bpy.props import FloatVectorProperty
from bpy.types import Operator
import bpy
bl_info = {
    "name": "New Object",
    "author": "Your Name Here",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Mesh > New Object",
    "description": "Adds a new Mesh Object",
    "warning": "",
    "wiki_url": "",
    "category": "Add Mesh",
}


def add_object(self, context):
    scale_x = self.scale.x
    scale_y = self.scale.y
    scale_z = self.scale.z
    bottom_thickness = self.bottom_thickness
    top_thickness = self.top_thickness
    has_top = self.has_top


    verts = [
        # bottom
        Vector((-1 * scale_x/2, 1 * scale_y/2, 0)),
        Vector((1 * scale_x/2, 1 * scale_y/2, 0)),
        Vector((1 * scale_x/2, -1 * scale_y/2, 0)),
        Vector((-1 * scale_x/2, -1 * scale_y/2, 0)),

        # top
        Vector((-1 * scale_x/2, 1 * scale_y/2, bottom_thickness)),
        Vector((1 * scale_x/2, 1 * scale_y/2, bottom_thickness)),
        Vector((1 * scale_x/2, -1 * scale_y/2, bottom_thickness)),
        Vector((-1 * scale_x/2, -1 * scale_y/2, bottom_thickness)),



        # bottom
        Vector((-1 * scale_x/2, 1 * scale_y/2, bottom_thickness + scale_z)),
        Vector((1 * scale_x/2, 1 * scale_y/2, bottom_thickness + scale_z)),
        Vector((1 * scale_x/2, -1 * scale_y/2, bottom_thickness + scale_z)),
        Vector((-1 * scale_x/2, -1 * scale_y/2, bottom_thickness + scale_z)),

        # top
        Vector((-1 * scale_x/2, 1 * scale_y/2,
                bottom_thickness + top_thickness + scale_z)),
        Vector((1 * scale_x/2, 1 * scale_y/2,
                bottom_thickness + top_thickness + scale_z)),
        Vector((1 * scale_x/2, -1 * scale_y/2,
                bottom_thickness + top_thickness + scale_z)),
        Vector((-1 * scale_x/2, -1 * scale_y/2,
                bottom_thickness + top_thickness + scale_z)),
    ]

    for vert in verts:
        vert.z += 0

    edges = []

    faces = []
    faces_template = [
        # bottom
        [0, 1, 2, 3],
        # top
        [4, 5, 6, 7],
        # back
        [0, 1, 5, 4],
        # front
        [2, 3, 7, 6],
        # left
        [0, 4, 7, 3],
        # right
        [6, 5, 1, 2]
    ]

    indexRange = len(faces_template) + 6 if has_top else len(faces_template)
    for x in range(0, indexRange):
        repeatingIndex = faces_template[x % len(faces_template)]
        loopCounter = x // len(faces_template)
        offset = loopCounter * 8

        offset_vector = [offset, offset, offset, offset]
        newVector = [repeatingIndex[i]+offset_vector[i]
                     for i in range(len(repeatingIndex))]
        faces.append(newVector)

    mesh = bpy.data.meshes.new(name="New Object Mesh")
    mesh.from_pydata(verts, edges, faces)
    # useful for development when the mesh may be invalid.
    # mesh.validate(verbose=True)
    newObject = object_data_add(context, mesh, operator=self)

#    bpy.ops.object.modifier_add(type='SOLIDIFY')
#    bpy.context.object.modifiers["Solidify"].thickness = my_float


class OBJECT_OT_add_object(Operator, AddObjectHelper):
    """Create a new Mesh Object"""
    bl_idname = "mesh.add_object"
    bl_label = "Add Mesh Object"
    bl_options = {'REGISTER', 'UNDO'}

    scale: FloatVectorProperty(
        name="scale",
        default=(1.0, 1.0, 1.0),
        subtype='TRANSLATION',
        description="scaling",
    )

    bottom_thickness: bpy.props.FloatProperty(
        name="Bottom thickness",
        unit='LENGTH',
        default=0.02
    )

    top_thickness: bpy.props.FloatProperty(
        name="Top thickness",
        unit='LENGTH',
        default=0.02
    )

    has_top:  bpy.props.BoolProperty(
        name="Top"
    )

    def execute(self, context):

        add_object(self, context)

        return {'FINISHED'}


# Registration

def add_object_button(self, context):
    self.layout.operator(
        OBJECT_OT_add_object.bl_idname,
        text="Add Object",
        icon='PLUGIN')


# This allows you to right click on a button and link to documentation
def add_object_manual_map():
    url_manual_prefix = "https://docs.blender.org/manual/en/latest/"
    url_manual_mapping = (
        ("bpy.ops.mesh.add_object", "scene_layout/object/types.html"),
    )
    return url_manual_prefix, url_manual_mapping


def register():
    bpy.utils.register_class(OBJECT_OT_add_object)
    bpy.utils.register_manual_map(add_object_manual_map)
    bpy.types.VIEW3D_MT_mesh_add.append(add_object_button)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_object)
    bpy.utils.unregister_manual_map(add_object_manual_map)
    bpy.types.VIEW3D_MT_mesh_add.remove(add_object_button)


if __name__ == "__main__":
    register()
