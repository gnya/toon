from __future__ import annotations

import math

from bpy.props import (
    EnumProperty,
    FloatProperty,
    FloatVectorProperty,
    IntProperty,
    PointerProperty,
)
from bpy.types import Light, Material, Object, PropertyGroup, Scene
from mathutils import Color, Euler, Vector


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

    def _get_color(self) -> Color:
        return self.id_data.color

    def _get_energy(self) -> float:
        return self.id_data.energy

    color: FloatVectorProperty(
        name="Color",
        get=_get_color,
    )

    energy: FloatProperty(
        name="Energy",
        get=_get_energy,
    )

    diffuse_threshold: FloatProperty(
        name="Diffuse Threshold",
        default=0.1,
        min=0.0,
        max=1.0,
        subtype="FACTOR",
    )

    specular_threshold: FloatProperty(
        name="Specular Threshold",
        default=0.1,
        min=0.0,
        max=1.0,
        subtype="FACTOR",
    )

    distance: FloatProperty(
        name="Distance",
        default=1.0,
        min=0.0,
        max=float("inf"),
        subtype="DISTANCE",
    )

    size: FloatProperty(
        name="Size",
        default=math.pi / 4.0,
        min=0.0,
        max=math.pi,
        subtype="ANGLE",
    )

    width: FloatProperty(
        name="Width",
        default=1.0,
        min=0.0,
        max=float("inf"),
        subtype="DISTANCE",
    )

    height: FloatProperty(
        name="Height",
        default=1.0,
        min=0.0,
        max=float("inf"),
        subtype="DISTANCE",
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


class ToonNodeSceneLight(PropertyGroup):
    PROP_NAME = "toon_node_scene_light"

    def _poll_light(self, obj: Object) -> bool:
        return obj.type in {"LIGHT"}

    light: PointerProperty(type=Object, poll=_poll_light)

    def _get_light_type(self) -> int:
        if self.light is None or self.light.data is None:
            return -1
        else:
            return ["POINT", "SUN", "SPOT", "AREA"].index(self.light.data.type)

    def _get_location(self) -> Vector:
        if self.light is None:
            return Vector((0.0, 0.0, 0.0))
        else:
            return self.light.matrix_world.translation

    def _get_rotation(self) -> Euler:
        if self.light is None:
            return Euler((0.0, 0.0, 0.0))
        else:
            return self.light.matrix_world.to_euler()

    def _get_color(self) -> Color:
        if self.light is None:
            return Color((0.0, 0.0, 0.0))
        else:
            return ToonNodeLightSettings.instance(self.light.data).color

    def _get_energy(self) -> float:
        if self.light is None:
            return 1.0
        else:
            return ToonNodeLightSettings.instance(self.light.data).energy

    def _get_diffuse_threshold(self) -> float:
        if self.light is None:
            return 0.1
        else:
            return ToonNodeLightSettings.instance(self.light.data).diffuse_threshold

    def _get_specular_threshold(self) -> float:
        if self.light is None:
            return 0.1
        else:
            return ToonNodeLightSettings.instance(self.light.data).specular_threshold

    def _get_distance(self) -> float:
        if self.light is None:
            return 1.0
        else:
            return ToonNodeLightSettings.instance(self.light.data).distance

    def _get_size(self) -> float:
        if self.light is None:
            return math.pi / 4.0
        else:
            return ToonNodeLightSettings.instance(self.light.data).size

    def _get_width(self) -> float:
        if self.light is None:
            return 1.0
        else:
            return ToonNodeLightSettings.instance(self.light.data).width

    def _get_height(self) -> float:
        if self.light is None:
            return 1.0
        else:
            return ToonNodeLightSettings.instance(self.light.data).height

    light_type: IntProperty(get=_get_light_type)

    location: FloatVectorProperty(get=_get_location)

    rotation: FloatVectorProperty(get=_get_rotation)

    color: FloatVectorProperty(get=_get_color)

    energy: FloatProperty(get=_get_energy)

    diffuse_threshold: FloatProperty(get=_get_diffuse_threshold)

    specular_threshold: FloatProperty(get=_get_specular_threshold)

    distance: FloatProperty(get=_get_distance)

    size: FloatProperty(get=_get_size)

    width: FloatProperty(get=_get_width)

    height: FloatProperty(get=_get_height)

    @staticmethod
    def instance(id: Scene) -> ToonNodeLightSettings:
        return getattr(id, ToonNodeSceneLight.PROP_NAME)

    @staticmethod
    def register():
        setattr(
            Scene,
            ToonNodeSceneLight.PROP_NAME,
            PointerProperty(type=ToonNodeSceneLight),
        )

    @staticmethod
    def unregister():
        delattr(Scene, ToonNodeSceneLight.PROP_NAME)
