from __future__ import annotations

from typing import TYPE_CHECKING

import bpy

from toon.ops import NODE_OT_toon_node_reload_all, NODE_OT_toon_node_setup_osl_render
from toon.utils import override

from .base import ToonNode

if TYPE_CHECKING:
    from bpy.types import Context, NodeTree, UILayout


class ToonNodeInput(ToonNode):
    bl_idname = "ToonNodeInput"
    bl_label = "Toon Input"

    @override
    def new_node_tree(self, name: str) -> tuple[NodeTree, bool]:
        node_tree = bpy.data.node_groups.new(name, "ShaderNodeTree")

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

        node_tree.outputs.new("NodeSocketFloat", "Diffuse")
        node_tree.outputs.new("NodeSocketFloat", "Specular")
        node_tree.outputs.new("NodeSocketVector", "UV")

        input = node_tree.nodes.new("NodeGroupInput")
        light = node_tree.nodes.new("ToonNodeLight")

        material = node_tree.nodes.new("ToonNodeMaterial")
        node_tree.links.new(input.outputs[0], material.inputs[2])
        node_tree.links.new(input.outputs[1], material.inputs[3])
        node_tree.links.new(input.outputs[2], material.inputs[4])
        node_tree.links.new(light.outputs[0], material.inputs[0])
        node_tree.links.new(light.outputs[1], material.inputs[1])

        output = node_tree.nodes.new("NodeGroupOutput")
        node_tree.links.new(material.outputs[0], output.inputs[0])
        node_tree.links.new(material.outputs[1], output.inputs[1])
        node_tree.links.new(light.outputs[3], output.inputs[2])

        return node_tree, light.node_ready and material.node_ready

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
