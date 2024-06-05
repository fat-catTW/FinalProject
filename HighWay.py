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
ROADBLOCK_FILTER = (160, 32, 240)
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
select_level = random.randint(0,2)
last_fuel_spawn = pygame.time.get_ticks()


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
    
animal_anim = []
for i in range(6):
    animal_img = pygame.image.load(os.path.join("img", f"animal{i}.png")).convert()
    animal_img.set_colorkey(BLACK)
    animal_anim.append(pygame.transform.scale(animal_img, (50, 120)))

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
for i in range(9):
    road_block = pygame.image.load(os.path.join("img", f"roadblockvv-{i}.png")).convert()
    road_block.set_colorkey(ROADBLOCK_FILTER)
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
    background_imgs.append(pygame.image.load(os.path.join("img", f"backgroundvv-{i}.png")).convert())

#load sound
turning_sound = pygame.mixer.Sound(os.path.join("Sounds", "CarTurn.mp3"))
turning_sound.set_volume(0.1)
player_turning = pygame.mixer.Channel(0)

player_rocket_sound = pygame.mixer.Sound(os.path.join("Sounds", "RPG_fire.mp3"))
player_NoAmmo_sound = pygame.mixer.Sound(os.path.join("Sounds", "AmmoEmpty.mp3"))


player_get_RPG_sound = pygame.mixer.Sound(os.path.join("Sounds", "RocketLauncher.mp3"))
player_get_RPG_sound.set_volume(0.8)

player_get_shield_sound = []
for i in range(2):
    temp = pygame.mixer.Sound(os.path.join("Sounds", f"BigBoy{i}.mp3"))
    temp.set_volume(0.8)
    player_get_shield_sound.append(temp)
shield_BigBoy_sound = pygame.mixer.Channel(1)

expl_sounds = []
for i in range(2):
    expl_sounds.append(pygame.mixer.Sound(os.path.join("Sounds", f"Explode{i}.wav")))

onFire_scream_sound = []
for i in range(7):
    onFire_scream_sound.append(pygame.mixer.Sound(os.path.join("Sounds", f"onFire{i}.wav")))

pygame.mixer.music.load(os.path.join("Sounds", "BGM0.mp3"))
pygame.mixer.music.queue(os.path.join("Sounds", "BGM2.mp3"))

hp_gain_sound = pygame.mixer.Sound(os.path.join("Sounds", "hpGain.mp3"))

get_coin_sound = pygame.mixer.Sound(os.path.join("Sounds", "GetCoin.mp3"))
get_coin_sound.set_volume(0.1)

Danger_sound = pygame.mixer.Sound(os.path.join("Sounds", "Danger.mp3"))

get_gas_sound = pygame.mixer.Sound(os.path.join("Sounds", "getGas.mp3"))

main_menu_sound = pygame.mixer.Sound(os.path.join("Sounds", "main_menu.mp3"))
main_menu_sound.set_volume(0.8)

button_click_sound = pygame.mixer.Sound(os.path.join("Sounds", "select.mp3"))
button_click_sound.set_volume(0.8)

end_sound = pygame.mixer.Sound(os.path.join("Sounds", "end.wav"))
end_sound.set_volume(0.6)
end_play = pygame.mixer.Channel(3)


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
    all_sprites.add(vic, layer = 1)
    other_vics.add(vic)
    normal_obstacles.add(vic)
    all_obstacles.add(vic)

def new_RandomBox(x):
    RB = RandomBox(x)
    all_sprites.add(RB, layer = 2)
    RandomBox_sprites.add(RB)

def new_Coin(x):
    C = GoldCoin(x)
    all_sprites.add(C, layer = 2)
    coin_sprites.add(C)

def new_Shield():
    shield = Player_Shield()
    all_sprites.add(shield, layer = 2)
    player_shield.add(shield)

def play_onFire():
    fire = Player_onFire()
    all_sprites.add(fire, layer = 2)
    
def new_roadblock(x):
    rdb = Roadblocks(x)
    all_sprites.add(rdb, layer = 1)
    road_blocks.add(rdb)
    normal_obstacles.add(rdb)
    all_obstacles.add(rdb)
    
def new_oppsiteRider():
    opp = OppositeRider()
    all_sprites.add(opp, layer = 1)
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
        
def new_fuel_tank():
    x = random.choice([105, 165, 228, 289, 348])
    ft = FuelTank(x)
    all_sprites.add(ft, layer = 2)
    fuel_tank_sprites.add(ft)
    
