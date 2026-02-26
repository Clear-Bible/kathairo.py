import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Optional

from machine.scripture.canon import ALL_BOOK_IDS

from kathairo.parsing.sections.usfm_section_scanner import scan_usfm_file
from kathairo.parsing.sections.usx_section_scanner import scan_usx_file


def _book_abbr_to_num(book_abbr: str) -> int:
    """Return 1-based book number, or 0 if not found."""
    try:
        return ALL_BOOK_IDS.index(book_abbr) + 1
    except ValueError:
        return 0


def build_section_trees_usfm(
    corpus_path: str,
    project_name: str,
    output_dir: str,
    file_pattern: str = "*.SFM",
    encoding: str = "utf-8-sig",
) -> None:
    """Scan all USFM files in corpus_path and write per-book section XML files."""
    for file_path in sorted(Path(corpus_path).glob(file_pattern)):
        book_abbr = _get_usfm_book_id(file_path, encoding)
        if not book_abbr:
            continue
        book_num = _book_abbr_to_num(book_abbr)
        if book_num <= 0:
            continue
        builder = scan_usfm_file(file_path, book_num, encoding)
        builder.write_xml(book_num, book_abbr, project_name, output_dir)


def build_section_trees_usx(
    corpus_path: str,
    project_name: str,
    output_dir: str,
) -> None:
    """Scan all USX files in corpus_path and write per-book section XML files."""
    for file_path in sorted(Path(corpus_path).glob("*.usx")):
        book_abbr = _get_usx_book_id(file_path)
        if not book_abbr:
            continue
        book_num = _book_abbr_to_num(book_abbr)
        if book_num <= 0:
            continue
        builder = scan_usx_file(file_path, book_num)
        builder.write_xml(book_num, book_abbr, project_name, output_dir)


def _get_usfm_book_id(file_path: Path, encoding: str) -> Optional[str]:
    try:
        with open(file_path, "r", encoding=encoding) as f:
            for line in f:
                line = line.strip()
                if line.startswith("\\id "):
                    id_part = line[4:]
                    idx = id_part.find(" ")
                    if idx != -1:
                        id_part = id_part[:idx]
                    return id_part.strip().upper() or None
    except Exception:
        pass
    return None


def _get_usx_book_id(file_path: Path) -> Optional[str]:
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        book_elem = root.find('.//book')
        if book_elem is not None:
            code = book_elem.get('code', '').strip().upper()
            return code or None
    except Exception:
        pass
    return None
