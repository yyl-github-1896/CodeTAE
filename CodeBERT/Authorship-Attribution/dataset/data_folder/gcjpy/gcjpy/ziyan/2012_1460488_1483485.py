import sys
 
 cipher = dict()
 
 def learn(encrypted_text, clear_text):
     for encrypted_letter, clear_letter in zip(encrypted_text, clear_text):
         if encrypted_letter in cipher:
             assert cipher[encrypted_letter] == clear_letter
         cipher[encrypted_letter] = clear_letter
 
 def test():
     alphabet = 'abcdefghijklmnopqrstuvwxyz '
     for letter in alphabet:
         if letter not in cipher.keys():
             print 'Googlerese letter %s does not have corresponding English letter.' % letter
         if letter not in cipher.values():
             print 'English letter %s not found in cipher dictionary values.' % letter
     if len(cipher.keys()) != len(alphabet):
         print 'Size of cipher dictionary and alphabet mismatch.'
 
 def decrypt(text):
     decrypted_text = ''
     for letter in text:
         assert letter in cipher
         decrypted_text += cipher[letter]
     return decrypted_text
 
 def main():
     learn(' yeqz', ' aozq')
     learn('ejp mysljylc kd kxveddknmc re jsicpdrysi', 'our language is impossible to understand')
     learn('rbcpc ypc rtcsra dkh wyfrepkym veddknkmkrkcd', 'there are twenty six factorial possibilities')
     learn('de kr kd eoya kw aej tysr re ujdr lkgc jv', 'so it is okay if you want to just give up')
     test()
 
     case_count = int(sys.stdin.readline())
 
     for case_index in range(1, case_count + 1):
         print 'Case #%i: %s' % (case_index, decrypt(sys.stdin.readline().strip()))
 
 if __name__ == '__main__':
     main()