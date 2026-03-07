from __future__ import annotations

from typing import TYPE_CHECKING

import bpy
from bpy.types import Context, UILayout

from toon.ops import NODE_OT_toon_node_reload_all, NODE_OT_toon_node_setup_osl_render
from toon.shaders import shader_filepath
from toon.utils import override

from .node import ToonNode

if TYPE_CHECKING:
    from bpy.types import Node, NodeTree


class ToonNodeOSL(ToonNode):
    osl_name = ""

    def _try_load_osl(self, node: Node | None) -> bool:
        if node is None:
            return False

        node.mode = "EXTERNAL"
        node.filepath = shader_filepath(self.osl_name)

        return len(node.inputs) > 0 or len(node.outputs) > 0

    def init_sockets(self, node_tree: NodeTree):
        pass

    def init_node_tree(self, node_tree: NodeTree, script: Node):
        pass

    @override
    def new_node_tree(self, name: str) -> tuple[NodeTree, bool]:
        node_tree = bpy.data.node_groups.new(name, "ShaderNodeTree")
        script = node_tree.nodes.new("ShaderNodeScript")

        self.init_sockets(node_tree)

        if not self._try_load_osl(script):
            return node_tree, False

        self.init_node_tree(node_tree, script)

        return node_tree, True

    @override
    def update(self):
        node_tree = self.node_tree

        if node_tree is None:
            return

        script = node_tree.nodes.get("Script")

        if not self._try_load_osl(script):
            self.node_ready = False

    @override
    def draw_buttons(self, context: Context, layout: UILayout):
        if not self.node_ready:
            if not (
                context.scene.render.engine == "CYCLES"
                and context.scene.cycles.shading_system
            ):
                layout.operator(
                    NODE_OT_toon_node_setup_osl_render.bl_idname,
                    text="Setup Render",
                    icon="PREFERENCES",
                )
            else:
                layout.operator(
                    NODE_OT_toon_node_reload_all.bl_idname,
                    text="Reload",
                    icon="FILE_REFRESH",
                )
