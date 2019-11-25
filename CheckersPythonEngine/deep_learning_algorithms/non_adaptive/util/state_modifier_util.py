def mirror_state(input_state):
    """
    Mirror the state by changing the colors of the current state
    :param input_state: State
    :return: mirrored state
    """
    from copy import deepcopy
    # iterate through pawn
    state = deepcopy(input_state)
    for x, row in enumerate(input_state.plateau.board):
        for y, piece in enumerate(row):
            if piece is not None:
                state.plateau.board[x][y].isWhite = not piece.isWhite

    state.isWhiteTurn = not state.isWhiteTurn
    state.plateau.numWhite, state.plateau.numBlack = state.plateau.numBlack, state.plateau.numWhite


def get_key_mirror_action(input_key_action: str):
    """
    Mirror the key name of action. It will mirror the coordinates.
    Also mirror the direction of move if the action is move or attack.
    :param input_key_action:
    :return:
    """

    # case of attack action
    # format attack input : mp*<y coor>,<x coor>*<y direction>,<x direction>
    # case of move action
    # format move input : mp*<y coor>,<x coor>*<y direction>,<x direction>
    if input_key_action[0:2] == 'mp':
        input_key_action_split = input_key_action.split('*')
        coor_string = input_key_action_split[1]
        y_coor = coor_string.split(",")[0]
        x_coor = coor_string.split(",")[1]
        (x_coor, y_coor) = mirror_coordinates(int(x_coor), int(y_coor))
        coor_dir_string = input_key_action_split[2]
        y_coor_dir = coor_dir_string.split(",")[0]
        x_coor_dir = coor_dir_string.split(",")[1]
        (x_coor_dir, y_coor_dir) = mirror_coordinates(int(x_coor_dir), int(y_coor_dir), 0)

        return input_key_action_split[0] + "*" + \
               str(y_coor) + ',' + str(x_coor) + "*" + \
               str(y_coor_dir) + ',' + str(x_coor_dir)

    # case of activate action
    # format activate input : a*<y coor>,<x coor>

    if input_key_action[0:2] == "a*":
        input_key_action_split = input_key_action.split("*")
        coor_string = input_key_action_split[1]
        y_coor = coor_string.split(",")[0]
        x_coor = coor_string.split(",")[1]
        (x_coor, y_coor) = mirror_coordinates(int(x_coor), int(y_coor))
        return input_key_action_split[0] + "*" + \
               str(y_coor) + ',' + str(x_coor)

    # case of promote action
    # format promote input : p*<y coor>,<x coor>*<class choice first character example:S>
    elif input_key_action[0:2] == "p*":
        input_key_action_split = input_key_action.split("*")
        coor_string = input_key_action_split[1]
        y_coor = coor_string.split(",")[0]
        x_coor = coor_string.split(",")[1]
        (x_coor, y_coor) = mirror_coordinates(int(x_coor), int(y_coor))
        return input_key_action_split[0] + "*" + \
               str(y_coor) + ',' + str(x_coor) + "*" + \
               str(input_key_action_split[2])

    elif input_key_action == "pass":
        return "pass"

    elif input_key_action == "skip":
        return "skip"