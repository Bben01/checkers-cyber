using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Piece : MonoBehaviour
{
    public bool IsKing { get; set; }
    public bool IsWhite { get; set; }

    public Piece(bool white)
    {
        IsWhite = white;
        IsKing = false;
    }

    public Piece(Piece p)
    {
        IsWhite = p.IsWhite;
        IsKing = p.IsKing;
    }

}
