from .node import (
    ToonNodeLightSettings,
    ToonNodeMaterialSettings,
    ToonNodeObjectSettings,
)
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

classes = (
    ToonNodeLightSettings,
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
