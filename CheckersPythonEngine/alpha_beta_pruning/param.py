import pickle

filename = r"F:\UnityProjects\ProjectGitHub\checkers-cyber\CheckersPythonEngine\genetic_algo\serialized"

ENNEMY_COLOR = True
WIN = float("inf")
LOSS = float("-inf")

# with open(filename, "rb") as f:
#     WEIGHTS = pickle.load(f)

WEIGHTS = (
    [(5, 0), (20, 0), (3, 0), (1, 0), (3, 0), (4, 0), (-2, 0), (-3, 0)],
    [(-5, 0), (-20, 0), (-3, 0), (-2, 0), (-3, 0), (-4, 0), (2, 0), (3, 0)]
)
