"""The AWPC UNIx UniCrypt module. This module contains all the encryption and decryption functions of the AWPC library, such as binary, ceasar, vigenere, railfence and OTP encryption and decryption."""

def BinaryEncrypt(InputString: str) -> str:
    RawBinary = ''.join(format(ord(i), '08b') for i in InputString)
    OutputString = ' '.join(RawBinary[i:i+8] for i in range(0, len(RawBinary), 8))
    return OutputString
def BinaryDecrypt(InputString: str) -> str:
    OutputString = ''.join(chr(int(b, 2)) for b in InputString.split())
    return OutputString
def CeasarEncrypt(InputString: str, Shift: int) -> str:
    OutputString = ""
    for Character in InputString:
        if Character.isalpha():               
            Position = ord(Character.lower()) - 96 
            NewPosition = (Position + Shift - 1) % 26 + 1   
            NewCharacter = chr(NewPosition + 96)        
            OutputString += NewCharacter                
        else:                                
            OutputString += Character 
    return OutputString
def CeasarDecrypt(InputString: str, Shift: int) -> str:
    OutputString = ""
    for Character in InputString:
        if Character.isalpha():               
            Position = ord(Character.lower()) - 96
            NewPosition = (Position - Shift - 1) % 26 + 1   
            NewCharacter = chr(NewPosition + 96)        
            OutputString += NewCharacter                
        else:                                 
            OutputString += Character
    return OutputString 
def VigenereEncrypt(InputString: str, KeyString: str) -> str:
    OutputString = ""

    for idx, Character in enumerate(InputString):
        if Character.isalpha():
            if Character.isupper():
                OutputString += chr((ord(Character) - ord(KeyString[idx % len(KeyString)].upper()) + 26) % 26 + ord("A"))
            else:
                OutputString += chr((ord(Character) - ord(KeyString[idx % len(KeyString)].lower()) + 26) % 26 + ord("a"))
        else:
            OutputString += Character
    return OutputString
def VigenereDecrypt(InputString: str, KeyString: str) -> str:
    OutputString = ""
    KeyString = KeyString.lower()
    KeyIdx = 0

    for Character in InputString:
        if Character.isalpha():
            Shift = ord(KeyString[KeyIdx % len(KeyString)]) - ord('a')
            if Character.isupper():
                DecryptedCharacter = chr((ord(Character) - ord('A') - Shift + 26) % 26 + ord('A'))
            else:
                DecryptedCharacter = chr((ord(Character) - ord('a') - Shift + 26) % 26 + ord('a'))
            OutputString += DecryptedCharacter
            KeyIdx += 1
        else:
            OutputString += Character

    return OutputString
def RailfenceEncrypt(InputString: str, Key: int) -> str:
    Key = int(Key)
    Position = 0
    Direction = 1
    Rows = [[] for _ in range(Key)]

    for Character in InputString:
        Rows[Position].append(Character)
    
        Position += Direction
        if Position == 0 or Position == Key - 1:
            Direction *= -1
    
    return ''.join([''.join(Row) for Row in Rows])
def RailfenceDecrypt(InputString: str, Key: int) -> str:
    Key = int(Key)
    length = len(InputString)
    pattern = []
    pos = 0
    direction = 1
    for _ in range(length):
        pattern.append(pos)
        pos += direction
        if pos == 0 or pos == Key - 1:
            direction *= -1

    counts = [pattern.count(r) for r in range(Key)]
    rows = []
    index = 0
    for c in counts:
        rows.append(list(InputString[index:index + c]))
        index += c

    plaintext = ''
    row_pointers = [0] * Key
    for r in pattern:
        plaintext += rows[r][row_pointers[r]]
        row_pointers[r] += 1

    return plaintext
def OTPEncrypt(InputString: str, KeyString: str) -> str:
    BinaryText = ''.join(format(ord(i), '08b') for i in InputString)
    BinaryKey = ''.join(format(ord(i), '08b') for i in KeyString)
    cipher = ''.join(str(int(b1) ^ int(b2)) for b1, b2 in zip(BinaryText, BinaryKey))
    return ' '.join(cipher[i:i+8] for i in range(0, len(cipher), 8))
def OTPDecrypt(InputString: str, KeyString: str) -> str:
    BinaryKey = ''.join(format(ord(i), '08b') for i in KeyString)
    plaintext_bits = ''.join(str(int(b1) ^ int(b2)) for b1, b2 in zip(InputString, BinaryKey))
    return ''.join(chr(int(plaintext_bits[i:i+8], 2)) for i in range(0, len(plaintext_bits), 8))
