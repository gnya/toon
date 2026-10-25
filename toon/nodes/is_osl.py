from __future__ import annotations

from typing import TYPE_CHECKING

from toon.utils import override

from .base import ToonNodeOSL

if TYPE_CHECKING:
    from bpy.types import Node, NodeTree


class ToonNodeIsOSL(ToonNodeOSL):
    bl_idname = "ToonNodeIsOSL"
    bl_label = "Is OSL"
    osl_name = "is_osl"

    @override
    def init_sockets(self, node_tree: NodeTree):
        node_tree.outputs.new("NodeSocketFloat", "Is OSL")

    @override
    def init_node_tree(self, node_tree: NodeTree, script: Node):
        output = node_tree.nodes.new("NodeGroupOutput")
        node_tree.links.new(script.outputs[0], output.inputs[0])
