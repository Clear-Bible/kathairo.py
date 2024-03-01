import sys
import csv
from pathlib import Path


def main():
    directory = Path(sys.argv[1])
    input_files = directory.glob("*reconstitution*.tsv")
    for input_file in input_files:
        rows = [r for r in csv.DictReader(input_file.open(), delimiter="\t")]
        verses = []
        parts = []
        last_verse = None
        for row in rows:
            this_verse = row["id"][0:8]
            if last_verse is None:
                last_verse = this_verse
                parts.append(f"{this_verse} ")

            if last_verse != this_verse:
                verses.append("".join(parts).strip())
                last_verse = this_verse
                parts = [f"{this_verse} "]

            parts.append(row["text"])
            if row["space_after"] == "n":
                continue
            parts.append(" ")
        verses.append("".join(parts).strip())

        output_file = input_file.parent / f"{input_file.stem}.txt"
        output_file.write_text("\n".join(verses))


if __name__ == "__main__":
    main()
