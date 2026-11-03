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
    import numbers
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
    # What each trap does to a list built at the reference settings, from answer_key.json (CONCRETE/docs/tclb_poee).
    TRAP_NUMBERS = {
        "names_missed": 2351,
        "extra_rowhouse_townhouse": 575,
        "extra_two_to_four": 643,
        "extra_vacant_land": 9330,
        "liens_left_no_lien": 46144,
        "under_100": 420,
        "under_1000": 3126,
        "median_lien": 1479.46,
        "reversed_sample_rows": 5,
    }
    # One row per trap in Evaluate. Designed traps come first, in task order; the last four appear only when a
    # list has some.
    TRAPS = {
        "names": {
            "title": "Matching town names", "task": 2,
            "what": "McKeesport and Clairton records are split into wards (\"1st Ward - McKEESPORT\"), and some "
                    "border homes are recorded under a neighbouring town, so their names never match TriCOG's list.",
            "fall_in": f"{TRAP_NUMBERS['names_missed']:,} homes missed",
            "costs": "TriCOG never looks at empty houses in two of its own towns.",
            "households": "Eligible empty houses in those towns stay empty, and the program's effort shifts elsewhere.",
        },
        "crs": {
            "title": "Two coordinate systems", "task": 3,
            "what": "Parcels are in feet and TriCOG is in longitude and latitude. Clipping one by the other returns "
                    "0 rows, with only a warning.",
            "fall_in": "Every home: the list comes out empty",
            "costs": "No list to send, or days spent finding out why.",
            "households": "No empty house gets looked at this year.",
        },
        "reversed": {
            "title": "Clipping with the tables swapped", "task": 4,
            "what": f"gp.clip returns rows of the table you pass first. With TriCOG first, the Braddock sample gives "
                    f"back {TRAP_NUMBERS['reversed_sample_rows']} town shapes, not parcels.",
            "fall_in": "No homes at all: the list holds towns",
            "costs": "Nothing on the list can be sent a letter.",
            "households": "No empty house gets looked at this year.",
        },
        "types": {
            "title": "Home types", "task": 5,
            "what": "Residential parcels carry 25 use codes. The director counts only single-family homes, not "
                    "townhouses.",
            "fall_in": f"{TRAP_NUMBERS['extra_rowhouse_townhouse']:,} rowhouses and townhouses, "
                       f"{TRAP_NUMBERS['extra_two_to_four']:,} two- to four-family homes, "
                       f"{TRAP_NUMBERS['extra_vacant_land']:,} vacant lots",
            "costs": "Offers go out on property the program can't use.",
            "households": "In two- to four-family homes, tenants could lose their homes.",
        },
        "no_lien": {
            "title": "Homes that owe nothing", "task": 6,
            "what": "A left join keeps every home, whether or not it has a lien.",
            "fall_in": f"{TRAP_NUMBERS['liens_left_no_lien']:,} extra homes",
            "costs": "Staff time goes on homes that aren't behind on anything.",
            "households": "Letters suggesting their home could be taken reach people who owe nothing.",
        },
        "cutoff": {
            "title": "Your lien cutoff", "task": 8,
            "what": "No column says whether a home is abandoned. A lien is only a clue, and a small debt is a weak one.",
            "fall_in": f"At $0: {TRAP_NUMBERS['under_100']:,} homes owe under $100, {TRAP_NUMBERS['under_1000']:,} "
                       f"under $1,000. Half owe less than ${TRAP_NUMBERS['median_lien']:,.2f}.",
            "costs": "Set it high and abandoned homes drop off the list.",
            "households": "Set it low and letters reach families still living there over a small debt.",
        },
        "outside": {
            "title": "Parcels outside TriCOG", "task": None,
            "what": "Parcels on your list that lie outside TriCOG's member municipalities.",
            "fall_in": "n/a",
            "costs": "By law the land bank can't buy them.",
            "households": "Staff time goes into homes TriCOG can never take on.",
        },
        "not_home": {
            "title": "Parcels that aren't homes", "task": None,
            "what": "Parcels whose class isn't residential, such as shops, municipal buildings and commercial land. "
                    "A left join when combining in task 7 brings them in.",
            "fall_in": "n/a",
            "costs": "Offers go out on property the program can't use.",
            "households": "Letters reach owners the program was never meant for.",
        },
        "duplicates": {
            "title": "The same parcel more than once", "task": None,
            "what": "The same parcel appears more than once.",
            "fall_in": "n/a",
            "costs": "Staff work the same home twice.",
            "households": "The same household could be written to twice.",
        },
        "other": {
            "title": "Other homes missing", "task": None,
            "what": "Homes that meet every rule at your cutoff but aren't on your list.",
            "fall_in": "n/a",
            "costs": "Homes that meet every rule aren't considered.",
            "households": "If they are empty, they stay empty.",
        },
    }
    DESIGNED_TRAPS = ("names", "crs", "reversed", "types", "no_lien")
    EXTRA_TRAPS = ("outside", "not_home", "duplicates", "other")
    NOT_IN_LIST = "Not in your final list"
    CANT_TELL = "Can't tell: your list has no parcel IDs."

    STAGES =("Predict", "Observe", "Explain", "Evaluate")
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
    .tc-card h4{color:#003594;font-size:18px;font-weight:700;margin:0 0 4px}
    .tc-h3{color:#003594;font-size:18px;font-weight:700;margin:24px 0 6px}
    .tc-counts{border-collapse:collapse;margin:8px 0}
    .tc-counts td{padding:3px 28px 3px 0;border-bottom:1px solid #e3e3e3}
    .tc-counts td.num{text-align:right}
    .tc-scroll{overflow-x:auto;max-width:100%}
    .tc-traps{border-collapse:collapse;width:100%;min-width:760px;font-size:14px}
    .tc-traps th,.tc-traps td{border-bottom:1px solid #ddd;padding:8px 10px 8px 0;text-align:left;vertical-align:top}
    .tc-traps th{color:#003594}
    .tc-traps .tc-task-no{color:#666}
    .tc-list{list-style:disc;padding-left:1.5em}
    ol.tc-list{list-style:decimal}
    .tc-list li{margin:4px 0}
    """

    CODE_BLOCK_STYLE = ("font-family:Menlo,ui-monospace,monospace;font-size:13px;border:1px solid #ccc;"
                        "padding:8px 10px;overflow-x:auto;white-space:nowrap;max-width:100%")

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
def list_ready(namespace: dict) -> bool:
    return isinstance(namespace.get("my_list"), pd.DataFrame)


@app.function
def frozen_list(namespace: dict) -> dict:
    """The learner's list and cutoff as they were at Submit; later changes to the namespace can't reach them."""
    my_list = namespace.get("my_list")
    return {"my_list": my_list.copy() if isinstance(my_list, (pd.DataFrame, pd.Series)) else my_list,
            "my_cutoff": namespace.get("my_cutoff")}


@app.function
def list_summary(frozen: dict, liens) -> dict:
    ids = list_ids(frozen["my_list"])
    rows = len(frozen["my_list"]) if isinstance(frozen["my_list"], pd.DataFrame) else 0
    cutoff = resolve_cutoff(frozen["my_cutoff"], ids, liens)[0] if ids is not None else 0.0
    return {"rows": rows, "cutoff": cutoff}


@app.function
def code_block_html(text: str) -> str:
    """Code or output as monospace HTML whose line breaks and indents survive being embedded in other HTML."""
    lines = [html.escape(line).replace("  ", "&nbsp;&nbsp;") for line in text.split("\n")]
    # Styled inline: page CSS doesn't reach inside marimo's folds.
    return (f"<div class='tc-code' style='{CODE_BLOCK_STYLE}'>" + "<br>".join(lines) + "</div>")


@app.function
def task_output_parts(mo, result: dict | None) -> list:
    """What one task's last run produced, as plain page elements (no coloured boxes)."""
    if result is None:
        return [mo.md("*Not run yet.*")]
    parts = []
    if result["stdout"]:
        parts.append(mo.Html(code_block_html(result["stdout"])))
    if result["size"] is not None:
        parts.append(mo.md(f"*{result['size']}*"))
    if result["shown"] is not None:
        parts.append(result["shown"])
    if result["value"] is not None:
        parts.append(mo.Html(code_block_html(result["value"])))
    if result["figure"] is not None:
        parts.append(mo.Html(result["figure"]))
    for warning in result["warnings"]:
        parts.append(mo.Html("<div class='tc-doc'><p class='tc-sub'>Python's warning</p></div>" + code_block_html(warning)))
    if result["error"]:
        parts.append(mo.Html("<div class='tc-doc'><p class='tc-sub'>Python's error</p></div>" + code_block_html(result["error"])))
    return parts or [mo.md("*Ran with no output.*")]


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
def id_column(my_list, name: str):
    """One ID column, even when the learner's table repeats the column name."""
    column = my_list[name]
    return column.iloc[:, 0] if isinstance(column, pd.DataFrame) else column


@app.function
def list_ids(my_list):
    """The parcel ID of each row on the learner's list. A left join can leave PARID empty on rows that still have
    a PIN, so each row takes the first ID column that has a value; rows with no ID at all are dropped."""
    if not isinstance(my_list, pd.DataFrame):
        return None
    columns = [name for name in ("PARID", "PIN", "pin") if name in my_list.columns]
    if not columns:
        return None
    ids = id_column(my_list, columns[0])
    for name in columns[1:]:
        ids = ids.fillna(id_column(my_list, name))
    return ids.dropna().rename("PARID").reset_index(drop=True)


@app.function
def is_number(value) -> bool:
    return isinstance(value, numbers.Real) and not isinstance(value, bool) and math.isfinite(value)


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
    reasons = {"outside": 0, "not_home": 0, "home_types": {}, "no_lien": 0, "below_cutoff": 0}
    for parid in extra:
        if parid not in inside:
            reasons["outside"] += 1
        elif parid not in records.index or records.at[parid, "CLASSDESC"] != "RESIDENTIAL":
            reasons["not_home"] += 1
        elif records.at[parid, "USEDESC"] not in REFERENCE_SETTINGS["types"]:
            kind = records.at[parid, "USEDESC"]
            kind = kind if isinstance(kind, str) else "no use code"
            reasons["home_types"][kind] = reasons["home_types"].get(kind, 0) + 1
        elif parid not in owed.index or pd.isna(owed.at[parid]):
            reasons["no_lien"] += 1
        else:
            reasons["below_cutoff"] += 1
    missing = reference[~reference["PARID"].isin(listed)]
    towns = missing["MUNIDESC"].map(town_name).str.upper()
    # A ward town counts as missed by name only when none of its homes made the list.
    listed_towns = set(reference.loc[reference["PARID"].isin(listed), "MUNIDESC"].map(town_name).str.upper())
    ward = towns.isin({"MCKEESPORT", "CLAIRTON"} - listed_towns)
    # Border homes recorded under a non-member town count as missed by name only when the list has none of them.
    listed_munidesc = records.loc[records.index.isin(listed), "MUNIDESC"].dropna().map(town_name).str.upper()
    border_listed = bool((~listed_munidesc.isin(MEMBER_TOWNS)).any())
    border = ~towns.isin(MEMBER_TOWNS) & ~border_listed
    empty = listed.size == 0
    return {
        **reasons,
        "home_types": dict(sorted(reasons["home_types"].items(), key=lambda item: -item[1])),
        "duplicates": int(len(ids) - ids.nunique()),
        "ward_towns": {} if empty else missing.loc[ward, "MUNIDESC"].map(town_name).value_counts().to_dict(),
        "border_towns": 0 if empty else int(border.sum()),
        "other": 0 if empty else int((~ward & ~border).sum()),
        "empty": empty,
        "listed": int(listed.size),
        "reference": len(reference),
    }


@app.function
def plural(count: int, word: str, words=None) -> str:
    return f"{count:,} {word if count == 1 else (words or word + 's')}"


@app.function
def money(value: float) -> str:
    value = float(value)
    return f"${value:,.0f}" if value == round(value) else f"${value:,.2f}"


@app.function
def names_status(diff: dict) -> str:
    ward, border = diff["ward_towns"], diff["border_towns"]
    parts = [counts_text(ward, lambda name: "in " + town_label(name))] if ward else []
    if border:
        parts.append(plural(border, "home") + " recorded under neighbouring towns")
    return f"Yes: {plural(sum(ward.values()) + border, 'home')} missed ({', '.join(parts)})"


@app.function
def cutoff_status(diff: dict, cutoff: float, card: dict) -> str:
    text = (f"Your choice: {money(cutoff)}. On the correct list at that cutoff, {card['under_1000']:,} homes owe "
            f"under $1,000 and {card['removed']:,} homes with liens are removed.")
    if diff["below_cutoff"]:
        text += (f" {plural(diff['below_cutoff'], 'home')} on your list owe {money(cutoff)} or less, which your "
                 "own rule meant to leave out.")
    return text


@app.function
def trap_status(key: str, diff: dict) -> tuple:
    """A designed trap's status, read from the list alone: (text, whether it shows in the list)."""
    if key == "names" and (diff["ward_towns"] or diff["border_towns"]):
        return names_status(diff), True
    if key == "crs" and diff["empty"]:
        return f"Yes: your list is empty, so all {diff['reference']:,} correct homes are missing.", True
    if key == "types" and diff["home_types"]:
        total = sum(diff["home_types"].values())
        return (f"Yes: {plural(total, 'parcel')} on your list: "
                f"{counts_text(diff['home_types'], lambda kind: kind.lower())}"), True
    if key == "no_lien" and diff["no_lien"]:
        return f"Yes: {plural(diff['no_lien'], 'home')} on your list owe nothing.", True
    return NOT_IN_LIST, False


@app.function
def extra_status(key: str, diff: dict) -> str:
    words = {"outside": "parcel", "not_home": "parcel", "duplicates": "extra row", "other": "home"}
    return f"Yes: {plural(diff[key], words[key])}"


@app.function
def trap_row(key: str, status: str, in_list: bool) -> dict:
    return {"key": key, **TRAPS[key], "status": status, "in_list": in_list}


@app.function
def trap_rows(diff: dict, cutoff: float, card: dict) -> list:
    """Designed traps in the list, then the cutoff, then extras the list has, then designed traps it doesn't."""
    designed = [trap_row(key, *trap_status(key, diff)) for key in DESIGNED_TRAPS]
    extras = [trap_row(key, extra_status(key, diff), True) for key in EXTRA_TRAPS if diff[key]]
    cutoff_row = trap_row("cutoff", cutoff_status(diff, cutoff, card), True)
    return ([row for row in designed if row["in_list"]] + [cutoff_row] + extras
            + [row for row in designed if not row["in_list"]])


@app.function
def unreadable_rows(cutoff) -> list:
    status = {"reversed": "Possibly: a list of town shapes has no parcel IDs."}
    if cutoff is not None:
        status["cutoff"] = f"Your choice: {money(cutoff)}."
    return [trap_row(key, status.get(key, CANT_TELL), False) for key in (*DESIGNED_TRAPS, "cutoff")]


@app.function
def counts_table_html(rows: tuple) -> str:
    cells = "".join(f"<tr><td>{html.escape(label)}</td><td class='num'>{count:,}</td></tr>" for label, count in rows)
    return f"<table class='tc-counts'>{cells}</table>"


@app.function
def comparison_html(diff: dict, row_count: int, guess: str, cutoff: float, note: str) -> str:
    """Part 1: the learner's list against the correct one, in distinct parcels."""
    only_yours = (diff["outside"] + diff["not_home"] + sum(diff["home_types"].values()) + diff["no_lien"]
                  + diff["below_cutoff"])
    only_correct = diff["reference"] if diff["empty"] else (
        sum(diff["ward_towns"].values()) + diff["border_towns"] + diff["other"])
    intro = ("TriCOG will send letters to the homes on your list and send staff to look at them. The correct list "
             "is what TriCOG's three rules give when they are applied to the data without slips: inside a member "
             f"town, a single-family home, and liens totalling more than your cutoff. It uses your own cutoff of "
             f"{money(cutoff)}, so any difference comes from how the list was built. Each home that is on only one "
             "of the two lists is a real household: a letter that shouldn't go out, or an empty house nobody visits.")
    counts = counts_table_html((
        ("Parcels on your list", diff["listed"]),
        (f"Homes on the correct list at {money(cutoff)}", diff["reference"]),
        ("On both lists", diff["listed"] - only_yours),
        ("Only on yours: letters that shouldn't go out", only_yours),
        ("Only on the correct list: empty houses nobody looks at", only_correct),
    ))
    no_id = row_count - diff["listed"] - diff["duplicates"]
    rows_line = ("" if row_count == diff["listed"] else
                 f"<p>Your list has {row_count:,} rows: {diff['duplicates']:,} repeat a parcel and {no_id:,} have "
                 "no parcel ID.</p>")
    guess_line = (f"In Predict you guessed {guess} homes. Your list has {plural(diff['listed'], 'parcel')}, in the "
                  f"{count_bucket(diff['listed'])} range. Part 2 shows where the differences come from, and the "
                  "counts there add up to the two \"only\" lines above.")
    note_html = f"<p>{html.escape(note)}</p>" if note else ""
    return f"<p>{html.escape(intro)}</p>{note_html}{counts}{rows_line}<p>{html.escape(guess_line)}</p>"


@app.function
def trap_cell_html(row: dict) -> str:
    task = f" <span class='tc-task-no'>· Task {row['task']}</span>" if row["task"] else ""
    return f"<td><strong>{html.escape(row['title'])}</strong>{task}<br>{html.escape(row['what'])}</td>"


@app.function
def trap_table_html(rows: list) -> str:
    """Part 2: one row per trap, scrolling inside its own box so a narrow window keeps the page width."""
    head = "".join(f"<th>{label}</th>" for label in (
        "The trap", "If you fall in", "In your final list", "What it costs TriCOG", "What it means for households"))
    body = "".join(
        f"<tr data-trap='{row['key']}'>{trap_cell_html(row)}<td>{html.escape(row['fall_in'])}</td>"
        + (f"<td><strong>{html.escape(row['status'])}</strong></td>" if row["in_list"]
           else f"<td>{html.escape(row['status'])}</td>")
        + f"<td>{html.escape(row['costs'])}</td><td>{html.escape(row['households'])}</td></tr>"
        for row in rows)
    return f'<div class="tc-scroll"><table class="tc-traps"><tr>{head}</tr>{body}</table></div>'


@app.function
def unreadable_list_html(my_list, my_cutoff, prediction: dict) -> str:
    row_count = len(my_list) if isinstance(my_list, (pd.DataFrame, pd.Series)) else 0
    cutoff = float(my_cutoff) if is_number(my_cutoff) else None
    intro = ("Your my_list has no usable parcel-ID column (PARID, PIN or pin), so it can't be compared with the "
             f"correct list. It has {plural(row_count, 'row')}. In Predict you guessed {prediction['bucket']} homes.")
    return (f"<h3 class='tc-h3'>Part 1 · Your list against the correct one</h3><p>{html.escape(intro)}</p>"
            "<h3 class='tc-h3'>Part 2 · What this scenario was testing</h3>" + trap_table_html(unreadable_rows(cutoff)))


@app.function
def evaluation_html(slim, liens, boundary, my_list, my_cutoff, prediction: dict) -> str:
    """The evaluation page. Submit has already locked everything, so a list it can't read gets the short page
    instead of an error."""
    try:
        return list_evaluation_html(slim, liens, boundary, my_list, my_cutoff, prediction)
    except Exception:
        return unreadable_list_html(my_list, my_cutoff, prediction)


@app.function
def list_evaluation_html(slim, liens, boundary, my_list, my_cutoff, prediction: dict) -> str:
    ids = list_ids(my_list)
    if ids is None:
        return unreadable_list_html(my_list, my_cutoff, prediction)
    cutoff, note = resolve_cutoff(my_cutoff, ids, liens)
    diff = list_differences(ids, slim, liens, boundary, cutoff)
    rows = trap_rows(diff, cutoff, cutoff_card(slim, liens, boundary, cutoff))
    return ("<h3 class='tc-h3'>Part 1 · Your list against the correct one</h3>"
            + comparison_html(diff, len(my_list), prediction["bucket"], cutoff, note)
            + "<h3 class='tc-h3'>Part 2 · What this scenario was testing</h3>" + trap_table_html(rows))


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
    lock_warning = (mo.Html("<div class='tc-doc'><p><i>Answer all four questions before you lock.</i></p></div>")
                    if lock_button.value and not _ready else "")
    return (lock_warning,)


@app.cell(hide_code=True)
def predict(get_prediction, lock_button, lock_warning, mo, predict_fields, start_button):
    mo.stop(not start_button.value)
    _guiding = "".join(f"<li>{html.escape(q)}</li>" for q in PREDICT_GUIDING)
    _header = [
        mo.Html(stage_header_html(1)),
        mo.Html(f"<div class='tc-doc'><p>These questions may help you think it through:</p><ul class='tc-list'>"
                f"{_guiding}</ul><p>Then answer the four questions below. Once you lock your prediction you "
                "can't change it.</p></div>"),
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
    tables = load_tables(blobs)
    slim = slim_table(tables)
    # One plain dict for the whole session: every task runs in it, so results chain like notebook cells.
    namespace = make_namespace(tables)
    task_previews = {key: task_preview(key, tables) for key in TASKS}
    return blobs, namespace, slim, tables, task_previews


@app.cell
def observe_states(mo):
    get_submitted, set_submitted = mo.state(False)
    get_final, set_final = mo.state(None)
    # Plain dicts: how many clicks of each button have been acted on, and each task's latest output.
    run_log = {"done": {}, "outputs": {}}
    reload_log = {"done": 0}
    return get_final, get_submitted, reload_log, run_log, set_final, set_submitted


@app.cell
def task_controls(mo):
    # Created once here, so re-running the cell that shows them never wipes the learner's code. The editors sit
    # in a plain dict, so a keystroke re-runs nothing; a Run click reads the code straight from the editor.
    task_editors = {
        key: mo.ui.code_editor(value=task["starter"], language="python", min_height=90)
        for key, task in TASKS.items()
    }
    task_run_buttons = mo.ui.dictionary({
        key: mo.ui.button(value=0, on_click=lambda count: count + 1, label="Run") for key in TASKS
    })
    reload_button = mo.ui.button(value=0, on_click=lambda count: count + 1, label="Reload the data")
    return reload_button, task_editors, task_run_buttons


@app.cell
def reload_data(blobs, namespace, reload_button, reload_log):
    if reload_button.value > reload_log["done"]:
        reload_into(namespace, load_tables(blobs))
        reload_log["done"] = reload_button.value
    return


@app.cell
def run_clicked_tasks(namespace, run_log, task_editors, task_run_buttons):
    for _key in clicked_cells(task_run_buttons.value, run_log["done"]):
        run_log["outputs"][_key] = run_code(task_editors[_key].value, namespace)
        run_log["done"][_key] = task_run_buttons.value[_key]
    task_outputs = dict(run_log["outputs"])
    list_saved = list_ready(namespace)
    return list_saved, task_outputs


@app.cell(hide_code=True)
def observe(get_prediction, get_submitted, mo, reload_button, task_editors, task_outputs, task_previews,
            task_run_buttons):
    mo.stop(get_prediction() is None)
    _reloaded = f" The data has been reloaded {reload_button.value} time(s)." if reload_button.value else ""
    _panels = [
        mo.Html(stage_header_html(2)),
        mo.Html(f"<div class='tc-doc'><p>If your code changes one of the four prepared tables and you want it "
                f"back as it was, reload the data. Your own results stay.{_reloaded}</p></div>"),
        reload_button,
    ]
    for _number, (_key, _task) in enumerate(TASKS.items(), 1):
        _preview = task_previews[_key]
        _panels += [
            mo.Html(f"<div class='tc-doc'><h3 class='tc-task'>Task {_number}. {html.escape(_task['title'])}</h3>"
                    f"<p>The director writes: \"{html.escape(_task['director'])}\"</p>"
                    "<p class='tc-sub'>The data</p></div>"),
            mo.Html(f"<div class='tc-doc'><p>{html.escape(_preview)}</p></div>") if isinstance(_preview, str)
            else table_ready(_preview),
            mo.Html(f"<div class='tc-doc'><p class='tc-sub'>What to do</p><p>{html.escape(_task['hint'])}</p></div>"),
            mo.accordion({
                "Show the pandas functions": mo.md(f"`{_task['functions']}`"),
                "Show an example": mo.Html(code_block_html(_task["example"])),
            }),
        ]
        if get_submitted():
            _panels.append(mo.Html(code_block_html(task_editors[_key].value)))
        else:
            _panels += [task_editors[_key], task_run_buttons[_key]]
        _panels += task_output_parts(mo, task_outputs.get(_key))
    _questions = mo.vstack([
        mo.Html("<div class='tc-doc'><p class='tc-sub' style='color:#003594'>Questions for the director</p></div>"),
        mo.accordion({question: mo.md(answer) for question, answer in DIRECTOR_QUESTIONS}),
    ])
    # A grid, not mo.hstack: minmax(0, ...) columns keep a long line of code scrolling inside its editor instead
    # of widening the page, and the sticky column keeps the questions beside whichever task is on screen.
    mo.Html(
        "<div style='display:grid;grid-template-columns:minmax(0,3fr) minmax(0,1.2fr);gap:24px;align-items:start'>"
        f"<div style='min-width:0'>{mo.vstack(_panels, gap=0.75)}</div>"
        f"<div style='position:sticky;top:16px;min-width:0'>{_questions}</div></div>"
    )
    return


@app.cell(hide_code=True)
def observe_gate(get_prediction, list_saved, mo):
    mo.stop(get_prediction() is None or list_saved)
    mo.Html("<div class='tc-doc'><p><i>Stage 3 opens when task 8 has saved my_list.</i></p></div>")
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
def submit_action(get_explain, mo, namespace, set_final, set_submitted, submit_button):
    _ready = can_submit(get_explain())
    if submit_button.value and _ready:
        set_final(frozen_list(namespace))
        set_submitted(True)
    submit_warning = (mo.Html("<div class='tc-doc'><p><i>Answer all three questions before you submit.</i></p></div>")
                      if submit_button.value and not _ready else "")
    return (submit_warning,)


@app.cell(hide_code=True)
def explain(explain_fields, get_explain, get_prediction, get_submitted, list_saved, mo, submit_button, submit_warning):
    mo.stop(get_prediction() is None or not (list_saved or get_submitted()))
    _header = [mo.Html(stage_header_html(3)), mo.Html(locked_prediction_html(get_prediction()))]
    if get_submitted():
        _answers = "".join(f"<p><b>{html.escape(q)}</b><br>{paragraph_html(get_explain()[f'r{i}'])}</p>"
                           for i, q in enumerate(EXPLAIN_PROMPTS, 1))
        _output = mo.vstack(_header + [mo.Html(f"<div class='tc-doc'>{_answers}<p><i>Submitted. Your code, your "
                                               "list and these answers are locked.</i></p></div>")])
    else:
        _questions = [item for i, q in enumerate(EXPLAIN_PROMPTS, 1)
                      for item in (mo.md(f"**{i}.** {q}"), explain_fields[f"r{i}"])]
        _output = mo.vstack(_header + _questions + [
            mo.md("Submitting locks your code, your list and these answers, then shows your evaluation."),
            submit_button, submit_warning,
        ])
    _output
    return


@app.cell(hide_code=True)
def evaluate(get_explain, get_final, get_prediction, get_submitted, mo, slim, tables):
    # One cell with the download: a separate cell would re-run (and fail) whenever the Explain answers change.
    mo.stop(not get_submitted())
    _final = get_final()
    _evaluation = evaluation_html(slim, tables["liens"], tables["boundary"], _final["my_list"], _final["my_cutoff"],
                                  get_prediction())
    _doc = report_html(get_prediction(), list_summary(_final, tables["liens"]), get_explain(), _evaluation)
    mo.vstack([
        mo.Html(stage_header_html(4)), mo.Html(f"<div class='tc-doc'>{_evaluation}</div>"),
        mo.Html("<div class='tc-doc'><h3 class='tc-task'>Download your brief</h3><p>The file holds your prediction, "
                "your list, your reflection and this evaluation. It opens in any browser; use Print, then Save as "
                "PDF, for a PDF.</p></div>"),
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
