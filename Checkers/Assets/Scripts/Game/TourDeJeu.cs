using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TourDeJeu
{
    private List<Deplacement> deplacements = new List<Deplacement>();
    private int CodeError { get; set; }
    public bool Success { get; set; }

    public TourDeJeu()
    {
        CodeError = -1;
        Success = false;
    }

    public bool AddDeplacement(Deplacement d)
    {
        deplacements.Add(d);
        Success = true;
        return true;
    }

    public void SetCodeError(int code)
    {
        CodeError = code;
    }
}
