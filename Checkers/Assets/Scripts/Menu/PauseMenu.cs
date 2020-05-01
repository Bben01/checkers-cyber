using UnityEngine;
using UnityEngine.SceneManagement;

public class PauseMenu : MonoBehaviour
{
    public static bool GameIsPaused = false;

    public GameObject PauseMenuUI;
    public GameObject chess;

    public string pauseKeyCode1;
    public KeyCode pauseKeyCode2 = KeyCode.Escape;

    private void Awake()
    {
        pauseKeyCode1 = PlayerPrefs.GetString("PauseKey", "space");
    }

    // Update is called once per frame
    void Update()
    {
        if (Input.GetKeyDown(pauseKeyCode1) || Input.GetKeyDown(pauseKeyCode2))
        {
            if (GameIsPaused)
            {
                Resume();
                Graphiques sn = chess.gameObject.GetComponent<Graphiques>();
                sn.Resume();
            }
            else
            {
                Pause();
            }
        }
    }

    public void Pause()
    {
        PauseMenuUI.SetActive(true);
        Time.timeScale = 0f;
        GameIsPaused = true;
    }

    public void Resume()
    {
        PauseMenuUI.SetActive(false);
        Time.timeScale = 1f;
        GameIsPaused = false;
    }

    public void LoadMenu()
    {
        // Client.End();
        Time.timeScale = 1f;
        SceneManager.LoadScene("MenuScene");
    }

    public void QuitGame()
    {
        Debug.Log("Quitting");
        Application.Quit();
    }
}
