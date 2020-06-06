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
    has_left = self.has_left
    has_right = self.has_right
    has_front = self.has_front
    front_direction = self.front_direction

    
    front_y_offset = 0
    if front_direction == "outside_2":
        front_y_offset = sides_thickness


    bottomMesh = [
        # bottomVertices
        Vector((-1 * scale_x/2, 1 * scale_y/2, 0)),
        Vector((1 * scale_x/2, 1 * scale_y/2, 0)),
        Vector((1 * scale_x/2, -1 * scale_y/2 + front_y_offset, 0)),
        Vector((-1 * scale_x/2, -1 * scale_y/2  + front_y_offset, 0)),

        # topVertices
        Vector((-1 * scale_x/2, 1 * scale_y/2, bottom_thickness)),  # 4
        Vector((1 * scale_x/2, 1 * scale_y/2, bottom_thickness)),
        Vector((1 * scale_x/2, -1 * scale_y/2  + front_y_offset, bottom_thickness)),
        Vector((-1 * scale_x/2, -1 * scale_y/2  + front_y_offset, bottom_thickness)),  # 7
    ]
    topMesh = [
        # bottomVertices
        Vector((-1 * scale_x/2, 1 * scale_y/2, scale_z)),
        Vector((1 * scale_x/2, 1 * scale_y/2, scale_z)),
        Vector((1 * scale_x/2, -1 * scale_y/2  + front_y_offset, scale_z)),
        Vector((-1 * scale_x/2, -1 * scale_y/2  + front_y_offset, scale_z)),
        # topVertices
        Vector((-1 * scale_x/2, 1 * scale_y/2, - top_thickness + scale_z)),  # 12
        Vector((1 * scale_x/2, 1 * scale_y/2, - top_thickness + scale_z)),
        Vector((1 * scale_x/2, -1 * scale_y/2  + front_y_offset , - top_thickness + scale_z)),
        Vector((-1 * scale_x/2, -1 * scale_y/2  + front_y_offset , - top_thickness + scale_z))  # 15
    ]
    leftMesh = [
        # outerVeticesBottom
        Vector((-1 * scale_x/2, 1 * scale_y/2,  bottom_thickness)),
        Vector((-1 * scale_x/2, -1 * scale_y/2, bottom_thickness)),
        # outerVeticesTop
        Vector((-1 * scale_x/2, -1 * scale_y/2, -top_thickness + scale_z)),
        Vector((-1 * scale_x/2, 1 * scale_y/2, - top_thickness + scale_z)),

        # innerverticesBottom
        Vector((-1 * scale_x/2 + sides_thickness, 1 * scale_y/2,  bottom_thickness)),
        Vector((-1 * scale_x/2 + sides_thickness, -1 * scale_y/2, bottom_thickness)),
        # innerverticesTop
        Vector((-1 * scale_x/2 + sides_thickness, -1 * scale_y/2, -top_thickness + scale_z)),
        Vector((-1 * scale_x/2 + sides_thickness, 1 * scale_y/2, - top_thickness + scale_z)),
    ]
    rightMesh = [
        Vector((1 * scale_x/2, 1 * scale_y/2, bottom_thickness)),
        Vector((1 * scale_x/2, -1 * scale_y/2, bottom_thickness)),
        Vector((1 * scale_x/2, -1 * scale_y/2, - top_thickness + scale_z)),
        Vector((1 * scale_x/2, 1 * scale_y/2, - top_thickness + scale_z)),

        Vector((1 * scale_x/2 - sides_thickness, 1 * scale_y/2, bottom_thickness)),
        Vector((1 * scale_x/2 - sides_thickness, - 1 * scale_y/2, bottom_thickness)),
        Vector((1 * scale_x/2 - sides_thickness, -1 * scale_y/2, - top_thickness + scale_z)),
        Vector((1 * scale_x/2 - sides_thickness, 1 * scale_y/2, - top_thickness + scale_z)),


    ]
    frontMeshInside = [
        Vector((1 * scale_x/2 - sides_thickness, - 1 * scale_y/2, bottom_thickness)),
        Vector((-1 * scale_x/2 + sides_thickness, - 1 * scale_y/2, bottom_thickness)),
        Vector((-1 * scale_x/2 + sides_thickness, -1 * scale_y/2, - top_thickness + scale_z)),
        Vector((1 * scale_x/2 - sides_thickness, -1 * scale_y/2, - top_thickness + scale_z)),

        # Inner
        Vector((1 * scale_x/2 - sides_thickness, -1 * scale_y/2 + sides_thickness, bottom_thickness)),
        Vector((-1 * scale_x/2 + sides_thickness, -1 * scale_y/2 + sides_thickness, bottom_thickness)),
        Vector((-1 * scale_x/2 + sides_thickness, -1 * scale_y / 2 + sides_thickness, - top_thickness + scale_z)),
        Vector((1 * scale_x/2 - sides_thickness, -1 * scale_y / 2 + sides_thickness, - top_thickness + scale_z)),
    ]
    
    frontMeshOutside_1 = [
        Vector((1 * scale_x/2, -1 * scale_y/2, 0)),
        Vector((-1 * scale_x/2, -1 * scale_y/2, 0)),
        Vector((-1 * scale_x/2, -1 * scale_y/2,  scale_z)),
        Vector((1 * scale_x/2, -1 * scale_y/2,  scale_z)),

        # outer
        Vector((1 * scale_x/2, -1 * scale_y/2 - sides_thickness, 0)),
        Vector((-1 * scale_x/2, -1 * scale_y/2 - sides_thickness, 0)),
        Vector((-1 * scale_x/2, -1 * scale_y/2 - sides_thickness,  + scale_z)),
        Vector((1 * scale_x/2, -1 * scale_y/2 - sides_thickness,  + scale_z)),
    ]

    frontMeshOutside_2 = [
        Vector((1 * scale_x/2, -1 * scale_y/2, 0)),
        Vector((-1 * scale_x/2, -1 * scale_y/2, 0)),
        Vector((-1 * scale_x/2, -1 * scale_y/2,  scale_z)),
        Vector((1 * scale_x/2, -1 * scale_y/2,  scale_z)),

        # inner
        Vector(( 1 * scale_x/2, -1 * scale_y/2 + sides_thickness, 0)),
        Vector((-1 * scale_x/2, -1 * scale_y/2 + sides_thickness, 0)),
        Vector((-1 * scale_x/2, -1 * scale_y/2 + sides_thickness,  + scale_z)),
        Vector(( 1 * scale_x/2, -1 * scale_y/2 + sides_thickness,  + scale_z)),
    ]

    print("front_direction:"+ front_direction)
    verts = bottomMesh
    if has_top:
        verts += topMesh
    if has_left:
        verts += leftMesh
    if has_right:
        verts += rightMesh
    if has_front:
        if front_direction == "inside":
            verts += frontMeshInside
        elif front_direction == "outside_1":
            verts += frontMeshOutside_1
        elif front_direction == "outside_2":
            verts += frontMeshOutside_2
            


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
        name="Top",
        default=True
    )

    has_left:  bpy.props.BoolProperty(
        name="Left",
        default=True
    )

    has_right:  bpy.props.BoolProperty(
        name="Right",
        default=True
    )
    has_front:  bpy.props.BoolProperty(
        name="Front",
        default=True
    )
    front_direction:  bpy.props.EnumProperty(
        name="Front direction",
        items=[
            # (unique identifier, property name, property description, icon identifier, number)
            ('inside', 'inside', 'Make the front panel within the object', 0),
            ('outside_1', 'outside simple', 'Make the front panel within the object', 1),
            ('outside_2', 'outside', 'Make the front panel on top of the object', 2)
        ],
        default='inside'
    )

    seperateParts:  bpy.props.BoolProperty(
        name="Separate Parts",
        default=True
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
