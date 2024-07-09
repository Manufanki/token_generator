
import bpy
import random

from .properties import *
from .utils import *
from .ui import *

class TOKEN_add(bpy.types.Operator):
    "Add Token"
    bl_idname = "token.add"
    bl_label = "Add Token"
    

    RADIUS : bpy.props.FloatProperty(name ="Radius", default= 0.4)
    MIN_DISTANCE : bpy.props.FloatProperty(name ="Min Distance", default= 1.6)
    LARGE_CIRCLE_DIAMETER : bpy.props.FloatProperty(name ="Large Circle Diameter", default= 4)
    MIN_SIGMA : bpy.props.FloatProperty(name ="Min Sigma", default= 0.2)
    MAX_SIGMA : bpy.props.FloatProperty(name ="Max Sigma", default= 0.6)
    MIN_D : bpy.props.FloatProperty(name ="Min D", default= 1)
    MAX_ATTEMPTS : bpy.props.IntProperty(name ="Max Attempts", default= 50000)

    def invoke(self, context, event):
                
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):

        MAX_DISTANCE = self.LARGE_CIRCLE_DIAMETER - 2 * self.RADIUS
        LARGE_CIRCLE_RADIUS = self.LARGE_CIRCLE_DIAMETER / 2
        tui_property = bpy.context.scene.tui_property
        
        # Generate three circles within the constraints
        circles = []
        best_circles = []
        attempts = 0
        best_d = 0

        while attempts < self.MAX_ATTEMPTS:
            x, y = random.uniform(-LARGE_CIRCLE_RADIUS + self.RADIUS, LARGE_CIRCLE_RADIUS - self.RADIUS), random.uniform(-LARGE_CIRCLE_RADIUS + self.RADIUS, LARGE_CIRCLE_RADIUS - self.RADIUS)
            valid = point_within_large_circle(x, y,self.RADIUS, LARGE_CIRCLE_RADIUS)
            
            for cx, cy in circles:
                if not circles_within_distance_constraints(x, y, cx, cy, self.MIN_DISTANCE, MAX_DISTANCE):
                    valid = False
                    break
            
            if valid:
                circles.append((x, y))
            
            # Check if we have three valid circles
            if len(circles) == 3:
                stddev = calculate_side_length_stddev(circles)
                if stddev > self.MIN_SIGMA and stddev < self.MAX_SIGMA:
                    f = get_feature_vectors(circles)
                    
                    d_list =[]
                    if len(tui_property.tokenlist) > 0:
                        for pToken in tui_property.tokenlist:
                            d = min_euclidean_norm(f[0], pToken.obj.token_property.feature_vector[0].value,pToken.obj.token_property.feature_vector[1].value,pToken.obj.token_property.feature_vector[2].value)
                            d_list.append(d)
                            
                        if min(d_list) > self.MIN_D and max(d_list) > best_d:
                            best_d = max(d_list)
                            best_circles = circles.copy()
                    else:
                        best_circles = circles.copy()

                circles.clear()
                            
            attempts += 1

        print("Best Circles 3: ", len(best_circles))
        if len(best_circles) < 3:
            print("Failed to place three circles within the constraints after {} attempts".format(attempts))
        else:   
            
            bpy.ops.mesh.primitive_circle_add(vertices=36, radius=LARGE_CIRCLE_RADIUS, location=(0, 0, 0))
            token = bpy.context.object      

            token_property = token.token_property
            token_property.token_id = tui_property.next_token_id
            tui_property.next_token_id += 1

            token_property.token_coll = addToCollection(self, context, "Token_" + str(token_property.token_id) , token)

            token_property.distance = best_d
            token_property.token_size = LARGE_CIRCLE_RADIUS * 2
            token_pointer = tui_property.tokenlist.add()
            token_pointer.name = "token_{}".format(len(token_property.token_id))
            token_pointer.obj = token
            
            center = find_centroid(best_circles)
            # Create circles in Blender
            for i, (x, y) in enumerate(best_circles):
                bpy.ops.mesh.primitive_cylinder_add(vertices=36, radius=self.RADIUS,depth=.3, location=(center[0] - x, center[1] - y, -.15))
                obj = bpy.context.object
                obj.parent = token
                addToCollection(self, context, "Token_" + str(token_property.token_id) , obj)
            feature_vectors = get_feature_vectors(best_circles)
            for feature in feature_vectors:
                feature_vector =  token_property.feature_vector.add()
                feature_vector.value = feature  




        return {'FINISHED'}


class TOKEN_update(bpy.types.Operator):
    """Recalculates the distance between all tokens"""
    bl_idname = "token.update"
    bl_label = "Update tokens"
    
    def execute(self, context):
        update_tokens(self,context)
        return {'FINISHED'}
blender_classes = [
    TOKEN_add,
    TOKEN_update
    
]

# Register and add to the "file selector" menu (required to use F3 search "Text Import Operator" for quick access)
def register():
    for blender_class in blender_classes:
        bpy.utils.register_class(blender_class)


def unregister():
    for blender_class in blender_classes:
        bpy.utils.unregister_class(blender_class)    
        

