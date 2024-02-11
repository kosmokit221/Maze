#створи гру "Лабіринт"!
from random import choice
from pygame import *
mixer.init()
font.init()

#створи вікно гри
TILESIZE = 45
MAP_WIDTH, MAP_HEIGHT = 19, 15
WIDTH, HEIGHT = TILESIZE*MAP_WIDTH , TILESIZE*MAP_HEIGHT
window = display.set_mode((WIDTH, HEIGHT))
FPS = 60

font1 = font.SysFont("Arial", 40)
font2 = font.SysFont("Arial", 50)



mixer.music.load("jungles.ogg")
mixer.music.set_volume(0.2)
mixer.music.play(loops=-1)

#kick_sound = mixer.Sound('kick.ogg')
#kick_sound.play()


display.set_caption("Лабіринт")
clock = time.Clock() #Стоворюємо ігровий таймер
#задай фон сцени
bg = image.load("background.jpg")
bg = transform.scale(bg, (WIDTH, HEIGHT))
player_img = image.load('hero.png')
enemy_img = image.load('cyborg.png')
wall_img = image.load('wall.png')
treasure_img = image.load('treasure.png')

#створи 2 спрайти та розмісти їх на сцені
sprites = sprite.Group()
class GameSprite(sprite.Sprite):
    def __init__(self, sprite_image, width, height, x, y):
        super().__init__()
        self.image = transform.scale(sprite_image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        sprites.add(self)

    def draw(self, window):
        window.blit(self.image, self.rect)

class Player(GameSprite):
    def __init__(self, sprite_image, width, height, x, y):
        super().__init__(sprite_image, width, height, x, y)   
        self.hp = 100
        self.damage = 20
        self.points = 0
        self.speed = 5
    

    def update(self):
        global hp_text
        self.old_pos = self.rect.x, self.rect.y

        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
        if keys[K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.right < WIDTH:
            self.rect.x += self.speed

        collidelist = sprite.spritecollide(self, walls, False)
        if len(collidelist) > 0:
            self.rect.x, self.rect.y = self.old_pos
        
        collidelist = sprite.spritecollide(self, enemys, False)
        if len(collidelist) >0:
            self.hp -= 20
            hp_text = font1.render(f"HP:{self.hp}", True, (255,255,255))
            self.rect.x, self.rect.y = self.start_x, self.start_y
            

        

enemys = sprite.Group()
class Enemy(GameSprite):
    def __init__(self, x, y):
        super().__init__(enemy_img,TILESIZE, TILESIZE, x, y)
        self.hp = 100
        self.damage = 20
        self.speed = 5
        self.dir_list = ['left', 'right','up','down']
        self.dir = choice(self.dir_list)
        enemys.add(self)

    def update(self):
        self.old_pos = self.rect.x, self.rect.y
        if self.dir == 'right':
            self.rect.x += self.speed
        elif self.dir == 'left':
            self.rect.x -= self.speed
        elif self.dir == 'up':
            self.rect.y -= self.speed
        elif self.dir == 'down':
            self.rect.y += self.speed

        collidelist = sprite.spritecollide(self, walls, False)
        if len(collidelist) > 0:
            self.rect.x, self.rect.y = self.old_pos
            self.dir = choice(self.dir_list)

walls = sprite.Group()
class Wall(GameSprite):
    def __init__(self, x, y):
        super().__init__(wall_img, TILESIZE, TILESIZE, x, y)
        walls.add(self)

player = Player(player_img, TILESIZE, TILESIZE, 300, 300)

with open("map.txt", "r") as file:
    x,y = 0,0
    map = file.readlines()
    for row in map:
        for symbol in row:
            if symbol == 'w':
                Wall(x,y)
            elif symbol == 'E':
                Enemy(x,y)
            elif symbol == 'P':
                player.rect.x = x
                player.rect.y = y
                player.start_x, player.start_y = x,y
            elif symbol == "T":
                GameSprite(treasure_img, TILESIZE, TILESIZE, x,y)
            x += TILESIZE
        y+= TILESIZE
        x = 0


hp_text = font1.render(f"HP:{player.hp}", True, (255,255,255))
finish_text = font2.render("GAME OVER", True, (255,0,0))
finish = False

while True:
#оброби подію «клік за кнопкою "Закрити вікно"»
    for e in event.get():
        if e.type == QUIT:
            quit()
    if not finish:
        player.update()
        enemys.update()
    window.blit(bg, (0,0))
    sprites.draw(window)
    window.blit(hp_text, (10,10))
    if player.hp <= 0:
        finish = True
    if finish:
        window.blit(finish_text, (300,250))
    display.update()
    clock.tick(FPS)


        

