from __future__ import annotations

from typing import TYPE_CHECKING, Iterator

from toon.utils import NodeLinkRebinder, all_node_users_itr

from .bridge import get_facade

if TYPE_CHECKING:
    from .core import ToonPalette, ToonPaletteColor, ToonPaletteGroup


def merge_color(src: ToonPaletteColor, dst: ToonPaletteColor) -> bool:
    type = src.type
    dst.type = type

    if type == "COLOR":
        setattr(*dst.color_ptr, getattr(*src.color_ptr))
    elif type == "TEXTURE":
        setattr(*dst.texture_ptr, getattr(*src.texture_ptr))
        setattr(*dst.mute_uv_pixel_snap_ptr, getattr(*src.mute_uv_pixel_snap_ptr))
        setattr(*dst.uv_map_ptr, getattr(*src.uv_map_ptr))
    elif type == "VECTOR":
        setattr(*dst.color_ptr, getattr(*src.color_ptr))
    elif type == "VALUE":
        setattr(*dst.color_ptr, getattr(*src.color_ptr))

    return True


def merge_group(
    src: ToonPaletteGroup, dst: ToonPaletteGroup, overwrite: bool = False
) -> bool:
    if dst.is_linked:
        return False

    for src_color in src.colors():
        if overwrite:
            dst_color = dst.get(src_color.name)
        else:
            dst_color = None

        if dst_color is None:
            dst_color = dst.add(src_color.name)

        if not merge_color(src_color, dst_color):
            return False

    for node in all_node_users_itr(src.node_tree):
        with NodeLinkRebinder(node):
            node.node_tree = dst.node_tree

    return True


def merge_palette(src: ToonPalette, dst: ToonPalette, overwrite: bool = False) -> bool:
    if dst.is_linked:
        return False

    for src_group in src.groups():
        if overwrite:
            dst_group = dst.get(src_group.name)
        else:
            dst_group = None

        if dst_group is None:
            dst_group = dst.add(src_group.name)

        if not merge_group(src_group, dst_group, overwrite):
            return False

    for node in all_node_users_itr(src.header):
        with NodeLinkRebinder(node):
            node.node_tree = dst.header

    return True


def mergable_palettes(src_palette: ToonPalette) -> Iterator[ToonPalette]:
    for dst_palette in get_facade().palettes():
        if not (
            dst_palette.is_orphens
            or dst_palette.is_linked
            or dst_palette.name == src_palette.name_full
        ):
            yield dst_palette


def mergable_groups(
    src_palette: ToonPalette, src_group: ToonPaletteGroup
) -> Iterator[tuple[ToonPalette, ToonPaletteGroup]]:
    for dst_palette in get_facade().palettes():
        if dst_palette.is_linked:
            continue

        if dst_palette.name == src_palette.name_full:
            for dst_group in dst_palette.groups():
                if not (dst_group.is_linked or dst_group.name == src_group.name_full):
                    yield dst_palette, dst_group
        else:
            for dst_group in dst_palette.groups():
                if not dst_group.is_linked:
                    yield dst_palette, dst_group
