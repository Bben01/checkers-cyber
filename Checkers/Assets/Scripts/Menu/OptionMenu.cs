using UnityEngine;
using TMPro;
using UnityEngine.UI;

public class OptionMenu : MonoBehaviour
{
    private string[] values;
    private bool IsKeyRequired = false;
    public GameObject PauseButton;
    public GameObject KeyBinding;
    public GameObject TextGameObject;
    public TMP_Text text;
    public Slider Slider;

    private void Awake()
    {
        values = KeyCodes.keys;
        UpdateText();
        LoadVolume();
    }

    private void Update()
    {
        if (IsKeyRequired && Input.anyKeyDown)
        {
            foreach (string key in values)
            {
                if (Input.GetKeyDown(key))
                {
                    IsKeyRequired = false;
                    PlayerPrefs.SetString("PauseKey", key);
                    KeyBinding.SetActive(false);
                    PauseButton.SetActive(true);
                    TextGameObject.SetActive(true);
                    UpdateText();
                    return;
                }
            }
        }
    }

    public void RequireKey()
    {
        IsKeyRequired = true;
    }

    private void UpdateText()
    {
        text.text = PlayerPrefs.GetString("PauseKey", "Space").ToUpper();
    }

    public void UpdateVolume()
    {
        float volume = Slider.value;
        PlayerPrefs.SetFloat("Volume", volume);
        FindObjectOfType<AudioManager>().SetVolume(volume);
    }

    private void LoadVolume()
    {
        float volume = PlayerPrefs.GetFloat("Volume", 0.5f);
        Slider.value = volume;
    }
}
