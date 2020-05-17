#version 120
// Uniform inputs
uniform mat4 p3d_ModelViewProjectionMatrix;
uniform mat4 p3d_ModelViewMatrix;

// Vertex inputs
attribute vec4 p3d_Vertex;
attribute vec2 p3d_MultiTexCoord0;
attribute vec3 p3d_Normal;
attribute vec4 p3d_Color;

// Output to fragment shader
varying vec3 normal;
varying vec2 texcoord;
varying float dist;

void main() {
  vec4 pos = p3d_ModelViewMatrix * p3d_Vertex;
  dist = -pos.z;
  normal = p3d_Normal;
  gl_Position = vec4(p3d_ModelViewProjectionMatrix * p3d_Vertex);
  texcoord = p3d_MultiTexCoord0;
}