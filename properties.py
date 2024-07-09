import bpy

from . utils import *
#region Properties


class ObjectPointerProperties(bpy.types.PropertyGroup):
    obj : bpy.props.PointerProperty(type=bpy.types.Object)
class FloatPointerProperties(bpy.types.PropertyGroup):
    value : bpy.props.FloatProperty()
class FloatVectorPointerProperties(bpy.types.PropertyGroup):
    value : bpy.props.FloatVectorProperty()

class TokenProperties(bpy.types.PropertyGroup):

    token_size : bpy.props.FloatProperty(default = 4)


    token_coll : bpy.props.PointerProperty(type= bpy.types.Collection)

    token_id : bpy.props.IntProperty( default = -1)

    distance : bpy.props.FloatProperty( default= 0.0)
        
    feature_vector : bpy.props.CollectionProperty(type = FloatVectorPointerProperties)

    circle_list : bpy.props.CollectionProperty(type = ObjectPointerProperties)

    token : bpy.props.PointerProperty(type=bpy.types.Object)

class TuiProperties(bpy.types.PropertyGroup):

    next_token_id : bpy.props.IntProperty(default=0)

    tokenlist_data_index : bpy.props.IntProperty(
        update=select_token
    )
    tokenlist : bpy.props.CollectionProperty(type = ObjectPointerProperties)
    active_token : bpy.props.PointerProperty(type=bpy.types.Object)
    
    master_coll : bpy.props.PointerProperty(type= bpy.types.Collection)


blender_classes = [
    ObjectPointerProperties,
    FloatPointerProperties,
    FloatVectorPointerProperties,
    TokenProperties,    
    TuiProperties,
    ]
def register():
    for blender_class in blender_classes:
        bpy.utils.register_class(blender_class)
    
    bpy.types.Scene.tui_property = bpy.props.PointerProperty(type = TuiProperties)    
    bpy.types.Object.token_property = bpy.props.PointerProperty(type = TokenProperties)


def unregister():
    for blender_class in blender_classes:
        bpy.utils.unregister_class(blender_class) 
    
    del bpy.types.Scene.tui_property
    del bpy.types.Object.token_property
#endregion Properties