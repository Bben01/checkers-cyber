using UnityEngine;
using TMPro;

public class OptionMenu : MonoBehaviour
{
    private string[] values;
    private bool IsKeyRequired = false;
    public GameObject PauseButton;
    public GameObject KeyBinding;
    public GameObject TextGameObject;
    public TMP_Text text;

    private void Awake()
    {
        values = KeyCodes.keys;
        UpdateText();
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
}
