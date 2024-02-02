from Tokenization import MaximalMatchingTokenizer
import os.path
import os
from typing import Optional
from pathlib import Path
#using System.Reflection;

#namespace ClearBible.Engine.Tokenization
#{
    # <summary>
    # A tokenizer for bible translations (not general Chinese translations, see below).
    # 
    # Chinese words and combination corrections provided by Andi Wu (andi.wu@globalbibleinitiative.org)
    # </summary>
class ChineseBibleWordTokenizer(MaximalMatchingTokenizer):
#{
    WORDS_FILE_NAME = "words.txt"
    COMBINATION_CORRECTIONS_FILE_NAME = "combination_corrections.txt"

    def __init__(self):#, chineseTokenizerDataDirectoryPath: Optional[str] = None, max_gram: Optional[int] = None): 
        #if max_gram is None:
        max_gram = 10
        super().__init__(max_gram)
   
        # set Words and overlaps.
        dataDirectoryFilePath = chineseTokenizerDataDirectoryPath 
        if dataDirectoryFilePath is None:
            #Path(__file__).parent / "Tokenization" / "Data" / "ChineseBibleWordTokenizer"
            wordsFilePath = os.path.join(os.getcwd,"Tokenization","Data","ChineseBibleWordTokenizer", WORDS_FILE_NAME)
            combinationsFilePath = os.path.join(os.getcwd,"Tokenization","Data","ChineseBibleWordTokenizer", COMBINATION_CORRECTIONS_FILE_NAME)
                       
        with open(wordsFilePath, "r", encoding='utf-8') as words_file:
            #lines = words_file.readlines()
            #for line in lines:
            #    if line is not "":
            #        super().Words.Add
                    
            self.Words.update(line.strip() for line in words_file if line.strip())

        with open(combinationsFilePath, "r", encoding='utf-8') as corrections_file:
            #lines = corrections_file.readlines()
            #for line in lines:
            #    parts = line.split("\t")
            #    if parts[0] not in super().CombinationCorrection:
            #        super().CombinationCorrection.Add(parts[0], parts[1])
            
            for line in corrections_file:
                parts = line.strip().split("\t")
                if parts[0] not in self.CombinationCorrections:
                    self.CombinationCorrections[parts[0]] = parts[1]
    #}
#}
#}