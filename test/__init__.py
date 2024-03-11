from lxml import etree
import csv

__macula_greek_tsv_rows__ = []

tsv_path = "../TSVs/target_BSB_new.tsv"
__tsv_files__ = [tsv_path]

with open(tsv_path, encoding='utf-8') as file:
    reader = csv.DictReader(file, delimiter="\t")
    for row in reader:
        __macula_greek_tsv_rows__.append(row)