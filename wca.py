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
                    text = lines2
                timestamp = lines[0]
            else:
                timestamp = ''
                speaker = ''
                text = lines[0]
            chat += [[timestamp, speaker, text]]
    return chat

def get_speaker_frequency(chat):
    frequency = {}
    for c in chat:
        if c[1] not in frequency.keys():
            frequency[c[1]] = 1
        else:
            frequency[c[1]] += 1
    return frequency

if len(sys.argv) < 1:
    print 'The usage is: python wca.py <filename>'

filename = sys.argv[1]
chat = read(filename)

# Number of lines
print 'Number of lines:', len(chat)

frequency = get_speaker_frequency(chat)
labels = []
freq = []
for k in frequency.keys():
    print k, frequency[k]
    labels += [k]
    freq += [frequency[k]]
