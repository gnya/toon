from .hsv_jitter import ToonNodeHSVJitter
from .input import ToonNodeInput
from .lambert import ToonNodeLambert
from .light import ToonNodeLight
from .matcap import ToonNodeMatCap
from .material import ToonNodeMaterial
from .output import ToonNodeOutput
from .palette import ToonNodePalette
from .transform import ToonNodeTransform
from .uv_pixel_snap import ToonNodeUVPixelSnap
from .visualize import ToonNodeVisualize

classes = (
    ToonNodePalette,
    ToonNodeMatCap,
    ToonNodeVisualize,
    ToonNodeHSVJitter,
    ToonNodeUVPixelSnap,
    ToonNodeTransform,
    ToonNodeInput,
    ToonNodeLambert,
    ToonNodeMaterial,
    ToonNodeLight,
    ToonNodeOutput,
)


def register():
    from bpy.utils import register_class

    for cls in classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class

    for cls in classes:
        unregister_class(cls)
