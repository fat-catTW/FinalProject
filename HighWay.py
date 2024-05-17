import pygame
import os
import random
import time
import sys

WIDTH = 500
HEIGHT = 700
FPS = 100
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

#Random vehicle position
RandomVicXPos1 = [100, 160, 223, 284, 343]
RandomVicXPos2 = [[100, 160],[100, 223], [100, 284], [100, 343], [160, 223], [160, 284], [160, 343], [223, 284], [223, 343], [284, 343]]
RandomVicXPos3 = [[100, 160, 223], [100, 160, 284], [100, 160, 343],
                  [100, 223, 284], [100, 223, 343],
                  [100, 284, 343], 
                  [160, 223, 284], [160, 223, 343], 
                  [160, 284, 343],
                  [223, 284, 343]]

RandomBoxXPos1 = [105, 165, 228, 289, 348]


#game init
pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(10)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("BR-116")
accelerate = 0.0


#load image
player_img = pygame.image.load(os.path.join("img", "player.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (6, 12))
player_mini_img.set_colorkey(BLACK)
pygame.display.set_icon(player_mini_img)

player_onFire_ani = []
for i in range(12):
    onFire_img = pygame.image.load(os.path.join("img", f"onFire_{i}.png")).convert()
    onFire_img.set_colorkey(BLACK)
    player_onFire_ani.append(pygame.transform.scale(onFire_img, (60, 60)))


player_BubbleShield = pygame.image.load(os.path.join("img", "BubbleShield.png")).convert()
player_BubbleShield.set_colorkey(BLACK)

otherVic_imgs = []
for i in range(7):
    otherVic_imgs.append(pygame.image.load(os.path.join("img", f"Vic{i}.png")).convert())

RandomBox_img = pygame.image.load(os.path.join("img", "RandomBox.png")).convert()

RPG_rocket = pygame.image.load(os.path.join("img", "RPG.png")).convert()
RPG_rocket.set_colorkey(BLACK)
RPG_remain3 = pygame.transform.scale(pygame.image.load(os.path.join("img", "RPG_3.png")).convert(), (30, 30))
RPG_remain2 = pygame.transform.scale(pygame.image.load(os.path.join("img", "RPG_2.png")).convert(), (30, 30))
RPG_remain1 = pygame.transform.scale(pygame.image.load(os.path.join("img", "RPG_1.png")).convert(), (30, 30))
RPG_remain3.set_colorkey(BLACK)
RPG_remain2.set_colorkey(BLACK)
RPG_remain1.set_colorkey(BLACK)


expl_anim = []
for i in range(9):
    expl_img = pygame.image.load(os.path.join("img", f"expl{i}.png")).convert()
    expl_img.set_colorkey(BLACK)
    expl_anim.append(pygame.transform.scale(expl_img, (90, 90)))

roadblock_img = []
for i in range(4):
    road_block = pygame.image.load(os.path.join("img", f"roadblock{i}.png")).convert()
    road_block.set_colorkey(BLACK)
    roadblock_img.append(road_block)

HP_img = pygame.image.load(os.path.join("img", "hp.png")).convert()
HP_img = pygame.transform.scale(HP_img, (20, 20))
HP_img.set_colorkey((192, 192, 192))

coin_img = pygame.image.load(os.path.join("img", "GoldCoin.jpg")).convert()
coin_img.set_colorkey(BLACK)

danger_sign_img = pygame.transform.scale(pygame.image.load(os.path.join("img", "Danger.png")).convert(),(50,50))
danger_sign_img.set_colorkey(WHITE)

opp_img = []
for i in range(5):
    opposite_rider = pygame.image.load(os.path.join("img", f"oppRider{i}.png")).convert()
    opposite_rider.set_colorkey(GREEN)
    opp_img.append(opposite_rider)

background_imgs = []
for i in range(3):
    background_imgs.append(pygame.image.load(os.path.join("img", f"background{i}.png")).convert())

background_img = random.choice(background_imgs)

#load sound
turning_sound = pygame.mixer.Sound(os.path.join("Sounds", "CarTurn.mp3"))
turning_sound.set_volume(0.1)
player_turning = pygame.mixer.Channel(0)

player_rocket_sound = pygame.mixer.Sound(os.path.join("Sounds", "RPG_fire.mp3"))
player_NoAmmo_sound = pygame.mixer.Sound(os.path.join("Sounds", "AmmoEmpty.mp3"))


player_get_RPG_sound = pygame.mixer.Sound(os.path.join("Sounds", "RocketLauncher.mp3"))
player_get_RPG_sound.set_volume(0.8)

player_get_shield_sound = pygame.mixer.Sound(os.path.join("Sounds", "BigBoy.mp3"))
player_get_shield_sound.set_volume(0.8)
shield_BigBoy_sound = pygame.mixer.Channel(1)

expl_sounds = []
for i in range(2):
    expl_sounds.append(pygame.mixer.Sound(os.path.join("Sounds", f"Explode{i}.wav")))

onFire_scream_sound = []
for i in range(7):
    onFire_scream_sound.append(pygame.mixer.Sound(os.path.join("Sounds", f"onFire{i}.wav")))

pygame.mixer.music.load(os.path.join("Sounds", "Hey.mp3"))

hp_gain_sound = pygame.mixer.Sound(os.path.join("Sounds", "hpGain.mp3"))

get_coin_sound = pygame.mixer.Sound(os.path.join("Sounds", "GetCoin.mp3"))
get_coin_sound.set_volume(0.1)

Danger_sound = pygame.mixer.Sound(os.path.join("Sounds", "Danger.mp3"))

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
    normal_obstacles.add(vic)
    all_obstacles.add(vic)

def new_RandomBox(x):
    RB = RandomBox(x)
    all_sprites.add(RB)
    RandomBox_sprites.add(RB)

def new_Coin(x):
    C = GoldCoin(x)
    all_sprites.add(C)
    coin_sprites.add(C)

def new_Shield():
    shield = Player_Shield()
    all_sprites.add(shield)
    player_shield.add(shield)

def play_onFire():
    fire = Player_onFire()
    all_sprites.add(fire)
    
def new_roadblock(x):
    rdb = Roadblocks(x)
    all_sprites.add(rdb)
    road_blocks.add(rdb)
    normal_obstacles.add(rdb)
    all_obstacles.add(rdb)
    
def new_oppsiteRider():
    opp = OppositeRider()
    all_sprites.add(opp)
    other_vics.add(opp)
    opposite_riders.add(opp)
    all_obstacles.add(opp)
    
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
    
def draw_hp(surf, hp):
    if hp > 3:
        hp = 3
    
    if hp == 3:
        surf.blit(HP_img, (WIDTH - 50, 10))
        surf.blit(HP_img, (WIDTH - 75, 10))
        surf.blit(HP_img, (WIDTH - 100, 10))
        
    elif hp == 2:
        surf.blit(HP_img, (WIDTH - 50, 10))
        surf.blit(HP_img, (WIDTH - 75, 10))
        
    elif hp == 1:
        surf.blit(HP_img, (WIDTH - 50, 10))

def draw_DangerSign(surf):
    surf.blit(danger_sign_img, (225, 300))

def draw_RocketAmmo(surf, ammo):
    if ammo == 3:
        surf.blit(RPG_remain3, (10, 30))
    
    if ammo == 2:
        surf.blit(RPG_remain2, (10, 30))
        
    if ammo == 1:
        surf.blit(RPG_remain1, (10, 30))
        

    
    


#class
class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50,100))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT - 10
        self.gas = 3000
        self.speedx = 8
        self.speedy = 8
    
    def shoot(self, ammo):

        if ammo > 0:
            rocket = Rocket(self.rect.centerx, self.rect.top)
            all_sprites.add(rocket)
            player_weapon.add(rocket)
            player_rocket_sound.play()
        else:
            player_NoAmmo_sound.play()

    
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

