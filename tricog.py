import marimo

__generated_with = "0.18.0"
app = marimo.App(width="medium", app_title="TriCOG Land Bank")

with app.setup:
    import io
    import sys
    from pathlib import Path

    import geopandas as gp
    import pandas as pd
    import pyarrow  # noqa: F401  (marimo loads Pyodide packages from imports; pandas needs it for parquet)

    DATA_FILES = ("assessments", "liens", "parcels", "tricog", "boundary")
    # Coordinate systems as each source publishes them: WPRDC parcels in Pennsylvania South feet,
    # TriCOG's Census boundary in longitude and latitude. WKT carries no coordinate system, so we name them here.
    PARCELS_CRS = "EPSG:2272"
    TRICOG_CRS = "EPSG:4326"
    REFERENCE_SETTINGS = {
        "boundary": "map",
        "types": ("SINGLE FAMILY",),
        "liens_join": "inner",
        "combine_join": "inner",
        "cutoff": 0.0,
    }
    MULTI_FAMILY = ("TWO FAMILY", "THREE FAMILY", "FOUR FAMILY")
    COUNT_BUCKETS = ("under 500", "500 to 5,000", "5,000 to 50,000", "more than 50,000")
    # Counts that don't depend on the student's settings, from the prepared snapshot (CONCRETE/docs/tclb_poee).
    MISMATCHED_CLIP_ROWS = 0
    REVERSED_CLIP_ROWS = 5
    HIDDEN_FACTS = (
        "The county's assessment file has 584,139 rows; you worked with the 171,425 around TriCOG. Only the "
        "parcels and TriCOG files carry shapes, and they arrive in different coordinate systems: feet for the "
        "parcels, longitude and latitude for TriCOG.",
        "Matching town names misses McKeesport and Clairton, whose assessment records are split into wards "
        "(\"1st Ward - McKEESPORT\"). That drops 2,351 homes from the list. Codes don't rescue it: the Census, "
        "the county and the wards each number McKeesport differently.",
        "With feet on one side and degrees on the other, the two maps don't overlap, so the clip returns 0 rows. "
        "geopandas prints a warning, and the cell still runs without an error.",
        "gp.clip returns rows of the table you pass first. With TriCOG first, the sample gives back 5 town "
        "shapes, not parcels.",
        "Residential parcels in the area carry 25 use codes. Adding rowhouses and townhouses brings in 575 more "
        "homes with liens, two- to four-family homes 643, and vacant land 9,330.",
        "A left join keeps every home whether or not it has a lien: 53,858 rows, 46,144 of them owing nothing. "
        "The row-by-row loop finds the same liens as an inner join, far more slowly.",
        "A left join when combining keeps every parcel inside TriCOG: 85,765 rows, of which 31,907 are not "
        "single-family homes and 46,144 are homes with no lien.",
        "Half the homes on the list owe less than $1,479.46. 420 owe under $100 and 3,126 owe under $1,000.",
        "The parcels file repeats 468 parcel IDs. None of the repeats reach the list.",
        "6,702 liens match no parcel anywhere in the county, and 50,931 match no parcel in your area, because "
        "the liens file covers the whole county.",
        "58 homes on the list sit partly outside TriCOG's border. The clip keeps the part inside.",
    )


@app.function
def read_blobs_local(base) -> dict:
    return {name: (Path(base) / f"{name}.parquet").read_bytes() for name in DATA_FILES}


@app.function
async def fetch_blobs(base: str) -> dict:
    """In the browser: fetch the bytes ourselves (no GDAL, and GitHub Pages' gzip header confuses readers)."""
    from pyodide.http import pyfetch

    blobs = {}
    for name in DATA_FILES:
        response = await pyfetch(f"{base}/{name}.parquet")
        blobs[name] = await response.bytes()
    return blobs


@app.function
def shapes_from_wkt(frame, crs: str):
    return gp.GeoDataFrame(frame.drop(columns="geometry"), geometry=gp.GeoSeries.from_wkt(frame["geometry"]), crs=crs)


@app.function
def load_tables(blobs: dict) -> dict:
    """Fresh tables from the downloaded bytes, so "Reload the data" undoes anything a student's code changed."""
    frames = {name: pd.read_parquet(io.BytesIO(blob)) for name, blob in blobs.items()}
    frames["parcels"] = shapes_from_wkt(frames["parcels"], PARCELS_CRS)
    frames["tricog"] = shapes_from_wkt(frames["tricog"], TRICOG_CRS)
    return frames


@app.function
def slim_table(tables: dict):
    """The four columns the list needs, copied once, so student code that edits `assessments` can't change the list."""
    return tables["assessments"][["PARID", "MUNIDESC", "CLASSDESC", "USEDESC"]].copy()


