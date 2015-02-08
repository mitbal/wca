import sys
import matplotlib.pyplot as plt
from datetime import date
import glob
from skimage import io
import requests as req
import re


def read(filename):
    """ Read text file containing whatsapp chat and return the list of list of time, author, and its text
    :param filename: the filename of the chat text file
    :return: chat 2d list
    """
    chat = []
    with open(filename, 'r') as f:
        for line in f:
            lines = line.split(' - ')
            if len(lines) > 1:
                lines2 = lines[1].split(': ')
                if len(lines2) > 1:
                    speaker = lines2[0]
                    text = lines2[1]
                else:
                    speaker = ''
                    text = lines2[0]
                timestamp = lines[0]
            else:
                timestamp = ''
                speaker = ''
                text = lines[0]
            chat += [[timestamp, speaker, text]]
    return chat


def read_stopwords(filename):
    """ Read text file filled with stopwords
    :param filename: The text file where the stopwords reside
    :return: list of stopwords
    """
    stopwords = []
    with open(filename, 'r') as f:
        f.readline()
        f.readline()  # discard header
        for line in f:
            stopwords += [line.rstrip()]
    stopwords += ['<Media']
    stopwords += ['<media']
    stopwords += ['omitted>']  # whatsapp special word if there is image attached in the text
    return stopwords


def get_speaker_frequency(chat):
    frequency = {}
    for c in chat:
        speaker = c[1]
        if speaker == '':
            continue
        if c[1] not in frequency.keys():
            frequency[c[1]] = 1
        else:
            frequency[c[1]] += 1
    return frequency


def get_word_frequency(chat, stopwords):
    frequency = {}
    for c in chat:
        text = c[2]
        words = text.split()
        for word in words:
            word = word.lower()
            if word in stopwords:
                continue
            if word not in frequency.keys():
                frequency[word] = 1
            else:
                frequency[word] += 1

    dictionary = []
    for k in frequency.keys():
        dictionary += [(k, frequency[k])]

    dictionary.sort(key= lambda x: x[1], reverse=True)
    return dictionary


def plot_word_frequency(dictionary, k):
    labels = []
    freq = []
    for i in xrange(k):
        labels += [unicode(dictionary[i][0], 'ascii', 'ignore')]
        freq += [dictionary[i][1]]
    index = range(len(labels))
    plt.xkcd()
    fig = plt.figure()
    plt.bar(index, freq)
    plt.xticks([x+0.5 for x in index], labels)
    plt.xticks(rotation=45)
    fig.autofmt_xdate()
    plt.show()


def plot_speaker_frequency(frequency):
    labels = []
    freq = []
    for k in frequency.keys():
        labels += [unicode(k, 'ascii', 'ignore')]
        freq += [frequency[k]]
    index = range(len(labels))
    plt.xkcd()
    fig = plt.figure()
    plt.bar(index, freq)
    plt.xticks([x+0.5 for x in index], labels)
    plt.xticks(rotation=45)
    fig.autofmt_xdate()
    plt.show()


def get_emoji_frequency(emoji_unicode, emoji_utf8, chat):
    freq = {}
    for codepoint in emoji_unicode:
        freq[codepoint] = 0
    for c in chat:
        text = c[2]
        for i in xrange(len(emoji_utf8)):
            utf8 = emoji_utf8[i]
            codepoint = emoji_unicode[i]
            freq[codepoint] += len(re.findall(utf8, text))
    return freq


def plot_emoji_frequency(frequency, n):

    dictionary = []
    for k in frequency.keys():
        dictionary += [(k, frequency[k])]

    dictionary.sort(key=lambda x: x[1], reverse=True)

    plt.xkcd()
    fig = plt.figure()
    for i in xrange(n):
        im = io.imread('emoji/'+ dictionary[i][0] +'.jpg')
        fig.figimage(im, 230+i*75, 0)
    plt.bar(range(n), [x[1] for x in dictionary[:n]])
    plt.show()

