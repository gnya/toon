from __future__ import annotations

from typing import TYPE_CHECKING

from bpy.props import IntProperty

from toon.props import ToonNodeSceneSettings
from toon.utils import NodeLinkRebinder, override

from .base import ToonNodeOSL

if TYPE_CHECKING:
    from bpy.types import Context, Node, NodeTree, UILayout


class ToonNodeLight(ToonNodeOSL):
    bl_idname = "ToonNodeLight"
    bl_label = "Light"
    osl_name = "light"

    def _update_light_index(self, context: Context):
        with NodeLinkRebinder(self):
            self.free()
            self.init(context)

    light_index: IntProperty(name="Light Index", default=0, update=_update_light_index)

    def _new_attribute_node(self, node_tree: NodeTree, name: str) -> Node:
        node = node_tree.nodes.new("ShaderNodeAttribute")

        node.attribute_type = "VIEW_LAYER"
        node.attribute_name = (
            f"{ToonNodeSceneSettings.PROP_NAME}.light_{self.light_index}.{name}"
        )

        return node

    @override
    def node_tree_key(self) -> str:
        return f"{super().node_tree_key()}_{self.light_index}"

    @override
    def init_sockets(self, node_tree: NodeTree):
        node_tree.outputs.new("NodeSocketVector", "Light")
        node_tree.outputs.new("NodeSocketFloat", "Ray Length")
        node_tree.outputs.new("NodeSocketColor", "Color")
        node_tree.outputs.new("NodeSocketFloat", "Diffuse Threshold")
        node_tree.outputs.new("NodeSocketFloat", "Specular Threshold")
        node_tree.outputs.new("NodeSocketVector", "UV")

    @override
    def init_node_tree(self, node_tree: NodeTree, script: Node):
        light_type = self._new_attribute_node(node_tree, "light_type")
        location = self._new_attribute_node(node_tree, "location")
        rotation = self._new_attribute_node(node_tree, "rotation")
        color = self._new_attribute_node(node_tree, "color")
        energy = self._new_attribute_node(node_tree, "energy")
        distance = self._new_attribute_node(node_tree, "distance")
        size = self._new_attribute_node(node_tree, "size")
        width = self._new_attribute_node(node_tree, "width")
        height = self._new_attribute_node(node_tree, "height")
        node_tree.links.new(light_type.outputs[2], script.inputs[0])
        node_tree.links.new(location.outputs[1], script.inputs[1])
        node_tree.links.new(rotation.outputs[1], script.inputs[2])
        node_tree.links.new(color.outputs[0], script.inputs[3])
        node_tree.links.new(energy.outputs[2], script.inputs[4])
        node_tree.links.new(distance.outputs[2], script.inputs[5])
        node_tree.links.new(size.outputs[2], script.inputs[6])
        node_tree.links.new(width.outputs[2], script.inputs[7])
        node_tree.links.new(height.outputs[2], script.inputs[8])

        output = node_tree.nodes.new("NodeGroupOutput")
        diffuse_threshold = self._new_attribute_node(node_tree, "diffuse_threshold")
        specular_threshold = self._new_attribute_node(node_tree, "specular_threshold")
        node_tree.links.new(script.outputs[0], output.inputs[0])
        node_tree.links.new(script.outputs[1], output.inputs[1])
        node_tree.links.new(script.outputs[2], output.inputs[2])
        node_tree.links.new(diffuse_threshold.outputs[0], output.inputs[3])
        node_tree.links.new(specular_threshold.outputs[0], output.inputs[4])
        node_tree.links.new(script.outputs[3], output.inputs[5])

    @override
    def draw_buttons(self, context: Context, layout: UILayout):
        super().draw_buttons(context, layout)

        layout.prop(self, "light_index", text="")
