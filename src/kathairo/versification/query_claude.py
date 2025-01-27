import anthropic
from machine.scripture import VerseRef
import kathairo.tsvs.tsv_corpus as TSV

client = anthropic.Anthropic()

get_mappings_prompt = """
Given verses from the Bible in its original languages (Biblical Hebrew, Koine Greek, and Aramaic) and verses from a translation of the Bible, please print out the mappings of which verses from the original and translation correspond to one another.

For example, given:

[Translation-A] And the dragon was enraged at the woman and went to make war with the rest of her children, who keep the commandments of God and hold to the testimony of Jesus. And the dragon stood on the shore of the sea.		
[Translation-B] Then I saw a beast with ten horns and seven heads rising out of the sea. There were ten royal crowns on its horns and blasphemous names on its heads.		
[Translation-C] The beast I saw was like a leopard, with the feet of a bear and the mouth of a lion. And the dragon gave the beast his power and his throne and great authority.		

[Original-D] Καὶ ὠργίσθη ὁ δράκων ἐπὶ τῇ γυναικὶ καὶ ἀπῆλθεν ποιῆσαι πόλεμον μετὰ τῶν λοιπῶν τοῦ σπέρματος αὐτῆς, τῶν τηρούντων τὰς ἐντολὰς τοῦ Θεοῦ καὶ ἐχόντων τὴν μαρτυρίαν Ἰησοῦ.		
[Original-E] Καὶ ἐστάθην ἐπὶ τὴν ἄμμον τῆς θαλάσσης
[Original-F] καὶ εἶδον ἐκ τῆς θαλάσσης Θηρίον ἀναβαῖνον, ἔχον κέρατα δέκα καὶ κεφαλὰς ἑπτά, καὶ ἐπὶ τῶν κεράτων αὐτοῦ δέκα διαδήματα καὶ ἐπὶ τὰς κεφαλὰς αὐτοῦ ὀνόματα βλασφημίας.

The printout should look like this:

[Translation-A]=[Original-D]
[Translation-A]=[Original-E]
[Translation-B]=[Original-F]

This is because [Original-E] maps to the second half of [Translation-A].  
Notice also how it's

[Translation-A]=[Original-D]
[Translation-A]=[Original-E]

and not

[Translation-A] = [Original-D], [Original-E]

This is because a mapping should only be between two verses.
If there are no mappings then print "No Mappings Found".  
Only map verses if they are the same verse.

Ensure that the translation's verse references are on the left of the mapping and the original's verse references are on the right.

Please do not elaborate, give any commentary, or introduce your answer.  Simply print out the mappings.
"""
   
def get_corrected_mappings_for_missing_source_verse(source_verse, tsv_path):

    if(int(source_verse)<40001001):
        original_df = TSV.load_tsv_to_corpus("src/kathairo/tsvs/verse_WLC.tsv")
    else:
        original_df = TSV.load_tsv_to_corpus("src/kathairo/tsvs/verse_GNT.tsv")
        
    translation_df = TSV.load_tsv_to_corpus(tsv_path)
    
    preceding_source_verse = TSV.get_preceding_id(original_df, source_verse)
    following_source_verse = TSV.get_following_id(original_df, source_verse)
    
    preceding_original_text = TSV.get_text_from_tsv(original_df, preceding_source_verse)
    current_original_text = TSV.get_text_from_tsv(original_df, source_verse)
    following_original_text = TSV.get_text_from_tsv(original_df, following_source_verse)
  
    preceding_id = TSV.get_id_from_source_verse(translation_df, preceding_source_verse)
    following_id = TSV.get_id_from_source_verse(translation_df, following_source_verse)
    
    preceding_translation_text = TSV.get_text_from_tsv(translation_df, preceding_id)
    following_translation_text = TSV.get_text_from_tsv(translation_df, following_id)
    
    tag_to_id_dictionary = {
        "[Translation-A]": preceding_id,
        "[Translation-B]": following_id,
        "[Original-C]": preceding_source_verse,
        "[Original-D]": source_verse,
        "[Original-E]": following_source_verse,
    }
    
    input = f"""
    [Translation-A] {preceding_translation_text}
    [Translation-B] {following_translation_text}

    [Original-C] {preceding_original_text}
    [Original-D] {current_original_text}
    [Original-E] {following_original_text}
    """

    message = client.messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=1000,
        temperature=0,
        system=get_mappings_prompt,
        messages=[
            {
                "role": "user",
                "content": [{"type": "text", "text": input}],
            }
        ],
    )
    
    mappings_list = []
    for mapping in message.content[0].text.splitlines():
        translation, original = mapping.split('=')
        translation_verse_ref = VerseRef.from_bbbcccvvv(int(tag_to_id_dictionary[translation]))
        original_verse_ref = VerseRef.from_bbbcccvvv(int(tag_to_id_dictionary[original]))
        mappings_list.append((translation_verse_ref.__str__(), original_verse_ref.__str__()))
    
    return mappings_list
    
print(get_corrected_mappings_for_missing_source_verse("18034037"))