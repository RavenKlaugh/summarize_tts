from gtts import gTTS
from io import BytesIO

summary = '''
{"summary":"During the administration of the French East India Company (until 1767) and subsequent French rule at least 12,000 workers arrived from India between 1721 and 1810. The descendants of these indentured labourers make up two-thirds of the island's current population. Between 1834 and 1920, nearly 700,000 Indian indentured laborers arrived at Aapravasi ghat."}
'''

text = '''During the administration of the French East India Company (until 1767) and subsequent French rule at least 12,000 workers arrived from India between 1721 and 1810 before the abolition of slavery. These first Indian immigrants came from various parts of India such as Pondicherry, Karikal, Yanaon, Bengal and others. They worked under contract as skilled stonemasons, blacksmiths, and carpenters although hundreds of them were slaves.[3][4] After the legislative changes of 1767 these Indian immigrants were allowed to start businesses, buy land and own slaves.[5]

Following the November 1810 British Invasion from the northern coast, the island came under British rule. With the liberation of about 65,000 African and Malagasy slaves after the 1833 abolition of slavery the Franco-Mauritian plantation owners and sugar oligarchs resorted to indentured labourers, or Coolies, from various parts of India to work in their fields. Between 1834 and 1920, nearly 700,000 Indian indentured laborers arrived at Aapravasi ghat, an embankment located in the harbor of Port-Louis.[6] Mauritius thus became the British colony's largest recipient of indentured migrants.[7] Indentured labourers were mostly brought from the Bhojpuri speaking regions of Bihar and Uttar Pradesh, with a large number of Tamils, Telugus and Marathis amongst them. The descendants of these indentured labourers make up two-thirds of the island's current population.[7]

As free immigrants, these later arrivals were commonly employed by the British in the armed forces, police forces, as security personnel with a substantial portion of immigrants from Gujarat and Sindh arriving as traders, businessmen, and merchants.

In the late 19th to early 20th century, Chinese men in Mauritius married Indian women due to both a lack of Chinese women and the higher numbers of Indian women on the island.[8][9][10] The 1921 census in Mauritius counted that Indian women there had a total of 148 children fathered by Chinese men.[11][12][13] These Chinese were mostly traders.[14]

Demographics'''


'''tatue in 1896, Bamiyan\nAfter statue destroyed by Islamist Taliban in 2001\nBuddhas of Bamiyan, Afghanistan in 1896 (top) and after destruction in 2001 by the Taliban Islamists.\nBu also had a foothold to some exten'''

'''kkha is one of the three marks of existence, along with impermanence and anatt (non-self).Dhyna is "state of perfect equanimity and awareness (upekkh-sati-parisuddhi)," reached through focused mental training.\n\nThe practice of dhyna aids in maintaining a calm mind, and avoiding disturbance of this calm mind by mindfulness of disturbing thoughts and feelings.[note 21]\n\nOrigins\nThe earliest evidence of yogis and their meditative tradition, states Karel Werner, is found in the Kein hymn 10.136 of the Rigveda.Antman and nyat\n The Five Aggregates (paca khandha)\naccording to the Pali Canon.\n \n \nform (rpa)\n 4 elements\n(mahbhta) \n \n  \n  contact\n(phassa)\n    \n \nconsciousness\n(vina)\n \n \n \n \n \n\n\n \n \n \n\n mental factors (cetasika)While evidence suggests meditation was practised in the centuries preceding the Buddha, the meditative methodologies described in the Buddhist texts are some of the earliest among texts that have survived into the modern era.Samsara end'''

import requests

url = "https://tldrthis.p.rapidapi.com/v1/model/abstractive/summarize-text/"

payload = {
	"text": text,
	"min_length": 100,
	"max_length": 300
}
headers = {
	"content-type": "application/json",
	"X-RapidAPI-Key": "f2be327b35mshd202d55375dbea6p14d31ajsn0fe9ce978bfe",
	"X-RapidAPI-Host": "tldrthis.p.rapidapi.com"
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)



mp3_fp = BytesIO()
tts = gTTS(response.text, lang='en')
tts.write_to_fp(mp3_fp)
tts.save('Mauritians.mp3')
# Load `mp3_fp` as an mp3 file in
# the audio library of your choice






'''
import wave
import sys
from pydub import AudioSegment
#sound = AudioSegment.from_mp3(sys.argv[1])
#sound.export("file.wav", format="wav")


import soundfile as sf
import pyrubberband as pyrb
#y, sr = sf.read("file.wav")
y, sr = sf.read(mp3_fp)
# Play back at 1.5X speed
y_stretch = pyrb.time_stretch(y, sr, 1.5)
# Play back two 1.5x tones
y_shift = pyrb.pitch_shift(y, sr, 1.5)
sf.write("analyzed_filepathX105.wav", y_stretch, sr, format='wav')
'''


import string
import re
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

def scrub_then_summarize(text, per):
    text.replace('\n', '')
    text_scrubbed = re.sub('\[\d*\]', '', text)
    print(text_scrubbed)
    return per

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