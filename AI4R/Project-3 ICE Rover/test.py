import matrix 

nBeacons = 3
meas= [[[0,1,2],[1,2,3],[2,3,4]],[[0,1.1,2.2],[1,2.2,3.1],[2,3.3,4.2]],[[0,1.2,2.1],[1,2.1,3.2],[2,3.1,4.2]]]
dim = 2*(1+nBeacons)

Omega = matrix.matrix()
Xi = matrix.matrix()

Omega.zero(dim,dim)
Xi.zero(dim,dim)

Omega.zero(dim, dim)
Omega.value[0][0] = 1.0
Omega.value[1][1] = 1.0   

            
Xi.zero(dim,1)
Xi.value[0][0] = 0
Xi.value[1][0] = 0

for measurements in meas:
    for measurement in measurements:
    
        m = 2 * ( 1 + measurement[0])
                    
        for b in range(2):
            Omega.value[b  ][b  ] += 1.0 
            Omega.value[m+b][m+b] += 1.0 
            Omega.value[m+b][b  ] += -1.0 
            Omega.value[b  ][m+b] += -1.0 
            
            Xi.value[b  ][0] += -measurement[1+b] 
            Xi.value[m+b][0] += measurement[1+b] 
        
mu = Omega.inverse() * Xi
    
x = mu[0][0]
y = mu[1][0]

print("x:",x)
print("y",y)
