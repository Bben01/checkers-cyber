﻿using System;
using System.Collections.Generic;
using UnityEngine;

public class ValidMoveMethods
{
    // Validate the move
    public static InformationsValidation ValidMove(Piece[,] board, Deplacement d)
    {
        // Pas dans le plateau | probleme - destination occupee
        if (Plateau.OutOfBounds(d.Destination.x, d.Destination.y))
        {
            return InformationsValidation.CreateWrongMove("the target zone is outside the board.");
        }
        if (Plateau.Occupied(board, d.Destination.x, d.Destination.y))
        {
            return InformationsValidation.CreateWrongMove("the target zone is occupied.");
        }
        Piece selected = board[d.Destination.x, d.Destination.y];
        Dictionary<int, Tuple<int, int>> hasToKill = KillerPlayAgain(board, d.Origin.x, d.Origin.y);

        bool hasSomethingToEat = HasSomethingToEat(board, selected.IsWhite);
        bool isKillingAgain = IsKillingAgain(hasToKill, d.Destination.x, d.Destination.y);

        // The player has to kill and is actually killing a piece
        if (hasSomethingToEat && isKillingAgain)
        {
            Vector2Int v = d.EatenPiece();
            return InformationsValidation.CreateKillMove(new Tuple<int, int>(v.x, v.y));
        }
        else if (hasSomethingToEat && !isKillingAgain)
        {
            return InformationsValidation.CreateWrongMove("you are forced to eat another piece.");
        }

        if (selected != null)
        {
            // Didn't move
            if (d.NullMove())
            {
                return InformationsValidation.CreateNotMove();
            }
            // Invalid move
            if (!ValidRules(board, d))
            {
                return InformationsValidation.CreateWrongMove("the rules are not respected.");
            }
            // Normal move
            return InformationsValidation.CreateNormalMove();
        }
        return InformationsValidation.CreateWrongMove("something went wrong...");
    }

    // Validate the rules of the game.
    private static bool ValidRules(Piece[,] board, Deplacement d)
    {
        int x1 = d.Origin.x;
        int x2 = d.Destination.x;
        int y1 = d.Origin.y;
        int y2 = d.Destination.y;

        return Move(board, true, x1, y1, x2, y2) || Move(board, false, x1, y1, x2, y2);
    }

    private static bool Move(Piece[,] board, bool checkWhite, int x1, int y1, int x2, int y2)
    {
        int deltaMoveX = Mathf.Abs(x1 - x2);
        int deltaMoveY = y2 - y1;
        bool IsWhite = board[x1, y1].IsWhite;
        bool isKing = board[x1, y1].IsKing;

        int multiplier = checkWhite ? 1 : -1;

        if (IsWhite && checkWhite || !IsWhite && !checkWhite || isKing)
        {
            if (deltaMoveX == 1 && deltaMoveY == multiplier)
            {
                return true;
            }
        }
        return false;
    }

    // If the piece can eat, it has to eat, and this method checks if it is actually eating
    public static bool IsKillingAgain(Dictionary<int, Tuple<int, int>> hasToKill, int x, int y)
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

    public static bool HasSomethingToEat(Piece[,] board, bool isWhite)
    {
        for (int i = 0; i < board.GetLength(0); i++)
        {
            for (int j = 0; j < board.GetLength(1); j++)
            {
                Piece p = board[i, j];
                if (p != null && p.IsWhite == isWhite && KillerPlayAgain(board, i, j) != null)
                {
                    return true;
                }
            }
        }
        return false;
    }

    public static Dictionary<int, Tuple<int, int>> KillerPlayAgain(Piece[,] board, int x, int y)
    {
        Dictionary<int, Tuple<int, int>> hasToKill = new Dictionary<int, Tuple<int, int>>();

        Vector2Int vPiece = new Vector2Int(x, y);
        Vector2Int[] vectors = {
            Vector2Int.down + Vector2Int.left, Vector2Int.down + Vector2Int.right, Vector2Int.up + Vector2Int.left, Vector2Int.up + Vector2Int.right
        };

        bool hasKilled = false;
        int count = 0;

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
        return hasKilled ? hasToKill : null;
    }

    private static bool Check(Piece[,] board, Vector2Int v, Vector2Int direction)
    {
        int rangeX = v.x + direction.x * 2;
        int rangeY = v.y + direction.y * 2;

        if (Plateau.OutOfBounds(rangeX, rangeY) || board[v.x + direction.x, v.y + direction.y] == null)
        {
            return false;
        }

        bool differentColor = board[v.x + direction.x, v.y + direction.y].IsWhite != board[v.x, v.y].IsWhite;
        bool unnocupiedTarget = board[rangeX, rangeY] == null;

        return differentColor && unnocupiedTarget;
    }

    public static bool CheckNewQueen(Deplacement d, bool checkWhite)
    {
        int zoneDames = checkWhite ? 0 : Plateau.taillePlateau - 1;
        if (d.Destination.x == zoneDames)
        {
            return true;
        }
        return false;
    }
}
