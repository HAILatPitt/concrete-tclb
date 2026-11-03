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


if __name__ == "__main__":
    app.run()
