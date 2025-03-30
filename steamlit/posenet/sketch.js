let capture; // Video capture
let poseNet; // PoseNet model
let poses = []; // Array to hold the pose data

function setup() {
  createCanvas(800, 500); // Creates an 800x500 pixel canvas
  capture = createCapture(VIDEO); // Starts capturing video from the webcam
  capture.size(800, 500); // Sets the capture size to match the canvas
  capture.hide(); // Hides the default capture element

  // Load the PoseNet model
  poseNet = ml5.poseNet(capture, modelLoaded);

  // Listen for new pose data and store it in the 'poses' array
  poseNet.on("pose", (results) => {
    poses = results;
  });
}

function modelLoaded() {
  console.log("PoseNet model loaded!");
}

function draw() {
  background(200); // Sets the background color

  // Display the video feed on the canvas
  image(capture, 0, 0, width, height);

  // Draw the pose keypoints and skeleton
  drawKeypoints();
  drawSkeleton();
}

// A function to draw keypoints
function drawKeypoints() {
  for (let i = 0; i < poses.length; i++) {
    let pose = poses[i].pose;
    for (let j = 0; j < pose.keypoints.length; j++) {
      let keypoint = pose.keypoints[j];
      if (keypoint.score > 0.3) { // Only draw keypoints with confidence > 0.2
        fill(255, 0, 0);
        noStroke();
        ellipse(keypoint.position.x, keypoint.position.y, 10, 10);
      }
    }
  }
}

// A function to draw the skeleton
function drawSkeleton() {
  for (let i = 0; i < poses.length; i++) {
    let skeleton = poses[i].skeleton;
    for (let j = 0; j < skeleton.length; j++) {
      let partA = skeleton[j][0];
      let partB = skeleton[j][1];
      stroke(255, 0, 0);
      line(partA.position.x, partA.position.y, partB.position.x, partB.position.y);
    }
  }
}
