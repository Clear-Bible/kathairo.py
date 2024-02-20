import csv
from machine.utils import string_utils
from machine.corpora import UsxFileTextCorpus
from machine.corpora import ParatextTextCorpus, UsfmFileTextCorpus, UsxFileTextCorpus
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

import os
from machine.corpora import ParatextTextCorpus
from machine.corpora import AlignedWordPair

from machine.translation import word_align_corpus
from machine.translation.thot import ThotIbm1WordAlignmentModel
from machine.translation import SymmetrizationHeuristic
from machine.translation.thot import ThotWordAlignmentModelTrainer, ThotWordAlignmentModelType
from machine.translation import SymmetrizedWordAlignmentModelTrainer
from machine.translation import SymmetrizationHeuristic
from machine.translation.thot import ThotSymmetrizedWordAlignmentModel

source_corpus = ParatextTextCorpus("data/VBL-PT")
target_corpus = ParatextTextCorpus("data/WEB-PT")
parallel_corpus = source_corpus.align_rows(target_corpus).tokenize(LatinWordTokenizer())







aligned_corpus = word_align_corpus(parallel_corpus.lowercase())
for row in aligned_corpus.take(5):
    print("Source:", row.source_text)
    print("Target:", row.target_text)
    print("Alignment:", AlignedWordPair.to_string(row.aligned_word_pairs, include_scores=False))




aligned_corpus = word_align_corpus(parallel_corpus.lowercase(), aligner="ibm1")
for row in aligned_corpus.take(5):
    print("Source:", row.source_text)
    print("Target:", row.target_text)
    print("Alignment:", AlignedWordPair.to_string(row.aligned_word_pairs, include_scores=False))









model = ThotIbm1WordAlignmentModel()
trainer = model.create_trainer(parallel_corpus.lowercase())
trainer.train(lambda status: print(f"Training IBM-1 model: {status.percent_completed:.2%}"))
trainer.save()








os.makedirs("out/VBL-WEB-IBM1", exist_ok=True)
trainer = ThotWordAlignmentModelTrainer(
    ThotWordAlignmentModelType.IBM1, parallel_corpus.lowercase(), "out/VBL-WEB-IBM1/src_trg"
)

trainer.train(lambda status: print(f"Training IBM-1 model: {status.percent_completed:.2%}"))
trainer.save()
print("IBM-1 model saved")







model = ThotIbm1WordAlignmentModel("out/VBL-WEB-IBM1/src_trg")
for row in parallel_corpus.lowercase().take(5):
    alignment = model.align(row.source_segment, row.target_segment)

    print("Source:", row.source_text)
    print("Target:", row.target_text)
    print("Alignment:", str(alignment))





segment_batch = list(parallel_corpus.lowercase().take(5))
alignments = model.align_batch(segment_batch)

for (source_segment, target_segment), alignment in zip(segment_batch, alignments):
    print("Source:", " ".join(source_segment))
    print("Target:", " ".join(target_segment))
    print("Alignment:", str(alignment))






model = ThotIbm1WordAlignmentModel("out/VBL-WEB-IBM1/src_trg")
prob = model.get_translation_probability("es", "is")
print(f"es -> is: {prob:.4f}")
prob = model.get_translation_probability(None, "that")
print(f"NULL -> that: {prob:.4f}")






segment_batch = list(parallel_corpus.lowercase().take(5))
alignments = model.align_batch(segment_batch)

for (source_segment, target_segment), alignment in zip(segment_batch, alignments):
    print("Source:", " ".join(source_segment))
    print("Target:", " ".join(target_segment))
    print("Score:", round(model.get_avg_translation_score(source_segment, target_segment, alignment), 4))










src_trg_trainer = ThotWordAlignmentModelTrainer(
    ThotWordAlignmentModelType.IBM1, parallel_corpus.lowercase(), "out/VBL-WEB-IBM1/src_trg"
)
trg_src_trainer = ThotWordAlignmentModelTrainer(
    ThotWordAlignmentModelType.IBM1, parallel_corpus.invert().lowercase(), "out/VBL-WEB-IBM1/trg_src"
)
symmetrized_trainer = SymmetrizedWordAlignmentModelTrainer(src_trg_trainer, trg_src_trainer)
symmetrized_trainer.train(lambda status: print(f"{status.message}: {status.percent_completed:.2%}"))
symmetrized_trainer.save()
print("Symmetrized IBM-1 model saved")








src_trg_model = ThotIbm1WordAlignmentModel("out/VBL-WEB-IBM1/src_trg")
trg_src_model = ThotIbm1WordAlignmentModel("out/VBL-WEB-IBM1/trg_src")
symmetrized_model = ThotSymmetrizedWordAlignmentModel(src_trg_model, trg_src_model)
symmetrized_model.heuristic = SymmetrizationHeuristic.GROW_DIAG_FINAL_AND

segment_batch = list(parallel_corpus.lowercase().take(5))
alignments = symmetrized_model.align_batch(segment_batch)

for (source_segment, target_segment), alignment in zip(segment_batch, alignments):
    print("Source:", " ".join(source_segment))
    print("Target:", " ".join(target_segment))
    print("Alignment:", alignment)






import time
start_time=time.time()
#do something

from machine.corpora import ParatextTextCorpus
from machine.tokenization import LatinWordTokenizer

sourceVersification = Versification(name = "sourceVersification", base_versification=ENGLISH_VERSIFICATION)
targetVersification = Versification(name = "targetVersification", base_versification=ENGLISH_VERSIFICATION)

source_corpus = UsfmFileTextCorpus("./resources/bsb_usfm", versification = sourceVersification)
target_corpus = UsfmFileTextCorpus("./resources/arb-vd_usfm", versification = targetVersification)

parallel_corpus = source_corpus.align_rows(target_corpus).tokenize(LatinWordTokenizer())

from machine.translation import word_align_corpus
from machine.corpora import AlignedWordPair

aligned_corpus = word_align_corpus(parallel_corpus.lowercase())
#aligned_corpus = word_align_corpus(parallel_corpus.lowercase(), aligner="ibm1")

end_time=time.time()-start_time

for row in aligned_corpus.take(5):
    print("Source:", row.source_text)
    print("Target:", row.target_text)
    print("Alignment:", AlignedWordPair.to_string(row.aligned_word_pairs, include_scores=False))