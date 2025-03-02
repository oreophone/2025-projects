from typing import List, Tuple, Set, FrozenSet, Dict
from collections import Counter,defaultdict,deque

class LettersSolver:
    """
    Given an array of `letters`, returns the best possible solutions,
    with optional consideration for familiarity. If wordlist is not given,
    uses one taken from the Internet (TODO credit here).

    GOAL: Implement proper algorithms and data structures to ensure an
    adequate runtime.

    ATTEMPT 1:
        - Sort each word in wordlist, map sorted letters to list of
        corresponding words = O(n * k log k) [k = mean word length]
        - Sort letters, determine max-length subset of letters contained
        in map using DFS = O(2^n)
        * would be faster with BFS

    results:
        - 9l 50k word: decent
        - 12l: slow

    ATTEMPT 2:
        - Changed DFS to BFS in step 2
        - Added option to return first find

    results:
        - 9l 50k word: instant
        - 16l: ~3s
    """

    WORDS = "en_50k.txt"
    def __init__(self,
                 wordlist: Set[str] | None = None,
                 doQuick: bool = True,
                 freqs: Dict[str, int] = {}):
        if not wordlist:
            self.getWordlist()
        else:
            self.wordlist = wordlist
            self.freqs = freqs

        self.letterMap = self.generateLetterMap()
        self.doQuick = doQuick


    def getWordlist(self):
        """
        Retrieves the default wordlist.
        """
        self.wordlist = set()
        self.freqs = {}
        with open(self.WORDS,"r") as file:
            for i in file.readlines():
                w,f = i.split()
                self.wordlist.add(w)
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
        if len(letters) == 0:
            return set()

        todo = deque([letters])
        returnSet = set()
        l = len(letters)
        while len(todo) > 0 and l > 0:
            cur = todo.pop()
            if len(cur) < l:
                if len(returnSet) > 0:
                    return returnSet
                l -= 1
            if cur in self.letterMap:
                curSet = self.letterMap[cur]
                if self.doQuick:
                    return curSet
                returnSet.update(curSet)

            for i in range(len(cur)):
                if i > 0 and cur[i-1] == cur[i]: continue
                todo.appendleft(cur[:i] + cur[i+1:])



    def generateLetterMap(self) -> Dict[str, Set[str]] :
        """
        Builds all required structures, called during initialisation.
        """
        returnDict = defaultdict(set)
        for w in self.wordlist:
            key = "".join(sorted(w))
            returnDict[key].add(w)

        return returnDict

    # OLD ATTEMPTS

    def _doSolveOLD(self, letters: str, best=0) -> Tuple[int, Set[str]]:
        """
        Main algorithm used to solve the Letters Game. Called by
        `LettersSolver.solve`. 
        """
        if len(letters) < best or len(letters) == 0:
            return (0,set())
        if letters in self.letterMap:
            return (len(letters), self.letterMap[letters])

        curBest = 0
        returnSet = set()
        for i in range(len(letters)):
            if i > 0 and letters[i] == letters[i-1]:
                continue
            newLetters = letters[:i]+letters[i+1:]
            l, result = self._doSolveOLD(newLetters,curBest)
            if l > curBest:
                returnSet = result
                curBest = l
            elif l == curBest:
                returnSet.update(result)

        return (curBest, returnSet)



def main():
    """
    tests
    """
    t = LettersSolver(doQuick=False)
    print("made lettermap!")
    print(t.solve("tuuecparnguhlop"))

if __name__ == "__main__":
    main()
