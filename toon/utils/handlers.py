from __future__ import annotations

from typing import TYPE_CHECKING, Callable

import bpy
from bpy.app.handlers import depsgraph_update_post, load_post, persistent
from bpy.types import NodeTree, Scene

if TYPE_CHECKING:
    from bpy.types import Depsgraph, DepsgraphUpdate

_node_group_ptrs: list[int] = []

node_group_update_post: list[Callable[[NodeTree], None]] = []
node_group_import_post: list[Callable[[NodeTree], None]] = []
"""
NOTE Alternative to `blend_import_post`.
"""


def _poll_node_group_update(graph: Depsgraph) -> bool:
    if graph.mode != "VIEWPORT":
        return False

    for update in graph.updates:
        if update.is_updated_shading:
            return True

    return False


def _node_group_import(update: DepsgraphUpdate):
    global _node_group_ptrs

    if update.is_updated_geometry and update.is_updated_transform:
        for node_tree in bpy.data.node_groups:
            if node_tree.as_pointer() not in _node_group_ptrs:
                for callback in node_group_import_post:
                    callback(node_tree)

    _node_group_ptrs = [n.as_pointer() for n in bpy.data.node_groups]


@persistent
def _node_group_update(scene: Scene, graph: Depsgraph):
    if not _poll_node_group_update(graph):
        return

    for update in graph.updates:
        origin = update.id.original

        if isinstance(origin, Scene):
            _node_group_import(update)
        elif (
            isinstance(origin, NodeTree)
            and origin.type == "SHADER"
            and origin.name != "Shader Nodetree"
        ):
            for callback in node_group_update_post:
                callback(origin)


@persistent
def _init_global_variables(scene: Scene):
    global _node_group_ptrs

    _node_group_ptrs = [n.as_pointer() for n in bpy.data.node_groups]


def register_handlers():
    if _node_group_update not in depsgraph_update_post:
        depsgraph_update_post.append(_node_group_update)

    if _init_global_variables not in load_post:
        load_post.append(_init_global_variables)


def unregister_handlers():
    if _node_group_update in depsgraph_update_post:
        depsgraph_update_post.remove(_node_group_update)

    if _init_global_variables in load_post:
        load_post.remove(_init_global_variables)
