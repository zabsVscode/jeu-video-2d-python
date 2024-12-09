import pygame
import random
import os

class Monstre(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y, buff, nom):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.buff = buff
        self.nom = nom
        self.hp_max = 50
        self.hp = self.hp_max
        self.alive = True
        self.armure = 0
        
        # Définir les dimensions de la hitbox (à ajuster selon les besoins)
        self.hitbox_width = self.rect.width // 2
        self.hitbox_height = self.rect.height // 2
        
        # Créer la hitbox avec les dimensions réduites
        self.hitbox = pygame.Rect(
            self.rect.x + self.rect.width // 4, 
            self.rect.y + self.rect.height // 4, 
            self.hitbox_width, 
            self.hitbox_height
        )

    def update(self):
        # Mettre à jour la position de la hitbox pour qu'elle suive la position du rect du monstre
        self.hitbox.topleft = (self.rect.x + self.rect.width // 4, self.rect.y + self.rect.height // 4)

    def draw_name(self, surface, camera_x, camera_y):
        font = pygame.font.Font(None, 36)
        text = font.render(self.nom, True, (255, 255, 255))
        text_rect = text.get_rect()
        
        # Positionner le texte en haut à droite de l'écran
        x = surface.get_width() - text_rect.width - 70
        y = 40
        
        surface.blit(text, (x, y))

    def draw(self, surface, camera_x, camera_y):
        if self.alive:
            surface.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))
            
            # Mettre à jour la position de la hitbox avant de la dessiner
            self.update()
            
            # Dessiner la hitbox
            pygame.draw.rect(surface, (255, 0, 0), 
                             pygame.Rect(self.hitbox.x - camera_x, self.hitbox.y - camera_y, self.hitbox.width, self.hitbox.height), 2)

    def recevoir_degats(self, degats):
        print(f"Monstre {self.nom} reçoit {degats} dégâts.")
        self.hp -= degats
        if self.hp <= 0:
            self.hp = 0
            self.alive = False
            print(f"Monstre {self.nom} est mort. Buff: {self.buff}")
            return self.buff
        return None

def create_monsters(carte_largeur, carte_hauteur, count):
    monsters = []
    monster_image_paths = [
        'assets/sprites/Monstres/Monstre Electrique - Metardi - (Dps)/Metard.png',
        'assets/sprites/Monstres/Monstre Electrique - Metardi - (Dps)/Metardi.png',
        'assets/sprites/Monstres/Monstre Insecte - Scorpy - (Vitesse DPS)/Scor.png',
        'assets/sprites/Monstres/Monstre Insecte - Scorpy - (Vitesse DPS)/Scorpy.png',
        'assets/sprites/Monstres/Monstre Nature - Evoliou - (Health)/Evo.png',
        'assets/sprites/Monstres/Monstre Nature - Evoliou - (Health)/Evoliou.png',
        'assets/sprites/Monstres/Monstre Pierre - Piery - (Armure)/Pier.png',
        'assets/sprites/Monstres/Monstre Pierre - Piery - (Armure)/Piery.png',
        'assets/sprites/Monstres/Monstre Vitesse - Vitas - (Vitesse)/Vi.png',
        'assets/sprites/Monstres/Monstre Vitesse - Vitas - (Vitesse)/Vitas.png',
        'assets/sprites/Monstres/Balk.png',
        'assets/sprites/Monstres/Bermite.png',
        'assets/sprites/Monstres/Craby.png',
        'assets/sprites/Monstres/Natours.png',
    ]

    buffs = {
        'Metard.png': 'dps',
        'Metardi.png': 'dps',
        'Scor.png': 'vitesse dps',
        'Scorpy.png': 'vitesse dps',
        'Evo.png': 'health',
        'Evoliou.png': 'health',
        'Pier.png': 'armure',
        'Piery.png': 'armure',
        'Vi.png': 'vitesse',
        'Vitas.png': 'vitesse'
    }

    names = {
        'Metard.png': 'Metard',
        'Metardi.png': 'Metardi',
        'Scor.png': 'Scorp',
        'Scorpy.png': 'Scorpy',
        'Evo.png': 'Evo',
        'Evoliou.png': 'Evoliou',
        'Pier.png': 'Pier',
        'Piery.png': 'Piery',
        'Vi.png': 'Vi',
        'Vitas.png': 'Vitas'
    }

    for i in range(count):
        image_path = random.choice(monster_image_paths)
        buff = None
        for key in buffs:
            if key in image_path:
                buff = buffs[key]
                break
        
        nom = names.get(os.path.basename(image_path), 'Monstre Inconnu')

        x = random.randint(0, carte_largeur - 50)
        y = random.randint(0, carte_hauteur - 50)

        monster = Monstre(image_path, x, y, buff, nom)
        monsters.append(monster)

    return monsters
