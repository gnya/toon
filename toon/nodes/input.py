from __future__ import annotations

from typing import TYPE_CHECKING

import bpy

from toon.ops import NODE_OT_toon_node_reload_all, NODE_OT_toon_node_setup_osl_render
from toon.props import ToonNodeSceneSettings
from toon.utils import override

from .base import ToonNode

if TYPE_CHECKING:
    from bpy.types import Context, Node, NodeTree, UILayout


class ToonNodeInput(ToonNode):
    bl_idname = "ToonNodeInput"
    bl_label = "Toon Input"

    def _new_attribute_node(self, node_tree: NodeTree, name: str) -> Node:
        node = node_tree.nodes.new("ShaderNodeAttribute")

        node.attribute_type = "VIEW_LAYER"
        node.attribute_name = f"{ToonNodeSceneSettings.PROP_NAME}.{name}"

        return node

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

        node_tree.outputs.new("NodeSocketColor", "Diffuse")
        node_tree.outputs.new("NodeSocketColor", "Specular")
        node_tree.outputs.new("NodeSocketVector", "UV")

        input = node_tree.nodes.new("NodeGroupInput")
        light = node_tree.nodes.new("ToonNodeLight")

        material = node_tree.nodes.new("ToonNodeMaterial")
        node_tree.links.new(input.outputs[0], material.inputs[2])
        node_tree.links.new(input.outputs[1], material.inputs[3])
        node_tree.links.new(input.outputs[2], material.inputs[4])
        node_tree.links.new(light.outputs[0], material.inputs[0])
        node_tree.links.new(light.outputs[1], material.inputs[1])
        node_tree.links.new(light.outputs[2], material.inputs[5])
        node_tree.links.new(light.outputs[3], material.inputs[6])
        node_tree.links.new(light.outputs[4], material.inputs[7])

        preview_diffuse = node_tree.nodes.new("ShaderNodeBsdfDiffuse")
        preview_diffuse.inputs[0].default_value = (1.0, 1.0, 1.0, 1.0)
        node_tree.links.new(input.outputs[0], preview_diffuse.inputs[2])

        shader_to_rgb = node_tree.nodes.new("ShaderNodeShaderToRGB")
        node_tree.links.new(preview_diffuse.outputs[0], shader_to_rgb.inputs[0])

        binalize = node_tree.nodes.new("ShaderNodeMath")
        binalize.operation = "GREATER_THAN"
        preview_threshold = self._new_attribute_node(node_tree, "preview_threshold")
        node_tree.links.new(shader_to_rgb.outputs[0], binalize.inputs[0])
        node_tree.links.new(preview_threshold.outputs[2], binalize.inputs[1])

        mix = node_tree.nodes.new("ShaderNodeMixRGB")
        is_osl = node_tree.nodes.new("ToonNodeIsOSL")
        node_tree.links.new(is_osl.outputs[0], mix.inputs[0])
        node_tree.links.new(binalize.outputs[0], mix.inputs[1])
        node_tree.links.new(material.outputs[0], mix.inputs[2])

        output = node_tree.nodes.new("NodeGroupOutput")
        node_tree.links.new(mix.outputs[0], output.inputs[0])
        node_tree.links.new(material.outputs[1], output.inputs[1])
        node_tree.links.new(light.outputs[5], output.inputs[2])

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
