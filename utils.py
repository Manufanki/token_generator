import bpy
import math
import numpy as np


def check_if_collection_exists(name, i = 0, collection = None):
        
    tmp_name = name
    if i != 0:
        tmp_name = name + "." + str(i)
    if bpy.data.collections.get(tmp_name) is None:
        collection = bpy.data.collections.new(tmp_name)
        return collection
    else:
        i+=1
        collection = check_if_collection_exists(name, i)

    if collection is not None:
        return collection

def update_collection_name(self, contex, collection):
    try:
        self.annotation.name = self.name
    except:
        try:
            self.annotation.layers[collection.name].name = self.name
        except Exception as e:
            print(e)
    collection.name = self.name

def delete_hierarchy(obj):
    names = set([obj.name])
    
    # recursion
    def get_child_names(obj):
        for child in obj.children:
            names.add(child.name)
            if child.children:
                get_child_names(child)

    get_child_names(obj)

    for n in names:
        bpy.data.objects.remove(bpy.data.objects[n], do_unlink=True)

def obj_in_objectlist(obj, list):
    for item in list:
        if item.obj == obj:
            return True
    return False
   
def addToCollection(self,context, collectionName, obj):
    for coll in obj.users_collection:
            # Unlink the object
            coll.objects.unlink(obj)

    if bpy.data.collections.get(collectionName) is None:
        collection = bpy.data.collections.new(collectionName)
        bpy.context.scene.collection.children.link(collection)
    else:
        collection = bpy.data.collections.get(collectionName)
    collection.objects.link(obj)
    return collection

#region tui

def distance_between_points(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def calculate_distance(p1,p2):
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[0]) ** 2) 


# Function to check if a point is within the large circle
def point_within_large_circle(x, y, radius, large_radius):
    return math.sqrt(x ** 2 + y ** 2) + radius <= large_radius

# Function to check if two circles are within the distance constraints
def circles_within_distance_constraints(x1, y1, x2, y2, min_distance, max_distance):
    distance = distance_between_points(x1, y1, x2, y2)
    return min_distance <= distance <= max_distance

# Function to calculate the standard deviation of the side lengths of a triangle
def calculate_side_length_stddev(points):
    side_lengths = [
        distance_between_points(points[0][0], points[0][1], points[1][0], points[1][1]),
        distance_between_points(points[1][0], points[1][1], points[2][0], points[2][1]),
        distance_between_points(points[2][0], points[2][1], points[0][0], points[0][1])
    ]
    return np.std(side_lengths)

def find_centroid(points):
    x = 0
    y = 0
    for p in points:
        x += p[0]
        y += p[1]
    
    center = ( x / len(points), y / len(points))
    return center

def euclidean_norm(vector):
    return math.sqrt(sum([x ** 2 for x in vector]))

def min_euclidean_norm(g, f1, f2, f3):
    d1 = euclidean_norm([g[i] - f1[i] for i in range(len(g))])
    d2 = euclidean_norm([g[i] - f2[i] for i in range(len(g))])
    d3 = euclidean_norm([g[i] - f3[i] for i in range(len(g))])
    return min(d1, d2, d3)


def get_feature_vectors(points):
    center = find_centroid(points)

    # Calculate angles for each point and store as tuples
    angles = [(point[0], point[1], math.atan2(point[1] - center[1], point[0] - center[0]) * 180 / math.pi) for point in points]

    # Sort vertices by angle
    sorted_vertices = sorted(angles, key=lambda point: point[2])

    # Calculate side lengths
    side_lengths = [
        calculate_distance(sorted_vertices[0], sorted_vertices[1]),
        calculate_distance(sorted_vertices[1], sorted_vertices[2]),
        calculate_distance(sorted_vertices[2], sorted_vertices[0])
    ]

    # Create feature vectors
    feature_vectors = [
        [side_lengths[0], side_lengths[1], side_lengths[2]],
        [side_lengths[2], side_lengths[0], side_lengths[1]],
        [side_lengths[1], side_lengths[2], side_lengths[0]]
    ]
    return feature_vectors

def select_token(self, context):
    bpy.ops.object.select_all(action='DESELECT')
    if self.tokenlist_data_index != -1:
        for token in self.tokenlist:
            token.obj.select_set(False)
        self.tokenlist[self.tokenlist_data_index].obj.select_set(True)
        bpy.context.view_layer.objects.active =  self.tokenlist[self.tokenlist_data_index].obj

def update_tokens(self, context):
    tui_property = context.scene.tui_property
    tokenlist = tui_property.tokenlist
    if len(tui_property.tokenlist) > 0:
        for i in range(len(tokenlist)):
            f = tokenlist[i].obj.token_property.feature_vector
            res = 100000
            for j in range(len(tokenlist)):
                if i != j:   
                    pToken = tokenlist[j]
                    d = min_euclidean_norm(f[0].value, pToken.obj.token_property.feature_vector[0].value,pToken.obj.token_property.feature_vector[1].value,pToken.obj.token_property.feature_vector[2].value)
                    if d < res:
                        res = d
            tokenlist[i].obj.token_property.distance = res
            print("res :", str(i) , " : ", res)
            print("tokenlist :", str(i) , " : ", tokenlist[i].obj.token_property.distance)