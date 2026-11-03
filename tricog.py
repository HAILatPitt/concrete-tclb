import marimo

__generated_with = "0.18.0"
app = marimo.App(width="medium", app_title="TriCOG Land Bank")

with app.setup:
    import ast
    import base64
    import contextlib
    import functools
    import html
    import io
    import sys
    import textwrap
    import time
    import warnings
    from pathlib import Path

    import geopandas as gp
    import pandas as pd
    import matplotlib
    import pyarrow  # noqa: F401  (marimo loads Pyodide packages from imports; pandas needs it for parquet)

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.axes import Axes

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
    # TriCOG's 30 member municipalities, upper-case, as named in its boundary file.
    MEMBER_TOWNS = (
        "BLAWNOX", "BRADDOCK", "BRADDOCK HILLS", "CHALFANT", "CHURCHILL", "CLAIRTON", "DRAVOSBURG",
        "EAST MCKEESPORT", "EAST PITTSBURGH", "EDGEWOOD", "ETNA", "FOREST HILLS", "GLASSPORT", "HOMESTEAD",
        "MCKEESPORT", "MILLVALE", "MONROEVILLE", "MUNHALL", "NORTH BRADDOCK", "NORTH VERSAILLES", "PITCAIRN",
        "RANKIN", "RESERVE", "SHARPSBURG", "SOUTH VERSAILLES", "SWISSVALE", "TURTLE CREEK", "WEST HOMESTEAD",
        "WHITE OAK", "WILKINS",
    )
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
        "Among the single-family homes inside TriCOG, a left join keeps every home whether or not it has a "
        "lien: 53,858 rows, 46,144 of them owing nothing. Cell 6 joins every home in the area, so it prints more. "
        "The row-by-row loop finds the same liens as an inner join, far more slowly.",
        "A left join when combining keeps every parcel inside TriCOG by the map: 85,765 rows, of which 31,907 are not "
        "single-family homes and 46,144 are homes with no lien.",
        "Half the homes on the list owe less than $1,479.46. 420 owe under $100 and 3,126 owe under $1,000.",
        "The parcels file repeats 468 parcel IDs. None of the repeats reach the list.",
        "6,702 liens match no parcel anywhere in the county, and 50,931 match no parcel in your area, because "
        "the liens file covers the whole county.",
        "58 homes on the list sit partly outside TriCOG's border. The clip keeps the part inside.",
    )

    STAGES = ("Predict", "Observe", "Explain", "Evaluate")
    OPENING_CARDS = {
        "story": {
            "title": "The story so far",
            "text": "The TriCOG Land Bank buys abandoned homes and makes them available as affordable housing. By "
                    "law it can only buy inside its 30 member municipalities, east and north of Pittsburgh. Tax "
                    "liens are its clue that a house may be abandoned: an owner who walks away stops paying "
                    "property tax.",
        },
        "role": {
            "title": "Your role",
            "text": "You're an intern working with TriCOG's data analyst. The director wants a first list of homes "
                    "the land bank should look at.",
        },
        "deliver": {
            "title": "What you deliver",
            "text": "A list of parcels that meet three rules: inside TriCOG, a single-family home, and at least one "
                    "tax lien. Then a short note to the director saying how far to trust it.",
        },
    }
    PREDICT_GUIDING = (
        "What could go wrong if you find places by matching their names?",
        "Which kinds of building would you call a single-family home?",
        "What does a tax lien tell you about a house, and what can't it tell you?",
    )
    PREDICT_TYPES = ("SINGLE FAMILY", "ROWHOUSE", "TOWNHOUSE", "TWO FAMILY", "THREE FAMILY", "FOUR FAMILY",
                     "CONDOMINIUM", "MOBILE HOME", "VACANT LAND")
    BOUNDARY_LABELS = {"names": "Match town names", "map": "Use the map"}
    JOIN_LABELS = {"inner": "Inner join: keep only rows that match", "left": "Left join: keep every row of the first table"}
    EXPLAIN_PROMPTS = (
        "Which rule was hardest to turn into code, and why?",
        "How did you choose your lien cutoff, and who carries the risk of that choice?",
        "A note to the director: your list, how far to trust it, and who might be harmed.",
    )
    STYLE = """
    .tc-card{border:1px solid rgba(127,127,127,.35);border-radius:8px;padding:10px 16px;margin:8px 0}
    .tc-card h4,.tc-eval h4{margin:0 0 4px;font-size:1.05rem;font-weight:700}
    .tc-title{font-size:2rem;font-weight:700;margin:16px 0}
    .tc-h3{font-size:1.25rem;font-weight:700;margin:22px 0 6px}
    .tc-list{list-style:disc;padding-left:1.5em}
    ol.tc-list{list-style:decimal}
    .tc-list li{margin:4px 0}
    .tc-stage{border-bottom:2px solid rgba(127,127,127,.5);margin:32px 0 8px;padding-bottom:4px}
    .tc-stage h2{font-size:1.6rem;font-weight:700;margin:2px 0}
    .tc-stage small{opacity:.7;text-transform:uppercase;letter-spacing:.05em}
    .tc-eval{border-left:4px solid #bf8700;border-radius:4px;padding:8px 16px;margin:10px 0}
    .tc-eval dt{font-weight:600;margin-top:6px}
    .tc-eval dd{margin:0 0 4px 0}
    """

    STDOUT_LIMIT = 5000
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
            "hint": "Compare the number of rows with the number of homes, and count the rows with no lien amount. "
                    "Try how='right' too. pd.merge keeps only rows that match unless you say otherwise: "
                    "how='inner' is the default.",
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
    towns = missed["MUNIDESC"].map(town_name)
    member = towns.str.upper().isin(MEMBER_TOWNS)
    return {"missed": len(missed), "by_town": towns[member].value_counts().to_dict(), "border": int((~member).sum())}


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
def prepared_tables(tables: dict) -> dict:
    # assessments is shared, not copied (it's the big one); "Reload the data" restores it.
    return {
        "assessments": tables["assessments"],
        "liens": tables["liens"].copy(),
        "parcels": tables["parcels"].copy(),
        "tricog": tables["tricog"].copy(),
    }


