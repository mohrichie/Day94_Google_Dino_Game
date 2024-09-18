import pygame, sys, random

# Initialize pygame
pygame.init()
# Configure the pygame screen
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
pygame.display.set_caption("Dino Game")

game_font = pygame.font.Font("assets/PressStart2P-Regular.ttf", 24)

# Create the Cloud class
class Cloud(pygame.sprite.Sprite):
    def __init__(self, image, x_pos, y_pos):
        super().__init__()
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        self.rect.x -= 1

# Create the Cactus class
class Cactus(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.sprites = []
        for i in range(1, 7):
            self.sprites.append(pygame.image.load(f"assets/Cactus/Cactus{i}.png"))

        self.image = random.choice(self.sprites)
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        self.x_pos -= game_speed
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))


class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x_pos = 1300
        self.y_pos = random.choice([280, 295, 350])
        self.sprites = []
        self.sprites.append(
            pygame.transform.scale(
                pygame.image.load("assets/Bird/Bird1.png"), (84, 62)))
        self.sprites.append(
            pygame.transform.scale(
                pygame.image.load("assets/Bird/Bird2.png"), (84, 62)))
        self.current_image = 0
        self.image = self.sprites[self.current_image]
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        self.animate()
        self.x_pos -= game_speed
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def animate(self):
        self.current_image += 0.025
        if self.current_image >= 2:
            self.current_image = 0
        self.image = self.sprites[int(self.current_image)]


# Create the Dino class
class Dino(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.running_sprites = []
        self.ducking_sprites = []
        self.running_sprites.append(pygame.image.load("assets/Dino/DinoRun1.png"))
        self.running_sprites.append(pygame.image.load("assets/Dino/DinoRun2.png"))

        self.ducking_sprites.append(pygame.image.load("assets/Dino/DinoDuck1.png"))
        self.ducking_sprites.append(pygame.image.load("assets/Dino/DinoDuck2.png"))

        self.x = x_pos
        self.y = y_pos
        self.current_image = 0
        self.image = self.running_sprites[self.current_image]
        self.rect = self.image.get_rect(center=(self.x, self.y))

        self.velocity = 50
        self.gravity = 4.5
        self.ducking = False

    def update(self):
        self.animate()
        self.apply_gravity()

    def animate(self):
        self.current_image += 1
        if self.current_image > 1:
            self.current_image = 0
        if self.ducking:
            self.image = self.ducking_sprites[self.current_image]
        else:
            self.image = self.running_sprites[self.current_image]

    def duck(self):
        self.ducking = True
        self.rect.centery = 380

    def unduck(self):
        self.ducking = False
        self.rect.centery = 360

    def apply_gravity(self):
        if self.rect.centery <= 360:
            self.rect.centery += self.gravity

    def jump(self):
        if self.rect.centery >= 360:
            while self.rect.centery - self.velocity > 40:
                self.rect.centery -= 1


# Variables
game_speed = 5
jump_count = 10
player_score = 0
game_over = False
obstacle_timer = 0
obstacle_spawn = False
obstacle_cooldown = 1000

# Set the ground
ground = pygame.image.load("assets/Other/Track.png")
ground_x = 0
ground_rect = ground.get_rect(center=(640, 400))

# Set the Cloud
cloud = pygame.image.load("assets/Other/Cloud.png")
cloud = pygame.transform.scale(cloud, (200, 80))

# Create groups
dino_group = pygame.sprite.GroupSingle()
cloud_group = pygame.sprite.Group()
Bird_group = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()

# Create the Dino object from the Dino Class
dinosaur = Dino(50, 360)
dino_group.add(dinosaur)

# Events
CLOUD_EVENT = pygame.USEREVENT
pygame.time.set_timer(CLOUD_EVENT, 3000)


def end_game():
    global player_score, game_speed
    game_over_text = game_font.render("Game Over!", True, "black")
    game_over_rect = game_over_text.get_rect(center=(640, 300))
    score_text = game_font.render(f"Score: {int(player_score)}", True, "black")
    score_rect = score_text.get_rect(center=(640, 340))
    screen.blit(game_over_text, game_over_rect)
    screen.blit(score_text, score_rect)
    game_speed = 5
    cloud_group.empty()
    obstacle_group.empty()

while True:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        dinosaur.duck()
    else:
        if dinosaur.ducking:
            dinosaur.unduck()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == CLOUD_EVENT:
            current_cloud_y = random.randint(50, 300)
            current_cloud = Cloud(cloud, 1380, current_cloud_y)
            cloud_group.add(current_cloud)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                dinosaur.jump()
                if game_over:
                    game_over = False
                    game_speed = 5
                    player_score = 0

    screen.fill("white")

    # Collisions
    if pygame.sprite.spritecollide(dino_group.sprite, obstacle_group, False):
        game_over = True

    if game_over:
        end_game()

    if not game_over:
        game_speed += 0.0025


        if pygame.time.get_ticks() - obstacle_timer >= obstacle_cooldown:
            obstacle_spawn = True

        if obstacle_spawn:
            obstacle_random = random.randint(1, 50)
            if obstacle_random in range(1, 7):
                new_obstacle = Cactus(1280, 340)
                obstacle_group.add(new_obstacle)
                obstacle_timer = pygame.time.get_ticks()
                obstacle_spawn = False
            elif obstacle_random in range(7, 10):
                new_obstacle = Bird()
                obstacle_group.add(new_obstacle)
                obstacle_timer = pygame.time.get_ticks()
                obstacle_spawn = False

    player_score += 0.1
    player_score_surface = game_font.render(
        str(int(player_score)), True, ("black"))
    screen.blit(player_score_surface, (1150, 10))

    dino_group.update()
    dino_group.draw(screen)

    cloud_group.update()
    cloud_group.draw(screen)

    Bird_group.update()
    Bird_group.draw(screen)

    obstacle_group.update()
    obstacle_group.draw(screen)

    ground_x -= game_speed


    screen.blit(ground, (ground_x, 362))
    if ground_x <= -1100:
        ground_x = 0

    pygame.display.update()
    clock.tick(120)





