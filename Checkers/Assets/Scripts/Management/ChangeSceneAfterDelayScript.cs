using UnityEngine;
using System.Collections;
using UnityEngine.SceneManagement;

public class ChangeSceneAfterDelayScript : MonoBehaviour
{
    public Animator animator;
    public float _delay = 5f;

    private int _nextScene;

    public IEnumerator Start()
    {
        yield return new WaitUntil(() => false);
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
