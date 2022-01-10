#type compute
#version 450 core

#define NEAR_CLIP 0.1
#define FAR_CLIP 1000.0
#define EPSILON 0.00001

struct Camera
{
    vec3 position;
    vec3 direction;
    vec3 up;
    vec3 right;
    float tanFovY;
    float tanFovX;
};

struct Light
{
    vec3 position;
    vec3 colour;
    vec3 attenuation;
    uint type;
};

struct Ray
{
    vec3 origin;
    vec3 direction;
};

struct Object
{
    vec3 position;
    int type;
    vec4 colour;

    vec4 data1;
    vec4 data2;
    vec4 data3;
};

layout(std430) buffer ObjectBuffer
{
    Object objects[];
};

layout(std430) buffer LightBuffer
{
    Light lights[];
};

uniform Camera camera;
uniform uint width;
uniform uint height;
uniform uint numberOfObjects;
uniform uint numberOfLights;
uniform uint reflectionDepth;

layout (rgba8) uniform image2D fullscreenQuad;

float sphere_intersection(Ray ray, int index)
{
    vec3 position = objects[index].position;
    float radius = objects[index].data1.x;

    vec3 oc = ray.origin - position;
    float a = dot(ray.direction, ray.direction);
    float b = 2.0 * dot(oc, ray.direction);
    float c = dot(oc, oc) - pow(radius, 2.0);
    float discriminant = pow(b, 2.0) - 4 * a * c;

    if (discriminant < 0.0)
    {
        return FAR_CLIP;
    }
    else
    {
        return (-b - sqrt(discriminant)) / (2.0 * a);
    }
}

float plane_intersection(Ray ray, int index)
{
    vec3 normal = objects[index].data1.xyz;
    float denominator = dot(normal, ray.direction);

    if (abs(denominator) >= EPSILON)
    {
        vec3 position = objects[index].position;
        vec2 size = objects[index].data2.xy;

        float t = dot(normal, objects[index].position - ray.origin) / denominator;
        vec3 intersectionPoint = ray.origin + ray.direction * t;

        vec3 p1 = vec3(0.0, 0.0, -EPSILON) + position;
        vec3 p2 = vec3(EPSILON, 0.0, -EPSILON) + position;
        vec3 p3 = vec3(0.0, 0.0, 0.0) + position;

        vec3 p2p1 = p2 - p1;
        vec3 p1p3 = p1 - p3;
        float normp2p1 = sqrt(pow(p2p1.x, 2.0) + pow(p2p1.y, 2.0) + pow(p2p1.z, 2.0));
        float normp1p3 = sqrt(pow(p1p3.x, 2.0) + pow(p1p3.y, 2.0) + pow(p1p3.z, 2.0));

        float X = dot(intersectionPoint - p1, p2p1) / normp2p1;
        float Y = dot(intersectionPoint - p1, p1p3) / normp1p3;

        if (X >= -size.x / 2.0 && X <= size.x / 2.0 && Y >= -size.y / 2.0 && Y <= size.y / 2.0)
            return t;
    }

    return FAR_CLIP;
}

float triangle_intersection(Ray ray, int index)
{
    vec3 position = objects[index].position;
    vec3 A = objects[index].data1.xyz + position;
    vec3 B = objects[index].data2.xyz + position;
    vec3 C = objects[index].data3.xyz + position;

    vec3 AB = B - A;
    vec3 AC = C - A;
    mat3 mat = mat3(AB, AC, -1.0f * ray.direction);
    float det = determinant(mat);

    if (det == 0.0)
    {
        return FAR_CLIP;
    }
    else
    {
        vec3 oA = ray.origin - A;

        mat3 Di = inverse(mat);
        vec3 solution = Di * oA;

        if (solution.x >= -EPSILON && solution.x <= 1.0 + EPSILON)
        {
            if (solution.y >= -EPSILON && solution.y <= 1.0 + EPSILON)
            {
                if (solution.x + solution.y <= 1.0 + EPSILON)
                {
                    return solution.z;
                }
            }
        }
        return FAR_CLIP;
    }
}

Ray initialize_ray(uint x, uint y)
{
    float halfWidth = float(width) / 2.0;
    float halfHeight = float(height) / 2.0;

    float a = camera.tanFovX * ((float(x) - halfWidth + 0.5) / halfWidth);
    float b = camera.tanFovY * ((halfHeight - float(y) - 0.5) / halfHeight);

    vec3 direction = normalize(a * camera.right - b * camera.up + camera.direction);

    return Ray(camera.position, direction);
}

