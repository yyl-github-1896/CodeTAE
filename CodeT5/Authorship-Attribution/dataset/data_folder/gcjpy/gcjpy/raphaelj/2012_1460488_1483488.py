import Data.List
 import Data.Maybe
 
 import Debug.Trace
 
 main = interact (unlines . map showCase . zip [1..] . tail . lines)
   where
     showCase (i, t) = "Case #" ++ show i ++ ": " ++ solve t
 
 solve = show . solve'' . map read . words
 solve' [a, b] = length [ () | 
         x <- [a..b]
     , let digits = nDigits x, let lastY = min b (10^digits - 1)
     , y <- [x+1..lastY]
     , isRecycled x y digits
     ]
     
 solve'' [a, b] = sum [ nRecycled | 
       x <- [a..b]
     , let digits = nDigits x
     , let nRecycled = length [ () |
               y <- nub $ sort $ moves x digits
             , y <= b, y > x
             ]
     ]
 
 isRecycled :: Int -> Int -> Int -> Bool
 isRecycled n m digits = any (== n) (m : moves m digits)
 
 nDigits :: Int -> Int
 nDigits n = nDigits' n 0
   where
     nDigits' 0 acc = acc
     nDigits' x acc = nDigits' (x `div` 10) (acc+1)
 
 moves :: Int -> Int -> [Int]
 moves n digits = [ dep n d digits | d <- [1..digits-1] ]
 dep x d digits = x * 10^d `rem` (10^digits) + x `div` 10^(digits - d)