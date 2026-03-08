from .node_menu import NODE_MT_toon_node_category
from .node_panel import (
    DATA_PT_toon_node_light_cycles,
    DATA_PT_toon_node_light_eevee,
    MATERIAL_PT_toon_node,
    OBJECT_PT_toon_node,
    VIEW3D_PT_toon_node,
)
from .palette_list import VIEW3D_UL_toon_palette_entry
from .palette_menu import (
    VIEW3D_MT_toon_palette,
    VIEW3D_MT_toon_palette_add,
    VIEW3D_MT_toon_palette_group,
    VIEW3D_MT_toon_palette_merge,
    VIEW3D_MT_toon_palette_merge_group,
    VIEW3D_MT_toon_palette_merge_group_overwrite,
    VIEW3D_MT_toon_palette_merge_overwrite,
)
from .palette_panel import VIEW3D_PT_toon_palette

classes = (
    NODE_MT_toon_node_category,
    VIEW3D_PT_toon_node,
    DATA_PT_toon_node_light_cycles,
    DATA_PT_toon_node_light_eevee,
    MATERIAL_PT_toon_node,
    OBJECT_PT_toon_node,
    VIEW3D_UL_toon_palette_entry,
    VIEW3D_MT_toon_palette,
    VIEW3D_MT_toon_palette_add,
    VIEW3D_MT_toon_palette_group,
    VIEW3D_MT_toon_palette_merge,
    VIEW3D_MT_toon_palette_merge_overwrite,
    VIEW3D_MT_toon_palette_merge_group,
    VIEW3D_MT_toon_palette_merge_group_overwrite,
    VIEW3D_PT_toon_palette,
)


def register():
    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class

    for cls in classes:
        unregister_class(cls)
