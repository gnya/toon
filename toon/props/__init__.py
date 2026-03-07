from .node import ToonNodeMaterialSettings, ToonNodeObjectSettings
from .palette import (
    ToonPaletteProperty,
    ToonPaletteSearchGroup,
    ToonPaletteSearchIndex,
    ToonPaletteSearchPalette,
    ToonPaletteUIItem,
    ToonPaletteUIPaletteState,
    ToonPaletteUIState,
    ToonPaletteViewSettings,
)

__all__ = [
    ToonNodeMaterialSettings,
    ToonNodeObjectSettings,
    ToonPaletteProperty,
    ToonPaletteSearchGroup,
    ToonPaletteSearchPalette,
    ToonPaletteSearchIndex,
    ToonPaletteViewSettings,
    ToonPaletteUIItem,
    ToonPaletteUIPaletteState,
    ToonPaletteUIState,
]


classes = (
    ToonNodeMaterialSettings,
    ToonNodeObjectSettings,
    ToonPaletteProperty,
    ToonPaletteSearchGroup,
    ToonPaletteSearchPalette,
    ToonPaletteSearchIndex,
    ToonPaletteViewSettings,
    ToonPaletteUIItem,
    ToonPaletteUIPaletteState,
    ToonPaletteUIState,
)


def register():
    from bpy.utils import register_class

    for c in classes:
        register_class(c)


def unregister():
    from bpy.utils import unregister_class

    for c in classes:
        unregister_class(c)
