import neat.config
import pygame
import random
import os

pygame.font.init()

GAME_HEIGHT = 800
GAME_WIDTH = 500

STAT_FONT = pygame.font.SysFont("comicsans", 50)

WINDOW = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))

NEO_CHARACTER = pygame.image.load(os.path.join("Assets", "Neo.png"))
BULLET_CHARACTER = pygame.image.load(os.path.join("Assets", "Bullet.png"))
BG = pygame.image.load(os.path.join("Assets", "BG.png"))

NEO_CHARACTER = pygame.transform.scale(NEO_CHARACTER, (NEO_CHARACTER.get_width() * 2, NEO_CHARACTER.get_height() * 2))
BULLET_CHARACTER = pygame.transform.scale(BULLET_CHARACTER, (BULLET_CHARACTER.get_width() * 2, BULLET_CHARACTER.get_height() * 2))
BG = pygame.transform.scale(BG, (BG.get_width() * 2, BG.get_height() * 2))

pygame.display.set_caption("neoDodge")


class NeoChar:
    def __init__(self):
        self.x = GAME_WIDTH // 2
        self.image = NEO_CHARACTER
        self.y = GAME_HEIGHT - self.image.get_height()
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.rect.topleft = (self.x, self.y)

    def draw(self):
        WINDOW.blit(self.image, (self.x, self.y))

    def move(self, direction):
        # right == true, left == false
        if direction and self.x + self.image.get_width() < GAME_WIDTH:
            self.x += 10
        elif not direction and self.x > 0:
            self.x -= 10
        self.rect.topleft = (self.x, self.y)

class Bullets:
    DISTBUL = 80
    VEL = 10
    PASSED = False

    def __init__(self):
        self.image = BULLET_CHARACTER
        self.x = random.randrange(0, GAME_WIDTH - self.image.get_width())
        self.y = 0
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.rect.topleft = (self.x, self.y)

    def draw(self):
        WINDOW.blit(self.image, (self.x, self.y))

    def move(self):
        self.y += self.VEL
        self.rect.topleft = (self.x, self.y)
        
    def collide(self, neo):
        return self.rect.colliderect(neo.rect)

def drawWindow(neo, bullets,Score):
    #WINDOW.fill((126, 126, 126))
    WINDOW.blit(BG,(0,0))
    for bullet in bullets:
        bullet.draw()
    neo.draw()

    ScoreText = STAT_FONT.render(f"Score: {int(Score)}", 1, (0, 0, 0))
    WINDOW.blit(ScoreText, (10, 10))

    pygame.display.update()

def main():

    Numpassed = 0
    neo = NeoChar()
    bullets = []
    last_bullet_spawn = pygame.time.get_ticks()
    bullet_spawn_interval = 400

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            neo.move(False)
        if keys[pygame.K_RIGHT]:
            neo.move(True)

        current_time = pygame.time.get_ticks()
        if current_time - last_bullet_spawn > bullet_spawn_interval:
            bullets.append(Bullets())
            last_bullet_spawn = current_time
        
        for bullet in bullets:
            bullet.move()
            if bullet.collide(neo):
                run = False

        bullets = [bullet for bullet in bullets if bullet.y < GAME_HEIGHT]

        Numpassed += (pygame.time.get_ticks() - last_bullet_spawn) / 5000

        drawWindow(neo, bullets,Numpassed)

    pygame.quit()
    quit()

if __name__ == "__main__":

    main()
