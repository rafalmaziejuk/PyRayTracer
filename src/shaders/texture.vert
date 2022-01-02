#version 450 core

layout (location = 0) in vec3 inPosition;
layout (location = 1) in vec2 inTextureCoords;

out vec2 textureCoords;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main()
{
	textureCoords = inTextureCoords;
	gl_Position = projection * view * model * vec4(inPosition, 1.0);
}
