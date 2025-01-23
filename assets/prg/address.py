import pygame
import json

datapath = "./assets/prg/data.json"

def writejson(path, data):
    dataport = open(path,"w")
    dataport.write(json.dumps(data))
    dataport.close()
    
def readjson(path):
    dataport = open(path,"r")
    data = json.loads(dataport.read())
    dataport.close()
    return data

writejson(datapath,{"status":"READ","data":["HOME"]})

currentLand = "HOME"
typing = ""

loadLand = False

pgmath = pygame.math

xsize = 1024
ysize = 64
pygame.init()
screen = pygame.display.set_mode((1024, 64))
clock = pygame.time.Clock()
running = True

pygame.display.set_caption("Address Bar")

def handledata():
    global currentLand
    global loadLand
    global running
    dataread = readjson(datapath)
    if dataread["status"] == "FREE":
        if loadLand:
            writejson(datapath,{"status":"READ","data":[currentLand]})
            loadLand = False
    if dataread["status"] == "QUIT":
        writejson(datapath,{"status":"OFF"})
        running = False
    
        

while running:
    handledata()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            writejson(datapath,{"status":"QUIT"})
            running = False
    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                typing += "A"
            if event.key == pygame.K_b:
                typing += "B"
            if event.key == pygame.K_c:
                typing += "C"
            if event.key == pygame.K_d:
                typing += "D"
            if event.key == pygame.K_e:
                typing += "E"
            if event.key == pygame.K_f:
                typing += "F"
            if event.key == pygame.K_g:
                typing += "G"
            if event.key == pygame.K_h:
                typing += "H"
            if event.key == pygame.K_i:
                typing += "I"
            if event.key == pygame.K_j:
                typing += "J"
            if event.key == pygame.K_k:
                typing += "K"
            if event.key == pygame.K_l:
                typing += "L"
            if event.key == pygame.K_m:
                typing += "M"
            if event.key == pygame.K_n:
                typing += "N"
            if event.key == pygame.K_o:
                typing += "O"
            if event.key == pygame.K_p:
                typing += "P"
            if event.key == pygame.K_q:
                typing += "Q"
            if event.key == pygame.K_r:
                typing += "R"
            if event.key == pygame.K_s:
                typing += "S"
            if event.key == pygame.K_t:
                typing += "T"
            if event.key == pygame.K_u:
                typing += "U"
            if event.key == pygame.K_v:
                typing += "V"
            if event.key == pygame.K_w:
                typing += "W"
            if event.key == pygame.K_x:
                typing += "X"
            if event.key == pygame.K_y:
                typing += "Y"
            if event.key == pygame.K_z:
                typing += "Z"
            if event.key == pygame.K_1:
                typing += "1"
            if event.key == pygame.K_2:
                typing += "2"
            if event.key == pygame.K_3:
                typing += "3"
            if event.key == pygame.K_4:
                typing += "4"
            if event.key == pygame.K_5:
                typing += "5"
            if event.key == pygame.K_6:
                typing += "6"
            if event.key == pygame.K_7:
                typing += "7"
            if event.key == pygame.K_8:
                typing += "8"
            if event.key == pygame.K_9:
                typing += "9"
            if event.key == pygame.K_0:
                typing += "0"
            if event.key == pygame.K_PERIOD:
                typing += "."
            if event.key == pygame.K_SEMICOLON:
                typing += ":"
            if event.key == pygame.K_MINUS:
                typing += "-"
            
            if event.key == pygame.K_BACKSPACE:
                typing = typing[:-1]
            if event.key == pygame.K_RETURN:
                currentLand = typing
                loadLand = True
            
    
    screen.fill(pygame.Color(32,0,64))
    
    tempfont = pygame.font.Font("./assets/fonts/arial/arial.ttf",32)
    temprender = tempfont.render(currentLand, False, pygame.Color(255,255,255))
    screen.blit(temprender,pgmath.Vector2(0,0))
    
    tempfont = pygame.font.Font("./assets/fonts/arial/arial.ttf",32)
    temprender = tempfont.render(">"+typing, False, pygame.Color(255,255,255))
    screen.blit(temprender,pgmath.Vector2(0,32))
    
    pygame.display.flip()

    clock.tick(10)

pygame.quit()