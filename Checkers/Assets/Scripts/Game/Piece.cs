using UnityEngine;

public class Piece : MonoBehaviour
{
    public Animator animator;
    public ParticleSystem plasmaExplosion;

    public bool IsKing { get; set; }
    public bool IsWhite { get; set; }

    public bool DestroyOnCollision { get; set; }

    public Piece(bool white)
    {
        IsWhite = white;
        IsKing = false;
        DestroyOnCollision = false;
    }

    public Piece(Piece p)
    {
        IsWhite = p.IsWhite;
        IsKing = p.IsKing;
        DestroyOnCollision = false;
    }

    public void ActivateAnimation()
    {
        animator.SetTrigger("AnimateKing");
    }

    private void OnTriggerEnter(Collider collider)
    {
        Debug.Log("New Collision");
        if (DestroyOnCollision && collider.gameObject.GetType() == gameObject.GetType())
        {
            var explosion = Instantiate(plasmaExplosion, gameObject.transform.position, Quaternion.identity);
            Destroy(gameObject);
        }
    }
}