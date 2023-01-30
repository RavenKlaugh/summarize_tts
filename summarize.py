import sys
from gtts import gTTS
import os
import re
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

def scrub_then_summarize(text, per):
    # throw away non-ascii stuff
    text = re.sub(r'[^\x00-\x7F]+','', text)
    # remove newline and \n string lits 
    text = text.replace('\n', ' ')
    text = text.replace('\\n', '')
    # remove footnote numbers like [31]
    text = re.sub('\[\d*\]', '', text)
    # remove [note 31], [web 31] and the like
    text = re.sub('\[(note|web) \d*\]', '', text)
    scrubed_then_summarized = summarize(text, per)
    return scrubed_then_summarized

def summarize(text, per):
    nlp = spacy.load('en_core_web_sm')
    doc= nlp(text)
    tokens=[token.text for token in doc]
    word_frequencies={}
    for word in doc:
        if word.text.lower() not in list(STOP_WORDS):
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1
    max_frequency=max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word]=word_frequencies[word]/max_frequency
    sentence_tokens= [sent for sent in doc.sents]
    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():                            
                    sentence_scores[sent]=word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent]+=word_frequencies[word.text.lower()]
    select_length=int(len(sentence_tokens)*per)
    summary=nlargest(select_length, sentence_scores,key=sentence_scores.get)
    final_summary=[word.text for word in summary]
    summary=''.join(final_summary)
    return summary 



# Check if a command line argument was provided
if len(sys.argv) < 3:
    print("Please provide a input text file and a summary percent target")
    print("Usage: summarize.py input.txt 0.05")
    sys.exit(1)

# add checks and try/catch for args


f = open(sys.argv[1], "r")
text_from_file = f.read()
input_wordcount = len(text_from_file.strip().split(" "))
summary = scrub_then_summarize(text_from_file, float(sys.argv[2]))
summary_wordcount = len(summary.strip().split(" "))
summary_compression = summary_wordcount/input_wordcount



print('input: \n' + text_from_file)
for n in range(4):
    print('----------')
print('output: ')
print(summary)

print('Input word count: {0}\nOutput word count: {1}\nCompression ratio: {2:.2f}'.format(input_wordcount, summary_wordcount, summary_compression))




#TTS Section

from gtts import gTTS
import datetime

now = datetime.datetime.now()
filename = 'summary' + now.strftime("%Y%m%d%H%M") + '.mp3'

tts = gTTS(text=summary, lang='en')
tts.save("summarygtts.mp3")

