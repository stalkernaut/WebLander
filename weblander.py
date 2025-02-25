import pygame
import subprocess
import json
import shutil

version = "0.1A"

datapath = "./assets/prg/data.json"

subprocess.Popen(['python','./assets/prg/address.py'])

#<[]> 4 def (<[size:16]>text)

def writejson(path, data):
    dataport = open(path,"w")
    dataport.write(json.dumps(data))
    dataport.close()
    
def readjson(path):
    try:
        open(path,"r").close()
    except FileNotFoundError:
        data = "NOTREAL"
    else:
        dataport = open(path,"r")
        data = json.loads(dataport.read())
        dataport.close()
    return data

xsize = 512
ysize = 512

def loadJSONfromfile(path):
    rawjson = readjson(path)
    send = rawjson
    if isinstance(rawjson,str) != True:
        for key in rawjson["landdata"]:
            if type(rawjson["landdata"][key]) == list:
                if rawjson["landdata"][key][0] == "Color":
                    send["landdata"][key] = pygame.Color(rawjson["landdata"][key][1],rawjson["landdata"][key][2],rawjson["landdata"][key][3])
        for i in range(len(rawjson["elements"])):
            for key in rawjson["elements"][i]:
                if type(rawjson["elements"][i][key]) == list:
                    if rawjson["elements"][i][key][0] == "Color":
                        send["elements"][i][key] = pygame.Color(rawjson["elements"][i][key][1],rawjson["elements"][i][key][2],rawjson["elements"][i][key][3])
                    elif type(rawjson["elements"][i][key][0] == list):
                        for i2 in range(len(rawjson["elements"][i][key])):
                            if rawjson["elements"][i][key][i2][0] == "Color":
                                send["elements"][i][key][i2] = pygame.Color(rawjson["elements"][i][key][i2][1],rawjson["elements"][i][key][i2][2],rawjson["elements"][i][key][i2][3])
    return send

pgmath = pygame.math

fonts = {
    "arial":"./assets/fonts/arial/arial.ttf"
}
landconnected = False
landdata = {}

pygame.init()
screen = pygame.display.set_mode((xsize,ysize))
clock = pygame.time.Clock()
running = True

def handledata():
    global running
    global site
    global landconnected
    global landdata
    dataread = readjson(datapath)
    if dataread["status"] == "QUIT":
        writejson(datapath,{"status":"OFF"})
        running = False
    if dataread["status"] == "READ":
        landdata = loadJSONfromfile("./Lands/"+dataread["data"][0]+"/main.json")
        if landdata == "NOTREAL":
            landconnected = False
        else:
            landconnected = True
        writejson(datapath,{"status":"FREE"})
        

while running:
    handledata()
    for event in pygame.event.get(): #onquit
        if event.type == pygame.QUIT:
            writejson(datapath,{"status":"QUIT"})
            running = False
    
    
    #compile onscreen data
    if landconnected:
        defaultcolor = landdata["landdata"].get("colr",pygame.Color(0,0,0))
        background   = landdata["landdata"].get("back",pygame.Color(255,255,255))
        defaultfont  = landdata["landdata"].get("font","arial")
        defaultsize  = landdata["landdata"].get("size",16)
        pagename     = landdata["landdata"].get("name","untitled STKN")
        defaultpadd  = landdata["landdata"].get("padd",0)
    else:
        defaultcolor = pygame.Color(0,0,0)
        background   = pygame.Color(255,255,255)
        defaultfont  = "arial"
        defaultsize  = 16
        pagename     = "untitled Land"
    screen.fill(background)
    pygame.display.set_caption(pagename)
    #draw here tupid
    verticalOffset=0
    if landconnected:
        i2 = 0
        for pagedata in landdata["elements"]: #drawloop
            if landdata["elements"][i2]["type"] == "text":
                text = pagedata.get("text","MISSING TEXT DATA")
                font = pagedata.get("font",defaultfont)
                size = pagedata.get("size",defaultsize)
                colr = pagedata.get("colr",defaultcolor)
                padd = pagedata.get("padd",defaultpadd)
                
                tempfont = pygame.font.Font(fonts[font],size)
                temprender = tempfont.render(text, True, colr)
                verticalOffset += padd
                screen.blit(temprender,pgmath.Vector2(0,verticalOffset))
                
                verticalOffset += size + padd
                
                
            if landdata["elements"][i2]["type"] == "line":
                size = pagedata.get("size",defaultsize)
                colr = pagedata.get("colr",defaultcolor)
                padd = pagedata.get("padd",0)
                
                verticalOffset += padd
                temprect = pygame.Rect(0,verticalOffset,xsize,size)
                pygame.draw.rect(screen,colr,temprect)
                
                verticalOffset += padd + size
            
            
            if landdata["elements"][i2]["type"] == "padd":
                size = pagedata.get("size",defaultsize)
                
                verticalOffset += size
                
                
            if landdata["elements"][i2]["type"] == "mctx":
                text = pagedata.get("text",["MISSING TEXT DATA"])
                font = pagedata.get("font",defaultfont)
                size = pagedata.get("size",defaultsize)
                colr = pagedata.get("colr",[defaultcolor])
                padd = pagedata.get("padd",defaultpadd)
                
                tempfont = pygame.font.Font(fonts[font],size)
                horizontalOffset = 0
                for i3 in range(len(text)):
                    temprender = tempfont.render(text[i3], True, colr[i3])
                    screen.blit(temprender,pgmath.Vector2(horizontalOffset,verticalOffset))
                    horizontalOffset += temprender.get_width()
                
                verticalOffset += size
            i2 += 1
    else:
        text = "No Land Loaded"
        font = "arial"
        size = 32
        colr = pygame.Color(255,0,0)
        tempfont = pygame.font.Font(fonts[font],size)
        temprender = tempfont.render(text, True, colr)
        screen.blit(temprender,pgmath.Vector2(0,verticalOffset))
    
    pygame.display.flip()
    
    clock.tick(10)
    
pygame.quit()