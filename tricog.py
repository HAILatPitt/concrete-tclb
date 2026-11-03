import marimo

__generated_with = "0.18.0"
app = marimo.App(width="medium", app_title="TriCOG Land Bank")

with app.setup:
    import ast
    import contextlib
    import io
    import sys
    import textwrap
    import time
    import warnings
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

    STDOUT_LIMIT = 5000
    TABLE_ROWS_SHOWN = 200
    DIRECTOR_REPLY = (
        "We mean single-family houses only: rows where CLASSDESC is RESIDENTIAL and USEDESC is SINGLE FAMILY. "
        "Not rowhouses, townhouses, two- to four-family homes or vacant land. Our program can't take those on."
    )
    STARTER_CELLS = {
        "load": {
            "title": "Load and look",
            "hint": "Four tables are ready for you: assessments, liens, parcels and tricog. What does each one hold, "
                    "and which of them can be drawn on a map?",
            "code": textwrap.dedent("""\
                tables = {"assessments": assessments, "liens": liens, "parcels": parcels, "tricog": tricog}
                for name, table in tables.items():
                    print(name, table.shape, "coordinate system:", getattr(table, "crs", "none (no shapes)"))
                assessments.head()"""),
        },
        "names": {
            "title": "Boundary by name",
            "hint": "TriCOG has 30 member towns. Do all 30 names turn up in the assessments? Look at the towns "
                    "that don't.",
            "code": textwrap.dedent("""\
                tricog_names = set(tricog["NAME"].str.upper())
                town = assessments["MUNIDESC"].str.strip().str.upper()
                matched = assessments[town.isin(tricog_names)]
                print(len(tricog_names), "TriCOG towns,", matched["MUNIDESC"].nunique(), "town names matched")
                matched["MUNIDESC"].value_counts()"""),
        },
        "crs": {
            "title": "Line up the maps",
            "hint": "Compare what cell 1 printed about each file. Once this clip works it takes about 10 seconds. "
                    "Keep parcels as the first table: clipping TriCOG by every parcel can crash this page.",
            "code": textwrap.dedent("""\
                inside = gp.clip(parcels, tricog)
                print(len(inside), "parcels inside TriCOG")
                inside"""),
        },
        "clip": {
            "title": "Boundary by map",
            "hint": "This cell tries the clip on a small square of parcels around Braddock. What kind of rows "
                    "come back?",
            "code": textwrap.dedent("""\
                sample = parcels.cx[1_376_000:1_380_000, 394_000:398_000]
                tricog_feet = tricog.to_crs(parcels.crs)
                inside = gp.clip(tricog_feet, sample)
                print(len(sample), "parcels in the sample,", len(inside), "rows inside TriCOG")
                inside"""),
        },
        "single_family": {
            "title": "Single-family",
            "hint": "What other kinds of home are in the data? Which column says whether a parcel is a home at all?",
            "code": textwrap.dedent("""\
                homes = assessments[assessments["USEDESC"] == "SINGLE FAMILY"]
                print(len(homes), "single-family homes")
                homes[["PARID", "MUNIDESC", "CLASSDESC", "USEDESC"]]"""),
        },
        "liens": {
            "title": "Joining liens",
            "hint": "Compare the number of rows with the number of homes. Try how='inner' and how='right' too. "
                    "How many rows have no lien amount?",
            "code": textwrap.dedent("""\
                homes = assessments[(assessments["CLASSDESC"] == "RESIDENTIAL") & (assessments["USEDESC"] == "SINGLE FAMILY")]

                # One way: look up each home's lien, one home at a time (timed on 300 homes).
                start = time.time()
                for parid in homes["PARID"].head(300):
                    match = liens[liens["pin"] == parid]
                seconds = time.time() - start
                print(f"300 homes took {seconds:.1f} s; all {len(homes):,} would take about {seconds / 300 * len(homes):,.0f} s")

                # A faster way: join the two tables.
                with_liens = pd.merge(homes, liens, left_on="PARID", right_on="pin", how="left")
                print(len(homes), "homes,", len(with_liens), "rows after the join")
                with_liens[["PARID", "MUNIDESC", "pin", "total_amount"]]"""),
        },
        "combine": {
            "title": "Combine",
            "hint": "inside_tricog holds the parcels inside TriCOG by the map. Compare the count with your guess "
                    "in Predict. Do all these rows meet all three rules?",
            "code": textwrap.dedent("""\
                homes = assessments[(assessments["CLASSDESC"] == "RESIDENTIAL") & (assessments["USEDESC"] == "SINGLE FAMILY")]
                homes_with_liens = pd.merge(homes, liens, left_on="PARID", right_on="pin")
                candidates = pd.merge(inside_tricog, homes_with_liens, on="PARID", how="left")
                print(len(candidates), "candidates")
                candidates[["PARID", "MUNIDESC", "USEDESC", "total_amount"]]"""),
        },
        "amounts": {
            "title": "Lien amounts",
            "hint": "How small is the smallest lien? What share of the candidates owe less than $1,000?",
            "code": textwrap.dedent("""\
                homes = assessments[(assessments["CLASSDESC"] == "RESIDENTIAL") & (assessments["USEDESC"] == "SINGLE FAMILY")]
                homes_with_liens = pd.merge(homes, liens, left_on="PARID", right_on="pin")
                candidates = pd.merge(inside_tricog, homes_with_liens, on="PARID")
                print(len(candidates), "candidates")
                candidates["total_amount"].describe()"""),
        },
    }


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
def cell_namespace(tables: dict) -> dict:
    # assessments is shared, not copied (it's the big one); "Reload the data" restores it.
    return {
        "assessments": tables["assessments"],
        "liens": tables["liens"].copy(),
        "parcels": tables["parcels"].copy(),
        "tricog": tables["tricog"].copy(),
        "inside_tricog": tables["boundary"].loc[tables["boundary"]["by_map"], ["PARID"]].reset_index(drop=True),
        "pd": pd,
        "gp": gp,
        "time": time,
    }


