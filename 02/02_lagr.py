def lagr(k,x,values):
    nom = 1
    denom = 1
    for i in range(1,values):
        if not i==k:
            nom *= (x-values[i][0])
            denom *= (values[k][0]-values[i][0])
    return nom/denom
    
    
def polX(x,values):
    prod = 1
    for i in range(1,values.size()):
        prod *= values[i][1]*lagr(i,x,values)
    return prod
