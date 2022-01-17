from enum import IntEnum
from struct import pack
from glm import vec2, vec3, vec4
from sqlite3 import Error, connect

class ObjectTypes(IntEnum):
    SPHERE = 1,
    PLANE = 2,
    TRIANGLE = 3

class LightTypes(IntEnum):
    POINT = 1,
    DIRECTIONAL = 2

class Object():
    def __init__(self, objectType, position, colour, data1, data2, data3):
        position = vec3(position)
        colour = vec4(colour, 1.0)

        self.bytesArray = bytearray()
        self.bytesArray.extend(pack("f", position.x))
        self.bytesArray.extend(pack("f", position.y))
        self.bytesArray.extend(pack("f", position.z))
        self.bytesArray.extend(pack("i", objectType))

        self.bytesArray.extend(pack("f", colour.x))
        self.bytesArray.extend(pack("f", colour.y))
        self.bytesArray.extend(pack("f", colour.z))
        self.bytesArray.extend(pack("f", colour.w))

        self.bytesArray.extend(pack("f", data1.x))
        self.bytesArray.extend(pack("f", data1.y))
        self.bytesArray.extend(pack("f", data1.z))
        self.bytesArray.extend(pack("f", data1.w))

        self.bytesArray.extend(pack("f", data2.x))
        self.bytesArray.extend(pack("f", data2.y))
        self.bytesArray.extend(pack("f", data2.z))
        self.bytesArray.extend(pack("f", data2.w))

        self.bytesArray.extend(pack("f", data3.x))
        self.bytesArray.extend(pack("f", data3.y))
        self.bytesArray.extend(pack("f", data3.z))
        self.bytesArray.extend(pack("f", data3.w))

class Sphere(Object):
    def __init__(self, position, radius, colour=(1.0, 1.0, 1.0)):
        data1 = vec4(radius, vec3(0.0))
        data2 = vec4(0.0)
        data3 = vec4(0.0)

        super().__init__(ObjectTypes.SPHERE, position, colour, data1, data2, data3)

class Plane(Object):
    def __init__(self, position, size, colour=(1.0, 1.0, 1.0)):
        data1 = vec4(vec3(0.0, 1.0, 0.0), 0.0)
        data2 = vec4(vec2(size), vec2(0.0))
        data3 = vec4(0.0)

        super().__init__(ObjectTypes.PLANE, position, colour, data1, data2, data3)

class Triangle(Object):
    def __init__(self, position, size, A, B, C, colour=(1.0, 1.0, 1.0)):
        A = vec3(A) * size
        B = vec3(B) * size
        C = vec3(C) * size

        data1 = vec4(A, 0.0)
        data2 = vec4(B, 0.0)
        data3 = vec4(C, 0.0)

        super().__init__(ObjectTypes.TRIANGLE, position, colour, data1, data2, data3)

class Cube():
    def __init__(self, position, size, colour=(1.0, 1.0, 1.0)):
        self.triangles = [
            # left
            Triangle(position, size, (-0.5, -0.5,  0.5), (-0.5,  0.5, -0.5), (-0.5, -0.5, -0.5), colour),
            Triangle(position, size, (-0.5, -0.5,  0.5), (-0.5,  0.5,  0.5), (-0.5,  0.5, -0.5), colour),
                                                                                               
            #front                                                                             
            Triangle(position, size, (-0.5, -0.5,  0.5), ( 0.5,  0.5,  0.5), (-0.5,  0.5,  0.5), colour),
            Triangle(position, size, (-0.5, -0.5,  0.5), ( 0.5, -0.5,  0.5), ( 0.5,  0.5,  0.5), colour),
                                                                                               
            # back                                                                             
            Triangle(position, size, ( 0.5, -0.5, -0.5), (-0.5, -0.5, -0.5), (-0.5,  0.5, -0.5), colour),
            Triangle(position, size, ( 0.5, -0.5, -0.5), (-0.5,  0.5, -0.5), ( 0.5,  0.5, -0.5), colour),
                                                                                               
            # right                                                                            
            Triangle(position, size, ( 0.5, -0.5,  0.5), ( 0.5, -0.5, -0.5), ( 0.5,  0.5, -0.5), colour),
            Triangle(position, size, ( 0.5,  0.5, -0.5), ( 0.5,  0.5,  0.5), ( 0.5, -0.5,  0.5), colour),
                                                                                               
            # top                                                                              
            Triangle(position, size, ( 0.5,  0.5, -0.5), (-0.5,  0.5, -0.5), (-0.5,  0.5,  0.5), colour),
            Triangle(position, size, ( 0.5,  0.5, -0.5), (-0.5,  0.5,  0.5), ( 0.5,  0.5,  0.5), colour),
                                                                                               
            # bottom                                                                           
            Triangle(position, size, ( 0.5, -0.5, -0.5), (-0.5, -0.5, -0.5), (-0.5, -0.5,  0.5), colour),
            Triangle(position, size, ( 0.5, -0.5, -0.5), (-0.5, -0.5,  0.5), ( 0.5, -0.5,  0.5), colour),
            ]

