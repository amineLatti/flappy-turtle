import os
import sys
import random
import webbrowser
import turtle

# --- Préparation du dossier de travail ---
os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

# --- Setup écran ---
win = turtle.Screen()
win.title("Flappy Turtle - Pollution Edition")
win.setup(width=500, height=500)
win.bgpic("fond.gif")
win.tracer(0)

# 1) Masquer le curseur système (Tkinter)
canvas = win.getcanvas()
root   = canvas.winfo_toplevel()
root.config(cursor="none")

# 2) Empêcher tout dessin parasite du "singleton turtle"
_default = turtle.getturtle()
_default.hideturtle()
_default.penup()

# --- Enregistrement des formes GIF ---
for fname in [
    "fond.gif", "flappyturtle.gif", "tortue.gif", "score.gif",
    "canette.gif", "sac.gif", "paille.gif",
    "game.gif", "try.gif", "info.gif"
]:
    try:
        turtle.register_shape(fname)
    except turtle.TurtleGraphicsError:
        print(f"⚠️ Impossible de charger {fname}")

# --- Objets globaux ---
player      = turtle.Turtle()
player.penup()
player.hideturtle()

obstacles   = []
score       = 0
game_running= False

score_image   = turtle.Turtle()
score_turtle  = turtle.Turtle()
message_turtle= turtle.Turtle()

# Images persistantes du game over
game_over_img = None
try_btn       = None
info_btn      = None

# --- Initialisation des tortues de score et de message ---
for t in (score_image, score_turtle, message_turtle):
    t.penup()
    t.hideturtle()

score_image.shape("score.gif")
score_image.goto(-160, 200)

score_turtle.color("#dfbb12")
score_turtle.goto(-70, 202)
# NB : on NE fait PAS score_turtle.showturtle()

# --- Mouvement & collisions ---
speed = 20
obs_min, obs_max = 4, 9
move_x = move_y = 0

def reset_game():
    global score, obstacles, move_x, move_y, game_running
    score = 0
    move_x = move_y = 0
    game_running = True

    player.shape("tortue.gif")
    player.goto(-150, 0)
    player.showturtle()

    for o in obstacles:
        o.hideturtle()
        o.clear()
    obstacles.clear()

    score_image.showturtle()
    update_score()
    message_turtle.clear()

def update_score():
    score_turtle.clear()
    score_turtle.write(f"{score}", align="left", font=("Arial", 16, "bold"))
    # pas de showturtle()

def create_obstacle():
    d = turtle.Turtle()
    d.penup()
    shape = random.choice(["canette.gif", "sac.gif", "paille.gif"])
    d.shape(shape)
    d.goto(250, random.randint(-200, 200))
    d.speed_x = random.uniform(obs_min, obs_max) + score * 0.05
    obstacles.append(d)

def move_obstacles():
    global score
    for d in obstacles[:]:
        d.setx(d.xcor() - d.speed_x)
        if d.xcor() < -270:
            d.hideturtle()
            d.clear()
            obstacles.remove(d)
            score += 1
            update_score()

def shake(t):
    for _ in range(3):
        t.setx(t.xcor()+4); t.setx(t.xcor()-4)
        t.sety(t.ycor()+4); t.sety(t.ycor()-4)

def check_collision():
    for d in obstacles:
        if player.distance(d) < 30:
            shake(player)
            shake(d)
            return True
    x, y = player.position()
    return not(-240 < x < 240 and -240 < y < 240)

# --- Écran de démarrage ---
def start_screen():
    global logo_turtle
    player.hideturtle()
    message_turtle.clear()
    score_image.hideturtle()
    score_turtle.clear()

    logo_turtle = turtle.Turtle()
    logo_turtle.penup()
    logo_turtle.hideturtle()
    logo_turtle.shape("flappyturtle.gif")
    logo_turtle.goto(0, 60)
    logo_turtle.showturtle()

    message_turtle.color("white")
    message_turtle.goto(0, -20)
    message_turtle.write("START", align="center", font=("Arial", 24, "bold"))

    win.update()

    def on_start(x, y):
        message_turtle.clear()
        logo_turtle.hideturtle()
        reset_game()
        win.ontimer(game_loop, 20)
        win.onclick(None)
    win.onclick(on_start)

