using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Plateau
{
    public static readonly int taillePlateau = 8;
    public Piece[,] pieces = new Piece[taillePlateau, taillePlateau];

    public Stack<TourDeJeu> historique = new Stack<TourDeJeu>();

    public TourDeJeu currentTourDeJeu;

    public bool isWhiteTurn;

    // Keeps track of the number of pieces on-board
    public int NumWhite { get; set; }
    public int NumBlack { get; set; }

    public Plateau()
    {
        isWhiteTurn = true;
    }

    public static bool OutOfBounds(int x, int y)
    {
        return x < 0 || y < 0 || x >= taillePlateau || y >= taillePlateau;
    }

    public static bool Occupied(Piece[,] board, int x, int y)
    {
        try
        {
            return board[x, y] != null;
        }
        catch (System.IndexOutOfRangeException)
        {
            return true;
        }

    }

    public InformationsCoup TryMove(Deplacement d, bool hasToEatAgain)
    {
        InformationsValidation status = ValidMoveMethods.ValidMove(pieces, d, hasToEatAgain);
        if (currentTourDeJeu == null)
        {
            currentTourDeJeu = new TourDeJeu();
        }
        // Didn't move
        if (status.DidntMoved)
        {
            return InformationsCoup.CreateDidntMove();
        }
        // Invalid move
        if (!status.ValidMove)
        {
            return InformationsCoup.CreateInvalidMove(status.ErrorMessage);
        }
        else
        {
            bool isNewQueen = !pieces[d.Origin.x, d.Origin.y].IsKing && ValidMoveMethods.CheckNewQueen(d, isWhiteTurn);
            // Killed
            if (status.Killed)
            {
                Piece pKilled = GetKilledPiece(d);
                NumWhite -= isWhiteTurn ? 0 : 1;
                NumBlack -= isWhiteTurn ? 1 : 0;
                MovePieceBoard(d);
                // If the player does not have to eat again
                if (ValidMoveMethods.CalculateEatPositions(pieces, d.Destination.x, d.Destination.y, false, true, true) == null)
                {
                    return InformationsCoup.CreateKillMove(status.KillPosition, false, d, pKilled).AddNewQueen(isNewQueen, ValidMoveMethods.PosNewQueen(isNewQueen, d));
                }
                else
                {
                    currentTourDeJeu.AddDeplacement(d);
                    return InformationsCoup.CreateKillMove(status.KillPosition, true, d, pKilled).AddNewQueen(isNewQueen, ValidMoveMethods.PosNewQueen(isNewQueen, d));
                }
            }
            // Normal move 
            if (status.NormalMove)
            {
                MovePieceBoard(d);
                return InformationsCoup.CreateNormalMove(d).AddNewQueen(isNewQueen, ValidMoveMethods.PosNewQueen(isNewQueen, d));
            }
        }
        return InformationsCoup.CreateInvalidMove("something went wrong...");
    }

    public void EndTurn(Deplacement lastDeplacement)
    {
        if (currentTourDeJeu == null)
        {
            return;
        }
        currentTourDeJeu.AddDeplacement(lastDeplacement);
        isWhiteTurn = !isWhiteTurn;
        historique.Push(currentTourDeJeu);
        currentTourDeJeu = null;
    }

    private void MovePieceBoard(Deplacement d)
    {
        pieces = UpdatePieceBoard(pieces, d);
        Debug.Log("Piece moved!");
    }

    public Piece[,] UpdatePieceBoard(Piece[,] board, Deplacement d)
    {
        board[d.Destination.x, d.Destination.y] = board[d.Origin.x, d.Origin.y];
        board[d.Origin.x, d.Origin.y] = null;
        Vector2Int eaten = d.EatenPiece();
        if (eaten != Vector2Int.zero)
        {
            board[eaten.x, eaten.y] = null;
        }
        return board;
    }

    private Piece GetKilledPiece(Deplacement d)
    {
        Vector2Int eaten = d.EatenPiece();
        return eaten != Vector2Int.zero ? pieces[eaten.x, eaten.y] : null;
    }

    public bool HasPiecesLeft(bool checkWhite)
    {
        return checkWhite ? NumWhite != 0 : NumBlack != 0;
    }
}
