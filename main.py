#Game Starting initialisation
from tkinter import *
from tkinter import filedialog
import pygame
import os
from pygame.locals import *
current_path = os.path.dirname(__file__)
saving_path = os.path.join(current_path, 'assets\saves')
timer = pygame.time.Clock()
music_path  = os.path.join(current_path, 'assets\music')
image_path = os.path.join(current_path, 'assets\images') 
chess_path = os.path.join(current_path, 'assets\images\Pieces')
pygame.font.init()
pygame.font.get_fonts()
text_font = pygame.font.SysFont(None , 40)
select_font = pygame.font.SysFont(None , 30)
pygame.init()
fps = 30
counter = 0
############################################################################################################
#Values
toplf = (114, 58)
hori_d = 86
Vert_d = 86
running = True
data = []
boardpos = pygame.Vector2(-1, -1)
L_click = 0
pid = -1
N = 0
rdeadcount = 0
bdeadcount = 0
############################################################################################################
#screen and background settings 
WIDTH = 1200
HEIGHT = 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
stratup = pygame.image.load(os.path.join(image_path, 'Startup_Screen.png')).convert()
startup = pygame.transform.scale(stratup, (WIDTH, HEIGHT)).convert()
background = pygame.image.load(os.path.join(image_path, 'Xiangqi_Background.png')).convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT)).convert()
WinR = pygame.image.load(os.path.join(image_path, 'Win_Red.png')).convert()
WinR = pygame.transform.scale(WinR, (WIDTH, HEIGHT)).convert()
WinB = pygame.image.load(os.path.join(image_path, 'Win_Black.png')).convert()
WinB = pygame.transform.scale(WinB, (WIDTH, HEIGHT)).convert()
caption = '2025 ICT SBA Project - Chinese Chess - 5B28 Wong King Hang'
winning_sound = pygame.mixer.Sound(os.path.join(music_path, 'Winning.mp3'))
music = pygame.mixer.music.load(os.path.join(music_path, 'Normal_BGM.mp3'))
pygame.display.set_icon(pygame.image.load(os.path.join(image_path, 'icon.png')).convert_alpha())
#Button initialisation
start_img = pygame.image.load(os.path.join(image_path, 'start.png')).convert_alpha()
quit_img = pygame.image.load(os.path.join(image_path, 'quit.png')).convert_alpha()
rs_img = pygame.image.load(os.path.join(image_path, 'Restart.png')).convert_alpha()
save_img = pygame.image.load(os.path.join(image_path, 'save.png')).convert_alpha()
load_img = pygame.image.load(os.path.join(image_path, 'load.png')).convert_alpha()
menu_img = pygame.image.load(os.path.join(image_path, 'back-button.png')).convert_alpha()
reverse_img = pygame.image.load(os.path.join(image_path, 'reverse.png')).convert_alpha()
class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale))).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
    
    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action
