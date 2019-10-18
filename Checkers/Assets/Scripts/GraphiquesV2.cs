﻿using System;
using UnityEngine;

public class GraphiquesV2 : MonoBehaviour
{
    public static readonly int taillePlateau = 8;
    public Piece[,] board; // TODO: faire quelque chose

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
            string[] returnInfos = Client.FormatSendAndResponse("try_move_piece", new string[5] { $"{startClick.x}", $"{startClick.y}", $"{x}", $"{y}", $"{hasToPlayAgain}"});
            AnalizeInfo(returnInfos);
        }
    }

    private void AnalizeInfo(string[] returnInfos)
    {
        // Error
        if (Helper.Activate(returnInfos[0], 0))
        {
            AfficherError(returnInfos[0].Substring(2));
            if (Helper.Activate(returnInfos[0], 1))
            {
                Reset();
            }
            return;
        }
        // Just move visually the piece
        Vector2Int lastDeplacement = Helper.GetLastDeplacementDest(returnInfos[4]);
        MovePieceVisual(selectedPiece, lastDeplacement.x, lastDeplacement.y);
        // New Queen
        if (Helper.Activate(returnInfos[1], 0))
        {
            AnimateQueen(Helper.GetPosNewQueen(returnInfos[1]));
        }
        // Killed
        if (Helper.Activate(returnInfos[2], 0))
        {
            Vector2Int posKilled = Helper.GetPosKilled(returnInfos[2]);
            Debug.Log($"Piece Killed: { posKilled }");
            // Has to play again
            if (Helper.Activate(returnInfos[2], 3))
            {
                hasToPlayAgain = true;
                posPieceToPlay = posKilled;
                startClick = lastDeplacement;
            }
        }
        // Ended turn
        if (Helper.Activate(returnInfos[3], 0))
        {
            EndTurn();
        }
    }

    private void Reset()
    {
        clicked = false;
        if (selectedPiece != null)
        {
            MovePieceVisual(selectedPiece, startClick.x, startClick.y);
            selectedPiece = null;
        }
        startClick = Vector2Int.zero;
    }

    private void EndTurn()
    {
        clicked = false;
        selectedPiece = null;
        hasToPlayAgain = false;
        startClick = Vector2Int.zero;
    }

    private void GenerateBoard()
    {
        // Generate white team
        for (int y = 0; y < (taillePlateau - 1) / 2; y++)
        {
            bool oddRow = y % 2 == 0;
            for (int x = 0; x < taillePlateau; x += 2)
            {
                // Generate the piece
                GeneratePiece(oddRow ? x : x + 1, y, true);
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
            }
        }
    }

    private void GeneratePiece(int x, int y, bool isWhite)
    {
        GameObject go = Instantiate(isWhite ? whitePiecePrefab : blackPiecePrefab) as GameObject;
        go.transform.SetParent(transform);
        Piece p = go.GetComponent<Piece>();
        p.IsWhite = isWhite;
        board[x, y] = p;
        MovePieceVisual(p, x, y);
        Client.FormatSendAndResponse("generate_board_submethod", new string[3] { $"{x}", $"{y}", $"{isWhite}" });
    }

    private void MovePieceVisual(Piece p, int x, int y)
    {
        p.transform.position = (Vector3.right * x) + (Vector3.forward * y) + boardOffset + pieceOffset;
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

    private void SelectPiece(int x, int y)
    {
        // Out of bounds
        if (x < 0 || x >= taillePlateau || y < 0 || y >= taillePlateau || clicked)
        {
            return;
        }
        Piece p = board[x, y];
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
        if (Helper.IsTrue(Client.FormatSendAndResponse("can_eat"), 0))
        {
            hasSomethingToEat = true;

            // Can't move the piece if this is not one of the selectable
            if (Helper.IsTrue(Client.FormatSendAndResponse("selectable", new string[2] { $"{x}", $"{y}" }), 0))
            {
                AfficherError("Another piece is forced to be played!");
                return;
            }
        }
        // Good selection
        if (p != null && p.IsWhite == Helper.IsTrue(Client.FormatSendAndResponse("is_white_turn"), 0) && Helper.IsTrue(Client.FormatSendAndResponse("selectable", new string[3] { $"{x}", $"{y}", $"{Helper.GetBools(!hasSomethingToEat)}" }), 0))
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

    public void AnimateQueen(Tuple<int, int> pos)
    {
        // TODO: a implementer
        // Just for now: 
        if (pos == null)
        {
            Debug.Log("Error with new Queen.");
            return;
        }
        Debug.Log("New Queen!");
        Piece p = board[pos.Item1, pos.Item2];
        p.transform.Rotate(180, 0, 0, Space.Self);
    }

    public static void AfficherError(string errorMessage)
    {
        // TODO: a implementer
        // Just for now:
        Debug.Log(errorMessage);
    }
}
