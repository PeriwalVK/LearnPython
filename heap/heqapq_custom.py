"""
heapify()	Transform list into a heap, in-place, in linear time.
heappop()	Pop and return the smallest item from the heap.
heappush()	Push item onto heap while maintaining the heap invariant.
heappushpop()	Push item on the heap, then pop and return the smallest item (more efficient than separate calls).
heapreplace()	Pop and return smallest item, and then push the new item.
merge()	Merge multiple sorted iterables into a single sorted iterator.
nlargest()	Return a list with the n largest elements.
nsmallest()	Return a list with the n smallest elements.
"""

from collections import defaultdict
import heapq
from typing import List


class WordFreq:
    def __init__(self, word: str, freq: int):
        self.word = word
        self.freq = freq

    def __lt__(self, other):
        # default one was "return self.value < other.value"
        # But can write our own logic here
        if self.freq != other.freq:
            return self.freq < other.freq
        else:
            return self.word > other.word


class Solution:
    def topKFrequent(self, words: List[str], k: int) -> List[str]:

        n = len(words)
        m = defaultdict(int)
        for word in words:
            m[word] += 1

        return [
            w.word
            for w in sorted(
                heapq.nlargest(k, [WordFreq(word, m[word]) for word in m]), reverse=True
            )
        ]


sol = Solution()
print(
    sol.topKFrequent(
        ["the", "day", "is", "sunny", "the", "the", "sunny", "is", "is"], k=4
    )
)

# Output: ["is", "the", "sunny", "day"]
# Explanation: "the", "is", "sunny" and "day" are the four most frequent words,
# with the number of occurrence being 3, 3, 2 and 1 respectively.