def new_background(pos, img):
    bg = Background(pos, img)
    all_sprites.add(bg, layer = 0)
    
font_name = pygame.font.match_font("arial")#setting 
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("img/font.ttf", size)

def main_menu(mainmenu):
    pygame.mixer.music.stop()
    global accelerate, is_shield, update_score
    accelerate = 0
    is_shield = False
    update_score = False
    main_menu_sound.play()

    background_image = pygame.image.load(os.path.join("img", "BR-116Brazil.png")).convert()
    background_image = pygame.transform.scale(background_image, (500, 700))
    screen.blit(background_image, (0, 0))

    while (mainmenu != 0):
        MENU_MOUSE_POS = pygame.mouse.get_pos()
    
        MENU_TEXT = get_font(50).render("BR-116", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(250, 130))
    
        PLAY_BUTTON = Button(image=pygame.image.load("img/Play Rect.png"), pos=(250, 430), 
                            text_input="PLAY", font=get_font(25), base_color="White", hovering_color="#d7fcd4")
        QUIT_BUTTON = Button(image=pygame.image.load("img/Quit Rect.png"), pos=(250, 540), 
                            text_input="QUIT", font=get_font(25), base_color="White", hovering_color="#d7fcd4")
    
        screen.blit(MENU_TEXT, MENU_RECT)
    
        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
            
        running = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.mixer.stop()
                    return False, 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.mixer.stop()
                    button_click_sound.play()
                    pygame.time.delay(300) #delay time for clicking music display
                    return True, 1
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.mixer.stop()
                    button_click_sound.play()
                    pygame.time.delay(300) #delay time for clicking music display
                    return False, 0
        pygame.display.update()
        
def display_final_score(screen, score):
    if end_play.get_busy() == False:
        end_sound.play()
        
    scores = read_high_scores()
    
    rect_width = WIDTH - 60
    rect_height = 300
    rect_x = 30
    rect_y = HEIGHT / 2 - 150
    pygame.draw.rect(screen, (255, 242, 0), (rect_x, rect_y, rect_width, rect_height))
    
    draw_text(screen, f"SCORE: {int(score)}", 50, WIDTH / 2, HEIGHT / 2 - 115)
    
    i = 0
    for high_score in scores:
        if i == 0:
            draw_text(screen, f"1st: {high_score}", 20, WIDTH / 2, HEIGHT / 2 - 30)
        elif i == 1:
            draw_text(screen, f"2nd: {high_score}", 20, WIDTH / 2, HEIGHT / 2 + 10)
        elif i == 2:
            draw_text(screen, f"3rd: {high_score}", 20, WIDTH / 2, HEIGHT / 2 + 50)
        i += 1
        
    draw_text(screen, f"[PRESS ANY KEY TO RETURN TO THE MAIN MENU]", 20, WIDTH / 2, HEIGHT / 2 + 100)
    
    pygame.display.update()
    
def read_high_scores():
    with open('./high_scores.txt', 'r') as file:
        scores = [int(line.strip()) for line in file]
    return scores

def write_high_scores(scores):
    with open('./high_scores.txt', 'w') as file:
        for score in scores:
            file.write(f"{score}\n")

