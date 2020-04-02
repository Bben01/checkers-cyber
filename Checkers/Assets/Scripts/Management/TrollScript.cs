using UnityEngine;

public class TrollScript : MonoBehaviour
{
    // Pour Sam :-)
    private string Password = "piou";
    public bool isTroll = false;

    // Update is called once per frame
    void Update()
    {
        if (Input.GetKeyDown(Password[0].ToString()))
        {
            Debug.Log(Password[0] + " has been pressed!");
            Password = Password.Substring(1);
            if (Password.Equals(""))
            {
                isTroll = true;
                enabled = false;
            }
        }
    }
}
