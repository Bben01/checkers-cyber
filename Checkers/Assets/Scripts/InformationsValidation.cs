using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class InformationsValidation
{
    public bool ValidMove { get; }
    public bool Killed { get; }
    public bool DidntMoved { get; }
    public bool NormalMove { get; }
    public Tuple<int, int> KillPosition { get; }
    public string ErrorMessage { get; set; }

    public InformationsValidation(bool validMove, bool killed, bool didntMoved, bool normalMove, Tuple<int, int> killPosition, string errorMessage)
    {
        ValidMove = validMove;
        Killed = killed;
        DidntMoved = didntMoved;
        NormalMove = normalMove;
        KillPosition = killPosition;
        ErrorMessage = errorMessage;
    }

    public static InformationsValidation CreateNormalMove()
    {
        return new InformationsValidation(true, false, false, true, null, "");
    }

    public static InformationsValidation CreateKillMove(Tuple<int, int> killPosition)
    {
        return new InformationsValidation(true, true, false, false, killPosition, "");
    }

    public static InformationsValidation CreateNotMove()
    {
        return new InformationsValidation(false, false, true, false, null, "The piece didn't move");
    }

    public static InformationsValidation CreateWrongMove(string errorMessage)
    {
        return new InformationsValidation(false, false, false, false, null, errorMessage);
    }
}
