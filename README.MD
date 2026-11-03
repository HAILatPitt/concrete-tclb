# ConCReTE: Finding Abandoned Homes for the TriCOG Land Bank

A [marimo](https://marimo.io) notebook in which students build a list of homes the TriCOG Land Bank should consider buying. Every home must be inside TriCOG's 30 member municipalities, be a single-family house, and carry at least one tax lien. It follows ConCReTE's Predict → Observe → Explain → Evaluate structure:

- **Predict:** commit to a method, a definition, a lien amount and a rough count before seeing the data.
- **Observe:** run and edit eight code cells that look fine until you dig, then build the list with five settings.
- **Explain:** write a reflection and a note to TriCOG's director.
- **Evaluate:** see what each of your choices would cost if nobody caught it, counted from the data.

The browser version runs entirely in your browser:

https://hailatpitt.github.io/concrete-tclb/

It downloads about 53 MB and takes a few seconds to load.

## The data

A fixed snapshot, taken 2 November 2026, in `public/data/`:

- [Allegheny County Property Assessments](https://data.wprdc.org/dataset/property-assessments) (WPRDC)
- [Allegheny County Tax Liens](https://data.wprdc.org/dataset/allegheny-county-tax-liens-filed-and-satisfied) (WPRDC), the "Summary of liens" table, all 85,990 liens in the county
- [Allegheny County Parcel Boundaries](https://data.wprdc.org/dataset/allegheny-county-parcel-boundaries1) (WPRDC), in Pennsylvania South state-plane feet (EPSG:2272), simplified by 2 ft
- TriCOG's boundary: its 30 member municipalities from the Census, in longitude and latitude (EPSG:4326)

The county files are too large for a browser (about 930 MB), so the snapshot keeps every parcel within one mile of TriCOG's boundary (171,356 parcels) and their assessment records, plus the records that match no parcel. The final list is the same as with the full county files, apart from five parcels on TriCOG's border. The answers in the Evaluate stage are fixed to this snapshot.

## Running on your own machine

This uses [`uv`](https://docs.astral.sh/uv/).

- Run mode (as students see it): `uv run marimo run tricog.py`
- Edit mode: `uv run marimo edit tricog.py`

## Publishing the web version

GitHub Pages serves the `docs/` folder on `main`. After changing the notebook, rebuild `docs/` and commit it:

```
uv run marimo export html-wasm tricog.py -o docs --mode run --no-show-code -f
cp -r public docs/
touch docs/.nojekyll
```
