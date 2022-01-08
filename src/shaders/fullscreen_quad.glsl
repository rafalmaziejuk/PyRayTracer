#type vertex
#version 450 core

layout (location = 0) in vec3 inPosition;
layout (location = 1) in vec2 inTextureCoords;

out vec2 textureCoords;

void main()
{
	textureCoords = inTextureCoords;
	gl_Position = vec4(inPosition, 1.0);
}

#type fragment
#version 450 core

in vec2 textureCoords;
out vec4 outColour;

uniform sampler2D texture0;

void main()
{
	outColour = texture(texture0, textureCoords);
}
