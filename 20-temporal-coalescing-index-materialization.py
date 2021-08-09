# A time machine for text search
# K Berberich, S Bedathur, T Neumann, G Weikum - Proceedings of the 30th annual international ACM …, 2007

"""
Sublist Materialization

Amac: 

Bir time-query (qt) icin diskte bulunan ilgili posting listin tamamini okumak fazladan I/O demektir. 
Onun yerine sadece posting list'te bulunan ve sadece qt yi kapsayan butun postinglerin olusturdugu bir alt kume diskten okunsa yeterlidir.
Boylece queryler daha hizli islenebilir.

Boylece belirli ardisik (ve ayrik) zaman kesitleri belirleyip bu kesitlerin her biri icin, bu zaman diliminde gecen butun postinglerden olusan
alt kumeleri diskte tutarsak daha az I/O yapmamiz yeterli olacak ve daha hizli query processing yapabilecegiz. 
Buna "Sublist Materialization" diyecegiz ve her bir zaman dilimini "Materialization Points" lerden olusturacagiz.

Ote yandan bir posting birden fazla alt kumenin icinde bulunabilecegi icin orijinal listeninkinden daha fazla disk alani kullanmamiz gerekmektedir.
Bu da time/space tradeoff anlamina gelmektedir.


Elementary time intervals tanimi:

Figure 6.1 uzerinden gosterecek olursak
[t1,t2),[t2,t3),[t3,4).. [t9,t10)

Yani posting listte mevcut butun zaman noktalarinin pes pese olusturdugu "atomic" zaman dilimleri.

Performance Optimal - Popt

Her bir elementary time interval icin ayri materialization yaparsak 
herhangi bir qt icin minimum sayida posting okumus oluruz; ancak bu da en fazla disk alani kaplayan materialization secimi anlamina gelmektedir

Space Optimal - Sopt

Orijinal posting listimiz halihazirda en az disk alani kaplayan materialization secimidir; ancak her elementary time interval icin butun posting list'i diskten okumamiz gerekeceginden query isleme hizi bu durumda en yavas olacaktir  


Algorithm 2 - Performance Guarantee

Bu optimizasyon probleminde her bir elementary time interval icin diskten okudugumuz "materialized sublist" boyutu, 
Popt'ta okuyacagimiz, karsilik gelen listenin boyutunun en fazla g kati kadar olabilir.
Baska bir deyisle, her bir elementary time interval icin, okuma hizimiz Popt'ta olacaginin maximum g kati kadar yavas olmalidir.
Bu kosulu saglayan minimum disk alani kaplayan materialization'u bulunuz.

Implementation

iki array var C[] ve B[]

C[i]: optimal cost of subproblem E1...i = yani en sag materialisation noktasi i olsa idi optimal cost'un kac olacagi bilgisini tutuyor.
Ornegin i = 5 ise, materialization noktalari  
{2,3,4}'un bir alt kumesi UNION {5} olmak zorunda

i = 7 ise, materialization noktalari   
{2,3,4,5,6}'nin bir alt kumesi UNION {7} olmak zorunda

B[i]: rightmost boundary for E1...1 = yani en sag materialisation noktasi i olursa, optimal cost'u veren materialization noktalari arasindan i' nin hemen solundaki nokta.

Ornegin i = 5 ise, ve optimal materialization noktalari
{3,5} ise B[5] = 3

i = 5 ise, ve optimal materialization noktalari
{2,3,5} ise B[5] = 3

i = 7 ise, ve optimal materialization noktalari
{2,3,4} ise B[7] = 4


Biz her k = 1..n icin

C[k] ve B[k] degerlerini bulmaya calisiyoruz:
k'nin hemen solunda olan nokta icin  j: k-1, k-2,...,1 'e kadar butun ihtimalleri deniyoruz. bu ihtimalleri tablodan O(1) surede fetch edebiliyoruz dynammic programming sayesinde.

Problemin constraint'ini saglamasi adina da her j icin condition(Lv:[tj,tk))'yi check ediyoruz. 
condition sunu soyluyor: [tj,tk) icinde bulunan her elementary time interval icin, Popt'taki materialized sublist buyukluklerinin toplaminin k kati, 
bu durumdaki (yani her biri icin tj,tk icinde bulunan postingleri okuma mecburiyeti) materialized sublist buyukluklerinin toplaminindan buyuk mu degil mi. 

Bu kosulu saglayan butun j ler icin, olusan zaman dilimlerinin costlarindan en kucugunu secip C[k]'ya bunu saglayan j degerini de B[k] ya yaziyoruz.

Isin guzel tarafi ise, bir j degeri icin condition bir kere fail ederse daha kucuk j ler icin kontrol etmemize gerek kalmamasi, cunku j azaldikca her zaman [tj,tk) costu artiyor.

Ornegin 

k = 8
biz k'nin en solundaki materialization noktasi nedir diye loop yaptik sirasiyla:
 j = 7     condition'a uydu: 
 j = 6     condition'a uydu.    
 j = 5     condition'a uymadi.       
 
minimum C[j] + |Lv:[tj,tk)| degerini saglayan j 6.
o halde  C[8] = C[6] + |Lv:[t6,t8)|

sonra k = 9 icin bakacagiz ve
  
j = 8
j = 7
j = 6
....
icin C[]'ye lookup yapip onceki buldugumuz orjinal degerlerden fadalanacagiz 

Input:
-Figure 6.1'deki posting list 
-gamma = 1.5

Output: 
C = [0 3 4 7 8 11 12 15 15 17]
B = [1 1 1 3 3 5   5 7  7  9 ]


Implementation:


Algorithm 3 - Space Bound

    Bu optimizasyon probleminde "materialized sublist"'lerin boyutlari toplami, 
    Sopt taki boyutun (=initial posting list size) en fazla k kati kadar olabilir. 
    Bu kosulu saglayan, minimum P_M'i veren Materialization'u bulunuz.

    Burada P_M expected processing cost anlamina gelmektedir, yani:

    her bir elementary time interval icin, 
    (bir query'in o zaman araliginda bulunma olasiligi) * (o query'in time intervalini iceren materialized sublist'in boyutu)

Implementation

    I_t: yeni materialization noktasi t eklenirse ne disk space'teki artis miktari.
    Ornegin Materialization points setine t6' yi eklersek
    [t4,t7)
    [t5,t8)
    postinglerini duplicate etmis olacagiz, yani artis miktari:2

    Ornegin Materialization points setine t9' u eklersek
    [t7,t10)
    postingini duplicate etmis olacagiz, yani artis miktari:1


    DP[0...n][0...cMax]: a matrix of possible materialisation sets. 
    DP[t][i] anlami: en sag noktadaki materialization noktasi t olursa ve bos disk space i olursa, en dusuk P_M'yi veren set nedir?

    Bunu da soyle hesapliyoruz:
    Figure 6.1'de t6'nin artisi 2 (I_t6 = 2) 
    eger bos alanimiz 1 tane ise t6'yi ekleyemeyiz o yuzden DP[6][1] = {}
    bos alanimiz 3 tane ise t6 yi ekleriz ve 
    DP[6][3] =   {6} UNION <1 space kaplayan en sag noktasi 6'dan kucuk olan optimum Materialization set> 

bir baska ornek:

    bos alanimiz 5 tane ise t6 yi ekleriz ve 
    DP[6][5] =   {6} UNION <2 space kaplayan en sag noktasi 6'dan kucuk olan optimum Materialization set> 


Input:
posting list of Figure 1.6
k = 1.6

Output:
DP matrixi:

[] [] [] []    []    []       []
[1][1][1][1]   [1]   [1]      [1]
[] [] [2][2]   [2]   [2]      [2]
[] [] [3][3]   [2, 3][2, 3]   [2, 3]
[] [] [4][4]   [2, 4][2, 4]   [2, 3, 4]
[] [] [5][5]   [3, 5][3, 5]   [2, 3, 5]
[] [] [6][6]   [3, 6][3, 6]   [2, 4, 6]
[] [] [7][7]   [4, 7][4, 7]   [3, 5, 7]
[] [] [8][8]   [4, 8][4, 8]   [3, 5, 8]
[] [9][9][5, 9][5, 9][3, 6, 9][3, 6, 9]


"""


