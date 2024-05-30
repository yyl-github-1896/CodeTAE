import Data.List
 import Data.Maybe
 
 alphabet = [(' ',' '),('a','y'),('b','h'),('c','e'),('d','s'),('e','o') 
     ,('f','c'),('g','v'),('h','x'),('i','d'),('j','u'),('k','i'),('l','g')
     ,('m','l'),('n','b'),('o','k'),('p','r'),('q','z'),('r','t'),('s','n')
     ,('t','w'),('u','j'),('v','p'),('w','f'),('x','m'),('y','a'),('z', 'q')
     ]
 
 main = interact (unlines . map showCase . zip [1..] . tail . lines)
   where
     showCase (i, t) = "Case #" ++ show i ++ ": " ++ solve t
 
 solve = map (fromJust . flip lookup alphabet)