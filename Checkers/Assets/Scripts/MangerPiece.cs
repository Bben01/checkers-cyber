using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MangerPiece : MonoBehaviour
{
    private bool InBoard(int x, int y)
    {
        return !(x < 0 || x > CheckersBoard.taillePlateau || y < 0 || y > CheckersBoard.taillePlateau);
    }

    private bool Unnocupied(Piece[,] board, int x, int y)
    {
        return true;
    }

    private bool Check(Piece[,] board, Vector2Int v, Vector2Int direction)
    {
        int rangeX = v.x + direction.x * 2;
        int rangeY = v.y + direction.y * 2;

        bool inRange = InBoard(rangeX, rangeY);
        bool differentColor = board[v.x + rangeX, v.y + rangeY].isWhite != board[v.x, v.y].isWhite;
        bool unnocupiedTarget = board[rangeX, rangeY] == null;

        return inRange && differentColor && unnocupiedTarget;
    }

    public bool CanEat(Piece[,] board, int x, int y, out Dictionary<int, Tuple<int, int>> hasToKill)
    {
        hasToKill = new Dictionary<int, Tuple<int, int>>();

        Vector2Int vPiece = new Vector2Int(x, y);
        Vector2Int[] vectors = {
            Vector2Int.down + Vector2Int.left, Vector2Int.down + Vector2Int.right, Vector2Int.up + Vector2Int.left, Vector2Int.up + Vector2Int.right
        };

        int count = 0;
        bool hasKilled = false;

        foreach (Vector2Int vector in vectors)
        {
            if (Check(board, vPiece, vector))
            {
                hasToKill.Add(count, new Tuple<int, int>(vPiece.x + vector.x * 2, vPiece.y + vector.y * 2));
                hasKilled = true;
                count++;
                Debug.Log("Le pion peut manger: " + (vector + vPiece));
            }
        }

        if (!hasKilled)
        {
            CheckersBoard.hasToKill = false;
            hasToKill = null;
        }
        return hasKilled;
    }
}
