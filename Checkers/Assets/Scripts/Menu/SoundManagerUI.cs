using UnityEngine;

public class SoundManagerUI : MonoBehaviour
{
    public void PlayOnClick()
    {
        FindObjectOfType<AudioManager>().Play("ButtonClick");
    }

    public void PlayOnHover()
    {
        FindObjectOfType<AudioManager>().Play("ButtonHover");
    }
}
