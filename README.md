# Lemmings — Python / Pygame

Recréation simplifiée du jeu classique **Lemmings** en Python, réalisée dans le cadre du cours d'IA à l'ESIEE Paris (3e année).

## Principe du jeu

15 lemmings apparaissent un par un et se déplacent automatiquement sur la carte. Le joueur doit en **sauver plus de 10** en leur assignant des aptitudes avant qu'ils ne meurent ou tombent hors de la fenêtre. Les lemmings sauvés atteignent la porte de sortie.

- **WIN** si plus de 10 lemmings atteignent la sortie
- **LOSE** sinon

## Lancement

### Prérequis

```
pip install pygame numpy
```

### Démarrage

```
python LEMMINGS.py
```

## Aptitudes disponibles

Cliquez sur une icône en bas de l'écran pour activer une aptitude, puis cliquez sur un lemming pour la lui appliquer.

| Icône | Aptitude | Effet |
|---|---|---|
| Blocker | Bloqueur | Le lemming s'arrête et fait demi-tour aux autres |
| Creuser | Creuseur | Creuse verticalement vers le bas |
| Climber | Grimpeur | Grimpe le long des murs au lieu de faire demi-tour |
| Floater | Parapluie | Descend lentement, ne meurt pas d'une grande chute |
| Bomber | Bombe | Le lemming sélectionné explose après 5 secondes |
| Apt6 | Builder | Construit un escalier de briques (20 marches) |
| Basher | Basheur | Creuse horizontalement dans la direction du lemming |
| Miner | Mineur | Creuse en diagonale vers le bas |
| MegaBomber | Méga-bombe | Tous les lemmings actifs explosent simultanément |

## États des lemmings

Chaque lemming est une machine à états finis avec 12 états :

```
EtatChute → EtatMarche ↔ EtatGrimpe
                ↓ (aptitudes)
EtatCreuse / EtatBash / EtatMine / EtatBuild / EtatStop / EtatBomb
                ↓
            EtatExplose → EtatDead
```

| État | Description |
|---|---|
| EtatMarche | Déplacement horizontal |
| EtatChute | Chute libre (3 px/frame) |
| EtatGrimpe | Escalade d'un mur |
| EtatFlotte | Chute lente au parapluie (1 px/frame) |
| EtatCreuse | Creusage vertical |
| EtatBash | Creusage horizontal |
| EtatMine | Creusage diagonal |
| EtatBuild | Construction d'un escalier |
| EtatStop | Bloqueur immobile |
| EtatBomb | Décompte avant explosion |
| EtatExplose | Animation d'explosion |
| EtatDead | Mort (état terminal) |

## Architecture du code

```
LEMMINGS.py      — boucle principale (événements, transitions, actions, affichage)
constants.py     — constantes, chargement des assets pygame, définition des états et icônes
lemming.py       — structure d'un lemming et fonction de création
transitions.py   — logique de changement d'état pour chaque état
actions.py       — effets physiques de chaque état (déplacement, modification du terrain)
affichage.py     — rendu des sprites pour chaque état
data/
  map.png        — carte du niveau
  planche.png    — feuille de sprites (11 lignes d'animation)
  sortie.png     — sprite de la porte de sortie
```

Le terrain est un objet `pygame.Surface` modifié en temps réel : creuser ou exploser efface des pixels à la couleur noire `(0, 0, 0)`, et les collisions sont détectées en lisant la couleur des pixels de `fond`.

## Paramètres configurables (constants.py)

| Constante | Valeur par défaut | Rôle |
|---|---|---|
| `FALL_LIMIT` | 100 px | Hauteur de chute mortelle |
| `BOMB_RADIUS` | 30 px | Rayon d'explosion |
| `BUILD_STEPS` | 20 | Nombre de marches posées par un Builder |
| `BUILD_W / BUILD_H` | 8 / 2 px | Dimensions d'une marche |
| `BRICK_COLOR` | (80, 200, 80) | Couleur des briques construites |
# lemmings
