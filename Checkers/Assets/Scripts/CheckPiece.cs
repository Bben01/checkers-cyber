using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CheckPiece : MonoBehaviour
{
    public bool IsKing { get; set; }
    public bool IsWhite { get; }

    public CheckPiece(bool white)
    {
        IsWhite = white;
        IsKing = false;
    }

}
