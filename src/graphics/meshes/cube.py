from graphics.meshes.mesh import Mesh
from graphics.vertex_buffer import Types
from glm import translate, rotate, scale, radians, mat4, vec3

VERTICES = [
         #position     #texCoords       #normals
    #back
    -0.5, -0.5, -0.5,   0.0, 0.0,    0.0,  0.0, -1.0, #0
     0.5, -0.5, -0.5,   1.0, 0.0,    0.0,  0.0, -1.0, #1
     0.5,  0.5, -0.5,   1.0, 1.0,    0.0,  0.0, -1.0, #2
    -0.5,  0.5, -0.5,   0.0, 1.0,    0.0,  0.0, -1.0, #3
                                      
    # front                           
    -0.5, -0.5,  0.5,   0.0, 0.0,    0.0,  0.0,  1.0, #4
     0.5, -0.5,  0.5,   1.0, 0.0,    0.0,  0.0,  1.0, #5
     0.5,  0.5,  0.5,   1.0, 1.0,    0.0,  0.0,  1.0, #6
    -0.5,  0.5,  0.5,   0.0, 1.0,    0.0,  0.0,  1.0, #7
                                                
    # left                                      
    -0.5,  0.5,  0.5,   1.0, 0.0,   -1.0, 0.0,   0.0, #8
    -0.5,  0.5, -0.5,   1.0, 1.0,   -1.0, 0.0,   0.0, #9
    -0.5, -0.5, -0.5,   0.0, 1.0,   -1.0, 0.0,   0.0, #10
    -0.5, -0.5,  0.5,   0.0, 0.0,   -1.0, 0.0,   0.0, #11
                                                
    # right                                     
     0.5,  0.5,  0.5,   1.0, 0.0,    1.0,  0.0,  0.0, #12
     0.5,  0.5, -0.5,   1.0, 1.0,    1.0,  0.0,  0.0, #13
     0.5, -0.5, -0.5,   0.0, 1.0,    1.0,  0.0,  0.0, #14
     0.5, -0.5,  0.5,   0.0, 0.0,    1.0,  0.0,  0.0, #15
                                                 
    # bottom                                     
    -0.5, -0.5, -0.5,   0.0, 1.0,    0.0, -1.0,  0.0, #16
     0.5, -0.5, -0.5,   1.0, 1.0,    0.0, -1.0,  0.0, #17
     0.5, -0.5,  0.5,   1.0, 0.0,    0.0, -1.0,  0.0, #18
    -0.5, -0.5,  0.5,   0.0, 0.0,    0.0, -1.0,  0.0, #19
                                                 
    # top                                        
    -0.5,  0.5, -0.5,   0.0, 1.0,    0.0,  1.0,  0.0, #20
     0.5,  0.5, -0.5,   1.0, 1.0,    0.0,  1.0,  0.0, #21
     0.5,  0.5,  0.5,   1.0, 0.0,    0.0,  1.0,  0.0, #22
    -0.5,  0.5,  0.5,   0.0, 0.0,    0.0,  1.0,  0.0  #23
    ]

INDICES = [
    # back
    0,  1,  2,
    2,  3,  0,
    
    # front        
    4,  5,  6, 
    6,  7,  4, 
    
    # left
    8,  9,  10, 
    10, 11, 8,  
    
    # right 
    12, 13, 14,
    14, 15, 12,
    
    # bottom
    16, 17, 18,
    18, 19, 16,
    
    # top
    20, 21, 22,
    22, 23, 20
    ]

class Cube(Mesh):
    def __init__(self, position, size, rotation=0.0, rotationVector=(1.0, 1.0, 1.0)):
        super().__init__(position, VERTICES, INDICES, [Types.FLOAT3, Types.FLOAT2, Types.FLOAT3])
        
        self.size = size
        self.rotation = rotation
        self.rotationVector = rotationVector
        self.modelMatrix = translate(mat4(1.0), vec3(self.position)) * \
                           rotate(mat4(1.0), radians(self.rotation), vec3(self.rotationVector)) * \
                           scale(mat4(1.0), vec3(self.size))
