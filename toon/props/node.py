from __future__ import annotations

import math

from bpy.props import EnumProperty, FloatProperty, IntProperty, PointerProperty
from bpy.types import Light, Material, Object, PropertyGroup


class ToonNodeIDProperties(PropertyGroup):
    def _set_cast_shadows(self, value: int):
        self.id_data.pass_index = (value << 12) | (self.id_data.pass_index & ~(7 << 12))

    def _set_shadow_id(self, value: int):
        self.id_data.pass_index = (value << 0) | (self.id_data.pass_index & ~(63 << 0))

    def _set_transparent_id(self, value: int):
        self.id_data.pass_index = (value << 6) | (self.id_data.pass_index & ~(63 << 6))

    def _get_cast_shadows(self) -> int:
        return (self.id_data.pass_index >> 12) & 7

    def _get_shadow_id(self) -> int:
        return (self.id_data.pass_index >> 0) & 63

    def _get_transparent_id(self) -> int:
        return (self.id_data.pass_index >> 6) & 63

    shadow_casting_types = [
        ("0", "Enable", ""),
        ("1", "Only Front Surface", ""),
        ("2", "Disable", ""),
    ]

    cast_shadows: EnumProperty(
        name="Cast Shadows",
        default="0",
        items=shadow_casting_types,
        set=_set_cast_shadows,
        get=_get_cast_shadows,
    )

    shadow_id: IntProperty(
        name="Shadow ID",
        default=0,
        min=0,
        max=63,
        set=_set_shadow_id,
        get=_get_shadow_id,
    )

    transparent_id: IntProperty(
        name="Transparent ID",
        default=0,
        min=0,
        max=63,
        set=_set_transparent_id,
        get=_get_transparent_id,
    )


class ToonNodeMaterialSettings(ToonNodeIDProperties):
    PROP_NAME = "toon_node_material_settings"

    @staticmethod
    def instance(id: Material) -> ToonNodeMaterialSettings:
        return getattr(id, ToonNodeMaterialSettings.PROP_NAME)

    @staticmethod
    def register():
        setattr(
            Material,
            ToonNodeMaterialSettings.PROP_NAME,
            PointerProperty(type=ToonNodeMaterialSettings),
        )

    @staticmethod
    def unregister():
        delattr(Material, ToonNodeMaterialSettings.PROP_NAME)


class ToonNodeObjectSettings(ToonNodeIDProperties):
    PROP_NAME = "toon_node_object_settings"

    shadow_terminator_geometry_offset: FloatProperty(
        name="Geometry Offset", default=0.1, min=0.0, max=1.0
    )

    @staticmethod
    def instance(id: Object) -> ToonNodeObjectSettings:
        return getattr(id, ToonNodeObjectSettings.PROP_NAME)

    @staticmethod
    def register():
        setattr(
            Object,
            ToonNodeObjectSettings.PROP_NAME,
            PointerProperty(type=ToonNodeObjectSettings),
        )

    @staticmethod
    def unregister():
        delattr(Object, ToonNodeObjectSettings.PROP_NAME)


class ToonNodeLightSettings(PropertyGroup):
    PROP_NAME = "toon_node_light_settings"

    def _get_energy(self) -> float:
        return self.id_data.energy

    def _set_energy(self, value: float):
        self.id_data.energy = value

    energy: FloatProperty(
        name="Energy", soft_min=0.0, soft_max=10.0, get=_get_energy, set=_set_energy
    )

    distance: FloatProperty(
        name="Distance", default=1.0, min=0.0, max=float("inf"), subtype="DISTANCE"
    )

    width: FloatProperty(
        name="Width", default=1.0, min=0.0, max=float("inf"), subtype="DISTANCE"
    )

    height: FloatProperty(
        name="Height", default=1.0, min=0.0, max=float("inf"), subtype="DISTANCE"
    )

    size: FloatProperty(
        name="Size", default=math.pi / 4.0, min=0.0, max=math.pi, subtype="ANGLE"
    )

    @staticmethod
    def instance(id: Light) -> ToonNodeLightSettings:
        return getattr(id, ToonNodeLightSettings.PROP_NAME)

    @staticmethod
    def register():
        setattr(
            Light,
            ToonNodeLightSettings.PROP_NAME,
            PointerProperty(type=ToonNodeLightSettings),
        )

    @staticmethod
    def unregister():
        delattr(Light, ToonNodeLightSettings.PROP_NAME)
