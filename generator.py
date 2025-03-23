from PIL import Image
import numpy as np
import colorsys

def generer_couleur(base, saturation=0.6, luminosite=0.8):
    h, l, s = colorsys.rgb_to_hls(*[c / 255.0 for c in base[:3]])
    h = (h + np.random.uniform(-0.02, 0.02)) % 1.0
    new_rgb = colorsys.hls_to_rgb(h, min(l * luminosite, 0.9), min(s * saturation, 0.9))
    return [int(x * 255) for x in new_rgb] + [255]

def dessiner_tete(grid, couleur_peau):
    for y in range(6, 13):
        for x in range(11, 21):
            if ((x - 16) / 4.5) ** 2 + ((y - 9) / 3.2) ** 2 < 1:
                grid[y][x] = generer_couleur(couleur_peau)

def dessiner_corps(grid, couleur_vetement):
    for y in range(13, 22):
        largeur = 10 - int(0.3 * (y - 13))
        for dx in range(largeur):
            x = 16 - largeur // 2 + dx
            if 0 <= x < 32:
                shade = 10 * abs(dx % 3 - 1)
                grid[y][x] = generer_couleur([max(c - shade, 0) for c in couleur_vetement], 0.5 + 0.1 * (dx % 2), 0.7 + 0.05 * (y % 3))

def dessiner_bras_jambes(grid, couleur_vetement):
    for y in range(14, 22):
        for dx in [-6, 6]:
            x = 16 + dx
            grid[y][x] = generer_couleur(couleur_vetement, 0.6, 0.7)

    for y in range(22, 30):
        for dx in [-2, 2]:
            x = 16 + dx
            grid[y][x] = generer_couleur(couleur_vetement, 0.5, 0.6)

def dessiner_expression(grid, emotion):
    yeux_position = (9, 13)
    bouche_position = 16

    couleur_yeux = {
        "joyeux": [50, 180, 250],
        "triste": [80, 160, 220],
        "colère": [200, 60, 80],
        "ennuyé": [150, 150, 150],
        "calme": [100, 200, 100]
    }.get(emotion, [0, 0, 0])

    for dx in [0, 4]:
        grid[yeux_position[0]][yeux_position[1] + dx] = couleur_yeux

    bouche_couleur = [200, 50, 50]
    if emotion == "joyeux":
        grid[bouche_position][14] = bouche_couleur
        grid[bouche_position][15] = bouche_couleur
    elif emotion == "triste":
        grid[bouche_position + 1][14] = bouche_couleur
        grid[bouche_position + 1][15] = bouche_couleur
    elif emotion == "colère":
        grid[bouche_position][14] = bouche_couleur
    elif emotion == "ennuyé":
        grid[bouche_position][14] = [150, 150, 150]
    elif emotion == "calme":
        grid[bouche_position][14] = [100, 200, 100]

def dessiner_coiffure(grid, element):
    couleurs_cheveux = {
        "feu": [255, 100, 50],
        "eau": [50, 150, 220],
        "vent": [200, 220, 240],
        "terre": [120, 80, 40],
        "lumière": [255, 240, 180],
        "obscurité": [60, 60, 120]
    }

    couleur_cheveux = generer_couleur(couleurs_cheveux.get(element, [180, 120, 80]), 0.7)
    for y in range(3, 8):
        for x in range(12, 20):
            if ((x - 16) / 5) ** 2 + ((y - 5) / 3) ** 2 < 1:
                grid[y][x] = couleur_cheveux

def ajouter_effet_magique(grid, element):
    couleurs_effets = {
        "feu": [255, 80, 40],
        "eau": [40, 120, 220],
        "vent": [200, 230, 240],
        "terre": [120, 80, 40],
        "lumière": [255, 240, 180],
        "obscurité": [40, 40, 80]
    }

    couleur_effet = couleurs_effets.get(element, [255, 255, 255])

    for y in range(3, 28, 3):
        for x in range(6, 26, 5):
            if np.random.random() > 0.6:
                grid[y][x] = couleur_effet + [180]

def generer_avatar(couleur_preferee, emotion_actuelle, element_favori):
    couleur_map = {
        "rose": [255, 180, 180],
        "bleu clair": [170, 210, 230],
        "vert menthe": [180, 230, 200],
        "lavande": [200, 180, 230],
        "saumon": [255, 200, 180]
    }

    grid = [[[240, 240, 240, 0] for _ in range(32)] for _ in range(32)]
    couleur_peau = generer_couleur([255, 240, 220], 0.45)
    couleur_vetement = couleur_map.get(couleur_preferee, [180, 180, 180])

    dessiner_tete(grid, couleur_peau)
    dessiner_corps(grid, couleur_vetement)
    dessiner_bras_jambes(grid, couleur_vetement)
    dessiner_expression(grid, emotion_actuelle)
    dessiner_coiffure(grid, element_favori)
    ajouter_effet_magique(grid, element_favori)

    img = Image.new("RGBA", (32, 32))
    img.putdata([tuple(p) for row in grid for p in row])
    img = img.resize((256, 256), Image.Resampling.NEAREST)
    img.save("static/mon_avatar.png")
