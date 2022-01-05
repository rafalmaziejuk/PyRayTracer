#type vertex
#version 450 core

layout (location = 0) in vec3 inPosition;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main()
{
	gl_Position = projection * view * model * vec4(inPosition, 1.0);
}

#type fragment
#version 450 core

out vec4 outColour;

uniform vec3 uMeshColour;

void main()
{
    outColour = vec4(uMeshColour, 1.0);
}
