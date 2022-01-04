#version 450 core

in vec2 textureCoords;
out vec4 outColour;

uniform sampler2D texture0;

void main()
{
	outColour = texture(texture0, textureCoords);
}
