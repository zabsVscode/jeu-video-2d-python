import pygame
import os

class Personnage(pygame.sprite.Sprite):
    def __init__(self, screen, nom):
        super().__init__()
        self.screen = screen
        self.nom = nom
        self.animations = {
            "repos": [],
            "run_right": [],
            "run_left": [],
            "run_up": [],
            "run_down": [],
            "attack_right": [],
            "attack_left": [],
            "attack_up": [],
            "attack_down": []
        }
        self.image = None
        self.rect = None
        self.position = (0, 0)
        self.animation = "repos"
        self.current_frame = 0
        self.frame_delay = 5
        self.is_attacking = False
        self.hp_max = 1000
        self.hp = self.hp_max
        self.attaque = 10
        self.vitesse = 5
        self.armure = 0  # Ajouter l'attribut armure ici
        self.load_images()

    def load_images(self):
        # Charger les images pour les animations
        repo_image_path = os.path.join('assets', 'sprites', 'Samurai_Repos', 'Samurai_Repos.png')
        if os.path.exists(repo_image_path):
            self.animations["repos"].append(pygame.image.load(repo_image_path).convert_alpha())
        else:
            raise FileNotFoundError(f"No file '{repo_image_path}' found.")

        # Charger les images pour courir vers la droite
        for i in range(1, 9):
            run_right_image_path = os.path.join('assets', 'sprites', 'Samurai_RunRight', f'Samurai_RunRight_Sequence{i}.png')
            if os.path.exists(run_right_image_path):
                image = pygame.image.load(run_right_image_path).convert_alpha()
                self.animations["run_right"].append(image)
            else:
                raise FileNotFoundError(f"No file '{run_right_image_path}' found.")

        # Charger les images pour courir vers la gauche
        for i in range(1, 9):
            run_left_image_path = os.path.join('assets', 'sprites', 'Samurai_RunLeft', f'Samurai_RunLeft_Sequence{i}.png')
            if os.path.exists(run_left_image_path):
                image = pygame.image.load(run_left_image_path).convert_alpha()
                image = pygame.transform.flip(image, True, False)
                self.animations["run_left"].append(image)
            else:
                raise FileNotFoundError(f"No file '{run_left_image_path}' found.")

        # Charger les images pour courir vers le haut
        for i in range(1, 9):
            run_up_image_path = os.path.join('assets', 'sprites', 'Samurai_RunUp', f'Samurai_RunUp_Sequence{i}.png')
            if os.path.exists(run_up_image_path):
                image = pygame.image.load(run_up_image_path).convert_alpha()
                self.animations["run_up"].append(image)
            else:
                raise FileNotFoundError(f"No file '{run_up_image_path}' found.")

        # Charger les images pour courir vers le bas
        for i in range(1, 9):
            run_down_image_path = os.path.join('assets', 'sprites', 'Samurai_RunDown', f'Samurai_RunDown_Sequence{i}.png')
            if os.path.exists(run_down_image_path):
                image = pygame.image.load(run_down_image_path).convert_alpha()
                self.animations["run_down"].append(image)
            else:
                raise FileNotFoundError(f"No file '{run_down_image_path}' found.")

        # Charger les images pour les attaques
        for i in range(1, 6):
            attack_right_image_path = os.path.join('assets', 'sprites', 'Samurai_AttackRight', f'Samurai_AttackRight_Sequence{i}.png')
            if os.path.exists(attack_right_image_path):
                image = pygame.image.load(attack_right_image_path).convert_alpha()
                self.animations["attack_right"].append(image)
            else:
                raise FileNotFoundError(f"No file '{attack_right_image_path}' found.")
        
        for i in range(1, 6):
            attack_left_image_path = os.path.join('assets', 'sprites', 'Samurai_AttackLeft', f'Samurai_AttackLeft_Sequence{i}.png')
            if os.path.exists(attack_left_image_path):
                image = pygame.image.load(attack_left_image_path).convert_alpha()
                image = pygame.transform.flip(image, True, False)
                self.animations["attack_left"].append(image)
            else:
                raise FileNotFoundError(f"No file '{attack_left_image_path}' found.")
        
        for i in range(1, 6):
            attack_up_image_path = os.path.join('assets', 'sprites', 'Samurai_AttackUp', f'Samurai_AttackUp_Sequence{i}.png')
            if os.path.exists(attack_up_image_path):
                image = pygame.image.load(attack_up_image_path).convert_alpha()
                self.animations["attack_up"].append(image)
            else:
                raise FileNotFoundError(f"No file '{attack_up_image_path}' found.")
        
        for i in range(1, 6):
            attack_down_image_path = os.path.join('assets', 'sprites', 'Samurai_AttackDown', f'Samurai_AttackDown_Sequence{i}.png')
            if os.path.exists(attack_down_image_path):
                image = pygame.image.load(attack_down_image_path).convert_alpha()
                self.animations["attack_down"].append(image)
            else:
                raise FileNotFoundError(f"No file '{attack_down_image_path}' found.")

        # Initialiser l'image et le rectangle du personnage
        self.image = self.animations["repos"][0] if self.animations["repos"] else None
        self.rect = self.image.get_rect() if self.image else pygame.Rect(self.position[0], self.position[1], 0, 0)

    def placer_sur_ecran(self, x, y):
        self.position = (x, y)
        self.rect.topleft = (x, y)

    def deplacer(self, direction, carte_largeur, carte_hauteur):
        if not self.is_attacking:  # Ne pas permettre de se déplacer pendant l'attaque
            x, y = self.position

            if direction == "right":
                x += self.vitesse
                self.animation = "run_right"
            elif direction == "left":
                x -= self.vitesse
                self.animation = "run_left"
            elif direction == "up":
                y -= self.vitesse
                self.animation = "run_up"
            elif direction == "down":
                y += self.vitesse
                self.animation = "run_down"
            elif direction == "stop":
                self.animation = "repos"
            
            # Assurer que le personnage reste dans les limites de la carte
            x = max(0, min(x, carte_largeur - self.rect.width))
            y = max(0, min(y, carte_hauteur - self.rect.height))

            self.position = (x, y)
            self.rect.topleft = (x, y)

    def attaquer(self, direction):
        self.is_attacking = True
        self.current_frame = 0  # Réinitialiser l'animation d'attaque
        if direction == "right":
            self.animation = "attack_right"
        elif direction == "left":
            self.animation = "attack_left"
        elif direction == "up":
            self.animation = "attack_up"
        elif direction == "down":
            self.animation = "attack_down"

    def recevoir_degats(self, degats):
        degats -= self.armure
        degats = max(0, degats)  # Les dégâts ne peuvent pas être négatifs
        self.hp -= degats
        if self.hp <= 0:
            self.hp = 0
            # Gestion de la mort du personnage (par exemple, fin du jeu ou réinitialisation)

    def draw(self, surface, camera_x, camera_y):
        if self.image:
            # Dessiner le personnage
            surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))
            # Dessiner la hitbox
            pygame.draw.rect(surface, (0, 255, 0),  # Couleur verte pour la hitbox
                            pygame.Rect(self.rect.x - camera_x, self.rect.y - camera_y, self.rect.width, self.rect.height), 2)



    def update(self, monsters):
        # Mise à jour de l'animation
        if self.animation == "repos":
            self.image = self.animations["repos"][0] if self.animations["repos"] else None
        elif self.animation in ["run_right", "run_left", "run_up", "run_down"]:
            if self.animations[self.animation]:
                self.current_frame += 1
                if self.current_frame >= len(self.animations[self.animation]) * self.frame_delay:
                    self.current_frame = 0
                self.image = self.animations[self.animation][self.current_frame // self.frame_delay]
        elif self.animation.startswith("attack"):
            if self.animations[self.animation]:
                self.current_frame += 1
                if self.current_frame >= len(self.animations[self.animation]) * self.frame_delay:
                    self.current_frame = 0
                    self.is_attacking = False  # Fin de l'attaque
                    self.animation = "repos"
                self.image = self.animations[self.animation][self.current_frame // self.frame_delay]

                # Vérifier les collisions avec les monstres pendant l'attaque
        if self.is_attacking:
            for monster in monsters:
                if self.animation == "attack_right" and self.rect.colliderect(pygame.Rect(monster.rect.left, monster.rect.top, monster.rect.width, monster.rect.height)):
                    monster.recevoir_degats(self.attaque)
                elif self.animation == "attack_left" and self.rect.colliderect(pygame.Rect(monster.rect.left, monster.rect.top, monster.rect.width, monster.rect.height)):
                    monster.recevoir_degats(self.attaque)
                elif self.animation == "attack_up" and self.rect.colliderect(pygame.Rect(monster.rect.left, monster.rect.top, monster.rect.width, monster.rect.height)):
                    monster.recevoir_degats(self.attaque)
                elif self.animation == "attack_down" and self.rect.colliderect(pygame.Rect(monster.rect.left, monster.rect.top, monster.rect.width, monster.rect.height)):
                    monster.recevoir_degats(self.attaque)

        # Assurer que l'image est mise à jour après chaque animation
        if self.image:
            self.rect.size = self.image.get_size()
