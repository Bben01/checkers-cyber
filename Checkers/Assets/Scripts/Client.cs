using System;
using System.Net.Sockets;
using System.Text;

public class Client
{
    private static readonly string ip = "127.0.0.1";
    private static readonly int port = 10001;
    private static bool openClient = false;
    private static TcpClient client;
    private static NetworkStream stream;

    public static string[][] infoAI = null;


    public static string FormatMessageNoArgs(string methodName)
    {
        string str = $"1{methodName.PadRight(64),'-'}0";
        return str.Length.ToString().PadLeft(4, '0') + str;
    }

    public static string FormatMessageArgs(string methodName, string[] args)
    {
        string str = $"1{methodName.PadRight(64),' '}{args.Length}{PrintArray(args)}";
        return str.Length.ToString().PadLeft(4, '0') + str;
    }

    private static string PrintArray(string[] list)
    {
        string returnString = "";
        foreach (string str in list)
        {
            if (returnString.Length != 0)
            {
                returnString += "##-+-##";
            }
            returnString += str;
        }
        return returnString;
    }

    private static void Start()
    {
        // Create a TcpClient.
        // Note, for this client to work you need to have a TcpServer 
        // connected to the same address as specified by the server, port
        // combination.
        client = new TcpClient(ip, port);

        // Get a client stream for reading and writing.
        //  Stream stream = client.GetStream();
        stream = client.GetStream();

        openClient = true;
    }

    public static string[] FormatSendAndResponse(string methodName, string[] args = null)
    {
        string format = args != null ? FormatMessageArgs(methodName, args) : FormatMessageNoArgs(methodName);
        return Send(format, true);
    }

    public static string SendAndResponseWithoutFormat(string methodName, string[] args = null)
    {
        string format = args != null ? FormatMessageArgs(methodName, args) : FormatMessageNoArgs(methodName);
        return Send(format, false)[0];
    }

    public static string[][] IAPlay()
    {
        string format = FormatMessageNoArgs("ia_play");
        string[] moves = Send(format, false, true);
        string[][] tabOfMoves = new string[moves.Length][];
        for (int i = 0; i < moves.Length; i++)
        {
            tabOfMoves[i] = moves[i].Split('-');
        }
        return tabOfMoves;
    }

    private static void End()
    {
        // Close everything.
        stream.Close();
        client.Close();
        openClient = false;
    }

    public static string[] Send(string message, bool getArgs, bool iaPlay=false)
    {
        try
        {
            if (!openClient)
            {
                Start();
            }
            // Translate the passed message into ASCII and store it as a Byte array.
            byte[] data = Encoding.ASCII.GetBytes(message);


            // Send the message to the connected TcpServer. 
            stream.Write(data, 0, data.Length);

            // Receive the TcpServer.response.
            byte[] len = new byte[4];
            stream.Read(len, 0, 4);
            int.TryParse(Encoding.ASCII.GetString(len), out int trueLen);

            // Buffer to store the response bytes.
            data = new byte[trueLen];

            // Read the first batch of the TcpServer response bytes.
            stream.Read(data, 0, trueLen);
            if (iaPlay)
            {
                return GetIAPlaysFromByteArray(data);
            }
            return getArgs ? GetArgsFromByteArray(data) : GetFromByteArray(data);
        }
        catch (ArgumentNullException e)
        {
            Console.WriteLine("ArgumentNullException: {0}", e);
        }
        catch (SocketException e)
        {
            Console.WriteLine("SocketException: {0}", e);
        }
        openClient = false;
        return null;
    }

    // Returns null if the message does not match the pattern -> <nbOfArgs>arg1-arg2-...
    private static string[] GetArgsFromByteArray(byte[] encodedMessage)
    {
        int.TryParse(Encoding.ASCII.GetString(new byte[] { encodedMessage[0] }), out int numberOfArgs);
        string[] args = Encoding.ASCII.GetString(encodedMessage).Substring(1).Split('-');
        return args.Length == numberOfArgs ? args : null;
    }

    private static string[] GetFromByteArray(byte[] encodedMessage)
    {
        return new string[] { Encoding.ASCII.GetString(encodedMessage) };
    }

    private static string[] GetIAPlaysFromByteArray(byte[] encodedMessage)
    {
        int.TryParse(Encoding.ASCII.GetString(new byte[] { encodedMessage[0] }), out int numberOfSupArgs);
        string[] args = Encoding.ASCII.GetString(encodedMessage).Substring(1).Split(new string[] { "//-//" }, StringSplitOptions.None);
        return args.Length == numberOfSupArgs ? args : null;
    }
}
