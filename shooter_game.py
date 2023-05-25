#Создай собственный Шутер!
from pygame import *
mixer.init()
from random import *
font.init()
from time import time as timer
window = display.set_mode((700,500))
display.set_caption('Шутер')
lost = 0
class  GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player (GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= speed
        if keys_pressed[K_RIGHT] and self.rect.x < 620:
            self.rect.x += speed
    def fire(self):
        bullet = Bullet('bullet.png ',self.rect.centerx, self.rect.top, 15, 20,5)
        bullets.add(bullet)
class Enemy (GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > 500 :
            self.rect.x = randint(80,620)
            self.rect.y = 0 
            lost += 1
class AsteroidEnemy (GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500 :
            self.rect.x = randint(80,620)
            self.rect.y = 0 
class Bullet (GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
score = 0
rocket = Player('rocket.png',5, 400, 80,90, 5)
galaxy = transform.scale(image.load('galaxy.jpg'), (700, 500))
bullets = sprite.Group()
asteroids = sprite.Group()
for t in range (1, 3):
    asteroid = AsteroidEnemy('asteroid.png',randint(80, 620), -40, 80, 50, randint(1, 4))
    asteroids.add(asteroid)

monsters = sprite.Group()
for i in range (1, 6):
    monster = Enemy('ufo.png',randint(80, 620), -40, 80, 50, randint(1, 3))
    monsters.add(monster)

firem = mixer.Sound('fire.ogg')
mixer.music.load('space.ogg')
mixer.music.play()
clock = time.Clock()
FPS = 60
speed = 2
run = True
finish = False
font2 = font.SysFont('Arial', 30)
font3 =  font.SysFont('Arial', 70)
font4 = font.SysFont('Arial', 80)
life = 7
num_fire = 0
rel_time = False
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type ==KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    rocket.fire()
                    firem.play()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True
    if not finish:
        window.blit(galaxy, (0, 0))
        rocket.reset()
        rocket.update()
        #monster.update()
        bullets.update()
        monsters.update()
        monsters.draw(window)
        asteroids.update()
        asteroids.draw(window)
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload1 = font2.render("Wait, reload...", 1 ,(150, 0, 0))
                window.blit(reload1,(260,460))
            else:
                num_fire = 0
                rel_time = False

        text_lose1 = font2.render("Пропущено: " + str(lost), 1 ,(255,255,255))
        text_lose2 = font2.render("Счет: " + str(score),1, (255,255,255))
        sprites_list = sprite.groupcollide(monsters, bullets, True, True)
        for o in sprites_list:
            score+=1
            monster = Enemy('ufo.png',randint(80, 620), -40, 80, 50, randint(1, 4))
            monsters.add(monster)
        if sprite.spritecollide(rocket, monsters, False ) or sprite.spritecollide(rocket, asteroids, False ):
            sprite.spritecollide(rocket, monsters, True)
            sprite.spritecollide(rocket, asteroids, True)
            life -=1
        if score >= 10:
            finish = True
            text_lose3 = font3.render("YOU WIN!", 1 ,(98, 245, 110))
            window.blit(text_lose3 ,(250, 270))
        if life == 0 or lost >= 5:# hghrj elgv rgvjr h vir
            finish = True
            text_lose4 = font3.render("YOU LOSE!", 1 ,(200,56,4))
            window.blit(text_lose4 ,(250, 270))
        if life>= 3:
            life_color = (0, 150, 0)
        if life==2 :
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)
        text_life = font4.render(str(life), 1 ,life_color)
        window.blit(text_life ,(650, 2))
        window.blit(text_lose1,(0,0))
        window.blit(text_lose2,(0,30))
        keys_pressed = key.get_pressed()
        bullets.draw(window)
        display.update()
    clock.tick(FPS) #time.delay(60)