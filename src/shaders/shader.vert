#version 330 core

layout (location = 0) in vec4 vertexData;

uniform mat4 model;
uniform mat4 projection;

void main()
{
	gl_Position = projection * model * vec4(vertexData.xy, 0.0, 1.0);
}
