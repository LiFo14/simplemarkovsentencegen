"""Simple Markov chain sentence generator

This script allows the user to get sentence generated with algorithm based on Markov chains.
"""
import random
import re


def analyze(src: str, random_start_word: bool = False) -> dict:
    """Raw data analyzer

    :param src: source data
    :type src: str
    :param random_start_word: flag to determine whether or not first
        word should be random (default is False)
    :type random_start_word: bool
    :returns: a dict with analysis result
    :rtype: dict
    """
    src = re.sub(r'[^\w\s]', '', src.lower())
    words = src.split(' ')
    analyzed_words = dict() if random_start_word else {'START': words[0]}

    for index, word in enumerate(words):
        if index != len(words) - 1:
            next_words = {words[index + 1]: words.count(words[index + 1])}
        else:
            next_words = {'END': 1}

        if word in analyzed_words:
            analyzed_words[word].update(next_words)
        else:
            analyzed_words[word] = next_words
    return analyzed_words


def generate_sentence(data: str, random_start_word: bool = False) -> str:
    """Construct sentence from analyzed data

    :param data: a string of data to generate sentence from
    :type data: str
    :param random_start_word: flag to determine whether or not first
        word should be random (default is False)
    :type random_start_word: bool
    :returns: generated string
    :rtype: str
    """
    words = analyze(data, random_start_word=random_start_word)
    sentence = random.choice(list(words.keys())) if random_start_word else words.pop('START')
    while words:
        last_word = sentence.split(' ')[-1]
        next_words = words[last_word]
        if len(set(next_words.values())) == 1:
            # any random key from dict
            next_word = random.choice(list(next_words.keys()))
        else:
            # the most possible value
            next_word = random.choice([x for x in next_words for _ in range(next_words[x])])

        if next_word == 'END':
            break
        else:
            sentence += ' ' + next_word

    return sentence


if __name__ == '__main__':
    while True:
        is_random = input('Should sentence\'s start word be random? (y/N): ').lower()
        if is_random == 'y':
            random_start = True
            break
        elif is_random == 'n':
            random_start = False
            break

    data = input('Enter source data: ')
    print(generate_sentence(data, random_start_word=random_start))
