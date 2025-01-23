import pygame
import subprocess
import json
import shutil
import os

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
    if type(rawjson) != str:
        for key in rawjson["sitedata"]:
            if type(rawjson["sitedata"][key]) == list:
                if rawjson["sitedata"][key][0] == "Color":
                    send["sitedata"][key] = pygame.Color(rawjson["sitedata"][key][1],rawjson["sitedata"][key][2],rawjson["sitedata"][key][3])
        for i in range(len(rawjson["elements"])):
            for key in rawjson["elements"][i]:
                if type(rawjson["elements"][i][key]) == list:
                    if rawjson["elements"][i][key][0] == "Color":
                        send["elements"][i][key] = pygame.Color(rawjson["elements"][i][key][1],rawjson["elements"][i][key][2],rawjson["elements"][i][key][3])
    return send

pgmath = pygame.math

fonts = {
    "arial":"./assets/fonts/arial/arial.ttf"
}
webpageconnected = False
webpagedata = {}

#print(webpagedata, type(webpagedata))

pygame.init()
screen = pygame.display.set_mode((xsize,ysize))
clock = pygame.time.Clock()
running = True

def handledata():
    global running
    global site
    global webpageconnected
    global webpagedata
    dataread = readjson(datapath)
    if dataread["status"] == "QUIT":
        writejson(datapath,{"status":"OFF"})
        running = False
    if dataread["status"] == "READ":
        webpagedata = loadJSONfromfile("./Lands/"+dataread["data"][0]+"/main.json")
        if webpagedata == "NOTREAL":
            webpageconnected = False
        else:
            webpageconnected = True
        writejson(datapath,{"status":"FREE"})
        

while running:
    handledata()
    for event in pygame.event.get(): #onquit
        if event.type == pygame.QUIT:
            writejson(datapath,{"status":"QUIT"})
            running = False
    
    
    #compile onscreen data
    if webpageconnected:
        defaultcolor = webpagedata["sitedata"].get("colr",pygame.Color(0,0,0))
        background   = webpagedata["sitedata"].get("back",pygame.Color(255,255,255))
        defaultfont  = webpagedata["sitedata"].get("font","arial")
        pagename     = webpagedata["sitedata"].get("name","untitled STKN")
    else:
        defaultcolor = pygame.Color(0,0,0)
        background   = pygame.Color(255,255,255)
        defaultfont  = "arial"
        pagename     = "untitled STKN"
    screen.fill(background)
    pygame.display.set_caption(pagename)
    #draw here tupid
    verticalOffset=0
    if webpageconnected:
        i2 = 0
        for pagedata in webpagedata["elements"]: #drawloop
            if webpagedata["elements"][i2]["type"] == "text":
                text = pagedata.get("text","MISSING TEXT DATA")
                font = pagedata.get("font","arial")
                size = pagedata.get("size",16)
                colr = pagedata.get("colr",defaultcolor)
                tempfont = pygame.font.Font(fonts[font],size)
                temprender = tempfont.render(text, False, colr)
                screen.blit(temprender,pgmath.Vector2(0,verticalOffset))
                verticalOffset += size
            i2 += 1
    else:
        text = "No Land Loaded"
        font = "arial"
        size = 32
        colr = pygame.Color(255,0,0)
        tempfont = pygame.font.Font(fonts[font],size)
        temprender = tempfont.render(text, False, colr)
        screen.blit(temprender,pgmath.Vector2(0,verticalOffset))
    
    pygame.display.flip()
    
    clock.tick(10)
    
pygame.quit()