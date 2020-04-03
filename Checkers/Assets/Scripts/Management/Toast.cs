using System.Collections;
using UnityEngine;
using TMPro;

public class Toast : MonoBehaviour
{
    public TMP_Text Text;

    public IEnumerator ShowToast(string message, float duration)
    {
        Text.enabled = true;

        Text.text = message;

        yield return Fade(true);

        yield return new WaitForSeconds(duration);

        yield return Fade(false);

        Text.enabled = false;
    }

    IEnumerator Fade(bool fadeIn)
    {
        float start = fadeIn ? 0f: 1f;
        float end = fadeIn ? 1f : 0f;

        float counter = 0f;
        float duration = .25f;

        while (counter < duration)
        {
            counter += Time.deltaTime;
            float alpha = Mathf.Lerp(start, end, counter / duration);

            Text.color = new Color(Text.color.r, Text.color.g, Text.color.b, alpha);
            yield return null;
        }
    }
}
