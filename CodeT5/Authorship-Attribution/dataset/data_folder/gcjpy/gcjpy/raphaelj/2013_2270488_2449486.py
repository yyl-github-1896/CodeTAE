import Control.Applicative
 import Data.Array.Unboxed
 import Data.List.Split
 import Text.Printf
 
 main = do
     interact (unlines . map showCase . zip [1..] . go . tail . lines)
 
   where
     go :: [String] -> [Bool]
     go []     = []
     go (l:ls) =
         let [h, w] = map read $ splitOn " " l
             (ls', ls'') = splitAt h ls
             table = map (map read . splitOn " ") ls'
         in solve h w table : go ls''
 
     showCase :: (Int, Bool) -> String
     showCase (i, r) = printf "Case #%d: %s" i (if r then "YES" else "NO")
 
 solve :: Int -> Int -> [[Int]] -> Bool
 solve h w table = and [ cell >= (maxLgn ! y) || cell >= (maxCol ! x)
     | y <- [0..h-1], x <- [0..w-1], let cell = arr ! (y, x)
     ]
   where
     arr :: Array (Int, Int) Int
     arr = listArray ((0, 0), (h-1, w-1)) $ concat table
 
     maxLgn, maxCol :: Array Int Int
     maxLgn = listArray (0, h-1) $ [ maximum [ arr ! (y, x) | x <- [0..w-1] ]
         | y <- [0..h-1]
         ]
 
     maxCol = listArray (0, w-1) $ [ maximum [ arr ! (y, x) | y <- [0..h-1] ]
         | x <- [0..w-1]
         ]