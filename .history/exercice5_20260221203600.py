"""
TP2 – Exercice 5 : Analyse de journaux d’incidents (Centre ORBIT-X)

Contexte :
Les ingénieurs reçoivent des rapports texte (logs) décrivant l’état des systèmes.
On veut analyser ces textes pour :
- calculer un score global (0 à 10)
- classer les rapports en catégories
- détecter les problèmes récurrents
- générer un rapport global + une tendance

Mots-clés :
On fournit un dictionnaire {mot_cle: score} avec des scores positifs ou négatifs.
Exemple :
mots_cles = {
    'stable': 2,
    'optimal': 3,
    'erreur': -2,
    'defaillant': -3
}

Règles générales :
- L’analyse est INSENSIBLE à la casse (majuscules/minuscules)
- On cherche des mots présents dans le texte (occurrences par mots)
- Un mot-clé peut apparaître plusieurs fois : chaque occurrence compte
- Le score final est borné entre 0 et 10
"""

# -------------------------------------------------------------
# 1) Analyser un rapport
# -------------------------------------------------------------


def analyser_rapport(texte, mots_cles):
    """
    Calcule le score d’un rapport et extrait les mots-clés détectés.

    Étapes attendues :
    1) Mettre le texte en minuscules
    2) Compter les occurrences de chaque mot-clé
       (approche simple autorisée : split() + comparaison de mots)
    3) score = 5 + somme(occurrences * score_mot)
    4) borner score entre 0 et 10
    5) retourner (score, liste_mots_trouves_sans_doublons)

    Args:
        texte (str)
        mots_cles (dict): {mot: score_int}

    Returns:
        tuple: (score_int, mots_trouves_list)
    """
    score = 5
    mots_trouves = []

    # TODO 1 : normaliser texte (minuscules)
    texte = texte.lower()

    # TODO 2 : découper en mots. Attention aussi à enlever la ponctuation basique aux extrémités (utiliser la fonction strip())S.
    mots = texte.split()
    new_mots = []
    for ponctuation in mots:
        phrase = ponctuation.strip(".,;:!?()[]\"'")
        if phrase != "":
            new_mots.append(phrase)
    # TODO 3 : pour chaque mot-clé :
    for mot_cle, valeur in mots_cles.items():
        occurence = 0
        for mot in new_mots:
            if mot == mot_cle:
                occurence += 1

        if occurence > 0:
            score += occurence * valeur
            if mot_cle not in mots_trouves:
                mots_trouves.append(mot_cle)

    #    - mettre à jour le score
    #    - si occurrences > 0 : ajouter le mot à mots_trouves (sans doublons)
    # TODO 4 : borner score entre 0 et 10 (min/max)
    if score < 0:
        score = 0
    if score > 10:
        score = 10
    # TODO 5 : retourner (score, mots_trouves)
    return score, mots_trouves


# -------------------------------------------------------------
# 2) Catégoriser une liste de rapports
# -------------------------------------------------------------


def categoriser_rapports(rapports, mots_cles):
    """
    Classe les rapports en 3 catégories selon leur score :

    - 'positifs' : score >= 7
    - 'neutres'  : 4 <= score <= 6
    - 'negatifs' : score <= 3

    Args:
        rapports (list): liste de chaînes
        mots_cles (dict)

    Returns:
        dict: {
            'positifs': [(texte, score), ...],
            'neutres':  [(texte, score), ...],
            'negatifs': [(texte, score), ...]
        }
    """
    categories = {"positifs": [], "neutres": [], "negatifs": []}

    # TODO :
    # Pour chaque texte :
    #   - faire une analyse du rapport pour en tirer le score
    #   - mettre à jour "categories"
    for texte in rapports:
        score, _ = analyser_rapport(texte, mots_cles)

        if score >= 7:
            categories["positifs"].append((texte, score))
        if score <= 3:
            categories["negatifs"].append((texte, score))
        elif score <= 6 and score >= 4:
            categories["neutres"].append((texte, score))
    return categories


# -------------------------------------------------------------
# 3) Identifier les problèmes récurrents dans les rapports négatifs
# -------------------------------------------------------------


def identifier_problemes(rapports_negatifs, mots_cles_negatifs):
    """
    À partir des rapports négatifs, compter combien de fois chaque mot-clé négatif apparaît.

    Args:
        rapports_negatifs (list): liste de tuples (texte, score) OU liste de textes
        mots_cles_negatifs (dict): {mot_negatif: score_negatif}

    Returns:
        dict: {mot_negatif: nombre_occurrences_total}
    """
    problemes = {}

    # TODO 1 : initialiser problemes avec 0 pour chaque mot négatif
    for mot in mots_cles_negatifs:
        problemes[mot] = 0
    # TODO 2 : parcourir les rapports négatifs :

    #   - si l’élément est un tuple, récupérer texte = element[0]
    #   - analyser le texte (minuscules + split)
    #   - compter les occurrences de chaque mot_negatif
    #   - incrémenter problemes[mot]
    for element in rapports_negatifs:
        if isinstance(element, tuple):
            texte = element[0]
        else:
            texte = element
        texte = texte.lower()
        mots = texte.split()

        suite_mots = []
        for terme in mots:
            phrase = terme.strip(".,;:!?()[]'")
            if phrase != "":
                suite_mots.append(phrase)

        for mot_negatif in mots_cles_negatifs:
            for mot in suite_mots:
                if mot == mot_negatif:
                    problemes[mot_negatif] += 1
    return problemes


# -------------------------------------------------------------
# 4) Générer un rapport global
# -------------------------------------------------------------


