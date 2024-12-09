import pygame
import random
import json
import os
from personnage import Personnage
from monstre import Monstre, create_monsters

class Carte:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.carte_largeur = 3500
        self.carte_hauteur = 3500
        self.taille_case = 24

        self.couleur_ciel = (255, 255, 255)
        self.afficher_nom = None

        # Charger les sprites
        self.sprites = self.load_sprites()

        # Initialisation de la matrice de la carte
        self.carte = [[0] * (self.carte_largeur // self.taille_case) for _ in range(self.carte_hauteur // self.taille_case)]

        # Liste pour les arbres
        self.trees = []

        # Charger une carte préexistante ou générer une nouvelle carte
        if os.path.exists('map.json'):
            self.load_map_from_file('map.json')
        else:
            self.generate_map()
            self.save_map_to_file('map.json')

        self.initialize_character()
        self.initialize_monsters()

    def load_sprites(self):
        sprite_paths = {
            'Herbe': 'assets/sprites/Map/Decors/Herbe.png',
            'Tree': 'assets/sprites/Map/Decors/Tree.png',
        }

        sprites = {}
        for name, path in sprite_paths.items():
            try:
                image = pygame.image.load(path).convert_alpha()
                sprites[name] = image
            except FileNotFoundError:
                print(f"Fichier non trouvé : {path}")
        return sprites

    def generate_map(self):
        """Génère une carte avec de l'herbe et ajoute des arbres spécifiques."""
        largeur = self.carte_largeur // self.taille_case
        hauteur = self.carte_hauteur // self.taille_case

        self.carte = [['Herbe'] * largeur for _ in range(hauteur)]

        # Ajouter des arbres à des positions spécifiques
        self.trees = [
            (5, 5), (10, 10), (15, 15)  # Liste d'exemple, à ajuster selon vos besoins
        ]

        for x, y in self.trees:
            if 0 <= x < largeur and 0 <= y < hauteur:
                self.carte[y][x] = 'Tree'

    def save_map_to_file(self, filename):
        """Sauvegarde la carte dans un fichier JSON."""
        with open(filename, 'w') as f:
            json.dump(self.carte, f)

    def load_map_from_file(self, filename):
        """Charge la carte depuis un fichier JSON."""
        with open(filename, 'r') as f:
            self.carte = json.load(f)
            # Charger les positions des arbres depuis la carte si disponibles
            self.trees = [(x, y) for y, row in enumerate(self.carte) for x, cell in enumerate(row) if cell == 'Tree']

    def position_trop_proche(self, x, y, distance_minimale=200):
        px, py = self.personnage.position
        return (abs(px - x) < distance_minimale) and (abs(py - y) < distance_minimale)

    def initialize_character(self):
        self.personnage = Personnage(self.screen, "Samurai")
        self.personnage.placer_sur_ecran(self.screen_width // 2, self.screen_height // 2)

    def initialize_monsters(self):
        self.monsters = pygame.sprite.Group()
        monsters = create_monsters(self.carte_largeur, self.carte_hauteur, 10)
        for monster in monsters:
            if not self.position_trop_proche(monster.rect.x, monster.rect.y):
                self.monsters.add(monster)

    def draw_health_bar(self, surface, x, y, hp, hp_max, armure):
        health_bar_length = 200
        health_bar_height = 20
        fill = (hp / hp_max) * health_bar_length
        border_color = (0, 0, 0)
        fill_color = (0, 255, 0)

        pygame.draw.rect(surface, border_color, (x, y, health_bar_length, health_bar_height))
        pygame.draw.rect(surface, fill_color, (x, y, fill, health_bar_height))

        if armure > 0:
            shield_height = 10
            shield_width = min((armure / 100) * health_bar_length, health_bar_length)
            shield_color = (0, 0, 255)
            pygame.draw.rect(surface, shield_color, (x, y - shield_height, shield_width, shield_height))

    def draw_health_bar_for_monster(self, surface, x, y, hp, hp_max):
        health_bar_length = 200
        health_bar_height = 20
        fill = (hp / hp_max) * health_bar_length
        border_color = (0, 0, 0)
        fill_color = (255, 0, 0)

        x_bar = self.screen_width - health_bar_length - 10
        y_bar = 10

        pygame.draw.rect(surface, border_color, (x_bar, y_bar, health_bar_length, health_bar_height))
        pygame.draw.rect(surface, fill_color, (x_bar, y_bar, fill, health_bar_height))

    def draw_map(self, surface, camera_x, camera_y):
        """Dessine la carte basée sur la matrice en remplissant l'écran avec de l'herbe comme fond."""
        # Calculer les indices de la carte visibles en fonction de la caméra
        start_x = max(0, camera_x // self.taille_case)
        start_y = max(0, camera_y // self.taille_case)
        end_x = min(len(self.carte[0]), (camera_x + self.screen_width) // self.taille_case + 1)
        end_y = min(len(self.carte), (camera_y + self.screen_height) // self.taille_case + 1)

        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                # Calculer la position du sprite en fonction de la caméra
                sprite_x = x * self.taille_case - camera_x
                sprite_y = y * self.taille_case - camera_y
                
                # Dessiner le sprite correspondant au type de case
                if self.carte[y][x] in self.sprites:
                    surface.blit(self.sprites[self.carte[y][x]], (sprite_x, sprite_y))
                else:
                    # Dessiner de l'herbe si aucun sprite spécifique n'est présent
                    surface.blit(self.sprites['Herbe'], (sprite_x, sprite_y))

        # Dessiner les arbres (en utilisant la liste des positions spécifiques)
        for x, y in self.trees:
            tree_x = x * self.taille_case - camera_x
            tree_y = y * self.taille_case - camera_y
            surface.blit(self.sprites['Tree'], (tree_x, tree_y))

    def update(self):
        camera_x = max(0, min(self.personnage.position[0] - self.screen_width // 2, self.carte_largeur - self.screen_width))
        camera_y = max(0, min(self.personnage.position[1] - self.screen_height // 2, self.carte_hauteur - self.screen_height))

        # Créer une surface de fond pour le double buffering
        buffer_surface = pygame.Surface((self.screen_width, self.screen_height))
        buffer_surface.fill(self.couleur_ciel)  # Remplir le fond avec la couleur du ciel

        # Dessiner la carte sur la surface de fond
        self.draw_map(buffer_surface, camera_x, camera_y)

        # Mettre à jour les animations du personnage
        self.personnage.update(self.monsters)

        # Dessiner le personnage
        buffer_surface.blit(self.personnage.image, 
                            (self.personnage.rect.x - camera_x, 
                             self.personnage.rect.y - camera_y))

        # Dessiner la barre de santé du personnage
        self.draw_health_bar(buffer_surface, 10, 10, 
                            self.personnage.hp, self.personnage.hp_max, self.personnage.armure)

        # Dessiner les monstres
        for monster in self.monsters:
            monster.update()
            monster.draw(buffer_surface, camera_x, camera_y)
            monster_x = monster.rect.x - camera_x
            monster_y = monster.rect.y - camera_y
            self.draw_health_bar_for_monster(buffer_surface, monster_x, monster_y, monster.hp, monster.hp_max)

        # Copier le buffer à l'écran
        self.screen.blit(buffer_surface, (0, 0))
        pygame.display.flip()

    def handle_collisions(self):
        self.afficher_nom = None

        for monster in self.monsters:
            if monster.alive and self.personnage.rect.colliderect(monster.rect):
                if self.personnage.is_attacking:
                    buff = monster.recevoir_degats(self.personnage.attaque)
                    if buff:
                        self.apply_buff(buff)
                        print(f"Buff {buff} appliqué.")
                        print(f"Monstre {monster.nom} reçoit {self.personnage.attaque} dégâts. HP restants: {monster.hp}")
                else:
                    degats = 10
                    if hasattr(self.personnage, 'armure'):
                        degats = max(0, degats - self.personnage.armure)
                    self.personnage.recevoir_degats(degats)
                    print(f"Personnage reçoit {degats} dégâts. HP restants: {self.personnage.hp}")

                if monster.alive:
                    self.afficher_nom = monster.nom

    def apply_buff(self, buff):
        if buff == "dps":
            self.personnage.attaque += 5
        elif buff == "vitesse":
            self.personnage.vitesse += 2
        elif buff == "health":
            self.personnage.hp_max += 20
            self.personnage.hp = self.personnage.hp_max
        elif buff == "armure":
            self.personnage.armure += 5
