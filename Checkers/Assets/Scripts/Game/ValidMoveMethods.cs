using System;
using System.Collections.Generic;
using UnityEngine;

public class ValidMoveMethods
{
    // Validate the move
    public static InformationsValidation ValidMove(Piece[,] board, Deplacement d, bool hasToEatAgain)
    {
        if (d.NullMove())
        {
            return InformationsValidation.CreateNotMove();
        }
        // Pas dans le plateau | probleme - destination occupee
        if (Plateau.OutOfBounds(d.Destination.x, d.Destination.y))
        {
            return InformationsValidation.CreateWrongMove("the target zone is outside the board.");
        }
        if (Plateau.Occupied(board, d.Destination.x, d.Destination.y))
        {
            return InformationsValidation.CreateWrongMove("the target zone is occupied.");
        }
        Piece selected = board[d.Origin.x, d.Origin.y];
        Dictionary<int, Tuple<int, int>> hasToKill = CalculateEatPositions(board, d.Origin.x, d.Origin.y, false, true, hasToEatAgain);

        bool hasSomethingToEat = HasSomethingToEat(board, selected.IsWhite, hasToEatAgain);
        bool isKillingAgain = hasSomethingToEat ? IsKillingAgain(hasToKill, d.Destination.x, d.Destination.y) : false;

        // The player has to kill and is actually killing a piece
        if (hasSomethingToEat && isKillingAgain)
        {
            Vector2Int v = d.EatenPiece();
            return InformationsValidation.CreateKillMove(new Tuple<int, int>(v.x, v.y));
        }
        else if (hasSomethingToEat && !isKillingAgain)
        {
            return InformationsValidation.CreateWrongMove("you are forced to eat a piece.");
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

    public static bool HasSomethingToEat(Piece[,] board, bool isWhite, bool hasToEatAgain)
    {
        for (int i = 0; i < board.GetLength(0); i++)
        {
            for (int j = 0; j < board.GetLength(1); j++)
            {
                Piece p = board[i, j];
                if (p != null && p.IsWhite == isWhite && CalculateEatPositions(board, i, j, false, true, hasToEatAgain) != null)
                {
                    return true;
                }
            }
        }
        return false;
    }

    public static Dictionary<int, Tuple<int, int>> CalculateEatPositions(Piece[,] board, int x, int y, bool checkNormal, bool checkKillPositions, bool hasToEatAgain)
    {
        Dictionary<int, Tuple<int, int>> positions = new Dictionary<int, Tuple<int, int>>();

        Vector2Int vPiece = new Vector2Int(x, y);
        Vector2Int[] vectors = {
            Vector2Int.down + Vector2Int.left, Vector2Int.down + Vector2Int.right, Vector2Int.up + Vector2Int.left, Vector2Int.up + Vector2Int.right
        };

        bool emptyDict = true;
        int countPositive = 1;
        int countNegative = -1;

        foreach (Vector2Int vector in vectors)
        {
            if (checkKillPositions && Check(board, vPiece, vector) && (hasToEatAgain || CanMoveDirection(board, x, y, vector)))
            {
                positions.Add(countPositive, new Tuple<int, int>(vPiece.x + vector.x * 2, vPiece.y + vector.y * 2));
                emptyDict = false;
                countPositive++;
                Debug.Log("Le pion peut manger: " + (vector + vPiece));
            }

            bool ok = checkNormal && !Plateau.OutOfBounds(vPiece.x + vector.x, vPiece.y + vector.y) && board[vPiece.x + vector.x, vPiece.y + vector.y] == null;
            if (ok && CanMoveDirection(board, x, y, vector))
            {
                positions.Add(countNegative, new Tuple<int, int>(vPiece.x + vector.x, vPiece.y + vector.y));
                emptyDict = false;
                countNegative--;
                Debug.Log("Le pion peut se deplacer sur la case: " + (vector + vPiece));
            }
        }

        return !emptyDict ? positions : null;
    }

    public static bool CanMoveDirection(Piece[,] board, int x, int y, Vector2Int direction)
    {
        Piece p = board[x, y];
        if (p.IsKing)
            return true;
        if (p.IsWhite)
            return direction == Vector2Int.up + Vector2Int.left || direction == Vector2Int.up + Vector2Int.right;

        return direction == Vector2Int.down + Vector2Int.left || direction == Vector2Int.down + Vector2Int.right;
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
        int zoneDames = checkWhite ? Plateau.taillePlateau - 1 : 0;
        if (d.Destination.y == zoneDames)
        {
            return true;
        }
        return false;
    }

    public static Tuple<int, int> PosNewQueen(bool isNewQueen, Deplacement d)
    {
        return isNewQueen ? new Tuple<int, int>(d.Destination.x, d.Destination.y) : null;
    }
}