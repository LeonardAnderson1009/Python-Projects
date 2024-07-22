import neat.config
import pygame
import random
import os
import neat

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

class NeuralNetwork:
    def __init__(self, config):
        self.config = config
        self.population = neat.Population(config)
        self.population.add_reporter(neat.StdOutReporter(True))
        self.population.add_reporter(neat.Checkpointer(50))

    def run(self, eval_genomes, generations):
        self.population.run(eval_genomes, generations)

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
        if direction and self.x + self.image.get_width() < GAME_WIDTH-50:
            self.x += 10
        elif not direction and self.x > 50:
            self.x -= 10
        self.rect.topleft = (self.x, self.y)

class Bullets:
    DISTBUL = 80
    VEL = 10
    PASSED = False

    def __init__(self):
        self.image = BULLET_CHARACTER
        RandomNom = random.randrange(50, GAME_WIDTH - self.image.get_width() -50)
        if RandomNom > 100 and RandomNom < GAME_WIDTH // 2:
            self.x = RandomNom - 25 
        elif RandomNom > GAME_WIDTH // 2 and RandomNom < GAME_WIDTH:
            self.x = RandomNom + 25
        else:
            self.x = RandomNom
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

def drawWindow(neo, bullets, Score):
    WINDOW.blit(BG, (0, 0))
    for bullet in bullets:
        bullet.draw()
    neo.draw()

    ScoreText = STAT_FONT.render(f"Score: {int(Score)}", 1, (0, 0, 0))
    WINDOW.blit(ScoreText, (10, 10))

    pygame.display.update()

def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        genome.fitness = 0
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

            # Find the closest bullet
            closest_bullet_X = float('inf')
            for bullet in bullets:
                if bullet.x < closest_bullet_X:
                    closest_bullet_X = bullet.x

            # Inputs for the neural network
            inputs = [neo.x / GAME_WIDTH, closest_bullet_X / GAME_WIDTH]
            output = net.activate(inputs)
            
            # Outputs control left (0) or right (1)
            if output[0] > 0.5:
                neo.move(True)  # Move right
            else:
                neo.move(False)  # Move left

            # Spawn new bullets
            current_time = pygame.time.get_ticks()
            if current_time - last_bullet_spawn > bullet_spawn_interval:
                bullets.append(Bullets())
                last_bullet_spawn = current_time

            # Move and check for collisions
            for bullet in bullets:
                bullet.move()
                if bullet.collide(neo):
                    run = False

            bullets = [bullet for bullet in bullets if bullet.y < GAME_HEIGHT]

            fit = (pygame.time.get_ticks() - last_bullet_spawn) / 5000

            # Update fitness based on survival time
            if neo.x <= 2*(GAME_WIDTH//3) and neo.x >= (GAME_WIDTH//3):
                genome.fitness += fit
            else:
                genome.fitness += fit*0.5

            # Draw the game window
            drawWindow(neo, bullets, genome.fitness)

    pygame.quit()

def main():
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)

    nn = NeuralNetwork(config)
    nn.run(eval_genomes, 50) 

if __name__ == "__main__":
    main()
