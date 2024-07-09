bl_info = {
    "name" : "TUI Token Generator",
    "author" : "Manuel Fankhaenel",
    "version" :(1, 0),
    "blender" : (3, 1, 0),
    "location" : "View3d > Tool",
    "warning" : "",
    "wiki_url" : "",
    "category" : "",
}

import bpy
import importlib

from . import properties, main_ops, utils, ui

# Reloading the modules to reflect any changes made during development
importlib.reload(properties)
importlib.reload(main_ops)
importlib.reload(ui)
importlib.reload(utils)

# Registering classes and operators from the imported modules
def register():
    properties.register()
    main_ops.register()
    ui.register()

def unregister():
    properties.unregister()
    main_ops.unregister()
    ui.unregister()
  
        


