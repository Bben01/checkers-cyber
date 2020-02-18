import pickle

filename = r"F:\UnityProjects\ProjectGitHub\checkers-cyber\CheckersPythonEngine\genetic_algo\serialized"

ENNEMY_COLOR = False
WIN = float("inf")
LOSS = float("-inf")

with open(filename, "rb") as f:
    WEIGHTS = pickle.load(f)
