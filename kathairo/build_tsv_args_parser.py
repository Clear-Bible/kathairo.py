from Tokenization import ChineseBibleWordTokenizer
from Tokenization.latin_whitespace_included_tokenizer import LatinWhitespaceIncludedWordTokenizer
from machine.corpora import UsxFileTextCorpus
from machine.corpora import UsfmFileTextCorpus, UsxFileTextCorpus
from machine.tokenization import LatinWordTokenizer, WhitespaceTokenizer
from machine.scripture import (
    ORIGINAL_VERSIFICATION,
    Versification,
)
import argparse
import build_tsv

argumentParser = argparse.ArgumentParser()

#add a parameter for source versification

argumentParser.add_argument("-n", "--projectName", type=str, required=True)

#add bunch of parameters for the default versification schemes included in machine and make target versification a mutually exclusive argument group
argumentParser.add_argument("-tv", "--targetVersificationPath", type=str, required=True)

corpusGroup = argumentParser.add_mutually_exclusive_group(required=True)
corpusGroup.add_argument("-uf", "--targetUsfmCorpusPath", type=str)
corpusGroup.add_argument("-ux", "--targetUsxCorpusPath", type=str)

tokenizerGroup = argumentParser.add_mutually_exclusive_group(required=True)
tokenizerGroup.add_argument("-zh", "--chineseTokenizer", action='store_true')
tokenizerGroup.add_argument("-lt", "--latinTokenizer", action='store_true')
tokenizerGroup.add_argument("-lw", "--latinWhiteSpaceIncludedTokenizer", action='store_true')

argumentParser.add_argument("-of", "--oldTsvFormat", action='store_true') #optional

args = argumentParser.parse_args()

#print(args.targetVersificationPath)
#print(args.targetUsfmCorpusPath)
#print(args.targetUsxCorpusPath)
#print(args.chineseTokenizer)
#print(args.latinTokenizer)
#print(args.oldTsvFormat)

projectName = args.projectName

sourceVersification = Versification(name = "sourceVersification", base_versification=ORIGINAL_VERSIFICATION)

targetVersification = Versification.load(args.targetVersificationPath, fallback_name="web")

if(args.targetUsfmCorpusPath is not None):
    corpus = UsfmFileTextCorpus(args.targetUsfmCorpusPath, versification = targetVersification)
if(args.targetUsxCorpusPath is not None):
    corpus = UsxFileTextCorpus(args.targetUsxCorpusPath, versification = targetVersification)

if(args.chineseTokenizer == True):
    tokenizer = ChineseBibleWordTokenizer.ChineseBibleWordTokenizer()
if(args.latinTokenizer == True):
    tokenizer = LatinWordTokenizer(treat_apostrophe_as_single_quote=True)
if(args.latinWhiteSpaceIncludedTokenizer == True):
    tokenizer = LatinWhitespaceIncludedWordTokenizer(treat_apostrophe_as_single_quote=True)

#build_tsv.corpus_to_verse_level_tsv
#build_tsv.corpus_to_word_level_tsv
build_tsv.corpus_to_word_level_tsv(targetVersification = targetVersification, 
                                    sourceVersification = sourceVersification, 
                                    corpus = corpus, 
                                    tokenizer = tokenizer, 
                                    project_name = projectName, 
                                    use_old_tsv_format = args.oldTsvFormat)    