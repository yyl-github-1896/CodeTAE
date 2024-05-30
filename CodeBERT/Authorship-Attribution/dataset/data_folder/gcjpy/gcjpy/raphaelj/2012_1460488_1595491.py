import Data.List
 import Data.Maybe
 
 main = interact (unlines . map showCase . zip [1..] . tail . lines)
   where
     showCase (i, t) = "Case #" ++ show i ++ ": " ++ solve t
 
 solve = show . solve' . map read . words
   where
     solve' (n:s:p:ts) = 
         let pts = map maxPoints ts
             directs = filter ((>= p) . fst) pts
             surps = filter (\(pd, ps) -> pd < p && ps >= p) pts
         in length directs + min (length surps) s
         
 maxPoints :: Int -> (Int, Int)
 maxPoints tot = 
     (maxScore $ scores normal, maxScore $ scores surprising)
   where
     scores cond = [ (x, y, z) |
         x <- [0..10], y <- [0..10], z <- [0..10]
         , x + y + z == tot, cond (x, y, z)
         ]
     normal t = bestScore t - badScore t <= 1
     surprising t = bestScore t - badScore t <= 2
     maxScore = maximum . map bestScore 
 
 bestScore (x, y, z) = maximum [x, y, z]
 badScore (x, y, z) = minimum [x, y, z]