# PG: Minimize Total Space = [each kapsayan chunkın posting sizeı].sum()
#     s.t. For each elementary; kapsayan chunk'ın posting sizeı elementarynin
#     posting sizeının 2 katından küçük
# SG: Minimize [for each elementary; kapsayan chunkın posting sizeı].sum()
#	  s.t. Total space tüm postinglerin sayısının 2 katından küçük

# 1 Performance Guarantee

def get_sublist_size(L, j, k):
    count = 0
    for posting in L:
        if posting[2] > j and posting[1] < k:
            count += 1
    return count 

def condition(L, coef, j, k):
    for i in range(j, k):
        if get_sublist_size(L, j, k) >= get_sublist_size(L, i, i+1) * coef:
            return False
    return True

def performance_guarantee(L, N, coef):
    
    C = [0] * N # C [ i ] :optimal cost for problem 0..i
    B = [0] * N # B [ i ] :rightmost boundary for problem 0..i

    for k in range(1, N):
        C[k] = float('inf')
        j = k-1
        while j>=0 and condition(L, coef, j, k):
            c = C[j] + get_sublist_size(L, j, k)
            if c < C[k]:
                C[k] = c
                B[k] = j
            j -= 1

    return C, B

def get_bounds(B, N):
    
    cur = N-1
    bounds = [N]
    
    while B[cur]>0:
        bounds.append(B[cur])
        cur = B[cur]
        
    bounds.append(0)
    bounds.reverse()
    
    return bounds


