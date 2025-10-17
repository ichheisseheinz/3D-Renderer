import pygame as pg
import sys
import math

from construction import *

# Screen Settings
FPS = 60
S_WIDTH, S_HEIGHT = 1280, 720
pg.init()
win = pg.display.set_mode((S_WIDTH, S_HEIGHT))
pg.display.set_caption("Basic 3d Rendering")
running = True
clock = pg.time.Clock()

# Render defaults
FOV = 500
x_rot = 0
y_rot = 0
z_rot = 0
zoom_out = 0.99
zoom_in = 1.01

# Control settings
SPEED = 0.05

# Main class
class Renderer:
    def __init__(self, shape, x_rot, y_rot, z_rot, fov):
        # Location properties
        self.origin = shape[0]
        self.points = shape[1]
        self.lines = shape[2]

        # Transformation properties
        self.rotations = [x_rot, y_rot, z_rot]
        self.fov = fov
        self.zoom = 1

        # UI properties
        self.font = pg.font.SysFont('default', 25)
        self.rotation_tracker = [x_rot, y_rot, z_rot]
        self.visible_verticies = True
        self.menu = True

        # Others
        self.alt_pressed = False
        self.m_pressed = False

    def render_ui(self):
        # FOV text
        text1 = self.font.render(f'FOV (Increase with UP, decrease with DOWN): {self.fov}', True, 'white')
        text1_rect = text1.get_rect()

        # Rotation text
        text2 = self.font.render\
            (f'Object Rotation (Control with W, A, S, D, Q, E): (x: {round(self.rotation_tracker[0], 3)}, y: {round(self.rotation_tracker[1], 3)}, z: {round(self.rotation_tracker[2], 3)})', True, 'white')
        text2_rect = text2.get_rect()

        # Scale text
        text3 = self.font.render(f'Viewport Scale (Increase with +, decrease with -): {round(self.zoom, 3)}', True, 'white')
        text3_rect = text3.get_rect()

        # Vertex toggle text
        text4 = self.font.render(f'Vertex toggle (Change with ALT): {'ON' if self.visible_verticies else 'OFF'}', True, 'white')
        text4_rect = text4.get_rect()

        # Menu text
        menu_text = self.font.render('Press M to toggle properties', True, 'white')
        menu_rect = menu_text.get_rect()

        # Draw text to the screen
        if self.menu:
            win.blit(menu_text, (5, 5), menu_rect)
        else:
            win.blit(text1, (5, 5), text1_rect)
            win.blit(text2, (5, 30), text2_rect)
            win.blit(text3, (5, 55), text3_rect)
            win.blit(text4, (5, 80), text4_rect)

    def scale(self, x:float, y:float, z:float, point:list):
        x = [point[0] * x, 0, 0]
        y = [0, point[1] * y, 0]
        z = [0, 0, point[2] * z]

        for i in range(3):
            point[i] = x[i] + y[i] + z[i]
    
    def rotate_x(self, theta:float, point:list):
        """
        Applies the matrix
        [ 1 0    0   ]
        [ 0 cos -sin ]
        [ 0 sin  cos ]
        to the specified point
        """

        x = [point[0], 0, 0]
        y = [0, point[1] * math.cos(theta), point[1] * math.sin(theta)]
        z = [0, point[2] * -math.sin(theta), point[2] * math.cos(theta)]

        for i in range(3):
            point[i] = x[i] + y[i] + z[i]
    
    def rotate_y(self, theta:float, point:list):
        """
        Applies the matrix
        [  cos 0 sin ]
        [  0   1 0   ]
        [ -sin 0 cos ]
        to the specified point
        """

        x = [point[0] * math.cos(theta), 0, point[0] * math.sin(theta)]
        y = [0, point[1], 0]
        z = [point[2] * -math.sin(theta), 0, point[2] * math.cos(theta)]

        for i in range(3):
            point[i] = x[i] + y[i] + z[i]

    def rotate_z(self, theta:float, point:list):
        """
        Applies the matrix
        [ cos -sin 0 ]
        [ sin  cos 0 ]
        [ 0    0   1 ]
        to the specified point
        """

        x = [point[0] * math.cos(theta), point[0] * -math.sin(theta), 0]
        y = [point[1] * math.sin(theta), point[1] * math.cos(theta), 0]
        z = [0, 0, point[2]]

        for i in range(3):
            point[i] = x[i] + y[i] + z[i]
    
    def control(self):
        keys = pg.key.get_pressed()
        
        # Rotation Controls
        if keys[pg.K_s]:
            self.rotations[0] = SPEED
            self.rotation_tracker[0] += SPEED

            for i in self.points:
                self.rotate_x(self.rotations[0], i)
        if keys[pg.K_w]:
            self.rotations[0] = -SPEED
            self.rotation_tracker[0] -= SPEED

            for i in self.points:
                self.rotate_x(self.rotations[0], i)
        if keys[pg.K_q]:
            self.rotations[2] = SPEED
            self.rotation_tracker[2] += SPEED

            for i in self.points:
                self.rotate_z(self.rotations[2], i)
        if keys[pg.K_e]:
            self.rotations[2] = -SPEED
            self.rotation_tracker[2] -= SPEED

            for i in self.points:
                self.rotate_z(self.rotations[2], i)
        if keys[pg.K_d]:
            self.rotations[1] = SPEED
            self.rotation_tracker[1] += SPEED

            for i in self.points:
                self.rotate_y(self.rotations[1], i)
        if keys[pg.K_a]:
            self.rotations[1] = -SPEED
            self.rotation_tracker[1] -= SPEED

            for i in self.points:
                self.rotate_y(self.rotations[1], i)
        
        # View settings
        if keys[pg.K_UP] and self.fov < 2000:
            self.fov += 25
        if keys[pg.K_DOWN] and self.fov > 200:
            self.fov -= 25

        if keys[pg.K_EQUALS]:
            self.zoom *= zoom_in/zoom_out

            for i in self.points:
                self.scale(zoom_in/zoom_out, zoom_in/zoom_out, zoom_in/zoom_out, i)
        if keys[pg.K_MINUS] and self.zoom > 0.1:
            self.zoom *= zoom_out/zoom_in

            for i in self.points:
                self.scale(zoom_out/zoom_in, zoom_out/zoom_in, zoom_out/zoom_in, i)
        
        # Toggle vertecies
        if (keys[pg.K_LALT] or keys[pg.K_RALT]):
            if not self.alt_pressed:
                self.visible_verticies = not self.visible_verticies
            self.alt_pressed = True
        else:
            self.alt_pressed = False

        # Toggle menu
        if keys[pg.K_m]:
            if not self.m_pressed:
                self.menu = not self.menu
            self.m_pressed = True
        else:
            self.m_pressed = False
        
        self.draw_lines(self.create_projected_points())
    
    # Converts point's 3d location to a point that can be represented in 3d space
    def create_projected_points(self):
        projected = []

        for i in range(len(self.points)):
            if self.points[i][2] > -self.fov:
                proj_x = (self.points[i][0] * self.fov) / (self.points[i][2] + self.fov)
                proj_y = (self.points[i][1] * self.fov) / (self.points[i][2] + self.fov)
            else:
                # Project points normally even if they are behind the camera
                proj_x = (self.points[i][0] * self.fov) / 0.01
                proj_y = (self.points[i][1] * self.fov) / 0.01

            projected.append((proj_x * self.zoom + (S_WIDTH / 2), proj_y * self.zoom + (S_HEIGHT / 2)))

        return projected
    
    # Draws lines between two points
    def draw_lines(self, points):
        for i in range(len(self.points)):
            if 0 <= points[i][0] <= S_WIDTH and 0 <= points[i][1] <= S_HEIGHT and self.visible_verticies:
                pg.draw.circle(win, 'white', points[i], 2 * self.zoom)
        for i in self.lines:
            pg.draw.line(win, pg.Color(255, 255, 255, a=122), points[i[0]], points[i[1]])

# Object setup
obj : list[Shape] = [CustomOBJ(0, 0, 0, 'objects/pawn.obj', 400)]
renderer : list[Renderer] = []
for i in obj:
    i.construct()
    renderer.append(Renderer(i.shape, x_rot, y_rot, z_rot, FOV))

# Main loop
while running:
    clock.tick(FPS)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    win.fill("black")
    
    for i in renderer:
        i.control()

    renderer[0].render_ui()

    pg.display.update()

pg.quit()
sys.exit()
