from __future__ import annotations

from typing import TYPE_CHECKING

from bpy.types import Menu, Node

from toon.nodes import (
    ToonNodeHSVJitter,
    ToonNodeInput,
    ToonNodeLambert,
    ToonNodeMatCap,
    ToonNodeOutput,
    ToonNodePalette,
    ToonNodeTransform,
    ToonNodeUVPixelSnap,
    ToonNodeVisualize,
)
from toon.utils import override

if TYPE_CHECKING:
    from bpy.types import Context, UILayout


class NODE_MT_toon_node_category(Menu):
    bl_idname = "NODE_MT_category_toon"
    bl_label = "Toon"
    bl_space_type = "NODE_EDITOR"

    @classmethod
    @override
    def poll(cls, context: Context) -> bool:
        return (
            context.space_data.type == "NODE_EDITOR"
            and context.space_data.tree_type == "ShaderNodeTree"
            and context.material is not None
        )

    def _draw_node(self, layout: UILayout, type: type):
        bl_rna = Node.bl_rna_get_subclass(type.__name__)

        if bl_rna is not None:
            label = bl_rna.name
        else:
            label = "Unknown"

        o = layout.operator("node.add_node", text=label)
        o.type = type.__name__
        o.use_transform = True

    @override
    def draw(self, context: Context):
        layout = self.layout

        col = layout.column(align=True)
        self._draw_node(col, ToonNodePalette)
        col.separator()
        self._draw_node(col, ToonNodeMatCap)
        self._draw_node(col, ToonNodeHSVJitter)
        self._draw_node(col, ToonNodeUVPixelSnap)
        self._draw_node(col, ToonNodeTransform)
        col.separator()
        self._draw_node(col, ToonNodeInput)
        col.separator()
        self._draw_node(col, ToonNodeVisualize)
        self._draw_node(col, ToonNodeLambert)
        col.separator()
        self._draw_node(col, ToonNodeOutput)

    @classmethod
    def register(cls):
        from nodeitems_utils import _node_categories

        def _draw(self: Menu, context: Context):
            layout = self.layout

            if cls.poll(context):
                layout.menu(cls.bl_idname)

        _node_categories["SHADER_TOON"] = ([], _draw, [cls])

    @staticmethod
    def unregister():
        from nodeitems_utils import _node_categories

        del _node_categories["SHADER_TOON"]
