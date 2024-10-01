### LIBRERIAS ###
import math


### CONSTANTES ###

PRIMOS = None


### CLASES ###
class ErrorNE():

    def __str__(self) -> str:
        return 'NE'

class Primos():
    def __init__(self):
        self.primos = [2,3]
        self.l = 2
    
    def __p__(self,n: int):
        """
        Actualiza la lista de primos hasta n
        """
        for m in range(PRIMOS.primos[-1]+2, n+1, 2):
            cota = math.sqrt(m)
            itis = True
            i = 0
            while itis and (PRIMOS.primos[i] <= cota):
                if m % PRIMOS.primos[i] == 0: itis = False
                i += 1
            if itis:
                PRIMOS.primos.append(m)  
                PRIMOS.l += 1

### FUNCIONES ###
def es_primo(n : int) -> str:
    if n < 0: return 'No'
    PRIMOS.__p__(round(math.sqrt(n)))
    if n > 3:
        for p in PRIMOS.primos:
            if n % p == 0: return 'No'
    
    return 'Sí'

def lista_primos(a: int, b: int, izq=0) -> list:
    if b <= a: return ErrorNE()
    PRIMOS.__p__(b)
    while PRIMOS.primos[izq] < a: izq += 1
    der = izq
    while der < PRIMOS.l and PRIMOS.primos[der] < b:
        der += 1
    return PRIMOS.primos[izq:der]
    ...

def factorizar(n: int, i=0, p=0) -> dict:
    r={}
    c = round(math.sqrt(n))
    PRIMOS.__p__(c)
    while (i < PRIMOS.l) and p < c:
        count = 0
        p = PRIMOS.primos[i]
        while n % p == 0:
            count += 1
            n /= p
        if count: r[p] = count
        i += 1
    if n > 1: r[int(n)] = 1
    return r

def bezout(a: int , b: int):
    lista = [1,0]
    listb = [0,1]
    listaux0, listaux1 = 0,0
    while b > 0:
        listaux0,listaux1 = listb[0],listb[1]
        listb[0] , listb[1] = lista[0]-(a//b)*listb[0] , lista[1]-(a//b)*listb[1]
        lista[0],lista[1] = listaux0,listaux1
        a,b = b, a % b
    return (a,listaux0,listaux1)

def mcd(a: int,b: int) -> int:
    #Algoritmo de Euclides tradicional
    return mcd(b,a%b) if b != 0 else a

def coprimos(a : int, b : int) -> bool:
    return 'Si' if mcd(a,b) == 1 else 'No'

def potencia_mod_p(b : int, e : int, p : int, r=1) -> int:
    
    if e < 0:
        d = p
        lista = [1,0]
        listb = [0,1]
        listaux0, listaux1 = 0,0
        while d > 0:
            listaux0,listaux1 = listb[0],listb[1]
            listb[0] , listb[1] = lista[0]-(b//d)*listb[0] , lista[1]-(b//d)*listb[1]
            lista[0],lista[1] = listaux0,listaux1
            b, d = d, (b % d)
        b = listaux0
        e = -e

    b %= p
    
    while (e > 0):
 
        if ((e & 1) != 0):
            r = (r * b) % p
        e = e >> 1 
        b = (b * b) % p  


    return r

def inversa_mod_p(n : int, p : int) -> int:
    sol = bezout(n,p)[1]
    if sol < 0: sol %= p
    if sol == 0 and n != 0: return ErrorNE()
    return sol

def euler(n: int, solucion=1, i=0, p=0):
    c = round(math.sqrt(n))
    PRIMOS.__p__(c)
    while (i < PRIMOS.l) and p < c:
        count = 0
        p = PRIMOS.primos[i]
        while n % p == 0:
            count += 1
            n /= p
        if count: solucion *= (int(p-1))*(p**(count-1))
        i += 1
    if n > 1: solucion *= int(n-1)
    return solucion
    
def legendre(n: int, p: int):
    return potencia_mod_p(n,(p-1)//2,p)

def resolver_sistema_congruencias(a: list, b: list[int], p: list[int]):
    # comprovar si son coprimos
    try:
        for i in p:
            for j in p:
                if i != j and coprimos(i,j) == 'No': return ErrorNE()

        m, l, s = 1, 0, 0
        for k in p:
            l += 1
            m *= k
        for i in range(l):
            c = (inversa_mod_p(a[i],k)*b[i])
            n = m/p[i]
            s += c*inversa_mod_p(n,p[i])*n

        return int(s%m)
    except Exception: return ErrorNE()

def raiz(n: int, p: int):
    n = n % p
    if legendre(n, p) == 1:
        return ErrorNE()
    q = p - 1
    s = 0
    while q % 2 == 0:
        q //= 2
        s += 1
    if s == 1:
        return potencia_mod_p(n,(p+1)//4,p)
    for z in range(2, p):
        if p - 1 == legendre(z, p):
            break
    c = potencia_mod_p(z,int(q),p)
    t = potencia_mod_p(n,int(q),p)
    r = potencia_mod_p(n,int((q+1)/2),p)
    m = s
    t2 = 0
    while (t-1)%p != 0:
        t2= (t*t)%p
        for i in range(1, m):
            if (t2 - 1) % p == 0:
                break
            t2 = (t2 * t2) % p
        try:
            b = potencia_mod_p(c, 1 << (m - i - 1), p)
        except:
            return ErrorNE()
        r = (r * b) % p
        c = (b * b) % p
        t = (t * c) % p
        m = i
    return r,-r%p

def ecuacion_cuadratica( a: int, b: int, c: int, p: int):
    if (((b**2)-4*a*c)%4*a**2) != 0:
        try:
            solucion = (raiz((b**2)-(4*a*c),p))[0]/(raiz(4*a,p)[0])
            solucion2 = (raiz((b**2)-(4*a*c),p))[1]/(raiz(4*a,p)[1])
            solucion -= b/(2*a)
            solucion2 -= b/(2*a)
            return  str(solucion)+','+str(solucion2)
        except:
            return ErrorNE()

    a = a%p
    b = b%p
    c = c%p
    m = b/a
    n = c/a

    try:
        solucion = raiz(((m**2)/4)-n,p)[0]
        solucion2 = raiz(((m**2)/4)-n,p)[1]
        solucion -= b/(2*a)
        solucion2 -= b/(2*a)
        return str(solucion)+','+str(solucion2)
    except:
        return ErrorNE()

PRIMOS = Primos() if not PRIMOS else PRIMOS