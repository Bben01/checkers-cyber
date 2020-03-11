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

    // Returns the position of the eaten piece, if there is no, the return is a Vector2Int.zero => (0, 0)
    public Vector2Int EatenPiece()
    {
        int sumX = Origin.x + Destination.x;
        int sumY = Origin.y + Destination.y;
        bool okX = (sumX) % 2 == 0;
        bool okY = (sumY) % 2 == 0;
        return okX && okY ? new Vector2Int(sumX / 2, sumY / 2) : Vector2Int.zero;
    }
}
