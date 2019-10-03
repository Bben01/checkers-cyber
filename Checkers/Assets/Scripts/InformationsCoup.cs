using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class InformationsCoup
{
    public string ErrorMsg { get; }
    public bool HasToEatAgain { get; }
    public bool EndedTurn { get; }
    public Tuple<int, int> PosKilled { get; }

    public InformationsCoup(string errorMsg, bool hasToEatAgain, bool endedTurn, Tuple<int, int> posKilled)
    {
        ErrorMsg = errorMsg;
        HasToEatAgain = hasToEatAgain;
        EndedTurn = endedTurn;
        posKilled = PosKilled;
    }

    public static InformationsCoup CreateDidntMove()
    {
        return new InformationsCoup("The piece didn't move!", false, false, null);
    }

    public static InformationsCoup CreateInvalidMove(string str)
    {
        return new InformationsCoup($"The move is invalid because { str }", false, false, null);
    }

    public static InformationsCoup CreateKillMove(Tuple<int, int> posKilled, bool hasToEatAgain)
    {
        return new InformationsCoup("", hasToEatAgain, !hasToEatAgain, posKilled);
    }

    public static InformationsCoup CreateNormalMove()
    {
        return new InformationsCoup("", false, true, null);
    }
}
