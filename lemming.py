import random
from constants import *

lemmingsLIST = []

def creerLemming(time):
   """Crée un nouveau lemming avec ses paramètres initiaux et l'ajoute à la liste."""
   new_lemming = {}
   new_lemming['x']               = 250
   new_lemming['y']               = 100
   new_lemming['vx']              = -1
   new_lemming['etat']            = EtatChute
   new_lemming['fallcount']       = 0
   new_lemming['decal']           = random.randint(0, len(marche) - 1)
   new_lemming['deadframe']       = 0
   new_lemming['last_dig_time']   = time
   new_lemming['floater']         = False
   new_lemming['climber']         = False
   new_lemming['bomb_start_time'] = -1
   new_lemming['explode_frame']   = 0
   new_lemming['build_step']      = 0
   lemmingsLIST.append(new_lemming)
