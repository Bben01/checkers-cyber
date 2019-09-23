using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;

public class Piece : MonoBehaviour
{
    public bool isWhite;
    public bool isKing;
    public Dictionary<int, Tuple<int, int>> hasToKill;
    public int x;
    public int y;

    public bool ValidMove(Piece[,] board, int x1, int y1, int x2, int y2)
    {
        // Moving on the top of another piece
        if (board[x2, y2] != null)
        {
            return false;
        }
        if (CheckersBoard.hasToKill && IsKillingAgain(x2, y2))
        {
            hasToKill = null;
            return true;
        }
        return Move(board, true, x1, y1, x2, y2) || Move(board, false, x1, y1, x2, y2);
    }

    private bool Move(Piece[,] board, bool checkWhite, int x1, int y1, int x2, int y2)
    {
        int deltaMoveX = Mathf.Abs(x1 - x2);
        int deltaMoveY = y2 - y1;

        int multiplier = checkWhite ? 1 : -1;

        if (isWhite && checkWhite || !isWhite && !checkWhite || isKing)
        {
            if (deltaMoveX == 1 && deltaMoveY == multiplier)
            {
                return true;
            }
            else if (deltaMoveX == 2 && deltaMoveY == 2 * multiplier)
            {
                Piece p = board[(x1 + x2) / 2, (y1 + y2) / 2];
                if (p != null && p.isWhite != isWhite)
                {
                    return true;
                }
            }
        }
        return false;
    }

    public bool IsKillingAgain(int x, int y)
    {
        foreach (KeyValuePair<int, Tuple<int, int>> entry in hasToKill)
        {
            if (entry.Value.Item1 == x && entry.Value.Item2 == y)
            {
                return true;
            }
        }
        return false;
    }

    public bool KillerPlayAgain(Piece[,] board, int x, int y)/* , out Dictionary<int, Tuple<int, int>> hasToKill */
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

    private bool InBoard(int x, int y)
    {
        return !(x < 0 || x > CheckersBoard.taillePlateau - 1 || y < 0 || y > CheckersBoard.taillePlateau - 1);
    }

    private bool Unnocupied(Piece[,] board, int x, int y)
    {
        return true;
    }

    private bool Check(Piece[,] board, Vector2Int v, Vector2Int direction)
    {
        int rangeX = v.x + direction.x * 2;
        int rangeY = v.y + direction.y * 2;

        if (!InBoard(rangeX, rangeY) || board[v.x + direction.x, v.y + direction.y] == null)
        {
            return false;
        }

        bool differentColor = board[v.x + direction.x, v.y + direction.y].isWhite != board[v.x, v.y].isWhite;
        bool unnocupiedTarget = board[rangeX, rangeY] == null;

        return differentColor && unnocupiedTarget;
    }
}