def generer_rapport_global(categories, problemes):
    """
    Génère un résumé global.

    Contenu attendu :
    - nb_positifs, nb_neutres, nb_negatifs
    - score_moyen (moyenne de tous les scores)
    - top_problemes : liste des 3 mots négatifs les plus fréquents (du plus fréquent au moins fréquent)

    Args:
        categories (dict) : résultat de categoriser_rapports
        problemes (dict)  : résultat de identifier_problemes

    Returns:
        dict
    """
    rapport = {
        "nb_positifs": 0,
        "nb_neutres": 0,
        "nb_negatifs": 0,
        "score_moyen": 0.0,
        "top_problemes": [],
    }

    # TODO 1 : récupérer tous les scores et calculer la moyenne (gérer le cas avec 0 rapports)
    rapport["nb_positifs"] = len(categories.get("positifs", []))
    rapport["nb_neutres"] = len(categories.get("neutres", []))
    rapport["nb_negatifs"] = len(categories.get("negatifs", []))

    scores = []
    for categorie in ['positifs', 'neutres', 'negatifs']:
        for texte, score in categories.get(categorie):
            scores.append(score)

    if len(scores) == 0:
        rapport['score_moyen'] = 0.0
    else:
        rapport['score_moyen'] = sum(scores) / len(scores)

    # TODO 2 : trouver les 3 problèmes les plus fréquents sans utiliser sorted(), un tri simple type “sélection des max” est suffisant.)
    problemes_frequent_3 = []
    copie = problemes.copy()

    for _ in range(3):
        max_mot = None
        max_val = None

        for mot, val in copie.items():
            if max_mot is None or val > max_val:
                max_mot = mot
                max_val = val

        # si dictionnaire vide ou tout à 0, on peut arrêter
        if max_mot is None or max_val <= 0:
            break

        problemes_frequent_3.append(max_mot)
        del copie[max_mot]  # enlever pour trouver le prochain

    rapport['top_problemes'] = problemes_frequent_3
    return rapport


# -------------------------------------------------------------
# 5) Calculer une tendance à partir d’un historique
# -------------------------------------------------------------

def calculer_tendance(historique_scores):
    """
    Calcule une tendance à partir d’une liste de scores (dans le temps).

    Règle simple :
    - Si moyenne de la 2e moitié > moyenne de la 1re moitié : 'amelioration'
    - Si moyenne de la 2e moitié < moyenne de la 1re moitié : 'degradation'
    - Sinon : 'stable'

    Cas particuliers :
    - si historique vide : 'stable'
    - si un seul élément : 'stable'

    Args:
        historique_scores (list): ex [4,5,6,7,8]

    Returns:
        str: 'amelioration' | 'degradation' | 'stable'
    """

    # TODO :
    # - Gérer les cas vides / 1 élément
    # - Couper en deux moitiés
    # - Comparer les moyennes
    if len(historique_scores) <= 1:
        return 'stable'

    milieu = len(historique_scores) // 2
    premiere = historique_scores[:milieu]
    seconde = historique_scores[milieu:]

    moy1 = sum(premiere) / len(premiere)
    moy2 = sum(seconde) / len(seconde)

    if moy2 > moy1:
        return 'amelioration'
    elif moy2 < moy1:
        return 'degradation'
    else:
        return "stable"


# -------------------------------------------------------------
# TESTS main
# -------------------------------------------------------------

if __name__ == "__main__":
    mots_cles = {
        "stable": 2,
        "optimal": 3,
        "nominal": 1,
        "ok": 1,
        "erreur": -2,
        "panne": -3,
        "defaillant": -3,
        "retard": -1,
        "surchauffe": -2,
        "fuite": -3,
    }

    mots_cles_negatifs = {
        "erreur": -2,
        "panne": -3,
        "defaillant": -3,
        "retard": -1,
        "surchauffe": -2,
        "fuite": -3,
    }

    # Grande liste de rapports (volontairement variée)
    rapports = [
        "Système stable et nominal. Tout est OK.",
        "Température stable, fonctionnement optimal, état OK.",
        "Erreur de communication détectée. Retard sur la séquence.",
        "Panne capteur pression. Système defaillant.",
        "Surchauffe moteur. Erreur erreur. Risque panne.",
        "Nominal, mais léger retard sur l'alignement.",
        "Fuite détectée dans le circuit secondaire. Panne possible.",
        "OK. Stable.",
        "Defaillant: panne panne panne sur module X.",
        "Rapport: fonctionnement optimal et stable, nominal.",
        "Surchauffe et fuite. Erreur critique.",
        "Tout nominal, tout ok.",
        "Retard retard retard. Erreur de synchronisation.",
        "Panne électrique. Système defaillant. Surchauffe.",
        "Stable, mais une erreur isolée.",
    ]

    print("=== Test analyse_rapport (exemples) ===")
    for i in [0, 2, 4, 8, 10]:
        s, mots = analyser_rapport(rapports[i], mots_cles)
        print(f"Rapport {i} -> score={s}, mots={mots}")

    print("\n=== Catégorisation ===")
    categories = categoriser_rapports(rapports, mots_cles)
    print("Nb positifs :", len(categories["positifs"]))
    print("Nb neutres  :", len(categories["neutres"]))
    print("Nb negatifs :", len(categories["negatifs"]))

    print("\n=== Problèmes récurrents (sur négatifs) ===")
    problemes = identifier_problemes(categories["negatifs"], mots_cles_negatifs)
    print(problemes)

    print("\n=== Rapport global ===")
    global_ = generer_rapport_global(categories, problemes)
    print(global_)

    print("\n=== Tendance (historique) ===")
    historique = [3, 4, 4, 5, 6, 6, 7, 7, 8, 8]
    print("Historique :", historique)
    print("Tendance :", calculer_tendance(historique))
