import Data.Int
 import Data.List.Split
 import Text.Printf
 
 main = do
     interact (unlines . map showCase . zip [1..] . map (solve . interval) . tail . lines)
 
   where
     interval :: String -> (Int64, Int64)
     interval l =
         let [a, b] = map read $ splitOn " " l
         in (a, b)
 
     showCase :: (Int64, Int) -> String
     showCase (i, r) = printf "Case #%d: %d" i r
 
 solve :: (Int64, Int64) -> Int
 solve (a, b) =
     length $ takeWhile (<= b) $ dropWhile (< a) [ sq
         | x <- [0..], palindrome x, let sq = x * x, palindrome sq
         ]
   where
     square x = x * x
     start = truncate $ sqrt $ double a
 
 -- | Returns True if s is a palindrome.
 palindrome s =
     let s' = show s
     in s' == reverse s'
 
 double :: Int64 -> Double
 double = fromIntegral