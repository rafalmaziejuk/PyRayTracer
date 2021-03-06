#type vertex
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

#type fragment
#version 450 core

struct Light {
    vec3 position;  
    vec3 direction;
    vec3 colour;
    float cutOff;
    float outerCutOff;
  
    vec3 ambient;
    vec3 diffuse;
    vec3 specular;
};

in vec3 fragmentPosition;
in vec3 normal;

out vec4 outColour;

uniform vec3 uMeshColour;
uniform vec3 uCameraPosition;
uniform Light uLight;

void main()
{
    vec3 viewDirection = normalize(uCameraPosition - fragmentPosition);
    vec3 lightDirection = normalize(uLight.position - fragmentPosition);
    vec3 reflectDirection = reflect(-lightDirection, normal);
    
    vec3 ambient = uLight.ambient;
    vec3 diffuse = uLight.diffuse * max(dot(lightDirection, normal), 0.0);
    vec3 specular = uLight.specular * pow(max(dot(viewDirection, reflectDirection), 0.0), 8.0);

    // spotlight (soft edges)
    float theta = dot(lightDirection, normalize(-uLight.direction)); 
    float epsilon = (uLight.cutOff - uLight.outerCutOff);
    float intensity = smoothstep(0.0, 1.0, (theta - uLight.outerCutOff) / epsilon);
    diffuse  *= intensity;
    specular *= intensity;

    vec3 result = (ambient + diffuse + specular) * uMeshColour;
    outColour = vec4(result, 1.0);
}