start_button = Button(240, 500, start_img,0.5)
quit_button = Button(600, 500, quit_img,0.5)
rs_button = Button(240, 500, rs_img,0.5)
save_button = Button(1080,734, save_img,0.2)
load_button = Button(1080,734, load_img,0.2)
menu_button = Button(1080,284, menu_img,0.2)
reverse_button = Button(1080,134, reverse_img,0.2)
#Chess initialisation
class chess():
    def __init__(self, id, x, y, colour, status, type, name, image, scale):
        self.id = id
        self.x = int(x)
        self.y = int(y)
        self.colour = colour
        self.status = status
        self.type = type
        self.name = name
        self.scale = scale
        self.original = image
        self.pg = pygame.image.load(os.path.join(chess_path, image)).convert_alpha()
        self.width = self.pg.get_width()
        self.height = self.pg.get_height()
        self.selected = 0
    def draw(self):
        if self.status == 1:
            if self.selected in (1,2):
                pg = pygame.image.load(os.path.join(chess_path, "a" + self.original)).convert_alpha()
                width = pg.get_width()
                height = pg.get_height()
                self.image = pygame.transform.scale(pg, (int(width * (self.scale+0.001)), int(height * (self.scale+0.001)))).convert_alpha()
                s_width = self.image.get_width()
                s_height = self.image.get_height()
                self.pos = (toplf[0] + hori_d * self.x - s_width // 2, toplf[1] + Vert_d * self.y - s_height // 2)
            else:
                self.image = pygame.transform.scale(self.pg, (int(self.width * self.scale), int(self.height * self.scale))).convert_alpha()
                s_width = self.image.get_width()
                s_height = self.image.get_height()
                self.pos = (toplf[0] + hori_d * self.x - s_width // 2, toplf[1] + Vert_d * self.y - s_height // 2)
        else:
            pg = pygame.image.load(os.path.join(chess_path, self.original)).convert_alpha()
            width = pg.get_width()
            height = pg.get_height()
            self.image = pygame.transform.scale(pg, (int(width * self.scale), int(height * self.scale))).convert_alpha()
            s_width = self.image.get_width()
            s_height = self.image.get_height()
            self.pos = (self.x, self.y)
        screen.blit(self.image, self.pos)

        
        #self.x = (mouse.x + s_width // 2 - toplf[0]) // hori_d
    def rollover(self, mousepos):
        if self.selected != 2:
            if self.pos[0] < mousepos[0] < self.pos[0] + self.image.get_width() and self.pos[1] < mousepos[1] < self.pos[1] + self.image.get_height():
                self.selected = 1
            else:
                self.selected = 0
                
    def select(self, mousepos):
        if self.pos[0] < mousepos[0] < self.pos[0] + self.image.get_width() and self.pos[1] < mousepos[1] < self.pos[1] + self.image.get_height():
            self.selected = 2
        else:
            self.selected = 0
    def move(self, x, y):
        self.x = x
        self.y = y
        if self.selected == 2:
            self.selected = 0
    def eat(self):
        self.status = 0
#Background position
def Background_pos(m_pos):
    global boardpos
    boardpos.x = (m_pos[0] - toplf[0]+ hori_d//2) // hori_d
    boardpos.y = (m_pos[1] - toplf[1]+ Vert_d//2) // Vert_d
    # print(boardpos.x, boardpos.y)
    # if 0 <= boardpos.x <= 8 and 0 <= boardpos.y <= 9:
    #     a = int(toplf[0] + hori_d * boardpos.x )
    #     b = int(toplf[1] + Vert_d * boardpos.y)
    #     pygame.draw.rect(screen,(0,0,0),[a,b,100 ,100], 2)
#checking turn
def Start(Turn):
    return Turn*16
def switch_turn(Turn):
    return 1 - Turn
#checking movement of chess
def count_chess(x,y):
    counter = 0
    if Pieces[pid].x == x:
        if Pieces[pid].y < y:
            for i in range(32):
                if Pieces[i].x == x and Pieces[i].y > Pieces[pid].y and Pieces[i].y < y and Pieces[i].status == 1:
                    counter += 1
        elif Pieces[pid].y > y:
            for i in range(32):
                if Pieces[i].x == x and Pieces[i].y < Pieces[pid].y and Pieces[i].y > y and Pieces[i].status == 1:
                    counter += 1
        return counter
    elif Pieces[pid].y == y :
        if Pieces[pid].x < x:
            for i in range(32):
                if Pieces[i].y == y and Pieces[i].x > Pieces[pid].x and Pieces[i].x < x and Pieces[i].status == 1:
                    counter += 1
        elif Pieces[pid].x > x:
            for i in range(32):
                if Pieces[i].y == y and Pieces[i].x < Pieces[pid].x and Pieces[i].x > x and Pieces[i].status == 1:
                    counter += 1
        return counter
def check_king(x,y):
    if Pieces[pid].colour == 0:
        if 5>= x >= 3 and 2 >= y >= 0:
            if Pieces[pid].x == x and (y == Pieces[pid].y + 1 or y == Pieces[pid].y - 1) :
                return True
            elif Pieces[pid].y == y and (x == Pieces[pid].x + 1 or x == Pieces[pid].x - 1):
                return True
        elif Pieces[pid].x == Pieces[27].x:
            if x == Pieces[27].x :
                if y == Pieces[27].y:
                    if Pieces[pid].y < y:
                        for i in range(32):
                            if Pieces[i].x == x and Pieces[i].y > Pieces[pid].y and Pieces[i].y < y and Pieces[i].status == 1:
                                return False
                    elif Pieces[pid].y > y:
                        for i in range(32):
                            if Pieces[i].x == x and Pieces[i].y < Pieces[pid].y and Pieces[i].y > y and Pieces[i].status == 1:
                                return False
                    return True
                else:
                    return False
            else:
                    return False
    if Pieces[pid].colour == 1:
        if 5>= x >= 3 and 9 >= y >= 7:
            if Pieces[pid].x == x and (y == Pieces[pid].y + 1 or y == Pieces[pid].y - 1) :
                return True
            elif Pieces[pid].y == y and (x == Pieces[pid].x + 1 or x == Pieces[pid].x - 1):
                return True
        elif Pieces[pid].x == Pieces[4].x:
            if x == Pieces[4].x :
                if y == Pieces[4].y:
                    if Pieces[pid].y < y:
                        for i in range(32):
                            if Pieces[i].x == x and Pieces[i].y > Pieces[pid].y and Pieces[i].y < y and Pieces[i].status == 1:
                                return False
                    elif Pieces[pid].y > y:
                        for i in range(32):
                            if Pieces[i].x == x and Pieces[i].y < Pieces[pid].y and Pieces[i].y > y and Pieces[i].status == 1:
                                return False
                    return True
                else:
                    return False
            else:
                    return False

    return False
def check_cars(x,y):
    if Pieces[pid].x == x:
        if Pieces[pid].y < y:
            for i in range(32):
                if Pieces[i].x == x and Pieces[i].y > Pieces[pid].y and Pieces[i].y < y and Pieces[i].status == 1:
                    return False
        elif Pieces[pid].y > y:
            for i in range(32):
                if Pieces[i].x == x and Pieces[i].y < Pieces[pid].y and Pieces[i].y > y and Pieces[i].status == 1:
                    return False
        else:
            return True
    elif Pieces[pid].y == y:
        if Pieces[pid].x < x:
            for i in range(32):
                if Pieces[i].y == y and Pieces[i].x > Pieces[pid].x and Pieces[i].x < x and Pieces[i].status == 1:
                    return False
        elif Pieces[pid].x > x:
            for i in range(32):
                if Pieces[i].y == y and Pieces[i].x < Pieces[pid].x and Pieces[i].x > x and Pieces[i].status == 1:
                    return False
        else:
            return True
    else:
        return False
def check_horse(x,y):
    if (Pieces[pid].x == x-1 and Pieces[pid].y == y-2) or (Pieces[pid].x == x+1 and Pieces[pid].y == y-2) :
        for i in range(32):
            if Pieces[i].status == 1:
                if Pieces[i].x == Pieces[pid].x and Pieces[i].y == Pieces[pid].y + 1:
                    return False
        return True
    elif (Pieces[pid].x == x+1 and Pieces[pid].y == y+2) or (Pieces[pid].x == x-1 and Pieces[pid].y == y+2):
        for i in range(32):
                if Pieces[i].status == 1:
                    if Pieces[i].x == Pieces[pid].x and Pieces[i].y == Pieces[pid].y - 1:
                        return False
        return True
    elif (Pieces[pid].x == x-2 and Pieces[pid].y == y-1) or (Pieces[pid].x == x-2 and Pieces[pid].y == y+1):
        for i in range(32):
            if Pieces[i].status == 1:
                if Pieces[i].x == Pieces[pid].x + 1 and Pieces[i].y == Pieces[pid].y:
                    return False 
        return True
    elif (Pieces[pid].x == x+2 and Pieces[pid].y == y-1) or (Pieces[pid].x == x+2 and Pieces[pid].y == y+1):
        for i in range(32):
            if Pieces[i].status == 1:
                if Pieces[i].x == Pieces[pid].x - 1 and Pieces[i].y == Pieces[pid].y:
                    return False
        return True
    return False
def check_cannons(x,y):
    CanGo = Check_space(x,y)
    if Pieces[pid].x == x:
        if Pieces[pid].y < y:
            for i in range(32):
                if Pieces[i].x == x and Pieces[i].y > Pieces[pid].y and Pieces[i].y < y and Pieces[i].status == 1:
                    count = count_chess(x,y)
                    if CanGo == 2 and count == 1:
                        return True
                    else:
                        return False
        elif Pieces[pid].y > y:
            for i in range(32):
                if Pieces[i].x == x and Pieces[i].y < Pieces[pid].y and Pieces[i].y > y and Pieces[i].status == 1:
                    count = count_chess(x,y)
                    if CanGo == 2 and count == 1:
                        return True
                    else:
                        return False
        if CanGo == 1:
            return True
        else:
            return False
    elif Pieces[pid].y == y and Pieces[pid].y == y:
        if Pieces[pid].x < x:
            for i in range(32):
                if Pieces[i].y == y and Pieces[i].x > Pieces[pid].x and Pieces[i].x < x and Pieces[i].status == 1:
                    count = count_chess(x,y)
                    if CanGo == 2 and count == 1:
                        return True
                    else:
                        return False
        elif Pieces[pid].x > x:
            for i in range(32):
                if Pieces[i].y == y and Pieces[i].x < Pieces[pid].x and Pieces[i].x > x and Pieces[i].status == 1:
                    count = count_chess(x,y)
                    if CanGo == 2 and count == 1:
                        return True
                    else:
                        return False
        if CanGo == 1:
            return True
        else:
            return False
    else:
        return False
def check_advisors(x,y):
    if Pieces[pid].colour == 0:
        if 5>= x >= 3 and 2 >= y >= 0:
            if Pieces[pid].x == x-1 or Pieces[pid].x == x+1:
                return True
    elif Pieces[pid].colour == 1:
        if 5>= x >= 3 and 9 >= y >= 7:
            if Pieces[pid].x == x - 1 or Pieces[pid].x == x + 1:
                return True
    return False
def check_elephants(x,y):
    if Pieces[pid].colour == 0:
        if y < 5:
            if (Pieces[pid].x == x + 2 and Pieces[pid].y == y + 2) or (Pieces[pid].x == x - 2 and Pieces[pid].y == y + 2) or  (Pieces[pid].x == x + 2 and Pieces[pid].y == y - 2) or (Pieces[pid].x == x - 2 and Pieces[pid].y == y - 2):
                for i in range(32):
                    if Pieces[i].status == 1:
                        if Pieces[i].x == x + 1 and Pieces[i].y == y + 1 :
                            return False
                        elif Pieces[i].x == x + 1 and Pieces[i].y == y - 1 :
                            return False
                        elif Pieces[i].x == x - 1 and Pieces[i].y == y + 1 :
                            return False
                        elif Pieces[i].x == x - 1 and Pieces[i].y == y - 1 :
                            return False
                return True
        return False
    if Pieces[pid].colour == 1:
        if y > 4:
            if (Pieces[pid].x == x + 2 and Pieces[pid].y == y + 2) or (Pieces[pid].x == x - 2 and Pieces[pid].y == y + 2) or  (Pieces[pid].x == x + 2 and Pieces[pid].y == y - 2) or (Pieces[pid].x == x - 2 and Pieces[pid].y == y - 2):
                for i in range(32):
                    if Pieces[i].status == 1:
                        if Pieces[i].x == x + 1 and Pieces[i].y == y + 1 :
                            return False
                        elif Pieces[i].x == x + 1 and Pieces[i].y == y - 1 :
                            return False
                        elif Pieces[i].x == x - 1 and Pieces[i].y == y + 1 :
                            return False
                        elif Pieces[i].x == x - 1 and Pieces[i].y == y - 1 :
                            return False
                return True
        return False
def check_soldiers(x,y):
    if Pieces[pid].x == x and y == Pieces[pid].y + 1 and Pieces[pid].colour == 0:
        return True
    elif Pieces[pid].x == x and y == Pieces[pid].y - 1 and Pieces[pid].colour == 1:
        return True
    elif Pieces[pid].y == y and ((Pieces[pid].y < 5 and (x == Pieces[pid].x - 1 or x == Pieces[pid].x + 1) and Pieces[pid].colour == 1) or (Pieces[pid].y > 4 and (x == Pieces[pid].x - 1 or x == Pieces[pid].x + 1)  and Pieces[pid].colour == 0)):
        return True
    return False
#chess pieces action
def create_Chess():
    for i in range(len(data)):
        temp = chess(data[i][0], data[i][1], data[i][2], data[i][3], data[i][4], data[i][5], data[i][6], data[i][7], 0.07)
        Pieces.append(temp)
def show_32p():
    for i in range(32):
        Pieces[i].draw()
def show_dead():
    global rdeadcount, bdeadcount
    for i in range(len(Dead)):
        Dead[i].draw()
def select_chess(pos):
    for i in range(Start(turns), Start(turns)+16):
        if Pieces[i].status == 1:
            Pieces[i].select(pos)
            if Pieces[i].selected == 2 and Pieces[i].colour == turns:
                global pid
                pid = i
                
def rollover_chess(pos):
    for i in range(Start(turns), Start(turns)+16):
        if Pieces[i].status == 1:
            Pieces[i].rollover(pos)
def Check_space(x,y):
    Space = 0 #1: space, 2: opponent, 3: self
    for i in range(32):
        if Pieces[i].x == x and Pieces[i].y == y and Pieces[i].status == 1:
            if Pieces[i].colour == turns:
                Space = 3
                print("self")
                print(Space)
                return Space
            else:
                Space = 2
                print("opponent")
                print(Space)
                return Space
        else:
            Space = 1
    return Space
def check_status(x,y):
    global rdeadcount, bdeadcount, Back
    for i in range(Start(turns), Start(turns)+16):
        if Pieces[i].x == x and Pieces[i].y == y:
            Pieces[i].eat()
            if turns == 0:
                rdeadcount += 1
            elif turns == 1:
                bdeadcount += 1
            Dead.append(Pieces[i])
            Dead[len(Dead)-1].x = 860
            if Dead[len(Dead)-1].colour == 0:
                Dead[len(Dead)-1].y = 10 + rdeadcount * 20
            elif Dead[len(Dead)-1].colour == 1:
                Dead[len(Dead)-1].y = 450 + bdeadcount * 20
def check_win():
    global Winner
    for i in range(Start(turns), Start(turns)+16):
        if (Pieces[i].id == 4 or Pieces[i].id == 27) and Pieces[i].status == 0:
            if Pieces[i].id == 4:
                print("Black Win")
                Winner = WinB
            elif Pieces[i].id == 27:
                print("Red Win")
                Winner = WinR
            print("Win")
            return 1
    return 0
def check_movement(x,y):
    if Pieces[pid].type == ("C"):
        CanMove = check_cars(x,y)
        return CanMove
    elif Pieces[pid].type == ("H"):
        CanMove = check_horse(x,y)
        return CanMove
    elif Pieces[pid].type == ("A"):
        CanMove = check_advisors(x,y)
        return CanMove
    elif Pieces[pid].type == ("E"):
        CanMove = check_elephants(x,y)
        return CanMove
    elif Pieces[pid].type == ("S"):
        print("S")
        CanMove = check_soldiers(x,y)
        return CanMove
    elif Pieces[pid].type == ("K"):
        CanMove = check_king(x,y)
        return CanMove
    elif Pieces[pid].type == ("CA"):
        print("CA")
        CanMove = check_cannons(x,y)
        return CanMove
#files management
def saveFile():
    global saving_path
    fp = filedialog.asksaveasfile(initialdir=saving_path,
                                    title="Name your saving",
                                    defaultextension='.csv',
                                    filetypes=[
                                        ("Text file",".csv"),
                                        ("All files", ".*"),
                                    ])

    if fp is None:
        print("the file does not exist")
        return
    #filetext = input("Enter some text I guess: ") //use this if you want to use console window
    write_file(fp)
    
    
def openFile():
    global saving_path, data
    fp = filedialog.askopenfilename(initialdir=saving_path,
                                          title="Select your saving",
                                          filetypes= (("text files","*.csv"),
                                          ("all files","*.*")))
    if fp is None:
        return
    read_file(fp)

def read_file(f):
    global data, N
    if os.path.exists(f):
        print("the file exists")
        data = open(f, "r").readlines()
        N = len(data)
        for i in range(N): 
            data[i] = data[i].replace("\n", "").split(",")
            for j in range(5):
                if data[i][j].isdigit():
                    data[i][j] = int(data[i][j])

def write_file(fp):
    global Pieces
    temp = []
    print(str(Pieces))
    for i in range(len(data)):
        temp.append(str(Pieces[i].id) + "," + str(int(Pieces[i].x)) + "," + str(int(Pieces[i].y)) + "," + str(Pieces[i].colour) + "," + str(Pieces[i].status) + "," + Pieces[i].type + "," + Pieces[i].name + "," + Pieces[i].original)
    for i in range(len(temp)):
        fp.write(temp[i] + "\n")
    fp.close()

#GUI
def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))
    
        
#Startup screen and main loop
def Startup():
    global running
    while running:
        for event in pygame.event.get():
            screen.blit(startup, (0, 0))
            if event.type == pygame.QUIT or quit_button.draw():
                running = False
                return
            elif load_button.draw():
                openFile()
            elif start_button.draw():
                main()
            elif event.type == pygame.MOUSEMOTION:
                pygame.display.set_caption(caption)
        pygame.display.update()

def main():
    global running, L_click, pid, turns, counter, Pieces, Dead, Win, rdeadcount, bdeadcount, gamecounter, Back, temppid
    turns = 0
    Pieces = []
    Dead = []
    Back = []
    Win = 0
    pid = -1
    create_Chess()
    for i in range(32):
        if Pieces[i].status == 0:
            Dead.append(Pieces[i])
            Dead[0].x = 860
            if Dead[0].colour == 0:
                Dead[0].y = 10
                rdeadcount += 1 
            elif Dead[0].colour == 1:
                Dead[0].y = 450
                bdeadcount += 1          
    while Win == 0 and running:
        Win = check_win()
        pos = pygame.mouse.get_pos()
        Background_pos(pos)
        screen.blit(background, (0, 0))
        if turns == 0:
            txtTurn = "Red"
        elif turns == 1:
            txtTurn = "Black"
        draw_text("Turns: "+txtTurn, text_font, (0,0,0), 1010, 10)
        draw_text("Red: "+str(rdeadcount), text_font, (0,0,0), 1055, 40)
        draw_text("Black: "+str(bdeadcount), text_font, (0,0,0), 1055, 70)
        draw_text("Selected: "+str(Pieces[pid].name), select_font, (0,0,0), 1010, 100)
        show_32p()
        show_dead()
        if save_button.draw():
            saveFile()
        if menu_button.draw():
            return
        if reverse_button.draw():
            if len(Back) != 0:
                Pieces[temppid].y = Back.pop()
                Pieces[temppid].x = Back.pop()
                turns = switch_turn(turns)
                print("Undo")
            else:
                print("No more undo")
        for event in pygame.event.get() :   
            if event.type == pygame.QUIT:
                running = False
                return
            elif event.type == pygame.MOUSEMOTION:
                pygame.display.set_caption(caption)
                rollover_chess(pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if L_click == 1:
                        CanGo = Check_space(boardpos.x, boardpos.y)
                        ValidMove = check_movement(boardpos.x, boardpos.y)
                        if L_click == 1 and pid != -1 and CanGo != 3 and ValidMove != False:
                            temppid = pid
                            Back.append(Pieces[temppid].x)
                            Back.append(Pieces[temppid].y)
                            Pieces[pid].move(boardpos.x, boardpos.y)
                            turns = switch_turn(turns)
                            L_click = 0
                            pid = -1
                            check_status(boardpos.x, boardpos.y)
                            CanGo = 0
                        else:
                            ValidMove = True
                            L_click = 0
                            pid = -1
                            print("Invalid Move")
                    else:
                        select_chess(pos)
                        print(pid)
                        if pid != -1:
                            L_click = 1 
        if Win == 1:
            End()
        pygame.display.update()
        timer.tick(fps)
        
        
def End():
    global running
    while running:
        for event in pygame.event.get():
            screen.blit(Winner, (0, 0))
            if event.type == pygame.QUIT or quit_button.draw():
                running = False
                return
            elif rs_button.draw():
                read_file(os.path.join(saving_path, 'Default.csv'))
                pygame.mixer.init()
                pygame.mixer.music.play()
                pygame.mixer.music.set_volume(0.5)
                main()
            elif event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                pygame.display.set_caption(caption + str(pos))
        pygame.display.update()
##################################################################
print("My SBA project has started")
read_file(os.path.join(saving_path, 'Default.csv'))
while running:
    pygame.mixer.init()
    pygame.mixer.music.play()
    pygame.mixer.music.set_volume(0.5)
    Startup()
pygame.quit()
