precision mediump float;

varying vec2 pos;

const int num_circles = 100 ;
uniform vec3 circles[num_circles];

uniform float millis;

void main(){ 
    float color=1.;
    for(int i=0;i<num_circles;i++){
        float d = length(pos-circles[i].xy)-circles[i].z;
    d=step(0.,d);
    color *=d;
    }
    gl_FragColor = vec4(color,color,color,1.);
}