using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Plateau
{
    public static readonly int taillePlateau = 8;
    public Piece[,] pieces = new Piece[taillePlateau, taillePlateau];

    public Stack<TourDeJeu> historique = new Stack<TourDeJeu>();

    // TODO: voir quand est ce que tour de jeu peut servir (pour rejouer par example) et du coup quand est ce que il va reelement etre instancie
    public TourDeJeu currentTourDeJeu;

    public bool isWhiteTurn;

    // Keeps track of the number of pieces on-board
    private int numWhite;
    private int numBlack;

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

    public InformationsCoup TryMove(Deplacement d)
    {
        InformationsValidation status = ValidMoveMethods.ValidMove(pieces, d);
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
            bool isNewQueen = ValidMoveMethods.CheckNewQueen(d, isWhiteTurn);
            // Killed
            if (status.Killed)
            {
                numWhite -= isWhiteTurn ? 0 : 1;
                numBlack -= isWhiteTurn ? 1 : 0;
                // If the player does not have to eat again
                if (ValidMoveMethods.KillerPlayAgain(pieces, d.Destination.x, d.Destination.y) == null)
                {
                    EndTurn(currentTourDeJeu, d);
                    return InformationsCoup.CreateKillMove(status.KillPosition, false, d).AddNewQueen(isNewQueen, ValidMoveMethods.PosNewQueen(isNewQueen, d));
                }
                else
                {
                    currentTourDeJeu.AddDeplacement(d);
                    return InformationsCoup.CreateKillMove(status.KillPosition, true, d).AddNewQueen(isNewQueen, ValidMoveMethods.PosNewQueen(isNewQueen, d));
                }
            }
            // Normal move 
            if (status.NormalMove)
            {
                EndTurn(currentTourDeJeu, d);
                return InformationsCoup.CreateNormalMove(d).AddNewQueen(isNewQueen, ValidMoveMethods.PosNewQueen(isNewQueen, d));
            }
        }
        return InformationsCoup.CreateInvalidMove("something went wrong...");
    }

    private void EndTurn(TourDeJeu t, Deplacement lastDeplacement)
    {
        t.AddDeplacement(lastDeplacement);
        isWhiteTurn = !isWhiteTurn;
        historique.Push(t);
        currentTourDeJeu = null;
    }
}
