import pygame
import random
import sqlite3

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
GRAY = (168,168,168)
DARKGREEN = (0,180,0)

# Font
font = pygame.font.Font(None, 36)

# Rychlosti
player_speed = 5
coin_speed = 4
rock_speed = 5
heart_speed = coin_speed * 2 - 1
bonus_speed = coin_speed

# Funkce pro nastavení databáze
def setup_database():
    conn = sqlite3.connect("highscores.db")  
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS highscores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    score INTEGER NOT NULL)''')
    conn.commit()
    conn.close()

# Funkce pro načtení nejvyššího skóre
def load_high_score():
    conn = sqlite3.connect("highscores.db")
    c = conn.cursor()
    c.execute("SELECT MAX(score) FROM highscores")
    high_score = c.fetchone()[0]  # Získání nejvyššího skóre
    conn.close()
    return high_score if high_score is not None else 0  # Pokud není žádné skóre, vrátí 0

# Funkce pro uložení skóre a aktualizaci high score
def save_score(name, score):
    conn = sqlite3.connect("highscores.db")
    c = conn.cursor()
    
    # Uložení skóre
    c.execute("INSERT INTO highscores (name, score) VALUES (?, ?)", (name, score))
    
    # Zkontrolování, zda je to nové high score
    c.execute("SELECT MAX(score) FROM highscores")
    current_high_score = c.fetchone()[0]
    
    conn.commit()
    conn.close()
    
    return current_high_score  # Vrátí aktuální high score

# Funkce pro načtení všech skóre (seřazené od nejvyššího)
def load_all_scores():
    conn = sqlite3.connect("highscores.db")
    c = conn.cursor()
    c.execute("SELECT name, score FROM highscores ORDER BY score DESC")
    scores = c.fetchall()  # Vrátí seznam všech skóre
    conn.close()
    return scores

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
    
def ask_for_name():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 48)
    small_font = pygame.font.Font(None, 36)  # Menší font pro instrukci

    input_box = pygame.Rect(screen_width // 2 - 100, screen_height // 2, 200, 50)
    player_name = ""
    active = True

    while active:
        screen.fill(GRAY)
        
        # Zobrazení textu "Zadej jméno:"
        text = font.render("Zadej jméno:", True, BLACK)
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, screen_height // 2 - 70))
        
        # Zobrazení vstupního pole
        pygame.draw.rect(screen, BLACK, input_box, 2)
        name_surface = font.render(player_name, True, BLACK)
        screen.blit(name_surface, (input_box.x + 10, input_box.y + 10))

        # Zobrazení instrukce "Pro start zmáčkni ENTER"
        instruction_text = small_font.render("Pro start zmáčkni ENTER", True, BLACK)
        screen.blit(instruction_text, (screen_width // 2 - instruction_text.get_width() // 2, screen_height // 2 + 100))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and player_name.strip():
                    return player_name  # Vrátíme jméno, pokud není prázdné
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]  # Mazání znaku
                elif len(player_name) < 10 and event.unicode.isprintable():
                    player_name += event.unicode  # Přidání znaku, pokud je délka < 10


# Funkce pro zobrazení menu
def menu():
    setup_database()
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
                player_name = ask_for_name()
                hra(player_name)

# Funkce pro hru
def hra(player_name):
    pygame.mixer.music.load("sounds/background_music.mp3")
    pygame.mixer.music.set_volume(volume - 0.2)
    pygame.mixer.music.play(-1)  # Opakované přehrávání 

    player = Player()
    coins = [Coin()]
    score = 0
    high_score = load_high_score()  # Načtení high score z databáze
    lives = 3  # Počet životů
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

        # Generování mincí
        if random.randint(1, 100) < 3:
            coins.append(Coin())

        # Generování kamenů
        if random.randint(1, 200) < 3:
            rocks.append(Rock())

        # Generování srdíček, pokud hráč nemá plné životy
        if lives < 3 and random.randint(1, 2000) < 2:
            hearts.append(HeartDrop())

        # Generování bonusů
        if random.randint(1, 500) < 2:
            bonuses.append(Bonus())

        # Aktualizace mincí
        score_coin = 10  
        for coin in coins[:]:
            coin.fall()
            if coin.y > screen_height:
                coins.remove(coin)

            if player.get_rect().colliderect(coin.get_rect()):
                coins.remove(coin)
                score += score_coin
                coin_sound.play()  # Zvuk sebrání mince
            coin.draw()

        # Aktualizace kamenů
        for rock in rocks[:]:
            rock.fall()
            if rock.y > screen_height:
                rocks.remove(rock)
            
            if player.get_rect().colliderect(rock.get_rect()):
                hit_sound.play()  # Zvuk nárazu
                lives -= 1 
                rocks.remove(rock)  # Odstranění kamene

                if lives <= 0:  # Game Over
                    pygame.time.delay(200)  # Krátká pauza
                    save_score(player_name, score)  # Uložení skóre do databáze
                    if score > high_score:  
                        save_score(player_name, score)  # Aktualizace high score
                    game_over(score, player_name)
                    return
            rock.draw()
        
        # Aktualizace srdíček
        for heart in hearts[:]:
            heart.fall()
            if heart.y > screen_height:
                hearts.remove(heart)

            if player.get_rect().colliderect(heart.get_rect()):
                if lives < 3:  # Maximálně 3 životy
                    lives += 1
                hearts.remove(heart)
            heart.draw()

        # Aktualizace bonusů
        for bonus in bonuses[:]:
            bonus.fall()
            if bonus.y > screen_height:
                bonuses.remove(bonus)

            if player.get_rect().colliderect(bonus.get_rect()):
                bonuses.remove(bonus)
                score += score_coin * 20
                coin_sound.play()  # Zvuk bonusu
            bonus.draw()

        # Aktualizace high score
        if score > high_score:
            high_score = score

        # Zobrazení skóre a high score
        score_text = font.render(f"Score: {score}", True, BLACK)
        high_score_text = font.render(f"High Score: {high_score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(high_score_text, (10, 40))
        
        # Zobrazení životů
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
def game_over(score, player_name):
    pygame.mixer.music.stop()
    game_over_sound.play()

    # Poloprůhledný efekt
    game_over_box = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    game_over_box.fill((255, 0, 0, 150))
    screen.blit(game_over_box, (0, 0))

    game_over_box2 = pygame.Surface((400, 175), pygame.SRCALPHA)
    game_over_box2.fill((0, 0, 0, 210))
    screen.blit(game_over_box2, (screen_width // 2 - 200, screen_height // 2 - 75))

    # Texty
    title_font = pygame.font.Font(None, 90)
    text_font = pygame.font.Font(None, 36)
    final_score_font = pygame.font.Font(None, 48)

    title = title_font.render("GAME OVER", True, RED)
    final_score = final_score_font.render(f"Tvoje skóre: {score}", True, WHITE)
    instruction = text_font.render("ENTER = restart | SPACE = leaderboard", True, WHITE)

    screen.blit(title, (screen_width // 2 - title.get_width() // 2, screen_height // 2 - 50))
    screen.blit(final_score, (screen_width // 2 - final_score.get_width() // 2, screen_height // 2 + 50))
    screen.blit(instruction, (screen_width // 2 - instruction.get_width() // 2, screen_height // 2 + 120))

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False
                    hra(player_name)  # Restart hry
                elif event.key == pygame.K_SPACE:
                    leaderboard_screen(player_name, score)  # Otevře leaderboard

# Funkce pro zobrazení leaderboardu
def leaderboard_screen(player_name, score):
    scores = load_all_scores()[:5]  # Načtení top 5 skóre

    screen.fill(GRAY)
    title_font = pygame.font.Font(None, 64)
    text_font = pygame.font.Font(None, 48)

    title = title_font.render("LEADERBOARD", True, GOLD)
    screen.blit(title, (screen_width // 2 - title.get_width() // 2, 100))

    # Vykreslení skóre
    y_offset = 180
    for i, (name, score) in enumerate(scores, start=1):
        text = text_font.render(f"{i}. {name}: {score}", True, BLACK)
        screen.blit(text, (screen_width // 2 - text.get_width() // 2, y_offset))
        y_offset += 50

    # Text pro restart
    restart_text = text_font.render("Stiskni ENTER pro restart", True, BLACK)
    screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, screen_height - 100))

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False
                    hra(player_name)  # Restart hry

menu()
hra()
