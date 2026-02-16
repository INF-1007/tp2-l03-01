"""
TP2 – Exercice 3 : Gestion des ressources vitales (Station ORBIT-X)

Objectif :
Gérer un inventaire de ressources (oxygène, eau, énergie, etc.) pour éviter
les ruptures et planifier un réapprovisionnement.

Structure des données
---------------------
1) Ressources (inventaire) :
    ressources = { 'oxygene': 120, 'eau': 300, 'energie': 500 }

2) Besoin / consommation (pour 1 cycle) :
    besoin = { 'oxygene': 5, 'eau': 12 }

3) Consommations par activité (menu_activites) :
    consommations = {
        'EVA': {'oxygene': 8, 'energie': 15},
        'Hydroponie': {'eau': 20, 'energie': 10}
    }

⚠️ Rappels / Contraintes importantes :
- Si une ressource est absente de l'inventaire des ressources, sa quantité est considérée comme 0.
- Vous devez éviter les KeyError en utilisant dict.get().
- Ne modifiez pas directement les dictionnaires si la fonction demande une copie.
"""
ressources = { 'oxygene': 120, 'eau': 300, 'energie': 500 }

besoin = { 'oxygene': 5, 'eau': 12 }

consommations ={
        'EVA': {'oxygene': 8, 'energie': 15},
        'Hydroponie': {'eau': 20, 'energie': 10}
}   
# Coûts unitaires (utilisés pour optimiser le réapprovisionnement)
COUTS_UNITAIRES = {
    'oxygene': 2.5,
    'eau': 0.5,
    'energie': 1.2,
    'nourriture': 3.0
}

# -------------------------------------------------------------------
# 1) Vérifier la disponibilité des ressources
# -------------------------------------------------------------------

def verifier_ressources(ressources, besoin):
    """
    Vérifie si les ressources disponibles suffisent pour couvrir un besoin.

    Args:
        ressources (dict): stock actuel {ressource: quantité}
        besoin (dict): ressources nécessaires {ressource: quantité}

    Returns:
        tuple: (peut_faire: bool, manquantes: list)
            - peut_faire = True si toutes les ressources sont suffisantes
            - manquantes = liste des ressources insuffisantes (noms)
    """
    peut_faire = True
    manquantes = []

    # TODO :
    # Pour chaque ressource requise dans besoin :
    #   - si stock actuel < quantite requise :
    #         peut_faire = False
    #         mettre à jour la liste "manquantes"
    for ressource, qte_requise in besoin.items():
        stock = ressources.get(ressource, 0)
        if stock < qte_requise:
            peut_faire = False
            manquantes.append(ressource)
    return peut_faire, manquantes


# -------------------------------------------------------------------
# 2) Mettre à jour les ressources après consommation
# -------------------------------------------------------------------

def mettre_a_jour_ressources(ressources, besoin, cycles=1):
    """
    Met à jour les ressources après avoir exécuté un certain nombre de cycles.

    Exemple :
- si besoin = {'oxygene': 5} et cycles=3, on consomme 15 d'oxygène.

    Args:
        ressources (dict): stock actuel
        besoin (dict): consommation par cycle
        cycles (int): nombre de cycles

    Returns:
        dict: nouveau dictionnaire de ressources (copie)
    """
    nouvelles = ressources.copy()

    # TODO :
    # Pour chaque ressource nécessaire :
    #   - calculer la consommation
    #   - mettre à jour le dictionnaire "nouvelles"
    # (On suppose que les données fournies sont cohérentes; pas besoin de borner à 0)
    for ressource, conso_par_cycle in besoin.items():
        conso_totale = conso_par_cycle * cycles
        stock_actuel = nouvelles.get(ressource, 0)  
        nouvelles[ressource] = stock_actuel - conso_totale
    return nouvelles


# -------------------------------------------------------------------
# 3) Générer des alertes sous un seuil
# -------------------------------------------------------------------

def generer_alertes_ressources(ressources, seuil=50):
    """
    Identifie les ressources dont le stock est inférieur au seuil.

    Pour chaque ressource en alerte, on suggère une quantité standard à commander
    pour revenir à un niveau cible.

    Règle de suggestion :
    - Niveau cible = 200 unités


    Args:
        ressources (dict)
        seuil (int)

    Returns:
        dict: {ressource: (stock_actuel, a_commander)}
    """
    alertes = {}
    niveau_cible = 200

    # TODO :
    # Pour chaque ressource du stock :
    #   - si stock < seuil :
    #         calculer a_commander
    #         mettre à jour alertes
    for ressource, stock in ressources.items():
        if stock < seuil:
            a_commander = niveau_cible - stock
            alertes[ressource] = (stock, a_commander)
    return alertes


