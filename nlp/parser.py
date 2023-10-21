from lexicon import Lexicon
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

from lexicon import Lexicon  # Import the Lexicon class

# Create an instance of the Lexicon class
lexicon_instance = Lexicon()

Dune = """
    Muad'Dib learned rapidly because his first training was in how to learn.
    And the first lesson of all was the basic trust that he could learn.
    It's shocking to find how many people do not believe they can learn,
    and how many more believe learning to be difficult."""

# Tokenize the text
print(lexicon_instance.tokenize(Dune))

worf_quote = "Sir, I protest. I am not a merry man!"
words_in_quote = lexicon_instance.tokenize(worf_quote)

print(words_in_quote)

# Access the 'stops' dictionary from the Lexicon instance
stop_words = lexicon_instance.vocab["stops"]

filtered_list = []

for word in words_in_quote:
    if word[0] not in stop_words:
        filtered_list.append(word)

print(filtered_list)

