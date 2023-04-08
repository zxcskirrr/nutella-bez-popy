from pygame import *

window = display.set_mode((700,500))
background = transform.scale(image.load('comnata.jpeg'),(700,500))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))    
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

bullets = sprite.Group()

class Player(GameSprite):
    # метод для управления спрайтом стрелками клавиатуры
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 700 - 80:
            self.rect.x += self.speed
    # метод "выстрел"
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 10)
        bullets.add(bullet)

# создайте стрельбу в игровом цикле при помощи пробела

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

score = 0
lost = 0

from random import *
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(10, 650)
            self.rect.y = -50
            lost += 1


class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.x = randint(10, 650)
            self.rect.y = -50




monsters = sprite.Group()
asteroids = sprite.Group()

for i in range(10):
    monster = Enemy('curtca.jpg', randint(50,650), randint(-350,0), 2)
    monsters.add(monster)
for i in range(3):
    asteroid = Asteroid('asteroid.png', randint(50,650), randint(-350,0), 2)
    asteroid.add(asteroids)

Hero = Player('mau.jpg', 350, 450, 5)

run = True

clock = time.Clock()
##################################################
# создаю шрифт
font.init()
font1 = font.Font(None, 36)
text_win = font1.render('you wiiiiin' , 1, (255,255,255))
text_looooooze = font1.render('ti balbes neobrazovany' , 1, (255,255,255))

beg = True
# создаю надписи

# самостоятельно, найдите как отрисовать надписи

while run:

    text_score = font1.render('Счет: ' + str(score), 1, (255,255,255))
    text_lost = font1.render('Пропустил: ' + str(lost), 1, (255,255,255))

    window.blit(background, (0,0))
    window.blit(text_score, (0,0))
    window.blit(text_lost, (0,50))

    monsters.draw(window)
    asteroids.draw(window)


    if beg :
        bullets.update()
        Hero.update()
        monsters.update()
        asteroids.update()

    bullets.draw(window)
    



    if sprite.spritecollide(Hero , monsters , False):
        window.blit(font1.render('ti balbes neobrazovany', 1 , (255, 255, 255)), (300, 200))
        beg = False

    if sprite.spritecollide(Hero , asteroids , False):
        window.blit(font1.render('ti balbes neobrazovany', 1 , (255, 255, 255)), (300, 200))
        beg = False

    if  sprite.groupcollide(monsters , bullets , True , True):
        monster = Enemy('curtca.jpg', randint(50,650), randint(-350,0), 2)
        monsters.add(monster)

        score = score + 1
        
        
    if lost >=5:
        window.blit(font1.render('ti balbes neobrazovany', 1 , (255, 255, 255)), (300, 200))
        beg = False

    if score >= 10:
        text_win = font1.render('you wiiiiin' , 1, (255,255,255))
        window.blit(text_win, (300 , 200))
        beg = False

    Hero.reset()

    


    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                Hero.fire()
        
    
    display.update()
    clock.tick(60)    