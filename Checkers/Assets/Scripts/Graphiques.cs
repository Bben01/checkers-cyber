﻿using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Graphiques : MonoBehaviour
{
    public static readonly int taillePlateau = 8;
    public Plateau plateau;

    public GameObject whitePiecePrefab;
    public GameObject blackPiecePrefab;

    private Vector3 boardOffset = new Vector3(-4.0f, 0, -4.0f);
    private Vector3 pieceOffset = new Vector3(0.5f, 0.1f, 0.5f);

    private Piece selectedPiece;

    private Vector2 mouseOver;
    private Vector2Int startClick;

    private bool clicked;

    private bool hasToPlayAgain;
    private Vector2Int posPieceToPlay;

    // Start is called before the first frame update
    void Start()
    {
        plateau = new Plateau();
        GenerateBoard();
        clicked = false;
    }

    // Update is called once per frame
    void Update()
    {
        UpdateMouseOver();

        int x = (int)mouseOver.x;
        int y = (int)mouseOver.y;
        if (selectedPiece != null)
        {
            UpdatePieceDrag(selectedPiece);
        }
        if (Input.GetMouseButtonDown(0) && !clicked)
        {
            SelectPiece(x, y);
            return;
        }
        if (Input.GetMouseButtonDown(0) && clicked)
        {
            InformationsCoup infos =  plateau.TryMove(new Deplacement(startClick.x, startClick.y, x, y), hasToPlayAgain);
            AnalizeInfo(infos);
        }
    }
    

    private void GenerateBoard()
    {
        int numWhite = 0;
        int numBlack = 0;
        // Generate white team
        for (int y = 0; y < (taillePlateau - 1) / 2; y++)
        {
            bool oddRow = y % 2 == 0;
            for (int x = 0; x < taillePlateau; x += 2)
            {
                // Generate the piece
                GeneratePiece(oddRow ? x : x + 1, y, true);
                numWhite++;
            }
        }

        // Generate black team
        for (int y = taillePlateau - 1; y > (taillePlateau - 1) / 2 + 1; y--)
        {
            bool oddRow = y % 2 == 0;
            for (int x = 0; x < taillePlateau; x += 2)
            {
                // Generate the piece
                GeneratePiece(oddRow ? x : x + 1, y, false);
                numBlack++;
            }
        }

        plateau.NumWhite = numWhite;
        plateau.NumBlack = numBlack;
    }

    private void GeneratePiece(int x, int y, bool isWhite)
    {
        // TODO: a adapter pour la nouvelle version
        GameObject go = Instantiate(isWhite ? whitePiecePrefab : blackPiecePrefab) as GameObject;
        go.transform.SetParent(transform);
        Piece p = go.GetComponent<Piece>();
        p.IsWhite = isWhite;
        plateau.pieces[x, y] = p;
        MovePieceVisual(p, x, y);
    }

    private void MovePieceVisual(Piece p, int x, int y)
    {
        p.transform.position = (Vector3.right * x) + (Vector3.forward * y) + boardOffset + pieceOffset;
    }

    private void SelectPiece(int x, int y)
    {
        // Out of bounds
        if (x < 0 || x >= taillePlateau || y < 0 || y >= taillePlateau || clicked)
        {
            return;
        }
        Piece p = plateau.pieces[x, y];
        if (hasToPlayAgain)
        {
            if (posPieceToPlay.x == x && posPieceToPlay.y == y)
            {
                SelectCorrectPiece(p, x, y);
                hasToPlayAgain = false;
            }
            else
            {
                Debug.Log("Non, c'est pas celle la...");
                return;
            }
        }
        bool hasSomethingToEat = false;
        if (ValidMoveMethods.HasSomethingToEat(plateau.pieces, plateau.isWhiteTurn, false))
        {
            hasSomethingToEat = true;

            // Can't move the piece if this is not one of the selectable
            if (ValidMoveMethods.CalculateEatPositions(plateau.pieces, x, y, false, true, false) == null)
            {
                AfficherError("Another piece is forced to be played!");
                return;
            }
        }
        // Good selection
        if (p != null && p.IsWhite == plateau.isWhiteTurn && ValidMoveMethods.CalculateEatPositions(plateau.pieces, x, y, !hasSomethingToEat, true, false) != null)
        {
            SelectCorrectPiece(p, x, y);
        }
        else
        {
            AfficherError("This piece cannot be selected!");
        }

    }

    // Called to select a piece that has been verified
    private void SelectCorrectPiece(Piece p, int x, int y)
    {
        selectedPiece = p;
        startClick = new Vector2Int(x, y);
        clicked = true;
    }

    private void UpdateMouseOver()
    {
        if (!Camera.main)
        {
            Debug.Log("Unable to find main Camera");
            return;
        }

        if (Physics.Raycast(Camera.main.ScreenPointToRay(Input.mousePosition), out RaycastHit hit, 25.0f, LayerMask.GetMask("Board")))
        {
            mouseOver.x = (int)(hit.point.x - boardOffset.x);
            mouseOver.y = (int)(hit.point.z - boardOffset.z);
        }
        else
        {
            mouseOver.x = -1;
            mouseOver.y = -1;
        }
    }

    private void UpdatePieceDrag(Piece p)
    {
        if (!Camera.main)
        {
            Debug.Log("Unable to find main Camera");
            return;
        }

        if (Physics.Raycast(Camera.main.ScreenPointToRay(Input.mousePosition), out RaycastHit hit, 25.0f, LayerMask.GetMask("Board")))
        {
            p.transform.position = hit.point + (Vector3.up / 2);
        }
    }

    private void AnalizeInfo(InformationsCoup infos)
    {
        // There was an error
        if (infos.ErrorMsg != "")
        {
            AfficherError(infos.ErrorMsg);
            if (!hasToPlayAgain)
            {
                ResetPositions();
            }
            return;
        }
        MovePieceVisual(selectedPiece, infos.LastDeplacement.Destination.x, infos.LastDeplacement.Destination.y);
        // There is a new Queen
        if (infos.IsNewQueen)
        {
            AnimateQueen(infos.PosNewQueen);
            plateau.pieces[infos.PosNewQueen.Item1, infos.PosNewQueen.Item2].IsKing = true;
        }
        if (infos.PosKilled != null)
        {
            Destroy(infos.PieceKilled.gameObject);
        }
        // Turn is ok, just ended
        if (infos.EndedTurn)
        {
            EndTurn(infos.LastDeplacement);
        }
        // Killed
        if (infos.HasToEatAgain)
        {
            Debug.Log($"Piece Killed: { infos.PosKilled }");
            hasToPlayAgain = true;
            posPieceToPlay = new Vector2Int(infos.PosKilled.Item1, infos.PosKilled.Item2);
            startClick = new Vector2Int(infos.LastDeplacement.Destination.x, infos.LastDeplacement.Destination.y);
        }
    }

    private void EndTurn(Deplacement lastDeplacement)
    {
        bool victory = CheckVictory(plateau.isWhiteTurn);
        plateau.EndTurn(lastDeplacement);
        clicked = false;
        selectedPiece = null;
        hasToPlayAgain = false;
        startClick = Vector2Int.zero;
    }

    private bool CheckVictory(bool checkWhite)
    {
        // TODO: a implementer
        // Just for now:
        if (!plateau.HasPiecesLeft(!checkWhite))
        {
            Debug.Log(checkWhite ? "White won!" : "Black won!");
            return true;
        }
        return false;
    }

    public void ResetPositions()
    {
        clicked = false;
        if (selectedPiece != null)
        {
            MovePieceVisual(selectedPiece, startClick.x, startClick.y);
            selectedPiece = null;
        }
        startClick = Vector2Int.zero;
    }

    public void AnimateQueen(Tuple<int, int> pos)
    {
        // TODO: a implementer
        // Just for now: 
        Debug.Log("New Queen!");
        plateau.pieces[pos.Item1, pos.Item2].IsKing = true;
    }

    public void AfficherError(string errorMessage)
    {
        // TODO: a implementer
        // Just for now:
        Debug.Log(errorMessage);
    }
}
