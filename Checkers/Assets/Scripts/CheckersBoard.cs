using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CheckersBoard : MonoBehaviour
{
    public static readonly int taillePlateau = 8;
    public Piece[,] pieces = new Piece[taillePlateau, taillePlateau];
    public GameObject whitePiecePrefab;
    public GameObject blackPiecePrefab;

    private Vector3 boardOffset = new Vector3(-4.0f, 0, -4.0f);
    private Vector3 pieceOffset = new Vector3(0.5f, 0.1f, 0.5f);

    private Vector2 mouseOver;
    private Vector2 startDrag;
    private Vector2 endDrag;

    private Piece selectedPiece;

    private bool isWhiteTurn;

    private int numWhite;
    private int numBlack;

    // Coordinates of the piece the player has to play
    private bool hasKilled = false;
    public static bool hasToKill = false;
    private int x;
    private int y;
    // Start is called before the first frame update
    void Start()
    {
        isWhiteTurn = true;
        GenerateBoard();

        numWhite = (taillePlateau / 2) * (taillePlateau / 2 - 1);
        numBlack = numWhite;

    }
    private void Update()
    {
        UpdateMouseOver();

        int x = (int)mouseOver.x;
        int y = (int)mouseOver.y;
        if (selectedPiece != null)
        {
            UpdatePieceDrag(selectedPiece);
        }
        if (Input.GetMouseButtonDown(0))
        {
            SelectPiece(x, y);
        }
        if (Input.GetMouseButtonUp(0))
        {
            TryMove((int)startDrag.x, (int)startDrag.y, x, y);
        }
    }

    private void TryMove(int x1, int y1, int x2, int y2)
    {
        startDrag = new Vector2(x1, y1);
        endDrag = new Vector2(x2, y2);
        selectedPiece = pieces[x1, y1];

        // Checks if the selected piece will do a correct move
        // Out of bounds
        if (x2 < 0 || x2 >= taillePlateau || y2 < 0 || y2 >= taillePlateau)
        {
            if (selectedPiece != null)
            {
                MovePiece(selectedPiece, x1, y1);
            }
            startDrag = Vector2.zero;
            selectedPiece = null;
            return;
        }

        if (selectedPiece != null)
        {
            // If it has not moved
            if (endDrag == startDrag)
            {
                ResetMove(x1, y1);
                return;
            }

            // Check if it's a valid move
            if (selectedPiece.ValidMove(pieces, x1, y1, x2, y2))
            {
                // Kill?
                // Jump?
                if (Mathf.Abs(x1 - x2) == 2)
                {
                    int posXKillPiece = (x1 + x2) / 2, posYKillPiece = (y1 + y2) / 2;
                    Piece p = pieces[posXKillPiece, posYKillPiece];
                    if (p != null)
                    {
                        pieces[posXKillPiece, posYKillPiece] = null;
                        numWhite -= p.isWhite ? 1 : 0;
                        numBlack -= p.isWhite ? 0 : 1;
                        Destroy(p.gameObject);
                        hasKilled = true;
                    }
                }

                pieces[x2, y2] = selectedPiece;
                pieces[x1, y1] = null;
                MovePiece(selectedPiece, x2, y2);

                if (hasKilled)
                {
                    pieces[x2, y2].KillerPlayAgain(pieces, x2, y2);
                    hasKilled = false;
                }
    
                if (pieces[x2, y2].hasToKill != null)
                {
                    hasToKill = true;
                    x = x2;
                    y = y2;
                    ResetMove(x2, y2);
                    return;
                }
                EndTurn();
            }
            else
            {
                ResetMove(x1, y1);
            }
        }
    }

    private void ResetMove(int x, int y)
    {
        MovePiece(selectedPiece, x, y);
        startDrag = Vector2.zero;
        selectedPiece = null;
    }

    private void EndTurn()
    {
        selectedPiece = null;
        startDrag = Vector2.zero;
        isWhiteTurn = !isWhiteTurn;
        CheckVictory();
    }

    private void CheckVictory()
    {
        bool whitePresence = numWhite == 0;
        bool blackPresence = numBlack == 0;
        if (whitePresence && !blackPresence || !whitePresence && blackPresence)
        {
            DisplayVictory(whitePresence);
        }

    }

    private void DisplayVictory(bool whitePresence)
    {
        // TODO: display the victory of one side
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

    private void SelectPiece(int x, int y)
    {
        // Out of bounds
        if (x < 0 || x >= taillePlateau || y < 0 || y >= taillePlateau)
        {
            return;
        }
        Piece p = pieces[x, y];
        if (hasToKill && (x != this.x || y!= this.y))
        {
            return;
        }
        if (p != null && p.isWhite == isWhiteTurn)
        {
            selectedPiece = p;
            startDrag = mouseOver;
        }

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

    private void UpdatePieceDrag(Piece p)
    {
        if (!Camera.main)
        {
            Debug.Log("Unable to find main Camera");
            return;
        }

        if (Physics.Raycast(Camera.main.ScreenPointToRay(Input.mousePosition), out RaycastHit hit, 25.0f, LayerMask.GetMask("Board")))
        {
            p.transform.position = hit.point + Vector3.up;
        }
    }

    private void GeneratePiece(int x, int y, bool isWhite)
    {
        GameObject go = Instantiate(isWhite ? whitePiecePrefab : blackPiecePrefab) as GameObject;
        go.transform.SetParent(transform);
        Piece p = go.GetComponent<Piece>();
        pieces[x, y] = p;
        MovePiece(p, x, y);

    }

    private void MovePiece(Piece p, int x, int y)
    {
        p.transform.position = (Vector3.right * x) + (Vector3.forward * y) + boardOffset + pieceOffset;
    }
}
