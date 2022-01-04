#version 450 core

layout (location = 0) in vec3 inPosition;
layout (location = 1) in vec2 inTextureCoords;
layout (location = 2) in vec3 inNormal;

out vec3 fragmentPosition;
out vec3 normal;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main()
{
	fragmentPosition = vec3(model * vec4(inPosition, 1.0));
	normal = inNormal;

	gl_Position = projection * view * model * vec4(inPosition, 1.0);
}
