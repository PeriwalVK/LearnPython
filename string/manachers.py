# Manacher's longest palindromic substring searching algorithm


"""
Manacher's Algorithm
--------------------
Goal: Find the longest palindromic substring in O(N)

Key idea:
- Convert the string so that even/odd length palindromes become uniform
- Use previously computed palindromes to avoid re-checking characters
"""


def manachers_algorithm(s: str) -> str:
    # 🔹 Step 1: Transform string
    # "abba" → "^#a#b#b#a#$"
    # '#' handles even-length palindromes
    # '^' and '$' are sentinels to avoid bounds checking, provided these 2 should never appear in original string
    transformed = "^#" + "#".join(s) + "#$"

    n = len(transformed)
    """
    # 🔹 P[i] = radius of palindrome centered at i
    # i.e. How much in the front is same as back, excluding center (thats why default 0 bcz khud ko nhi count kiya)
    # So finally when we compare that to real string
    #       -> length of actual palindrom with that center and removing all # is => P[i]
    #       -> index of palindrome start in original string is => 
    #               first find leftmost # of palindrome => (i - P[i])
    #               Now find corresponsing index in original string
    #                   ^#a#b#$ 
    #                       isme i=1 means original me 0 (yaani 1//2)
    #                       isme i=3 means original me 1 (yaani 3//2)
    #               Hence original index = (i - P[i])//2
    """

    P = [0] * n

    right = 0  # right boundary of that palindrome that has reached rightmost till now
    center = 0  # center of that current rightmost palindrome

    # 🔹 Step 2: Scan each position as center
    for i in range(1, n - 1):
        mirror = 2 * center - i
        """
        # mirror of i around center, bcz: [mirror .....center.....i] => center - mirror = i - center
        # And notice that i will always lie right to current center
        #     bcz initialised as center= 0 and i=1
        #     and post that whenever updated (center = i) -> i increases in next loop
        """

        # # 🔹 Step 2.1: Even length case
        # if i < right:
        #     P[i] = min(right - i, P[mirror])

        # 🔹 Step 3: Reuse previous information (key optimization)
        # if i < right: # else defailut = 0
        #     P[i] = min(right - i, P[mirror])
        P[i] = max(0, min(right - i, P[mirror]))

        # 🔹 Step 4: Try to expand palindrome centered at i
        while transformed[i + P[i] + 1] == transformed[i - P[i] - 1]:
            P[i] += 1

        # 🔹 Step 5: Update center & right boundary if expanded past right
        if i + P[i] > right:
            center = i
            right = i + P[i]

    # 🔹 Step 6: Find maximum palindrome (or could have had that logic in last loop itself)
    max_len = max(P)
    center_index = P.index(max_len)

    # 🔹 Convert back to original string indices
    start = (center_index - max_len) // 2
    return s[start : start + max_len]


# ---------------- Driver Code ----------------

if __name__ == "__main__":
    # text = "babad"
    # print(manachers_algorithm(text))  # "bab" or "aba"

    while True:
        s = input("Enter a string: ")
        if s == "0":
            print("EXITING...")
            break
        print(f"\t\t\tinput is: {s}")
        print(f"\t\t\tpalindrome is: {manachers_algorithm(s)}")


# def construct(input: str):
#     return "^" + "#".join(input) + "$"


# def Manachers(input: str):
#     n = len(input)
#     if n == 0:
#         return None
#     s: str = construct(input)

#     m = len(s)
#     p = [0] * m

#     c, r = 0, 0

#     for i in range(m):
#         mirror: int = 2 * c - i
#         p[i] = min(p[mirror], r - i) if i < r else 0
#         # // if(i<r) p[i] = min(r-i,p[mirror]);

#         while s[i + p[i] + 1] == s[i - p[i] - 1]:
#             p[i] += 1
#             if i + p[i] > r:
#                 c = i
#                 r = i + p[i]

#     # // should work with this
#     # // if(r==m-2) break;

#     cindex = 0
#     max_len = 0
#     for i in range(1, m):
#         if max_len < p[i]:
#             cindex = i
#             max_len = p[i]

#     start = (cindex - max_len - 1) / 2
#     return input[start : start + max_len]


# # // Driver program to test above function
# def main():
#     # // string s = "babcbaabcbaccba";
#     while True:
#         # // string s = "abababa";
#         s = input("Enter a string")
#         if s == "0":
#             break
#         print(f"input is: {s}")
#         print(f"palindrome is: {Manachers(s)}")


# main()
