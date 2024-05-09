import pygame
import os
import random
import time
import sys

pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(10)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

WIDTH = 500
HEIGHT = 700
FPS = 100
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

#functions
font_name = pygame.font.match_font("arial")#setting 
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("img/font.ttf", size)

def options():
    while True:
        
        background_image =  pygame.image.load(os.path.join("img", "BR-116Brazil.png")).convert()
        background_image = pygame.transform.scale(background_image, (500, 700))
        screen.blit(background_image, (0, 0))
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        OPTIONS_TEXT = get_font(50).render("OPTIONS", True, "#b68f40")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(250, 130))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)
        '''screen.blit()
        screen.blit()'''
        
        OPTIONS_BACK = Button(image=pygame.image.load("img/Quit Rect.png"), pos=(250, 600),
                             text_input="BACK", font=get_font(25), base_color="White", hovering_color="#d7fcd4")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    button_click_sound = pygame.mixer.Sound(os.path.join("Sounds", "select.mp3"))
                    button_click_sound.set_volume(0.8)
                    button_click_sound.play()
                    pygame.time.delay(300) #delay time for clicking music display
                    return True
        pygame.display.update()

def main_menu():
    while True:
        background_image =  pygame.image.load(os.path.join("img", "BR-116Brazil.png")).convert()
        background_image = pygame.transform.scale(background_image, (500, 700))
        screen.blit(background_image, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(50).render("BR-116", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(250, 130))

        PLAY_BUTTON = Button(image=pygame.image.load("img/Play Rect.png"), pos=(250, 360), 
                            text_input="PLAY", font=get_font(25), base_color="White", hovering_color="#d7fcd4")
        OPTIONS_BUTTON = Button(image=pygame.image.load("img/Options Rect.png"), pos=(250, 480), 
                            text_input="OPTIONS", font=get_font(25), base_color="White", hovering_color="#d7fcd4")
        QUIT_BUTTON = Button(image=pygame.image.load("img/Quit Rect.png"), pos=(250, 600), 
                            text_input="QUIT", font=get_font(25), base_color="White", hovering_color="#d7fcd4")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    running = False
                    return running
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    button_click_sound = pygame.mixer.Sound(os.path.join("Sounds", "select.mp3"))
                    button_click_sound.set_volume(0.8)
                    button_click_sound.play()
                    pygame.time.delay(300) #delay time for clicking music display
                    running = True
                    return running
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    button_click_sound = pygame.mixer.Sound(os.path.join("Sounds", "select.mp3"))
                    button_click_sound.set_volume(0.8)
                    button_click_sound.play()
                    pygame.time.delay(300) #delay time for clicking music display
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    button_click_sound = pygame.mixer.Sound(os.path.join("Sounds", "select.mp3"))
                    button_click_sound.set_volume(0.8)
                    button_click_sound.play()
                    pygame.time.delay(300) #delay time for clicking music display
                    running = False
                    return running
        pygame.display.update()
        
#class
class Button():
    def __init__(self, image=None, pos=(0, 0), text_input="", font=None, base_color=(255, 255, 255), hovering_color=(255, 255, 255), width=260, height=80):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)

        #if no image, create a rectangle
        if self.image is None:
            self.image = pygame.Surface((width, height))
            self.image.fill(self.base_color)
        else:
            #stansform the image
            self.image = pygame.transform.scale(self.image, (width, height))
        
        # button size
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=self.rect.center)
    
    def update(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        return self.rect.collidepoint(position)

    def changeColor(self, position):
        if self.rect.collidepoint(position):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

main_menu()
pygame.quit()