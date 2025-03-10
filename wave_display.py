import glfw
from OpenGL.GL import *
import numpy as np
import math

SIZE = 300
QUALITY = 7
LINE_WIDTH = 2*QUALITY + 1

CENTER = SIZE/2

#amplitude -> color value (1 = pure white, -1 = pure black)
def interpolate_color(amplitude):
    if(amplitude > 1):
        amplitude = 1
    elif(amplitude < -1):
        amplitude = -1

    color_value = (amplitude + 1) / 2
    return color_value

def draw_wave(time, x, y, wavelength):
    glLineWidth(LINE_WIDTH)
    glBegin(GL_LINE_STRIP)
    #normalize pixel x, y to OpenGL -1 to 1
    x = (x - CENTER) / CENTER
    y = (y - CENTER) / CENTER
    
    for r in np.linspace(-2,2,int((-1.5*CENTER/5)*QUALITY + (13*CENTER/5))):
        for theta in range(360):
            color = interpolate_color(math.sin((1/wavelength)*(5/math.pi)*(r-time)))
            glColor3f(color,color,color)
            x_pixel = x + r*math.cos(math.radians(theta))
            y_pixel = y + r*math.sin(math.radians(theta))
            if(x_pixel <= 1 or x_pixel >= -1) and (y_pixel <= 1 or y_pixel >= -1):
                glVertex2f(x_pixel, y_pixel)
    glEnd()

def main():
    if not glfw.init():
        return
    
    window = glfw.create_window(SIZE, SIZE, "2D Wave", None, None)
    if not window:
        glfw.terminate()
        return
    
    glfw.make_context_current(window)
    glClearColor(0, 0, 0, 1)
    
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity() # resets transformation matrix
        
        time = glfw.get_time()
        draw_wave(time, CENTER, CENTER, 0.1)
        
        #OpenGL renders to a hidden (back) buffer while the previous frame is still displayed. 
        #This moves the back buffer to the front.
        glfw.swap_buffers(window) 
        glfw.poll_events() #processes user input
    
    glfw.terminate()

if __name__ == "__main__":
    main()