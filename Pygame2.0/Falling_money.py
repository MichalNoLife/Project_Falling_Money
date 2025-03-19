import pygame
import random

# Inicializace Pygame
pygame.init()

# Nastavení obrazovky
screen_width, screen_height = 800, 600
# FPS
fps = 90
# Zobrazení obrazovky
screen = pygame.display.set_mode((screen_width, screen_height))
# Název
pygame.display.set_caption("Falling Money")
# Ikona hry
icon = pygame.image.load("images/icon.png")
pygame.display.set_icon(icon)
# Zvuk
volume = 0.5

# Načtení obrázků
background = pygame.image.load("images/background.jpg")
background = pygame.transform.scale(background, (screen_width, screen_height))
menu_background = pygame.image.load("images/menu_background.jpg")
menu_background = pygame.transform.scale(menu_background, (screen_width, screen_height))

player_img = pygame.image.load("images/player.png")
player_img = pygame.transform.scale(player_img, (80, 80))
coin_img = pygame.image.load("images/coin.png")
coin_img = pygame.transform.scale(coin_img, (40, 40))
rock_img = pygame.image.load("images/rock.png")
rock_img = pygame.transform.scale(rock_img, (50,50))
heart_img = pygame.image.load("images/heart.png")
heart_img = pygame.transform.scale(heart_img, (50,50))
bonus_img = pygame.image.load("images/bonus.png")
bonus_img = pygame.transform.scale(bonus_img, (40, 40))

# Načtení zvuků
pygame.mixer.init()
coin_sound = pygame.mixer.Sound("sounds/coin.mp3")
coin_sound.set_volume(volume)
hit_sound = pygame.mixer.Sound("sounds/hit.mp3")
hit_sound.set_volume(volume)
game_over_sound = pygame.mixer.Sound("sounds/game_over.mp3")
game_over_sound.set_volume(volume)

# Barvy
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0) 
RUBY = (224, 17, 95)
RED = (255, 0, 0)
# Font
font = pygame.font.Font(None, 36)

# Rychlosti
player_speed = 5
coin_speed = 4
rock_speed = 5
heart_speed = coin_speed * 2 - 1
bonus_speed = coin_speed

