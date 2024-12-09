import pygame
import sys
from carte import Carte

def main():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)  # Passer en plein écran
    pygame.display.set_caption("My Game")
    clock = pygame.time.Clock()

    carte = Carte(screen)

    running = True
    keys = {"right": False, "left": False, "up": False, "down": False}  # Pour suivre l'état des touches

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False  # Quitter le plein écran si on appuie sur ESC
                elif event.key == pygame.K_RIGHT:
                    keys["right"] = True
                elif event.key == pygame.K_LEFT:
                    keys["left"] = True
                elif event.key == pygame.K_UP:
                    keys["up"] = True
                elif event.key == pygame.K_DOWN:
                    keys["down"] = True
                elif event.key == pygame.K_SPACE:
                    carte.personnage.attaquer("right")
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    keys["right"] = False
                elif event.key == pygame.K_LEFT:
                    keys["left"] = False
                elif event.key == pygame.K_UP:
                    keys["up"] = False
                elif event.key == pygame.K_DOWN:
                    keys["down"] = False

        if keys["right"]:
            carte.personnage.deplacer("right", carte.carte_largeur, carte.carte_hauteur)
        elif keys["left"]:
            carte.personnage.deplacer("left", carte.carte_largeur, carte.carte_hauteur)
        elif keys["up"]:
            carte.personnage.deplacer("up", carte.carte_largeur, carte.carte_hauteur)
        elif keys["down"]:
            carte.personnage.deplacer("down", carte.carte_largeur, carte.carte_hauteur)
        else:
            carte.personnage.deplacer("stop", carte.carte_largeur, carte.carte_hauteur)

        carte.update()  # Dessine la carte, les monstres et les barres de vie

        # Dessiner le personnage et sa hitbox
        carte.personnage.draw(screen, 0, 0)  # Ajustez camera_x et camera_y si nécessaire

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
