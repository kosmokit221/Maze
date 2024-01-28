#створи гру "Лабіринт"!
from pygame import *
mixer.init()

#створи вікно гри
WIDTH, HEIGHT = 800, 650
window = display.set_mode((WIDTH, HEIGHT))
FPS = 60

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

#створи 2 спрайти та розмісти їх на сцені
class GameSprite(sprite.Sprite):
    def __init__(self, sprite_image, width, height, x, y):
        super().__init__()
        self.image = transform.scale(sprite_image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

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
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
        if keys[K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.right < WIDTH:
            self.rect.x += self.speed

player = Player(player_img, 50, 50, 300, 300)

while True:
#оброби подію «клік за кнопкою "Закрити вікно"»
    for e in event.get():
        if e.type == QUIT:
            quit()
    player.update()
    window.blit(bg, (0,0))
    player.draw(window)
    display.update()
    clock.tick(FPS)

        

