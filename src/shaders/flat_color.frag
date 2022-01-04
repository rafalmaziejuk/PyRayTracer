#version 450 core

out vec4 outColour;

uniform vec3 uMeshColour;

void main()
{
    outColour = vec4(uMeshColour, 1.0);
}
