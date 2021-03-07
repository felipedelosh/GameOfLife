"""
Test Juego de la Vida
"""
matrix = []

for i in range(0, 50):
    matrix.append(i)

def verPuntero(puntero):
    lm = len(matrix)
    puntos = (puntero-1)%lm, (puntero)%lm, (puntero+1)%lm
    print(puntos)

print(matrix)
print("//")
verPuntero(49)