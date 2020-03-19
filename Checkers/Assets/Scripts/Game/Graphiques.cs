using System;
using UnityEngine;
using System.Threading;

public class Graphiques : MonoBehaviour
{
    public static readonly int taillePlateau = 8;
    public Piece[,] board = new Piece[taillePlateau, taillePlateau];

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

    private bool isWhiteTurn;

    private bool isVictory;

    private string[][] interThread = null;

    private bool isIAing = false;

    // Start is called before the first frame update
    void Start()
    {
        enabled = true;
        GenerateBoard();
        clicked = false;
        isWhiteTurn = true;
        isVictory = false;
    }

    // Update is called once per frame
    void Update()
    {
        if (PauseMenu.GameIsPaused)
        {
            enabled = false;
        }

        if (isVictory)
        {
            // TODO: Appeler la prochaine scene ici
            return;
        }

        UpdateMouseOver();

        if (isWhiteTurn)
        {
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
                string[] returnInfos = Client.FormatSendAndResponse("try_move_piece", new string[5] { $"{startClick.x}", $"{startClick.y}", $"{x}", $"{y}", $"{hasToPlayAgain}" });
                AnalizeInfo(returnInfos);
            }
        }
        else
        {
            if (!isIAing)
            {
                isIAing = true;
                ThreadStart childref = new ThreadStart(IACom);

                Thread childThread = new Thread(childref);
                childThread.Start();
            }
            else
            {
                if (interThread != null)
                {
                    IAPlay(interThread);
                    interThread = null;
                    isIAing = false;
                }
            }
        }
    }

    void OnApplicationQuit() => Client.CloseClient();

    public void Resume()
    {
        enabled = true;
    }

    private void IACom()
    {
        interThread = Client.IAPlay();
    }

    private void IAPlay(string[][] infos)
    {
        bool firstTime = true;
        foreach (string[] info in infos)
        {
            AnalizeInfo(info, true, firstTime);
            firstTime = false;
        }
        Reset();
    }

    private void AnalizeInfo(string[] returnInfos, bool iaPlay = false, bool firstTime = false)
    {
        // Error
        // TODO: There is an error here when the last piece is eaten
        if (Helper.Activate(returnInfos[0], 0))
        {
            AfficherError(returnInfos[1].Substring(1));
            if (Helper.Activate(returnInfos[1], 0))
            {
                Reset();
            }
            return;
        }
        // Just move visually the piece
        Vector2Int lastDeplacement = Helper.GetLastDeplacementDest(returnInfos[4]);
        if (iaPlay)
        {
            int x = (int)char.GetNumericValue(returnInfos[6], 1);
            int y = (int)char.GetNumericValue(returnInfos[6], 2);
            if (firstTime)
            {
                startClick = new Vector2Int(x, y);
            }
            selectedPiece = board[x, y];
        }

        MovePieceVisual(selectedPiece, lastDeplacement.x, lastDeplacement.y);
        // Killed
        if (Helper.Activate(returnInfos[2], 0))
        {
            Vector2Int posKilled = Helper.GetPosKilled(returnInfos[2]);
            Debug.Log($"Piece Killed: { posKilled }");
            Piece p = board[posKilled.x, posKilled.y];
            board[posKilled.x, posKilled.y] = null;
            Destroy(p.gameObject);
            // Has to play again
            if (Helper.Activate(returnInfos[2], 3))
            {
                hasToPlayAgain = true;
                posPieceToPlay = posKilled;
                MovePieceBoard(new Deplacement(startClick.x, startClick.y, lastDeplacement.x, lastDeplacement.y));
                startClick = lastDeplacement;
            }
            else
            {
                MovePieceBoard(new Deplacement(startClick.x, startClick.y, lastDeplacement.x, lastDeplacement.y));
            }
        }
        else
        {
            MovePieceBoard(new Deplacement(startClick.x, startClick.y, lastDeplacement.x, lastDeplacement.y));
        }

        // New Queen
        if (Helper.Activate(returnInfos[1], 0))
        {
            AnimateQueen(Helper.GetPosNewQueen(returnInfos[1]));
        }
        // Ended turn
        if (Helper.Activate(returnInfos[3], 0))
        {
            EndTurn();
        }
        // Victory
        if (Helper.Activate(returnInfos[5], 0))
        {
            Debug.Log(returnInfos[5].Substring(1));
            isVictory = true;
        }
    }

    private void MovePieceBoard(Deplacement lastDeplacement)
    {
        board[lastDeplacement.Destination.x, lastDeplacement.Destination.y] = board[lastDeplacement.Origin.x, lastDeplacement.Origin.y];
        board[lastDeplacement.Origin.x, lastDeplacement.Origin.y] = null;
        Vector2Int eaten = lastDeplacement.EatenPiece();
        if (eaten != Vector2Int.zero)
        {
            board[eaten.x, eaten.y] = null;
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
        isWhiteTurn = PlayAgain() ? !isWhiteTurn : isWhiteTurn;
        startClick = Vector2Int.zero;
    }

    private bool PlayAgain()
    {
        bool hasSomethingToPlay = Client.SendAndResponseWithoutFormat("has_something_to_play", new string[2] { $"{!isWhiteTurn}", "false" }).ToLower().Equals("true");
        if (!hasSomethingToPlay)
        {
            string color = isWhiteTurn ? "White" : "Black";
            AfficherError($"{color} plays again!");
        }
        return hasSomethingToPlay;
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
        Client.SendAndResponseWithoutFormat("generate_board_submethod", new string[3] { $"{x}", $"{y}", $"{isWhite}" });
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
        if (Helper.IsTrue(Client.SendAndResponseWithoutFormat("can_eat")))
        {
            hasSomethingToEat = true;

            // Can't move the piece if this is not one of the selectable
            if (!Helper.IsTrue(Client.SendAndResponseWithoutFormat("selectable", new string[2] { $"{x}", $"{y}" })))
            {
                AfficherError("Another piece is forced to be played!");
                return;
            }
        }
        // Good selection
        if (p != null && p.IsWhite == Helper.IsTrue(Client.SendAndResponseWithoutFormat("is_white_turn")) && Helper.IsTrue(Client.SendAndResponseWithoutFormat("selectable", new string[3] { $"{x}", $"{y}", $"{Helper.GetBools(!hasSomethingToEat)}" })))
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
        if (pos == null)
        {
            Debug.Log("Error with new Queen.");
            return;
        }
        Debug.Log("New Queen!");
        Piece p = board[pos.Item1, pos.Item2];
        p.IsKing = true;
        p.ActivateAnimation();
    }

    public static void AfficherError(string errorMessage)
    {
        // TODO: a implementer
        // Just for now:
        Debug.Log(errorMessage);
    }
}
