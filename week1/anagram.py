from sys import argv

myDict = {}

def main():
    if len(argv) != 3:
        print("Usage: python anagram.py randomword dictionary.txt")
        return 1
    if not argv[1].isalpha():
        print("Invalid word.")
        return 1
    dictionaryfile = argv[2]
    load_dict(dictionaryfile)
    word = argv[1].lower()
    word_list = []
    # each word has 2 to the power N combinations
    # use bitwise operators to get all possible combinations
    n = len(word)
    binarynum = 1 << n
    for i in range(1, binarynum):
        currentword = []
        int_pos = 1
        for index in range(n):
            if i & int_pos:
                currentword.append(word[index])
            int_pos <<= 1
        # dont include words that has less than 3 chars
        if len(currentword) > 2:
            word_list.append("".join(currentword))
    anagrams = find_anagram(word_list)
    if anagrams:
        for word in anagrams:
            print(word)
    else:
        print("No anagrams found.")

def find_anagram(wordlist):
    anagrams_found = []
    # dont search for the same key twice
    searched_strkey = []
    for word in wordlist:
        strkey = convert_into_int(word)
        if strkey in myDict and strkey not in searched_strkey:
            for dictword in myDict[strkey]:
                anagrams_found.append(dictword)
        searched_strkey.append(strkey)
    return anagrams_found


def load_dict(dictionaryfile):
    # load dictionary into a python dictionary
    with open(dictionaryfile, "r") as file:
        lines = file.readlines()
        for line in lines:
            word = line.lower().strip()
            myStrKey = convert_into_int(word)
            if myStrKey in myDict:
                myDict[myStrKey].append(word)
            else:
                myDict[myStrKey] = [word]


def convert_into_int(word):
    # key is represented by a string of 26 numbers
    # each number represents the number of each char in the string
    myKey = [0] * 26
    for char in word:
        myKey[ord(char) - 97] += 1
    return(''.join(str(x) for x in myKey))


main()