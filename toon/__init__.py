bl_info = {
    "name": "Toon",
    "author": "gnya",
    "version": (0, 2, 3),
    "blender": (3, 6, 0),
    "description": "Pre-2.79 style render nodes with a shared color palette system.",
    "category": "Material",
}


from . import nodes, ops, props, shaders, ui, utils


def register():
    utils.register()
    props.register()
    ops.register()
    ui.register()
    shaders.register()
    nodes.register()


def unregister():
    utils.unregister()
    props.unregister()
    ops.unregister()
    ui.unregister()
    shaders.unregister()
    nodes.unregister()
