using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Plateau : MonoBehaviour
{
    public static readonly int taillePlateau = 8;
    public static Piece[,] pieces = new Piece[taillePlateau, taillePlateau];

    public static Stack<TourDeJeu> historique = new Stack<TourDeJeu>();

    // TODO: voir quend est ce que tour de jeu peut servir (pour rejouer par example) et du coup quand est ce que il va reelement etre instancie
    public static TourDeJeu currentTourDeJeu;

    public static bool isWhiteTurn;

    // Keeps track of the number of pieces on-board
    private static int numWhite;
    private static int numBlack;

    public Plateau ()
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

    public bool TryMove(Deplacement d)
    {
        int status = ValidMoveMethods.ValidMove(pieces, d);
        // Didn't move
        if (status == 0)
        {
            return false;
        }
        // Invalid move
        if (status == -1)
        {
            Graphiques.AfficherError("This move is invalid!");
        }
        // Killed
        if (status == 1)
        {
            numWhite -= isWhiteTurn ? 0 : 1;
            numBlack -= isWhiteTurn ? 1 : 0;
            if (ValidMoveMethods.KillerPlayAgain(pieces, d.Destination.x, d.Destination.y) == null)
            {
                status = 2;
            }
            else
            {
                currentTourDeJeu.AddDeplacement(d);
                Graphiques.Reset();
            }
        }
        // Normal move 
        if (status == 2)
        {
            currentTourDeJeu.AddDeplacement(d);
            EndTurn(currentTourDeJeu);
        }
        return false;
    }

    private void EndTurn(TourDeJeu t)
    {
        isWhiteTurn = !isWhiteTurn;
        historique.Push(t);
        currentTourDeJeu = null;
        Graphiques.EndTurn();
    }
}