@app.function
def make_namespace(tables: dict) -> dict:
    """One namespace for the whole session, like a notebook: what a task saves, later tasks can use."""
    return {**prepared_tables(tables), "pd": pd, "gp": gp, "plt": plt, "time": time}


@app.function
def reload_into(namespace: dict, tables: dict) -> None:
    """Put fresh copies of the prepared tables back; the learner's own results stay."""
    namespace.update(prepared_tables(tables))


@app.function
def figure_html(figure) -> str:
    """Draw now, so a figure that can't be drawn fails inside run_code's guard, not in the page."""
    buffer = io.BytesIO()
    figure.savefig(buffer, format="png", dpi=100, bbox_inches="tight")
    encoded = base64.b64encode(buffer.getvalue()).decode()
    return f"<img src='data:image/png;base64,{encoded}' style='max-width:100%' alt='Your map'>"


@app.function
def table_ready(value):
    """marimo 0.18 can't draw a pandas 3 table whose text index has no name (without pyarrow), so name it."""
    if isinstance(value, (pd.DataFrame, pd.Series)) and value.index.nlevels == 1 and value.index.name is None:
        return value.rename_axis("index")
    return value


@app.function
def shown_table(value) -> tuple:
    """The table to draw (shapes as their type, so the page stays light) and its size."""
    frame = value.to_frame() if isinstance(value, pd.Series) else value
    size = f"{len(frame):,} rows, {frame.shape[1]} columns"
    shown = frame
    if isinstance(shown, gp.GeoDataFrame):
        shown = pd.DataFrame(shown).assign(**{shown.geometry.name: shown.geom_type})
    return table_ready(shown), size


@app.function
def drawn_table(frame):
    """Format the table now, inside run_code's guard: a table marimo can't draw (duplicate column names, say)
    must not break the Observe stage later. None means "show it as text instead"."""
    import marimo as mo

    try:
        return mo.as_html(frame)
    except Exception:
        return None


@app.function
def cut_text(text: str) -> str:
    if len(text) <= STDOUT_LIMIT:
        return text
    return text[:STDOUT_LIMIT] + f"\n(output cut at {STDOUT_LIMIT:,} characters)"


