from game_engine import ValidMoveMethods, Server

game_instance = Server.running_threads["127.0.0.1"]
x = 4
y = 6
ValidMoveMethods.calculate_eat_positions(game_instance.plateau.pieces, x, y, False, True, False)
