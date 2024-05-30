t = int(input())
 
 VIDE = 0
 MINE = 1
 CURSEUR = 2
 
 def test_position(arr, lignes, cols, y, x):
     def voisinage_libre(arr, y, x):
         if y > 0:
             if x > 0 and arr[y-1][x-1] == MINE:
                 return False
             if arr[y-1][x] == MINE:
                 return False
             if x < cols - 1 and arr[y-1][x+1] == MINE:
                 return False
 
         if x > 0 and arr[y][x-1] == MINE:
             return False
         if x < cols - 1 and arr[y][x+1] == MINE:
             return False
 
         if y < lignes - 1:
             if x > 0 and arr[y+1][x-1] == MINE:
                 return False
             if arr[y+1][x] == MINE:
                 return False
             if x < cols - 1 and arr[y+1][x+1] == MINE:
                 return False
 
         return True
 
     def remplissage_rec(arr, y, x):
         if x < 0 or y < 0 or x >= cols or y >= lignes:
             return
         elif arr[y][x] == CURSEUR:
             return
 
         arr[y][x] = CURSEUR
         if voisinage_libre(arr, y, x):
             remplissage_rec(arr, y-1, x-1)
             remplissage_rec(arr, y-1, x)
             remplissage_rec(arr, y-1, x+1)
             remplissage_rec(arr, y, x-1)
             remplissage_rec(arr, y, x+1)
             remplissage_rec(arr, y+1, x-1)
             remplissage_rec(arr, y+1, x)
             remplissage_rec(arr, y+1, x+1)
 
     if arr[y][x] != VIDE:
         return False
 
     # Copie arr and arr2
     arr2 = [ [ arr[i][j] for j in range(0, cols) ] for i in range(0, lignes) ]
 
     remplissage_rec(arr2, y, x)
 
     for i in range(0, lignes):
         for j in range(0, cols):
             if arr2[i][j] == VIDE:
                 return False
     return True
 
 def dfs(arr, lignes, cols, mines, y, x):
     cases_restantes = (cols - x) + ((lignes - y) * cols)
 
     if cases_restantes < mines:
         return None
     elif mines <= 0:
         for i in range(0, lignes):
             for j in range(0, cols):
                 if test_position(arr, lignes, cols, i, j):
                     return (i, j)
     elif x >= cols:
         return dfs(arr, lignes, cols, mines, y+1, 0)
     elif y >= lignes:
         return None
     else:
         res = dfs(arr, lignes, cols, mines, y, x+1)
         if res != None:
             return res
 
         arr[y][x] = MINE
         res = dfs(arr, lignes, cols, mines-1, y, x+1)
         if res != None:
             return res
 
         arr[y][x] = VIDE
         return None
 
 for i in range(0, t):
     ligne  = input().split(" ")
     lignes = int(ligne[0])
     cols   = int(ligne[1])
     mines  = int(ligne[2])
 
     arr = [ [VIDE] * cols for _ in range(0, lignes) ]
 
     res = dfs(arr, lignes, cols, mines, 0, 0)
 
     print ("Case #"+str(i+1)+":")
 
     if res == None:
         print ("Impossible")
     else:
         (y, x) = res
 
         for i in range(0, lignes):
             for j in range(0, cols):
                 if i == y and j == x:
                     print('c', end='')
                 elif arr[i][j] == VIDE:
                     print('.', end='')
                 else:
                     print('*', end='')
 
             print('', end='\n')
