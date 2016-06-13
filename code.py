from SimpleCV import Camera, Color, Display, DrawingLayer, np
#import RPi.GPIO as GPIO ## Import GPIO library
import time
import pygame

#GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
#GPIO.setup(7, GPIO.OUT) ## Setup GPIO Pin 7 to OUT
#GPIO.cleanup()
width = 320
height = 240
screensize = width * height
cam = Camera(0, {"width": width,"height":height})

img2 = cam.getImage().flipHorizontal().scale(320,240)

display = Display()
clock = pygame.time.Clock()

#Create the layer to display a left sign
def leftlayer():
    newlayer = DrawingLayer(img.size())
   
    #The corner points for a rectangle sign
    points = [(0,0),(100,0),(100,240),(0,240)]
    newlayer.polygon(points, filled=True, color=Color.GREEN)
    newlayer.setLayerAlpha(75)
    newlayer.text("Left",(256/4,480/4),color=Color.WHITE)
    return newlayer
   
def stopleftlayer():
    newlayer = DrawingLayer(img.size())
   
    #The corner points for a rectangle sign
    points = [(0,0),(100,0),(100,240),(0,240)]
    newlayer.polygon(points, filled=True, color=Color.RED)
    newlayer.setLayerAlpha(75)
    newlayer.text("Left",(256/4,480/4),color=Color.WHITE)
    return newlayer
   
def rightlayer():
    newlayer = DrawingLayer(img.size())
   
    #The corner points for a rectangle sign
    points = [(430/2,0),(640/2,0),(640,480/2),(430/2,480/2)]
    newlayer.polygon(points, filled=True, color=Color.GREEN)
    newlayer.setLayerAlpha(75)
    newlayer.text("Right",(550/2,480/4),color=Color.WHITE)
    return newlayer   

def stoprightlayer():
    newlayer = DrawingLayer(img.size())
   
    #The corner points for a rectangle sign
    points = [(430/2,0),(640/2,0),(640/2,480/2),(430/2,480/2)]
    newlayer.polygon(points, filled=True, color=Color.RED)
    newlayer.setLayerAlpha(75)
    newlayer.text("Right",(550/2,480/4),color=Color.WHITE)
    return newlayer   
       
#Create the layer to display a stop sign
def stoplayer():
    newlayer = DrawingLayer(img.size())
   
    #The corner points for a rectangle sign
    points = [(200/2,0),(430/2,0),(430/2,480/2),(200/2,480/2)]
    newlayer.polygon(points, filled=True, color=Color.RED)
    newlayer.setLayerAlpha(75)
    newlayer.text("Stop",(640/4,480/4),color=Color.WHITE)
    return newlayer   

#Create the layer to display a go sign

def golayer():
    newlayer = DrawingLayer(img.size())
   
    #The corner points for a rectangle sign
    points = [(200/2,0),(430/2,0),(430/2,480/2),(200/2,480/2)]
    newlayer.polygon(points, filled=True, color=Color.GREEN)
    newlayer.setLayerAlpha(75)
    newlayer.text("Go",(640/4,480/4),color=Color.WHITE)
    return newlayer   

'''def blink_led():
	GPIO.cleanup()
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(7, GPIO.OUT)
	GPIO.output(7,True)## Switch on pin 7
	time.sleep(1)## Wait
	GPIO.output(7,False)## Switch off pin 7
	time.sleep(1)## Wait
	GPIO.cleanup()'''
while display.isNotDone():
    img = cam.getImage().flipHorizontal().scale(640/2,480/2)
    #img3 = img - img2
    #By default, show the go layer
    layer = golayer()
    left = leftlayer()
    right = rightlayer()
   # blink = blink_led()
    '''This section used to measure the performance of the algorithm
    using frame rate per second. A slower system will have a slower frame
    rates while faster processors will have higher FPS'''
    milliseconds = clock.tick(30) # do not go faster than this framerate
    # Print framerate and playtime in titlebar.
    text = "FPS: {0:.2f}".format(clock.get_fps())
    img.drawText(text, 10, 10, fontsize = 20, color=Color.BLUE)
    
    #The minimum blob is at least 10% of screen
    min_blob_size = 0.50*screensize
   
    #The maximum blobl is at most 80% of screen
    max_blob_size = 0.95*screensize
   
    #Find the Yellow blob in image
    dist = img.colorDistance(Color.BLACK).dilate(2)
    segmented = dist.binarize()
    blobs = segmented.findBlobs(minsize=1000)
    if blobs:
        circles = blobs.filter([b.isCircle(0.2) for b in blobs])
        if circles:
            for c in circles:
                bcrd = c.coordinates()
                if(bcrd[-2]<=200/2):
                    left = stopleftlayer()
                    print "moving left"
                    img.drawText("Obstacle found left",0,0, fontsize=20, color=Color.RED)
               
                elif(bcrd[-2]>200/2 and bcrd[-2]<430/2):
                    layer = stoplayer()
                    print "moving center"
                    img.drawText("Obstacle found Center",0,0, fontsize=20, color=Color.RED)
                    #blink = blink_led()

                elif(bcrd[-2]>=430/2):
                    right = stoprightlayer()
                    print "moving right"
                    img.drawText("Obstacle found Right",0,0, fontsize=20, color=Color.RED)

                else:
                    right = rightlayer()
                    left = leftlayer()
                    layer = golayer()
        else:
            img.drawText("No Obstacle found",0,0, fontsize=20, color=Color.RED)
            
       
    #Finally, add the drawing layer
    img.addDrawingLayer(layer)
    img.addDrawingLayer(left)
    img.addDrawingLayer(right)   
    img.show()
    time.sleep(0)
