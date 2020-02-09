using UnityEngine;

public class SceneChanger : MonoBehaviour
{
    public Animator animator;

    // Update is called once per frame
    void Update()
    {
        if (Input.GetMouseButtonDown(0))
        {
            FadeToLevel(1);
            Debug.Log("OK");
        }
    }

    public void FadeToLevel(int levelIndex)
    {
        animator.SetTrigger("NextScene");
    }
}
