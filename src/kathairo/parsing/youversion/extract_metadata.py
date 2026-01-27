"""
Usage: python kathairo/parsing/youversion/extract_metadata.py https://www.bible.com/id/versions/<version-id>

Fetch version metadata from Bible.com and write it out to a format
resembling DBL metadata.xml
"""

import dataclasses
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.dom import minidom

import requests

YOUVERSION_API_ROOT = "https://www.bible.com/api/bible"

RESOURCES_ROOT = Path("resources")
INCLUDE_JSON_OUTPUT = True


@dataclasses.dataclass
class YouVersionRequest:
    version_id: str

    @property
    def version_url(self):
        return "/".join([YOUVERSION_API_ROOT, "version", str(self.version_id)])

    def get_version_data(self):
        version_request = requests.get(self.version_url)
        if not version_request.ok:
            raise ValueError(f"Failed to get version data from {self.version_url}")
        return version_request.json()


def json_to_xml(json_data):
    def create_element(parent, tag, text=None, attrib=None):
        elem = ET.SubElement(parent, tag)
        if text is not None:
            elem.text = str(text)
        if attrib:
            for key, value in attrib.items():
                elem.set(key, str(value))
        return elem

    root = ET.Element("DBLMetadata")
    root.set("version", "2.2.1")
    # NOTE: The id value here is from the YouVersion API
    # and we should manually replace it with the actual
    # ID from DBL; typically this is done by searching for
    # `name` on the DBL website
    root.set("id", str(json_data["id"]))

    # Identification
    identification = create_element(root, "identification")
    create_element(identification, "name", json_data["title"])
    create_element(identification, "nameLocal", json_data["local_title"])
    create_element(identification, "abbreviation", json_data["abbreviation"])
    create_element(identification, "abbreviationLocal", json_data["local_abbreviation"])
    create_element(
        identification,
        "description",
        f"{json_data['language']['name']}: {json_data['local_title']} (Bible)",
    )
    create_element(identification, "scope", "Bible")

    # Language
    language = create_element(root, "language")
    create_element(language, "iso", json_data["language"]["iso_639_3"])
    create_element(language, "name", json_data["language"]["name"])
    create_element(language, "nameLocal", json_data["language"]["local_name"])
    # create_element(language, "script", json_data["language"]["script"])
    create_element(
        language, "scriptDirection", json_data["language"]["text_direction"].upper()
    )

    # Countries
    # countries = create_element(root, "countries")
    # country = create_element(countries, "country")
    # create_element(
    #     country, "name", "Philippines"
    # )  # Assuming Philippines based on Tagalog language

    # Type
    type_elem = create_element(root, "type")
    create_element(type_elem, "medium", "text")

    # Format
    # format_elem = create_element(root, "format")
    # create_element(format_elem, "versedParagraphs", str(json_data["format"]["versedParagraphs"]).lower())

    # Names
    names = create_element(root, "names")
    for book in json_data["books"]:
        name = create_element(
            names, "name", attrib={"id": f"book-{book['usfm'].lower()}"}
        )
        create_element(name, "abbr", book["abbreviation"])
        create_element(name, "short", book["human"])
        create_element(name, "long", book["human_long"])

    # Manifest (placeholder, as we don't have this information in the JSON)
    create_element(root, "manifest")

    # Publications
    publications = create_element(root, "publications")
    publication = create_element(
        publications, "publication", attrib={"id": "p1", "default": "true"}
    )
    create_element(publication, "name", json_data["title"])
    create_element(publication, "nameLocal", json_data["local_title"])
    create_element(publication, "abbreviation", json_data["abbreviation"])

    # Add canonicalContent to publication
    canonical_content = create_element(publication, "canonicalContent")
    for book in json_data["books"]:
        create_element(canonical_content, "book", attrib={"code": book["usfm"]})

    # Add structure to publication
    structure = create_element(publication, "structure")
    for book in json_data["books"]:
        content = create_element(structure, "content")
        content.set("name", f"book-{book['usfm'].lower()}")
        content.set("role", book["usfm"])
        content.set(
            "src",
            f"https://www.bible.com/bible/{json_data['id']}/{book['usfm']}.1.{json_data['abbreviation']}",
        )

    # Copyright
    # TODO: Ensure we are encoding short versus long
    copyright = create_element(root, "copyright")
    full_statement = create_element(copyright, "fullStatement")
    statement_content = create_element(
        full_statement, "statementContent", attrib={"type": "xhtml"}
    )
    create_element(statement_content, "p", json_data["copyright_short"]["text"])

    # Convert to string and pretty print
    xml_str = ET.tostring(root, encoding="unicode")
    pretty_xml = minidom.parseString(xml_str).toprettyxml(indent="  ")

    return pretty_xml


def main():
    try:
        version_id = sys.argv[1].rsplit("/", maxsplit=1)[1]
    except IndexError:
        version_id = sys.argv[1]

    youversion_request = YouVersionRequest(
        version_id=version_id,
    )
    version_data_json = youversion_request.get_version_data()

    version_name = version_data_json["abbreviation"]
    language_code = version_data_json["language"]["iso_639_3"]
    version_path = RESOURCES_ROOT / language_code / version_name
    version_path.mkdir(parents=True, exist_ok=True)

    if INCLUDE_JSON_OUTPUT:
        json_path = version_path / "youversion-metadata.json"
        with json_path.open("w", encoding="utf-8") as f:
            json.dump(version_data_json, f, ensure_ascii=False, indent=2)

    version_data_xml = json_to_xml(version_data_json)
    xml_path = version_path / "youversion-metadata.xml"
    with xml_path.open("w", encoding="utf-8") as f:
        f.write(version_data_xml)


if __name__ == "__main__":
    main()
