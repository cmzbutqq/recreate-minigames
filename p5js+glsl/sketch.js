let exampleshader;

function preload() {
  exampleshader = loadShader("example.vert", "example.frag");
  bg = loadImage("bg.jpg");
}

function setup() {
  createCanvas(600, 600, WEBGL);
  shader(exampleshader);

  const num_circles = 100;
  const circles = [];
  for (let i = 0; i < num_circles; i++) {
    circles.push(random(), random(), random(0.01, 0.05));
  }

  exampleshader.setUniform("circles", circles);
  noStroke();
}

function draw() {
  exampleshader.setUniform("millis", millis());
  rect(0, 0, width, height);
}