L = [ # Posting list
    ('d1', 0, 1), ('d2', 1, 2), ('d3', 2, 5), ('d4', 5, 7),
    ('d5', 0, 3), ('d6', 3, 6),('d7', 6, 9),
    ('d8', 0, 4), ('d9', 4, 8), ('d10', 8, 9)
]

j = 3
k = 5
print(get_sublist_size(L, j, k))
print(condition(L, 1.5, 3, 5))

N = 10 #number of timepoints if N=10 => 0...9
C, B = performance_guarantee(L, N, coef=5/3)
print(C)
print(B)

print('bounds', get_bounds(B, N))


# 2 Space Guarantee (Todo: handle zero indexing or one. also will end be like N-1 or N)
# 
# c[7][5]  -> c[5][4]
# c[7][4]  -> c[5][3]
# neden bunu es geçiyoz. es geçmiyoruz aslında. c[7][4] te ele alınıyor
# 
# c[5][3] yerine c[5][4] besttir diyoruz. çünük basit mantık, c[5][3] teki solution 
# mantıken c[5][4] te de ele alınmış olmalı. (tabloda takip ederek düşünme; basit mantık yap)
# ve c[5][4] en kötü ihtimal c[5][3] sonucunu verir bu yüzden

import pprint 

def get_sublist_size(L, j, k):
    count = 0
    for posting in L:
        if posting[2] > j and posting[1] < k:
            count += 1
    return count 

def get_space_increase(t):
    count = 0
    for posting in L:
        if posting[1] < t and posting[2] > t:
            count += 1
    return count

def get_processing_cost(L, materialization_points):
    materialization_points = materialization_points.copy()
    materialization_points.add(0)
    materialization_points.add(9) #todo: boundary elements will be inferred automatically

    materialization_points = sorted(materialization_points)
    
    total_cost = 0
    for i in range(len(materialization_points)-1):
        j = materialization_points[i]
        k = materialization_points[i+1]

        total_cost += (k-j) * get_sublist_size(L,j,k)

    return total_cost


def space_guarantee(L, N, cmax):
    DP = [ [ None for i in range(cmax) ] for j in range(N) ]
    pprint.pprint(DP)

    for i in range(cmax):
        DP[0][i] = set()
        
    for t in range(1, N):
        for i in range(get_space_increase(t)):
            DP[t][i] = set()
        
        for i in range(get_space_increase(t), cmax):
            
            min_cost = float('inf')
            min_materialization_points = None
            
            for t_ in range(t):
                materialization_points = DP[t_][i-get_space_increase(t)].copy()
                materialization_points.add(t)
                processing_cost = get_processing_cost(L, materialization_points)
                if min_cost > processing_cost:
                    min_cost = processing_cost
                    min_materialization_points = materialization_points
            
            DP[t][i] = min_materialization_points
    return DP

L = [ # Posting list
    ('d1', 0, 1), ('d2', 1, 2), ('d3', 2, 5), ('d4', 5, 7),
    ('d5', 0, 3), ('d6', 3, 6),('d7', 6, 9),
    ('d8', 0, 4), ('d9', 4, 8), ('d10', 8, 9)
]

N = 10
cmax = 5
print( get_processing_cost(L, {4,2}) )
print( get_processing_cost(L, {4,0,9,2}) )


DP = space_guarantee(L, N, cmax)
pprint.pprint(DP)


