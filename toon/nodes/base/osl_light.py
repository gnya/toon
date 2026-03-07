from __future__ import annotations

from typing import TYPE_CHECKING

import bpy
from bpy.props import PointerProperty
from bpy.types import Object

from toon.props import ToonNodeLightSettings
from toon.utils import NodeLinkRebinder, override

from .osl import ToonNodeOSL

if TYPE_CHECKING:
    from bpy.types import Context, Node, NodeSocket, NodeTree, UILayout


class ToonNodeOSLLight(ToonNodeOSL):
    DRIVER_VARIABLE_NAME = "_ToonNodeOSLLight"

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

            anim = node_tree.animation_data

            if anim is None:
                continue

            for fcurve in anim.drivers:
                for variable in fcurve.driver.variables:
                    if variable.name != self.DRIVER_VARIABLE_NAME:
                        continue

                    for target in variable.targets:
                        if target.id == self.object:
                            return node_tree

        return None

    def _add_transform_driver_to_socket(self, socket: NodeSocket, transform_type: str):
        driver = socket.driver_add("default_value").driver
        variable = driver.variables.new()
        variable.name = self.DRIVER_VARIABLE_NAME
        variable.type = "TRANSFORMS"
        target = variable.targets[0]
        target.id = self.object
        target.transform_type = transform_type
        target.transform_space = "WORLD_SPACE"
        driver.expression = self.DRIVER_VARIABLE_NAME

    def _add_property_driver_to_socket(self, socket: NodeSocket, data_path: str):
        driver = socket.driver_add("default_value").driver
        variable = driver.variables.new()
        variable.name = self.DRIVER_VARIABLE_NAME
        variable.type = "SINGLE_PROP"
        target = variable.targets[0]
        target.id = self.object
        target.data_path = f"data.{ToonNodeLightSettings.PROP_NAME}.{data_path}"
        driver.expression = self.DRIVER_VARIABLE_NAME

    def new_location_node(self, node_tree: NodeTree) -> Node:
        node = node_tree.nodes.new("ShaderNodeCombineXYZ")

        self._add_transform_driver_to_socket(node.inputs[0], "LOC_X")
        self._add_transform_driver_to_socket(node.inputs[1], "LOC_Y")
        self._add_transform_driver_to_socket(node.inputs[2], "LOC_Z")

        return node

    def new_rotation_node(self, node_tree: NodeTree) -> Node:
        node = node_tree.nodes.new("ShaderNodeCombineXYZ")

        self._add_transform_driver_to_socket(node.inputs[0], "ROT_X")
        self._add_transform_driver_to_socket(node.inputs[1], "ROT_Y")
        self._add_transform_driver_to_socket(node.inputs[2], "ROT_Z")

        return node

    def new_property_node(self, node_tree: NodeTree, data_path: str) -> Node:
        node = node_tree.nodes.new("ShaderNodeValue")

        self._add_property_driver_to_socket(node.outputs[0], data_path)

        return node

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
        super().draw_buttons(context, layout)

        layout.prop(self, "object", text="Object")
