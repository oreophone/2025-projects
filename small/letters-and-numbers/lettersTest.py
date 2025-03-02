from letters import LettersSolver
import random
from typing import List, Tuple, Dict, Set, Generator
from time import time
from collections import Counter

class LettersTest(LettersSolver):
    """
    A subclass of LetterSolver that tests and times its
    implementation with randomised dictionaries.
    """

    ALPHA = "abcdefghijklmnopqrstuvwxyz"

    def __init__(self,
                 numLetters: int = 10,  # Goal: 1_000
                 numWords: int = 1_000, # Goal: 1_000_000
                 doQuick: bool = True
                 ):
        self.numLetters = numLetters
        self.numWords = numWords
        self.letters = ""
        self.solution = ""
        self.lettersCounter = {}

        self.wordIter = iter(["a"])

        super().__init__(self.wordIter,doQuick) # lettermap regen'd in test

        self.genTest()

    def isSolution(self,word: str) -> bool:
        """
        Returns True if `word` is a solution to the Letters game
        with letters `self.letters` that is better than `self.solution`.
        """
        if len(word) <= len(self.solution): return False
        wordCount = Counter(word)
        for w,v in wordCount.items():
            if w not in self.lettersCounter: return False
            if v > self.lettersCounter[w]: return False
        return True

    def runTest(self) -> Tuple[bool, float]:
        """
        The currently generated test is ran, with diagnostics printed.
        Returns True if the test was successful, along with runtime
        (not including genWords runtime).
        """
        print("Timing Generator...")
        genStart = time()
        for w in self.genWords():
            continue
        genTime = time() - genStart
        print(f"Generator took {genTime} s.")
        
        print(f"Timing Dictionary Preprocessing...")
        dStart = time()
        self.generateLetterMap()
        
        dTime = time() - dStart
        print(f"Dictionary Preprocessing took {dTime} s.")

        print(f"Timing Solution Finding...")
        solStart = time()
        results = self.solve(self.letters)
        solTime = time() - solStart
        print(f"Solution Finding took {solTime} s.")

        isGood = self.solution in results
        if isGood:
            print(f"Correct! Solution = '{self.solution}' (len = {len(self.solution)})")
        else:
            print("Wrong... Solution/Found below:")
            print(self.solution)
            print(results[0])

        print(f'\nLetters = {self.letters}')

        runtime = solTime + dTime - genTime
        print("\n\n-----")
        print(f"Runtime: {runtime} s. ({solTime} + {dTime} - {genTime}")
        print(f"Letters/Words = {self.numLetters}/{self.numWords}")
        return (isGood, runtime)

    def genTest(self):
        """
        Generates all required variables for testing in the correct
        sequence (letters, solution, words).
        """
        self.genLetters()
        solLength = random.randint(1,self.numLetters)
        self.solution = "".join(random.sample(self.letters,solLength))
        self.wordIter = self.genWords()
        self.wordlist = self.wordIter


    def genLetters(self) -> str:
        """
        Generates and returns the letters for the test.
        """
        ls = random.choices(self.ALPHA,k=self.numLetters)
        self.letters = "".join(ls)
        self.lettersCounter = Counter(ls)
        return self.letters


    def genWords(self) -> Generator:
        """
        Generates and yields the words for the test dictionary, making
        sure `self.solution` remains a maximal solution.
        """
        yield self.solution
        wordLens = random.choices(range(1,self.numLetters+1),k=self.numWords-1)
        for n in wordLens:
            curWord = None
            while curWord is None or self.isSolution(curWord):
                curWord = "".join(random.choices(self.ALPHA,k=n))
            yield curWord

if __name__ == "__main__":
    t = LettersTest(30,300_000)
    t.runTest()




