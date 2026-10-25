from __future__ import annotations

from typing import TYPE_CHECKING

from toon.props import ToonNodeSceneLight
from toon.utils import override

from .base import ToonNodeOSL

if TYPE_CHECKING:
    from bpy.types import Node, NodeTree


class ToonNodeLight(ToonNodeOSL):
    bl_idname = "ToonNodeLight"
    bl_label = "Light"
    osl_name = "light"

    def _new_attribute_node(self, node_tree: NodeTree, name: str) -> Node:
        node = node_tree.nodes.new("ShaderNodeAttribute")

        node.attribute_type = "VIEW_LAYER"
        node.attribute_name = f"{ToonNodeSceneLight.PROP_NAME}.{name}"

        return node

    @override
    def init_sockets(self, node_tree: NodeTree):
        node_tree.outputs.new("NodeSocketVector", "Light")
        node_tree.outputs.new("NodeSocketFloat", "Ray Length")
        node_tree.outputs.new("NodeSocketVector", "UV")

    @override
    def init_node_tree(self, node_tree: NodeTree, script: Node):
        light_type = self._new_attribute_node(node_tree, "light_type")
        location = self._new_attribute_node(node_tree, "location")
        rotation = self._new_attribute_node(node_tree, "rotation")
        energy = self._new_attribute_node(node_tree, "energy")
        distance = self._new_attribute_node(node_tree, "distance")
        size = self._new_attribute_node(node_tree, "size")
        width = self._new_attribute_node(node_tree, "width")
        height = self._new_attribute_node(node_tree, "height")
        node_tree.links.new(light_type.outputs[2], script.inputs[0])
        node_tree.links.new(location.outputs[1], script.inputs[1])
        node_tree.links.new(rotation.outputs[1], script.inputs[2])
        node_tree.links.new(energy.outputs[2], script.inputs[3])
        node_tree.links.new(distance.outputs[2], script.inputs[4])
        node_tree.links.new(size.outputs[2], script.inputs[5])
        node_tree.links.new(width.outputs[2], script.inputs[6])
        node_tree.links.new(height.outputs[2], script.inputs[7])

        output = node_tree.nodes.new("NodeGroupOutput")
        node_tree.links.new(script.outputs[0], output.inputs[0])
        node_tree.links.new(script.outputs[1], output.inputs[1])
        node_tree.links.new(script.outputs[2], output.inputs[2])
