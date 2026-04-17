import pygame
from constants import *

def afficheChute(lemming, time):
   """Affiche l'animation de chute (synchronisée sur time global)."""
   screen.blit(tombe[time % len(tombe)], (lemming['x'], lemming['y']))

def afficheMarche(lemming, time):
   """Affiche l'animation de marche, avec décalage individuel pour désynchroniser.
   Sprite miroir si le lemming va à droite."""
   idx = (time + lemming['decal']) % len(marche)
   if lemming['vx'] == -1:
      screen.blit(marche[idx], (lemming['x'], lemming['y']))
   else:
      screen.blit(marche_droite[idx], (lemming['x'], lemming['y']))

def afficheCreuse(lemming, time):
   """Affiche l'animation de creusage."""
   screen.blit(creuse[time % len(creuse)], (lemming['x'], lemming['y']))

def afficheGrimpe(lemming, time):
   """Affiche l'animation d'escalade, orientée vers le mur (selon vx)."""
   spr = grimpe[time % len(grimpe)]
   if lemming['vx'] == -1:
      screen.blit(spr, (lemming['x'], lemming['y']))
   else:
      screen.blit(pygame.transform.flip(spr, True, False), (lemming['x'], lemming['y']))

def afficheFlotte(lemming, time):
   """Affiche l'animation du parapluie."""
   screen.blit(flotte[time % len(flotte)], (lemming['x'], lemming['y']))

def afficheBomb(lemming, time):
   """Pendant le décompte : affiche l'animation blocker + le compte à rebours au-dessus de la tête."""
   screen.blit(blocker[time % len(blocker)], (lemming['x'], lemming['y']))
   decompte = max(1, 5 - (time - lemming['bomb_start_time']) // 10)
   texte = font_bombe.render(str(decompte), True, (255, 50, 50))
   screen.blit(texte, (lemming['x'] + LARG // 2 - texte.get_width() // 2, lemming['y'] - 16))

def afficheBuild(lemming, time):
   """Affiche l'animation du builder, orientée selon vx."""
   spr = builder[time % len(builder)]
   if lemming['vx'] == -1:
      screen.blit(spr, (lemming['x'], lemming['y']))
   else:
      screen.blit(pygame.transform.flip(spr, True, False), (lemming['x'], lemming['y']))

def afficheExplose(lemming, time):
   """Joue l'animation d'explosion (sprite bomber) une seule fois."""
   frame = min(lemming['explode_frame'], len(bomber) - 1)
   screen.blit(bomber[frame], (lemming['x'], lemming['y']))
   lemming['explode_frame'] += 1

def afficheMine(lemming, time):
   """Affiche l'animation de creusage diagonal, orientée selon vx."""
   spr = miner[time % len(miner)]
   if lemming['vx'] == -1:
      screen.blit(spr, (lemming['x'], lemming['y']))
   else:
      screen.blit(pygame.transform.flip(spr, True, False), (lemming['x'], lemming['y']))

def afficheBash(lemming, time):
   """Affiche l'animation de creusage horizontal, orientée selon vx."""
   spr = basher[time % len(basher)]
   if lemming['vx'] == -1:
      screen.blit(spr, (lemming['x'], lemming['y']))
   else:
      screen.blit(pygame.transform.flip(spr, True, False), (lemming['x'], lemming['y']))

def afficheStop(lemming, time):
   """Affiche l'animation du Blocker."""
   screen.blit(blocker[time % len(blocker)], (lemming['x'], lemming['y']))

def afficheDead(lemming, time):
   """Affiche l'animation de mort une seule fois, puis se fige sur la dernière frame."""
   frame = min(lemming['deadframe'], len(dead) - 1)
   screen.blit(dead[frame], (lemming['x'], lemming['y']))
   lemming['deadframe'] += 1
