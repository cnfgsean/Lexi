import functions_en as en
import random


class Poem(object):
    def __init__(self, lines, subject):
        self.lines = lines
        self.content = []
        self.syllable_limit = random.randint(7, 13)
        self.subject = subject
        if self.subject == "?":
            self.subject = en.new_noun(random.randint(1, 4))
        self.subject2 = en.new_noun(random.randint(1, 4))
        print("Poem created.")
        print("Lines: {}".format(self.lines))
        print("Syllable limit: {}".format(self.syllable_limit))
        print("Subject: {}".format(self.subject))
        print("Subject2: {}".format(self.subject2))

    def rant(self):
        for i in range(self.lines):
            s = []
            syllables = 0
            # adjective, noun, adverb, verb
            pos = 0
            if i % 4 == 0:
                x = random.randint(0, 3)
                if x == 0:
                    s.append("the")
                elif x == 1:
                    s.append("of")
                elif x == 2:
                    s.append("what")
                elif x == 3:
                    s.append("to")
                syllables += 1
            while syllables < self.syllable_limit:
                if self.syllable_limit - syllables > 4:
                    new_word_syllables = random.randint(1, 4)
                else:
                    new_word_syllables = self.syllable_limit - syllables
                syllables += new_word_syllables

                if pos % 4 == 0:
                    s.append(en.new_adjective(new_word_syllables))
                elif pos % 4 == 1:
                    x = random.randint(0, 25)
                    if i % 4 == 0 or i % 4 == 3:
                        s.append(self.subject)
                    elif x > 13:
                        s.append(en.new_noun(new_word_syllables))
                    elif x > 9:
                        s.append(self.subject)
                    else:
                        s.append(self.subject2)
                if pos % 4 == 2:
                    s.append(en.new_verb(new_word_syllables))
                if pos % 4 == 3:
                    s.append(en.new_adverb(new_word_syllables))

                pos += 1
            self.content.append(" ".join(s))

    def recite(self):
        for i in range(self.lines):
            print(self.content[i])
