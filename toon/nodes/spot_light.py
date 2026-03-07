from __future__ import annotations

from typing import TYPE_CHECKING

from toon.utils import override

from .base import ToonNodeOSLLight

if TYPE_CHECKING:
    from bpy.types import Node, NodeTree


class ToonNodeLightSpot(ToonNodeOSLLight):
    bl_idname = "ToonNodeLightSpot"
    bl_label = "Spot Light"
    osl_name = "spot_light"

    @override
    def init_sockets(self, node_tree: NodeTree):
        node_tree.outputs.new("NodeSocketVector", "Light")
        node_tree.outputs.new("NodeSocketFloat", "Ray Length")
        node_tree.outputs.new("NodeSocketVector", "UV")

    @override
    def init_node_tree(self, node_tree: NodeTree, script: Node):
        location = self.new_location_node(node_tree)
        rotation = self.new_rotation_node(node_tree)
        energy = self.new_property_node(node_tree, "energy")
        size = self.new_property_node(node_tree, "size")
        node_tree.links.new(location.outputs[0], script.inputs[0])
        node_tree.links.new(rotation.outputs[0], script.inputs[1])
        node_tree.links.new(energy.outputs[0], script.inputs[2])
        node_tree.links.new(size.outputs[0], script.inputs[3])

        output = node_tree.nodes.new("NodeGroupOutput")
        node_tree.links.new(script.outputs[0], output.inputs[0])
        node_tree.links.new(script.outputs[1], output.inputs[1])
        node_tree.links.new(script.outputs[2], output.inputs[2])
