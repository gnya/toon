from __future__ import annotations

from typing import TYPE_CHECKING, Callable

import bpy
from bpy.app.handlers import depsgraph_update_post, load_post, persistent
from bpy.types import Light, NodeTree, Scene

if TYPE_CHECKING:
    from bpy.types import Depsgraph, DepsgraphUpdate

_node_group_ptrs: list[int] = []
_last_light_type: dict[int, str] = {}

light_type_update_post: list[Callable[[Light], None]] = []
node_group_update_post: list[Callable[[NodeTree], None]] = []
node_group_import_post: list[Callable[[NodeTree], None]] = []
"""
NOTE Alternative to `blend_import_post`.
"""


def _node_group_import(update: DepsgraphUpdate):
    global _node_group_ptrs

    if (
        update.is_updated_shading
        and update.is_updated_geometry
        and update.is_updated_transform
    ):
        if isinstance(update.id, Scene):
            for node_tree in bpy.data.node_groups:
                if node_tree.as_pointer() in _node_group_ptrs:
                    continue

                for callback in node_group_import_post:
                    callback(node_tree)
    else:
        if isinstance(update.id, Scene):
            _node_group_ptrs = [n.as_pointer() for n in bpy.data.node_groups]


def _node_group_update(update: DepsgraphUpdate):
    if (
        update.is_updated_shading
        and not update.is_updated_geometry
        and not update.is_updated_transform
    ):
        if (
            isinstance(update.id, NodeTree)
            and update.id.type == "SHADER"
            and update.id.name != "Shader Nodetree"
        ):
            for callback in node_group_update_post:
                callback(update.id.original)


def _light_type_update(update: DepsgraphUpdate):
    global _last_light_type

    if (
        update.is_updated_geometry
        and update.is_updated_shading
        and update.is_updated_transform
    ):
        # Using `update.id.original` to retrieve the correct pointer.
        id = update.id.original
        type = _last_light_type.get(id.as_pointer(), None)

        if isinstance(update.id, Light) and id.type != type:
            for callback in light_type_update_post:
                callback(id)

            _last_light_type = {l.as_pointer(): l.type for l in bpy.data.lights}


@persistent
def _depsgraph_update(scene: Scene, graph: Depsgraph):
    if graph.mode != "VIEWPORT":
        return False

    for update in graph.updates:
        _node_group_import(update)
        _node_group_update(update)
        _light_type_update(update)


@persistent
def _init_global_variables(scene: Scene):
    global _node_group_ptrs
    global _last_light_type

    _node_group_ptrs = [n.as_pointer() for n in bpy.data.node_groups]
    _last_light_type = {l.as_pointer(): l.type for l in bpy.data.lights}


def register_handlers():
    if _depsgraph_update not in depsgraph_update_post:
        depsgraph_update_post.append(_depsgraph_update)

    if _init_global_variables not in load_post:
        load_post.append(_init_global_variables)


def unregister_handlers():
    if _depsgraph_update in depsgraph_update_post:
        depsgraph_update_post.remove(_depsgraph_update)

    if _init_global_variables in load_post:
        load_post.remove(_init_global_variables)
