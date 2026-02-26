import os
import re
import xml.etree.ElementTree as ET
from typing import List, Optional, Tuple

_SECTION_TAG_RE = re.compile(r'^(ms\d*|s\d*)$')


def is_section_tag(tag: str) -> bool:
    return bool(_SECTION_TAG_RE.match(tag))


def _tag_sort_key(tag: str) -> Tuple[int, int]:
    """Returns (type_key, level). Lower = higher in hierarchy (closer to root).

    ms* tags have type_key 0; s* tags have type_key 1.
    Unnumbered ms/s are treated as level 1 for sorting purposes only;
    the original tag string is preserved in the output.
    """
    if tag.startswith('ms'):
        suffix = tag[2:]
        return (0, int(suffix) if suffix else 1)
    if tag.startswith('s'):
        suffix = tag[1:]
        return (1, int(suffix) if suffix else 1)
    return (2, 0)


def make_word_id(bbb: int, ccc: int, vvv: int) -> str:
    return f"{bbb:03d}{ccc:03d}{vvv:03d}001"


class _SectionNode:
    def __init__(self, tag: str, text: str) -> None:
        self.tag = tag
        self.text = text
        self.range_start: Optional[str] = None
        self.range_end: Optional[str] = None
        self.children: List['_SectionNode'] = []

    def to_xml(self) -> ET.Element:
        attribs = {'text': self.text}
        if self.range_start is not None:
            attribs['range_start'] = self.range_start
        if self.range_end is not None:
            attribs['range_end'] = self.range_end
        elem = ET.Element(self.tag, attribs)
        for child in self.children:
            elem.append(child.to_xml())
        return elem


class SectionTreeBuilder:
    """Builds a nested XML section tree from ms and s USFM/USX markers.

    Call on_section_heading() when an ms/s heading is encountered.
    Call on_verse() when a verse begins.
    Call write_xml() (which calls finalize() internally) when the book is done.

    Range semantics:
      range_start = first word ID (word 001) of the first verse after the heading.
      range_end   = first word ID of the last verse before the next same-or-higher
                    section, or the last verse of the book for terminal sections.
    """

    def __init__(self) -> None:
        self._roots: List[_SectionNode] = []
        self._open_stack: List[Tuple[Tuple[int, int], _SectionNode]] = []
        self._pending_start: List[_SectionNode] = []
        self._last_verse_id: Optional[str] = None

    def on_section_heading(self, tag: str, text: str) -> None:
        """Call when an ms/s section heading marker is encountered."""
        new_key = _tag_sort_key(tag)

        # Close sections at the same or deeper nesting level.
        # When a section closes, its range_end = last verse seen before this heading.
        while self._open_stack and self._open_stack[-1][0] >= new_key:
            _, node = self._open_stack.pop()
            if node.range_end is None:
                node.range_end = self._last_verse_id

        new_node = _SectionNode(tag=tag, text=text.strip())

        if self._open_stack:
            self._open_stack[-1][1].children.append(new_node)
        else:
            self._roots.append(new_node)

        self._open_stack.append((new_key, new_node))
        self._pending_start.append(new_node)

    def on_verse(self, bbb: int, ccc: int, vvv: int) -> None:
        """Call when a new verse begins. Resolves any pending range_starts."""
        word_id = make_word_id(bbb, ccc, vvv)
        for node in self._pending_start:
            node.range_start = word_id
        self._pending_start.clear()
        self._last_verse_id = word_id

    def finalize(self) -> None:
        """Close all open sections at end of book."""
        self._pending_start.clear()
        for _, node in self._open_stack:
            if node.range_end is None:
                node.range_end = self._last_verse_id
        self._open_stack.clear()

    def write_xml(self, book_num: int, book_abbr: str, project_name: str, output_dir: str) -> None:
        """Finalize and write the section tree to an XML file.

        Output path: {output_dir}/sections/sections_{book_num:02d}_{book_abbr}_{project_name}.xml
        """
        self.finalize()
        root_elem = ET.Element("sections")
        for node in self._roots:
            root_elem.append(node.to_xml())
        _indent_xml(root_elem)
        tree = ET.ElementTree(root_elem)
        filename = f"sections_{book_num:02d}_{book_abbr}_{project_name}.xml"
        out_path = os.path.join(output_dir, "sections", filename)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        tree.write(out_path, encoding="unicode", xml_declaration=True)


def _indent_xml(elem: ET.Element, level: int = 0) -> None:
    """Add pretty-print indentation to an XML element tree (Python 3.8-compatible)."""
    indent = "\n" + "  " * level
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = indent + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = indent
        for child in elem:
            _indent_xml(child, level + 1)
        # Correct the last child's tail to align with the closing tag
        if not child.tail or not child.tail.strip():
            child.tail = indent
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = indent
