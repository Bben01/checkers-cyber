using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Deplacement : MonoBehaviour
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
}
