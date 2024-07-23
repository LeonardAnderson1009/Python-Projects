import os
import pygame
import random
import neat

#Inspiration and some code from https://github.com/techwithtim/

pygame.font.init()

GAME_HEIGHT = 800
GAME_WIDTH = 500

STATFONT = pygame.font.SysFont("comicsans", 20)

WINDOW = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))

BIRDIMG = pygame.image.load(os.path.join("Assets", "bird1.png"))
PIPEIMG = pygame.image.load(os.path.join("Assets", "pipe.png"))
BIRDIMG = pygame.transform.scale(BIRDIMG,(3*(BIRDIMG.get_width() // 2),3*(BIRDIMG.get_height() // 2)))
PIPEIMG = pygame.transform.scale(PIPEIMG,(3*(PIPEIMG.get_width() // 2),3*(PIPEIMG.get_height() // 2)))

gen = 0

pygame.display.set_caption("FlappyAI")

class Bird:
    def __init__(self):
        self.x = GAME_WIDTH // 3
        self.image = BIRDIMG
        self.y = GAME_HEIGHT // 2 - self.image.get_height()
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.vel = 0
        self.tickcount = 0

    def Draw(self):
        WINDOW.blit(self.image, (self.x, self.y))
    
    def Jump(self):
        self.vel = -10.5
        self.tickcount = 0

    def Move(self):
        self.tickcount += 1
        displacement = self.vel * self.tickcount + 0.5 * 3 * self.tickcount**2  # delta x = vt + 0.5at^2

        if displacement >= 20:
            displacement = 20
        elif displacement < 0:
            displacement -= 2

        self.y += displacement
        self.rect.topleft = (self.x, self.y)

class Pipe:
    def __init__(self):
        self.x = GAME_WIDTH

        self.PipeTop = pygame.transform.flip(PIPEIMG, False, True)
        self.PipeBottom = PIPEIMG

        self.top = 0
        self.bottom = 0

        self.Setheight()

    def Setheight(self):
        self.height = random.randrange(50, 450) 
        self.top = self.height - self.PipeTop.get_height()
        self.bottom = self.height + 200
        
        self.rectTop = self.PipeTop.get_rect(topleft=(self.x, self.top))
        self.rectBottom = self.PipeBottom.get_rect(topleft=(self.x, self.bottom))

    def Draw(self):
        WINDOW.blit(self.PipeTop, (self.x, self.top))
        WINDOW.blit(self.PipeBottom, (self.x, self.bottom))

    def Move(self):
        self.x -= 5
        self.rectTop.topleft = (self.x, self.top)
        self.rectBottom.topleft = (self.x, self.bottom)

    def Collide(self, bird):
        if self.rectBottom.colliderect(bird.rect) or self.rectTop.colliderect(bird.rect):
            return True
        return False

def DrawWindow(birds, pipe,count,gen):
    WINDOW.fill((255, 255, 255))
    pipe.Draw()
    for bird in birds:
        bird.Draw()

    #Score text
    scoretext = STATFONT.render(f"Score: {count}",1,(0,0,0))
    WINDOW.blit(scoretext, (0,0))
    #Gen Text
    gentext = STATFONT.render(f"Gen: {gen -1}",1,(0,0,0))
    WINDOW.blit(gentext, (100,0))
    #Alive Text
    alivetext = STATFONT.render(f"Alive: {len(birds)}",1,(0,0,0))
    WINDOW.blit(alivetext, (200,0))
    pygame.display.update()

def EvalGenomes(genomes,config):

    global WINDOW, gen
    gen += 1

    nets = []
    birds = []
    ge = []
    for genome_id, genome in genomes:
        genome.fitness = 0  
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird())
        ge.append(genome)

    pipe = Pipe()
    clock = pygame.time.Clock()
    pipepassed = False
    count = 0
    run = True
    while run and len(birds) > 0:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                break

        for x,bird in enumerate(birds):
            ge[x].fitness += 0.1
            bird.Move()

            output = nets[birds.index(bird)].activate((bird.y, abs(bird.y - pipe.top), abs(bird.y - pipe.bottom)))

            if output[0] > 0.5: 
                bird.Jump()     

        pipe.Move()

        for bird in birds:
            if pipe.Collide(bird):
                ge[birds.index(bird)].fitness -= 1
                nets.pop(birds.index(bird))
                ge.pop(birds.index(bird))
                birds.pop(birds.index(bird))

        if pipe.x + pipe.PipeBottom.get_width() < GAME_WIDTH // 3 and not pipepassed:
            count += 1
            for genome in ge:
                genome.fitness += 5
            pipepassed = True
            
        if pipe.x + pipe.PipeBottom.get_width() < 0:
            pipe.x = GAME_WIDTH
            pipe.Setheight()
            pipepassed = False

        for bird in birds:
            if bird.y >= GAME_HEIGHT - bird.image.get_height() or bird.y < 0:
                nets.pop(birds.index(bird))
                ge.pop(birds.index(bird))
                birds.pop(birds.index(bird))

        DrawWindow(birds, pipe,count,gen)

def run(confpath):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         confpath)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(EvalGenomes, 50)

    print('\nBest genome:\n{!s}'.format(winner))

if __name__ == "__main__":
    localdir = os.path.dirname(__file__)
    confpath = os.path.join(localdir,"config.txt")
    run(confpath)
