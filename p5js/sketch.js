let exampleshader;

function preload() {
  exampleshader = loadShader("example.vert", "example.frag");
}

function setup() {
  createCanvas(600, 600, WEBGL);
  shader(exampleshader);
  noStroke();
}

function draw() {
  clear();
  background(100, 100, 100);
  ellipse(0, 0, width, height,200);
}
