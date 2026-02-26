import re
from pathlib import Path
from typing import List, Optional

from kathairo.parsing.sections.section_tree_builder import SectionTreeBuilder

_CHAPTER_RE = re.compile(r'^\\c\s+(\d+)')
_VERSE_RE = re.compile(r'^\\v\s+(\S+)')
_SECTION_RE = re.compile(r'^\\(ms\d*|s\d*)\s*(.*)')
_ANY_MARKER_RE = re.compile(r'^\\')


def scan_usfm_file(file_path: Path, book_num: int, encoding: str = "utf-8-sig") -> SectionTreeBuilder:
    """Scan a single USFM file and return a populated SectionTreeBuilder."""
    with open(file_path, "r", encoding=encoding) as f:
        text = f.read()
    builder = SectionTreeBuilder()
    _scan(text, book_num, builder)
    return builder


def _scan(text: str, book_num: int, builder: SectionTreeBuilder) -> None:
    current_chapter = 0
    pending_tag: Optional[str] = None
    pending_text_parts: List[str] = []

    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue

        m = _CHAPTER_RE.match(line)
        if m:
            _flush(builder, pending_tag, pending_text_parts)
            pending_tag = None
            pending_text_parts = []
            current_chapter = int(m.group(1))
            continue

        m = _VERSE_RE.match(line)
        if m:
            _flush(builder, pending_tag, pending_text_parts)
            pending_tag = None
            pending_text_parts = []
            # Normalize verse: strip ranges ("1-3"), suffixes ("1a"), etc.
            verse_str = re.split(r'[-a-zA-Z]', m.group(1))[0]
            try:
                builder.on_verse(book_num, current_chapter, int(verse_str))
            except ValueError:
                pass
            continue

        m = _SECTION_RE.match(line)
        if m:
            _flush(builder, pending_tag, pending_text_parts)
            pending_tag = m.group(1)
            pending_text_parts = [m.group(2).strip()]
            continue

        # Accumulate continuation lines for multi-line section headings.
        # Stop accumulating if a new marker begins.
        if pending_tag is not None:
            if _ANY_MARKER_RE.match(line):
                _flush(builder, pending_tag, pending_text_parts)
                pending_tag = None
                pending_text_parts = []
            else:
                pending_text_parts.append(line)

    _flush(builder, pending_tag, pending_text_parts)
    builder.finalize()


def _flush(builder: SectionTreeBuilder, tag: Optional[str], text_parts: List[str]) -> None:
    if tag is not None:
        text = ' '.join(p for p in text_parts if p)
        builder.on_section_heading(tag, text)
