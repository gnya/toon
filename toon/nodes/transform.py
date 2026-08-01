from __future__ import annotations

from typing import TYPE_CHECKING

import bpy
from bpy.props import PointerProperty, StringProperty
from bpy.types import Object

from toon.utils import NodeLinkRebinder, override

from .base import ToonNode

if TYPE_CHECKING:
    from bpy.types import Context, Node, NodeSocket, NodeTree, UILayout


class ToonNodeTransform(ToonNode):
    bl_idname = "ToonNodeTransform"
    bl_label = "Transform"
    DRIVER_VARIABLE_NAME = "_ToonNodeTransform"

    def _update_object(self, context: Context):
        # Call _update_bone.
        self.bone = ""

    def _update_bone(self, context: Context):
        with NodeLinkRebinder(self):
            self.free()
            self.init(context)

    object: PointerProperty(name="Object", type=Object, update=_update_object)

    bone: StringProperty(name="Bone", update=_update_bone)

    def _get_node_tree(self, name: str) -> NodeTree | None:
        for node_tree in bpy.data.node_groups:
            if node_tree.name.startswith(name) and any(
                t.id == self.object and t.bone_target == self.bone
                for f in node_tree.animation_data.drivers
                for v in f.driver.variables
                if v.name == self.DRIVER_VARIABLE_NAME
                for t in v.targets
            ):
                return node_tree

        return None

    def _add_transform_driver_to_socket(self, socket: NodeSocket, transform_type: str):
        driver = socket.driver_add("default_value").driver
        variable = driver.variables.new()
        variable.name = self.DRIVER_VARIABLE_NAME
        variable.type = "TRANSFORMS"
        target = variable.targets[0]
        target.id = self.object
        target.bone_target = self.bone
        target.transform_type = transform_type
        target.transform_space = "WORLD_SPACE"
        driver.expression = self.DRIVER_VARIABLE_NAME

    def _new_location_node(self, node_tree: NodeTree) -> Node:
        node = node_tree.nodes.new("ShaderNodeCombineXYZ")

        self._add_transform_driver_to_socket(node.inputs[0], "LOC_X")
        self._add_transform_driver_to_socket(node.inputs[1], "LOC_Y")
        self._add_transform_driver_to_socket(node.inputs[2], "LOC_Z")

        return node

    def _new_rotation_node(self, node_tree: NodeTree) -> Node:
        node = node_tree.nodes.new("ShaderNodeCombineXYZ")

        self._add_transform_driver_to_socket(node.inputs[0], "ROT_X")
        self._add_transform_driver_to_socket(node.inputs[1], "ROT_Y")
        self._add_transform_driver_to_socket(node.inputs[2], "ROT_Z")

        return node

    def _new_scale_node(self, node_tree: NodeTree) -> Node:
        node = node_tree.nodes.new("ShaderNodeCombineXYZ")

        self._add_transform_driver_to_socket(node.inputs[0], "SCALE_X")
        self._add_transform_driver_to_socket(node.inputs[1], "SCALE_Y")
        self._add_transform_driver_to_socket(node.inputs[2], "SCALE_Z")

        return node

    @override
    def new_node_tree(self, name: str) -> tuple[NodeTree, bool]:
        node_tree = bpy.data.node_groups.new(name, "ShaderNodeTree")

        node_tree.outputs.new("NodeSocketVector", "Location")
        node_tree.outputs.new("NodeSocketVector", "Rotation")
        node_tree.outputs.new("NodeSocketVector", "Scale")

        location = self._new_location_node(node_tree)
        rotation = self._new_rotation_node(node_tree)
        scale = self._new_scale_node(node_tree)

        output = node_tree.nodes.new("NodeGroupOutput")
        node_tree.links.new(location.outputs[0], output.inputs[0])
        node_tree.links.new(rotation.outputs[0], output.inputs[1])
        node_tree.links.new(scale.outputs[0], output.inputs[2])

        return node_tree, True

    @override
    def get_node_tree(self) -> tuple[NodeTree | None, bool]:
        name = self.node_tree_key()

        if name == "":
            return None, False
        elif (node_tree := self._get_node_tree(name)) is None:
            return self.new_node_tree(name)
        else:
            return node_tree, True

    @override
    def draw_buttons(self, context: Context, layout: UILayout):
        super().draw_buttons(context, layout)

        layout.prop(self, "object", text="Object")

        if self.object is not None and self.object.type == "ARMATURE":
            layout.prop_search(self, "bone", self.object.data, "bones")
