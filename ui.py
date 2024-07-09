from distutils.log import debug
import bpy

from . utils import *


class TUI_PT_TokenListPanel(bpy.types.Panel):
    """Creates a Panel for all Player Settings"""
    bl_label = "Player"
    bl_idname = "PT_ui_player_list"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'TUI'
    
    def draw(self, context):
        layout = self.layout
        tui_property = context.scene.tui_property

        list_row_layout = layout.row()
        list_row_layout.template_list("TUI_UL_Tokenlist", "", tui_property, "tokenlist", tui_property, "tokenlist_data_index")
        menu_sort_layout_column = list_row_layout.column()
        menu_sort_layout = menu_sort_layout_column.column(align=True)
        menu_sort_layout.operator("token.update", text="", icon="FILE_REFRESH")
        menu_sort_layout.operator("token.add", text="", icon="ADD")
        #menu_sort_layout.operator("list.list_o", text="", icon="ADD").menu_active = 6
        menu_sort_layout.operator("list.token_op", text="", icon="REMOVE").menu_active = 7
        menu_sort_layout2 = menu_sort_layout_column.column(align=True)
        menu_sort_layout.separator(factor=3.0)
        menu_sort_layout2.operator("list.token_op", text="", icon="TRIA_UP").menu_active = 4
        menu_sort_layout2.operator("list.token_op", text="", icon="TRIA_DOWN").menu_active = 5


        col = layout.column()
        row = layout.row()

        for token in tui_property.tokenlist:
            if bpy.context.object == token.obj: 
                token_property = token.obj.token_property
                layout.prop(token_property, "token_id")
               
                list_row = layout.row()
                list_row.prop(token_property, "distance", text="")
                list_row.prop(token_property, "token_id", text="")
                break

#endregion
#region lists
class TUI_UL_Tokenlist(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        ob = data
        slot = item
        ma = slot.name
        token_property = slot.obj.token_property


        tui_property = context.scene.tui_property
        # draw_item must handle the three layout types... Usually 'DEFAULT' and 'COMPACT' can share the same code.
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            split = layout.split(factor=0.3)
            row = layout.row(align=True)
            if ma:
                split.prop(slot, "name", text="", emboss=False, icon_value=icon)
                split.prop(token_property, "distance", text="", emboss=False)
                split.prop(token_property.token_coll, "hide_viewport", text="", emboss=False, icon_value=icon)
            else:
                split.label(text="", translate=False, icon_value=icon)
        # 'GRID' layout type should be as compact as possible (typically a single icon!).
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=icon)

class Token_List_Button(bpy.types.Operator):
    """List Operations"""
    bl_idname = "list.token_op"
    bl_label = "Token List Operator"
    bl_description = "List Operations"
    bl_options = {"REGISTER", "UNDO"}

    menu_active: bpy.props.IntProperty(name="Button Index")

    def execute(self, context):
        tui_property = context.scene.tui_property

        list = tui_property.tokenlist
        index = tui_property.tokenlist_data_index
        
        if self.menu_active == 1:
            print("Select")
            pass
			
        if self.menu_active == 2:
            anim_entry = list[index]
            anim_entry.width = anim_entry.width + 1

        if self.menu_active == 3:
            list.clear()

		# Move entry up
        if self.menu_active == 4:
            if index > 0:
                list.move(index, index-1)
                index -= 1

		# Move entry down
        if self.menu_active == 5:
            if index < len(list)-1:
                list.move(index, index+1)
                index += 1
        
        # Add entry
        if self.menu_active == 6:
            item = index.add()
            if len(bpy.data.actions) > 0:
                item.action = bpy.data.actions[0]
            if index < len(list)-1:
                list.move(len(list)-1, index+1)
                index += 1

		# Remove Item
        if self.menu_active == 7:
            if index >= 0 and index < len(list):
                collection = list[index].obj.token_property.token_coll
                delete_hierarchy(list[index].obj)
                list.remove(index)
                index = min(index, len(list)-1)
                bpy.context.scene.collection.children.unlink(collection)
               
        return {"FINISHED"}


blender_classes = [
    TUI_PT_TokenListPanel,
    TUI_UL_Tokenlist,
    Token_List_Button
]
    
def register():
    for blender_class in blender_classes:
        bpy.utils.register_class(blender_class)


def unregister():
    for blender_class in blender_classes:
        bpy.utils.unregister_class(blender_class) 
    
