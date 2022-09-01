import pygame
import math

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rotate = 0
        self.scale = 0.5
        self.img = pygame.image.load("assets/ship.png").convert_alpha()
        self.w = self.img.get_width()
        self.h = self.img.get_height()
        self.x = WIDTH//2
        self.y = 100
        self.angle = 0
        self.image = pygame.transform.rotozoom(self.img, self.angle,self.scale).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine * self.w//2, self.y - self.sine * self.h//2)
        self.vel = 0
        self.acc = 0
        self.mask = pygame.mask.from_surface(self.image)

    def movement(self, num = None):
        if num:
            self.angle += num
        else:
            self.x += self.cosine * 6
            self.y -= self.sine * 6

        self.image = pygame.transform.rotozoom(self.img, self.angle, self.scale).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.x + self.cosine + self.w//2, self.y - self.sine * self.h//2)


    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.movement()

        if keys[pygame.K_a]:
            self.movement(5)

        if keys[pygame.K_d]:
            self.movement(-5)

    def draw(self, win):
        win.blit(self.image, [self.x, self.y, self.w, self.h])

    def update(self):
        self.input()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/alpha.png")
        self.image = pygame.transform.rotozoom(self.image, 0, 0.5).convert_alpha()
        self.rect = self.image.get_rect(center = (WIDTH//2, HEIGHT//2))
        self.mask = pygame.mask.from_surface(self.image)


pygame.init()

WIDTH = 600
HEIGHT = 600
ds = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame masks!")
clock = pygame.time.Clock()
FPS = 60

# texts
font = pygame.font.SysFont('calibri', 32)
on_text = font.render("Sprites not touching", True, "black")
on_rect = on_text.get_rect(center = (WIDTH//2, 50))
on_off = font.render("rects touching but sprites dont", True, "black")
on_off_rect = on_off.get_rect(center = (WIDTH//2, 50))
off_text = font.render("sprites touching", True, "black")
off_rect = off_text.get_rect(center = (WIDTH//2, 50))

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle = pygame.sprite.GroupSingle()
obstacle.add(Obstacle())

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    ds.fill((255,255,255))

    # objects
    player.draw(ds)
    player.update()

    obstacle.draw(ds)

    # texts
    
    

    # collision
    if pygame.sprite.spritecollide(player.sprite, obstacle, False):
        if pygame.sprite.spritecollide(player.sprite, obstacle, False, pygame.sprite.collide_mask):
            ds.blit(off_text, off_rect)
        else:
            ds.blit(on_off, on_off_rect)
    else:
        ds.blit(on_text, on_rect)


    pygame.display.update()

pygame.quit()