def update_high_scores(new_score):
    scores = read_high_scores()
    new_score = int(new_score)

    if scores == [0, 0, 0]:
        scores[0] = new_score
    else:
        if len(scores) < 3 or new_score > min(scores):
            scores.append(new_score)
            scores = sorted(scores, reverse=True)
            while len(scores) < 3:
                scores.append(0)
    
    write_high_scores(scores[:3])


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
    
    def shoot(self, ammo):

        if ammo > 0:
            rocket = Rocket(self.rect.centerx, self.rect.top)
            all_sprites.add(rocket, layer = 2)
            player_weapon.add(rocket)
            player_rocket_sound.play()
        else:
            player_NoAmmo_sound.play()
            
    def clean(self):
        self.kill()

    
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
        choose = random.choice(player_get_shield_sound)
        shield_BigBoy_sound.play(choose)
        
    def clean(self):
        self.kill()
    
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
        
    def clean(self):
        self.kill()
    
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
        self.appearance = random.random()
        if select_level == 2:
            self.appearance = 1
        if self.appearance < 0.03:
            self.init_frame = 0
            self.frame = self.init_frame
            self.image = animal_anim[self.init_frame]
        elif self.appearance < 0.06:
            self.init_frame = 2
            self.frame = self.init_frame
            self.image = animal_anim[self.init_frame]
        elif self.appearance < 0.09:
            self.init_frame = 4
            self.frame = self.init_frame
            self.image = animal_anim[self.init_frame]
        else:
            self.image = pygame.transform.scale(random.choice(otherVic_imgs), (50, 100))
            
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = random.randrange(-180, -150)
        self.speedy = 2
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 80
    
    def clean(self):
        self.kill()
    
    def update(self):
        self.rect.y += self.speedy + accelerate
        
        if self.rect.top > HEIGHT + 100:
            self.kill()
            
        if self.appearance < 0.09:    
            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_rate:
                self.last_update = now
                self.frame += 1
                
                if self.frame > self.init_frame + 1:
                    self.frame = self.init_frame
                    
                self.image = animal_anim[self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center
            
     
            

class RandomBox(pygame.sprite.Sprite):
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(RandomBox_img, (40,40))
        choose = random.random()
        if choose <= 0.2:
            self.type = "Shield"
        elif choose >= 0.2 and choose <=0.5:
            self.type = "Health" 
        elif choose > 0.5 and choose <= 0.8:
            self.type = "RPG"
        else:
            self.type = "Gas"
        #self.type = random.choice(["RPG", "Shield", "Health"])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = -180
        self.speedy = 4
        
    def clean(self):
        self.kill()
    
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
        
    def clean(self):
        self.kill()
    
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
        
    def clean(self):
        self.kill()
    
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
        
    def clean(self):
        self.kill()
        
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
        if select_level == 0:
            self.image = pygame.transform.scale(roadblock_img[random.randint(0,2)], (50, 60))
        if select_level == 1:
            self.image = pygame.transform.scale(roadblock_img[random.randint(3,5)], (50, 60))
        if select_level == 2:
            self.image = pygame.transform.scale(roadblock_img[random.randint(6,8)], (50, 60))

        #self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = 0
        self.speedy = 4     #路障的初始速度(因為在道路上靜止，所以相對來說速度更快)
        
    def clean(self):
        self.kill()
    
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
        self.rect.bottom = -3
        self.speedy = 3
        self.p1 = 0
        self.p2 = 0
        
        while self.p1 == 0 and self.p2 == 0:
            self.p1 = random.randint(0, 2)
            self.p2 = random.randint(0, 2)
        
    def clean(self):
        self.kill()
    
    def update(self):
        self.rect.y += self.speedy + accelerate
        x = random.random()
        if x < 0.15*self.p1 :
            self.rect.x += 10
        elif x < 0.3*self.p2:
            self.rect.x -= 10
        else:
            self.rect.x += 0
        
        if self.rect.top > HEIGHT + 80:
            self.kill()
            
        if self.rect.x > WIDTH - 50:
            self.rect.x = WIDTH - 50
        elif self.rect.x < 50:
            self.rect.x = 50
    
    
    
class FuelTank(pygame.sprite.Sprite):
    def __init__(self, x):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(os.path.join("img", "fuelbox.png")).convert(), (40, 40))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = -40
        self.speedy = 4
        
    def clean(self):
        self.kill()

    def update(self):
        self.rect.y += self.speedy + accelerate
        if self.rect.top > HEIGHT:
            self.kill()
            
            
            
class Background(pygame.sprite.Sprite): 
    def __init__(self, position, randImg):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(background_imgs[randImg], (WIDTH, HEIGHT*2))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.top = position
        self.speedy = 4
        
    def clean(self):
        self.kill()
    
    def update(self):
        self.rect.y += self.speedy + accelerate
        
        if self.rect.top > HEIGHT + HEIGHT:
            self.kill()
            
            
            
class BackgroundManager:
    def __init__(self, group, randFirstImg):
        self.sprite_group = group
        self.last_background = None
        self.nowImg = randFirstImg
        self.count = 0

    def generate_background(self):
        new_background = Background(HEIGHT*(-2), self.nowImg)
        self.sprite_group.add(new_background, layer = 0)
        self.last_background = new_background

    def update(self):
        global select_level
        if self.last_background is None or self.last_background.rect.top > -10:
            self.generate_background()
            self.count += 1
            
        if self.count == 4:
            self.count = 0
            self.nowImg = random.randint(0, 2)
            select_level = self.nowImg
            
            
            
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


all_sprites = pygame.sprite.LayeredUpdates()
normal_obstacles = pygame.sprite.Group()
all_obstacles = pygame.sprite.Group()
other_vics = pygame.sprite.Group()
opposite_riders = pygame.sprite.Group()
player_weapon = pygame.sprite.Group()
player_shield = pygame.sprite.Group()
RandomBox_sprites = pygame.sprite.Group()
road_blocks = pygame.sprite.Group()
coin_sprites = pygame.sprite.Group()
fuel_tank_sprites = pygame.sprite.Group()
expl_sprites = pygame.sprite.Group()




