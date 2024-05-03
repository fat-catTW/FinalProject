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

#Random vehicle position
RandomVicXPos1 = [80, 140, 200, 260, 320, 380]
RandomVicXPos2 = [[80, 140],[80, 200], [80, 260], [80, 320], [80, 380], [140, 200], [140, 260], [140, 320], [140, 380], [200, 260], [200, 320], [200, 380], [260, 320], [260, 380],
                   [320, 380]]
RandomVicXPos3 = [[80, 140, 200], [80, 140, 260], [80, 140, 320], [80, 140, 380],
                  [80, 200, 260], [80, 200, 320], [80, 200, 380],
                  [80, 260, 320], [80, 260, 380],
                  [80, 320, 380],
                  [140, 200, 260], [140, 200, 320], [140, 200, 380], 
                  [140, 260, 320], [140, 260, 380],
                  [140, 320, 380],
                  [200, 260, 320], [200, 260, 380],
                  [200, 320, 380],
                  [260, 320, 380]]


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

RandomBox_img = pygame.image.load(os.path.join("img", "RandomBox.png")).convert()

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


player_get_RPG_sound = pygame.mixer.Sound(os.path.join("Sounds", "RocketLauncher.mp3"))
player_get_RPG_sound.set_volume(0.8)

expl_sounds = []
for i in range(2):
    expl_sounds.append(pygame.mixer.Sound(os.path.join("Sounds", f"Explode{i}.wav")))

pygame.mixer.music.load(os.path.join("Sounds", "Hey.mp3"))

#functions
font_name = pygame.font.match_font("arial")#setting 
def draw_text(surf, text, size, x, y):

    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)
    

def new_vics(x):
    vic = Vehicle(x)
    all_sprites.add(vic)
    other_vics.add(vic)


def new_RandomBox(x):
    RB = RandomBox(x)
    all_sprites.add(RB)
    RandomBox_sprites.add(RB)


    
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
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(random.choice(otherVic_imgs), (50, 100))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = random.randrange(-180, -150)
        self.speedy = 5
    
    def update(self):
        self.rect.y += self.speedy
        
        if self.rect.top > HEIGHT + 100:
            self.kill()
            

class RandomBox(pygame.sprite.Sprite):
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(RandomBox_img, (40,40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = -180
        self.speedy = 5
    
    def update(self):
        self.rect.y += self.speedy
        
        if self.rect.top > HEIGHT + 100:
            self.kill()



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
RandomBox_sprites = pygame.sprite.Group()

player = Player()
all_sprites.add(player)



#game loop

pygame.mixer.music.play()

running = True
score = 0

spawnVicTimer1 = 3000
spawnVicTimer2 = 4500
last_now1 = pygame.time.get_ticks()
last_now2 = pygame.time.get_ticks()

spawnRandBoxTimer = 2000
RandomBox_last_spawn = pygame.time.get_ticks()

while running:
    
    clock.tick(FPS)
    now = pygame.time.get_ticks()
    score += 0.1
    
    #spawn vic

    if now - last_now1 >= spawnVicTimer1: #spawn one vehicle
        x = random.choice(RandomVicXPos1)
        new_vics(x)
        last_now1 = now

    if now - last_now2 >= spawnVicTimer2: #spawn mutiple vehicle

        spawn = random.randint(2,3)

        match spawn:
            case 2:
                tempList = random.choice(RandomVicXPos2)
                last_now2 = now
                for x in tempList:
                    new_vics(x)
            
            case 3:
                tempList = random.choice(RandomVicXPos3)
                last_now2 = now
                for x in tempList:
                    new_vics(x)

    #spawn RandomBox
    if now - RandomBox_last_spawn >= spawnRandBoxTimer:
        x = random.choice(RandomVicXPos1)
        new_RandomBox(x)
        RandomBox_last_spawn = now

    
    #gas consumption
    player.gas -= 0.015
    if(player.gas <= 0):
        running = False
    
    #Player collide with vehicle
    player_crash = pygame.sprite.spritecollide(player, other_vics, True)
    
    for crash in player_crash:
        random.choice(expl_sounds).play()
        expl = Explosion(crash.rect.center)
        all_sprites.add(expl)
    
    #Player collide with randomBox
    player_hit_RandomBox = pygame.sprite.spritecollide(player, RandomBox_sprites, True)

    for hits in player_hit_RandomBox:
        player_get_RPG_sound.play()


    #Weapon destory vehicle
    weapon_destroy = pygame.sprite.groupcollide(player_weapon, other_vics, True, True)
    
    for boom in weapon_destroy:
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