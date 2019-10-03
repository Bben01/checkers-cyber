using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Deplacement
{
    public Vector2Int Origin { get; }
    public Vector2Int Destination { get; }

    public Deplacement(int x1, int y1, int x2, int y2)
    {
        Origin = new Vector2Int(x1, y1);
        Destination = new Vector2Int(x2, y2);
    }

    public bool NullMove()
    {
        return Origin == Destination;
    }

    // Returns the position of the eaten piece, if there is no, the return is very bad
    public Vector2Int EatenPiece()
    {
        return Vector2Int.Max(Origin, Destination) - Vector2Int.one;
    }
}