@app.function
def build_list(slim, liens, boundary, settings: dict):
    """Boundary, then type, then liens, then combine, then cutoff. Rows with no lien survive the cutoff."""
    inside = boundary.loc[boundary["by_map" if settings["boundary"] == "map" else "by_name"], ["PARID"]]
    homes = slim[(slim["CLASSDESC"] == "RESIDENTIAL") & slim["USEDESC"].isin(settings["types"])]
    with_liens = homes.merge(liens[["pin", "total_amount"]], left_on="PARID", right_on="pin", how=settings["liens_join"])
    combined = inside.merge(with_liens, on="PARID", how=settings["combine_join"])
    keep = combined["total_amount"].isna() | (combined["total_amount"] > settings["cutoff"])
    return combined[keep].drop(columns="pin").reset_index(drop=True)


@app.function
def reference_list(slim, liens, boundary, cutoff: float):
    return build_list(slim, liens, boundary, {**REFERENCE_SETTINGS, "cutoff": cutoff})


@app.function
def one_change(slim, liens, boundary, settings: dict, name: str):
    """The reference list with only one setting (and the cutoff) taken from the student's choices."""
    changed = {**REFERENCE_SETTINGS, name: settings[name], "cutoff": settings["cutoff"]}
    return build_list(slim, liens, boundary, changed)


@app.function
def town_name(munidesc: str) -> str:
    return munidesc.split("-")[-1].strip()


@app.function
def boundary_card(slim, liens, boundary, settings: dict) -> dict | None:
    if settings["boundary"] == REFERENCE_SETTINGS["boundary"]:
        return None
    reference = reference_list(slim, liens, boundary, settings["cutoff"])
    chosen = one_change(slim, liens, boundary, settings, "boundary")
    missed = reference[~reference["PARID"].isin(chosen["PARID"])]
    return {"missed": len(missed), "by_town": missed["MUNIDESC"].map(town_name).value_counts().head(5).to_dict()}


@app.function
def definition_card(slim, liens, boundary, settings: dict) -> dict | None:
    if set(settings["types"]) == set(REFERENCE_SETTINGS["types"]):
        return None
    reference = reference_list(slim, liens, boundary, settings["cutoff"])
    chosen = one_change(slim, liens, boundary, settings, "types")
    extra = chosen[~chosen["PARID"].isin(reference["PARID"])]
    return {
        "extra": len(extra),
        "extra_by_type": extra["USEDESC"].value_counts().to_dict(),
        "missed": int((~reference["PARID"].isin(chosen["PARID"])).sum()),
        "multi_family_extra": int(extra["USEDESC"].isin(MULTI_FAMILY).sum()),
    }


@app.function
def liens_join_card(slim, liens, boundary, settings: dict) -> dict | None:
    if settings["liens_join"] == REFERENCE_SETTINGS["liens_join"]:
        return None
    chosen = one_change(slim, liens, boundary, settings, "liens_join")
    return {"no_lien_rows": int(chosen["total_amount"].isna().sum())}


@app.function
def combine_card(slim, liens, boundary, settings: dict) -> dict | None:
    if settings["combine_join"] == REFERENCE_SETTINGS["combine_join"]:
        return None
    reference = reference_list(slim, liens, boundary, settings["cutoff"])
    chosen = one_change(slim, liens, boundary, settings, "combine_join")
    added_ids = chosen.loc[~chosen["PARID"].isin(reference["PARID"]), ["PARID"]]
    looked_up = added_ids.merge(slim, on="PARID", how="left")
    is_home = (looked_up["CLASSDESC"] == "RESIDENTIAL") & looked_up["USEDESC"].isin(REFERENCE_SETTINGS["types"])
    return {"not_single_family": int((~is_home).sum()), "single_family_no_lien": int(is_home.sum())}


@app.function
def cutoff_card(slim, liens, boundary, cutoff: float) -> dict:
    kept = reference_list(slim, liens, boundary, cutoff)
    return {
        "under_100": int((kept["total_amount"] < 100).sum()),
        "under_1000": int((kept["total_amount"] < 1000).sum()),
        "removed": len(reference_list(slim, liens, boundary, 0)) - len(kept),
    }


@app.function
def count_bucket(count: int) -> str:
    if count < 500:
        return COUNT_BUCKETS[0]
    if count < 5000:
        return COUNT_BUCKETS[1]
    if count <= 50000:
        return COUNT_BUCKETS[2]
    return COUNT_BUCKETS[3]


@app.function
def checking_numbers(slim, liens, boundary, settings: dict, guess: str) -> dict:
    your_count = len(build_list(slim, liens, boundary, settings))
    single_family = (slim["CLASSDESC"] == "RESIDENTIAL") & slim["USEDESC"].isin(REFERENCE_SETTINGS["types"])
    return {
        "mismatched_clip_rows": MISMATCHED_CLIP_ROWS,
        "reversed_clip_rows": REVERSED_CLIP_ROWS,
        "single_family_in_area": int(single_family.sum()),
        "your_count": your_count,
        "your_bucket": count_bucket(your_count),
        "guess": guess,
    }


if __name__ == "__main__":
    app.run()
