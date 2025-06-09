let imgFond, imgTortue, imgCanette, imgSac, imgPaille;
let imgGameOver, imgTry, imgInfo;
let player, obstacles = [];
let score = 0, gameOver = false;

function preload() {
  imgFond   = loadImage('assets/fond.png');
  imgTortue = loadImage('assets/tortue.png');
  imgCanette= loadImage('assets/canette.png');
  imgSac    = loadImage('assets/sac.png');
  imgPaille = loadImage('assets/paille.png');
  imgGameOver = loadImage('assets/game.png');
  imgTry      = loadImage('assets/try.png');
  imgInfo     = loadImage('assets/info.png');
}

function setup() {
  createCanvas(500,500);
  resetGame();
}

function resetGame() {
  obstacles = [];
  score = 0;
  gameOver = false;
  player = { x:50, y: height/2, w:50, h:50, vy:0 };
}

function draw() {
  background(imgFond);
  if (gameOver) {
    showGameOver();
    return;
  }
  // Gravité
  player.vy += 0.6;
  player.y += player.vy;
  image(imgTortue, player.x, player.y, player.w, player.h);

  // Gestion obstacles
  if (frameCount % 60 === 0) {
    let y = random(50, height-50);
    let type = random([imgCanette,imgSac,imgPaille]);
    obstacles.push({ x: width, y, img: type, w:40, h:40 });
  }
  for (let o of obstacles) {
    o.x -= 4 + score*0.02;
    image(o.img, o.x, o.y, o.w, o.h);
    if (o.x + o.w < 0) {
      score++;
      obstacles.shift();
    }
    // Collision simple AABB
    if (!gameOver &&
        o.x < player.x+player.w && o.x+o.w > player.x &&
        o.y < player.y+player.h && o.y+o.h > player.y) {
      gameOver = true;
    }
  }
  // Score
  fill('#dfbb12'); textSize(24);
  text(`Score: ${score}`, 10, 30);
}

function keyPressed() {
  if (!gameOver && key === ' ') {
    player.vy = -10;
  } else if (gameOver && key === 'R') {
    resetGame();
  }
}

function showGameOver() {
  image(imgGameOver, width/2-150, 50, 300, 100);
  fill('white'); textSize(32); textAlign(CENTER);
  text(`Déchets évités : ${score}`, width/2, 200);
  image(imgTry, width/2-75, 250, 150, 50);
  image(imgInfo, width/2-75, 320, 150, 50);
  cursor(HAND);
}

function mousePressed() {
  if (!gameOver) return;
  // Try Again
  if (mouseX > width/2-75 && mouseX < width/2+75
      && mouseY > 250 && mouseY < 300) {
    resetGame();
    cursor(ARROW);
  }
  // En savoir plus
  if (mouseX > width/2-75 && mouseX < width/2+75
      && mouseY > 320 && mouseY < 370) {
    window.open('https://www.un.org/fr/observances/oceans-day','_blank');
  }
}
