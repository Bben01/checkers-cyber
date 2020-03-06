using UnityEngine;
using UnityEngine.SceneManagement;

public class ChangeSceneOnClickScript : MonoBehaviour
{
    public Animator animator;
    public int delay = 60 * 5;
    public bool acceptTouch = true;
    public bool acceptDelay = true;

    private int _nextScene;

    // Update is called once per frame
    public void Update()
    {
        if (acceptTouch && (Input.GetMouseButtonDown(0) || (Input.touches != null && Input.touches.Length > 0) || (delay == 0 && acceptDelay)))
        {
            FadeToNextLevel();
        }
        delay--;
    }

    public void FadeToNextLevel()
    {
        FadeToLevel(SceneManager.GetActiveScene().buildIndex + 1);
    }

    public void FadeToLevel(int levelIndex)
    {
        _nextScene = levelIndex;
        animator.SetTrigger("NextScene");
    }

    public void OnFadeComplete()
    {
        SceneManager.LoadScene(_nextScene);
    }
}
