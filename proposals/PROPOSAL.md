# Standardizing tokenization

## What's the "problem", anyway?

We're using "word tokens" (`explicit_references` in ACAI terms) as the driver for a lot of our datasets and annotations.

We're currently using word tokens defined by TSVs from `macula-greek` and `macula-hebrew`.

Those word tokens are using a particular identifier (the `macula_id`) that has several presuppositions:

- Includes "subsumed definite articles" (e.g. `o010010050031ה`), which I understand is used largely as [canitlation marks](https://en.wikipedia.org/wiki/Hebrew_cantillation); those characters are _not_ in the "surface" text for the `WLCM`
- Prefx (`o` or `n`)
- An `after` attribute to encode whitespace _and_ punctuation within a verse
- Varying identifier lengths (based on Hebrew or Greek)
  - oBBCCCVVVWWWP
  - nBBCCCVVVWWW

_macula-hebrew_ sample:

[macula-hebrew-sample.tsv](./macula-hebrew-sample.tsv)


| xml:id         | macula_text | after | english   |
|----------------|-------------|-------|-----------|
| o010010050011  | וַ           |       | and       |
| o010010050012  | יִּקְרָ֨א        |       | called    |
| o010010050021  | אֱלֹהִ֤ים       | ׀     | God       |
| o010010050031  | לָ           |       | to        |
| o010010050031ה |             |       | the       |
| o010010050032  | אוֹר֙         |       | light     |
| o010010050041  | י֔וֹם         |       | day       |
| o010010050051  | וְ           |       | and       |
| o010010050052  | לַ           |       | to        |
| o010010050052ה |             |       | the       |
| o010010050053  | חֹ֖שֶׁךְ         |       | darkness  |
| o010010050061  | קָ֣רָא         |       | called    |
| o010010050071  | לָ֑יְלָה        |       | night     |
| o010010050081  | וַֽ           |       | and       |
| o010010050082  | יְהִי         | ־     | there was |
| o010010050091  | עֶ֥רֶב         |       | evening   |
| o010010050101  | וַֽ           |       | and       |
| o010010050102  | יְהִי         | ־     | there was |
| o010010050111  | בֹ֖קֶר         |       | morning   |
| o010010050121  | י֥וֹם         |       | day       |
| o010010050131  | אֶחָֽד         | ׃פ    | first     |

We also have *existing legacy* alignment data in `internal-Alignments` (e.g., the Grape City).

For the *target* tokenizations in that data there are:

- Consistent identifier lengths:
  - `BBCCCVVVWWWP` (No prefix)
- No `after` column, but an `isPunc` column
- Punctuation is tokenized (no `after` column)

For the `target` tokenizations, since we are tokenizing punctuation, reconstitution needs a little more effort.  We have to evaluate each token and determine how to handle whitespace.  Without it, we get something like this when just concatenating tokens for MRK 1:3 (BSB):

```
“ A voice of one calling in the wilderness , ‘ Prepare the way for the Lord , make straight paths for Him .’”
```

Concatenating the tokens is used to reconstitute the original text.  And for "new" alignments done using Clear-Aligner, if we can communicate the tokenization algorithm, it would be possible to map token-level annotations back onto the formatting stored in the USFM/X versions of a particular translation.

(For `macula-greek` and `macula-hebrew`, we are currently using a TEI edition of WLCM and SBLGNT that includes a limited amount of formatting).

It would be great if at least the "target" TSV files containing the tokens had a consistent way for us to handle reconstitution, so let's start there.

## Target tokens: encoding whitespace

If the GrapeCity data and the data being ran through `kathairo.py` are including punctuation as tokens, it would be pretty trivial to add an additional column to the TSVs that help indicate where whitespace should *not* be introduced.

Here is a sample:

[bsb-mrk-sample.tsv](./bsb-mrk-sample.tsv)


| id          | text       | space_after |
|-------------|------------|-------------|
| 41001003001 | “          | n           |
| 41001003002 | A          |             |
| 41001003003 | voice      |             |
| 41001003004 | of         |             |
| 41001003005 | one        |             |
| 41001003006 | calling    |             |
| 41001003007 | in         |             |
| 41001003008 | the        |             |
| 41001003009 | wilderness | n           |
| 41001003010 | ,          |             |
| 41001003011 | ‘          | n           |
| 41001003012 | Prepare    |             |
| 41001003013 | the        |             |
| 41001003014 | way        |             |
| 41001003015 | for        |             |
| 41001003016 | the        |             |
| 41001003017 | Lord       | n           |
| 41001003018 | ,          |             |
| 41001003019 | make       |             |
| 41001003020 | straight   |             |
| 41001003021 | paths      |             |
| 41001003022 | for        |             |
| 41001003023 | Him        | n           |
| 41001003024 | .          | n           |
| 41001003025 | ’          | n           |
| 41001003026 | ”          |             |

So if `space_after` is `n`, we should _not_ introduce whitespace, but if it is empty, we an assume whitespace can separate the tokens.

This would make it very trivial to reconstitute the text as:

```
“A voice of one calling in the wilderness, ‘Prepare the way for the Lord, make straight paths for Him.’”
```

This is an approach that @jacobwegner and @jtauber used working with data for on the Scaife Viewer project for the Perseus Digital Library, and was inspired by how [spaCy tokens track whitespace](https://spacy.io/api/token#:~:text=str-,whitespace_,-Trailing%20space%20character) and how the [spacy_conll library represents whitespace](https://github.com/BramVanroy/spacy_conll/blob/f2d41da649f1f440c4ec35a3b046d345b5516fd3/spacy_conll/formatter.py#L197) in the [CoNLL-U Format](https://universaldependencies.org/format.html) used by the [Universal Dependencies](https://universaldependencies.org/) framework.

## Target tokens: excluding tokens for alignment

I recognize that part of the legacy data including `isPunc` was to maintain portions of the surface text, but to exclude tokens with `isPunc=True` from alignment.  I think the TSVs we generate in `kathairo.py` could add an `eligible` column that serves a similar purpose.

Given the example from above, the following tokens would not be eligible:

[bsb-mrk-sample-excluded.tsv](./bsb-mrk-sample-excluded.tsv)

| id          | source_verse | text | space_after | eligible |
|-------------|--------------|------|-------------|----------|
| 41001003001 | 41001003     | “    | n           | n        |
| 41001003010 | 41001003     | ,    |             | n        |
| 41001003011 | 41001003     | ‘    | n           | n        |
| 41001003018 | 41001003     | ,    |             | n        |
| 41001003024 | 41001003     | .    | n           | n        |
| 41001003025 | 41001003     | ’    | n           | n        |
| 41001003026 | 41001003     | ”    |             | n        |

I consider this an "optional" part of my proposal, the [sample TSVs](#sample-tsvs) listed at the end of the document implement it.

If we solely adopted `space_after`, I think that would make the TSV more useful for applications consuming these TSVs (Clear-Aligner, ATLAS, our other Python libs, etc)

## Shipping a source token dataset more similar to target tokens

I think we could adapt our "source tokens" to be more consistent with the target tokens.  We would eventually want the "legacy" alignment data to be made consistent to.

I want to respect the integrity of the existing `macula-greek` and `macula-hebrew` data design, but allow us to work more consistently with "target tokens".

I think we can continue to maintain WLCM and SBLGNT identifiers as-is; if we were to "retokenize" the SBLGNT with punctuation, for example, that could introduce some backward incompatible changes.  I experimented with a bit with the USFM version of the SBLGNT and the existing `kathairo.py` pipeline, but did not take it forward to samples like I did with the BSB.

But I do think we could provide a derivative dataset for the `macula-greek` and `macula-hebrew` TSVs that:

- Uses the same "length" identifiers as the target tokens
- Concatenates the `after` column values into a `text` column
- Indicates where `space_after` is `n`

Here are some <a name="sample-tsvs">sample TSVs</a>:

- [source_WLCM_reconstitution_sample.tsv](source_WLCM_reconstitution_sample.tsv)
- [source_SBLGNT_reconstitution_sample.tsv](source_SBLGNT_reconstitution_sample.tsv)

And `.txt` files showing "v-line" like reconstitution:

- [source_WLCM_reconstitution_sample.txt](source_WLCM_reconstitution_sample.txt)
- [source_SBLGNT_reconstitution_sample.txt](source_SBLGNT_reconstitution_sample.txt)


I also demonstrated a small iteration of this concept dealing with the subsumed definite articles.  In [source_SBLGNT_reconstitution_sample.txt](source_SBLGNT_reconstitution_sample.txt), they are included in the TSV, but marked as `eligible=n`.

I prepared an [additional TSV]([text](source_WLCM_reconstitution_sample_wo_definite_articles.tsv)) and [reconstitution sample]([text](source_WLCM_reconstitution_sample_wo_definite_articles.txt)) that just exclude them from the TSVs altogether.

## Consistent length identifiers

Lastly, if we are doing a derivative dataset away from the XML IDs in the macula data, I am suggesting that token identifiers always have a consistent length:

```
BBCCCVVVWWWPP
010010010011
410010030011
410010030011
```

This would allow the WLCM identifiers to match other identifiers, and if we had sub-word tokenization in a target token dataset (e.g., an Arabic New Testament with sub-word tokenization), we could support it.

Otherwise, the "status quo" would be that we drop it unless the token dataset needs it (which right now, would only be for the WLCM).
