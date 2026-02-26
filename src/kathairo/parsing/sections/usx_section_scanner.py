import re
import xml.etree.ElementTree as ET
from pathlib import Path

from kathairo.parsing.sections.section_tree_builder import SectionTreeBuilder

_SECTION_STYLE_RE = re.compile(r'^(ms\d*|s\d*)$')


def scan_usx_file(file_path: Path, book_num: int) -> SectionTreeBuilder:
    """Scan a single USX file and return a populated SectionTreeBuilder."""
    builder = SectionTreeBuilder()
    with open(file_path, "r", encoding="utf-8") as f:
        tree = ET.parse(f)
    _scan(tree.getroot(), book_num, builder)
    return builder


def _scan(root: ET.Element, book_num: int, builder: SectionTreeBuilder) -> None:
    current_chapter = 0

    for child in root:
        if child.tag == 'chapter':
            # Chapter end elements have 'eid'; chapter start elements have 'number'.
            if 'eid' in child.attrib:
                continue
            num_str = child.get('number', '')
            if not num_str:
                continue
            try:
                current_chapter = int(num_str)
            except ValueError:
                pass

        elif child.tag == 'para':
            style = child.get('style', '')
            if _SECTION_STYLE_RE.match(style):
                text = ''.join(child.itertext()).strip()
                builder.on_section_heading(style, text)
            else:
                # Scan for verse elements inside verse paragraphs.
                for verse_elem in child.iter('verse'):
                    if 'eid' in verse_elem.attrib:
                        continue
                    verse_str = verse_elem.get('number', '').split('-')[0]
                    try:
                        builder.on_verse(book_num, current_chapter, int(verse_str))
                    except ValueError:
                        pass

    builder.finalize()