@app.function
def table_ready(value):
    """marimo 0.18 can't draw a pandas 3 table whose text index has no name (without pyarrow), so name it."""
    if isinstance(value, (pd.DataFrame, pd.Series)) and value.index.nlevels == 1 and value.index.name is None:
        return value.rename_axis("index")
    return value


@app.function
def shown_table(value) -> tuple:
    """The first rows to draw (shapes as their type, so the page stays light) and the table's true size."""
    frame = value.to_frame() if isinstance(value, pd.Series) else value
    size = f"{len(frame):,} rows, {frame.shape[1]} columns"
    shown = frame.head(TABLE_ROWS_SHOWN)
    if isinstance(shown, gp.GeoDataFrame):
        shown = pd.DataFrame(shown).assign(**{shown.geometry.name: shown.geom_type})
    return table_ready(shown), size


@app.function
def cut_text(text: str) -> str:
    if len(text) <= STDOUT_LIMIT:
        return text
    return text[:STDOUT_LIMIT] + f"\n(output cut at {STDOUT_LIMIT:,} characters)"


@app.function
def run_cell(code: str, tables: dict) -> dict:
    """Run a student's cell; return its printed text, last value, warnings and error. Nothing is graded."""
    namespace = cell_namespace(tables)
    stdout = io.StringIO()
    value, error, caught = None, None, []
    try:
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            tree = ast.parse(code)
            last = tree.body.pop() if tree.body and isinstance(tree.body[-1], ast.Expr) else None
            with contextlib.redirect_stdout(stdout):
                exec(compile(tree, "<cell>", "exec"), namespace)
                if last is not None:
                    value = eval(compile(ast.Expression(last.value), "<cell>", "eval"), namespace)
    except (Exception, SystemExit) as exc:
        error = f"{type(exc).__name__}: {exc}"
    result, size = shown_table(value) if isinstance(value, (pd.DataFrame, pd.Series)) else (None, None)
    return {
        "stdout": cut_text(stdout.getvalue()),
        "value": None if value is None or result is not None else cut_text(repr(value)),
        "result": result,
        "size": size,
        "warnings": list(dict.fromkeys(str(w.message) for w in caught))[:5],
        "error": error,
    }


@app.function
def explain_unlocked(prediction, runs: dict) -> bool:
    return prediction is not None and all(runs.get(key, 0) >= 1 for key in STARTER_CELLS)


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
