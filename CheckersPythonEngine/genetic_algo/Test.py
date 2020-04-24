import pickle

from genetic_algo import args


def save_fit():
    with open(r"F:\UnityProjects\ProjectGitHub\checkers-cyber\CheckersPythonEngine\genetic_algo\serialized", 'wb') as f:
        pickle.dump(args.weights, f)


save_fit()
