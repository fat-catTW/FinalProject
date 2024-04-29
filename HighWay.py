import pygame
import os
import random
import time


WIDTH = 500
HEIGHT = 700
FPS = 100
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

#game init
pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(10)
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

RPG_rocket = pygame.image.load(os.path.join("img", "RPG.png")).convert()
RPG_rocket.set_colorkey(BLACK)

expl_anim = []
for i in range(9):
    expl_img = pygame.image.load(os.path.join("img", f"expl{i}.png")).convert()
    expl_img.set_colorkey(BLACK)
    expl_anim.append(pygame.transform.scale(expl_img, (90, 90)))




#load sound
turning_sound = pygame.mixer.Sound(os.path.join("Sounds", "CarTurn.mp3"))
turning_sound.set_volume(0.1)

player_turning = pygame.mixer.Channel(0)
player_rocket_sound = pygame.mixer.Sound(os.path.join("Sounds", "RPG_fire.mp3"))

expl_sounds = []
for i in range(2):
    expl_sounds.append(pygame.mixer.Sound(os.path.join("Sounds", f"Explode{i}.wav")))

pygame.mixer.music.load(os.path.join("Sounds", "Hey.mp3"))

#functions
font_name = pygame.font.match_font("arial")
def draw_text(surf, text, size, x, y):

    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)
    

def new_vics():
    vic = Vehicle()
    all_sprites.add(vic)
    other_vics.add(vic)
    
def draw_gas(surf, gas, x, y):
    if gas < 0:
        gas = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 15
    fill = (gas/30)*BAR_LENGTH
    outline_rect = pygame.Rect( x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, BLACK, outline_rect, 2)


#class
class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50,100))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT - 10
        self.gas = 30
        self.speedx = 8
        self.speedy = 8
    
    def shoot(self):
        rocket = Rocket(self.rect.centerx, self.rect.top)
        all_sprites.add(rocket)
        player_weapon.add(rocket)
        player_rocket_sound.play()

    
    def update(self):
        
        key_pressed = pygame.key.get_pressed()
            
        
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speedx
            if(player_turning.get_busy() == False):
                player_turning.play(turning_sound)
            
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx
            if(player_turning.get_busy() == False):
                player_turning.play(turning_sound)
            
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
            self.image = pygame.transform.scale(random.choice(otherVic_imgs), (50, 100))
            self.image.set_colorkey(BLACK)
            
            
class Rocket(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(RPG_rocket, (6,60))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -15
    
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = expl_anim[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
        
    
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(expl_anim):
                self.kill()
            else:
                self.image = expl_anim[self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center
        
    

all_sprites = pygame.sprite.Group()
other_vics = pygame.sprite.Group()
player_weapon = pygame.sprite.Group()

player = Player()
all_sprites.add(player)


for i in range(3):
    clock.tick(1)
    new_vics()


#game loop

pygame.mixer.music.play()

running = True
score = 0

while running:
    
    clock.tick(FPS)
    score += 0.1
    
    
    #gas consumption
    player.gas -= 0.015
    if(player.gas <= 0):
        running = False
    
    #Player collide with vehicle
    player_crash = pygame.sprite.spritecollide(player, other_vics, True)
    
    for crash in player_crash:
        new_vics()
    
    #Weapon destory vehicle
    weapon_destroy = pygame.sprite.groupcollide(player_weapon, other_vics, True, True)
    
    for boom in weapon_destroy:
        new_vics()
        random.choice(expl_sounds).play()
        expl = Explosion(boom.rect.center)
        all_sprites.add(expl)
    
    
    #input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LCTRL:
                player.shoot()
            
    
    #game update
    all_sprites.update()
    
    
    
    #display
    screen.fill(WHITE)
    all_sprites.draw(screen)
    draw_gas(screen, player.gas, 10, 10)
    draw_text(screen, str(int(score)), 18, WIDTH/2, 10)
    pygame.display.update()


pygame.quit()