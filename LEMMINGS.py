from constants import *
from lemming import lemmingsLIST, creerLemming
from transitions import *
from actions import *
from affichage import *

# ─── DICTS D'ÉTATS ───────────────────────────────────────────────────────────
Transitions = {
   EtatChute  : transitionChute,
   EtatMarche : transitionMarche,
   EtatGrimpe : transitionGrimpe,
   EtatFlotte : transitionFlotte,
   EtatCreuse : transitionCreuse,
   EtatBash   : transitionBash,
   EtatMine   : transitionMine,
   EtatBomb   : transitionBomb,
   EtatExplose: transitionExplose,
   EtatBuild  : transitionBuild,
   EtatStop   : transitionStop,
   EtatDead   : transitionDead,
}

Actions = {
   EtatChute  : actionChute,
   EtatMarche : actionMarche,
   EtatGrimpe : actionGrimpe,
   EtatFlotte : actionFlotte,
   EtatCreuse : actionCreuse,
   EtatBash   : actionBash,
   EtatMine   : actionMine,
   EtatBomb   : actionBomb,
   EtatExplose: actionExplose,
   EtatBuild  : actionBuild,
   EtatStop   : actionStop,
   EtatDead   : actionDead,
}

Affichages = {
   EtatChute  : afficheChute,
   EtatMarche : afficheMarche,
   EtatGrimpe : afficheGrimpe,
   EtatFlotte : afficheFlotte,
   EtatCreuse : afficheCreuse,
   EtatBash   : afficheBash,
   EtatMine   : afficheMine,
   EtatBomb   : afficheBomb,
   EtatExplose: afficheExplose,
   EtatBuild  : afficheBuild,
   EtatStop   : afficheStop,
   EtatDead   : afficheDead,
}

# ─── VARIABLES DE JEU ────────────────────────────────────────────────────────
aptitude_active   = None
compteur_creation = 0
survivants        = 0

# ─── BOUCLE PRINCIPALE ───────────────────────────────────────────────────────
done = False
pygame.mouse.set_visible(1)

while not done:
   event = pygame.event.Event(pygame.USEREVENT)
   time  = int(pygame.time.get_ticks() / 100)

   screen.blit(fond, (0, 0))

   # création des lemmings
   if compteur_creation < 15 and (time + compteur_creation) % 15 == 0:
      compteur_creation += 1
      creerLemming(time)

   # ── gestion des événements ──────────────────────────────────────────────
   for event in pygame.event.get():

      if event.type == pygame.QUIT:
         done = True

      if event.type == pygame.MOUSEBUTTONDOWN:
         x, y = pygame.mouse.get_pos()
         print("Click :", x, y)

         for nom, (zone, lampe) in icones.items():
            if zone.collidepoint(x, y):
               aptitude_active = nom
               print("Aptitude active:", aptitude_active)

               if aptitude_active == 'MegaBomber':
                  for onelemming in lemmingsLIST:
                     if onelemming['etat'] != EtatDead and onelemming['etat'] != EtatBomb:
                        onelemming['etat']            = EtatBomb
                        onelemming['bomb_start_time'] = time

               elif aptitude_active == 'Bomber':
                  for onelemming in lemmingsLIST:
                     if onelemming['etat'] == EtatStop:
                        onelemming['etat']            = EtatBomb
                        onelemming['bomb_start_time'] = time

         for onelemming in lemmingsLIST:
            rect = pygame.Rect(onelemming['x'], onelemming['y'], LARG, HAUT)
            if rect.collidepoint(x, y):
               if onelemming['etat'] == EtatMarche:
                  if aptitude_active == 'Blocker':
                     onelemming['etat'] = EtatStop
                  elif aptitude_active == 'Creuser':
                     onelemming['etat']           = EtatCreuse
                     onelemming['last_dig_time']  = time
                  elif aptitude_active == 'Floater':
                     onelemming['floater'] = True
                  elif aptitude_active == 'Climber':
                     onelemming['climber'] = True
                  elif aptitude_active == 'Basher':
                     onelemming['etat']          = EtatBash
                     onelemming['last_dig_time'] = time
                  elif aptitude_active == 'Miner':
                     onelemming['etat']          = EtatMine
                     onelemming['last_dig_time'] = time
                  elif aptitude_active == 'Apt6':
                     onelemming['etat']          = EtatBuild
                     onelemming['build_step']    = 0
                     onelemming['last_dig_time'] = time

   # ETAPE 1 : transitions d'états
   for onelemming in lemmingsLIST:
      Transitions[onelemming['etat']](onelemming, time)

   # ETAPE 2 : actions
   for onelemming in lemmingsLIST:
      Actions[onelemming['etat']](onelemming, time)

   # boutons cliquables
   for nom, (zone, lampe) in icones.items():
      couleur = (0, 0, 255) if nom == aptitude_active else (255, 255, 255)
      pygame.draw.rect(screen, couleur, lampe)

   # porte de sortie
   screen.blit(sortie, (SORTIE_X, SORTIE_Y))

   # détection des lemmings entrant dans la porte
   sortie_cx = SORTIE_X + sortie.get_width()  // 2
   sortie_cy = SORTIE_Y + sortie.get_height() // 2
   a_supprimer = []
   for onelemming in lemmingsLIST:
      cx = onelemming['x'] + LARG // 2
      cy = onelemming['y'] + HAUT // 2
      dist2 = (cx - sortie_cx)**2 + (cy - sortie_cy)**2
      if dist2 < LARG**2:
         a_supprimer.append(onelemming)
         survivants += 1
   for l in a_supprimer:
      lemmingsLIST.remove(l)

   # ETAPE 3 : affichage des lemmings
   for onelemming in lemmingsLIST:
      Affichages[onelemming['etat']](onelemming, time)

   # compteurs
   actifs = [l for l in lemmingsLIST if l['etat'] not in (EtatStop, EtatDead)]
   texte_compteur = font_compteur.render("Restants : " + str(len(actifs)), True, (255, 255, 255))
   screen.blit(texte_compteur, (10, 10))
   texte_sauves = font_compteur.render("Sauvés : " + str(survivants), True, (0, 255, 0))
   screen.blit(texte_sauves, (10, 40))

   # fin de partie
   if compteur_creation == 15 and len(actifs) == 0:
      if survivants > 10:
         texte = font_win.render("WIN",  True, (255, 255, 0))
      else:
         texte = font_win.render("LOSE", True, (255, 0, 0))
      screen.blit(texte, (WINDOW_SIZE[0] // 2 - texte.get_width()  // 2,
                          WINDOW_SIZE[1] // 2 - texte.get_height() // 2))

   clock.tick(20)
   pygame.display.flip()

pygame.quit()