months = {
    'Jan': 1,
    'Feb': 2,
    'Mar': 3,
    'Apr': 4,
    'May': 5,
    'Jun': 6,
    'Jul': 7,
    'Aug': 8,
    'Sep': 9,
    'Oct': 10,
    'Nov': 11,
    'Dec': 12
}


def convert_date(txt):
    start_date = txt.split(', ')
    start_month = months[start_date[0].split(' ')[0]]
    start_day = int(start_date[0].split(' ')[1])
    if len(start_date) > 2:
        start_year = int(start_date[1])
    else:
        start_year = date.today().year
    return date(start_year, start_month, start_day)


def convert_unicode(codepoint):
    dec = int(codepoint, 16)
    binary = bin(dec)[2:]
    while len(binary) < 21:
        binary = '0' + binary
    utf8 = '\\'+hex(int('11110' + binary[0:3], 2))[1:] + '\\'+ hex(int('10' + binary[3:9], 2))[1:] + '\\'+ hex(int('10' + binary[9:15], 2))[1:] \
           + '\\'+ hex(int('10' + binary[15:21], 2))[1:]
    return utf8

### End of method


### Start of main code
if len(sys.argv) < 1:
    print 'The usage is: python wca.py <filename>'

filename = sys.argv[1]
chat = read(filename)

# Date counting
start_date = convert_date(chat[0][0])
end_date = convert_date(chat[-1][0])
num_days = (end_date - start_date).days
print 'From:', start_date, 'to', end_date, 'total:', num_days, 'days'

# Number of lines
print 'Number of lines:', len(chat)
print 'Average per day:', len(chat) / num_days

# Speaker's frequency
frequency = get_speaker_frequency(chat)
for k in frequency.keys():
    print k, frequency[k]
plot_speaker_frequency(frequency)

# Word frequency
stopwords = read_stopwords('stopwords_id.txt')
dictionary = get_word_frequency(chat, stopwords)
for i in xrange(50):
    print dictionary[i][0], dictionary[i][1]
plot_word_frequency(dictionary, 30)

# Load emoji
emoji_unicode = []
emoji_utf8 = []
all_files = glob.glob('emoji/*.png')
for f in all_files:
    codepoint = f.split('\\')[1][:-4]
    emoji_unicode += [codepoint]
    utf8 = convert_unicode(codepoint)
    emoji_utf8 += [utf8]

frequency = get_emoji_frequency(emoji_unicode, emoji_utf8, chat)
for k in frequency.keys():
    print k, frequency[k]

plot_emoji_frequency(frequency, 20)

# Translate Indonesian text to English using Yandex translate API
translated_text = ''
index = 0
for c in chat:
    index += 1
    print 'chat ke:', index
    text = c[2]
    text = re.sub('%', '', text)
    r = req.get('https://translate.yandex.net/api/v1.5/tr.json/translate?key=trnsl.1.1.20150205T222339Z.64f03508b6f2088b.662c53df2c183b47f48e0436e75b106888ecd123&lang=id-en&text='+text)
    translated_text += ' ' + r.json()['text'][0]

f = open('translated.txt', 'w')
f.write(translated_text.encode('utf8')+'\n')
f.close()

# Analyze using MonkeyLearn Generic Topic Classifier
data = {'text': translated_text}
response = req.post(
    "https://api.monkeylearn.com/api/v1/categorizer/cl_5icAVzKR/classify_text/",
    data=data,
    headers={'Authorization': 'Token 0f584e47400267bc6118b1b4aa46c966b5b0e5df'}
)

print response.json()['result']
topics = response.json()['result']

prob = []
labels = []
for topic in topics:
    prob += [topic['probability']]
    labels += [topic['label']]

index = range(len(labels))
plt.xkcd()
fig = plt.figure()
plt.bar(index, prob)
plt.xticks([x+0.5 for x in index], labels)
plt.xticks(rotation=45)
fig.autofmt_xdate()
plt.show()
