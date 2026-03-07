from __future__ import annotations

from typing import TYPE_CHECKING

from toon.utils import override

from .base import ToonNodeOSLLight

if TYPE_CHECKING:
    from bpy.types import Node, NodeTree


class ToonNodeLightSun(ToonNodeOSLLight):
    bl_idname = "ToonNodeLightSun"
    bl_label = "Sun Light"
    osl_name = "sun_light"

    @override
    def init_sockets(self, node_tree: NodeTree):
        node_tree.outputs.new("NodeSocketVector", "Light")
        node_tree.outputs.new("NodeSocketFloat", "Ray Length")
        node_tree.outputs.new("NodeSocketVector", "UV")

    @override
    def init_node_tree(self, node_tree: NodeTree, script: Node):
        rotation = self.new_rotation_node(node_tree)
        energy = self.new_property_node(node_tree, "data.energy")
        node_tree.links.new(rotation.outputs[0], script.inputs[0])
        node_tree.links.new(energy.outputs[0], script.inputs[1])

        output = node_tree.nodes.new("NodeGroupOutput")
        node_tree.links.new(script.outputs[0], output.inputs[0])
        node_tree.links.new(script.outputs[1], output.inputs[1])
        node_tree.links.new(script.outputs[2], output.inputs[2])
