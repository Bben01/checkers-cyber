using System.Net;
using System.Text;
using System;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

public class RESTClient
{
    private static WebClient wb = new WebClient();

    private struct RequestJSON
    {
        public bool is_white_turn { get; set; }
        public bool has_to_play_again { get; set; }
        public string board { get; set; }
        public string method { get; set; }
        public string[] args { get; set; }

        public override string ToString()
        {
            return JsonConvert.SerializeObject(this);
        }
    }

    public static string PostAndResponse(string method, string[] args, Piece[,] board, bool is_white_turn, bool has_to_play_again)
    {
        RequestJSON request = new RequestJSON() { is_white_turn=is_white_turn, has_to_play_again=has_to_play_again, board=BoardToString(board), method=method, args=args};
        wb.Headers.Add("Content-Type", "application/json");
        return RESTResponse(wb.UploadString("http://localhost:5000/", "POST", request.ToString()));
    }

    private static string BoardToString(Piece[,] board)
    {
        // Serializes the board to a string.
        StringBuilder sb = new StringBuilder((int) Math.Pow(board.Length, 2));
        for (int i = 0; i < board.GetLength(0); i++)
        {
            for (int j = 0; j < board.GetLength(0); j++)
            {
                Piece p = board[i, j];
                sb.Append(p == null ? "E" : p.ToString());
            }
        }
        return sb.ToString();
    }

    public static string RESTResponse(string json_file)
    {
        var response = JObject.Parse(json_file);
        return response["response"].ToString();
    }

    // Returns null if the message does not match the pattern -> <nbOfArgs>arg1-arg2-...
    private static string[] GetArgsFromResponse(string message)
    {
        int.TryParse("" + message[0], out int numberOfArgs);
        string[] args = message.Substring(1).Split('-');
        return args.Length == numberOfArgs ? args : null;
    }

    private static string[] GetIAPlaysFromResponse(string message)
    {
        int.TryParse("" + message[0], out int numberOfSupArgs);
        string[] args = message.Substring(1).Split(new string[] { "//-//" }, StringSplitOptions.None);
        return args.Length == numberOfSupArgs ? args : null;
    }

    public static string[] FormatSendAndResponse(string method, string[] args, Piece[,] board, bool is_white_turn, bool has_to_play_again)
    {
        return GetArgsFromResponse(PostAndResponse(method, args, board, is_white_turn, has_to_play_again));
    }

    public static string[][] IAPlay(Piece[,] board, bool is_white_turn, bool has_to_play_again)
    {
        string[] moves = GetIAPlaysFromResponse(PostAndResponse("ia_play", new string[] { }, board, is_white_turn, has_to_play_again));
        if (moves == null)
        {
            return new string[100][];
        }
        string[][] tabOfMoves = new string[moves.Length][];
        for (int i = 0; i < moves.Length; i++)
        {
            tabOfMoves[i] = moves[i].Split('-');
        }
        return tabOfMoves;
    }

    public static void HiServer()
    {
        // Prepare the server connection
        wb.DownloadData("http://localhost:5000");
    }
}