@app.function
def run_code(code: str, namespace: dict) -> dict:
    """Run a learner's code in the shared namespace; return its printed text, last value, figure, warnings and
    error. Nothing is graded."""
    stdout = io.StringIO()
    value, error, caught = None, None, []
    result, shown, size, text, figure = None, None, None, None, None
    plt.close("all")
    try:
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            tree = ast.parse(code)
            last = tree.body.pop() if tree.body and isinstance(tree.body[-1], ast.Expr) else None
            with contextlib.redirect_stdout(stdout):
                exec(compile(tree, "<cell>", "exec"), namespace)
                if last is not None:
                    value = eval(compile(ast.Expression(last.value), "<cell>", "eval"), namespace)
        if isinstance(value, (pd.DataFrame, pd.Series)):
            result, size = shown_table(value)
            shown = drawn_table(result)
        if plt.get_fignums():
            figure = figure_html(plt.gcf())
        if value is not None and shown is None and not isinstance(value, Axes):
            text = cut_text(repr(value))
    except (Exception, SystemExit) as exc:
        error = f"{type(exc).__name__}: {exc}"
    plt.close("all")
    return {
        "stdout": cut_text(stdout.getvalue()),
        "value": text,
        "result": result,
        "shown": shown,
        "size": size,
        "figure": figure,
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


@app.function
def with_entry(mapping: dict, name: str, value) -> dict:
    return {**mapping, name: value}


@app.function
def record_field(setter, key: str, value) -> None:
    setter(lambda fields: with_entry(fields, key, value))


@app.function
def clicked_cells(clicks: dict, done: dict) -> list:
    """Cells whose Run button has been clicked since we last ran them (each button counts its clicks)."""
    return [key for key, count in clicks.items() if count > done.get(key, 0)]


@app.function
def prediction_ready(fields: dict) -> bool:
    texts = ("boundary_why", "amount", "harmed")
    return bool(fields.get("boundary")) and bool(fields.get("types")) and bool(fields.get("bucket")) and all(
        str(fields.get(key) or "").strip() for key in texts)


@app.function
def can_submit(fields: dict) -> bool:
    return all(fields.get(f"r{i}", "").strip() for i in range(1, len(EXPLAIN_PROMPTS) + 1))


@app.function
def settings_from_controls(boundary, types, liens_join, combine_join, cutoff) -> dict | None:
    if None in (boundary, liens_join, combine_join):
        return None
    return {"boundary": boundary, "types": tuple(types), "liens_join": liens_join,
            "combine_join": combine_join, "cutoff": float(cutoff)}


@app.function
def stage_header_html(stage: int) -> str:
    return f"<div class='tc-stage'><small>Stage {stage} of 4</small><h2>{STAGES[stage - 1]}</h2></div>"


@app.function
def paragraph_html(text: str) -> str:
    return html.escape(text.strip()).replace("\n", "<br>") if text.strip() else "<i>(left blank)</i>"


@app.function
def opening_cards_html() -> str:
    cards = "".join(f"<div class='tc-card'><h4>{html.escape(card['title'])}</h4><p>{html.escape(card['text'])}</p></div>"
                    for card in OPENING_CARDS.values())
    return f"<style>{STYLE}</style><h1 class='tc-title'>Finding abandoned homes for the TriCOG Land Bank</h1>{cards}"


@app.function
def types_text(types) -> str:
    return ", ".join(t.capitalize() for t in types) if types else "none"


@app.function
def locked_prediction_html(prediction: dict) -> str:
    return (
        "<div class='tc-card'><h4>Your locked prediction</h4>"
        f"<p><b>Finding parcels inside TriCOG:</b> {html.escape(BOUNDARY_LABELS[prediction['boundary']])}. "
        f"{paragraph_html(prediction['boundary_why'])}</p>"
        f"<p><b>Counts as single-family:</b> {html.escape(types_text(prediction['types']))}</p>"
        f"<p><b>Lien amount that suggests abandonment:</b> {paragraph_html(prediction['amount'])}. "
        f"<b>Who is harmed if that's wrong:</b> {paragraph_html(prediction['harmed'])}</p>"
        f"<p><b>Parcels meeting all three rules:</b> {html.escape(prediction['bucket'])}</p></div>"
    )


@app.function
def settings_html(settings: dict) -> str:
    return (
        "<ul class='tc-list'>"
        f"<li>Boundary: {html.escape(BOUNDARY_LABELS[settings['boundary']])}</li>"
        f"<li>Home types: {html.escape(types_text(settings['types']))}</li>"
        f"<li>Joining liens: {html.escape(JOIN_LABELS[settings['liens_join']])}</li>"
        f"<li>Combining: {html.escape(JOIN_LABELS[settings['combine_join']])}</li>"
        f"<li>Lien cutoff: more than ${settings['cutoff']:,.0f}</li></ul>"
    )


@app.function
def town_label(name: str) -> str:
    return name.title().replace("Mck", "McK")


@app.function
def counts_text(counts: dict, label) -> str:
    return ", ".join(f"{count:,} {label(name)}" for name, count in counts.items())


@app.function
def eval_card_html(card_id: str, title: str, rows: tuple) -> str:
    items = "".join(f"<dt>{html.escape(label)}</dt><dd>{html.escape(text)}</dd>" for label, text in rows)
    return f'<div class="tc-eval" data-card="{card_id}"><h4>{html.escape(title)}</h4><dl>{items}</dl></div>'


@app.function
def border_text(border: int) -> str:
    if not border:
        return ""
    return f", and {border:,} on parcels that straddle TriCOG's border and are recorded under a neighbouring town"


@app.function
def boundary_card_html(card: dict) -> str:
    return eval_card_html("boundary", "Finding parcels by town name", (
        ("What you chose", "You matched town names instead of using the map."),
        ("Why it matters", "McKeesport's and Clairton's assessment records are split into wards, so their names "
                           "never match TriCOG's list."),
        ("The count", f"{card['missed']:,} homes on the map-based list are missing from yours: "
                      f"{counts_text(card['by_town'], lambda name: 'in ' + town_label(name))}"
                      f"{border_text(card['border'])}."),
        ("What happens", "Eligible empty houses in those towns are never considered, and TriCOG's effort shifts "
                         "away from them."),
    ))


@app.function
def definition_card_html(card: dict, types) -> str:
    rows = [("What you chose", f"You counted these as single-family: {types_text(types)}."),
            ("Why it matters", "The director means single-family houses only.")]
    if card["extra"]:
        rows.append(("The count", f"{card['extra']:,} extra parcels on your list: "
                                  f"{counts_text(card['extra_by_type'], lambda name: name.lower())}."))
        happens = "TriCOG makes offers its program can't use."
        if card["multi_family_extra"]:
            happens += (f" {card['multi_family_extra']:,} of them are two- to four-family homes, where tenants "
                        "could lose their homes.")
        rows.append(("What happens", happens))
    if card["missed"]:
        rows.append(("Homes missed", f"{card['missed']:,} eligible single-family homes are missing from your list, "
                                     "so those houses stay empty."))
    return eval_card_html("definition", "Which homes count as single-family", tuple(rows))


@app.function
def liens_join_card_html(card: dict) -> str:
    return eval_card_html("liens_join", "Joining homes to liens", (
        ("What you chose", "A left join, which keeps every home whether or not it has a lien."),
        ("The count", f"{card['no_lien_rows']:,} rows on your list owe nothing."),
        ("What happens", "Letters suggesting their home could be taken go to households that owe nothing."),
    ))


@app.function
def combine_card_html(card: dict) -> str:
    return eval_card_html("combine", "Combining the three rules", (
        ("What you chose", "A left join, which keeps every parcel inside TriCOG whether or not it passed the "
                           "other two rules."),
        ("The count", f"{card['not_single_family']:,} parcels that aren't single-family homes, and "
                      f"{card['single_family_no_lien']:,} homes with no lien."),
        ("What happens", "Offers on businesses, apartments and lots the program can't use, and letters to "
                         "households that owe nothing."),
    ))


@app.function
def small_debts_text(card: dict) -> str:
    if not card["under_1000"]:
        return ("No home on the list at your cutoff owes under $1,000, so the letters least supported by the "
                "evidence are gone. The removed homes below are the other side of that choice.")
    return (f"On the list at your cutoff, {card['under_100']:,} homes owe under $100 and {card['under_1000']:,} owe "
            "under $1,000. A small debt is weak evidence of abandonment, so these are the letters most likely to "
            "reach families still living there.")


@app.function
def removed_text(removed: int) -> str:
    if not removed:
        return "None. Every home with a lien stays on your list, including the smallest debts above."
    return f"{removed:,} homes with a lien. If any of them are abandoned, they stay empty."


@app.function
def cutoff_card_html(card: dict, cutoff: float) -> str:
    return eval_card_html("cutoff", "Your lien cutoff", (
        ("What you chose", f"Keep homes whose liens total more than ${cutoff:,.0f}."),
        ("What the data can't say", "No column says whether a home is abandoned or lived in, so a lien is only "
                                    "a clue."),
        ("Small debts", small_debts_text(card)),
        ("Homes your cutoff removed", removed_text(card["removed"])),
    ))


@app.function
def checking_html(numbers: dict, reference_count: int) -> str:
    bigger = (" Your list has more rows than that." if numbers["your_count"] > numbers["single_family_in_area"]
              else "")
    items = (
        f"The clip across two coordinate systems returned {numbers['mismatched_clip_rows']} rows.",
        f"The reversed clip returned {numbers['reversed_clip_rows']} rows: towns, not parcels.",
        f"The whole prepared area holds {numbers['single_family_in_area']:,} single-family homes, so a list "
        f"larger than that can't be a list of homes.{bigger}",
        f"You guessed {numbers['guess']}. Your list has {numbers['your_count']:,} rows ({numbers['your_bucket']}). "
        f"With the map, the director's definition and inner joins, at your cutoff, the list has "
        f"{reference_count:,}.",
    )
    return "<ul class='tc-list'>" + "".join(f"<li>{html.escape(item)}</li>" for item in items) + "</ul>"


@app.function
def evaluation_html(slim, liens, boundary, settings: dict, prediction: dict) -> str:
    args = (slim, liens, boundary, settings)
    cards = [
        boundary_card_html(card) if (card := boundary_card(*args)) else "",
        definition_card_html(card, settings["types"]) if (card := definition_card(*args)) else "",
        liens_join_card_html(card) if (card := liens_join_card(*args)) else "",
        combine_card_html(card) if (card := combine_card(*args)) else "",
        cutoff_card_html(cutoff_card(slim, liens, boundary, settings["cutoff"]), settings["cutoff"]),
    ]
    numbers = checking_numbers(*args, prediction["bucket"])
    reference_count = len(reference_list(slim, liens, boundary, settings["cutoff"]))
    facts = "".join(f"<li>{html.escape(fact, quote=False)}</li>" for fact in HIDDEN_FACTS)
    return (
        "<h3 class='tc-h3'>Part 1 · Your choices</h3><p>Each card changes one of your settings from the director's version and "
        "counts what that one choice did, at your own cutoff.</p>" + "".join(cards)
        + "<h3 class='tc-h3'>Part 2 · Numbers worth checking</h3>" + checking_html(numbers, reference_count)
        + f"<h3 class='tc-h3'>Part 3 · What the data was hiding</h3><ol class='tc-list'>{facts}</ol>"
    )


@app.function
def report_html(prediction: dict, settings: dict, explain: dict, evaluation: str) -> str:
    answers = "".join(f"<h3>{html.escape(q)}</h3><p>{paragraph_html(explain.get(f'r{i}', ''))}</p>"
                      for i, q in enumerate(EXPLAIN_PROMPTS, 1))
    return (
        "<!doctype html><html><head><meta charset='utf-8'><title>TriCOG Land Bank brief</title>"
        f"<style>body{{font-family:system-ui,sans-serif;max-width:760px;margin:2em auto;line-height:1.5}}{STYLE}</style>"
        "</head><body><h1>TriCOG Land Bank brief</h1>"
        f"<h2>My prediction</h2>{locked_prediction_html(prediction)}"
        f"<h2>My list settings</h2>{settings_html(settings)}"
        f"<h2>My reflection</h2>{answers}"
        f"<h2>Evaluation</h2>{evaluation}</body></html>"
    )


@app.cell(hide_code=True)
def opening(mo, start_button):
    mo.vstack([mo.Html(opening_cards_html()), start_button])
    return


@app.cell
def start_control(mo):
    # Buttons here count their clicks and cells read the count: in the browser build, a button's on_change
    # callback fires only for its first click.
    start_button = mo.ui.button(value=0, on_click=lambda count: count + 1, label="Start with Stage 1", kind="success")
    return (start_button,)


@app.cell
def predict_states(mo):
    get_predict_draft, set_predict_draft = mo.state(
        {"boundary": None, "boundary_why": "", "types": [], "amount": "", "harmed": "", "bucket": None})
    get_prediction, set_prediction = mo.state(None)
    return get_predict_draft, get_prediction, set_predict_draft, set_prediction


@app.cell
def predict_inputs(mo, set_predict_draft):
    # Created once here, so re-running the cell that shows them never wipes what the learner typed.
    predict_fields = {
        "boundary": mo.ui.radio(options={label: key for key, label in BOUNDARY_LABELS.items()}, value=None,
                                on_change=functools.partial(record_field, set_predict_draft, "boundary")),
        "boundary_why": mo.ui.text_area(rows=3, full_width=True,
                                        on_change=functools.partial(record_field, set_predict_draft, "boundary_why")),
        "types": mo.ui.multiselect(options={t.capitalize(): t for t in PREDICT_TYPES},
                                   on_change=functools.partial(record_field, set_predict_draft, "types")),
        "amount": mo.ui.text(placeholder="for example $500",
                             on_change=functools.partial(record_field, set_predict_draft, "amount")),
        "harmed": mo.ui.text_area(rows=3, full_width=True,
                                  on_change=functools.partial(record_field, set_predict_draft, "harmed")),
        "bucket": mo.ui.radio(options=list(COUNT_BUCKETS), value=None,
                              on_change=functools.partial(record_field, set_predict_draft, "bucket")),
    }
    lock_button = mo.ui.run_button(label="Lock my prediction", kind="success")
    return lock_button, predict_fields


@app.cell
def lock_prediction(get_predict_draft, lock_button, mo, set_prediction):
    _draft = get_predict_draft()
    _ready = prediction_ready(_draft)
    if lock_button.value and _ready:
        set_prediction({**_draft, "types": list(_draft["types"])})
    lock_warning = (mo.callout("Answer all four questions before you lock.", kind="warn")
                    if lock_button.value and not _ready else "")
    return (lock_warning,)


@app.cell(hide_code=True)
def predict(get_prediction, lock_button, lock_warning, mo, predict_fields, start_button):
    mo.stop(not start_button.value)
    _guiding = "".join(f"<li>{html.escape(q)}</li>" for q in PREDICT_GUIDING)
    _header = [
        mo.Html(stage_header_html(1)),
        mo.Html(f"<p>Before you look at the data, decide what you think. These questions may help, and nobody "
                f"grades them:</p><ul class='tc-list'>{_guiding}</ul><p>Then answer the four questions below. "
                "<b>Once you lock your prediction you can't change it.</b></p>"),
    ]
    if get_prediction() is None:
        _output = mo.vstack(_header + [
            mo.md("**1.** To find parcels inside TriCOG's 30 towns, would you match town names or use the map? Why?"),
            predict_fields["boundary"], predict_fields["boundary_why"],
            mo.md("**2.** Which kinds of home count as single-family?"), predict_fields["types"],
            mo.md("**3.** What lien amount would make you believe a house is abandoned? Who is harmed if you're wrong?"),
            predict_fields["amount"], predict_fields["harmed"],
            mo.md("**4.** Roughly how many parcels will meet all three rules?"), predict_fields["bucket"],
            lock_button, lock_warning,
        ])
    else:
        _output = mo.vstack(_header + [mo.Html(locked_prediction_html(get_prediction()))])
    _output
    return


@app.cell
async def load_data(mo):
    # A local folder when run locally, a URL in the browser build.
    _base = mo.notebook_location() / "public" / "data"
    blobs = await fetch_blobs(str(_base)) if "pyodide" in sys.modules else read_blobs_local(_base)
    # A plain dict, so "Reload the data" can swap in fresh tables without re-running the cells that use them.
    shared = {"tables": load_tables(blobs)}
    slim = slim_table(shared["tables"])
    return blobs, shared, slim


@app.cell
def observe_states(mo):
    get_submitted, set_submitted = mo.state(False)
    get_final_settings, set_final_settings = mo.state(None)
    # Plain dicts: how many clicks of each button have been acted on, and each cell's latest output.
    run_log = {"done": {}, "outputs": {}}
    reload_log = {"done": 0}
    return get_final_settings, get_submitted, reload_log, run_log, set_final_settings, set_submitted


@app.cell
def cell_controls(mo):
    # Created once here, so re-running the cell that shows them never wipes the learner's code. The editors sit
    # in a plain dict, so a keystroke re-runs nothing; a Run click reads the code straight from the editor.
    cell_editors = {
        key: mo.ui.code_editor(value=cell["code"], language="python", min_height=100)
        for key, cell in STARTER_CELLS.items()
    }
    cell_run_buttons = mo.ui.dictionary({
        key: mo.ui.button(value=0, on_click=lambda count: count + 1, label="Run") for key in STARTER_CELLS
    })
    director_button = mo.ui.button(value=0, on_click=lambda count: count + 1, label="Ask the director")
    reload_button = mo.ui.button(value=0, on_click=lambda count: count + 1, label="Reload the data")
    return cell_editors, cell_run_buttons, director_button, reload_button


@app.cell
def reload_data(blobs, reload_button, reload_log, shared):
    if reload_button.value > reload_log["done"]:
        shared["tables"] = load_tables(blobs)
        reload_log["done"] = reload_button.value
    return


@app.cell
def run_clicked_cells(cell_editors, cell_run_buttons, run_log, shared):
    for _key in clicked_cells(cell_run_buttons.value, run_log["done"]):
        run_log["outputs"][_key] = run_code(cell_editors[_key].value, make_namespace(shared["tables"]))
        run_log["done"][_key] = cell_run_buttons.value[_key]
    cell_outputs = dict(run_log["outputs"])
    runs = dict(run_log["done"])
    return cell_outputs, runs


@app.cell(hide_code=True)
def observe_intro(get_prediction, mo, reload_button):
    mo.stop(get_prediction() is None)
    _reloaded = f" Reloaded {reload_button.value} time(s)." if reload_button.value else ""
    mo.vstack([
        mo.Html(stage_header_html(2)),
        mo.md("Each cell below runs as written, with no errors, and each one hides a problem you'll only see if "
              "you look closely. Edit the code and run it again as often as you like; nothing here is marked "
              "right or wrong. Every cell starts from the prepared tables, so one cell can't break another. If "
              f"your code changes `assessments` itself, reload the data.{_reloaded}"),
        reload_button,
    ])
    return


@app.cell(hide_code=True)
def observe_cells(cell_editors, cell_outputs, cell_run_buttons, director_button, get_prediction, get_submitted, mo):
    mo.stop(get_prediction() is None)
    _panels = []
    for _number, (_key, _cell) in enumerate(STARTER_CELLS.items(), 1):
        _result = cell_outputs.get(_key)
        _shown = [mo.md("*Not run yet.*")]
        if _result is not None:
            _shown = []
            if _result["stdout"]:
                _shown.append(mo.md(f"```\n{_result['stdout']}\n```"))
            if _result["size"] is not None:
                _shown.append(mo.md(f"*{_result['size']}*"))
            if _result["shown"] is not None:
                _shown.append(_result["shown"])
            if _result["value"] is not None:
                _shown.append(mo.md(f"```\n{_result['value']}\n```"))
            for _warning in _result["warnings"]:
                _shown.append(mo.callout(mo.md(f"**Warning from Python**\n\n```\n{_warning}\n```"), kind="warn"))
            if _result["error"]:
                _shown.append(mo.callout(mo.md(f"**Error**\n\n```\n{_result['error']}\n```"), kind="danger"))
            if not _shown:
                _shown = [mo.md("*Ran with no output.*")]
        if _key == "single_family":
            _shown.append(mo.callout(DIRECTOR_REPLY, kind="info") if director_button.value else director_button)
        _code = ([mo.md(f"```python\n{cell_editors[_key].value}\n```")] if get_submitted()
                 else [cell_editors[_key], cell_run_buttons[_key]])
        _panels.append(mo.vstack([
            mo.md(f"#### Code cell {_number} of {len(STARTER_CELLS)}: {_cell['title']}\n\n*{_cell['hint']}*"),
            *_code, *_shown,
        ]))
    mo.vstack(_panels, gap=1.5)
    return


@app.cell
def list_controls(mo, slim):
    _residential = sorted(slim.loc[slim["CLASSDESC"] == "RESIDENTIAL", "USEDESC"].dropna().unique())
    boundary_control = mo.ui.radio(options={label: key for key, label in BOUNDARY_LABELS.items()}, value=None,
                                   label="Finding parcels inside TriCOG")
    types_control = mo.ui.multiselect(options={t.capitalize(): t for t in _residential},
                                      label="Home types that count as single-family")
    liens_control = mo.ui.radio(options={label: key for key, label in JOIN_LABELS.items()}, value=None,
                                label="Joining homes to liens")
    combine_control = mo.ui.radio(options={label: key for key, label in JOIN_LABELS.items()}, value=None,
                                  label="Combining the boundary with the homes that have liens")
    cutoff_control = mo.ui.slider(start=0, stop=10000, step=50, value=0, show_value=True,
                                  label="Keep homes whose liens total more than ($)")
    return boundary_control, combine_control, cutoff_control, liens_control, types_control


@app.cell(hide_code=True)
def build_your_list(boundary_control, combine_control, cutoff_control, get_final_settings, get_prediction,
                    get_submitted, liens_control, mo, shared, slim, types_control):
    mo.stop(get_prediction() is None)
    _settings = get_final_settings() if get_submitted() else settings_from_controls(
        boundary_control.value, types_control.value, liens_control.value, combine_control.value,
        cutoff_control.value)
    _controls = ([mo.Html(settings_html(_settings))] if get_submitted()
                 else [boundary_control, types_control, liens_control, combine_control, cutoff_control])
    if _settings is None:
        _list = [mo.md("*Choose an option in each setting to see your list.*")]
    else:
        _tables = shared["tables"]
        _table, _size = shown_table(build_list(slim, _tables["liens"], _tables["boundary"], _settings))
        _list = [mo.md(f"**Your list: {_size}**"), _table]
    mo.vstack([
        mo.md("### Build your list\n\nThese settings turn TriCOG's three rules into a list, in this order: "
              "boundary, home type, liens, combining, cutoff. Homes with no lien amount stay on the list at any "
              "cutoff."),
        *_controls, *_list,
    ])
    return


@app.cell(hide_code=True)
def observe_gate(get_prediction, mo, runs):
    mo.stop(get_prediction() is None)
    _waiting = [cell["title"] for key, cell in STARTER_CELLS.items() if runs.get(key, 0) == 0]
    (mo.callout(f"Run every code cell at least once to continue to Stage 3. Still to run: {', '.join(_waiting)}.",
                kind="neutral") if _waiting else mo.md("*You've run every cell. Stage 3 is below.*"))
    return


@app.cell
def explain_inputs(mo):
    get_explain, set_explain = mo.state({f"r{i}": "" for i in range(1, len(EXPLAIN_PROMPTS) + 1)})
    submit_button = mo.ui.run_button(label="Submit for evaluation", kind="success")
    return get_explain, set_explain, submit_button


@app.cell
def explain_fields(mo, set_explain):
    # Created once here, so re-running the explain cell never wipes what the learner typed.
    explain_fields = {
        f"r{i}": mo.ui.text_area(rows=5, full_width=True, on_change=functools.partial(record_field, set_explain, f"r{i}"))
        for i in range(1, len(EXPLAIN_PROMPTS) + 1)
    }
    return (explain_fields,)


@app.cell
def submit_action(boundary_control, combine_control, cutoff_control, get_explain, liens_control, mo,
                  set_final_settings, set_submitted, submit_button, types_control):
    _settings = settings_from_controls(boundary_control.value, types_control.value, liens_control.value,
                                       combine_control.value, cutoff_control.value)
    _ready = can_submit(get_explain()) and _settings is not None
    if submit_button.value and _ready:
        set_final_settings(_settings)
        set_submitted(True)
    submit_warning = (mo.callout("Answer all three questions and choose every list setting before you submit.",
                                 kind="warn") if submit_button.value and not _ready else "")
    return (submit_warning,)


@app.cell(hide_code=True)
def explain(explain_fields, get_explain, get_prediction, get_submitted, mo, runs, submit_button, submit_warning):
    mo.stop(not explain_unlocked(get_prediction(), runs))
    _header = [mo.Html(stage_header_html(3)), mo.Html(locked_prediction_html(get_prediction()))]
    if get_submitted():
        _answers = "".join(f"<p><b>{html.escape(q)}</b><br>{paragraph_html(get_explain()[f'r{i}'])}</p>"
                           for i, q in enumerate(EXPLAIN_PROMPTS, 1))
        _output = mo.vstack(_header + [mo.Html(_answers),
                                       mo.callout("Submitted. Your code, list settings and answers are locked.",
                                                  kind="success")])
    else:
        _questions = [item for i, q in enumerate(EXPLAIN_PROMPTS, 1)
                      for item in (mo.md(f"**{i}.** {q}"), explain_fields[f"r{i}"])]
        _output = mo.vstack(_header + _questions + [
            mo.md("Submitting locks your code cells, your list settings and these answers, then shows your evaluation."),
            submit_button, submit_warning,
        ])
    _output
    return


@app.cell(hide_code=True)
def evaluate(get_explain, get_final_settings, get_prediction, get_submitted, mo, shared, slim):
    # One cell with the download: a separate cell would re-run (and fail) whenever the Explain answers change.
    mo.stop(not get_submitted())
    _tables = shared["tables"]
    _evaluation = evaluation_html(slim, _tables["liens"], _tables["boundary"], get_final_settings(), get_prediction())
    _doc = report_html(get_prediction(), get_final_settings(), get_explain(), _evaluation)
    mo.vstack([
        mo.Html(stage_header_html(4)), mo.Html(_evaluation),
        mo.md("### Download your brief\n\nThe file holds your prediction, your list settings, your reflection and "
              "this evaluation. It opens in any browser; use **Print → Save as PDF** for a PDF."),
        mo.download(data=_doc.encode("utf-8"), filename="tricog_brief.html", mimetype="text/html",
                    label="Download brief (.html)"),
        mo.md("*Nothing is saved online. Refreshing or closing this page erases your work, so download before you leave.*"),
    ])
    return


@app.cell
def _():
    import marimo as mo
    return (mo,)


if __name__ == "__main__":
    app.run()