#game loop

player = Player()

mainmenu = 1
running = True

while (mainmenu != 0):
    running, mainmenu = main_menu(mainmenu)
    if running:
        pygame.mixer.stop()
        
        running_start_time = pygame.time.get_ticks()
        
        all_sprites.add(player, layer = 2) 
            
        score = 0
        score_increment = 0
        
        rocket_ammo = 0
        hp = 3
        is_onFire = 0
        
        spawnVicTimer = 1800
        last_vic = pygame.time.get_ticks()
        
        spawnRandBoxTimer = 2000
        RandomBox_last_spawn = pygame.time.get_ticks()
        
        spawnCoinTimer = 1000
        Coin_last_spawn = pygame.time.get_ticks()
        
        genRoadblockTimer = 1000
        last_Roadblocks = pygame.time.get_ticks()
        
        genOppRiderTimer = 10000
        last_oppositeRider = pygame.time.get_ticks()
        
        dangerSignTimer = 1000
        start_dangerSign = pygame.time.get_ticks()
        danger = False
        
        
        new_background(0, select_level)
        background_manager = BackgroundManager(all_sprites, select_level)

        player.image = pygame.transform.scale(player_img, (50,100))
        player.image.set_colorkey(BLACK)
        player.rect = player.image.get_rect()
        player.rect.centerx = WIDTH/2
        player.rect.bottom = HEIGHT - 10
        player.gas = 30
        player.speedx = 8
        player.speedy = 8
        
        
        pygame.mixer.music.play()

        while running:
            clock.tick(FPS)
            now = pygame.time.get_ticks()
            
            if hp > 0 and player.gas > 0:
                score += 0.1
                score_increment += 0.1
            
                #speed up
                if score_increment >= 500 * (1 + accelerate):
                    accelerate += 1
                    score_increment = 0
                
                #spawn vic
                if now - last_vic >= spawnVicTimer:
            
                    spawn = random.randint(1,3)
            
                    match spawn:
                        case 1:
                            x = random.choice(RandomVicXPos1)
                            last_vic = now
                            new_vics(x)
                        
                        case 2:
                            tempList = random.choice(RandomVicXPos2)
                            last_vic = now
                            for x in tempList:
                                new_vics(x)
                        
                        case 3:
                            tempList = random.choice(RandomVicXPos3)
                            last_vic = now
                            for x in tempList:
                                new_vics(x)
            
                #spawn RandomBox
                if now - RandomBox_last_spawn >= spawnRandBoxTimer:
                    if random.random() > 0.7:
                        x = random.choice(RandomBoxXPos1)
                        new_RandomBox(x)
                    RandomBox_last_spawn = now
                    
                #generate roadblocks
                if now - last_Roadblocks >= genRoadblockTimer:
                    x = random.randint(1, 3)
                    
                    if x == 1:  #generate roadblock on the left side
                        new_roadblock(20)
                        last_Roadblocks = now
                    
                    elif x == 2:
                        new_roadblock(WIDTH - 70)   #generate roadblock on the right side
                        last_Roadblocks = now
                        
                    else:   #not generate roadblock
                        last_Roadblocks = now
            
                if now - last_fuel_spawn > 10000:  #A tank is generated every 10 seconds, the time can be adjusted as needed
                    new_fuel_tank()
                    last_fuel_spawn = now
            
                #Detect player collisions with fuel tanks
                player_hit_fuel = pygame.sprite.spritecollide(player, fuel_tank_sprites, True)
                for fuel in player_hit_fuel:
                    player.gas = 30  #Assume 30 is the maximum value of player fuel
                    get_gas_sound.play()
                        
                #generate opposite rider
                if accelerate > 1 and now - last_oppositeRider >= genOppRiderTimer/accelerate:
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
                    
                #generate new background
                background_manager.update()
                        
                #gas consumption
                if hp > 0:
                    player.gas -= 0.015
                
                #Player collide with vehicles, roadblocks, and opposite riders
                player_crash = pygame.sprite.spritecollide(player, all_obstacles, True)
                
                for crash in player_crash:
                    random.choice(expl_sounds).play()
                    expl = Explosion(crash.rect.center)
                    all_sprites.add(expl, layer = 2)
                    expl_sprites.add(expl)
                    
                    if is_shield == False:
                        hp -= 1
                
                #Player collide with randomBox
                player_hit_RandomBox = pygame.sprite.spritecollide(player, RandomBox_sprites, True)
                
                for hits in player_hit_RandomBox:
                    if hits.type == "RPG":
                        rocket_ammo = 3
                        player_get_RPG_sound.play()
                    
                    if hits.type == "Shield":
                        new_Shield()
                        is_shield = True
                        
                    if hits.type == "Health":
                        if hp < 3:
                            hp += 1
                        hp_gain_sound.play()
                    if hits.type == "Gas":
                        player.gas = 30  
                        get_gas_sound.play()
                
                #Player get a coin
                player_get_coin = pygame.sprite.spritecollide(player, coin_sprites, True)
                for get in player_get_coin:
                    get_coin_sound.play()
                    score += 100
                    score_increment += 100
            
                #on fire statement
                if hp < 2 and is_onFire == 0:
                    is_onFire = 1
                    random.choice(onFire_scream_sound).play()
                    play_onFire()
            
                if hp > 1:
                    is_onFire = 0
            
                #RPG destory vehicle
                weapon_destroy = pygame.sprite.groupcollide(other_vics, player_weapon, True, True)
                
                for boom in weapon_destroy:
                    random.choice(expl_sounds).play()
                    expl = Explosion(boom.rect.center)
                    all_sprites.add(expl, layer = 2)
                    expl_sprites.add(expl)
            
                weapon_destroy = pygame.sprite.groupcollide(road_blocks, player_weapon, True, True)
                
                for boom in weapon_destroy:
                    random.choice(expl_sounds).play()
                    expl = Explosion(boom.rect.center)
                    all_sprites.add(expl, layer = 2)
                    expl_sprites.add(expl)
                
                #Shield destroy vehicle
                shield_destroy = pygame.sprite.groupcollide(other_vics, player_shield, True, False)
                for boom in shield_destroy:
                    random.choice(expl_sounds).play()
                    expl = Explosion(boom.rect.center)
                    all_sprites.add(expl)
                    expl_sprites.add(expl)
                    
                shield_destroy = pygame.sprite.groupcollide(road_blocks, player_shield, True, False)
                for boom in shield_destroy:
                    random.choice(expl_sounds).play()
                    expl = Explosion(boom.rect.center)
                    all_sprites.add(expl, layer = 2)
                    expl_sprites.add(expl)
                    
                #Shield statement check    
                if len(player_shield) == 0:
                    is_shield = False
                
                #Opposite rider collide with other vehicles and roadblocks
                opp_crash = pygame.sprite.groupcollide(opposite_riders, normal_obstacles, True, True)
            
                for crash in opp_crash:
                    random.choice(expl_sounds).play()
                    expl = Explosion(crash.rect.center)
                    all_sprites.add(expl, layer = 2)
                    expl_sprites.add(expl)
        
            #input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    mainmenu = 0
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LCTRL:
                        player.shoot(rocket_ammo)
                        rocket_ammo -= 1
                        
                    if hp <= 0 or player.gas <= 0:  #當hp<=0或gas<=0，遊戲結束，按任意鍵回到menu
                        #reset values
                        is_onFire = 0
                        rocket_ammo = 0
                        hp = 3
                        select_level = random.randint(0, 2)
                            
                        #delete all the sprites
                        for every in all_sprites:
                            every.clean()
                            
                        running = False
                    
            
            #game update
            if hp > 0 and player.gas > 0:
                all_sprites.update()
            else:
                pygame.mixer.music.stop()
                if update_score == False:
                    update_high_scores(score)
                    update_score = True
                
            
            #display
            if hp > 0 and player.gas > 0:
                screen.fill(BLACK)
                all_sprites.draw(screen)
                draw_gas(screen, player.gas, 10, 10)
                draw_text(screen, str(int(score)), 18, WIDTH/2, 10)
                draw_hp(screen, hp)
                draw_RocketAmmo(screen, rocket_ammo)
                
                if now - start_dangerSign < dangerSignTimer and now - running_start_time > 5000:
                    draw_DangerSign(screen)
                    
                pygame.display.update()
            else:
                screen.fill(BLACK)
                all_sprites.draw(screen)
                draw_gas(screen, player.gas, 10, 10)
                draw_hp(screen, hp)
                draw_RocketAmmo(screen, rocket_ammo)
                display_final_score(screen, score)
            
        pygame.mixer.stop()

pygame.quit()