class Light():
    def __init__(self, position, attenuation, colour, lightType):
        self.position = vec3(position)
        self.attenuation = vec3(attenuation)
        self.colour = vec3(colour)
        self.lightType = lightType
        
        self.bytesArray = bytearray()
        self.bytesArray.extend(pack("f", self.position.x))
        self.bytesArray.extend(pack("f", self.position.y))
        self.bytesArray.extend(pack("f", self.position.z))
        self.bytesArray.extend(pack("f", 0.0)) #padding
        self.bytesArray.extend(pack("f", self.colour.x))
        self.bytesArray.extend(pack("f", self.colour.y))
        self.bytesArray.extend(pack("f", self.colour.z))
        self.bytesArray.extend(pack("f", 0.0)) #padding
        self.bytesArray.extend(pack("f", self.attenuation.x))
        self.bytesArray.extend(pack("f", self.attenuation.y))
        self.bytesArray.extend(pack("f", self.attenuation.z))
        self.bytesArray.extend(pack("i", self.lightType))

QUERY_SPHERE = """
select 	x, y, z, radius, r, g, b
from 	sphere sp 
	 	join scene sc on sp.id_scene = sc.id_scene
        join colour col on sp.id_colour = col.id_colour
where sc.scene_name = ?; 
"""

QUERY_PLANE = """
select 	x, y, z, plane_size_x, plane_size_y, r, g, b
from 	plane pl 
	 	join scene sc on pl.id_scene = sc.id_scene
        join colour col on pl.id_colour = col.id_colour
where sc.scene_name = ?; 
"""

QUERY_CUBE = """
select 	x, y, z, cube_size, r, g, b
from 	cube cu 
	 	join scene sc on cu.id_scene = sc.id_scene
        join colour col on cu.id_colour = col.id_colour
where sc.scene_name = ?; 
"""

QUERY_LIGHT = """
select 	x, y, z, a_x, a_y, a_z, r, g, b, light_type
from 	light li
	 	join scene sc on li.id_scene = sc.id_scene
        join colour col on li.id_colour = col.id_colour
where sc.scene_name = ?; 
"""

class Scene():
    def __init__(self, sceneName):
        connection = self.__connect_to_database('scenes/scenes.db')
        self.cursor = connection.cursor()
        self.sceneName = sceneName
        self.objectsData = bytearray()
        self.objectsCount = 0
        self.lightsData = bytearray()
        self.lightsCount = 0
        
        sphereRows = self.__execute_query(QUERY_SPHERE)
        planeRows = self.__execute_query(QUERY_PLANE)
        cubeRows = self.__execute_query(QUERY_CUBE)
        lightRows = self.__execute_query(QUERY_LIGHT)
        
        for row in sphereRows:
            self.objectsCount += 1
            self.objectsData.extend(self.__parse_sphere(row))

        for row in planeRows:
            self.objectsCount += 1
            self.objectsData.extend(self.__parse_plane(row))

        for row in cubeRows:
            count, data = self.__parse_cube(row)
            self.objectsCount += count
            self.objectsData.extend(data)

        for row in lightRows:
            self.lightsCount += 1
            self.lightsData.extend(self.__parse_light(row))

    def __connect_to_database(self, database):
        connection = None
        try:
            connection = connect(database)
        except Error as e:
            print(e)

        return connection

    def __execute_query(self, query):
        self.cursor.execute(query, (self.sceneName,))
        rows = self.cursor.fetchall()

        return rows

    def __parse_sphere(self, row):
        position = row[0:3]
        radius = row[3]
        colour = row[4:7]

        sphere = Sphere(position, radius, colour)
        return sphere.bytesArray

    def __parse_plane(self, row):
        position = row[0:3]
        size = row[3:5]
        colour = row[5:8]

        plane = Plane(position, size, colour)
        return plane.bytesArray

    def __parse_cube(self, row):
        position = row[0:3]
        size = row[3]
        colour = row[4:7]

        cube = Cube(position, size, colour)
        bytesArray = bytearray()
        for triangle in cube.triangles:
            bytesArray.extend(triangle.bytesArray)

        return len(cube.triangles), bytesArray

    def __parse_light(self, row):
        position = row[0:3]
        attenuation = row[3:6]
        colour = row[6:9]
        lightType = LightTypes.POINT if ''.join(row[9:]) == 'POINT' else LightTypes.DIRECTIONAL

        light = Light(position, attenuation, colour, lightType)
        return light.bytesArray

    def get_objects_data(self):
        return self.objectsCount, self.objectsData

    def get_lights_data(self):
        return self.lightsCount, self.lightsData
