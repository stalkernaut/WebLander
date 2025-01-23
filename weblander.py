import pygame
import subprocess
import json

version = "0.1A"


#<[]> 4 def (<[size:16]>text)

xsize = 512
ysize = 512

def loadJSONfromfile(path):
    file = open(path,"r")
    rawjson = json.loads(file.read())
    file.close()
    send = rawjson
    for key in rawjson["sitedata"]:
        if type(rawjson["sitedata"][key]) == list:
            if rawjson["sitedata"][key][0] == "Color":
                send["sitedata"][key] = pygame.Color(rawjson["sitedata"][key][1],rawjson["sitedata"][key][2],rawjson["sitedata"][key][3])
    for i in range(len(rawjson["elements"])):
        for key in rawjson["elements"][i]:
            if type(rawjson["elements"][i][key]) == list:
                if rawjson["elements"][1][key][0] == "Color":
                    send["elements"][i][key] = pygame.Color(rawjson["elements"][i][key][1],rawjson["elements"][i][key][2],rawjson["elements"][i][key][3])
    return send

pgmath = pygame.math

fonts = {
    "arial":"./assets/fonts/arial/arial.ttf"
}
webpageconnected = True
webpagedata = loadJSONfromfile("./LoadedSite/main.json")

#print(webpagedata, type(webpagedata))

pygame.init()
screen = pygame.display.set_mode((xsize,ysize))
clock = pygame.time.Clock()
running = True

while running:
    
    for event in pygame.event.get(): #onquit
        if event.type == pygame.QUIT:
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
        for pagedata in webpagedata["elements"]: #drawloop
            text = pagedata.get("text","MISSING TEXT DATA")
            font = pagedata.get("font","arial")
            size = pagedata.get("size",16)
            colr = pagedata.get("colr",defaultcolor)
            tempfont = pygame.font.Font(fonts[font],size)
            temprender = tempfont.render(text, False, colr)
            screen.blit(temprender,pgmath.Vector2(0,verticalOffset))
            verticalOffset += size
    else:
        text = "No Webpage Loaded"
        font = "arial"
        size = 32
        colr = pygame.Color(255,0,0)
        tempfont = pygame.font.Font(fonts[font],size)
        temprender = tempfont.render(text, False, colr)
        screen.blit(temprender,pgmath.Vector2(0,verticalOffset))
    
    pygame.display.flip()
    
    clock.tick(60)
    
pygame.quit()