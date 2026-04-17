from constants import *
from lemming import lemmingsLIST

def transitionChute(lemming, time):
   """Depuis EtatChute : détecte le sol sous le lemming.
   Si sol → Marche (chute ok) ou Dead (chute trop haute).
   Si hors fenêtre par le bas → Dead."""
   if lemming['y'] > 400:
      lemming['etat'] = EtatDead
      return
   px = int(lemming['x'] + LARG // 2)
   py = int(lemming['y'] + HAUT)
   if 0 <= px < 800 and 0 <= py < 400:
      if fond.get_at((px, py)) != (0, 0, 0):
         if lemming['fallcount'] >= FALL_LIMIT:
            lemming['etat'] = EtatDead
         else:
            lemming['etat']      = EtatMarche
            lemming['fallcount'] = 0

def transitionMarche(lemming, time):
   """Depuis EtatMarche :
   - vide sous les pieds → Chute
   - mur devant → demi-tour
   - Blocker  → demi-tour"""

   # vide sous les pieds → chute
   px = int(lemming['x'] + LARG // 2)
   py = int(lemming['y'] + HAUT)
   if 0 <= px < 800 and 0 <= py < 400:
      if fond.get_at((px, py)) == (0, 0, 0):
         lemming['etat']      = EtatFlotte if lemming['floater'] else EtatChute
         lemming['fallcount'] = 0
         return

   # mur devant le lemming : teste toute la colonne frontale sur la hauteur du lemming (hors pixels de sol)
   px_devant = int(lemming['x']) if lemming['vx'] == -1 else int(lemming['x'] + LARG)
   mur_detecte = False
   for dy in range(HAUT - 2):
      py_devant = int(lemming['y'] + dy)
      if 0 <= px_devant < 800 and 0 <= py_devant < 400:
         if fond.get_at((px_devant, py_devant)) != (0, 0, 0):
            mur_detecte = True
            break
   if mur_detecte:
      if lemming['climber']:
         lemming['etat'] = EtatGrimpe
      else:
         lemming['vx'] = -lemming['vx']   # non grimpeur → demi-tour

   # collision avec un Blocker
   for autre in lemmingsLIST:
      if autre['etat'] in (EtatStop, EtatBomb):
         if abs(lemming['x'] - autre['x']) < LARG and abs(lemming['y'] - autre['y']) < HAUT:
            if autre['x'] < lemming['x'] and lemming['vx'] == -1:
               lemming['vx'] = 1
            elif autre['x'] > lemming['x'] and lemming['vx'] == 1:
               lemming['vx'] = -1

def transitionCreuse(lemming, time):
   """Depuis EtatCreuse :
   - hors fenêtre par le bas → Dead
   - 20 pixels sous le lemming tous noirs → Marche"""
   if lemming['y'] + HAUT >= 400:
      lemming['etat'] = EtatDead
      return
   all_black = True
   for dy in range(20):
      for dx in range(LARG):
         px = int(lemming['x']) + dx
         py = int(lemming['y']) + HAUT + dy
         if 0 <= px < 800 and 0 <= py < 400:
            if fond.get_at((px, py))[:3] != (0, 0, 0):
               all_black = False
               break
   if all_black:
      lemming['etat'] = EtatMarche

def transitionBash(lemming, time):
   """Depuis EtatBash :
   - hors fenêtre par le côté vx → Dead
   - colonne devant (HAUT pixels) toute noire → Marche"""
   if lemming['vx'] == -1 and lemming['x'] <= 0:
      lemming['etat'] = EtatDead
      return
   if lemming['vx'] == 1 and lemming['x'] + LARG >= 800:
      lemming['etat'] = EtatDead
      return
   px_devant = int(lemming['x']) if lemming['vx'] == -1 else int(lemming['x'] + LARG)
   all_black = True
   for dy in range(HAUT):
      py = int(lemming['y']) + dy
      if 0 <= py < 400:
         if fond.get_at((px_devant, py))[:3] != (0, 0, 0):
            all_black = False
            break
   if all_black:
      lemming['etat'] = EtatMarche

def transitionGrimpe(lemming, time):
   """Depuis EtatGrimpe :
   - pixel du côté vx est noir (plus de mur) → sommet atteint → EtatMarche
   - pixel au-dessus coloré (plafond) → EtatMarche"""
   px_mur = int(lemming['x']) if lemming['vx'] == -1 else int(lemming['x'] + LARG)
   py_mur = int(lemming['y'] + HAUT // 2)
   if 0 <= px_mur < 800 and 0 <= py_mur < 400:
      if fond.get_at((px_mur, py_mur)) == (0, 0, 0):
         lemming['etat'] = EtatMarche
         return

   px_haut = int(lemming['x'] + LARG // 2)
   py_haut = int(lemming['y'] - 1)
   if 0 <= px_haut < 800 and 0 <= py_haut < 400:
      if fond.get_at((px_haut, py_haut)) != (0, 0, 0):
         lemming['etat'] = EtatMarche

def transitionFlotte(lemming, time):
   """Depuis EtatFlotte : sol détecté sous le lemming → Marche.
   Si hors fenêtre par le bas → Dead."""
   if lemming['y'] > 400:
      lemming['etat'] = EtatDead
      return
   px = int(lemming['x'] + LARG // 2)
   py = int(lemming['y'] + HAUT)
   if 0 <= px < 800 and 0 <= py < 400:
      if fond.get_at((px, py)) != (0, 0, 0):
         lemming['etat']      = EtatMarche
         lemming['fallcount'] = 0

def transitionMine(lemming, time):
   """Depuis EtatMine :
   - hors fenêtre → Dead
   - zone diagonale devant tout noire → Marche"""
   if lemming['y'] + HAUT >= 400 or lemming['x'] <= 0 or lemming['x'] + LARG >= 800:
      lemming['etat'] = EtatDead
      return
   px_diag = int(lemming['x']) if lemming['vx'] == -1 else int(lemming['x'] + LARG)
   py_diag = int(lemming['y'] + HAUT)
   all_black = True
   for dy in range(HAUT // 2):
      py = py_diag + dy
      if 0 <= py < 400:
         if fond.get_at((px_diag, py))[:3] != (0, 0, 0):
            all_black = False
            break
   if all_black:
      lemming['etat'] = EtatMarche

def transitionBomb(lemming, time):
   """Depuis EtatBomb : le lemming attend 5 secondes.
   Quand le timer expire → détruit le terrain autour → EtatExplose."""
   if time - lemming['bomb_start_time'] >= 50:
      cx = int(lemming['x'] + LARG // 2)
      cy = int(lemming['y'] + HAUT // 2)
      for dy in range(-BOMB_RADIUS, BOMB_RADIUS + 1):
         for dx in range(-BOMB_RADIUS, BOMB_RADIUS + 1):
            if dx*dx + dy*dy <= BOMB_RADIUS * BOMB_RADIUS:
               px, py = cx + dx, cy + dy
               if 0 <= px < 800 and 0 <= py < 400:
                  fond.set_at((px, py), (0, 0, 0))
      lemming['etat']          = EtatExplose
      lemming['explode_frame'] = 0

def transitionExplose(lemming, time):
   """Depuis EtatExplose : quand l'animation est terminée → EtatDead."""
   if lemming['explode_frame'] >= len(bomber):
      lemming['etat'] = EtatDead

def transitionBuild(lemming, time):
   """Depuis EtatBuild : 12 marches posées → EtatMarche. Hors fenêtre → EtatDead."""
   if lemming['x'] <= 0 or lemming['x'] + LARG >= 800 or lemming['y'] <= 0:
      lemming['etat'] = EtatDead
      return
   if lemming['build_step'] >= BUILD_STEPS:
      lemming['etat']       = EtatMarche
      lemming['build_step'] = 0

def transitionStop(lemming, time):
   """EtatStop est terminal : aucune transition possible."""
   pass

def transitionDead(lemming, time):
   """EtatDead est terminal : aucune transition possible."""
   pass