# --- Fonction Game Over ---
def game_over():
    global game_running, game_over_img, try_btn, info_btn
    game_running = False

    # cache tout
    player.hideturtle()
    for o in obstacles:
        o.hideturtle(); o.clear()
    obstacles.clear()
    score_image.hideturtle()
    score_turtle.clear()
    message_turtle.clear()

    # Game Over image
    game_over_img = turtle.Turtle()
    game_over_img.penup()
    game_over_img.shape("game.gif")
    game_over_img.goto(0, 120)
    game_over_img.showturtle()

    # Score texte
    message_turtle.goto(0, 70)
    message_turtle.color("white")
    #message_turtle.write(f"Déchets évités : {score}", align="center",
    #                     font=("Arial", 18, "bold"))

    # Bouton Try Again
    try_btn = turtle.Turtle()
    try_btn.penup()
    try_btn.shape("try.gif")
    try_btn.goto(0, -20)
    try_btn.showturtle()

    # Bouton En savoir plus
    info_btn = turtle.Turtle()
    info_btn.penup()
    info_btn.shape("info.gif")
    info_btn.goto(0, -80)
    info_btn.showturtle()

    win.update()

    def on_click(x, y):
        if try_btn.distance(x, y) < 50:
            game_over_img.hideturtle()
            try_btn.hideturtle()
            info_btn.hideturtle()
            message_turtle.clear()
            reset_game()
            win.ontimer(game_loop, 20)
        elif info_btn.distance(x, y) < 50:
            webbrowser.open("https://www.un.org/fr/observances/oceans-day")
    win.onclick(on_click)

# --- Victoire (100 déchets évités) ---
def show_final_block():
    global game_running
    game_running = False
    player.hideturtle()
    for o in obstacles:
        o.hideturtle(); o.clear()
    obstacles.clear()
    message_turtle.clear()

    wall = []
    for x in range(-240, 241, 40):
        b = turtle.Turtle(); b.penup()
        b.shape("square"); b.color("red")
        b.shapesize(stretch_wid=2, stretch_len=2)
        b.goto(x, 0); wall.append(b)

    message_turtle.goto(0, 80)
    message_turtle.write("🌊 Pollution massive ! 🌊", align="center", font=("Arial", 24, "bold"))
    message_turtle.goto(0, 40)
    message_turtle.write(f"Tu as évité {score} déchets !", align="center", font=("Arial", 18, "normal"))

    # Bouton Try Again
    r = turtle.Turtle(); r.penup()
    r.shape("try.gif"); r.goto(0, 0); r.showturtle()
    # Bouton Info
    i = turtle.Turtle(); i.penup()
    i.shape("info.gif"); i.goto(0, -80); i.showturtle()

    win.update()

    def on_click2(x, y):
        if r.distance(x, y) < 50:
            for b in wall: b.hideturtle(); b.clear()
            r.hideturtle(); i.hideturtle()
            message_turtle.clear()
            reset_game()
            win.ontimer(game_loop, 20)
        elif i.distance(x, y) < 50:
            webbrowser.open("https://www.un.org/fr/observances/oceans-day")
    win.onclick(on_click2)

# --- Contrôles clavier ---
def go_left():   global move_x; move_x = -speed
def go_right():  global move_x; move_x =  speed
def stop_x():    global move_x; move_x = 0
def go_up():     global move_y; move_y =  speed
def go_down():   global move_y; move_y = -speed
def stop_y():    global move_y; move_y = 0

win.listen()
win.onkeypress(go_left, "Left");    win.onkeyrelease(stop_x, "Left")
win.onkeypress(go_right, "Right");  win.onkeyrelease(stop_x, "Right")
win.onkeypress(go_up, "Up");        win.onkeyrelease(stop_y, "Up")
win.onkeypress(go_down, "Down");    win.onkeyrelease(stop_y, "Down")

# --- Boucle principale ---
def game_loop():
    if not game_running:
        return
    win.update()
    nx = max(min(player.xcor() + move_x, 240), -240)
    ny = max(min(player.ycor() + move_y, 240), -240)
    player.goto(nx, ny)
    move_obstacles()
    if len(obstacles) < min(3 + score // 4, 10):
        create_obstacle()
    if score >= 100:
        show_final_block()
        return
    if check_collision():
        game_over()
        return
    win.ontimer(game_loop, 16)

# --- Lancement ---
start_screen()
win.mainloop()
