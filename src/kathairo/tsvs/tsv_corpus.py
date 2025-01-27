import polars as pl

def load_tsv_to_corpus(tsv_path: pl.DataFrame):
    return pl.read_csv(tsv_path, separator='\t', infer_schema_length=0)

def get_text_from_tsv(df:pl.DataFrame, id):
    return df.filter(pl.col("id") == id).select("text").item()

def get_preceding_id(df: pl.DataFrame, id):
    return df.filter(pl.col("id") < id).select("id").tail(1).item()

def get_following_id(df: pl.DataFrame, id):
    return df.filter(pl.col("id") > id).select("id").head(1).item()

def get_id_from_source_verse(df: pl.DataFrame, source_verse):
    return df.filter(pl.col("source_verse") == source_verse).select("id").item()

def check_for_null(result):
    return result.last().item() if not result.is_empty() else None