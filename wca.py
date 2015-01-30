import sys
import matplotlib.pyplot as plt

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

if len(sys.argv) < 1:
    print 'The usage is: python wca.py <filename>'

filename = sys.argv[1]
chat = read(filename)

# Number of lines
print 'Number of lines:', len(chat)

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
