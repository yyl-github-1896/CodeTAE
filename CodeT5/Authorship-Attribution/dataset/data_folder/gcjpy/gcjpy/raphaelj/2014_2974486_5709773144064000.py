import Data.Int
 import Data.List
 import qualified Data.Foldable as F
 import Text.Printf
 
 import Debug.Trace
 
 data Test = Test {
       cout     :: Double
     , bonus    :: Double
     , objectif :: Double
     } deriving Show
 
 newtype Solution = Solution { temps :: Double }
 
 instance Show Solution where
     show (Solution t) = show t
 
 main = do
     interact (unlines . map showCase . zip [1..] . map resoudre . goTest . tail . lines)
 
   where
     goTest [] = []
     goTest (l:ls) =
         let [c, f, x] = map read $ words l
         in Test c f x : goTest ls
 
     showCase :: (Int, Solution) -> String
     showCase (i, s) = printf "Case #%d: %s" i (show s)
 
 resoudre :: Test -> Solution
 resoudre Test {..} | premierAchat > sansAchat = Solution sansAchat
                    | otherwise                = go premierAchat 2
   where
     go t prod | tempsAvecAchat >= tempsSansAchat = Solution (t + tempsSansAchat)
               | otherwise                        =
                   go (t + delaiProchainAchat) prod'
       where
         prod' = prod + bonus
 
         tempsAvecAchat = objectif / prod'
         tempsSansAchat = (objectif - cout) / prod
 
         delaiProchainAchat = cout / prod'
 
     premierAchat = cout / 2
     sansAchat    = objectif / 2
