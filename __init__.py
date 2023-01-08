# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "NX_SetOrigin",
    "author" : "Franck Demongin",
    "description" : "Set origin to selected in edit mode",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "View 3D",
    "category" : "Generic"
}

import bpy

class NXSO_OT_set_origin(bpy.types.Operator):    
    """Set origin to selected."""    
    bl_idname = 'nxso.set_origin'
    bl_label = 'Set Origin to Selected'
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        if (
            context.object and
            context.mode == 'EDIT_MESH'
        ):
            return True
        
        return False
    
    def execute(self, context):
        old_cursor_loc = context.scene.cursor.location.copy()
        selected = context.object.select_get()
        context.object.select_set(True)
        
        area = next(iter([area for area in context.screen.areas if area.type == 'VIEW_3D']))
        with context.temp_override(area=area):
            bpy.ops.view3d.snap_cursor_to_selected()
        
        bpy.ops.object.editmode_toggle()    
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')    
        bpy.ops.object.editmode_toggle()    
        context.scene.cursor.location = old_cursor_loc
        context.object.select_set(selected)

        return {'FINISHED'}


def draw_menu(self, context):    
    layout = self.layout
    layout.separator()
    layout.operator('nxso.set_origin', text="Set Origin to Selected")

classes = (
   NXSO_OT_set_origin,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.VIEW3D_MT_edit_mesh.append(draw_menu)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
          
    bpy.types.VIEW3D_MT_edit_mesh.remove(draw_menu)
