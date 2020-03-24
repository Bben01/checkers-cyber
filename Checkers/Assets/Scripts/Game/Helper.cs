using System;
using UnityEngine;

public class Helper
{
    public static string arrayToStr(string[] array)
    {
        string returnStr = "";
        foreach (string str in array)
        {
            returnStr += str;
        }
        return returnStr;
    }

    public static Tuple<int, int> GetPosNewQueen(string infos)
    {
        if (int.TryParse(infos.Substring(1, 1), out int x) && int.TryParse(infos.Substring(2, 1), out int y))
        {
            return new Tuple<int, int>(x, y);
        }
        return null;
    }

    public static Vector2Int GetPosKilled(string infos)
    {
        if (int.TryParse(infos.Substring(1, 1), out int x) && int.TryParse(infos.Substring(2, 1), out int y))
        {
            return new Vector2Int(x, y);
        }
        return Vector2Int.zero;
    }

    public static Vector2Int GetLastDeplacementDest(string infos)
    {
        if (int.TryParse(infos.Substring(1, 1), out int x) && int.TryParse(infos.Substring(2, 1), out int y))
        {
            return new Vector2Int(x, y);
        }
        return Vector2Int.zero;
    }

    public static bool HasToPlayAgain(string infos)
    {
        try
        {
            return infos.Substring(1, 1).Equals("1");
        }
        catch (Exception)
        {
            return false;
        }
    }

    public static bool Activate(string info, int position)
    {
        if (!int.TryParse(info.Substring(position, 1), out int code))
        {
            return false;
        }
        return code == 1;
    }

    public static bool IsTrue(string msg)
    {
        try
        {
            return msg.ToLower().Equals("true");
        }
        catch (Exception)
        {
            return false;
        }
    }

    public static string GetBools(bool b)
    {
        return b ? "True" : "False";
    }
}