Ray compute_reflection_ray(Ray ray, float t, int index)
{
    vec3 N = vec3(0.0);
    vec3 intersectionPoint = ray.origin + ray.direction * t;

    switch (objects[index].type)
    {
    case 1:
        vec3 position = objects[index].position;
        N = normalize(intersectionPoint - position);
        break;

    case 2:
        vec3 normal = objects[index].data1.xyz;
        N = normalize(normal);
        break;

    case 3:
        vec3 A = objects[index].data1.xyz;
        vec3 B = objects[index].data2.xyz;
        vec3 C = objects[index].data3.xyz;
        N = normalize(cross(B - A, C - A));
        break;
    }

    vec3 reflectedDirection = normalize(ray.direction - 2 * dot(ray.direction, N) * N);

    return Ray(intersectionPoint + reflectedDirection * 0.01, reflectedDirection);
}

vec4 compute_colour(Ray ray, float t, int index)
{
    vec4 resultColour = vec4(0.0);
    vec3 N = vec3(0.0);
    vec3 intersectionPoint = ray.origin + t * ray.direction;

    switch (objects[index].type)
    {
    case 1:
        vec3 position = objects[index].position;
        N = normalize(intersectionPoint - position);
        break;

    case 2:
        vec3 normal = objects[index].data1.xyz;
        N = normalize(normal);
        if (dot(N, camera.position - intersectionPoint) < 0.0)
        {
            N = -N;
        }
        break;

    case 3:
        vec3 A = objects[index].data1.xyz;
        vec3 B = objects[index].data2.xyz;
        vec3 C = objects[index].data3.xyz;
        N = normalize(cross(B - A, C - A));
        break;
    }

    intersectionPoint = intersectionPoint + N * 0.01;

    for (int i = 0; i < numberOfLights; i++)
    {
        vec3 L = vec3(0.0);
        switch (lights[i].type)
        {
        case 1:
            L = normalize(lights[i].position - intersectionPoint);
            break;

        case 2:
            L = normalize(-lights[i].position);
            break;
        }

        Ray shadowRay = Ray(intersectionPoint, L);
        bool inShadow = false;
        for (int j = 0; j < numberOfObjects; j++) 
        {
            float temp = FAR_CLIP;
        
            switch (objects[j].type) 
            {
            case 1:
                temp = sphere_intersection(shadowRay, j);
                break;
        
            case 2:
                temp = plane_intersection(shadowRay, j);
                break;
        
            case 3:
                temp = triangle_intersection(shadowRay, j);
                break;
            }
        
            switch (lights[i].type)
            {
            case 1:
                if (temp < FAR_CLIP && temp >= NEAR_CLIP && temp < length(intersectionPoint - lights[i].position))
                {
                    inShadow = true;
                }
                break;
        
            case 2:
                if (temp < FAR_CLIP && temp >= NEAR_CLIP) 
                {
                    inShadow = true;
                }
                break;
            }

            if (inShadow)
                break;
        }
        
        if (!inShadow)
        {
            vec3 H = normalize(L + normalize(camera.position - intersectionPoint));

            if (dot(N, L) > 0.0)
            {
                float distanceToIntersectionPoint = length(lights[i].position - intersectionPoint);
                vec3 attCoef = lights[i].colour /
                    (lights[i].attenuation.x +
                        lights[i].attenuation.y * distanceToIntersectionPoint +
                        lights[i].attenuation.z * pow(distanceToIntersectionPoint, 2.0) * 0.01);

                vec3 phong = vec3(0.5, 0.5, 0.5) * max(dot(N, L), 0.0) +
                    vec3(0.5, 0.5, 0.5) * pow(max(dot(N, H), 0.0), 256.0);
                resultColour += vec4(attCoef * phong, 1.0);
            }
        }
    }

    return resultColour * objects[index].colour;
}

layout(local_size_x = 16, local_size_y = 16, local_size_z = 1) in;
void main()
{
    uint x = gl_GlobalInvocationID.x;
    uint y = gl_GlobalInvocationID.y;

    if (x < width && y < height)
    {
        vec4 colour = vec4(0.0);
        Ray ray = initialize_ray(x, y);
        
        for (int depth = 0; depth < reflectionDepth; depth++)
        {
            int index = -1;
            float distance = FAR_CLIP;
        
            for (int i = 0; i < numberOfObjects; i++)
            {
                float tempDistance = 0.0;
        
                switch (objects[i].type)
                {
                case 1:
                    tempDistance = sphere_intersection(ray, i);
                    break;
        
                case 2:
                    tempDistance = plane_intersection(ray, i);
                    break;
        
                case 3:
                    tempDistance = triangle_intersection(ray, i);
                    break;
                }
        
                if (tempDistance >= NEAR_CLIP && tempDistance < distance)
                {
                    distance = tempDistance;
                    index = i;
                }
            }
        
            if (index != -1)
            {
                colour += compute_colour(ray, distance, index);
                ray = compute_reflection_ray(ray, distance, index);
            }
        }

        imageStore(fullscreenQuad, ivec2(x, y), colour);
    }
}
