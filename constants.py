import pygame
import numpy as np
import os, inspect
import random
import pygame.surfarray as surfarray


scriptPATH = os.path.abspath(inspect.getsourcefile(lambda:0))
scriptDIR  = os.path.dirname(scriptPATH)
assets     = os.path.join(scriptDIR, "data")

# chargement des images (avant pygame.init car pas besoin de l'écran)
fond            = pygame.image.load(os.path.join(assets, "map.png"))
planche_sprites = pygame.image.load(os.path.join(assets, "planche.png"))
planche_sprites.set_colorkey((0, 0, 0))
sortie = pygame.image.load(os.path.join(assets, "sortie.png"))

# dimensions d'un sprite (largeur × hauteur)
LARG = 30
HAUT = 32

def ChargeSerieSprites(id):
   """Charge une ligne d'animation depuis la planche de sprites.
   Arrête au premier sprite rouge (case vide)."""
   sprite = []
   for i in range(18):
      spr  = planche_sprites.subsurface((LARG * i, LARG * id, LARG, LARG))
      test = spr.get_at((10, 10))
      if test != (255, 0, 0, 255):   # case rouge = fin de l'animation
         sprite.append(spr)
   return sprite


pygame.init()

WINDOW_SIZE = [800, 400]
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("LEMMINGS")

clock         = pygame.time.Clock()
font_win      = pygame.font.SysFont(None, 120)  # police WIN / LOSE
font_compteur = pygame.font.SysFont(None, 36)   # police compteur de lemmings
font_bombe    = pygame.font.SysFont(None, 22)   # police compte à rebours bomber

# ─── ÉTATS ───────────────────────────────────────────────────────────────────
EtatMarche  = 'EtatMarche'
EtatChute   = 'EtatChute'
EtatStop    = 'EtatStop'
EtatDead    = 'EtatDead'
EtatCreuse  = 'EtatCreuse'
EtatFlotte  = 'EtatFlotte'
EtatGrimpe  = 'EtatGrimpe'
EtatBash    = 'EtatBash'
EtatMine    = 'EtatMine'
EtatBomb    = 'EtatBomb'
EtatExplose = 'EtatExplose'
EtatBuild   = 'EtatBuild'

# ─── CONSTANTES DE JEU ───────────────────────────────────────────────────────
FALL_LIMIT  = 100
BOMB_RADIUS = 30
BUILD_W     = 8
BUILD_H     = 2
BUILD_STEPS = 20
BRICK_COLOR = (80, 200, 80)

# ─── SPRITES ─────────────────────────────────────────────────────────────────
marche   = ChargeSerieSprites(0)
tombe    = ChargeSerieSprites(1)
grimpe   = ChargeSerieSprites(2)
flotte   = ChargeSerieSprites(3)
blocker  = ChargeSerieSprites(4)
bomber   = ChargeSerieSprites(5)
basher   = ChargeSerieSprites(8)
miner    = ChargeSerieSprites(9)
creuse   = ChargeSerieSprites(7)
builder  = ChargeSerieSprites(6)
dead     = ChargeSerieSprites(10)

# sprite marche droite = miroir horizontal de marche gauche
marche_droite = [pygame.transform.flip(spr, True, False) for spr in marche]

# ─── INTERFACE ICÔNES ────────────────────────────────────────────────────────
icones = {
   'Blocker'   : (pygame.Rect(190, 342, 44, 55), pygame.Rect(193, 345, 36, 13)),
   'Creuser'   : (pygame.Rect(241, 344, 42, 52), pygame.Rect(244, 345, 37, 13)),
   'Climber'   : (pygame.Rect(281, 358, 49, 40), pygame.Rect(291, 345, 36, 14)),
   'Floater'   : (pygame.Rect(336, 344, 41, 52), pygame.Rect(338, 346, 36, 12)),
   'Bomber'    : (pygame.Rect(385, 345, 40, 51), pygame.Rect(387, 347, 35, 11)),
   'Apt6'      : (pygame.Rect(432, 344, 41, 52), pygame.Rect(435, 346, 35, 12)),
   'Basher'    : (pygame.Rect(479, 343, 45, 54), pygame.Rect(481, 347, 38, 10)),
   'Miner'     : (pygame.Rect(519, 357, 51, 39), pygame.Rect(532, 346, 35, 11)),
   'MegaBomber': (pygame.Rect(567, 357, 50, 39), pygame.Rect(580, 346, 35,  9)),
}

# ─── PORTE DE SORTIE ─────────────────────────────────────────────────────────
SORTIE_X = 657 - sortie.get_width()  // 2
SORTIE_Y = 322 - sortie.get_height()