class Player_Shield(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_BubbleShield, (120,120))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = player.rect.centerx
        self.rect.centery = player.rect.centery
        self.spawn_time = pygame.time.get_ticks()
        self.duration = 8000

        pygame.mixer.music.set_volume(0)
        if shield_BigBoy_sound.get_busy() == True:
            shield_BigBoy_sound.stop()
        shield_BigBoy_sound.play(player_get_shield_sound)

    
    def update(self):
        self.rect.centerx = player.rect.centerx
        self.rect.centery = player.rect.centery
        now = pygame.time.get_ticks()
        if now - self.spawn_time >= self.duration:
            if shield_BigBoy_sound.get_busy() == False:
                pygame.mixer.music.set_volume(1)
            self.kill()

class Player_onFire(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_onFire_ani[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = player.rect.centerx
        self.rect.centery = player.rect.centery - 50
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
        
    
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(player_onFire_ani):
                self.frame = 0
        self.image = player_onFire_ani[self.frame]
        self.rect.centerx = player.rect.centerx
        self.rect.centery = player.rect.centery - 50

        
        if(hp > 1):
            self.kill()
            


class Vehicle(pygame.sprite.Sprite):
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(random.choice(otherVic_imgs), (50, 100))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = random.randrange(-180, -150)
        self.speedy = 2
    
    def update(self):
        self.rect.y += self.speedy + accelerate
        
        if self.rect.top > HEIGHT + 100:
            self.kill()
            

class RandomBox(pygame.sprite.Sprite):
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(RandomBox_img, (40,40))
        self.type = random.choice(["RPG", "Shield", "Health"])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = -180
        self.speedy = 4
    
    def update(self):
        self.rect.y += self.speedy +accelerate
        
        if self.rect.top > HEIGHT + 100:
            self.kill()

class GoldCoin(pygame.sprite.Sprite):
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(coin_img, (30,30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = -180
        self.speedy = 4
    
    def update(self):
        self.rect.y += self.speedy +accelerate
        
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
        
        
class Roadblocks(pygame.sprite.Sprite):
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(random.choice(roadblock_img), (50, 100))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = 0
        self.speedy = 3     #路障的初始速度(因為在道路上靜止，所以相對來說速度更快)
    
    def update(self):
        self.rect.y += self.speedy + accelerate
        
        if self.rect.top > HEIGHT + 100:
            self.kill()
            
            
class OppositeRider(pygame.sprite.Sprite): 
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(random.choice(opp_img), (50, 80))
        self.image.set_colorkey(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH)
        self.rect.bottom = 0
        self.speedy = 3
        self.p1 = random.randint(0, 2)
        self.p2 = random.randint(0, 2)
        

    
    def update(self):
        self.rect.y += self.speedy + accelerate
        x = random.random()
        if x < 0.1*self.p1 :
            self.rect.x += 10
        elif x < 0.2*self.p2:
            self.rect.x -= 10
        else:
            self.rect.x += 0
        
        if self.rect.top > HEIGHT + 80:
            self.kill()
            
        if self.rect.x > WIDTH - 45:
            self.rect.x = WIDTH - 45
        elif self.rect.x < 45:
            self.rect.x = 45
    

all_sprites = pygame.sprite.Group()
normal_obstacles = pygame.sprite.Group()
all_obstacles = pygame.sprite.Group()
other_vics = pygame.sprite.Group()
opposite_riders = pygame.sprite.Group()
player_weapon = pygame.sprite.Group()
player_shield = pygame.sprite.Group()
RandomBox_sprites = pygame.sprite.Group()
road_blocks = pygame.sprite.Group()
coin_sprites = pygame.sprite.Group()

player = Player()
all_sprites.add(player)



#game loop

pygame.mixer.music.play()

running = True
running_start_time = pygame.time.get_ticks()
score = 0
score_increament = 0

rocket_ammo = 0
hp = 3
is_onFire = 0

spawnVicTimer1 = 3000
spawnVicTimer2 = 4500
last_now1 = pygame.time.get_ticks()
last_now2 = pygame.time.get_ticks()

spawnRandBoxTimer = 2000
RandomBox_last_spawn = pygame.time.get_ticks()

spawnCoinTimer = 1000
Coin_last_spawn = pygame.time.get_ticks()

genRoadblockTimer = 1500
last_Roadblocks = pygame.time.get_ticks()

genOppRiderTimer = 10000
last_oppositeRider = pygame.time.get_ticks()

dangerSignTimer = 1000
start_dangerSign = pygame.time.get_ticks()
danger = False

while running:
    
    clock.tick(FPS)
    now = pygame.time.get_ticks()
    score += 0.1
    score_increament += 1
    
    #speed up
    if(score_increament >= 15 * FPS):
        accelerate += 1
        score_increament = 0
    
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
        x = random.choice(RandomBoxXPos1)
        new_RandomBox(x)
        RandomBox_last_spawn = now
        
    #generate roadblocks
    if now - last_Roadblocks >= genRoadblockTimer:
        x = random.randint(1, 3)
        
        if x == 1:  #generate roadblock on the left side
            new_roadblock(0)
            last_Roadblocks = now
        
        elif x == 2:
            new_roadblock(WIDTH - 50)   #generate roadblock on the right side
            last_Roadblocks = now
            
        else:   #not generate roadblock
            last_Roadblocks = now
            
    #generate opposite rider
    if accelerate > 0 and now - last_oppositeRider >= genOppRiderTimer/accelerate:
        new_oppsiteRider()
        last_oppositeRider = now        
        danger = True
        Danger_sound.play()
        start_dangerSign = pygame.time.get_ticks()
            
    #spawn GoldCoin
    if now - Coin_last_spawn >= spawnCoinTimer:
        x = random.choice(RandomBoxXPos1)
        new_Coin(x)
        Coin_last_spawn = now
            
    #gas consumption
    player.gas -= 0.015
    if(player.gas <= 0):
        running = False
        
    
    #Player collide with vehicles, roadblocks, and opposite riders
    player_crash = pygame.sprite.spritecollide(player, all_obstacles, True)
    
    for crash in player_crash:
        random.choice(expl_sounds).play()
        expl = Explosion(crash.rect.center)
        all_sprites.add(expl)
        hp -= 1
    
    #Player collide with randomBox
    player_hit_RandomBox = pygame.sprite.spritecollide(player, RandomBox_sprites, True)
    
    for hits in player_hit_RandomBox:
        if hits.type == "RPG":
            rocket_ammo = 3
            player_get_RPG_sound.play()
        
        if hits.type == "Shield":
            new_Shield()
            
        if hits.type == "Health":
            if hp < 3:
                hp += 1
            hp_gain_sound.play()
    
    #Player get a coin
    player_get_coin = pygame.sprite.spritecollide(player, coin_sprites, True)
    for get in player_get_coin:
        get_coin_sound.play()
        score += 100

    #hp check
    if(hp < 2 and is_onFire == 0):
        is_onFire = 1
        random.choice(onFire_scream_sound).play()
        play_onFire()

    if(hp > 1):
        is_onFire = 0

    if(hp <= 0):
        running = False

    #RPG destory vehicle
    weapon_destroy = pygame.sprite.groupcollide(other_vics, player_weapon, True, True)
    
    for boom in weapon_destroy:
        random.choice(expl_sounds).play()
        expl = Explosion(boom.rect.center)
        all_sprites.add(expl)

    weapon_destroy = pygame.sprite.groupcollide(road_blocks, player_weapon, True, True)
    
    for boom in weapon_destroy:
        random.choice(expl_sounds).play()
        expl = Explosion(boom.rect.center)
        all_sprites.add(expl)
    
    #Shield destroy vehicle
    shield_destroy = pygame.sprite.groupcollide(other_vics, player_shield, True, False)
    for boom in shield_destroy:
        random.choice(expl_sounds).play()
        expl = Explosion(boom.rect.center)
        all_sprites.add(expl)
        
    shield_destroy = pygame.sprite.groupcollide(road_blocks, player_shield, True, False)
    for boom in shield_destroy:
        random.choice(expl_sounds).play()
        expl = Explosion(boom.rect.center)
        all_sprites.add(expl)
    
    #Opposite rider collide with other vehicles and roadblocks
    opp_crash = pygame.sprite.groupcollide(opposite_riders, normal_obstacles, True, True)

    for crash in opp_crash:
        random.choice(expl_sounds).play()
        expl = Explosion(crash.rect.center)
        all_sprites.add(expl)

    #input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LCTRL:
                player.shoot(rocket_ammo)
                rocket_ammo -= 1
            
    
    #game update
    all_sprites.update()
    
    
    
    #display
    screen.fill(WHITE)
    screen.blit(background_img, (0, 0))
    all_sprites.draw(screen)
    draw_gas(screen, player.gas, 10, 10)
    draw_text(screen, str(int(score)), 18, WIDTH/2, 10)
    draw_hp(screen, hp)
    draw_RocketAmmo(screen, rocket_ammo)
    
        
    
    if now - start_dangerSign < dangerSignTimer and now - running_start_time > 5000:
        draw_DangerSign(screen)

    pygame.display.update()


pygame.quit()