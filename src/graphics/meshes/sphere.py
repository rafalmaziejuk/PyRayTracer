from graphics.meshes.mesh import Mesh
from graphics.vertex_buffer import Types
from glm import translate, normalize, pi, cos, sin, mat4, vec3

class Sphere(Mesh):
    def __init__(self, position, radius, sectors, stacks):
        vertices = []
        indices = []

        for i in range(sectors + 1):
            V = i / stacks
            phi = V * pi()
        
            for j in range(sectors + 1):
                U = j / sectors;
                theta = U * pi() * 2;

                vector = vec3(cos(theta) * sin(phi) * radius,
                              cos(phi) * radius,
                              sin(theta) * sin(phi) * radius)
                vertices.append(vector.x)
                vertices.append(vector.y)
                vertices.append(vector.z)

                vertices.append(j / sectors)
                vertices.append(i / stacks)
                
                normalizedVector = normalize(vector)
                vertices.append(normalizedVector.x)
                vertices.append(normalizedVector.y)
                vertices.append(normalizedVector.z)
                
        for i in range(sectors * stacks + sectors):
            indices.append(i)
            indices.append(i + sectors + 1)
            indices.append(i + sectors)
        
            indices.append(i + sectors + 1)
            indices.append(i)
            indices.append(i + 1)

        self.radius = radius
        self.sectors = sectors
        self.stacks = stacks
            
        super().__init__(position, vertices, indices, [Types.FLOAT3, Types.FLOAT2, Types.FLOAT3])
        self.modelMatrix = translate(mat4(1.0), vec3(self.position))
