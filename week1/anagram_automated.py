import requests
from bs4 import BeautifulSoup

myDict = {}
myPoints = []

def main():
    count = 0
    while count < 10:
        url = "https://icanhazwordz.appspot.com/"
        dictionaryfile = "dictionarywords.txt"
        load_dict(dictionaryfile)
        with requests.session() as s:
            resp = s.get(url)
            soup = BeautifulSoup(resp.text, "lxml")
            previousWords = []
            seed = soup.find(attrs={"name": "Seed"})['value']
            started = soup.find(attrs={"name": "Started"})['value']
            payload = {"Seed": seed, "Started": started}
        
            for i in range(10):
                soup = BeautifulSoup(resp.text, "lxml")
                scrapedWords = soup.find_all("div", class_="letter")

                scrapedWordsList = []

                for elem in scrapedWords:
                    if elem.get_text() == 'Qu':
                        scrapedWordsList.append('q')
                    else:
                        scrapedWordsList.append(elem.get_text())
                word = "".join(scrapedWordsList).lower()
                print(word)
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
                            if word[index] == 'q':
                                currentword.append('u')
                        int_pos <<= 1
                    # dont include words that has less than 3 chars
                    if len(currentword) > 2:
                        word_list.append("".join(currentword))
                anagrams = find_anagram(word_list)
                
                if anagrams:
                    best_anagram = calculate_points(anagrams)
                    payload["move"] = best_anagram
                    payload['Moves'] = previousWords
                    previousWords.append(best_anagram)
                    resp = s.post(url, data=payload)
                else:
                    resp = s.post(url)
            if final_point(myPoints) > 1500:
                count += 1
                url = "https://icanhazwordz.appspot.com/highscores"
                payload = {"Seed": seed, "Started": started, "Moves": previousWords}
                payload["NickName"] = "Jasmine"
                payload["URL"] = "https://gist.github.com/teeyingyap/9ec611c80b118b7ae3351fe8633aff25"
                payload["Agent"] = "Robot"
                payload["Name"] = "Yap Tee Ying"
                payload["Email"] = "yapteeying@gmail.com"
                resp = s.post(url, data=payload)
            del myPoints[:]


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


def calculate_points(anagram_list):
    chosen_word = ""
    current_point = 0
    for word in anagram_list:
        points = 1 # bonus 1 point
        # if q is not the first letter skip it
        if 'q' in word and 'q' != word[0]:
            continue
        for char in word:
            if char in ['c', 'h', 'f', 'l', 'm', 'p', 'v', 'w', 'y']:
                points += 2
            elif char in ['j', 'k', 'x', 'z']:
                points += 3
            else:
                points += 1
        # take care of Qu case
        if word[0] == 'q' and word[1] == 'u':
            points += 1
        if points > current_point:
            chosen_word = word
            current_point = points
    myPoints.append(current_point)
    print("The word with highest points is", chosen_word, current_point)
    return chosen_word


def final_point(points_list):
    x = 0
    for point in points_list:
        x += point**2
    print(x)
    return x

    
main()