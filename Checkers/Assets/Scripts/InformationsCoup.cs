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
    public bool IsNewQueen { get; set; }
    public Tuple<int, int> PosNewQueen { get; set; }
    public Deplacement LastDeplacement { get; }

    public InformationsCoup(string errorMsg, bool hasToEatAgain, bool endedTurn, Tuple<int, int> posKilled, Deplacement lastDeplacement)
    {
        ErrorMsg = errorMsg;
        HasToEatAgain = hasToEatAgain;
        EndedTurn = endedTurn;
        PosKilled = posKilled;
        IsNewQueen = false;
        PosNewQueen = null;
        LastDeplacement = lastDeplacement;
    }

    public static InformationsCoup CreateDidntMove()
    {
        return new InformationsCoup("The piece didn't move!", false, false, null, null);
    }

    public static InformationsCoup CreateInvalidMove(string str)
    {
        return new InformationsCoup($"The move is invalid because { str }", false, false, null, null);
    }

    public static InformationsCoup CreateKillMove(Tuple<int, int> posKilled, bool hasToEatAgain, Deplacement lastDeplacement)
    {
        return new InformationsCoup("", hasToEatAgain, !hasToEatAgain, posKilled, lastDeplacement);
    }

    public static InformationsCoup CreateNormalMove(Deplacement lastDeplacement)
    {
        return new InformationsCoup("", false, true, null, lastDeplacement);
    }

    public InformationsCoup AddNewQueen(bool isNewQueen, Tuple<int, int> posNewQueen)
    {
        IsNewQueen = isNewQueen;
        PosNewQueen = posNewQueen;
        return this;
    }


}
