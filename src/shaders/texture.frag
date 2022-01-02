#version 450 core

in vec2 textureCoords;
out vec4 outColor;

uniform sampler2D texture0;

void main()
{
	outColor = texture(texture0, textureCoords);
}
