from typing import List, Tuple, Set, FrozenSet, Dict, Iterable
from collections import Counter,defaultdict,deque


class LettersSolver:
    """
    Given an array of `letters`, returns the best possible solutions,
    with optional consideration for familiarity. If wordlist is not given,
    uses one taken from the Internet (TODO credit here). 

    Note: This version uses ATTEMPT 3: letters_old.py contains ATTEMPT 2.

    GOAL: Implement proper algorithms and data structures to ensure an
    adequate runtime.

    ATTEMPT 1:
        - Sort each word in wordlist, map sorted letters to list of
        corresponding words = O(n * k log k) [k = mean word length]
        - Sort letters, determine max-length subset of letters contained
        in map using DFS = O(2^l) [l = len(letters)]
        * would be faster with BFS

    results:
        - 9l 50k word: decent
        - 12l: slow

    ATTEMPT 2: (high words, low letters)
        - Changed DFS to BFS in step 2
        - Added option to return first find

    results:
        - 9l 50k word: instant
        - 16l: ~3s

    ATTEMPT 3: (high letters)
        - maps each word to letterset, sorts keys into length buckets
        = O(n * k) [k = mean word length]
        - from bucket <= len(letters), searches thru. lettersets until
        one is a subset of letters. Returns words if first find, else
        searches remaining bucket. = O(n)
        * Choose Attempt 2 if n > 2^l, else Attempt 3, e.g.
        n = 10^7 ~ l = 23.25

    results:
        - 16l 50k word: instant
        - 100l: instant
        - 1000l: instant with JIT warmup (!?!?!?!?)
    """

    WORDS = "en_50k.txt"
    def __init__(self,
                 wordlist: Iterable[str] | None = None,
                 doQuick: bool = True,
                 freqs: Dict[str, int] = {}):
        if not wordlist:
            self.getWordlist()
        else:
            self.wordlist = wordlist
            self.freqs = freqs

        self.letterMap = {}
        self.generateLetterMap()
        self.doQuick = doQuick


    def getWordlist(self):
        """
        Retrieves the default wordlist.
        """
        self.wordlist = []
        self.freqs = {}
        with open(self.WORDS,"r") as file:
            for i in file.readlines():
                w,f = i.split()
                self.wordlist.append(w)
                self.freqs[w] = int(f)


    def solve(self, letters: str) -> List[str]:
        """
        Solves the Letters Game with the given `letters` using the
        stored `wordlist`. Returns a list of best solves.
        """
        result = self._doSolve("".join(sorted(letters)))
        result = list(result)
        if self.freqs:
            result.sort(key=lambda l: -self.freqs[l])
        return result

    def _doSolve(self, letters: str) -> Set[str]:
        """
        Main algorithm used to solve the Letters Game. Called by
        `LettersSolver.solve`. If `self.doQuick`, returns the very first 
        match, otherwise attempts to find all maximal matches.
        """
        c = Counter(letters)
        fr = frozenset( # saves copy from making set before freezing
                [l + str(i) for (l,n) in c.items()
                for i in range(n)])

        returnSet = set()
        for i in range(len(letters),0,-1):
            if i not in self.letterMap: continue
            curOfLen = self.letterMap[i]
            found = False
            for s in iter(curOfLen): # gen, instead of d.keys() = set
                if not s.issubset(fr): continue
                if self.doQuick:
                    return curOfLen[s]
                returnSet.update(curOfLen[s])
                found = True

            if found:
                return returnSet



        return returnSet


    def generateLetterMap(self) -> Dict[int,Dict[FrozenSet[str],Set[str]]] :
        """
        Builds all required structures, called during initialisation.
        """
        def inner() -> Dict[FrozenSet[str],Set[str]]:
            return defaultdict(set)
        returnDict = defaultdict(inner)

        for w in self.wordlist:
            c = Counter(w)
            fr = frozenset( # saves copy from making set before freezing
                     [l + str(i) for (l,n) in c.items()
                     for i in range(n)])
            returnDict[len(w)][fr].add(w)

        self.letterMap = returnDict
        return returnDict




from random import choices

def main():
    """
    tests
    """
    CHARS = "abdefghijklmnopqrstuvwxyz"
    s = "".join(choices(CHARS,k=30))
    print(f"test = {s}")
    t = LettersSolver(doQuick=False)
    print("made lettermap!")
    print(t.solve(s))

if __name__ == "__main__":
    main()
