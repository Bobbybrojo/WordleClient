
# class that stores and tracks the running list of possible words
class WordManager:

    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                'u', 'v', 'w', 'x', 'y', 'z']

    def __init__(self):

        self.letters = {}
        for letter in self.alphabet:
            self.letters[letter] = [True, True, True, True, True]

        self.final_word = [" ", " ", " ", " ", " "]

        with open("words.txt") as f:
            self.words = f.readlines()

        for word in self.words:
            word.strip("\n")

    def filter_words(self):
        for word in list(self.words):
            if not self.valid_word(word):
                self.words.remove(word)

    def valid_word(self, word):
        for x in range(0, 5, 1):
            if self.final_word[x] != " ":
                return word[x] == self.final_word[x]

        for l in word:
            return self.letters[l][word.find(l)]
        return True

    def add_letter(self, letter, value, pos):
        if value == 0:
            self.letters[letter] = [False, False, False, False, False]
        elif value == 1:
            self.letters[letter][pos] = False
        elif value == 2:
            self.final_word[pos] = letter
            self.letters[letter][pos] = True
        else:
            print("Unable to add letter")

    def get_word(self):

        if " " not in self.final_word:
            return "".join(self.final_word)

        word = self.words[0]
        self.words.remove(word)
        return word.strip("\n")





