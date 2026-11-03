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
    import math
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
        "lien: 53,858 rows, 46,144 of them owing nothing. Task 6's example joins every home in the area, so it prints more. "
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
            "text": "Across the Mon Valley and Pittsburgh's eastern suburbs, many houses stand empty. Owners move "
                    "away or die, taxes go unpaid, and the houses decay. An empty house costs its neighbours: lower "
                    "property values, pests and break-ins, and more spending by the town on inspections, police "
                    "and fire calls. In 2017, two councils of governments here set up the Tri-COG Land Bank to break "
                    "that cycle. Pennsylvania's Land Bank Act lets it take over vacant, tax-delinquent properties, "
                    "clear their titles, and sell them to people who will live in them or fix them up. The same law "
                    "limits it: TriCOG can act only in the municipalities that have joined it.",
        },
        "role": {
            "title": "Your role",
            "text": "You've just started as an intern on TriCOG's small staff. You work with the land bank's GIS "
                    "and data analyst, who looks after the maps and county records. The director, who runs the "
                    "land bank, wants a first list of homes to look at before the next round of purchases. The "
                    "analyst has handed the data work to you. You can ask the director questions while you work.",
        },
        "deliver": {
            "title": "What you deliver",
            "text": "A list of parcels that meet three rules: inside TriCOG's member municipalities, a single-family "
                    "home, and signs of abandonment. No dataset says which homes are abandoned, so the director "
                    "suggests tax liens as the clue: an owner who walks away stops paying property tax. With the "
                    "list, you write a short note to the director: how you built it, how far to trust it, and who "
                    "could be hurt if it's wrong. The list has real effects. Staff will visit these homes, and "
                    "their owners may get letters.",
        },
        "words": {
            "title": "Words you'll meet",
            "text": "Parcel: one piece of land with its own ID, usually a house with its yard and driveway.\n"
                    "Municipality: a town, borough or township with its own local government. TriCOG's boundary "
                    "file holds 30 of them.\n"
                    "Tax delinquency: being behind on property tax. Paying what's owed ends it.\n"
                    "Tax lien: a legal claim on a property for unpaid tax. It has to be paid off before the "
                    "property can be sold.\n"
                    "Coordinate system: the way a map file turns places into numbers, such as feet on a "
                    "Pennsylvania grid or degrees of longitude and latitude.",
        },
    }
    STAGE_INTROS = {
        1: "Before you open the data, decide what you expect. You'll lock four answers here and come back to them "
           "at the end. Nobody grades them.",
        2: "You'll build the director's list in eight tasks. Each task shows you some of the data first and says in "
           "plain words what to do, and you write the code. What you save in one task is there for the next, and "
           "task 8 saves your finished list as my_list.",
        3: "Look back at what you predicted and what the data showed. Your answers go to the director with your list.",
        4: "Your list is compared with the one that follows TriCOG's three rules at your own cutoff. Each card counts "
           "one difference and says what it would mean for real households.",
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
    # Pitt Royal for headings and links, a Pitt Gold rule under stage headings; structure from size and weight only.
    STYLE = """
    .tc-doc{font-family:Georgia,"Times New Roman",serif;color:#222;font-size:15px;line-height:1.55}
    .tc-doc p{margin:6px 0}
    .tc-doc a{color:#003594}
    .tc-title{font-family:Georgia,"Times New Roman",serif;color:#003594;font-size:30px;font-weight:700;line-height:1.2;margin:16px 0 18px}
    .tc-stage h2{color:#003594;font-size:23px;font-weight:700;margin:36px 0 6px;padding-bottom:4px;border-bottom:3px solid #FFB81C}
    .tc-task{color:#003594;font-size:18px;font-weight:700;margin:22px 0 4px}
    .tc-sub{font-size:15px;font-weight:700;margin:14px 0 4px}
    .tc-card{margin:16px 0}
    .tc-card h4,.tc-eval h4{color:#003594;font-size:18px;font-weight:700;margin:0 0 4px}
    .tc-h3{color:#003594;font-size:18px;font-weight:700;margin:24px 0 6px}
    .tc-eval{border-top:1px solid #ccc;padding-top:8px;margin:14px 0}
    .tc-eval dt{font-weight:700;margin-top:6px}
    .tc-eval dd{margin:0 0 4px 0}
    .tc-list{list-style:disc;padding-left:1.5em}
    ol.tc-list{list-style:decimal}
    .tc-list li{margin:4px 0}
    """

    STDOUT_LIMIT = 5000
    DIRECTOR_QUESTIONS = (
        ("Do townhouses or rowhouses count as single-family homes?",
         "We mean single-family houses only: rows where CLASSDESC is RESIDENTIAL and USEDESC is SINGLE FAMILY. "
         "Not townhouses, rowhouses, two- to four-family homes or vacant land. Our program can't take those on."),
        ("How many homes can we buy this year?",
         "A few dozen, so the list has to be one we can trust."),
        ("When do you need the list?",
         "By the end of the month, so take the time to check it."),
        ("Can we buy homes just outside our towns?",
         "No. By law we can buy only inside our member municipalities."),
    )
    TASKS = {
        "files": {
            "title": "Look at the files",
            "director": "The analyst left you four tables. Before anything else, find out what is in each one.",
            "hint": "Look at each table's size and first rows. Two of the tables can be drawn on a map. Find out "
                    "which two, and what coordinate system each of them uses. Nothing needs saving here.",
            "functions": "len(table), table.head(), table.columns, table.crs",
            "example": textwrap.dedent("""\
                tables = {"assessments": assessments, "liens": liens, "parcels": parcels, "tricog": tricog}
                for name, table in tables.items():
                    print(name, table.shape, getattr(table, "crs", "no shapes"))"""),
            "saves": (),
        },
        "names": {
            "title": "Try the quick way: match town names",
            "director": "The assessments have a town column. Can you start by keeping the rows from our 30 towns?",
            "hint": "Make both lists of town names look the same: upper case, with no spaces at the ends. Keep the "
                    "assessment rows whose town is on TriCOG's list and save them as inside_by_name. To see where "
                    "they are, pick out the parcels with the same IDs and draw them as dots.",
            "functions": "series.str.upper(), series.str.strip(), series.isin(values), "
                         "parcels[parcels['PIN'].isin(ids)], shapes.centroid.plot(markersize=1)",
            "example": textwrap.dedent("""\
                tricog_names = set(tricog["NAME"].str.upper())
                town = assessments["MUNIDESC"].str.strip().str.upper()
                inside_by_name = assessments[town.isin(tricog_names)]
                parcels[parcels["PIN"].isin(inside_by_name["PARID"])].centroid.plot(markersize=1)"""),
            "saves": ("inside_by_name",),
        },
        "map": {
            "title": "Use the map instead",
            "director": "Try the map as well. TriCOG's boundary file shows exactly where our towns are.",
            "hint": "Keep the parcels whose shapes fall inside TriCOG's boundary and save them as inside_tricog. "
                    "Check how many you got, then draw them as dots. Keep parcels as the first table: clipping "
                    "TriCOG by every parcel can crash this page.",
            "functions": "gp.clip(shapes, mask), shapes.to_crs(other.crs), len(table), shapes.centroid.plot(markersize=1)",
            "example": textwrap.dedent("""\
                inside_tricog = gp.clip(parcels, tricog)
                len(inside_tricog)"""),
            "saves": ("inside_tricog",),
        },
        "clip": {
            "title": "Check what the clip gives back",
            "director": "Before you trust the clip, try it on a small area and look closely at the rows it returns.",
            "hint": "The box starts with sample, a small square of parcels around Braddock. Clip one layer with "
                    "the other and look at what kind of rows come back.",
            "functions": "gp.clip(shapes, mask), shapes.to_crs(other.crs), table.head()",
            "starter": "sample = parcels.cx[1_376_000:1_380_000, 394_000:398_000]\n# Your code here",
            "example": textwrap.dedent("""\
                tricog_feet = tricog.to_crs(parcels.crs)
                gp.clip(tricog_feet, sample)"""),
            "saves": (),
        },
        "single_family": {
            "title": "Keep the single-family homes",
            "director": "We buy single-family homes. Find them in the assessments.",
            "hint": "Look at the CLASSDESC and USEDESC columns in the table above. Keep the residential parcels "
                    "used as single-family homes and save them as homes. If you aren't sure what counts, ask the "
                    "director.",
            "functions": "table[table['COLUMN'] == 'VALUE'], (condition_1) & (condition_2), series.value_counts()",
            "example": textwrap.dedent("""\
                homes = assessments[assessments["USEDESC"] == "SINGLE FAMILY"]
                len(homes)"""),
            "saves": ("homes",),
        },
        "liens": {
            "title": "Attach the liens",
            "director": "Now find out which of those homes have tax liens, and how much is owed.",
            "hint": "Attach each home's lien amount from the liens table, matching the home's PARID to the lien's "
                    "pin. Decide what should happen to homes that have no lien, and save the result as "
                    "homes_with_liens. Count the rows before and after. You could also look homes up one at a "
                    "time; time that on a few hundred homes first.",
            "functions": "pd.merge(left, right, left_on=..., right_on=..., how=...), series.isna().sum(), time.time()",
            "example": textwrap.dedent("""\
                start = time.time()
                for parid in homes["PARID"].head(300):
                    match = liens[liens["pin"] == parid]
                print(f"300 homes, one at a time: {time.time() - start:.1f} s")
                homes_with_liens = pd.merge(homes, liens, left_on="PARID", right_on="pin", how="left")
                len(homes), len(homes_with_liens)"""),
            "saves": ("homes_with_liens",),
        },
        "combine": {
            "title": "Put the three rules together",
            "director": "Combine your results into one list of homes that pass all three rules.",
            "hint": "Join the parcels in inside_tricog to the homes in homes_with_liens on their parcel IDs and "
                    "save the result as candidates. Then check whether every row passes all three rules.",
            "functions": "pd.merge(left, right, left_on=..., right_on=..., how=...), table[['PIN']], len(table)",
            "example": textwrap.dedent("""\
                candidates = pd.merge(inside_tricog[["PIN"]], homes_with_liens, left_on="PIN", right_on="PARID", how="left")
                len(candidates)"""),
            "saves": ("candidates",),
        },
        "amounts": {
            "title": "Decide which liens count",
            "director": "Some liens are tiny. Decide how much a home must owe before we treat it as abandoned.",
            "hint": "Look at the spread of lien amounts above. Choose a cutoff and save it as my_cutoff. Keep the "
                    "candidates whose lien is above it and save them as my_list. Draw your list as dots to see "
                    "where the homes are.",
            "functions": "table[table['total_amount'] > number], series.describe(), shapes.centroid.plot(markersize=1)",
            "example": textwrap.dedent("""\
                my_cutoff = 0
                my_list = candidates[candidates["total_amount"] > my_cutoff]
                len(my_list)"""),
            "saves": ("my_cutoff", "my_list"),
        },
    }
    for _task in TASKS.values():
        _task.setdefault("starter", "# Your code here")


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
def town_name(munidesc: str) -> str:
    return munidesc.split("-")[-1].strip()


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
def task_preview(key: str, tables: dict):
    """What the learner sees before writing code, built only from the prepared tables (never the answer)."""
    assessments, liens, parcels, tricog = (tables[name] for name in ("assessments", "liens", "parcels", "tricog"))
    if key == "files":
        return pd.DataFrame([{"table": name, "rows": len(t), "columns": t.shape[1],
                              "coordinate system": str(getattr(t, "crs", "no shapes"))}
                             for name, t in (("assessments", assessments), ("liens", liens),
                                             ("parcels", parcels), ("tricog", tricog))])
    if key == "names":
        towns = assessments["MUNIDESC"].value_counts().rename_axis("Town in the assessments").reset_index(name="Rows")
        names = pd.Series(sorted(tricog["NAME"]), name="TriCOG's list")
        return pd.concat([names, towns], axis=1).fillna("")
    if key == "map":
        return pd.DataFrame([{"table": name, "coordinate system": str(t.crs),
                              "x from": round(t.total_bounds[0], 2), "x to": round(t.total_bounds[2], 2),
                              "y from": round(t.total_bounds[1], 2), "y to": round(t.total_bounds[3], 2)}
                             for name, t in (("parcels", parcels), ("tricog", tricog))])
    if key == "clip":
        sample = parcels.cx[1_376_000:1_380_000, 394_000:398_000]
        return f"The sample holds {len(sample):,} parcels in a small square around Braddock."
    if key == "single_family":
        return assessments.groupby(["CLASSDESC", "USEDESC"]).size().rename("Rows").reset_index().sort_values(
            "Rows", ascending=False).head(40)
    if key == "liens":
        return liens.head(20)
    if key == "combine":
        return ("So far you have saved inside_tricog (task 3), homes (task 5) and homes_with_liens (task 6). "
                "Print the length of each before you combine them.")
    single_family = assessments[(assessments["CLASSDESC"] == "RESIDENTIAL") & (assessments["USEDESC"] == "SINGLE FAMILY")]
    owed = single_family.merge(liens, left_on="PARID", right_on="pin")["total_amount"]
    return owed.describe().rename("Liens on single-family homes in the area").to_frame()


@app.function
def explain_unlocked(prediction, runs: dict) -> bool:
    return prediction is not None and all(runs.get(key, 0) >= 1 for key in TASKS)


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
def checking_numbers(slim, your_count: int, guess: str) -> dict:
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
def stage_header_html(stage: int) -> str:
    return (f"<div class='tc-doc tc-stage'><h2>Stage {stage}: {STAGES[stage - 1]}</h2>"
            f"<p>{html.escape(STAGE_INTROS[stage], quote=False)}</p></div>")


@app.function
def paragraph_html(text: str) -> str:
    return html.escape(text.strip()).replace("\n", "<br>") if text.strip() else "<i>(left blank)</i>"


@app.function
def opening_cards_html() -> str:
    cards = "".join(f"<div class='tc-card'><h4>{html.escape(card['title'])}</h4><p>{paragraph_html(card['text'])}</p></div>"
                    for card in OPENING_CARDS.values())
    return (f"<style>{STYLE}</style><div class='tc-doc'><h1 class='tc-title'>Finding abandoned homes for the TriCOG "
            f"Land Bank</h1>{cards}</div>")


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
def list_ids(my_list):
    """The parcel IDs on the learner's list, from the first ID column their joins kept; None if there is none."""
    if not isinstance(my_list, pd.DataFrame):
        return None
    for column in ("PARID", "PIN", "pin"):
        if column in my_list.columns:
            return my_list[column]
    return None


@app.function
def is_number(value) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


@app.function
def resolve_cutoff(my_cutoff, ids, liens) -> tuple:
    if is_number(my_cutoff):
        return float(my_cutoff), ""
    owed = liens.loc[liens["pin"].isin(ids), "total_amount"]
    if owed.empty:
        return 0.0, "You didn't save a number as my_cutoff, and no home on your list has a lien, so this uses $0."
    value = float(owed.min()) - 0.01
    return value, (f"You didn't save a number as my_cutoff, so this uses ${value:,.2f}, just under the smallest lien "
                   "on your list.")


@app.function
def list_differences(ids, slim, liens, boundary, cutoff: float) -> dict:
    """Why the learner's list differs from the correct one at their cutoff. Each parcel gets the first reason
    that applies, so the counts add up."""
    reference = reference_list(slim, liens, boundary, cutoff)
    listed = pd.Series(ids.unique(), name="PARID")
    extra = listed[~listed.isin(reference["PARID"])]
    inside = set(boundary.loc[boundary["by_map"], "PARID"])
    records = slim.drop_duplicates("PARID").set_index("PARID")
    owed = liens.drop_duplicates("pin").set_index("pin")["total_amount"]
    reasons = {"outside": 0, "not_single_family": {}, "no_lien": 0, "below_cutoff": 0}
    for parid in extra:
        if parid not in inside:
            reasons["outside"] += 1
        elif parid not in records.index or records.at[parid, "CLASSDESC"] != "RESIDENTIAL" or \
                records.at[parid, "USEDESC"] not in REFERENCE_SETTINGS["types"]:
            kind = records.at[parid, "USEDESC"] if parid in records.index else "no record"
            kind = kind if isinstance(kind, str) else "no record"
            reasons["not_single_family"][kind] = reasons["not_single_family"].get(kind, 0) + 1
        elif parid not in owed.index or pd.isna(owed.at[parid]):
            reasons["no_lien"] += 1
        else:
            reasons["below_cutoff"] += 1
    missing = reference[~reference["PARID"].isin(listed)]
    towns = missing["MUNIDESC"].map(town_name)
    ward = towns.str.upper().isin(("MCKEESPORT", "CLAIRTON"))
    return {
        **reasons,
        "not_single_family": dict(sorted(reasons["not_single_family"].items(), key=lambda item: -item[1])),
        "duplicates": int(len(ids) - ids.nunique()),
        "ward_towns": towns[ward].value_counts().to_dict(),
        "other": int((~ward).sum()),
        "listed": int(listed.size),
        "reference": len(reference),
    }


@app.function
def reason_cards_html(diff: dict) -> str:
    cards = []
    if diff["outside"]:
        cards.append(eval_card_html("outside", "Parcels outside TriCOG", (
            ("The count", f"{diff['outside']:,} parcels on your list are outside TriCOG's member municipalities."),
            ("What happens", "By law the land bank can't buy them, so staff time goes into homes it can never take on."),
        )))
    if diff["not_single_family"]:
        total = sum(diff["not_single_family"].values())
        multi = sum(count for kind, count in diff["not_single_family"].items() if kind in MULTI_FAMILY)
        happens = "TriCOG makes offers on property its program can't use."
        if multi:
            happens += f" {multi:,} are two- to four-family homes, where tenants could lose their homes."
        cards.append(eval_card_html("not_single_family", "Parcels that aren't single-family homes", (
            ("The count", f"{total:,} parcels on your list: "
                          f"{counts_text(diff['not_single_family'], lambda kind: kind.lower())}."),
            ("What happens", happens),
        )))
    if diff["no_lien"]:
        cards.append(eval_card_html("no_lien", "Homes with no lien", (
            ("The count", f"{diff['no_lien']:,} homes on your list owe nothing."),
            ("What happens", "Letters suggesting their home could be taken go to households that owe nothing."),
        )))
    if diff["below_cutoff"]:
        cards.append(eval_card_html("below_cutoff", "Homes under your own cutoff", (
            ("The count", f"{diff['below_cutoff']:,} homes on your list owe no more than the cutoff you saved."),
            ("What happens", "Your list includes homes your own rule meant to leave out."),
        )))
    if diff["duplicates"]:
        cards.append(eval_card_html("duplicates", "The same parcel more than once", (
            ("The count", f"{diff['duplicates']:,} extra rows repeat a parcel already on your list."),
            ("What happens", "The same household could be visited or written to twice."),
        )))
    if diff["ward_towns"]:
        missed = sum(diff["ward_towns"].values())
        cards.append(eval_card_html("ward_towns", "Homes missing from McKeesport and Clairton", (
            ("The count", f"{missed:,} homes are missing: "
                          f"{counts_text(diff['ward_towns'], lambda name: 'in ' + town_label(name))}."),
            ("Why", "Their assessment records are split into wards, so the town names never match TriCOG's list."),
            ("What happens", "Eligible empty houses in those towns are never considered, and TriCOG's effort "
                             "shifts away from them."),
        )))
    if diff["other"]:
        cards.append(eval_card_html("other", "Other homes missing from your list", (
            ("The count", f"{diff['other']:,} homes that meet every rule at your cutoff aren't on your list."),
            ("What happens", "If they are empty, they stay empty."),
        )))
    return "".join(cards)


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
def checking_html(numbers: dict, reference_count) -> str:
    bigger = (" Your list has more rows than that." if numbers["your_count"] > numbers["single_family_in_area"]
              else "")
    compare = ("" if reference_count is None else
               f" The list that follows TriCOG's three rules at your cutoff has {reference_count:,}.")
    items = (
        f"Clipping across two coordinate systems returns {numbers['mismatched_clip_rows']} rows.",
        f"Clipping TriCOG by the Braddock sample returns {numbers['reversed_clip_rows']} rows: towns, not parcels.",
        f"The whole prepared area holds {numbers['single_family_in_area']:,} single-family homes, so a list "
        f"larger than that can't be a list of homes.{bigger}",
        f"You guessed {numbers['guess']}. Your list has {numbers['your_count']:,} rows ({numbers['your_bucket']})."
        + compare,
    )
    return "<ul class='tc-list'>" + "".join(f"<li>{html.escape(item)}</li>" for item in items) + "</ul>"


@app.function
def evaluation_html(slim, liens, boundary, my_list, my_cutoff, prediction: dict) -> str:
    ids = list_ids(my_list)
    facts = "".join(f"<li>{html.escape(fact, quote=False)}</li>" for fact in HIDDEN_FACTS)
    part_three = f"<h3 class='tc-h3'>Part 3 · What the data was hiding</h3><ol class='tc-list'>{facts}</ol>"
    your_count = len(my_list) if isinstance(my_list, (pd.DataFrame, pd.Series)) else 0
    if ids is None:
        numbers = checking_numbers(slim, your_count, prediction["bucket"])
        return ("<p>Your my_list has no parcel-ID column (PARID, PIN or pin), so it can't be compared with the "
                "correct list. Parts 2 and 3 still apply.</p><h3 class='tc-h3'>Part 2 · Numbers worth checking</h3>"
                + checking_html(numbers, None) + part_three)
    cutoff, note = resolve_cutoff(my_cutoff, ids, liens)
    diff = list_differences(ids, slim, liens, boundary, cutoff)
    numbers = checking_numbers(slim, your_count, prediction["bucket"])
    cutoff_note = f"<p>{html.escape(note)}</p>" if note else ""
    return (
        "<h3 class='tc-h3'>Part 1 · Your list</h3><p>Your list is compared with the list that follows TriCOG's "
        "three rules at your own cutoff. Each card counts one reason the two differ.</p>" + cutoff_note
        + reason_cards_html(diff) + cutoff_card_html(cutoff_card(slim, liens, boundary, cutoff), cutoff)
        + "<h3 class='tc-h3'>Part 2 · Numbers worth checking</h3>" + checking_html(numbers, diff["reference"])
        + part_three
    )


@app.function
def report_html(prediction: dict, list_summary: dict, explain: dict, evaluation: str) -> str:
    answers = "".join(f"<h3>{html.escape(q)}</h3><p>{paragraph_html(explain.get(f'r{i}', ''))}</p>"
                      for i, q in enumerate(EXPLAIN_PROMPTS, 1))
    return (
        "<!doctype html><html><head><meta charset='utf-8'><title>TriCOG Land Bank brief</title>"
        f"<style>body{{font-family:system-ui,sans-serif;max-width:760px;margin:2em auto;line-height:1.5}}{STYLE}</style>"
        "</head><body><h1>TriCOG Land Bank brief</h1>"
        f"<h2>My prediction</h2>{locked_prediction_html(prediction)}"
        f"<h2>My list</h2><p>{list_summary['rows']:,} rows, lien cutoff ${list_summary['cutoff']:,.2f}</p>"
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
        key: mo.ui.code_editor(value=cell["starter"], language="python", min_height=100)
        for key, cell in TASKS.items()
    }
    cell_run_buttons = mo.ui.dictionary({
        key: mo.ui.button(value=0, on_click=lambda count: count + 1, label="Run") for key in TASKS
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
    for _number, (_key, _cell) in enumerate(TASKS.items(), 1):
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
            _shown.append(mo.callout(DIRECTOR_QUESTIONS[0][1], kind="info") if director_button.value else director_button)
        _code = ([mo.md(f"```python\n{cell_editors[_key].value}\n```")] if get_submitted()
                 else [cell_editors[_key], cell_run_buttons[_key]])
        _panels.append(mo.vstack([
            mo.md(f"#### Code cell {_number} of {len(TASKS)}: {_cell['title']}\n\n*{_cell['hint']}*"),
            *_code, *_shown,
        ]))
    mo.vstack(_panels, gap=1.5)
    return


@app.cell(hide_code=True)
def observe_gate(get_prediction, mo, runs):
    mo.stop(get_prediction() is None)
    _waiting = [cell["title"] for key, cell in TASKS.items() if runs.get(key, 0) == 0]
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
def submit_action(get_explain, mo, set_final_settings, set_submitted, submit_button):
    _ready = can_submit(get_explain())
    if submit_button.value and _ready:
        set_final_settings({"my_list": None, "my_cutoff": None})
        set_submitted(True)
    submit_warning = (mo.callout("Answer all three questions before you submit.", kind="warn")
                      if submit_button.value and not _ready else "")
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
    _final = get_final_settings()
    _evaluation = evaluation_html(slim, _tables["liens"], _tables["boundary"], _final["my_list"], _final["my_cutoff"],
                                  get_prediction())
    _doc = report_html(get_prediction(), {"rows": 0, "cutoff": 0.0}, get_explain(), _evaluation)
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
