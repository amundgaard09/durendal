def BinaryEncrypt(InputString: str) -> str:
    OutputString  = ''.join(format(ord(i), '08b') for i in InputString)
    return OutputString
def BinaryDecrypt(InputString: str) -> str:
    OutputString = ''.join(chr(int(b, 2)) for b in InputString)
    return OutputString


class Solution:
    def reverseBits(self, n: int) -> int:
        binary = format(n, '032b')
        reversed_binary = binary[::-1]
        return int(reversed_binary, 2)

print(Solution().reverseBits(102030120))