from random import *
import pygame

pygame.init()

screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake")

#############################################################################################################################
#------------------------------------------- Paramètre general du programe -------------------------------------------------#
#############################################################################################################################

bsnakeX = screen_width / 2
bsnakeY = screen_height / 2
bsnake_width = 20
bsnake_height = 20

cloak = pygame.time.Clock()
appleX = randint(0, screen_width - 20)
appleY = randint(0, screen_height - 20)

snake_parts = [{'x': bsnakeX, 'y': bsnakeY}]
growth_rate = 3

white = (255, 255, 255)
black = (0, 0, 0)
gray = (128,128,128)
green = (0,255,0)
red = (255,0,0)

font = pygame.font.Font('freesansbold.ttf', 32)

home_back = pygame.image.load("image/home snake.png")
player_back = pygame.image.load("image/player snake.png")
main_back = pygame.image.load("image/main snake.png")

#############################################################################################################################
#---------------------------------------------------------- Def utile ------------------------------------------------------#
#############################################################################################################################

def draw_snake():
    for part in snake_parts:
        pygame.draw.rect(screen, (0, 255, 0), (part['x'], part['y'], bsnake_width, bsnake_height))

def check_self_collision():
    global bsnakeX, bsnakeY
    for part in snake_parts[1:]:
        if part['x'] == bsnakeX and part['y'] == bsnakeY:
            return True
    return False

#############################################################################################################################
#------------------------------------------------ Afficher Texte -----------------------------------------------------------#
#############################################################################################################################

def afficher_texte(texte, x, y, couleur):
    texte_affiche = font.render(texte, True, couleur)
    screen.blit(texte_affiche, (x, y))

#############################################################################################################################
#-------------------------------------------- Creation des bouton ----------------------------------------------------------#
#############################################################################################################################

def bouton(message, x, y, largeur, hauteur, couleur_base, couleur_survol, action=None):
    souris = pygame.mouse.get_pos()
    clic = pygame.mouse.get_pressed()

    if x + largeur > souris[0] > x and y + hauteur > souris[1] > y:
        pygame.draw.rect(screen, couleur_survol, (x, y, largeur, hauteur))
        if clic[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, couleur_base, (x, y, largeur, hauteur))

    # Rendu du texte pour obtenir ses dimensions
    texte_surface = font.render(message, True, white)
    texte_rect = texte_surface.get_rect()

    # Centrage du texte dans le bouton
    texte_x = x + (largeur - texte_rect.width) / 2
    texte_y = y + (hauteur - texte_rect.height) / 2

    screen.blit(texte_surface, (texte_x, texte_y))

#############################################################################################################################
#------------------------------------------ Creation de l'ecran d'aceuill --------------------------------------------------#
#############################################################################################################################

def home():
    running = True
    while running:
        screen.blit(home_back,(0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # Récupération des coordonnées de la souris
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            # Bouton "Démarrer le jeu"
            if 275 + 250 > mouse[0] > 275 and 350 + 50 > mouse[1] > 350:
                pygame.draw.rect(screen, (150, 150, 150), (275, 350, 250, 50))
                if click[0] == 1:
                    player_choice()  # Lancer la fonction main_game()

            # Bouton "Score"
            if 275 + 250 > mouse[0] > 275 and 450 + 50 > mouse[1] > 450:
                pygame.draw.rect(screen, (150, 150, 150), (275, 450, 250, 50))
                if click[0] == 1:
                    tab_score() # Lancer la fonction tab_score()

        # Affichage des boutons
        bouton("Démarrer le jeu", 275, 350, 250, 50, gray, green)
        bouton("Score", 275, 450, 250, 50, gray, green)

        pygame.display.update()

#############################################################################################################################
#--------------------------------------- Ecran de jeux ---------------------------------------------------------------------#
#############################################################################################################################

def main_game():
    global bsnakeX , bsnakeY , appleX , appleY ,score
    previous_direction = None
    direction = None
    running = True
    score = 0
    while running:
        screen.blit(main_back,(0,0))

        draw_snake()
        pygame.draw.rect(screen, (255, 0, 0), (appleX, appleY, 20, 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # Pour determiner le sens de déplacement
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and previous_direction != "right":
                    direction = "left"
                elif event.key == pygame.K_RIGHT and previous_direction != "left":
                    direction = "right"
                elif event.key == pygame.K_UP and previous_direction != "down":
                    direction = "up"
                elif event.key == pygame.K_DOWN and previous_direction != "up":
                    direction = "down"

            previous_direction = direction

        # Mouvement automatique dans une direction donner
        if direction == "left":
            bsnakeX -= 5 
        elif direction == "right":
            bsnakeX += 5
        elif direction == "up":
            bsnakeY -= 5
        elif direction == "down":
            bsnakeY += 5

        # SI il sort des limite de la map
        if bsnakeX < 0:
            bsnakeX = screen_width - 20
        if bsnakeX > screen_width - 20:
            bsnakeX = 0
        if bsnakeY < 0:
            bsnakeY = screen_height - 20
        if bsnakeY > screen_height - 20:
            bsnakeY = 0

        if bsnakeX < appleX + 20 and bsnakeX + 20 > appleX and bsnakeY < appleY + 20 and bsnakeY + 20 > appleY:
            appleX = randint(0, screen_width - 20)
            appleY = randint(0, screen_height - 20)
            score += 1
            for _ in range(growth_rate):
                snake_parts.append({'x': snake_parts[-1]['x'], 'y': snake_parts[-1]['y']})

        for i in range(len(snake_parts) - 1, 0, -1):
            snake_parts[i]['x'] = snake_parts[i - 1]['x']
            snake_parts[i]['y'] = snake_parts[i - 1]['y']
        snake_parts[0]['x'] = bsnakeX
        snake_parts[0]['y'] = bsnakeY

        if check_self_collision():
            print(score)
            with open("score.txt", "a") as file:
                file.write(f"{player} : {score}" + "\n")
            home()

        cloak.tick(60)
        pygame.display.flip()
    pygame.quit()
    quit()

#############################################################################################################################
#------------------------------------------- Choix du nom de joueur --------------------------------------------------------#
#############################################################################################################################

def player_choice():
    global player
    name_player = ""
    running = True
    while running:
        screen.blit(player_back,(0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    home()
                if event.key == pygame.K_RETURN:
                    player = name_player
                    name_player = ""
                    main_game()
                else:
                    # Récupérer les touches pressées pour former un mot
                    lettre = chr(event.key)
                    name_player += lettre

        display_word = font.render(' '.join(name_player), True, green)
        afficher_texte(f"{name_player}", screen_width // 2 - display_word.get_width() // 2, screen_height // 2, green)  # Affiche le mot en cours de formation

        pygame.display.update()

#############################################################################################################################
#----------------------------------------------- Ecran de Score ------------------------------------------------------------#
#############################################################################################################################

def tab_score():
    running = True
    scores = []

    with open("score.txt", "r") as fichier:
        lines = fichier.readlines()
        for line in lines:
            scores.append(line)  

    while running:
        screen.blit(main_back,(0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    home()
        y = 150
        for l in scores:
            afficher_texte(l, 275, y,red)
            y += 40

        pygame.display.update()

home()