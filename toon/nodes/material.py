from __future__ import annotations

from typing import TYPE_CHECKING

from toon.props import ToonNodeObjectSettings
from toon.utils import override

from .base import ToonNodeOSL

if TYPE_CHECKING:
    from bpy.types import Node, NodeTree


class ToonNodeMaterial(ToonNodeOSL):
    bl_idname = "ToonNodeMaterial"
    bl_label = "Material"
    osl_name = "material"

    @override
    def init_sockets(self, node_tree: NodeTree):
        i = node_tree.inputs.new("NodeSocketVector", "Light")
        i.default_value = (0.0, 0.0, 0.0)
        i.min_value = float("-inf")
        i.max_value = float("inf")
        i.hide_value = True

        i = node_tree.inputs.new("NodeSocketFloat", "Ray Length")
        i.default_value = 0.0
        i.min_value = float("-inf")
        i.max_value = float("inf")
        i.hide_value = True

        i = node_tree.inputs.new("NodeSocketVector", "Normal")
        i.default_value = (0.0, 0.0, 0.0)
        i.min_value = -1.0
        i.max_value = 1.0
        i.hide_value = True

        i = node_tree.inputs.new("NodeSocketFloatFactor", "Reflectance")
        i.default_value = 0.5
        i.min_value = 0.0
        i.max_value = 1.0

        i = node_tree.inputs.new("NodeSocketFloat", "Exponent")
        i.default_value = 10.0
        i.min_value = 0.0
        i.max_value = float("inf")

        i = node_tree.inputs.new("NodeSocketColor", "Color")
        i.default_value = (0.0, 0.0, 0.0, 0.0)

        i = node_tree.inputs.new("NodeSocketFloat", "Diffuse Threshold")
        i.default_value = 0.1
        i.min_value = 0.0
        i.max_value = 1.0

        i = node_tree.inputs.new("NodeSocketFloat", "Specular Threshold")
        i.default_value = 0.1
        i.min_value = 0.0
        i.max_value = 1.0

        node_tree.outputs.new("NodeSocketColor", "Diffuse")
        node_tree.outputs.new("NodeSocketColor", "Specular")

    @override
    def init_node_tree(self, node_tree: NodeTree, script: Node):
        input = node_tree.nodes.new("NodeGroupInput")
        node_tree.links.new(input.outputs[0], script.inputs[0])
        node_tree.links.new(input.outputs[1], script.inputs[1])
        node_tree.links.new(input.outputs[2], script.inputs[2])
        node_tree.links.new(input.outputs[3], script.inputs[4])
        node_tree.links.new(input.outputs[4], script.inputs[5])
        node_tree.links.new(input.outputs[5], script.inputs[6])
        node_tree.links.new(input.outputs[6], script.inputs[7])
        node_tree.links.new(input.outputs[7], script.inputs[8])

        offset = node_tree.nodes.new("ShaderNodeAttribute")
        offset.attribute_name = (
            f"{ToonNodeObjectSettings.PROP_NAME}.shadow_terminator_geometry_offset"
        )
        offset.attribute_type = "OBJECT"
        node_tree.links.new(offset.outputs[2], script.inputs[3])

        output = node_tree.nodes.new("NodeGroupOutput")
        node_tree.links.new(script.outputs[0], output.inputs[0])
        node_tree.links.new(script.outputs[1], output.inputs[1])
