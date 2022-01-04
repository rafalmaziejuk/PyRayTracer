from glm import cos, radians, vec3

class Light():
    def __init__(self, position, direction, colour, radius):
        self.position = position
        self.direction = direction
        self.colour = colour
        self.radius = radius

    def set_light_uniform(self, shader):
        shader.set_vec3f('uLight.position', vec3(self.position))
        shader.set_vec3f('uLight.direction', vec3(self.direction))
        shader.set_vec3f('uLight.colour', vec3(self.colour))
        shader.set_float('uLight.cutOff', cos(radians(self.radius)))
        shader.set_float('uLight.outerCutOff', cos(radians(self.radius + 5.0)))

        shader.set_vec3f('uLight.ambient', vec3(0.1, 0.1, 0.1))
        shader.set_vec3f('uLight.diffuse', vec3(0.8, 0.8, 0.8))
        shader.set_vec3f('uLight.specular', vec3(1.0, 1.0, 1.0))
