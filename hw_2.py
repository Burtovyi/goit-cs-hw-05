import re
import requests
from collections import Counter
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor

# Код реалізації MapReduce
def mapper(text):
    words = re.findall(r'\w+', text.lower())
    return Counter(words)

def reducer(counters):
    return sum(counters, Counter())

def map_reduce(data, mapper, reducer, num_workers=4):
    chunks = [data[i::num_workers] for i in range(num_workers)]
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        mapped = executor.map(mapper, chunks)
    reduced = reducer(mapped)
    return reduced

# Функція для візуалізації результатів
def visualize_top_words(counter, top_n=10):
    top_words = counter.most_common(top_n)
    words, counts = zip(*top_words)
    plt.bar(words, counts)
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.title('Top {} Words'.format(top_n))
    plt.xticks(rotation=45)
    plt.show()

# URL для завантаження тексту
url = "https://gutenberg.net.au/ebooks01/0100021.txt"

# Отримання тексту за URL
response = requests.get(url)
text = response.text

# Застосування MapReduce для аналізу частоти слів
word_count = map_reduce(text, mapper, reducer)

# Візуалізація топ-слів з найвищою частотою використання
visualize_top_words(word_count)
