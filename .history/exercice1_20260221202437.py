# -------------------------------------------------------------------
# 1) Analyse des modules
# -------------------------------------------------------------------

def analyser_modules(modules):
    """
    Analyse les modules de la station.

    Args:
        modules (dict): {nom_module: (cout, temps, criticite)}

    Returns:
        dict contenant :
            - 'module_plus_critique' : str ou None
            - 'cout_moyen' : float
            - 'temps_moyen' : float
    """

    stats = {
        'module_plus_critique': None,
        'cout_moyen': 0.0,
        'temps_moyen': 0.0
    }

    # TODO 1 : Gérer le cas où le dictionnaire est vide
    if not modules:
        return stats

    somme_couts = 0.0
    somme_temps = 0.0

    meilleur_ratio = None
    meilleur_module = None

    # TODO 2 + TODO 3 : Parcourir et calculer
    for nom_module, (cout, temps, criticite) in modules.items():
        somme_couts += cout
        somme_temps += temps

        # Ignorer temps == 0 pour le ratio
        if temps != 0:
            ratio = criticite / temps
            if (meilleur_ratio is None) or (ratio > meilleur_ratio):
                meilleur_ratio = ratio
                meilleur_module = nom_module
            # égalité -> on ne change rien (on garde le premier rencontré)

    nb_modules = len(modules)
    stats['cout_moyen'] = somme_couts / nb_modules
    stats['temps_moyen'] = somme_temps / nb_modules
    stats['module_plus_critique'] = meilleur_module

    return stats


# -------------------------------------------------------------------
# 2) Regroupement des modules par type
# -------------------------------------------------------------------

def regrouper_modules_par_type(modules, types):
    """
    Regroupe les modules par type.

    Args:
        modules (dict): dictionnaire des modules
        types (dict): {nom_module: type}

    Returns:
        dict: {type: [liste des modules]}
    """

    modules_par_type = {}

    for nom_module in modules:  # parcourt les clés du dict
        t = types.get(nom_module)   # None si absent
        if t is None:
            continue  # Ignorer silencieusement les modules sans type

        # Crée la liste si absente puis ajoute
        modules_par_type.setdefault(t, []).append(nom_module)

    return modules_par_type


# -------------------------------------------------------------------
# 3) Calcul du cout total
# -------------------------------------------------------------------

def calculer_cout_total(modules, interventions):
    """
    Calcule le coût total de maintenance prévu.

    Args:
        modules (dict): {nom_module: (cout, temps, criticite)}
        interventions (dict): {nom_module: nombre_interventions}

    Returns:
        float: coût total
    """

    cout_total = 0.0

    for nom_module, nb in interventions.items():
        if nom_module not in modules:
            continue  # Ignorer les modules absents de modules

        cout_module = modules[nom_module][0]  # (cout, temps, criticite) -> cout
        cout_total += cout_module * nb

    return cout_total


# -------------------------------------------------------------------
# TESTS main
# -------------------------------------------------------------------

if __name__ == "__main__":
    modules_test = {
        'Laboratoire': (120, 15, 8),
        'Habitat': (200, 10, 9),
        'Observatoire': (150, 20, 6)
    }

    types_test = {
        'Laboratoire': 'science',
        'Habitat': 'vie',
        'Observatoire': 'science'
    }

    interventions_test = {
        'Laboratoire': 2,
        'Habitat': 1
    }

    print(analyser_modules(modules_test))
    print(regrouper_modules_par_type(modules_test, types_test))
    print(calculer_cout_total(modules_test, interventions_test))