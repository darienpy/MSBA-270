def count_letters(text):
    letter_counts = { }
    for letter in text:
        if letter in letter_counts:
            letter_counts[letter] += 1
        else:
            letter_counts[letter] = 1
    return letter_counts
dict2 = {}
text = str("Pear")
dict2[text] = 5
print(dict2)
print