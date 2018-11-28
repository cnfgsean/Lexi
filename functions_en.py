import random
from string import ascii_lowercase


def random_from_txt(file, index=None):
    lines = 0
    with open(file, encoding="utf8") as inFile:
        for _ in inFile:
            lines += 1
        if not index:
            ind = random.randint(1, lines)
        else:
            ind = index
        inFile.seek(0)
        for i in range(1, lines + 1):
            word = inFile.readline()
            if i == ind:
                return word.strip()


def is_word(word):
    with open("texts/en_words.txt") as inFile:
        for i in inFile:
            if word.strip().lower() == i.strip().lower():
                return True
    return False


def new_adjective(syllables):
    if syllables < 1 or syllables > 4:
        return
    if syllables == 1:
        return random_from_txt("texts/1syllableadjectives.txt")
    elif syllables == 2:
        return random_from_txt("texts/2syllableadjectives.txt")
    elif syllables == 3:
        return random_from_txt("texts/3syllableadjectives.txt")
    elif syllables == 4:
        return random_from_txt("texts/4syllableadjectives.txt")


def new_adverb(syllables):
    if syllables < 1 or syllables > 4:
        return
    if syllables == 1:
        return random_from_txt("texts/1syllableadverbs.txt")
    elif syllables == 2:
        return random_from_txt("texts/2syllableadverbs.txt")
    elif syllables == 3:
        return random_from_txt("texts/3syllableadverbs.txt")
    elif syllables == 4:
        return random_from_txt("texts/4syllableadverbs.txt")


def new_noun(syllables):
    if syllables < 1 or syllables > 4:
        return
    if syllables == 1:
        return random_from_txt("texts/1syllablenouns.txt")
    elif syllables == 2:
        return random_from_txt("texts/2syllablenouns.txt")
    elif syllables == 3:
        return random_from_txt("texts/3syllablenouns.txt")
    elif syllables == 4:
        return random_from_txt("texts/4syllablenouns.txt")


def new_verb(syllables):
    if syllables < 1 or syllables > 4:
        return
    if syllables == 1:
        return random_from_txt("texts/1syllableverbs.txt")
    elif syllables == 2:
        return random_from_txt("texts/2syllableverbs.txt")
    elif syllables == 3:
        return random_from_txt("texts/3syllableverbs.txt")
    elif syllables == 4:
        return random_from_txt("texts/4syllableverbs.txt")


def will_like(phrase):
    length = len(phrase)
    alpha_index = 50
    auto_likes = ["sean", "lexi", "music", "robots", "bots", "randombot"]
    if "".join(phrase).lower() in auto_likes:
        adj = random_from_txt("texts/positive_adjectives.txt").lower()
        return ["I already like {}.".format("".join(phrase)), "I already know that is {}.".format(adj)]
    for word in phrase:
        for letter in word.strip().lower():
            if letter.isalpha():
                pos = ascii_lowercase.index(letter) + 1
                length += 1
                if pos % 2 == 0:
                    alpha_index += pos % 2
                else:
                    alpha_index += pos % 3
            else:
                continue

    sub_total = length * alpha_index ** 3
    total_index = 0
    for i in str(sub_total):
        total_index += int(i)
    liking = total_index % 4
    response = total_index % 5
    print("Total index {}, liking {}, response {}".format(total_index, liking, response))
    if total_index == 0:
        return ["Uhh, it seems like I don't have something to give my completely predetermined opinion to."]
    if liking == 3:  # TODO: Finish up responses
        adj = random_from_txt("texts/positive_adjectives.txt", (total_index % 1925) + 1).lower()
        if response == 1:
            return ["I really like {}.".format(" ".join(phrase)), "That stuff is pretty {}. 10/10".format(adj)]
        elif response == 2:
            return ["I absolutely love {}.".format(" ".join(phrase)), "I would rate it very {}.".format(adj)]
        else:
            return ["I absolutely love {}.".format(" ".join(phrase)), "I would rate it being {}".format(adj)]
    elif liking == 1:
        adj = random_from_txt("texts/positive_adjectives.txt", (total_index % 1925) + 1).lower()
        if response == 1:
            return ["I kinda like the sound of {}.".format(" ".join(phrase)),
                    "I feel that it's {} when I think of it.".format(adj)]
        elif response == 2:
            return ["I think I am starting to like {}.".format(" ".join(phrase)),
                    "I feel {} when I think of that.".format(adj)]
        else:
            return ["I think I am starting to like {}.".format(" ".join(phrase)),
                    "I feel {} when I think of that.".format(adj)]
    elif liking == 0:
        adj = random_from_txt("texts/negative_adjectives.txt", (total_index % 98) + 1).lower()
        if response == 1:
            return ["I am not particularly fond of {}.".format(" ".join(phrase)), "It seems kinda {}.".format(adj)]
        elif response == 2:
            return ["I don't really like thinking of {}.".format(" ".join(phrase)), "Don't you think it's {}?".format(adj)]
        else:
            return ["I don't really like thinking of {}.".format(" ".join(phrase)),
                    "Don't you think it's {}?".format(adj)]
    else:
        adj = random_from_txt("texts/negative_adjectives.txt", (total_index % 98) + 1).lower()
        if response == 1:
            return ["I don't really like {}.".format(" ".join(phrase)), "I feel {} when I think of that stuff.".format(adj)]
        elif response == 2:
            return ["Not a big fan of {}.".format(" ".join(phrase)),
                    "That stuff is pretty {}.".format(adj)]
        else:
            return ["Not a big fan of {}.".format(" ".join(phrase)),
                    "That stuff is pretty {}.".format(adj)]
