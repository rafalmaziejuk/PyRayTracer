from graphics.meshes.mesh import Mesh
from graphics.vertex_buffer import Types
from glm import translate, rotate, scale, radians, mat4, vec3

class Grid(Mesh):
    def __init__(self, position, slices, size, rotation=0.0, rotationVector=(1.0, 1.0, 1.0)):
        vertices = []
        indices = []

        for j in range (slices + 1):
            for i in range (slices + 1):
                x = i / slices - 0.5
                y = 0.0
                z = j / slices - 0.5
                vertices.append(x)
                vertices.append(y)
                vertices.append(z)

        for j in range (slices):
            for i in range (slices):
                row1 =  j      * (slices + 1)
                row2 = (j + 1) * (slices + 1)
                indices.append(row1 + i)
                indices.append(row1 + i + 1)
                indices.append(row1 + i + 1)
                indices.append(row2 + i + 1)
                indices.append(row2 + i + 1)
                indices.append(row2 + i)
                indices.append(row2 + i)
                indices.append(row1 + i)
        
        super().__init__(position, vertices, indices, [Types.FLOAT3])

        self.slices = slices
        self.size = size
        self.rotation = rotation
        self.rotationVector = rotationVector
        self.modelMatrix = translate(mat4(1.0), vec3(self.position)) * \
                           rotate(mat4(1.0), radians(self.rotation), vec3(self.rotationVector)) * \
                           scale(mat4(1.0), vec3(self.size))

