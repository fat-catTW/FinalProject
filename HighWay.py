import pygame
import os
import random



WIDTH = 500
HEIGHT = 700
FPS = 90
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#game init
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("HighWay69")


#load image
player_img = pygame.image.load(os.path.join("img", "player.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (6, 12))
player_mini_img.set_colorkey(BLACK)
pygame.display.set_icon(player_mini_img)

otherVic_imgs = []
for i in range(7):
    otherVic_imgs.append(pygame.image.load(os.path.join("img", f"Vic{i}.png")).convert())


#load sound


#functions

#class
class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50,100))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 8
        self.speedy = 8
    
    def update(self):
        
        key_pressed = pygame.key.get_pressed()
        
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speedx
        
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx
        
        if key_pressed[pygame.K_UP]:
            self.rect.y -= self.speedy
            
        if key_pressed[pygame.K_DOWN]:
            self.rect.y += self.speedy
        
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        
        if self.rect.left < 0:
            self.rect.left = 0
        
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        
        if self.rect.top < 0:
            self.rect.top = 0

class Vehicle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(random.choice(otherVic_imgs), (50, 100))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.bottom = random.randrange(-180, -100)
        self.speedy = 5
    
    def update(self):
        self.rect.y += self.speedy
        
        if self.rect.top > HEIGHT + 100:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.top = -200
        
    

all_sprites = pygame.sprite.Group()
other_vic = Vehicle()
all_sprites.add(other_vic)
player = Player()
all_sprites.add(player)

#game loop

running = True

while running:
    
    clock.tick(FPS)
    
    
    
    
    #input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    
    #game update
    all_sprites.update()
    
    
    
    #display
    screen.fill(WHITE)
    all_sprites.draw(screen)
    pygame.display.update()


pygame.quit()