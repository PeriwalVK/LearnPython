class Solution:
    def __init__(self):
        self.delim = '@'
    def calcLPS(self, s: str):
        n = len(s)
        lps = [0]
        for i in range(1, n):
            l = lps[i - 1]
            while l > 0 and s[i] != s[l]:
                l = lps[l - 1]

            lps.append(l + 1 if s[l] == s[i] else 0)
        return lps

    def z_algo_search(self, pat, txt):
        # code here
        s = pat + self.delim + txt
        lp = len(pat)
        x = self.calcLPS(s)
        ret = []
        for i in range(lp, len(x)):
            if x[i] == lp:
                ret.append(i - 2 * lp)
        return ret


print(Solution().z_algo_search("iki", "vikasikikiajnabi"))