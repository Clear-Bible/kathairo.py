import csv
from pathlib import Path

def reconstitute(tsv_file_path:Path):
    #directory = Path(sys.argv[1])
    #input_files = directory.glob("*reconstitution*.tsv")
    input_files = [Path(tsv_file_path)]
    for input_file in input_files:
        rows = [r for r in csv.DictReader(input_file.open("r", encoding='utf-8'), delimiter="\t")]
        verses = []
        verses.append(["id", "text"])
        text = ""
        parts = []
        last_verse = None
        for row in rows:
            this_verse = row["id"][0:8]
            if last_verse is None:
                last_verse = this_verse
                parts.append(f"{this_verse}")

            if last_verse != this_verse:
                parts.append(text)
                verses.append(parts)#.strip()
                
                last_verse = this_verse
                
                text = ""
                parts = [f"{this_verse}"]#[f""]#

            text+=(row["text"])
            if row["skip_space_after"] == "y":
                continue
            text+=(" ")
        parts.append(text)
        verses.append(parts)#.strip()

        output_file = input_file.parent.parent.parent / "test" /"reconstituted" / f"{input_file.stem}_reconstitution.tsv"
        
        with open(output_file, 'w', newline='', encoding='utf-8') as out_file:
            tsv_writer = csv.writer(out_file, delimiter='\t')

            tsv_writer.writerows(verses) #OLD WAY