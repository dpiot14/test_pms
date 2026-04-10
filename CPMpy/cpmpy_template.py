import cpmpy as cp
import numpy as np
import json

from pms.box import Box
from pms.box_var import BoxVar, BlockvizEncoder
from cpmpy.solvers.ortools import OrtSolutionPrinter

import sys
from contextlib import contextmanager





# ===============================
# Fonctions utilitaires
# ===============================

@contextmanager
def redirect_ortools_logs(filepath):
    """
    Permet de rediriger les logs d'ortools vers un fichier.
    """
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    f = open(filepath, "w")
    sys.stdout = f
    sys.stderr = f

    try:
        yield
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        f.close()



def save_solution_to_json(scene: dict) -> None:
    """
    Fonction permettant de sauvegarder une solution dans un format JSON compatible avec Blockviz.
    """
    json_line = json.dumps(
        scene,
        cls=BlockvizEncoder
    )
    return json_line


# ===============================
# Classe CPMpyModel
# ===============================



class CPMpyModel:
    def __init__(self):
        self.model = cp.Model()   # Le modèle CPMPy
        self.list_boxes = []
        self.list_boxes_var = []

    def open_data(self, path: str) -> list[Box]:
        """
        Permet d'ouvrir une instance de données, et de créer une liste d'objets Box à partir de ces données.
        """
        with open(path, "r") as f:
            list_boxes = Box.read_csv(f)
        self.list_boxes = list_boxes
        return list_boxes
    
    def create_variables(self, max_dimension : int = 5000) -> list[BoxVar]:
        """
        Permet de créer les variables pour chaque boite, et renvoie une liste d'objets BoxVar.
        """
        list_boxes_var = []
        for box in self.list_boxes:
            position = cp.intvar(0, max_dimension, shape = 3, name = f"{box.name}_position")
            color = np.random.randint(0, 255, size = 3)
            box_var = BoxVar(box, position, color)
            list_boxes_var.append(box_var)
        self.list_boxes_var = list_boxes_var
        return list_boxes_var
    

    def create_objective(self):
        """
        Permet de créer la fonction objectif du problème.
        """
        max_x = cp.max(box_var.position[0] + box_var.box.size[0] for box_var in self.list_boxes_var)
        max_y = cp.max(box_var.position[1] + box_var.box.size[1] for box_var in self.list_boxes_var)
        max_z = cp.max(box_var.position[2] + box_var.box.size[2] for box_var in self.list_boxes_var)
        self.model.minimize(cp.sum([max_x, max_y, max_z]))


    def solve(self, ortools_logs = False, ortools_logs_path = "ortools_logs.txt", **kwargs):
        """
        Permet de résoudre le modèle CPMpy, et d'afficher les solutions trouvées au fur et à mesure de leur découverte, dans un format compatible avec Blockviz.

        Parameters
        -----------------
        ortools_logs : bool
            Si True, les logs d'ortools seront redirigés vers un fichier.
        ortools_logs_path : str
            Le chemin du fichier dans lequel les logs d'ortools seront redirigés.
        kwargs : dict
            Les arguments supplémentaires à passer à la méthode solve d'ortools.
        """
        scene_list = []

        def myprint():
            time = cb.WallTime()
            sol_nbr = cb.solution_count()
            obj_val = cb.ObjectiveValue()
            scene = {"boxes": [],
                    "text": "Solution {}: objective value = {}, time = {}s".format(sol_nbr, obj_val, time)}
            for box_var in self.list_boxes_var:
                scene["boxes"].append({"position" : box_var.position.value().tolist(),
                                        "size" : box_var.box.size,
                                        "color" : box_var.color.tolist()})
            scene_list.append(scene)
            print(save_solution_to_json(scene), file=sys.__stdout__)

        s = cp.SolverLookup.get('ortools', self.model)
        cb = OrtSolutionPrinter(s, display = myprint)

        if ortools_logs:
            with redirect_ortools_logs(ortools_logs_path):
                s.solve(enumerate_all_solutions=False, solution_callback=cb, log_search_progress=True, log_to_stdout = False, **kwargs)
        else:
            s.solve(enumerate_all_solutions=False, solution_callback=cb, log_search_progress=False, **kwargs)
    


# ===============================
# Code principal
# ===============================



# Lien vers le jeu de données
data_path = ...

def main():
    # Initialisation du modèle CPMpy, ouverture des données et création des variables
    mymodel = CPMpyModel()
    mymodel.open_data(path = data_path)
    list_boxes_var = mymodel.create_variables()

    # Vous pouvez ajouter ici des contraintes à votre modèle, en accédant directement au modèle CPMpy via mymodel.model, et en utilisant les variables de list_boxes_var.



    
    # Création de la fonction objectif et résolution du modèle
    mymodel.create_objective()
    mymodel.solve(time_limit = 60)   # Vous pouvez utiliser des arguments supplémentaires pour paramétrer le solveur ORTools ou enregistrer les logs du solveur ORTools.



if __name__ == "__main__":
    main()