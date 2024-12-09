# Jeu Vidéo 2D - Pygame

## Description

Ce projet consiste en la création d'un jeu vidéo 2D en utilisant **Pygame**, où le joueur contrôle un personnage principal avec la possibilité de se déplacer, attaquer et interagir avec des ennemis. Les ennemis ont des comportements et des capacités variées, et le système de combat est basé sur des attaques physiques avec gestion des dégâts, de la santé et de l'armure. Ce projet inclut également la gestion des animations pour le personnage et les ennemis, ainsi qu'un système de caméra pour un monde de jeu étendu.

## Fonctionnalités

- **Personnage jouable** : Animations de repos, de déplacement et d'attaque dans 4 directions.
- **Système de combat** : Attaques infligeant des dégâts aux ennemis et gestion des buffs (dégâts, vitesse, armure, etc.).
- **Monstres variés** : Plusieurs types de monstres avec différents buffs et comportements.
- **Gestion des collisions** : Détection des collisions entre le personnage et les ennemis pendant les déplacements et les attaques.
- **Caméra dynamique** : Suivi du personnage dans un monde de jeu plus vaste.

## Prérequis

Avant de lancer le projet, assure-toi d'avoir **Python** et la bibliothèque **Pygame** installés. 

### Installation de Pygame

Si tu n'as pas encore installé Pygame, tu peux le faire via `pip` :

```bash
pip install pygame




LANCER LE PROJET




Étape 1 : Cloner le projet
Si tu n'as pas encore cloné le projet, fais-le en utilisant Git :

bash
Copier le code
git clone https://github.com/ton-compte/jeu-video-2d-pygame.git
cd jeu-video-2d-pygame




Étape 2 : 

Préparer les ressources
Le jeu utilise des ressources graphiques images d'animations qui doivent être présentes dans les répertoires suivants :

assets/sprites/Samurai_Repos/
assets/sprites/Samurai_RunRight/
assets/sprites/Samurai_RunLeft/
assets/sprites/Samurai_RunUp/
assets/sprites/Samurai_RunDown/
assets/sprites/Samurai_AttackRight/
assets/sprites/Samurai_AttackLeft/
assets/sprites/Samurai_AttackUp/
assets/sprites/Samurai_AttackDown/
assets/sprites/Monstres/ (Monstres divers, par exemple, Metardi, Scorpy, etc.)
Assure-toi que ces fichiers sont bien présents dans ton répertoire de travail. Sinon, les animations ne se chargeront pas correctement.




Étape 3 : 

Lancer le jeu
Une fois tout configuré, tu peux lancer le jeu avec le fichier Python principal. Ouvre un terminal dans le répertoire du projet et exécute la commande suivante :

bash
Copier le code
python main.py
Cela démarrera le jeu dans une fenêtre où tu pourras contrôler le personnage et interagir avec les ennemis.




Étape 4 : 

Commandes du joueur
Flèches directionnelles ou Touches WASD : Déplacement du personnage dans les quatre directions.
Touches ZQSD : Alternatif pour les touches de direction.
Espace : Attaque dans la direction actuelle.
#   j e u - v i d e o - 2 d - p y t h o n  
 