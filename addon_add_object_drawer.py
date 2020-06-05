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
    VERICES_PER_MESH = 8
    scale_x = self.scale.x
    scale_y = self.scale.y
    scale_z = self.scale.z
    bottom_thickness = self.bottom_thickness
    top_thickness = self.top_thickness
    sides_thickness = self.sides_thickness
    has_top = self.has_top

    bottomMesh = [
        # bottomVertices
        Vector((-1 * scale_x/2, 1 * scale_y/2, 0)),
        Vector((1 * scale_x/2, 1 * scale_y/2, 0)),
        Vector((1 * scale_x/2, -1 * scale_y/2, 0)),
        Vector((-1 * scale_x/2, -1 * scale_y/2, 0)),

        # topVertices
        Vector((-1 * scale_x/2, 1 * scale_y/2, bottom_thickness)),  # 4
        Vector((1 * scale_x/2, 1 * scale_y/2, bottom_thickness)),
        Vector((1 * scale_x/2, -1 * scale_y/2, bottom_thickness)),
        Vector((-1 * scale_x/2, -1 * scale_y/2, bottom_thickness)),  # 7
    ]
    topMesh = [
        # bottomVertices
        Vector((-1 * scale_x/2, 1 * scale_y/2, scale_z)),
        Vector((1 * scale_x/2, 1 * scale_y/2, scale_z)),
        Vector((1 * scale_x/2, -1 * scale_y/2, scale_z)),
        Vector((-1 * scale_x/2, -1 * scale_y/2, scale_z)),
        # topVertices
        Vector((-1 * scale_x/2, 1 * scale_y/2, - top_thickness + scale_z)),  # 12
        Vector((1 * scale_x/2, 1 * scale_y/2, - top_thickness + scale_z)),
        Vector((1 * scale_x/2, -1 * scale_y/2, - top_thickness + scale_z)),
        Vector((-1 * scale_x/2, -1 * scale_y/2, - top_thickness + scale_z))  # 15
    ]
    leftMesh = [
        # outerVeticesBottom
        Vector((-1 * scale_x/2, 1 * scale_y/2,  bottom_thickness)),
        Vector((-1 * scale_x/2, -1 * scale_y/2, bottom_thickness)),
        # outerVeticesTop
        Vector((-1 * scale_x/2, -1 * scale_y/2, -top_thickness + scale_z)),
        Vector((-1 * scale_x/2, 1 * scale_y/2, - top_thickness + scale_z)),

        #innerverticesBottom
        Vector((-1 * scale_x/2 + sides_thickness, 1 * scale_y/2,  bottom_thickness)),
        Vector((-1 * scale_x/2 + sides_thickness, -1 * scale_y/2, bottom_thickness)),
        #innerverticesTop
        Vector((-1 * scale_x/2 + sides_thickness, -1 * scale_y/2, -top_thickness + scale_z)),
        Vector((-1 * scale_x/2 + sides_thickness, 1 * scale_y/2, - top_thickness + scale_z)),
    ]

    verts = bottomMesh
    if has_top:
        verts += topMesh
        verts += leftMesh

    # for vert in verts:
    #     vert.z += 0

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

    indexRange = int(len(verts) / VERICES_PER_MESH * len(faces_template))
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

    if self.seperateParts:
        bpy.ops.mesh.separate(type='LOOSE')


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

    top_thickness: bpy.props.FloatProperty(
        name="Top thickness",
        unit='LENGTH',
        default=0.02
    )

    bottom_thickness: bpy.props.FloatProperty(
        name="Bottom thickness",
        unit='LENGTH',
        default=0.02
    )
    sides_thickness: bpy.props.FloatProperty(
        name="Sides thickness",
        unit='LENGTH',
        default=0.02
    )

    has_top:  bpy.props.BoolProperty(
        name="Top"
    )

    seperateParts:  bpy.props.BoolProperty(
        name="Separate Parts"
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
