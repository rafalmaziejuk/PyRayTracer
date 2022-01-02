from graphics.meshes.mesh import Mesh
from graphics.vertex_buffer import Types
from glm import translate, scale, mat4, vec3

VERTICES = [
    # origin
    0.0, 0.0, 0.0,
    
    # x        
    1.0, 0.0, 0.0,
    
    # y 
    0.0, 1.0, 0.0,
    
    # z        
    0.0, 0.0, 1.0
    ]

INDICES = [
    0, 1,
    0, 2,
    0, 3
    ]

class OriginAxis(Mesh):
    def __init__(self):
        super().__init__((0.0, 0.0, 0.0), VERTICES, INDICES, [Types.FLOAT3])

        self.modelMatrix = translate(mat4(1.0), vec3(0.0, 0.0, 0.0)) * \
                           scale(mat4(1.0), vec3(3.0, 3.0, 3.0))
