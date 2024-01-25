import csv
from machine.utils import string_utils
from machine.corpora import UsxFileTextCorpus
from machine.corpora import ParatextTextCorpus, UsfmFileTextCorpus
from machine.tokenization import LatinWordTokenizer, WhitespaceTokenizer
from machine.scripture import (
    ENGLISH_VERSIFICATION,
    ORIGINAL_VERSIFICATION,
    RUSSIAN_ORTHODOX_VERSIFICATION,
    RUSSIAN_PROTESTANT_VERSIFICATION,
    SEPTUAGINT_VERSIFICATION,
    VULGATE_VERSIFICATION,
    LAST_BOOK,
    ValidStatus,
    VerseRef,
    Versification,
    get_bbbcccvvv,
)

versification = Versification.load("./resources/versification/eng.vrs", fallback_name="web")
#versification = Versification(ENGLISH_VERSIFICATION)

#point to a folder full of .SFM files (cannot be .usfm)
corpus = UsfmFileTextCorpus("./resources/arb-vd_usfm", versification=versification)

tokenizer = LatinWordTokenizer()
with open('output.tsv', 'w', newline='', encoding='utf-8') as out_file:
    tsv_writer = csv.writer(out_file, delimiter='\t')
    tsv_writer.writerow(["id", "target_verse", "token"])

    for row in corpus.tokenize(tokenizer).lowercase().nfc_normalize():    
        
        #print(f"{row.ref}: {row.text}")

        vref = VerseRef.from_bbbcccvvv(row.ref.bbbcccvvv, ENGLISH_VERSIFICATION) #dependent on .vrs being used
        vref.change_versification(ORIGINAL_VERSIFICATION)
        
        wordIndex = 1
        for token in row.segment:
            wordIndexStr = str(wordIndex).zfill(3)
            tsv_writer.writerow([f" {vref.bbbcccvvvs}{wordIndexStr}", f"{row.ref.bbbcccvvvs}", token ])
            wordIndex += 1

#What punctuation data can we get from machine?
    #a tokenized verse is just returned as an array so there's no accompanying data to signify that a token is punctuation. 
    #there is a is_punctuation method we could use though
#Is there USFM validation?
    #I don't seen any tools for it, and when I fed it USFM with faulty and duplicate verses it just ignored the errors
#What kind of versification data can we get to enrich the current alignment data structures?
    #VerseRef.change_versification, which translates a verse ref into it's equivalent in another versification scheme
    #various tools of comparing verses from different versification (equality, >, <)
            

#rename Project
#publish to GitHub
#scripture burrito alignment format

"""

for text in corpus.texts:
    print(text.id)
    print("======")
    for row in text.take(3):
        verse_ref = row.ref
        chapter_verse = f"{verse_ref.chapter}:{verse_ref.verse}"
        print(f"{chapter_verse}: {row.text}")
    print()

"""