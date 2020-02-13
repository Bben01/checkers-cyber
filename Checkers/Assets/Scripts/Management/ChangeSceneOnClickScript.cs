using UnityEngine;
using UnityEngine.SceneManagement;

public class ChangeSceneOnClickScript : MonoBehaviour
{
    public Animator animator;

    private int _nextScene;

    // Update is called once per frame
    public void Update()
    {
        if (Input.GetMouseButtonDown(0) || (Input.touches != null && Input.touches.Length > 0))
        {
            FadeToNextLevel();
        }
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
