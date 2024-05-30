import Data.Int
 import Data.List
 import qualified Data.Foldable as F
 import Text.Printf
 
 import Debug.Trace
 
 data Test = Test {
       choix1 :: Int
     , table1 :: [[Int]]
     , choix2 :: Int
     , table2 :: [[Int]]
     } deriving Show
 
 data Solution = Bonne Int | BadMag | Cheat
 
 instance Show Solution where
     show (Bonne i) = show i
     show BadMag    = "Bad magician!"
     show Cheat     = "Volunteer cheated!"
 
 main = do
     interact (unlines . map showCase . zip [1..] . map (resoudre) . goTest . tail . lines)
 
   where
     goTest [] = []
     goTest ls =
         let (c1, t1, ls')  = goTable ls
             (c2, t2, ls'') = goTable ls'
         in Test c1 t1 c2 t2 : goTest ls''
 
     goTable (n:ls) =
         let c = read n
             (t, ls') = splitAt 4 ls
         in (c, map goLigne t, ls')
 
     goLigne = map read . words
 
     showCase :: (Int, Solution) -> String
     showCase (i, s) = printf "Case #%d: %s" i (show s)
 
 resoudre :: Test -> Solution
 resoudre Test {..} =
     let choisis1 = table1 !! (choix1 - 1)
         choisis2 = table2 !! (choix2 - 1)
         communs  = filter (`elem` choisis1) choisis2
     in case communs of
         [x]     -> Bonne x
         (_:_:_) -> BadMag
         []      -> Cheat
