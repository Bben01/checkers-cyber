using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Graphiques : MonoBehaviour
{
    public static readonly int taillePlateau = 8;

    public GameObject whitePiecePrefab;
    public GameObject blackPiecePrefab;

    private Vector3 boardOffset = new Vector3(-4.0f, 0, -4.0f);
    private Vector3 pieceOffset = new Vector3(0.5f, 0.1f, 0.5f);

    private Piece selectedPiece;

    private Vector2 mouseOver;
    private Vector2 startClick;

    private bool clicked;


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
        }
        if (Input.GetMouseButtonDown(0) && clicked)
        {
            Plateau.TryMove(new Deplacement((int)startClick.x, (int)startClick.y, x, y));
            clicked = false;
        }
    }

    private void UpdatePieceOver(Piece p)
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
        // TODO: a adapter pour la nouvelle version
        GameObject go = Instantiate(isWhite ? whitePiecePrefab : blackPiecePrefab) as GameObject;
        go.transform.SetParent(transform);
        Piece p = go.GetComponent<Piece>();
        Plateau.pieces[x, y] = p;
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
        Piece p = Plateau.pieces[x, y];
        // Can't move the piece if this is not one of the selectable
        if (ValidMoveMethods.HasSomethingToEat(Plateau.pieces, Plateau.isWhiteTurn) && ValidMoveMethods.KillerPlayAgain(Plateau.pieces, x, y) == null)
        {
            return;
        }
        if (p != null && p.isWhite == Plateau.isWhiteTurn)
        {
            selectedPiece = p;
            clicked = true;
        }

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

    public static void EndTurn()
    {
        // TODO: a implementer
    }

    public static void Reset()
    {
        // TODO: a implementer
    }

    public static void AnimateQueen()
    {
        // TODO: a implementer
    }

    public static void AfficherError(string errorMessage)
    {
        // TODO: a implementer
    }
}
