from __future__ import annotations

from typing import TYPE_CHECKING

from bpy.types import Panel

from toon.ops import (
    NODE_OT_toon_node_compile_all,
    NODE_OT_toon_node_reload_all,
    NODE_OT_toon_node_setup_osl_render,
)
from toon.props import (
    ToonNodeLightSettings,
    ToonNodeMaterialSettings,
    ToonNodeObjectSettings,
)
from toon.utils import override

if TYPE_CHECKING:
    from bpy.types import Context


def _draw_pass_index_warning(self: Panel, context: Context):
    if context.scene.render.engine == "CYCLES" and context.scene.cycles.shading_system:
        layout = self.layout

        layout.box().label(
            text="Do not modify the pass index number directly.", icon="INFO"
        )


class OBJECT_PT_toon_node(Panel):
    bl_idname = "OBJECT_PT_toon"
    bl_label = "Toon"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"

    @override
    def draw(self, context: Context):
        layout = self.layout

        if context.object is None:
            return

        settings = ToonNodeObjectSettings.instance(context.object)

        col = layout.column()
        col.use_property_split = True
        col.prop(settings, "cast_shadows", text="Cast Shadows")
        col.prop(settings, "shadow_id", text="Shadow ID")
        col.prop(settings, "transparent_id", text="Transparent ID")
        col.prop(settings, "shadow_terminator_geometry_offset", text="Geometry Offset")

    @staticmethod
    def register():
        from bpy.types import OBJECT_PT_relations

        OBJECT_PT_relations.append(_draw_pass_index_warning)

    @staticmethod
    def unregister():
        from bpy.types import OBJECT_PT_relations

        OBJECT_PT_relations.remove(_draw_pass_index_warning)


class MATERIAL_PT_toon_node(Panel):
    bl_idname = "MATERIAL_PT_toon"
    bl_label = "Toon"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "material"

    @override
    def draw(self, context: Context):
        layout = self.layout

        if context.object is None or context.material is None:
            return

        object_settings = ToonNodeObjectSettings.instance(context.object)
        material_settings = ToonNodeMaterialSettings.instance(context.material)

        col = layout.column()
        col.use_property_split = True

        row = col.row()
        row.prop(material_settings, "cast_shadows", text="Cast Shadows")
        row.active = int(object_settings.cast_shadows) == 0

        row = col.row()
        row.prop(material_settings, "shadow_id", text="Shadow ID")
        row.active = object_settings.shadow_id == 0

        row = col.row()
        row.prop(material_settings, "transparent_id", text="Transparent ID")
        row.active = object_settings.transparent_id == 0

    @staticmethod
    def register():
        from bpy import types
        from bpy.types import EEVEE_MATERIAL_PT_viewport_settings

        EEVEE_MATERIAL_PT_viewport_settings.append(_draw_pass_index_warning)

        if hasattr(types, "CYCLES_MATERIAL_PT_settings"):
            types.CYCLES_MATERIAL_PT_settings.append(_draw_pass_index_warning)

    @staticmethod
    def unregister():
        from bpy import types
        from bpy.types import EEVEE_MATERIAL_PT_viewport_settings

        EEVEE_MATERIAL_PT_viewport_settings.remove(_draw_pass_index_warning)

        if hasattr(types, "CYCLES_MATERIAL_PT_settings"):
            types.CYCLES_MATERIAL_PT_settings.remove(_draw_pass_index_warning)


def _poll_toon_node_light(cls: type[Panel], context: Context) -> bool:
    if context.object is None:
        return False

    return getattr(context.object.data, "type", "") in {"POINT", "SPOT", "AREA"}


def _draw_toon_node_light(self: Panel, context: Context):
    layout = self.layout

    if context.object is None:
        return

    type = getattr(context.object.data, "type", "")
    settings = ToonNodeLightSettings.instance(context.object.data)

    col = layout.column()
    col.use_property_split = True

    if type == "POINT":
        col.prop(settings, "distance", text="Distance")
    elif type == "SPOT":
        col.prop(settings, "size", text="Size")
    elif type == "AREA":
        col.prop(settings, "distance", text="Distance")
        col.prop(settings, "width", text="Width")
        col.prop(settings, "height", text="Height")


class DATA_PT_toon_node_light_eevee(Panel):
    bl_idname = "DATA_PT_toon_node_light_eevee"
    bl_label = "Toon"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "data"
    bl_parent_id = "DATA_PT_EEVEE_light"

    @classmethod
    def poll(cls, context: Context) -> bool:
        return _poll_toon_node_light(cls, context)

    @override
    def draw(self, context: Context):
        _draw_toon_node_light(self, context)


class DATA_PT_toon_node_light_cycles(Panel):
    bl_idname = "DATA_PT_toon_node_light_cycles"
    bl_label = "Toon"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "data"
    bl_parent_id = "CYCLES_LIGHT_PT_light"

    @classmethod
    def poll(cls, context: Context) -> bool:
        return _poll_toon_node_light(cls, context)

    @override
    def draw(self, context: Context):
        _draw_toon_node_light(self, context)


class VIEW3D_PT_toon_node(Panel):
    bl_idname = "VIEW3D_PT_toon_node"
    bl_label = "Shader"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Toon"

    @override
    def draw(self, context: Context):
        layout = self.layout

        layout.operator(
            NODE_OT_toon_node_setup_osl_render.bl_idname,
            text="Setup OSL Render",
            icon="PREFERENCES",
        )
        layout.operator(
            NODE_OT_toon_node_reload_all.bl_idname,
            text="Reload All Nodes",
            icon="FILE_REFRESH",
        )
        layout.operator(
            NODE_OT_toon_node_compile_all.bl_idname,
            text="Compile All Shaders",
            icon="FILE_CACHE",
        )
