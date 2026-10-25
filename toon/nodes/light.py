from __future__ import annotations

from typing import TYPE_CHECKING

from toon.utils import override

from .base import ToonNodeOSLLight

if TYPE_CHECKING:
    from bpy.types import Node, NodeTree


class ToonNodeLight(ToonNodeOSLLight):
    bl_idname = "ToonNodeLight"
    bl_label = "Light"
    osl_name = "light"

    @override
    def init_sockets(self, node_tree: NodeTree):
        i = node_tree.inputs.new("NodeSocketFloat", "Type")
        i.default_value = 0.0
        i.min_value = 0.0
        i.max_value = 3.0

        node_tree.outputs.new("NodeSocketVector", "Light")
        node_tree.outputs.new("NodeSocketFloat", "Ray Length")
        node_tree.outputs.new("NodeSocketVector", "UV")

    @override
    def init_node_tree(self, node_tree: NodeTree, script: Node):
        input = node_tree.nodes.new("NodeGroupInput")
        location = self.new_location_node(node_tree)
        rotation = self.new_rotation_node(node_tree)
        energy = self.new_property_node(node_tree, "energy")
        distance = self.new_property_node(node_tree, "distance")
        size = self.new_property_node(node_tree, "size")
        width = self.new_property_node(node_tree, "width")
        height = self.new_property_node(node_tree, "height")
        node_tree.links.new(input.outputs[0], script.inputs[0])
        node_tree.links.new(location.outputs[0], script.inputs[1])
        node_tree.links.new(rotation.outputs[0], script.inputs[2])
        node_tree.links.new(energy.outputs[0], script.inputs[3])
        node_tree.links.new(distance.outputs[0], script.inputs[4])
        node_tree.links.new(size.outputs[0], script.inputs[5])
        node_tree.links.new(width.outputs[0], script.inputs[6])
        node_tree.links.new(height.outputs[0], script.inputs[7])

        output = node_tree.nodes.new("NodeGroupOutput")
        node_tree.links.new(script.outputs[0], output.inputs[0])
        node_tree.links.new(script.outputs[1], output.inputs[1])
        node_tree.links.new(script.outputs[2], output.inputs[2])