# Funkce pro načtení high score
def load_high_score():
    try:
        with open("highscore.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0
    except ValueError:
        return 0

# Funkce pro uložení high score
def save_high_score(score):
    with open("highscore.txt", "w") as file:
        file.write(str(score))

# Třída hráče
class Player:
    def __init__(self):
        self.x = screen_width // 2
        self.y = screen_height - 100
        self.speed = player_speed

    def move(self, keys):
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x += self.speed

        # Udržení hráče v obrazovce
        self.x = max(0, min(self.x, screen_width - 80))

    def draw(self):
        screen.blit(player_img, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, 80, 80)

# Třída mince
class Coin:
    def __init__(self):
        self.x = random.randint(50, screen_width - 50)
        self.y = 0
        self.speed = coin_speed

    def fall(self):
        self.y += self.speed

    def draw(self):
        screen.blit(coin_img, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, 40, 40)

# Třída kámen
class Rock:
    def __init__(self):
        self.x = random.randint(50, screen_width - 50)
        self.y = 0
        self.speed = rock_speed

    def fall(self):
        self.y += self.speed

    def draw(self):
        screen.blit(rock_img, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, 50, 50)    
    
# Třída padající srdce
class HeartDrop:
    def __init__(self):
        self.x = random.randint(50, screen_width - 50)
        self.y = 0
        self.speed = heart_speed
    
    def fall(self):
        self.y += self.speed

    def draw(self):
        screen.blit(heart_img, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, 30, 30)

# Třída bonusu
class Bonus:
    def __init__(self):
        self.x = random.randint(50, screen_width - 50)
        self.y = 0
        self.speed = bonus_speed

    def fall(self):
        self.y += self.speed

    def draw(self):
        screen.blit(bonus_img, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, 40, 40)
    
# Funkce pro zobrazení menu
def menu():
    screen.blit(menu_background, (0, 0))  # Vykreslení pozadí
# Poloprůhledný box za text
    menu_box = pygame.Surface((400, 150), pygame.SRCALPHA)  # Vytvoření poloprůhledného obdélníku
    menu_box.fill((0, 0, 0, 200))  # Černá s průhlednost
    screen.blit(menu_box, (screen_width // 2 - 200, screen_height // 2 - 75))
# Vykreslení textu
    title_font = pygame.font.Font(None, 64)
    text_font = pygame.font.Font(None, 36)
    title = title_font.render("FALLING MONEY", True, GOLD)
    screen.blit(title, (screen_width // 2 - title.get_width() // 2, screen_height // 2 - 50))

    instruction = text_font.render("Stiskni ENTER pro spuštění", True, GOLD)
    screen.blit(instruction, (screen_width // 2 - instruction.get_width() // 2, screen_height // 2 + 25))
    pygame.display.update()


# Čekání na stisknutí ENTER
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False

# Funkce pro hru
def hra():
    # Spuštění hudby při startu hry
    pygame.mixer.music.load("sounds/background_music.mp3")
    pygame.mixer.music.set_volume(volume - 0.2)
    pygame.mixer.music.play(-1)  # Opakované přehrávání 

    player = Player()
    coins = [Coin()]
    score = 0
    high_score = load_high_score()
    lives = 3 # Počet životů
    rocks = []
    hearts = []
    bonuses = []
    clock = pygame.time.Clock()
    
    running = True
    while running:
        screen.blit(background, (0, 0))

        # Zpracování vstupu
        keys = pygame.key.get_pressed()
        player.move(keys)

        # Generování nových mincí
        if random.randint(1, 100) < 3:
            coins.append(Coin())

        # Generování nových kamenů
        if random.randint(1, 200) < 3:
            rocks.append(Rock())

        # Generování nových srdíček
        if lives < 3:
            if random.randint(1, 2000) < 2:
                hearts.append(HeartDrop())

        # Generování bonusu
        if random.randint(1, 500) < 2:
            bonuses.append(Bonus())

        # Aktualizace mincí a kontrola kolize s hráčem
        score_coin = 10 
        for coin in coins[:]:
            coin.fall()
            if coin.y > screen_height:
                coins.remove(coin)

            if player.get_rect().colliderect(coin.get_rect()):
                coins.remove(coin)
                score += score_coin
                coin_sound.play() # Přehrání zvuku sebrání mince
            coin.draw()

        # Aktualizace kamenů a kontrola kolize s hráčem
        for rock in rocks[:]:
            rock.fall()
            if rock.y > screen_height:
                rocks.remove(rock)
            
            if player.get_rect().colliderect(rock.get_rect()):
                hit_sound.play()  # Přehrání zvuku nárazu
                lives -= 1 
                rocks.remove(rock) # Odstranit kámen po nárazu

                if lives <= 0:  # Pokud hráč ztratí všechny životy - Game Over
                    pygame.time.delay(200)  # Pauza před Game Over
                    game_over(score)
                    return
            rock.draw()
        
        # Aktualizace padajících srdíček a kolize s hráčem
        for heart in hearts[:]:
            heart.fall()
            if heart.y > screen_height:
                hearts.remove(heart)

            if player.get_rect().colliderect(heart.get_rect()):
                if lives < 3:  # Maximálně 3 životy
                    lives += 1
                hearts.remove(heart)
            heart.draw()

        # Aktualizace bonusu a kolize s hráčem
        for bonus in bonuses[:]:
            bonus.fall()
            if bonus.y > screen_height:
                bonuses.remove(bonus)

            if player.get_rect().colliderect(bonus.get_rect()):
                bonuses.remove(bonus)
                score += score_coin * 20
                coin_sound.play() # Přehrání zvuku
            bonus.draw()

        # Aktualizace high score
        if score > high_score:
            high_score = score
            save_high_score(high_score)

        # Zobrazení textů
        score_text = font.render(f"Score: {score}", True, BLACK)
        high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(high_score_text, (10, 40))
        for i in range(lives):
            screen.blit(heart_img, (screen_width - (i + 1) * 50, 10))

        # Vykreslení hráče
        player.draw()

        # Kontrola událostí
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()

# Funkce pro game over
def game_over(score):
    # Zastavení hudby
    pygame.mixer.music.stop()
    # Přehrát zvuk Game Over
    game_over_sound.play()

    # Poloprůhledný box
    game_over_box = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    game_over_box.fill((255, 0, 0, 150))  # Červená s průhledností
    screen.blit(game_over_box, (0, 0))

    game_over_box2 = pygame.Surface((400, 150), pygame.SRCALPHA)
    game_over_box2.fill((0, 0, 0, 210))
    screen.blit(game_over_box2, (screen_width // 2 - 200, screen_height // 2 - 75))

    # Vykreslení textu
    game_over_text = "GAME OVER"
    title_font = pygame.font.Font(None, 90)
    text_font = pygame.font.Font(None, 36)
    final_score = pygame.font.Font(None, 48)

    title = title_font.render(game_over_text, True, RED)
    instruction = text_font.render("Stiskni ENTER pro restart", True, WHITE)
    final_score = final_score.render(f"Tvoje skóre: {score}", True, WHITE)

    screen.blit(title, (screen_width // 2 - title.get_width() // 2, screen_height // 2 - 50))
    screen.blit(instruction, (screen_width // 2 - instruction.get_width() // 2, screen_height // 2 + 25))
    screen.blit(final_score, (screen_width // 2 - final_score.get_width() // 2, screen_height // 2 + 125))

    pygame.display.update()

    # Čekání na ENTER
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False
                hra()

menu()
hra()
