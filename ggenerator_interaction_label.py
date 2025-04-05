from PIL import Image
import numpy as np
import colorsys

def generer_avatar(couleur_preferee, etat_actuel, element_favori, interaction_reelle="virtuel"):
    def generer_couleur(base, saturation=0.6, luminosite=0.8):
        h, l, s = colorsys.rgb_to_hls(*[c / 255.0 for c in base[:3]])
        h = (h + np.random.uniform(-0.02, 0.02)) % 1.0
        new_rgb = colorsys.hls_to_rgb(h, min(l * luminosite, 0.9), min(s * saturation, 0.9))
        return [int(x * 255) for x in new_rgb] + [255]

    def flatten_and_fix_grid(grid):
        flat_pixels = []
        for row in grid:
            for p in row:
                if len(p) == 4:
                    flat_pixels.append(tuple(p))
                elif len(p) == 3:
                    flat_pixels.append(tuple(p) + (255,))
                else:
                    flat_pixels.append((0, 0, 0, 0))
        return flat_pixels

    def dessiner_tete(grid, couleur_peau):
        for y in range(6, 13):
            for x in range(11, 21):
                if ((x - 16) / 4.5) ** 2 + ((y - 9) / 3.2) ** 2 < 1:
                    grid[y][x] = couleur_peau + [255]

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

    def dessiner_expression(grid, etat):
        yeux_position = (9, 13)
        bouche_position = 16
        couleur_yeux = {
            "fatigué": [120, 120, 120],
            "détendu": [100, 160, 120],
            "énergique": [80, 200, 200],
            "endormi": [90, 110, 160]
        }.get(etat, [0, 0, 0])
        for dx in [0, 4]:
            grid[yeux_position[0]][yeux_position[1] + dx] = couleur_yeux + [255]
        grid[bouche_position][14] = [180, 80, 80, 255]

    def dessiner_coiffure(grid, element):
        couleurs_cheveux = {
            "feu": [255, 100, 50],
            "eau": [50, 150, 220],
            "vent": [180, 220, 240],
            "terre": [120, 80, 40],
            "lumière": [240, 210, 60],
            "obscurité": [60, 60, 120]
        }
        base_color = couleurs_cheveux.get(element, [180, 120, 80])
        for y in range(2, 9):
            for x in range(10, 22):
                if ((x - 16) / 6.0) ** 2 + ((y - 5.5) / 3.5) ** 2 < 1:
                    shade = np.random.randint(-20, 20)
                    r = min(max(base_color[0] + shade, 0), 255)
                    g = min(max(base_color[1] + shade, 0), 255)
                    b = min(max(base_color[2] + shade, 0), 255)
                    grid[y][x] = [r, g, b, 255]

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
        for y in range(2, 30, 2):
            for x in range(6, 26, 3):
                if not (10 <= x <= 22 and (4 <= y <= 12 or 22 <= y <= 31)):
                    if np.random.random() > 0.35:
                        grid[y][x] = couleur_effet + [180]

    def dessiner_objet_interaction(grid, interaction_reelle):
        if interaction_reelle == "réalité":
            flower_center = [255, 200, 80, 255]
            flower_petal = [255, 120, 180, 255]
            flower_stem = [100, 200, 100, 255]
            cx, cy = 22, 20
            grid[cy][cx] = flower_center
            grid[cy - 1][cx] = flower_petal
            grid[cy + 1][cx] = flower_petal
            grid[cy][cx - 1] = flower_petal
            grid[cy][cx + 1] = flower_petal
            grid[cy + 2][cx] = flower_stem
            grid[cy + 3][cx] = flower_stem
        else:
            couleur_herbe_1 = [100, 180, 100, 255]
            couleur_herbe_2 = [80, 160, 80, 255]
            couleur_herbe_3 = [60, 140, 60, 255]
            grid[20][21] = couleur_herbe_1
            grid[21][21] = couleur_herbe_2
            grid[21][22] = couleur_herbe_3
            grid[22][21] = couleur_herbe_2

    couleur_map = {
        "rouge": [200, 80, 80],
        "vert": [120, 180, 120],
        "bleu": [100, 150, 200],
        "jaune": [230, 220, 140],
        "violet": [160, 120, 200],
        "noir": [80, 80, 80]
    }

    grid = [[[240, 240, 240, 0] for _ in range(32)] for _ in range(32)]
    couleur_peau = [255, 225, 210]  # 固定肤色
    couleur_vetement = couleur_map.get(couleur_preferee, [180, 180, 180])

    dessiner_tete(grid, couleur_peau)
    dessiner_corps(grid, couleur_vetement)
    dessiner_bras_jambes(grid, couleur_vetement)
    dessiner_expression(grid, etat_actuel)
    dessiner_coiffure(grid, element_favori)
    ajouter_effet_magique(grid, element_favori)
    dessiner_objet_interaction(grid, interaction_reelle)

    img = Image.new("RGBA", (32, 32))
    img.putdata(flatten_and_fix_grid(grid))
    img = img.resize((256, 256), Image.Resampling.NEAREST)
    return img

