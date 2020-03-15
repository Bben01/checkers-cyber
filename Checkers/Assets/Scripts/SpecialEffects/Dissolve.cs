using System.Collections;
using UnityEngine;

public class Dissolve : MonoBehaviour
{
    public Material material;
    public Piece piece;

    private bool first;

    void Start()
    {
        material.SetFloat("Vector1_FEFF47F1", 0);
        first = true;
    }

    void Update()
    {
        if (first && Input.GetMouseButtonDown(0))
        {
            StartCoroutine("DissolveShader");
            first = false;
        }
    }

    private IEnumerator DissolveShader()
    {
        float dissolve = 0;
        while (dissolve < 0.8)
        {
            dissolve += 0.01f;
            material.SetFloat("Vector1_FEFF47F1", dissolve);
            yield return null;
        }
        Destroy(piece.gameObject);
    }
}
