from __future__ import annotations

from typing import TYPE_CHECKING

import bpy
from bpy.props import PointerProperty
from bpy.types import Object

from toon.ops import NODE_OT_toon_node_reload_all, NODE_OT_toon_node_setup_osl_render
from toon.utils import NodeLinkRebinder, all_node_itr, light_type_update_post, override

from .base import ToonNode

if TYPE_CHECKING:
    from bpy.types import Context, Light, NodeTree, UILayout


class ToonNodeInput(ToonNode):
    bl_idname = "ToonNodeInput"
    bl_label = "Toon Input"

    def _poll_object(self, obj: Object) -> bool:
        return obj.type in {"LIGHT"}

    def _update_object(self, context: Context):
        with NodeLinkRebinder(self):
            self.free()
            self.init(context)

    object: PointerProperty(
        name="Object", type=Object, poll=_poll_object, update=_update_object
    )

    def _get_node_tree(self, name: str) -> NodeTree | None:
        for node_tree in bpy.data.node_groups:
            if not node_tree.name.startswith(name):
                continue

            for node in node_tree.nodes:
                if hasattr(node, "object") and node.object == self.object:
                    return node_tree

        return None

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

        type = "SUN" if self.object is None else self.object.data.type

        if type == "POINT":
            light = node_tree.nodes.new("ToonNodeLightPoint")
        elif type == "SUN":
            light = node_tree.nodes.new("ToonNodeLightSun")
        elif type == "SPOT":
            light = node_tree.nodes.new("ToonNodeLightSpot")
        elif type == "AREA":
            light = node_tree.nodes.new("ToonNodeLightArea")
        else:
            raise ValueError(f"Unknown data type. : {type}")

        light.object = self.object

        material = node_tree.nodes.new("ToonNodeMaterial")
        node_tree.links.new(light.outputs[0], material.inputs[0])
        node_tree.links.new(light.outputs[1], material.inputs[1])
        node_tree.links.new(input.outputs[0], material.inputs[2])
        node_tree.links.new(input.outputs[1], material.inputs[3])
        node_tree.links.new(input.outputs[2], material.inputs[4])

        output = node_tree.nodes.new("NodeGroupOutput")
        node_tree.links.new(material.outputs[0], output.inputs[0])
        node_tree.links.new(material.outputs[1], output.inputs[1])
        node_tree.links.new(light.outputs[2], output.inputs[2])

        return node_tree, light.node_ready and material.node_ready

    @override
    def get_node_tree(self) -> tuple[NodeTree | None, bool]:
        name, _ = self.node_tree_key()

        if name == "":
            return None, False
        elif (node_tree := self._get_node_tree(name)) is None:
            return self.new_node_tree(name)
        else:
            return node_tree, True

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

        layout.prop(self, "object", text="Object")

    @staticmethod
    def _sync_light_type(light: Light):
        for node in all_node_itr():
            if isinstance(node, ToonNodeInput):
                if node.object.data == light:
                    node.reload()

    @staticmethod
    def register():
        if ToonNodeInput._sync_light_type not in light_type_update_post:
            light_type_update_post.append(ToonNodeInput._sync_light_type)

    @staticmethod
    def unregister():
        if ToonNodeInput._sync_light_type in light_type_update_post:
            light_type_update_post.remove(ToonNodeInput._sync_light_type)
