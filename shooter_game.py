#Создай собственный Шутер!
from pygame import *
from random import randint

# вынесем размер окна в константы для удобства
# W - width, ширина
# H - height, высота
WIN_W = 700
WIN_H = 500
UFOS = 7
x1 = 100
y1 = 325
x2 = 100
y2 = 200
size  = 100
step = 4
FPS = 60
w = 100
h = 100
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BELI = (255 , 255 , 255)
piupiu = 


mixer.init()
mixer.music.load('space.ogg')
mixer.music.play(-1)
mixer.music.set_volume(0.25)


font.init()
title_font = font.SysFont('papyrus' , 60)

win = title_font.render('Ура ! вы устроили геноци!' ,True , GREEN)
lost = title_font.render('ахахаха проиграл )))' ,True , RED)

label_font = font.SysFont('papyrus' , 30)

count_txt = label_font.render('Убито :' ,True , BELI)
missed_txt = label_font.render('Пропущено:' ,True , BELI)

class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, w, h):
        super().__init__()
        self.image = transform.scale(
            image.load(img),
            # здесь - размеры картинки
            (w, h)
        )
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(GameSprite):
    def __init__(self, img, x, y, w, h , speed = step):
        super().__init__(img, x, y, w, h )
        self.speed = speed

    def update(self) :
        if self.rect.y >= WIN_H:
            self.kill()
        self.rect.y -= self.speed

class Playr(GameSprite):
    def __init__(self, img, x, y, w, h , speed = step):
        super().__init__(img, x, y, w, h )
        self.speed = speed 
        self.shot  = 0
        self.missed = 0
        self.bullets = sprite.Group()

    def update(self , up , down , left , right )  :
        key_pressed = key.get_pressed()
        if key_pressed[left] and self.rect.x > 5:
            self.rect.x -= step

        if key_pressed[right] and self.rect.x < WIN_W - size:
            self.rect.x += step

        if key_pressed[up] and self.rect.y > 5:
            self.rect.y -= step

        if key_pressed[down] and self.rect.y < WIN_H - size:
            self.rect.y += step

    def fire(self) :
        bullet = Bullet('bullet.png' , self.rect.x + self.rect.width / 2, self.rect.y , 15 ,25)
        self.bullets.add(bullet)

class Enemy(GameSprite):
    def __init__(self, img, x, y, w, h , speed = step):
        super().__init__(img, x, y, w, h )
        self.speed = speed
        self.rect.x = randint(0 , WIN_W-self.rect.width)
        self.rect.y = randint(0 , 40 )

    def update(self, rocket) :
        if self.rect.y >= WIN_H:
            rocket.missed += 1
            self.rect.x = randint(0 , WIN_W-self.rect.width)
            self.rect.y = randint(0 , 40 )
        self.rect.y += self.speed

# создание окна размером 700 на 500
window = display.set_mode((WIN_W, WIN_H))

# название окна
display.set_caption("Догонялки")
clock = time.Clock()

# задать картинку фона такого же размера, как размер окна
background = GameSprite('galaxy.jpg' , 0, 0, WIN_W , WIN_H)

rocket = Playr('rocket.png', x1 ,y1 , size ,size*1.75)

ufos = sprite.Group()
for i in range(UFOS):
    ufo = Enemy('ufo.png', 0, 0, 70 ,50)
    ufos.add(ufo)

bullet_vs_nigers = sprite.groupcollide(
    ufos , rocket.bullets , True , True
)
#treasure = GameSprite('treasure.png', 400 ,400 , size ,size)


# игровой цикл

game = True
finish = False
while game:
    for e in event.get():
        # выйти, если нажат "крестик"
        if e.type == QUIT:
            game = False

        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                rocket.fire()
    if not finish:
        if sprite.spritecollide(rocket , ufos , False):
            finish = True

        background.draw(window)

        count = label_font.render(str(rocket.shot) ,True , BELI)
        missed = label_font.render(str(rocket.missed) ,True , BELI)

        window.blit(count_txt ,(10 ,10))
        window.blit(count ,(150 ,10))
        window.blit(missed_txt ,(10 ,30))
        window.blit(missed ,(150 ,30))

        rocket.draw(window)
        ufos.draw(window)

        ufos.update(rocket)
        rocket.update(K_w , K_s, K_a , K_d )

        rocket.bullets.draw(window)
        rocket.bullets.update()

        collisions = sprite.groupcollide(
        ufos , rocket.bullets , True , True
    )

        for collision in collisions:
            rocket.shot += 1
            ufo = Enemy('ufo.png', 0, 0, 70 ,50)
            ufos.add(ufo)

        if rocket.shot > 9:
            window.blit(win, (100, 200))
            finish = True

        if rocket.missed > 39:
            window.blit(win, (100, 200))
            finish = True

        if sprite.spritecollide(rocket, ufos, False):
                window.blit(lost, (100, 200))
                display.update()
                finish = True
        # отобразить картинку фона

    # слушать события и обрабатывать
    # обновить экран, чтобы отобрзить все изменения
    display.update()
    clock.tick(FPS)

#создай окно игры

#задай фон сцены

#создай 2 спрайта и размести их на сцене

#обработай событие «клик по кнопке "Закрыть окно"»