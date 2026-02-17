class PatternSearch:
    def __init__(self):
        self._delim = "@"

    def calcLPS(self, s: str):
        n = len(s)
        lps = [0]
        for i in range(1, n):
            j = lps[i - 1]
            while j > 0 and s[i] != s[j]:
                j = lps[j - 1]

            lps.append(j + 1 if s[j] == s[i] else 0)
        return lps

    def z_algo_search(self, pat, txt):
        # code here
        s = pat + self._delim + txt
        lp = len(pat)
        lps = self.calcLPS(s)

        ret = []
        for i in range(lp, len(lps)):
            if lps[i] == lp:
                print(f"[Z-Algo]: Found pattern at index {i - 2 * lp}")
                ret.append(i - 2 * lp)
        return ret

    def kmp_algo_search(self, pat, txt):
        # code here
        m = len(pat)
        n = len(txt)

        # Preprocess the pattern (calculate lps[] array)
        lps = self.calcLPS(pat)
        ret = []

        j = 0
        for i in range(n):
            while j > 0 and txt[i] != pat[j]:
                j = lps[j - 1]
            if txt[i] == pat[j]:
                j += 1

            if j == m:
                print(f"[KMP]: Found pattern at index {i - j + 1}")
                ret.append(i - j + 1)
                j = lps[j - 1]

        return ret


if __name__ == "__main__":
    pat, txt = "aaba", "aabaacaadaabaaba"
    # pat, txt = "doms", "somerandomstringkingdoms"

    print(PatternSearch().z_algo_search(pat, txt))
    print(PatternSearch().kmp_algo_search(pat, txt))
