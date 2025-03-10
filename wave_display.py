import glfw
from OpenGL.GL import *
import numpy as np
import math

SIZE = 300

CENTER = SIZE/2

amplitude = np.zeros((SIZE, SIZE))
number_of_waves = 0

#amplitude -> color value (n = pure white, -n = pure black)
def interpolate_color(amplitude):
    #constructive interference between n waves with amplitude 1 must be less then n
    if(amplitude > number_of_waves):
        amplitude = number_of_waves
    elif(amplitude < -number_of_waves):
        amplitude = -number_of_waves

    color_value = (amplitude + number_of_waves) / (2*number_of_waves)
    return color_value

def reset_amplitudes():
    for x in range(SIZE):
        for y in range(SIZE):
            amplitude[x][y] = 0

def generate_wave(time, x_center, y_center, wavelength):
    #normalize pixel x, y to OpenGL -1 to 1
    #x_center = (x_center / SIZE) * 2 - 1  # Normalize x from [0, SIZE] to [-1, 1]
    #y_center = (y_center / SIZE) * 2 - 1  # Normalize y from [0, SIZE] to [-1, 1]
    
    for x in range(SIZE):
        for y in range(SIZE):
            distance = math.sqrt((x_center-x)**2 + (y_center-y)**2)
            amplitude[x][y] += math.sin((2*math.pi/wavelength)*distance - time)

def draw_wave():
    for x in range(SIZE):
        for y in range(SIZE):
            color = interpolate_color(amplitude[x][y])

            # Normalize the coordinates from (0, SIZE) to (-1, 1)
            norm_x = (x / SIZE) * 2 - 1  # Normalize x from [0, SIZE] to [-1, 1]
            norm_y = (y / SIZE) * 2 - 1  # Normalize y from [0, SIZE] to [-1, 1]

            glColor3f(color, color, color)
            glBegin(GL_POINTS)
            glVertex2f(norm_x, norm_y)  # Use glVertex2f for normalized coordinates
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
    
    global number_of_waves
    number_of_waves = 2
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity() # resets transformation matrix
        
        time = glfw.get_time()
        reset_amplitudes()
        
        generate_wave(time, 0, 0, 50)
        generate_wave(time, SIZE, SIZE, 50)
        
        draw_wave()
        
        #OpenGL renders to a hidden (back) buffer while the previous frame is still displayed. 
        #This moves the back buffer to the front.
        glfw.swap_buffers(window) 
        glfw.poll_events() #processes user input
    
    glfw.terminate()

if __name__ == "__main__":
    main()