# -------------------------------------------------------------------
# 4) Calculer combien de cycles sont possibles par activité
# -------------------------------------------------------------------

def calculer_cycles_possibles(ressources, consommations):
    """
    Calcule, pour chaque activité, combien de cycles peuvent être réalisés
    avec les ressources actuelles.

    ⚠️ Si une activité nécessite une ressource avec conso 0, vous pouvez l'ignorer
       pour éviter une division par zéro (comme dans l'exercice 1).

    Args:
        ressources (dict)
        consommations (dict): {activite: {ressource: conso_par_cycle}}

    Returns:
        dict: {activite: nb_cycles_possibles}
    """
    possibles = {}

    # TODO :
    # Pour chaque activité :
    #   - pour chaque ressource requise :
    #       si conso > 0 :
    #           calculer nb_cycles en fonction du stock et de la conso
    #   - une ressource est considérée valide si conso > 0
    #   - si aucune ressource valide (toutes conso==0), décider nb_cycles=0 
    #   - mettre à jour "possibles"
    for activite, conso_actuelle in consommations.items():
        nb_cycles = None
        conso_val = False

        for ressource, conso_cycle in conso_actuelle.items():
            if conso_cycle > 0:
                conso_val = True
                stock = ressources.get(ressource, 0)
                cycles = stock // conso_cycle 
                if nb_cycles is None or cycles < nb_cycles:
                    nb_cycles = cycles
        if not conso_val:
            possibles[activite] = 0
        else:
            possibles[activite] = nb_cycles           

    return possibles


# -------------------------------------------------------------------
# 5) Optimiser le réapprovisionnement sous contrainte de budget
# -------------------------------------------------------------------

def optimiser_reapprovisionnement(ressources, besoins_prevus, budget):
    """
    Objectif :
Déterminer une liste d'achats {ressource: quantite_a_acheter}
pour couvrir des besoins prévus, sans dépasser le budget.

Paramètres :
- ressources : stock actuel
- besoins_prevus : besoins totaux à couvrir (déjà agrégés)
    ex: {'oxygene': 300, 'eau': 500}
- budget : budget disponible (float)

Étapes attendues (guidage) :
1) Calculer le manque pour chaque ressource 
2) Acheter en respectant le budget, selon les coûts unitaires.
   Stratégie simple attendue :
   - acheter dans l'ordre des manques décroissants
   - acheter autant que possible sans dépasser le budget

⚠️ On attend une solution SIMPLE, pas une optimisation mathématique parfaite.

Returns:
    dict: {ressource: quantite_a_acheter}
    """
    achats = {}

    # TODO 1 : Calculer les manques dans un dict manques = {}
    manques = {}
    for ressource, besoin_total in besoins_prevus.items():
        stock = ressources.get(ressource, 0)
        manque = besoin_total - stock
        if manque > 0:
            manques[ressource] = manque
    priorites = list(manques.items())
    # TODO 2 : Trier les manques par ordre décroissant (utiliser la fonction sorted())
    def cle_tri(element):
        return element[1]

    priorites = sorted(manques.items(), key=cle_tri, reverse=True)
    # TODO 3 : Parcourir les ressources par priorité :
    #          - calculer la quantite max achetable
    #          - acheter la quantite requise et soustraire du budget
    for ressource, manque in priorites:

        cout_unitaire = COUTS_UNITAIRES.get(ressource, None)
        if cout_unitaire is None or cout_unitaire <= 0:
            continue
        qte_max = int(budget // cout_unitaire)
        if qte_max <= 0:
            break

        qte_achetee = min(manque, qte_max)

        achats[ressource] = qte_achetee
        budget -= qte_achetee * cout_unitaire

    return achats


if __name__ == "__main__":
    ressources_test = {'oxygene': 120, 'eau': 300, 'energie': 500}
    besoin_cycle = {'oxygene': 5, 'eau': 12}

    print("Vérif :", verifier_ressources(ressources_test, besoin_cycle))
    print("Après 3 cycles :", mettre_a_jour_ressources(ressources_test, besoin_cycle, cycles=3))
    print("Alertes :", generer_alertes_ressources({'oxygene': 40, 'eau': 120}, seuil=50))

    consommations_test = {
        'EVA': {'oxygene': 8, 'energie': 15},
        'Hydroponie': {'eau': 20, 'energie': 10}
    }
    print("Cycles possibles :", calculer_cycles_possibles(ressources_test, consommations_test))

    besoins_prevus = {'oxygene': 300, 'eau': 500, 'energie': 650}
    print("Achats :", optimiser_reapprovisionnement(ressources_test, besoins_prevus, budget=200))
    