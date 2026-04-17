from constants import *

def actionChute(lemming, time):
   """Le lemming tombe de 3 pixels par frame et incrémente son compteur de chute."""
   lemming['y']         += 3
   lemming['fallcount'] += 3

def actionMarche(lemming, time):
   """Le lemming avance horizontalement selon sa vitesse vx (+1 ou -1)."""
   lemming['x'] += lemming['vx']

def actionCreuse(lemming, time):
   """Toutes les 0.2s : efface une rangée LARG×1 pixels sous le lemming
   et descend d'un pixel pour suivre le trou creusé."""
   if time - lemming['last_dig_time'] >= 2:
      for dy in range(HAUT - LARG + 1):
         for dx in range(LARG):
            px = int(lemming['x']) + dx
            py = int(lemming['y']) + LARG + dy
            if 0 <= px < 800 and 0 <= py < 400:
               fond.set_at((px, py), (0, 0, 0))
      lemming['y']            += 1
      lemming['last_dig_time'] = time

def actionGrimpe(lemming, time):
   """Le lemming grimpe le long du mur : monte de 2 pixels par frame."""
   lemming['y'] -= 2

def actionFlotte(lemming, time):
   """Le lemming descend lentement (1px/frame) grâce au parapluie."""
   lemming['y'] += 1

def actionBash(lemming, time):
   """Toutes les 0.2s : efface une colonne HAUT×1 pixel devant le lemming
   et avance d'un pixel dans la direction vx."""
   if time - lemming['last_dig_time'] >= 2:
      px_devant = int(lemming['x']) if lemming['vx'] == -1 else int(lemming['x'] + LARG)
      for dy in range(HAUT):
         py = int(lemming['y']) + dy
         if 0 <= px_devant < 800 and 0 <= py < 400:
            fond.set_at((px_devant, py), (0, 0, 0))
      lemming['x']            += lemming['vx']
      lemming['last_dig_time'] = time

def actionMine(lemming, time):
   """Toutes les 0.2s : efface une zone diagonale puis avance d'un pixel en x et descend en y."""
   if time - lemming['last_dig_time'] >= 2:
      px_diag = int(lemming['x']) if lemming['vx'] == -1 else int(lemming['x'] + LARG)
      for dy in range(HAUT // 2):
         py = int(lemming['y'] + LARG) + dy
         if 0 <= px_diag < 800 and 0 <= py < 400:
            fond.set_at((px_diag, py), (0, 0, 0))
      for gap in range(HAUT - LARG + 1):
         for dx in range(LARG):
            px = int(lemming['x']) + dx
            py = int(lemming['y'] + LARG) + gap
            if 0 <= px < 800 and 0 <= py < 400:
               fond.set_at((px, py), (0, 0, 0))
      lemming['x']            += lemming['vx']
      lemming['y']            += 1
      lemming['last_dig_time'] = time

def actionBomb(lemming, time):
   """Le lemming reste immobile pendant le décompte."""
   pass

def actionExplose(lemming, time):
   """EtatExplose : animation pure, aucun déplacement."""
   pass

def actionBuild(lemming, time):
   """Toutes les 0.3s : pose une marche de briques aux pieds, avance et monte."""
   if time - lemming['last_dig_time'] >= 3:
      bx = int(lemming['x'] + (LARG if lemming['vx'] == 1 else 0))
      by = int(lemming['y'] + HAUT - BUILD_H)
      for dy in range(BUILD_H + 1):
         for dx in range(BUILD_W):
            px = bx + lemming['vx'] * dx
            py = by + dy
            if 0 <= px < 800 and 0 <= py < 400:
               fond.set_at((px, py), BRICK_COLOR)
      lemming['x']            += lemming['vx'] * BUILD_W
      lemming['y']            -= BUILD_H
      lemming['build_step']   += 1
      lemming['last_dig_time'] = time

def actionStop(lemming, time):
   """EtatStop est terminal : aucune action."""
   pass

def actionDead(lemming, time):
   """EtatDead est terminal : aucune action."""
   pass
