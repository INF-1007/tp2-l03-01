"""
TP2 – Exercice 2 : Priorisation des interventions (Station ORBIT-X)

Objectif :
Les interventions techniques arrivent en continu. Il faut :
- Calculer une priorité pour chaque intervention
- Trier les interventions par priorité décroissante (SANS sorted)
- Estimer le temps total de traitement
- Identifier les interventions urgentes

Structure d'une intervention (dict) :
{
  'id': 1,
  'urgence': 20,     # int (plus grand = plus urgent)
  'duree': 3,        # int (unités abstraites)
  'critique': True   # bool (True = intervention critique)
}

⚠️ Champs manquants :
- Utiliser 0 par défaut pour urgence et duree
- Utiliser False par défaut pour critique
"""

# -------------------------------------------------------------------
# 1) Calcul de priorité
# -------------------------------------------------------------------

def calculer_priorite(intervention):
    """
    score = (urgence × 2) + (duree × 1) + (critique × 10)
    """
    urgence = intervention.get('urgence', 0)
    duree = intervention.get('duree', 0)
    critique = intervention.get('critique', False)

    # critique est un bool -> int(True)=1, int(False)=0
    score = (urgence * 2) + (duree * 1) + (int(critique) * 10)
    return score


# -------------------------------------------------------------------
# 2) Tri des interventions (stable, décroissant, sans sorted/sort)
# -------------------------------------------------------------------

def trier_interventions(liste_interventions):
    """
    Tri par insertion (stable).
    """
    interventions = liste_interventions[:]  # copie

    # Tri par insertion décroissant, stable :
    # on décale tant que l'élément de gauche a une priorité STRICTEMENT plus petite
    for i in range(1, len(interventions)):
        cle = interventions[i]
        score_cle = calculer_priorite(cle)

        j = i - 1
        while j >= 0 and calculer_priorite(interventions[j]) < score_cle:
            interventions[j + 1] = interventions[j]
            j -= 1

        interventions[j + 1] = cle

    return interventions


# -------------------------------------------------------------------
# 3) Estimation du temps
# -------------------------------------------------------------------

def estimer_temps_interventions(liste_triee):
    """
    1 unité de 'duree' = 4 minutes
    """
    temps_stats = {
        'temps_total': 0,
        'temps_moyen': 0.0
    }

    if not liste_triee:
        return temps_stats

    total_minutes = 0
    for itv in liste_triee:
        duree = itv.get('duree', 0)
        total_minutes += duree * 4

    temps_stats['temps_total'] = total_minutes
    temps_stats['temps_moyen'] = total_minutes / len(liste_triee)

    return temps_stats


# -------------------------------------------------------------------
# 4) Interventions urgentes
# -------------------------------------------------------------------

def identifier_interventions_urgentes(liste, seuil=30):
    urgentes = []

    for itv in liste:
        urgence = itv.get('urgence', 0)
        if urgence > seuil:
            # choix cohérent : si id manquant -> on ignore
            if 'id' in itv:
                urgentes.append(itv['id'])

    return urgentes


# -------------------------------------------------------------------
# TESTS main
# -------------------------------------------------------------------

if __name__ == "__main__":
    interventions_test = [
        {'id': 1, 'urgence': 10, 'duree': 3, 'critique': False},
        {'id': 2, 'urgence': 25, 'duree': 2, 'critique': True},
        {'id': 3, 'urgence': 5,  'duree': 5, 'critique': False},
        {'id': 4, 'urgence': 35, 'duree': 1, 'critique': False},
        {'id': 5, 'urgence': 15, 'duree': 4, 'critique': True},
    ]

    print("Priorités :")
    for itv in interventions_test:
        print(itv['id'], calculer_priorite(itv))

    tri = trier_interventions(interventions_test)
    print("\nTri (ids) :", [x.get('id') for x in tri])

    temps = estimer_temps_interventions(tri)
    print("\nTemps :", temps)

    urg = identifier_interventions_urgentes(interventions_test, seuil=30)
    print("\nUrgentes :", urg)