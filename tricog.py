import marimo

__generated_with = "0.14.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import micropip
    return (micropip,)


@app.cell
async def _(micropip):
    await micropip.install("folium")
    await micropip.install("mapclassify")
    await micropip.install("geopandas")

    # import geopandas as gp
    return


@app.cell(hide_code=True)
def imports():
    import marimo as mo
    import geopandas as gp
    import pandas as pd
    from shapely import wkt
    import time
    import copy
    return copy, gp, mo, pd, time, wkt


@app.cell(hide_code=True)
def constant_text():
    # tricog_geo_path_cell_one_text = [
    #         f"""One method to find the parcels we're looking for is to use the GeoPandas clip function. Clip is a tool \
    #         that is common across GIS programs (such as ArcGIS, QGIS, and others). The tool "clips" a geospatial file to \
    #         the boundaries of a second file that you specify (referred to as an "overlay layer"). You can think of \
    #         clipping like using a cookie cutter on cookie dough; the clip function returns only the features (dough) that \
    #         fell within the overlay layer's boundaries (cookie cutter). In GeoPandas, the clip function returns a new \
    #         dataframe, where every row contains data from the base layer, so long as the data is within the overlay \
    #         layer's boundaries. Data outside of those boundaries is excluded.""",
    #     ]

    # opening_greeting = f"""Hello! Glad to have you on board, because I can really use your help. We're excited to move forward with our goal of buying abandoned houses and converting them to affordable houses.

    # I'm going to give you a file that has every parcel in Allegheny County, and I want you to tell me which parcels we should consider buying. The list can be as long as you think is appropriate as long as the parcels meet three rules: 

    # 1. The parcels are within our boundaries. 
    # 2. The parcels have single-family houses on them. 
    # 3. The parcels are tax delinquent. 

    # I know I'm throwing a lot at you, so feel free to ask for help. You can ask for information about those three rules, about key vocabulary terms, or about the important concepts you'll learn by helping me out. 

    # Simply type **guidelines**, **vocabulary**, **concepts** or **files** to learn more about those topics. You can always type **help** if you need a reminder of this information, and you can also type **done** if you're finished and ready to start working."""
    # vocab_response = f"""Here's a list of field-specific words I can help you with. 

    # "**Land Bank**"

    # "**Parcel**"

    # "**Polygon**"

    # "**Multipolygon**"

    # "**Tax Delinquency**"

    # "**Liens**"

    # If you type in any of those words, I can tell you what they mean. You can also type "**help**" and I'll repeat the different ways I can help. Or you can type "**Done**" if you're ready to start working!
    # """

    # land_bank_response = f"""A land bank is a special organization created by state and local laws to generate affordable housing in a community. Land Banks typically get special permission to purchase abandonded properties and sell them to individuals in the community for below market rates."""
    # parcels_response = f"""Parcels are the smallest distinct units of land in a municipality. For these purposes, it may help to think of a parcel as what a homeowner would call their "property" -- you don't usually think about just their house, but also their yard, their driveway, or whatever else is inside their "property". That said, all sorts of land can be a parcel: city parks are parcels, the buildings at school sit on parcels, warehouses and hospitals are on parcels too."""
    # polygon_response = f"""In GIS terms, polygons are one of three vector features that can be represented on a map (along with points and lines). Polygons have at least three lines that form the border of a shape (much like polygons in the context of geometry). Typically, parcels in a town are polygons."""
    # multipolygon_response = f"""Multipolygons are multiple polygons that, together, represent a singular entity. The US map would be represented as a multipolygon (with its 48 connected states, Alaska, Hawaii, and other territories)."""
    # tax_delinquency_response = f"""If you have not paid your taxes on time, you are said to be tax delinquent. If you eventually do pay your taxes, you can exit tax delinquency (in other words, 'tax delinquency' is not a permanent state or label)."""
    # lien_response = f"""A penalty assigned to someone who is tax delinquent. Liens are debts that are attached to properties or other large-value possessions. If you have a lien on your house and you sell it, the lien has to be paid off before you receive money from the sale."""
    # concept_response = f"""After completing this project, you will have: \n\n1. been introduced to geospatial file types, and ways to open the files\n\n2. be introduced to geopandas and compare that library\n\n3. be introduced to GIS processing techniques such as 'clip'\n\n4. consider the human context behind data"""
    # rules_response = f"""When you create your final list of parcels, every parcel must meet these three rules:\n\n1. They must all be within TriCOG's boundaries\n\n2. They must be residential properties with single-family homes\n\n3. They must be abandoned.\n\nWhich would you like to know more about? Type **1**, **2**, or **3**."""
    # one_response = f"""**Boundaries**: The TriCOG Land Bank operates within legally-defined borders. Any houses or parcels we purchase have to be within those borders. One of the files I give you will be a map that shows exactly where those borders are."""
    # two_response = f"""**Residential Properties**: Properties are classified by how they're used: if they're for living, they're residential. If they're for businesses, they're commercial. There are several other different classifications, and parcels of all different types will be on the list I give you. You just need to make sure that any you select are residential."""
    # three_response = f"""**Abandoned Homes**: There's no document that lists abandoned homes in the county. But we can use tax liens as a proxy -- if someone has stopped paying their taxes, it may be because they've abandoned the house. I have a file with liens I can give you that'll tell you which houses have liens on them."""
    # files_response = f"""I'm giving you four files that you'll need to use to complete the project: **`liens.csv`**, **`assessments.csv`**, **`parcels.geojson`**, and **`tricog.geojson`**. You can type in the name of any of those files (with the extension) if you want more information."""
    # liens_csv_response = f"""**`liens.csv`** is a file that lists every parcel in Allegheny County that currently has liens against it."""
    # assessments_response = f"""**`assessments.csv`** is a file that has descriptive data about every parcel in the county. This can tell us which parcels have houses or businesses or parks (among other details) without having to drive and look at them."""
    # parcels_geojson_response = f"""**`parcels.geojson`** is a file that contains data on the shape and size of every parcel in the county."""
    # help_response = f"""I can provide more information about the **guidelines** for your task, the **concepts** you'll learn by doing it, the **vocabulary** specific to the field, the **files** needed to perform the task. If you're ready to begin, you can type **done**."""
    # tricog_response = f"""**`tricog.geojson`** contains the shape of the TriCOG land bank's operating boundaries. By law, our business efforts have to stay within these boundaries."""
    # done_response = f"""Great! The files you'll need should be loading shortly, along with some notes about how to use them. Good luck!"""

    # response_dict = {'vocab': vocab_response,
    #                  'land bank': land_bank_response,
    #                  'parcel': parcels_response,
    #                  'polygon': polygon_response,
    #                  'multi': multipolygon_response,
    #                  'tax delinquen': tax_delinquency_response,
    #                  'lien': lien_response,
    #                  'concepts': concept_response,
    #                  'guidelines': rules_response,
    #                  '1': one_response,
    #                  '2': two_response,
    #                  '3': three_response,
    #                  'help': help_response,
    #                  'files': files_response,
    #                  'done': done_response,
    #                  'liens_file': liens_csv_response,
    #                  'parcels_geojson': parcels_geojson_response,
    #                  'tricog': tricog_response,
    #                  'assessments': assessments_response,
    #                  }
    return


@app.cell
def _(mo):
    # data_host = "https://rds-concrete.com/data"
    data_host = mo.notebook_location() / "public" /  "data"
    data_host = str(data_host)

    # PARCELS_PATH = f"{data_host}/parcels.geojson"
    # ASSESSMENTS_PATH = f"{data_host}/assessments.csv"
    # LIENS_PATH = f"{data_host}/liens.csv"
    # TRICOG_PATH = f"{data_host}/tricog_footprint.geojson"
    # OVERLAY_LAYER = f"{data_host}/overlay_layer.geojson"
    # OAKLAND_PARCELS_PATH = f"{data_host}/oakland_parcels.geojson"


    PARCELS_PATH = str(mo.notebook_location() / "data" / "parcels.geojson")
    PARCELS_CSV_PATH = str(mo.notebook_location() / "data" / "parcels.csv")
    ASSESSMENTS_PATH = str(mo.notebook_location() / "data" / "assessments.csv")
    LIENS_PATH = str(mo.notebook_location() / "data"/ "liens.csv")
    TRICOG_PATH = str(mo.notebook_location() / "data"/ "tricog_footprint.geojson")
    OVERLAY_LAYER = str(mo.notebook_location() / "data"/ "overlay_layer.geojson")
    OAKLAND_PARCELS_PATH = str(mo.notebook_location() / "data"/ "oakland_parcels.geojson")


    TRICOG_OVER_PARCELS_IMG_PATH = str(mo.notebook_location() / "public"  / "images" / "tricog_over_parcels.png")
    ALL_PARCELS_IMG_PATH = str(mo.notebook_location() / "public"  / "images" / "ac_parcels.png")
    OAKLAND_PARCELS_IMG_PATH = str(mo.notebook_location() / "public"  / "images" / "oakland_parcels.png")
    CLIPPED_PARCELS_IMG_PATH = str(mo.notebook_location()  / "public" / "images" / "clipped_parcels.png")
    ARROW_IMAGE_PATH = str(mo.notebook_location() / "public"  / "images" / "clip_arrow.png")
    PARCELS_CLIPPED_TO_TRICOG_IMG_PATH = str(mo.notebook_location() / "public"  / "images" / "parcels_clipped_to_tricog.png")
    TRICOG_CLIPPED_TO_PARCELS_IMG_PATH = str(mo.notebook_location() / "public"  / "images" / "tricog_clipped_to_parcels.png")
    TRICOG_BASE_PARCEL_OVERLAY_IMG_PATH = str(mo.notebook_location() / "public"  / "images" / "tricog_base_parcel_overlay.png")

    # CLIPPED_PARCELS_PATH = f"{data_host}/clipped_parcels.geojson"
    # CLIPPED_PARCELS_TRICOG_BASE_PATH = f"{data_host}/clipped_parcels_tricog_base.geojson"

    CLIPPED_PARCELS_PATH = str(mo.notebook_location() / "data" / "clipped_parcels.geojson")
    CLIPPED_PARCELS_TRICOG_BASE_PATH = str(mo.notebook_location() / "data"/ "clipped_parcels_tricog_base.geojson")
    return (
        ALL_PARCELS_IMG_PATH,
        ARROW_IMAGE_PATH,
        ASSESSMENTS_PATH,
        CLIPPED_PARCELS_PATH,
        CLIPPED_PARCELS_TRICOG_BASE_PATH,
        LIENS_PATH,
        OAKLAND_PARCELS_PATH,
        OVERLAY_LAYER,
        PARCELS_CLIPPED_TO_TRICOG_IMG_PATH,
        PARCELS_CSV_PATH,
        TRICOG_BASE_PARCEL_OVERLAY_IMG_PATH,
        TRICOG_CLIPPED_TO_PARCELS_IMG_PATH,
        TRICOG_OVER_PARCELS_IMG_PATH,
        TRICOG_PATH,
    )


@app.cell(hide_code=True)
def expected_values():
    # expected values

    # file_reading_section
    assessments_file_expected_code = 'pd.read_csv(ASSESSMENTS_PATH)'
    liens_file_expected_code = 'pd.read_csv(LIENS_PATH)'
    parcels_file_expected_code = 'gp.read_file(PARCELS_PATH)'
    tricog_file_expected_code = 'gp.read_file(TRICOG_PATH)'
    oakland_parcel_expected_code = 'oakland_parcels_df.explore()'

    # tricog_border_analysis_section
    # text
    tricog_municipality_name_expected_code = "list(tricog.NAME)"
    countywide_municipality_name_list = 'list(set(assessments.MUNIDESC))'
    countywide_municipality_name_list_sorted = 'munidesc.sort()'
    countywide_municipality_name_list_sorted_printed = 'print(munidesc[:20])'
    # geospatial
    oakland_overlay_expected_output = 'gp.clip(oakland_parcels_df, overlay)'
    clip_function_code = 'clipped_parcels = gp.clip(parcels, tricog)'
    clip_function_parcel_length_code = "f'length of parcels: {len(parcels)}'"
    clip_function_clip_output_length_code = "f'length of clipped_parcels: {len(clipped_parcels)}'"
    return (
        assessments_file_expected_code,
        clip_function_clip_output_length_code,
        countywide_municipality_name_list,
        countywide_municipality_name_list_sorted,
        liens_file_expected_code,
        oakland_overlay_expected_output,
        oakland_parcel_expected_code,
        parcels_file_expected_code,
        tricog_file_expected_code,
        tricog_municipality_name_expected_code,
    )


@app.cell(hide_code=True)
def _(OAKLAND_PARCELS_PATH, gp):
    oakland_parcels_df = gp.read_file(OAKLAND_PARCELS_PATH)
    return (oakland_parcels_df,)


@app.cell(hide_code=True)
def buttons(
    handle_begin_button,
    handle_intro_concepts_button,
    handle_intro_files_button,
    handle_intro_objective_button,
    handle_intro_vocab_button,
    handle_start_analysis_button,
    mo,
):
    # buttons

    # prologue
    begin_button = mo.ui.run_button(label="Click Here To Begin", on_change=handle_begin_button)
    moving_on = mo.ui.run_button(label="Moving on...")
    read_files_button = mo.ui.run_button(label="Read In Files")
    start_analysis_button = mo.ui.button(label="Start Analysis", on_click=handle_start_analysis_button)

    # introduction
    intro_objective_button = mo.ui.run_button(label="Objective", on_change=handle_intro_objective_button)
    intro_vocab_button = mo.ui.run_button(label="Key Terms", on_change=handle_intro_vocab_button)
    intro_files_button = mo.ui.run_button(label="Provided Files", on_change=handle_intro_files_button)
    intro_concepts_button = mo.ui.run_button(label="Educational Concepts", on_change=handle_intro_concepts_button)

    # misc
    tricog_button = mo.ui.run_button(label="Find Parcels Within TriCOG")
    tricog_button_2 = mo.ui.run_button(label="Find Parcels Within TriCOG")
    tricog_button_3 = mo.ui.run_button(label="Find Parcels Within TriCOG")
    residential_button = mo.ui.run_button(label="Find Residential Parcels")
    abandoned_button = mo.ui.run_button(label="Find Abandoned Parcels")
    return (
        begin_button,
        intro_concepts_button,
        intro_files_button,
        intro_objective_button,
        intro_vocab_button,
        start_analysis_button,
    )


@app.cell(hide_code=True)
def text_boxes(
    mo,
    set_liens_counter,
    set_oakland_parcels_counter,
    set_parcels_counter,
    set_tricog_counter,
):
    # user text entry boxes

    # file_reading_section
    assessments_text_box = mo.ui.text(full_width=True).form(clear_on_submit=True)
    liens_text_box = mo.ui.text(full_width=True).form(clear_on_submit=True,
                                                      on_change=lambda _: set_liens_counter(lambda x: x + 1))
    tricog_text_geojson_box = mo.ui.text(full_width=True).form(clear_on_submit=True,
                                                               on_change=lambda _: set_tricog_counter(lambda x: x + 1))
    tricog_explore_text_box = mo.ui.text(full_width=True).form(clear_on_submit=True)
    parcels_text_box = mo.ui.text(full_width=True).form(clear_on_submit=True,
                                                        on_change=lambda _: set_parcels_counter(lambda x: x + 1))
    oakland_parcels_text_box = mo.ui.text(full_width=True).form(clear_on_submit=True,
                                                                on_change=lambda _: set_oakland_parcels_counter(
                                                                    lambda x: x + 1))

    # other_sections
    join_text_box = mo.ui.text(full_width=True).form(clear_on_submit=True)
    abandoned_text_box_one = mo.ui.text(full_width=True).form(clear_on_submit=True)
    abandoned_text_box_two = mo.ui.text(full_width=True).form(clear_on_submit=True)
    abandoned_text_box_three = mo.ui.text_area(full_width=True).form(clear_on_submit=True)
    residential_text_box_one = mo.ui.text(full_width=True).form(clear_on_submit=True)
    residential_text_box_two = mo.ui.text(full_width=True).form(clear_on_submit=True)
    residential_text_box_three = mo.ui.text(full_width=True).form(clear_on_submit=True)
    # tricog_text_box_one = mo.ui.text(full_width=True).form(clear_on_submit=True)
    # tricog_text_box_two = mo.ui.text(full_width=True).form(clear_on_submit=True)
    # tricog_text_box_two_a = mo.ui.text(full_width=True).form(clear_on_submit=True)
    # tricog_text_box_three = mo.ui.text(full_width=True).form(clear_on_submit=True)
    # tricog_text_box_four = mo.ui.text(full_width=True).form(clear_on_submit=True)
    # tricog_text_box_five = mo.ui.text(full_width=True).form(clear_on_submit=True)
    # tricog_text_box_six = mo.ui.text(full_width=True).form(clear_on_submit=True)

    # combining_data_text_box_one = mo.ui.text(full_width=True).form(clear_on_submit=True)
    # combining_data_text_box_two = mo.ui.text(full_width=True).form(clear_on_submit=True)

    # instantiating seperate buttons to use at different stages while avoiding conflicts
    return (
        assessments_text_box,
        liens_text_box,
        oakland_parcels_text_box,
        parcels_text_box,
        tricog_explore_text_box,
        tricog_text_geojson_box,
    )


@app.cell(hide_code=True)
def drop_down_forms():
    # drop down form
    return


@app.cell
def getters_and_setters(mo):
    # global state

    # introduction
    get_intro_objective_button, set_intro_objective_button = mo.state(False)
    get_intro_vocab_button, set_intro_vocab_button = mo.state(False)
    get_intro_files_button, set_intro_files_button = mo.state(False)
    get_intro_concepts_button, set_intro_concepts_button = mo.state(False)
    get_begin_button, set_begin_button = mo.state(False)

    get_oakland_parcels_state, set_oakland_parcels_state = mo.state(False)

    # tracks state of which steps the user took
    get_launch_tasks, set_launch_tasks = mo.state(False)

    get_iteration_move_along, set_iteration_move_along = mo.state(False)

    get_parcels_display, set_parcels_display = mo.state(False)
    get_combined_data_step_one, set_combined_data_step_one = mo.state(False)
    get_combined_data_step_two, set_combined_data_step_two = mo.state(False)
    get_start_analysis_button, set_start_analysis_button = mo.state(False)
    get_geo_path_oakland_clip_expectations, set_geo_path_oakland_clip_expectations = mo.state(False)
    get_parcels_file_input_complete, set_parcels_file_input_complete = mo.state(False)

    # file_reading_section
    get_liens_counter, set_liens_counter = mo.state(0)
    get_tricog_counter, set_tricog_counter = mo.state(0)
    get_parcels_counter, set_parcels_counter = mo.state(0)
    get_oakland_parcels_counter, set_oakland_parcels_counter = mo.state(0)
    get_oakland_overlay_counter, set_oakland_overlay_counter = mo.state(0)
    get_continue_on_to_parcels_geojson, set_continue_on_to_parcels_geojson = mo.state(False)
    return (
        get_begin_button,
        get_continue_on_to_parcels_geojson,
        get_intro_concepts_button,
        get_intro_files_button,
        get_intro_objective_button,
        get_intro_vocab_button,
        get_liens_counter,
        get_oakland_overlay_counter,
        get_oakland_parcels_counter,
        get_oakland_parcels_state,
        get_parcels_counter,
        get_parcels_file_input_complete,
        get_start_analysis_button,
        get_tricog_counter,
        set_begin_button,
        set_continue_on_to_parcels_geojson,
        set_geo_path_oakland_clip_expectations,
        set_intro_concepts_button,
        set_intro_files_button,
        set_intro_objective_button,
        set_intro_vocab_button,
        set_liens_counter,
        set_oakland_overlay_counter,
        set_oakland_parcels_counter,
        set_oakland_parcels_state,
        set_parcels_counter,
        set_parcels_file_input_complete,
        set_start_analysis_button,
        set_tricog_counter,
    )


@app.cell(hide_code=True)
def handler_functions(
    get_intro_concepts_button,
    get_intro_files_button,
    get_intro_objective_button,
    get_intro_vocab_button,
    set_begin_button,
    set_intro_concepts_button,
    set_intro_files_button,
    set_intro_objective_button,
    set_intro_vocab_button,
    set_start_analysis_button,
):
    # handler functions

    # intro button handler functions
    def handle_intro_objective_button(value):
        curr = get_intro_objective_button()
        make_all_intro_buttons_false()
        set_intro_objective_button(not curr)
        return not curr

    def handle_intro_vocab_button(value):
        curr = get_intro_vocab_button()
        make_all_intro_buttons_false()
        set_intro_vocab_button(not curr)
        return not curr

    def handle_intro_files_button(value):
        curr = get_intro_files_button()
        make_all_intro_buttons_false()
        set_intro_files_button(not curr)
        return not curr

    def handle_intro_concepts_button(value):
        curr = get_intro_concepts_button()
        make_all_intro_buttons_false()
        set_intro_concepts_button(not curr)
        return not curr

    def make_all_intro_buttons_false():
        set_intro_objective_button(False)
        set_intro_vocab_button(False)
        set_intro_files_button(False)
        set_intro_concepts_button(False)
        return True

    def handle_begin_button(value):
        make_all_intro_buttons_false()
        set_begin_button(True)
        return True

    # start analysis button
    def handle_start_analysis_button(value):
        set_start_analysis_button(True)
        return True
    return (
        handle_begin_button,
        handle_intro_concepts_button,
        handle_intro_files_button,
        handle_intro_objective_button,
        handle_intro_vocab_button,
        handle_start_analysis_button,
    )


@app.cell(hide_code=True)
def misc_functions():
    def strip_string(unstripped: str):
        return unstripped.replace('"', '').replace(' ', '').replace("'", "").replace("\n", "").replace('`', '').replace(
            '&nbsp;', '').lower()

    def incorrect_answer_text_generator(
            user_input,
            expected_code,
            counting_get_function,
    ):
        if counting_get_function < 2:
            return f"""That doesn't look quite right. Try again?""", None
        elif counting_get_function == 2:
            return f"""'{user_input}' still seems a bit off...try one more time!""", 1
        else:
            return f"""You entered {user_input}. The answer we're looking for is {expected_code}. Try entering that and see what happens.""", 1

    def parcel_guess_validation(value):
        if not value.isnumeric():
            return "Please enter a number between 0 and 499999"
        elif int(value) > 499999:
            return "That number seems awfully high...try a smaller guess."
        else:
            return None
    return (
        incorrect_answer_text_generator,
        parcel_guess_validation,
        strip_string,
    )


@app.cell(hide_code=True)
def title(mo):
    mo.md(text="#TriCOG Land Bank Scenario").center()
    return


@app.cell(hide_code=True)
def intro_text(mo):
    mo.md(r"""Congratulations on your new role with TriCOG Land Bank! You have been hired to assist their GIS and Data Analyst. Your task is to help the analyst identify homes that the Land Bank can purchase and make available as affordable housing. Please press one of four buttons immediately below for background information, or select "Click Here To Begin" to get started!""")
    return


@app.cell(hide_code=True)
def intro_button_display(
    intro_concepts_button,
    intro_files_button,
    intro_objective_button,
    intro_vocab_button,
    mo,
):
    mo.hstack([intro_objective_button, intro_vocab_button, intro_files_button, intro_concepts_button],
              justify='space-between')
    return


@app.cell(hide_code=True)
def intro_button_text(
    get_intro_concepts_button,
    get_intro_files_button,
    get_intro_objective_button,
    get_intro_vocab_button,
    mo,
):
    if get_intro_objective_button():
        mo.output.replace(
            mo.md(
                f"""<br>You will be given four data files. Using them, you will generate an output file that lists parcels that the TriCOG Land Bank should consider buying. The list can be any length, but regardless of size, each parcel must meet three standards: <br><br>1. They must all be within TriCOG's boundaries<br><br>2. They must be residential properties with single-family homes<br><br>3. They must be abandoned.<br><br>""")
        )
    elif get_intro_vocab_button():
        mo.output.replace(
            mo.md(f"""<br>"**Land Bank**": A land bank is a special organization created by state and local laws to generate affordable housing in a community. Land Banks typically get special permission to purchase abandonded properties and sell them to individuals in the community for below market rates.

    "**Parcel**": Parcels are the smallest distinct units of land in a municipality. For these purposes, it may help to think of a parcel as what a homeowner would call their "property" -- you don't usually think about just their house, but also their yard, their driveway, or whatever else is inside their "property". That said, all sorts of land can be a parcel: city parks are parcels, the buildings at school sit on parcels, warehouses and hospitals are on parcels too.

    "**Polygon**": In GIS terms, polygons are one of three vector features that can be represented on a map (along with points and lines). Polygons have at least three lines that form the border of a shape (much like polygons in the context of geometry). Typically, parcels in a town are polygons.

    "**Multipolygon**": Multipolygons are multiple polygons that, together, represent a singular entity. The US map would be represented as a multipolygon (with its 48 connected states, Alaska, Hawaii, and other territories).

    "**Municipality**": For our purposes, we can think of municipalities as local areas that have their own system of local governance. The city of Pittsburgh is a municipality (has a mayor and a city council), but the neighborhood of Central Oakland is not a municipality. Allegheny County has 130 municipalities, including Ross Township, Plum Borough, Monroeville municipality, and more.  

    "**Tax Delinquency**": If you have not paid your taxes on time, you are said to be tax delinquent. If you eventually do pay your taxes, you can exit tax delinquency (in other words, 'tax delinquency' is not a permanent state or label).

    "**Liens**": A penalty assigned to someone who is tax delinquent. Liens are debts that are attached to properties or other large-value possessions. If you have a lien on your house and you sell it, the lien has to be paid off before you receive money from the sale.""")
        )
    elif get_intro_concepts_button():
        mo.output.replace(
            mo.md(f"""<br>After completing this project, you will have:

            1. been introduced to geospatial file types, and ways to open the files

            2. been introduced to GeoPandas and compare that library's functionality to pandas

            3. been introduced to GIS processing techniques such as 'clip'

            4. considered the human context behind data""")
        )
    elif get_intro_files_button():
        mo.output.replace(
            mo.md(f"""<br>You will be given four files to complete the project: 

            **`assessments.csv`** contains descriptive data about every parcel in the county. This can tell us which parcels have houses or businesses or parks (among other details) without having to drive and look at them. 

            **`liens.csv`** lists every parcel in Allegheny County that currently has liens against it

            **`tricog.geojson`** contains the shape of the TriCOG land bank's operating boundaries. By law, TriCOG's business efforts have to stay within these boundaries

            **`parcels.geojson`** contains data on the shape and size of every parcel in the county.
            """)
        )
    else:
        mo.output.clear()
    return


@app.cell(hide_code=True)
def display_begin_button(begin_button, get_begin_button, mo):
    if not get_begin_button():
        mo.output.replace(
            begin_button.center().style({"padding": "20px 0 0 0"})
        )
    else:
        mo.output.clear()
    return


@app.cell
def _(
    ASSESSMENTS_PATH,
    assessments_file_expected_code,
    assessments_text_box,
    get_begin_button,
    mo,
    pd,
    strip_string,
):
    # Instructions on how to read assessments file
    assessments_code_entry = None
    assessments_df = None
    if get_begin_button():
        mo.output.replace(
            mo.vstack([
                mo.md(f"""#Reading In Files""").center(),
                mo.md(f"""To begin your work, you'll need to read in four files:<br>
                1. **assessments.csv**<br>
                2. **liens.csv**<br>
                3. **tricog.geojson**<br>
                4. **parcels.geojson**<br>"""),
                mo.md(f"""Reading in `csv` files is a fairly straightforward process, thanks to the `pandas` library. You can read in the files using pandas' `read_csv()` function.<br>
                In the function's simplest form, all you need is the location of the file. Try and run it now: type the following line of code into the text box below and hit 'submit'. (In this code, `ASSESSMENTS_PATH` is a variable that represents the location of `assessments.csv` on your computer.) <br><br>
                `assessments_df = {assessments_file_expected_code}`<br><br>"""),
                mo.hstack([
                    mo.md(f"""`assessments_df = `"""), assessments_text_box,
                ], gap=0, justify="space-around", align='center', widths=[1, 7]),
            ])
        )
        # capture input
        assessments_code_entry = assessments_text_box.value

        # check input
        if assessments_code_entry:
            if strip_string(assessments_file_expected_code) == strip_string(assessments_code_entry):
                with mo.status.spinner(
                        title="Reading in 'assessments.csv'",
                        subtitle="Please be patient, this may take a minute"
                ) as _spinner:
                    assessments_df = pd.read_csv(ASSESSMENTS_PATH, low_memory=False)
                    mo.output.replace_at_index("Correct!", 1)
            else:
                mo.output.append('Not quite...  Try again.')
    return (assessments_df,)


@app.cell(hide_code=True)
def _(assessments_df, mo):
    # wait for assessments dataframe to be created (i.e. correct input from user)
    mo.stop(assessments_df is None)

    #
    mo.output.replace(mo.vstack(
        [
            mo.md(f"""##assessments_df"""),
            assessments_df,
            mo.md(
                f"""<br>The dataframe above is the `assessments.csv` file that was just read in and stored as `assessments_df`. Notice that it has 86 columns and over 584,000 rows. This is a large file! Also notice the column on the far left is a column named `PARID`. This is the parcel identification number. That means that every row contains data about a different parcel. Finally, it's important to note that this file does not have any geospatial data in it; the contents are entirely descriptive; in other words, the file tells you details about the parcels, but it doesn't tell you where they are.<br>""")
        ]
    ))
    return


@app.cell(hide_code=True)
def _(
    LIENS_PATH,
    assessments_df,
    get_liens_counter,
    incorrect_answer_text_generator,
    liens_file_expected_code,
    liens_text_box,
    mo,
    pd,
    strip_string,
):
    # Read in liens.csv file
    mo.stop(assessments_df is None)

    mo.output.replace(mo.vstack(
        [
            mo.md(f"""Let's read in the other csv file, `liens.csv`. The variable that tells your computer where that file is is `LIENS_PATH`.  The process is very much the same as the one you used to read the assessments.<br>
            <br>1. Use the method `pd.read_csv()` from the previous step
            <br>2. Use `LIENS_PATH` as the argument for the method
            <br>3. Hit submit!<br><br>"""),
            mo.hstack([
                mo.md(f"""`liens_df = `"""), liens_text_box,
            ], gap=0, justify="center", align='center', widths=[1, 7])
        ]
    ))

    liens_code_entry = liens_text_box.value

    liens_df = None
    if liens_code_entry:
        if strip_string(liens_file_expected_code) == strip_string(liens_code_entry):
            with mo.status.spinner(
                    title="Reading in 'liens.csv'",
                    subtitle="This should be a bit quicker, thankfully"
            ) as _spinner:
                liens_df = pd.read_csv(LIENS_PATH)
                mo.output.replace_at_index("Correct!", 1)
        else:
            output_text, output_position = incorrect_answer_text_generator(liens_code_entry, liens_file_expected_code,
                                                                           get_liens_counter())
            if output_position is None:
                mo.output.append(output_text)
            else:
                mo.output.replace_at_index(output_text, output_position)
    return (liens_df,)


@app.cell(hide_code=True)
def _(liens_df, mo):
    # wait for correct user input (i.e. the dataframe gets instantiated)
    mo.stop(liens_df is None)

    mo.output.replace(
        mo.vstack(
            [
                mo.md(f"""##liens_df"""),
                liens_df,
                mo.md(
                    f"""<br>`liens_df` (read from the file `liens.csv`) is a dataset that contains information about properties that have liens against them. You'll notice that this file also has a new parcel ID for each row, only in this file the column is labeled 'pin' (instead of 'PARID'). The three columns of note are the parcel ID, the number of liens a property has, and the total amount of money owed.""")
            ]
        )
    )
    return


@app.cell(hide_code=True)
def _(
    TRICOG_PATH,
    get_tricog_counter,
    gp,
    liens_df,
    mo,
    strip_string,
    tricog_file_expected_code,
    tricog_text_geojson_box,
):
    mo.stop(liens_df is None)

    tricog_code_entry = tricog_text_geojson_box.value
    tricog_df = None

    mo.output.replace(
        mo.vstack([
            mo.md(
                f"""The next file is not a `.csv` file: it's a `.geojson` file. Unfortunately, pandas does not have a `read_geojson()` function. This is where `GeoPandas` comes in! `GeoPandas` is a Python library that adds geospatial support to pandas objects. `GeoPandas` has a similarly easy function for reading in files: `read_file()`. Let's try and use it! 
                <br><br>Your code will be in the same format as before, except the file path constant is `TRICOG_PATH`, and you will use `gp.read_file()` instead of `pd.read_csv()`. Once you've typed that out, hit submit!.<br><br>"""
            ),
            mo.hstack([
                mo.md(f"""`tricog_df = `"""), tricog_text_geojson_box,
            ], gap=0, justify="center", align='center', widths=[1, 7])
        ])
    )

    if tricog_code_entry:
        if strip_string(tricog_file_expected_code) == strip_string(tricog_code_entry):
            with mo.status.spinner(
                    title="Reading in 'tricog_df.geojson'",
                    subtitle="Please be patient, this may take a minute"
            ) as _spinner:
                tricog_df = gp.read_file(TRICOG_PATH)
                mo.output.replace_at_index("Correct!", 1)
        else:
            if get_tricog_counter() < 2:
                mo.output.append(f"""That doesn't look quite right. Try again?""")
            elif get_tricog_counter() == 2:
                mo.output.replace_at_index(f"""'{tricog_code_entry}' still seems a bit off...try one more time!""", 1)
            else:
                mo.output.replace_at_index(
                    f"""You entered {tricog_code_entry}. The answer we're looking for is {tricog_file_expected_code}. Try entering that and see what happens.""",
                    1)
    return (tricog_df,)


@app.cell(hide_code=True)
def _(mo, pd, tricog_df):
    def handle_tricog(tricog):
        """convert ot plain ol' dataframe for display purposes """
        if tricog is not None:
            return pd.DataFrame(tricog.astype({'geometry': 'str'}))
        else:
            return None

    # wait for correct user input (i.e. the dataframe get's instantiated)
    mo.stop(tricog_df is None)

    mo.output.replace(
        mo.vstack([
            mo.md(f"""##tricog_df"""),
            handle_tricog(tricog_df),
            mo.md(
                f"""Unlike the other files we've looked at so far, `tricog.geojson` isn't organized at the parcel level. Instead, each row of this file represents a different municipality that is a member of the TriCOG land bank. Also unlike the other files, `tricog.geojson` has a column at the far right called 'geometry' that contains the shape of each municipality.<br><br>"""),
        ]
        )
    )
    return (handle_tricog,)


@app.cell(hide_code=True)
def _(mo, tricog_df, tricog_explore_text_box):
    mo.stop(tricog_df is None)

    exploration = None

    mo.output.replace(
        mo.vstack(
            [
                mo.md(f"""Because this shape data is contained in the file, GeoPandas lets us do neat things like visualizing the content. Watch what happens when you enter the following line of code into the textbox.<br><br>
        `tricog_df.explore()`"""),
                tricog_explore_text_box
            ]
        )
    )

    explore_code_entry = tricog_explore_text_box.value

    if explore_code_entry:
        if explore_code_entry.strip() == 'tricog_df.explore()':
            with mo.status.spinner(
                    title="Loading 'tricog_df.explore()'",
                    subtitle="Please be patient, this may take a minute"
            ) as _spinner:
                exploration = tricog_df.explore(height='90%',
                                                style_kwds=dict(color='black', fillColor='yellow', fillOpacity=0.3))
                mo.output.replace_at_index("Correct!", 1)
        else:
            mo.output.append(mo.md('Try again.'))
    return (exploration,)


@app.cell(hide_code=True)
def _(exploration, mo):
    # wait for correct input
    mo.stop(exploration is None)

    mo.output.replace(
        mo.vstack(
            [
                mo.md(f"""##tricog_df.explore()"""),
                exploration,
                mo.md(
                    f"""Here, we see the various municipalities in which TriCOG operates. If you hover your mouse over any of the shaded areas, a pop-up will display the rest of the data that we saw in the dataframe.""", )
            ]
        )
    )
    return


@app.cell
def _(
    exploration,
    get_parcels_counter,
    mo,
    parcels_file_expected_code,
    parcels_text_box,
    set_continue_on_to_parcels_geojson,
    strip_string,
):
    mo.stop(exploration is None)

    mo.output.replace(
        mo.vstack([
            mo.md(
                f"""Finally, let's read in our last file: parcels.geojson. Since this file is also a GeoJSON file, we'll once again use the GeoPandas file reading method, `read_file()`. The constant `PARCELS_PATH` is storing the path to the parcels.geojson file. Type the method and path constant into the  and press submit.<br><br>"""),
            mo.hstack([
                mo.md(f"""`parcels_df = `"""),
                parcels_text_box,
            ], gap=0, justify="center", align='center', widths=[1, 7])
        ])
    )

    parcel_code_entry = parcels_text_box.value
    if parcel_code_entry:
        if strip_string(parcels_file_expected_code) == strip_string(parcel_code_entry):
            mo.output.replace_at_index(f'Great! {parcel_code_entry} is correct.', 1)
            set_continue_on_to_parcels_geojson(True)
        else:
            if get_parcels_counter() < 2:
                mo.output.append(f"""Try again! That's not exactly it.""")
            elif get_parcels_counter() == 2:
                mo.output.replace_at_index(f"""'{parcel_code_entry}' still seems a bit off...try one more time!""", 1)
            else:
                mo.output.replace_at_index(
                    f"""You entered '{parcel_code_entry}'. The answer we're looking for is {parcels_file_expected_code}. Try entering that and see what happens.""",
                    1)
    return


@app.cell
def _(
    PARCELS_CSV_PATH,
    get_continue_on_to_parcels_geojson,
    gp,
    mo,
    pd,
    set_parcels_file_input_complete,
    wkt,
):
    mo.stop(not get_continue_on_to_parcels_geojson())

    mo.output.replace(
        mo.md(f"""""")
    )

    with mo.status.spinner(
            title="Reading in 'parcels.geojson'",
            subtitle="Please be patient, this may take a minute. Even longer than the others!"
    ) as _spinner:
        parcels_df_df = pd.read_csv(PARCELS_CSV_PATH)
        parcels_geometry = parcels_df_df['geometry'].map(wkt.loads)
        parcels_df = gp.GeoDataFrame(parcels_df_df, geometry=parcels_geometry)
        set_parcels_file_input_complete(True)


    return parcels_df, parcels_df_df


@app.cell
def read_in_parcels_file(get_parcels_file_input_complete, mo, parcels_df_df):
    mo.stop(not get_parcels_file_input_complete())

    mo.output.replace(
        mo.vstack(
            [
                mo.md(f"""##parcels_df"""),
                parcels_df_df,
            ]
        )
    )
    return


@app.cell
def read_in_parcels_file_safety():
    # continue_with_parcels_df_discussion = False
    # parcels_df = None
    # parcels_df_df = None
    # mo.stop(not get_continue_on_to_parcels_geojson())

    # with mo.status.spinner(
    #         title="Reading in 'parcels.geojson'",
    #         subtitle="Please be patient, this may take a minute. Even longer than the others!"
    # ) as _spinner:
    #     parcels_df = gp.read_file(PARCELS_PATH)
    #     parcels_df_df = pd.DataFrame(parcels_df)
    # test_text = ''

    # mo.output.replace(
    #     mo.vstack(
    #         [
    #             mo.md(f"""##parcels.geojson"""),
    #             parcels_df_df,
    #         ]
    #     )
    # )
    # continue_with_parcels_df_discussion = True
    return


@app.cell(hide_code=True)
def _(ALL_PARCELS_IMG_PATH, get_parcels_file_input_complete, mo):
    mo.stop(not get_parcels_file_input_complete())

    mo.output.replace(
        mo.vstack(
            [
                mo.md(
                    f"""Here we see the parcels.geojson file, stored as `parcels_df`. Unfortunately, the file is too large to use the explore function: doing so would likely make your browser crash. That said, if you load  the file into GIS software, it looks like this: <br>"""),
                mo.image(ALL_PARCELS_IMG_PATH),
            ]
        )
    )
    return


@app.cell(hide_code=True)
def _(
    get_oakland_parcels_counter,
    get_parcels_file_input_complete,
    incorrect_answer_text_generator,
    mo,
    oakland_parcel_expected_code,
    oakland_parcels_df,
    oakland_parcels_text_box,
    set_oakland_parcels_state,
    strip_string,
):
    mo.stop(not get_parcels_file_input_complete())

    oakland_parcels_user_entry = oakland_parcels_text_box.value

    mo.output.replace(
        mo.vstack(
            [
                mo.md(f"""Because there are so many parcels, it's difficult to make them all out at this distance. Let's take a look at a subset of the parcels so you can get a better feel for what they are and how they look plotted on a the map. <br><br>
                A subset of parcels located within Oakland has been saved to the dataframe `oakland_parcels_df`. Go ahead and use the `explore()` method on the `oakland_parcels_df` dataframe exactly how you used it on `tricog_df` above."""),
                oakland_parcels_text_box,
            ]
        )
    )
    if oakland_parcels_user_entry:
        if strip_string(oakland_parcels_user_entry) == strip_string(oakland_parcel_expected_code):
            oakland_parcel_exploration = oakland_parcels_df.explore(style_kwds=dict(color='black', fillColor='yellow'))
            mo.output.replace_at_index('Correct!', 1)
            set_oakland_parcels_state(True)
        else:
            oakland_parcels_output_response = incorrect_answer_text_generator(oakland_parcels_user_entry,
                                                                              oakland_parcel_expected_code,
                                                                              get_oakland_parcels_counter())
            mo.output.replace_at_index(f"""{oakland_parcels_output_response[0]}""", 1)
    return (oakland_parcel_exploration,)


@app.cell(hide_code=True)
def _(get_oakland_parcels_state, mo, oakland_parcel_exploration):
    mo.stop(not get_oakland_parcels_state())

    if get_oakland_parcels_state():
        mo.output.replace(
            mo.vstack(
                [
                    oakland_parcel_exploration,
                    mo.md(f"""Above, you'll see a small subset of the parcels from across Allegheny County. These parcels are all in the Central Oakland neighborhood. Notice that the street above the parcels is Fifth Avenue, and the street cutting through the middle is Forbes -- these parcels are Pitt's campus and the surrounding businesses! The largest shape in the far right is the parcel that contains the Cathedral and Heinz Chapel. The larger group of parcels on the right side of the map are Pitt Campus buildings, the Carnegie Library, Schenley Plaza, and Soldiers and Sailors Memorial Hall. The smaller parcels on the left side of the map are the the restaurants and shops that populate that stretch, as well as the rowhouses that appear as you move south.<br><br>
                    Just like with `tricog_df.explore()`, you can see the data associated with any individual parcel by hovering your mouse above it. Doing so will show you the column names from `parcels_df` dataframe and the values associated with the specific parcel.<br><br>
                    We have now loaded all of the main files we'll need to begin considering our central question. When you've finished looking at the dataframes and interactive maps, click the button below to begin your analysis."""),
                ]
            )
        )
    else:
        mo.output.clear()
    return


@app.cell(hide_code=True)
def _(get_oakland_parcels_state, mo, start_analysis_button):
    mo.stop(not get_oakland_parcels_state())

    if get_oakland_parcels_state():
        mo.output.replace(
            start_analysis_button.center()
        )
    else:
        mo.output.clear()
    return


@app.cell(hide_code=True)
def tricog_boundary_text_boxes(
    mo,
    parcel_guess_validation,
    set_geo_path_oakland_clip_expectations,
    set_oakland_overlay_counter,
    set_tricog_geo_path_parcel_count_guess,
):
    tricog_municipality_name_text_box = mo.ui.text(full_width=True).form(clear_on_submit=True)
    tricog_text_path_box_countywide_muni_name_list = mo.ui.text(full_width=True).form(clear_on_submit=True)
    tricog_text_path_box_countywide_muni_name_list_sorted = mo.ui.text(full_width=True).form(clear_on_submit=True)
    tricog_text_path_box_countywide_muni_name_list_sorted_printed = mo.ui.text(full_width=True).form(
        clear_on_submit=True)
    tricog_geo_path_text_box_oakland_clip_demo = mo.ui.text(full_width=True).form(clear_on_submit=True, on_change=lambda
        _: set_oakland_overlay_counter(lambda x: x + 1))
    tricog_geo_path_text_box_clip_function = mo.ui.text(full_width=True).form(clear_on_submit=True)

    tricog_geo_path_clip_function_parcel_length = mo.ui.text(full_width=True).form(clear_on_submit=True)
    tricog_geo_path_clip_function_clip_output_length = mo.ui.text(full_width=True).form(clear_on_submit=True)
    tricog_geo_path_oakland_clip_expectations = mo.ui.text(
        full_width=True, 
        label="**What will the output from clipping the Oakland parcels with the circular overlay look like?**").form(
            clear_on_submit=True,
            on_change=set_geo_path_oakland_clip_expectations
        )
    tricog_geo_path_post_clip_parcel_count_guess_box = mo.ui.text(full_width=False).form(clear_on_submit=True,
                                                                                         validate=parcel_guess_validation,
                                                                                         on_change=set_tricog_geo_path_parcel_count_guess)
    return (
        tricog_geo_path_clip_function_clip_output_length,
        tricog_geo_path_oakland_clip_expectations,
        tricog_geo_path_post_clip_parcel_count_guess_box,
        tricog_geo_path_text_box_oakland_clip_demo,
        tricog_municipality_name_text_box,
        tricog_text_path_box_countywide_muni_name_list,
        tricog_text_path_box_countywide_muni_name_list_sorted,
    )


@app.cell(hide_code=True)
def tricog_boundary_drop_down_forms(handle_tricog_path_selection, mo):
    municipal_analysis_form = (mo.md("""Select a variable to begin using: {municipal_variable_selection}<br><br>
    Explain why you chose to use that variable: {municipal_text_box}""").batch(
        municipal_variable_selection=mo.ui.dropdown(options=['assessments_df', 'parcels_df']),
        municipal_text_box=mo.ui.text_area())).form(on_change=handle_tricog_path_selection, clear_on_submit=True)
    return (municipal_analysis_form,)


@app.cell(hide_code=True)
def tricog_boundary_survey(
    handle_tricog_text_survey,
    mo,
    set_tricog_text_path_learn_text_box,
):
    tricog_text_path_list_difference_text_box = mo.ui.text_area(label="**Why are the list contents different?**",
                                                                full_width=True).form(clear_on_submit=True)

    tricog_text_path_what_did_you_learn_text_box = mo.ui.text_area(
        label=f"""**What did you learn by performing this attempt?**""", full_width=True).form(clear_on_submit=True,
                                                                                               on_change=set_tricog_text_path_learn_text_box)

    tricog_text_path_can_we_do_it_radio_buttons = mo.ui.radio(options=['Yes', 'No'])

    tricog_text_path_isolate_columns_checkbox = mo.ui.checkbox(
        label="How to access and isolate a column from a pandas/GeoPandas DataFrame using the column name")
    tricog_text_path_set_list_checkbox = mo.ui.checkbox(label="How to turn a column into a set and/or list and sort it")
    tricog_text_path_data_differences_checkbox = mo.ui.checkbox(
        label="Some of the reasons why different datasets represent the same data in different text formats, such as different publishers or purposes")
    tricog_text_path_analyze_anyway_checkbox = mo.ui.checkbox(
        label="Ways to think about matching text data when the format is different")
    tricog_text_path_other_text_box = mo.ui.text(label="Other (Enter here)")

    tricog_text_path_output_survey = mo.md("{isolate}<br>{setlist}<br>{differences}<br>{anyway}<br>{other}").batch(
        isolate=tricog_text_path_isolate_columns_checkbox, setlist=tricog_text_path_set_list_checkbox,
        differences=tricog_text_path_data_differences_checkbox, anyway=tricog_text_path_analyze_anyway_checkbox,
        other=mo.md("{one}  {two}").batch(one=mo.ui.checkbox(label=''), two=tricog_text_path_other_text_box)).form(
        label="**What did you learn?**", on_change=handle_tricog_text_survey)
    return (
        tricog_text_path_can_we_do_it_radio_buttons,
        tricog_text_path_list_difference_text_box,
        tricog_text_path_output_survey,
    )


@app.cell(hide_code=True)
def tricog_boundary_getters_setters(mo):
    # tricog_boundary_section
    get_tricog_text_path_cell_one, set_tricog_text_path_cell_one = mo.state(False)
    get_tricog_geo_path_cell_one, set_tricog_geo_path_cell_one = mo.state(False)
    get_tricog_geo_path_1a, set_tricog_geo_path_1a = mo.state(False)
    get_tricog_geo_path_1b, set_tricog_geo_path_1b = mo.state(False)
    get_tricog_geo_path_cell_two, set_tricog_geo_path_cell_two = mo.state(False)
    get_attempted_text_first, set_attempted_text_first = mo.state(False)
    get_view_clipped_parcels_df, set_view_clipped_parcels_df = mo.state(False)
    get_tricog_clip_parcels_button, set_tricog_clip_parcels_button = mo.state(False)
    get_tricog_clip_tricog_button, set_tricog_clip_tricog_button = mo.state(False)
    get_tricog_geo_path_parcel_count_guess, set_tricog_geo_path_parcel_count_guess = mo.state(False)

    get_tricog_text_path_radio_buttons, set_tricog_text_path_radio_buttons = mo.state(False)
    get_tricog_text_path_cell_two, set_tricog_text_path_cell_two = mo.state(False)
    get_tricog_text_learn_text_box, set_tricog_text_path_learn_text_box = mo.state(False)
    get_tricog_text_output_survey, set_tricog_text_output_survey = mo.state(False)

    get_tricog_text_path_cell_two, set_tricog_text_path_cell_two = mo.state(False)
    get_tricog_text_question_box_cell_two, set_tricog_text_question_box_cell_two = mo.state(False)
    get_tricog_text_question_box_cell_three, set_tricog_text_question_box_cell_three = mo.state(False)
    get_tricog_text_path_cell_three, set_tricog_text_path_cell_three = mo.state(False)
    return (
        get_attempted_text_first,
        get_tricog_clip_parcels_button,
        get_tricog_clip_tricog_button,
        get_tricog_geo_path_1a,
        get_tricog_geo_path_1b,
        get_tricog_geo_path_cell_one,
        get_tricog_geo_path_cell_two,
        get_tricog_text_output_survey,
        get_tricog_text_path_cell_one,
        get_tricog_text_path_cell_three,
        get_tricog_text_path_cell_two,
        get_tricog_text_path_radio_buttons,
        get_tricog_text_question_box_cell_three,
        get_tricog_text_question_box_cell_two,
        get_view_clipped_parcels_df,
        set_attempted_text_first,
        set_tricog_clip_parcels_button,
        set_tricog_clip_tricog_button,
        set_tricog_geo_path_1a,
        set_tricog_geo_path_1b,
        set_tricog_geo_path_cell_one,
        set_tricog_geo_path_cell_two,
        set_tricog_geo_path_parcel_count_guess,
        set_tricog_text_output_survey,
        set_tricog_text_path_cell_one,
        set_tricog_text_path_cell_three,
        set_tricog_text_path_cell_two,
        set_tricog_text_path_learn_text_box,
        set_tricog_text_path_radio_buttons,
        set_tricog_text_question_box_cell_three,
        set_tricog_text_question_box_cell_two,
        set_view_clipped_parcels_df,
    )


@app.cell(hide_code=True)
def tricog_boundary_handlers(
    selected_clip_output,
    set_attempted_text_first,
    set_tricog_clip_parcels_button,
    set_tricog_clip_tricog_button,
    set_tricog_geo_path_cell_one,
    set_tricog_text_output_survey,
    set_tricog_text_path_cell_one,
    set_tricog_text_path_cell_three,
    set_tricog_text_path_cell_two,
    set_tricog_text_path_radio_buttons,
    set_tricog_text_question_box_cell_three,
    set_tricog_text_question_box_cell_two,
):
    # tricog_boundary_section

    def handle_tricog_path_selection(value):
        if value == 'assessments_df':
            set_tricog_text_path_cell_one(True)
            set_tricog_geo_path_cell_one(False)
            return value
        if value == 'parcels_df':
            set_tricog_text_path_cell_one(False)
            set_tricog_geo_path_cell_one(True)
            set_tricog_text_path_radio_buttons(False)
            set_tricog_text_output_survey(False)
            set_tricog_geo_path_cell_one(True)
            return value
        if (value['municipal_variable_selection'] == "assessments_df"):
            set_tricog_text_path_cell_one(True)
            set_tricog_geo_path_cell_one(False)
            set_attempted_text_first(True)
            return "assessments_df"
        if (value['municipal_variable_selection'] == "parcels_df"):
            set_tricog_text_path_cell_one(False)
            set_tricog_geo_path_cell_one(True)
            return "parcels_df"

    def handle_tricog_clip_button(value):
        if value == 'parcel_base':
            set_tricog_clip_parcels_button(True)
            set_tricog_clip_tricog_button(False)
        elif value == 'tricog_base':
            set_tricog_clip_parcels_button(False)
            set_tricog_clip_tricog_button(True)

    def handle_tricog_clip_parcels_button(value):
        set_tricog_clip_parcels_button(True)
        set_tricog_clip_tricog_button(False)
        return True

    def handle_tricog_clip_tricog_button(value):
        set_tricog_clip_parcels_button(False)
        set_tricog_clip_tricog_button(True)
        return True

    def handle_tricog_text_path_dead_end_button(value):
        set_tricog_text_path_cell_one(False)
        set_tricog_text_path_cell_two(False)
        set_tricog_text_question_box_cell_two(False)
        set_tricog_text_question_box_cell_three(False)
        set_tricog_text_path_cell_three(False)
        set_tricog_text_path_radio_buttons(False)
        set_tricog_text_output_survey(False)
        set_tricog_geo_path_cell_one(True)
        set_attempted_text_first(True)


    def handle_tricog_text_len():
        if selected_clip_output:
            return len(selected_clip_output)
        else:
            return '0'

    def handle_tricog_text_path_radio_buttons(value):
        set_tricog_text_path_radio_buttons(True)

    def handle_tricog_text_survey(value):
        set_tricog_text_output_survey(True)
        return value
    return (
        handle_tricog_clip_button,
        handle_tricog_path_selection,
        handle_tricog_text_path_dead_end_button,
        handle_tricog_text_survey,
    )


@app.cell(hide_code=True)
def tricog_boundary_buttons(
    handle_tricog_clip_button,
    handle_tricog_path_selection,
    handle_tricog_text_path_dead_end_button,
    mo,
    set_view_clipped_parcels_df,
):
    # tricog_boundary_section
    tricog_geo_path_parcels_as_overlay_button = mo.ui.button(label="clipped_parcels = gp.clip(tricog_df, parcels_df)",
                                                             value='tricog_base', on_change=handle_tricog_clip_button)

    tricog_geo_path_tricog_as_overlay_button = mo.ui.button(label="clipped_parcels = gp.clip(parcels_df, tricog_df)",
                                                            value='parcel_base', on_change=handle_tricog_clip_button)

    view_clipped_parcels_button = mo.ui.run_button(label="View `clipped_oakland_parcels` dataframe",
                                                   on_change=set_view_clipped_parcels_df)

    text_analysis_btn = mo.ui.button(label="Use Text Analysis", value="TEXT", on_click=handle_tricog_path_selection)

    geo_analysis_btn = mo.ui.button(label="Use Geospatial Analysis", value="parcels_df",
                                    on_click=handle_tricog_text_path_dead_end_button)
    return (
        geo_analysis_btn,
        tricog_geo_path_parcels_as_overlay_button,
        tricog_geo_path_tricog_as_overlay_button,
        view_clipped_parcels_button,
    )


@app.cell(hide_code=True)
def _(
    CLIPPED_PARCELS_PATH,
    CLIPPED_PARCELS_TRICOG_BASE_PATH,
    OVERLAY_LAYER,
    assessments_df,
    get_start_analysis_button,
    gp,
    mo,
    oakland_parcel_exploration,
):
    # Analysis prep

    # text_analysis_button = mo.ui.run_button(label="Use Text Analysis")
    # geospatial_button = mo.ui.run_button(label="Use Geospatial Analysis")

    # other
    if get_start_analysis_button():
        if assessments_df is not None:
            munis = list(set(assessments_df.MUNIDESC))
            munis.sort()
            list_of_sorted_munis = munis[:20]
        with mo.status.spinner(
                title="Reading files necessary for the next section",
                subtitle="Please be patient, this may take a minute"
        ) as _spinner:
            clipped_parcels = gp.read_file(CLIPPED_PARCELS_PATH)
            # clipped_parcels_df = pd.DataFrame(clipped_parcels.astype({'geometry':'str'}))
            clipped_parcels_df = clipped_parcels.iloc[0:, 0:-1]
            clipped_parcels_tricog_base = gp.read_file(CLIPPED_PARCELS_TRICOG_BASE_PATH)
            clipped_parcels_tricog_base_df = clipped_parcels_tricog_base.iloc[0:30, 0:24]
            # clipped_parcels_tricog_base_df = pd.DataFrame(clipped_parcels_tricog_base.astype({'geometry':'str'}))
            m = oakland_parcel_exploration
            overlay = gp.read_file(OVERLAY_LAYER)
    return (
        clipped_parcels,
        clipped_parcels_df,
        clipped_parcels_tricog_base,
        clipped_parcels_tricog_base_df,
        m,
        overlay,
    )


@app.cell(hide_code=True)
def _(get_start_analysis_button, mo):
    view_analysis = get_start_analysis_button()

    mo.stop(not view_analysis)

    tricog_intro_output = mo.vstack(
        [
            mo.md(f"""###Finding Parcels Within TriCOG's Boundaries"""),
            mo.md("""
    Now that we've loaded various datafiles with information about the county's parcels and TriCOG's borders, we can begin to find parcels that fall within those borders. You may remember from the introduction that finding parcels within TriCOG's boundaries was our first objective. And it's an important one! State law only allows TriCOG to operate within a certain boundary, so it is crucial that the properties included on your list of recommended acquisitions be within those boundaries. 

    In order to achieve this goal, we'll need to know what the TriCOG boundaries are, and what parcels are inside them. `tricog.geojson`, which we loaded in the last step (and saved as `tricog_df`), has both the names of the municipalities (towns, boroughs, and such) where TriCOG can operate, and it also has the geospatial borders for each of those municipalities.  

    Two of the dataframes that were generated in the previous step were read from files that have county-wide parcel data: <br> 1. `assessments_df` (from the assessments.csv file) has text data about the parcels, including the names of the municipalites each parcel is inside of.<br>2. `parcels_df` (from the parcels.geojson file) includes geospatial data, allowing you to see where the parcels are located on a map.
    <br>

    We can use Python to compare the parcels' municipality names listed in `assessments_df` to the allowable municipality names in `tricog_df`, or we can compare the location of each parcel from `parcels_df` to the location of the municipalities in `tricog_df`.<br>

    Do you think it's better to start with `assessments_df` and analyze the text? Or is it better to start with `parcels_df` and analyze the geospatial data? In the form below, select which dataframe you think would make a better choice to work with. Then, in the text box, explain why you think that choice is the best. (Don't worry too much, you can always go back and re-choose later if you change your mind!)<br>
    """)
        ]
    )

    mo.output.replace(tricog_intro_output)
    return (view_analysis,)


@app.cell(hide_code=True)
def _(get_attempted_text_first, mo, municipal_analysis_form, view_analysis):
    mo.stop(not view_analysis and get_attempted_text_first())

    if not get_attempted_text_first():
        mo.output.replace(municipal_analysis_form)
    else:
        mo.output.clear()
    return


@app.cell(hide_code=True)
def _():
    # text options for tricog path

    tricog_text = {
        'geo_path': {
            'cell_one_text': {
                'part_one':
                    f"""One method to find the parcels we're looking for is to use the GeoPandas clip function. Clip is a tool that is common across GIS programs (such as ArcGIS, QGIS, and others). The tool 'clips' a geospatial file to the boundaries of a second file that you specify (referred to as an "overlay layer"). You can think of clipping like using a cookie cutter on cookie dough; the clip function returns only the features (dough) that fell within the overlay layer's boundaries (cookie cutter). In GeoPandas, the clip function returns a new dataframe, where every row contains data from the base layer, so long as the data is within the overlay layer's boundaries. Data outside of those boundaries is excluded.<br><br>In GeoPandas, the clip function returns a new dataframe, where every row contains data from the base layer, and is a geospatial feature located within the overlay layer. The format for using the clip function in GeoPandas is as follows: <br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;*output_variable_name* = **gp.clip(** *base_layer_name*,  *overlay_layer_name* **)** <br>There are additional parameters that can be used in the function, but this is all we will need for this example. <br><br> Let's look at the parcels from Oakland that were introduced above. This time, however, you'll notice that there's a blue circle in the middle of the map. This blue circle is a shape that we'll use as our overlay layer on the Oakland parcels, as a demonstration. (Overlay layers from real-world data are rarely perfect shapes, but this is just an example).""",
                'part_two':
                    f"<br>For this example, the base layer is named `oakland_parcels_df` and the overlay layer is named `overlay`. Using the GeoPandas `clip` function format outlined above, write the clip function in the box below and hit Submit.<br><br>",
            },
            'cell_one_a_clipping_text': {
                'part_one':
                    f"The clip function that you just ran generated a new GeoPandas dataframe, which we have stored in the variable `clipped_oakland_parcels`. The output dataframe has the same columns as the base layer dataframe (`oakland_parcels`). The data in columns that have descriptive data (such as PIN and MAPBLOCKLO) have remained the same, but the columns with geospatial data have updated to reflect the size of the output parcels.<br><br> Click the button below if you would like to look at the dataframe.",
                'optional_dataframe_button_text':
                    f"At a quick glance, you can see that the dataframe only has [x number] of rows, but if you scroll up to the map above with the original oakland_parcels mapped out, you can notice that the map clearly displays more consider whether or not the parcels than that (in fact, it has [y number] of parcels). This is piece of evidence we can use to clip function worked: if the overlay layer was smaller than the base layer, but the output dataframe had the same number of rows, it would suggest that something went wrong. (This is not a full confirmation of success or failure - just one partial check).",
                'part_two':
                    f"Just like we did before with the tricog_df dataframe, we can visualize the `clipped_oakland_parcels` dataframe using the explore method! Before we do that, though, take a second to think about what the output will look like when mapped out. Before you ran the clip function, you had a group of parcels, and a circular overlay layer on top of them. What will `clipped_oakland_parcels` look like? Consider, for example: if a parcel was partially inside and partially outside of the overlay layer, will it be included in the output? Will it be completely included? Will it be cut in half? Describe how you imagine the result of the clipping will look when you map it in the text box. <br><br>",
            },
            'cell_one_b_clipping_text': {
                'part_one':
                    f"As you can see above, the parcels that are left fit into the shape made by the overlay layer. Any parcel that extended outside of the overlay layer was cut along the border of the overlay layer, and only the portion of the parcel inside the overlay layer remains. (Just like cookie cutters and cookie dough!) The remaining parcels have the same descriptive data in the new dataframe -- the PIN and MAPBLOCKLO are the same, but the shapes' lengths and areas represent their new, smaller, shape.<br><br>",
            },
            'cell_two': {
                'part_one':
                    f"Now that we have seen how clip works, let's try it on the countywide parcel set. Remember: we are trying to find the parcels within the county (`parcels_df`) that are within TriCOG's operating boundaries (`tricog_df`).<br><br> With that goal in mind, which file would be the base layer, and which file would be the overlay layer? Select your response below and click 'run' to try it out.",
                'part_two':
                    f""
            },
        }
    }
    return (tricog_text,)


@app.cell
def _(mo):
    mo.Html('<div id="geospatial_analysis"></div>')
    return


@app.cell(hide_code=True)
def tricog_path_header(
    get_tricog_geo_path_cell_one,
    get_tricog_text_path_cell_one,
    mo,
):
    tricog_text_path_cell_one = get_tricog_text_path_cell_one()
    tricog_geo_path_cell_one = get_tricog_geo_path_cell_one()
    mo.stop(not tricog_text_path_cell_one and not tricog_geo_path_cell_one)

    if tricog_text_path_cell_one:
        mo.output.replace(
            mo.md(f"""##Text Analysis""")
        )
    elif tricog_geo_path_cell_one:
        mo.output.replace(
            mo.md(f"""##Geospatial Analysis""")
        )
    else:
        mo.output.clear()
    return (tricog_geo_path_cell_one,)


@app.cell
def tricog_path_cell_1(
    get_attempted_text_first,
    get_tricog_text_path_cell_one,
    handle_tricog,
    m,
    mo,
    overlay,
    time,
    tricog_df,
    tricog_geo_path_cell_one,
    tricog_municipality_name_expected_code,
    tricog_text,
):
    # tricog path, text choice, cell 1

    mo.stop(not get_tricog_text_path_cell_one() and not tricog_geo_path_cell_one)
    tricog_text_path_cell_two = False
    # tricog_geo_path_cell_two = False 

    # text analysis path
    if get_tricog_text_path_cell_one():
        mo.output.replace(
            mo.vstack(
                [
                    mo.md(f"""Let's take a look at the TriCOG boundaries again: """),
                    handle_tricog(tricog_df),
                    mo.md(f"""As you can see in the above, there is a column named "NAME" that contains the names of the municipalities included in their operating boundaries.

                    We can isolate these names as a list and then compare them to the municipality names found in the assessments file that was introduced above.

                    Type the following code into the text entry box as it appears and hit 'Submit'<br>
                    `tclb_municipalities = {tricog_municipality_name_expected_code}`"""),
                ]
            )
        )


    # geo analysis path
    elif tricog_geo_path_cell_one:
        if get_attempted_text_first():
            time.sleep(1)
        mo.output.replace(
            mo.vstack(
                [
                    mo.md(tricog_text['geo_path']['cell_one_text']['part_one']),
                    overlay.explore(m=m, fillColor='blue', opacity=0.25, fillOpacity=0.25, ),

                ]))
    else:
        mo.output.clear()
    return


@app.cell
def _(
    get_tricog_text_path_cell_one,
    mo,
    set_tricog_text_path_cell_two,
    tricog_df,
    tricog_municipality_name_expected_code,
    tricog_municipality_name_text_box,
):
    mo.stop(not get_tricog_text_path_cell_one())

    if get_tricog_text_path_cell_one(): 
        mo.output.replace(
            mo.hstack(
                [
                    mo.md(f"""`tclb_municipalities = `"""), tricog_municipality_name_text_box,
                ], 
                gap=0, justify="space-around", align='center', widths=[1, 5]
            )
        )

        tricog_muni_user_text_entry = tricog_municipality_name_text_box.value
        if tricog_muni_user_text_entry:
            if tricog_muni_user_text_entry == tricog_municipality_name_expected_code:
                tclb_municipalities = list(set(tricog_df.NAME))
                tclb_municipalities.sort()
                mo.output.replace_at_index("Correct!", 1)
                set_tricog_text_path_cell_two(True)
            else:
                mo.output.append("Try again")

    else: 
        mo.output.clear()
    return (tclb_municipalities,)


@app.cell(hide_code=True)
def _(
    get_oakland_overlay_counter,
    incorrect_answer_text_generator,
    mo,
    oakland_overlay_expected_output,
    set_tricog_geo_path_1a,
    strip_string,
    tricog_geo_path_cell_one,
    tricog_geo_path_text_box_oakland_clip_demo,
    tricog_text,
):
    mo.stop(not tricog_geo_path_cell_one)
    oakland_overlay_output_response = ''

    if tricog_geo_path_cell_one:
        mo.output.replace(
            mo.vstack(
                [
                    mo.md(tricog_text['geo_path']['cell_one_text']['part_two']),
                    mo.hstack(
                        [
                            mo.md(f"""**clipped_oakland_parcels  =**"""),
                            tricog_geo_path_text_box_oakland_clip_demo,
                        ], gap=0, justify="space-around", align='center', widths=[1, 5]),
                ]
            )
        )
        if tricog_geo_path_text_box_oakland_clip_demo.value:
            oakland_overlay_input = tricog_geo_path_text_box_oakland_clip_demo.value
            oakland_overlay_expected_output_stripped = strip_string(oakland_overlay_expected_output)
            if strip_string(oakland_overlay_input) == oakland_overlay_expected_output_stripped:
                # clipped_oakland_parcels = gp.clip(oakland_parcels_df, overlay)
                # clipped_oakland_parcels_df = pd.DataFrame(clipped_oakland_parcels.astype({'geometry': 'str'}))
                set_tricog_geo_path_1a(True)
                mo.output.replace_at_index(f"""Correct!""", 1)
            else:
                oakland_overlay_output_response = incorrect_answer_text_generator(oakland_overlay_input,
                                                                                  oakland_overlay_expected_output,
                                                                                  get_oakland_overlay_counter())
                mo.output.replace_at_index(f"""{oakland_overlay_output_response[0]}""", 1)
    else:
        mo.output.clear()
    return


@app.cell(hide_code=True)
def tricog_path_cell_1a_clipping(
    get_tricog_geo_path_1a,
    gp,
    mo,
    oakland_parcels_df,
    overlay,
    pd,
    tricog_text,
    view_clipped_parcels_button,
):
    mo.stop(not get_tricog_geo_path_1a())
    clipped_oakland_parcels = gp.clip(oakland_parcels_df, overlay)
    clipped_oakland_parcels_df = pd.DataFrame(clipped_oakland_parcels.astype({'geometry': 'str'}))
    if get_tricog_geo_path_1a():
        mo.output.replace(
            mo.vstack([
                mo.md(tricog_text['geo_path']['cell_one_a_clipping_text']['part_one']),
                view_clipped_parcels_button,
            ]
            )
        )
    else:
        mo.output.clear()
    return clipped_oakland_parcels, clipped_oakland_parcels_df


@app.cell(hide_code=True)
def _(clipped_oakland_parcels_df, get_view_clipped_parcels_df, mo):
    mo.stop(not get_view_clipped_parcels_df())
    mo.vstack(
        [
            mo.md(f"""###clipped_oakland_parcels"""),
            clipped_oakland_parcels_df
        ]
    )
    return


@app.cell(hide_code=True)
def _(
    get_tricog_geo_path_1a,
    mo,
    set_tricog_geo_path_1b,
    tricog_geo_path_oakland_clip_expectations,
    tricog_text,
):
    # mo.stop(strip_string(oakland_overlay_input) != oakland_overlay_expected_output_stripped)
    mo.stop(not get_tricog_geo_path_1a())
    tricog_geo_path_cell_one_a = False
    if get_tricog_geo_path_1a():
        mo.output.replace(
            mo.vstack([
                mo.md(tricog_text['geo_path']['cell_one_a_clipping_text']['part_two']),
                tricog_geo_path_oakland_clip_expectations,
            ])
        )
        if tricog_geo_path_oakland_clip_expectations.value:
            tricog_geo_path_cell_one_a = True
            set_tricog_geo_path_1b(True)
    else:
        mo.output.clear()
    return (tricog_geo_path_cell_one_a,)


@app.cell(hide_code=True)
def _(
    clipped_oakland_parcels,
    get_tricog_geo_path_1b,
    mo,
    tricog_geo_path_cell_one_a,
    tricog_text,
):
    mo.stop(not get_tricog_geo_path_1b())
    if tricog_geo_path_cell_one_a:
        clipped_oakland_parcels_exploration = clipped_oakland_parcels.explore(
            style_kwds=dict(color='black', fillColor='yellow'))
        mo.output.replace(
            mo.vstack(
                [
                    clipped_oakland_parcels_exploration,
                    mo.md(tricog_text['geo_path']['cell_one_b_clipping_text']['part_one']),
                ]
            )
        )
    else:
        mo.output.clear()
    return


@app.cell(hide_code=True)
def _(
    mo,
    tricog_geo_path_cell_one_a,
    tricog_geo_path_parcels_as_overlay_button,
    tricog_geo_path_tricog_as_overlay_button,
    tricog_text,
):
    mo.stop(not tricog_geo_path_cell_one_a)

    mo.output.replace(
        mo.vstack(
            [
                mo.md(tricog_text['geo_path']['cell_two']['part_one']),
                mo.md(f"""###Select the Correct Function:<br>"""),
                mo.hstack(
                    [tricog_geo_path_parcels_as_overlay_button, tricog_geo_path_tricog_as_overlay_button],
                    justify='space-around'
                ),
            ]
        )
    )
    return


@app.cell(hide_code=True)
def _(
    ARROW_IMAGE_PATH,
    PARCELS_CLIPPED_TO_TRICOG_IMG_PATH,
    TRICOG_BASE_PARCEL_OVERLAY_IMG_PATH,
    TRICOG_CLIPPED_TO_PARCELS_IMG_PATH,
    TRICOG_OVER_PARCELS_IMG_PATH,
    get_tricog_clip_parcels_button,
    get_tricog_clip_tricog_button,
    mo,
):
    mo.stop(not get_tricog_clip_parcels_button() and not get_tricog_clip_tricog_button())
    if get_tricog_clip_tricog_button():
        selected_base_layer = 'tricog_df'
        selected_overlay_layer = 'parcels_df'
        mo.output.replace(
            mo.vstack(
                [
                    mo.hstack([mo.image(TRICOG_BASE_PARCEL_OVERLAY_IMG_PATH, width=1195 * .3, height=844 * .3),
                               mo.image(ARROW_IMAGE_PATH, width=452 * .5, height=398 * .5),
                               mo.image(TRICOG_CLIPPED_TO_PARCELS_IMG_PATH, width=1194 * .3, height=846 * .3)],
                              justify='space-around', align='center')
                ]
            )
        )
    elif get_tricog_clip_parcels_button():
        selected_base_layer = 'parcels_df'
        selected_overlay_layer = 'tricog_df'
        mo.output.replace(
            mo.vstack(
                [
                    mo.hstack([mo.image(TRICOG_OVER_PARCELS_IMG_PATH, width=1194 * .3, height=838 * .3),
                               mo.image(ARROW_IMAGE_PATH, width=452 * .5, height=398 * .5),
                               mo.image(PARCELS_CLIPPED_TO_TRICOG_IMG_PATH, width=1199 * .3, height=847 * .3)],
                              justify='space-around', align='center')
                ]
            )
        )
    else:
        mo.output.clear()
    return selected_base_layer, selected_overlay_layer


@app.cell(hide_code=True)
def _(
    get_tricog_clip_parcels_button,
    get_tricog_clip_tricog_button,
    mo,
    selected_base_layer,
    selected_overlay_layer,
    set_tricog_geo_path_cell_two,
    tricog_geo_path_post_clip_parcel_count_guess_box,
):
    mo.stop(not get_tricog_clip_parcels_button() and not get_tricog_clip_tricog_button())
    mo.output.replace(
        mo.vstack(
            [
                mo.md(
                    f"""The images above represent your selection (because the files are too large to load with the explore method!): because `{selected_base_layer}` is the first argument listed in the clip function, it is the base layer. It's styled in yellow in the image. And because `{selected_overlay_layer}` is the second argument, it is the overlay layer (represented in blue). After running clip, the image on the right displays what the clipped `{selected_base_layer}` would look like in the explore function (if the files weren't so big!).  

    The shape looks like what we would expect! But because we can't explore the images in the same way we explored other files, let's take a look at the dataframe and see if that looks right.  

    There were over 500,000 parcels across the whole county, and we are trying to find how many of them are in the 30 municipalities that TriCOG operates in. How many rows (parcels) do you think the clipped `{selected_base_layer}` dataframe will have?"""),
                tricog_geo_path_post_clip_parcel_count_guess_box.center(),
            ]
        )
    )
    if tricog_geo_path_post_clip_parcel_count_guess_box.value:
        set_tricog_geo_path_cell_two(True)
    return


@app.cell(hide_code=True)
def _(tricog_geo_path_post_clip_parcel_count_guess_box):
    parcel_count_guess = None
    if tricog_geo_path_post_clip_parcel_count_guess_box.value:
        parcel_count_guess = int(tricog_geo_path_post_clip_parcel_count_guess_box.value)
    return


@app.cell
def tricog_path_cell_2(
    assessments_df,
    clipped_parcels_df,
    clipped_parcels_tricog_base,
    clipped_parcels_tricog_base_df,
    countywide_municipality_name_list,
    get_tricog_clip_parcels_button,
    get_tricog_clip_tricog_button,
    get_tricog_geo_path_cell_two,
    get_tricog_text_path_cell_two,
    mo,
):
    mo.stop(not get_tricog_text_path_cell_two() and not get_tricog_geo_path_cell_two())
    tricog_text_question_box_two_bool = False
    tricog_geo_question_box_two_bool = False
    begin_residential_path = False

    if get_tricog_text_path_cell_two():
        mo.output.replace(
            mo.vstack(
                [
                    mo.md(
                        f"""Looking back at the assessments file, we can see a column named "MUNIDESC". That means Municipal Description -- the text name of the municipality that that row's parcel is in."""),
                    assessments_df,
                    mo.md(f"""The size of the spreadsheet makes it hard to get a sense of what the values in that column are. Let's take a look at a de-duplicated list of values from that column. But using three lines of code, we can get a nice, short sample of unique names in the MUNIDESC field. 
                    <br><br>To start, enter the code below and hit 'Submit' to take the first step, which isolates the MUNICDESC column, removes all duplicates, and converts it to a list that we can reorder and subsample. """),
                    mo.md(f"""`munidesc = {countywide_municipality_name_list}`"""),  
                ]
            )
        )
    elif get_tricog_geo_path_cell_two():
        if get_tricog_clip_parcels_button():
            clip_attempt_output = mo.vstack(
                [
                    mo.md(f"""###clipped_parcels"""),
                    clipped_parcels_df,
                    mo.md(f"""You've produced the dataframe `clipped_parcels` -- it looks like the `clip` function worked! The final number of rows is {len(clipped_parcels_df)}. That's significantly less than the 500,000 we started with.<br><br>
                    If you want to explore these clipped parcels on a map and you have GIS software, you can output the `clipped_parcels` variable using `GeoPandas`' `to_file()` command. The argument you would use in the function is the name you want the outputted file to have. Running the command: <br>

                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`clipped_parcels.to_file("clipped_parcels_output.geojson")`
    <br><br>
                    would create a file in your current working directory called `clipped_parcels_output.geojson`. 

                    Unfortunately, the specifics of using standalone GIS software to view the file are outside the scope of this lesson."""),
                ]
            )
            begin_residential_path = True
        if get_tricog_clip_tricog_button():
            clip_attempt_output = mo.vstack(
                [
                    clipped_parcels_tricog_base_df,
                    mo.md(f"""The final number of rows is {len(clipped_parcels_tricog_base)}. That number seems suspiciously low. If it also seems \
                    familiar, it's because it's the same number of municipalities within TriCOG's borders.<br><br>
                    Remember we said earlier than when you run the clip function, the output dataframe contains only matching data from \
                    the base layer. In this case, because you selected `tricog_df` as the base layer, the output only contains data that \
                    was from `tricog_df`. We were hoping that our output file would contain data about the parcels within these \
                    boundaries.<br><br>
                    Scroll back up and select the other clip function option (with `parcels_df` as the base layer) and see if that \
                    makes a difference."""),
                ]
            )
            begin_residential_path = False
        mo.output.replace(
            clip_attempt_output
        )
    else:
        mo.output.clear()
    return begin_residential_path, tricog_geo_question_box_two_bool


@app.cell
def _(
    assessments_df,
    countywide_municipality_name_list,
    get_tricog_text_path_cell_two,
    mo,
    set_tricog_text_question_box_cell_two,
    tricog_text_path_box_countywide_muni_name_list,
):
    mo.stop(not get_tricog_text_path_cell_two())

    if get_tricog_text_path_cell_two():
        mo.output.replace(
            mo.hstack(
                [
                    mo.md(f"""`munidesc = `"""), tricog_text_path_box_countywide_muni_name_list,
                ], 
                gap=0, 
                justify="space-around", 
                align='center', 
                widths=[1, 7]
            ),
        )
        if tricog_text_path_box_countywide_muni_name_list.value:
            if tricog_text_path_box_countywide_muni_name_list.value == countywide_municipality_name_list:
                munidesc = list(set(assessments_df.MUNIDESC))
                mo.output.replace_at_index('Correct!', 1)
                set_tricog_text_question_box_cell_two(True)
            else:
                mo.output.append('Try again!')
    else: 
        mo.output.clear()
    return (munidesc,)


@app.cell(hide_code=True)
def tricog_path_cell_2a(
    clip_function_clip_output_length_code,
    clipped_parcels,
    countywide_municipality_name_list_sorted,
    get_tricog_text_question_box_cell_two,
    mo,
    munidesc,
    parcels_df,
    set_tricog_text_question_box_cell_three,
    tricog_geo_path_clip_function_clip_output_length,
    tricog_geo_question_box_two_bool,
    tricog_text_path_box_countywide_muni_name_list_sorted,
):
    mo.stop(not get_tricog_text_question_box_cell_two() and not tricog_geo_question_box_two_bool)
    tricog_text_question_box_three_bool = False

    if get_tricog_text_question_box_cell_two():
        mo.output.replace(
            mo.vstack(
                [
                    mo.md(
                        f"""<br>This piece of code will sort the municipality names, to make sure we're all looking at the same list.<br>Type the code into the box and submit it."""),
                    mo.md(text=f"""`{countywide_municipality_name_list_sorted}`"""),
                    tricog_text_path_box_countywide_muni_name_list_sorted,
                ],
            )
        )
        if tricog_text_path_box_countywide_muni_name_list_sorted.value:
            if tricog_text_path_box_countywide_muni_name_list_sorted.value == countywide_municipality_name_list_sorted:
                mo.output.replace_at_index('Correct!', 1)
                munidesc.sort()
                set_tricog_text_question_box_cell_three(True)
            else:
                mo.output.append('Try again!')
    elif tricog_geo_question_box_two_bool:
        mo.output.replace(
            mo.vstack(
                [
                    mo.md(f"""`{clip_function_clip_output_length_code}`"""),
                    tricog_geo_path_clip_function_clip_output_length,
                ]
            )
        )
        if tricog_geo_path_clip_function_clip_output_length.value:
            if tricog_geo_path_clip_function_clip_output_length.value == clip_function_clip_output_length_code:
                output_to_append = mo.md(f"""Correct!<br><br>length of parcels: `{len(parcels_df)}`<br>
                          length of clipped_parcels: `{len(clipped_parcels)}`""")
                mo.output.replace_at_index(output_to_append, 1)
            else:
                mo.output.append("Try again!")

    else:
        mo.output.clear()
        parcel_length_code = "f''"
        clip_length_code = "f'length of clipped_parcels: {len(clipped_parcels)}'"
    return


@app.cell
def tricog_path_cell_2b(
    get_tricog_text_question_box_cell_three,
    mo,
    munidesc,
    tclb_municipalities,
):
    mo.stop(not get_tricog_text_question_box_cell_three())
    tricog_text_path_cell_three = False

    if get_tricog_text_question_box_cell_three():
        mo.output.replace(
            mo.vstack(
                [
                    mo.md(f"""Now that we have generated lists of the unique municipality names from both of the dataframes, \
                    we can compare the lists to each other and see if text matching seems feasible. Let's look at the first \
                    twenty municipalities from both lists side by side.<br><br>"""),
                    mo.hstack(
                        [
                            mo.vstack(
                                [
                                    mo.md(f"""Municipalities in `tricog_df` (First 20)"""),
                                    tclb_municipalities[:20],
                                    mo.md(
                                        f"""Number of unique municipalities in `tricog_df`: {len(tclb_municipalities)}""")
                                ]
                            ),
                            mo.vstack(
                                [
                                    mo.md(f"""Municipalities in `assessments_df` (First 20)"""),
                                    munidesc[:20],
                                    mo.md(f"""Number of unique municipalities in `assessments_df`: {len(munidesc)}""")
                                ]
                            ),
                        ], justify='space-between'
                    ),
                    mo.md(f"""Already, things look a bit unusual. The two lists are formatted differently, and the list from `assessments_df` includes multiple entries for certain municipalities, like Pittsburgh.<br><br>
                    We can see that both dataframes have some of the same municipality names, such as Clairton and McKeesport. If \
                    the data is about the same municipalities, why are the list contents formatted differently? Enter your thoughts \
                    into the box and hit `Submit`.<br>"""),
                ]
            )
        )
    else:
        mo.output.clear()
    return


@app.cell
def _(
    get_tricog_text_question_box_cell_three,
    mo,
    set_tricog_text_path_cell_three,
    tricog_text_path_list_difference_text_box,
):
    mo.stop(not get_tricog_text_question_box_cell_three())

    if get_tricog_text_question_box_cell_three(): 
        mo.output.replace(
            tricog_text_path_list_difference_text_box
        )
        if tricog_text_path_list_difference_text_box.value:
            set_tricog_text_path_cell_three(True)
    else:
        mo.output.clear()
    return


@app.cell(hide_code=True)
def _(
    get_tricog_text_path_cell_three,
    mo,
    set_tricog_text_path_radio_buttons,
    tricog_text_path_can_we_do_it_radio_buttons,
    tricog_text_path_list_difference_text_box,
):
    mo.stop(not get_tricog_text_path_cell_three())

    if get_tricog_text_path_cell_three():
        mo.output.replace(
            mo.vstack(
                [
                    mo.md(f"""Your answer was: _{tricog_text_path_list_difference_text_box.value}_.<br>
                    There are many valid answers that can explain why the municipalities are listed so differently, but here are two\
                    reasons data about the same objects can differ from one dataframe to another:<br><br> 
                    1. **The dataframes were made by different organizations/agencies that were not coordinating with each other.**<br>
                    In this case, the data from `tricog_df` was created by TriCOG, and `assessments_df` was created by Allegheny County.
                    <br><br>
                    2. **The data is collected for different purposes**. <br>
                    `tricog_df` was created for in-house use at TriCOG to have a map of their boundaries. `assessments_df` was created \
                    to maintain financial assessment data on every parcel across the county. It may make sense for the county to keep \
                    track of wards to compare parcels and properties, but TriCOG may not have that need. """),
                    mo.md(f"""Despite these differences, can we still use text analysis to find matches between the TriCOG municipalities \
                    and the assessments municipalities?<br>"""),
                    tricog_text_path_can_we_do_it_radio_buttons,
                ]
            )
        )
        if tricog_text_path_can_we_do_it_radio_buttons.value:
            set_tricog_text_path_radio_buttons(True)
    # elif geo_flag:
    #     pass
    else:
        mo.output.clear()
    return


@app.cell
def _(
    get_tricog_text_path_radio_buttons,
    mo,
    tricog_text_path_can_we_do_it_radio_buttons,
):
    mo.stop(not get_tricog_text_path_radio_buttons())
    tricog_text_path_radio_button_response = ""
    if tricog_text_path_can_we_do_it_radio_buttons.value == "Yes":
        tricog_text_path_radio_button_response = f"""Correct! We still could try and match the municipalities between the two files."""
    if tricog_text_path_can_we_do_it_radio_buttons.value == "No":
        tricog_text_path_radio_button_response = f"""We actually could still try and match them!"""

    if get_tricog_text_path_radio_buttons():
        mo.output.replace(
            mo.vstack(
                [
                    mo.md(tricog_text_path_radio_button_response),
                    mo.md(f"""However, it would require a lot of work. To do so, we would need to standardize the data: you would want to \
                    think about the ways in which the data is formatted differently and remove those differences. In this case, that includes \
                    making the capitalization match, removing ward references, and finding (and correcting) any other differences in \
                    formatting that may exist between the two lists after the first twenty entries. """),
                    mo.md(f"""It may be frustrating to go through a series of analysis steps that lead to a dead end, but usually \
                    doing so has the silver lining of helping you learn something new. Look at the list below and select any of the \
                    following items that you learned through this text-analysis process. You can also add your own in the text entry \
                    box. """),
                ]
            )
        )
    else:
        mo.output.clear()
    return


@app.cell
def _(get_tricog_text_path_radio_buttons, mo, tricog_text_path_output_survey):
    mo.stop(not get_tricog_text_path_radio_buttons())

    if get_tricog_text_path_radio_buttons():
        mo.output.replace(
            tricog_text_path_output_survey
        )
    else:
        mo.output.clear()
    return


@app.cell
def _(
    geo_analysis_btn,
    get_tricog_text_output_survey,
    mo,
    tricog_geo_path_cell_one,
):
    mo.stop(not get_tricog_text_output_survey() and not tricog_geo_path_cell_one)

    geo_analysis_btn_with_link = mo.md(f"""<a href=#geospatial_analysis>""""""{geo_analysis_btn}</a>""").batch(geo_analysis_btn=geo_analysis_btn)

    if get_tricog_text_output_survey():
        mo.output.replace(
            mo.vstack(
                [
                    mo.md(
                        f"""Now that we've exhausted this path and reflected on what we learned, it may be time to try the geographic analysis path. Click the button below to begin that task.<br><br>"""),
                    geo_analysis_btn_with_link.center()
                ]
            )
        )
    else:
        mo.output.clear()
    return


@app.cell(hide_code=True)
def residential_prep(handle_residential_filter, mo, set_residential_path_zero):
    # residential path prep

    # buttons
    residential_start_button = mo.ui.run_button(label="Push to Start", on_change=set_residential_path_zero)

    # text_boxes
    residential_text_box_parcel_class_descriptions = mo.ui.text(full_width=True).form(clear_on_submit=True)
    residential_text_box_only_classdesc_value_residential = mo.ui.text(full_width=True).form(clear_on_submit=True)
    residential_text_box_final_classdesc_usedesc_filter = mo.ui.text(full_width=True).form(clear_on_submit=True,
                                                                                           on_change=handle_residential_filter)

    # chat variable
    response_message = "I'm glad you asked! The assessments file is very large and confusing. You'll want to find parcels where the CLASSDESC value is 'RESIDENTIAL' and the USEDESC value is 'SINGLE FAMILY'."

    def generate_usedesc_incorrect_singular_or_plural_text(usedesc_value_dict: dict[str, bool])->str:
        usedesc_incorrect_responses_counter = 0
        for a, b in usedesc_value_dict.items():
            if b == True:
                usedesc_incorrect_responses_counter += 1
        if usedesc_incorrect_responses_counter == 1: 
            return 'that makes'
        else: 
            return 'any of those make'
    return (
        generate_usedesc_incorrect_singular_or_plural_text,
        residential_start_button,
        residential_text_box_final_classdesc_usedesc_filter,
        response_message,
    )


@app.cell(hide_code=True)
def residential_path_text_boxes(mo, set_column_boolean_explanation_box):
    # column_guess_text_box = mo.ui.text_area(label="**Which column has data about residential parcels?**", full_width=True).form(on_change=handle_column_text_box, clear_on_submit=True)

    column_boolean_explanation_box = mo.ui.text_area(label="**Why did all the values become True or False?**",
                                                     full_width=True).form(on_change=set_column_boolean_explanation_box,
                                                                           clear_on_submit=True)
    return (column_boolean_explanation_box,)


@app.cell(hide_code=True)
def residential_path_checkboxes(
    handle_column_radio_buttons,
    mo,
    set_residential_path_usedesc_checkbox,
):
    assessments_df_columns = ['PARID', 'PROPERTYHOUSENUM', 'PROPERTYFRACTION', 'PROPERTYADDRESS',
                              'PROPERTYCITY', 'PROPERTYSTATE', 'PROPERTYUNIT', 'PROPERTYZIP',
                              'MUNICODE', 'MUNIDESC', 'SCHOOLCODE', 'SCHOOLDESC', 'LEGAL1', 'LEGAL2',
                              'LEGAL3', 'NEIGHCODE', 'NEIGHDESC', 'TAXCODE', 'TAXDESC', 'TAXSUBCODE',
                              'TAXSUBCODE_DESC', 'OWNERCODE', 'OWNERDESC', 'CLASS', 'CLASSDESC',
                              'USECODE', 'USEDESC', 'LOTAREA', 'HOMESTEADFLAG', 'FARMSTEADFLAG',
                              'CLEANGREEN', 'ABATEMENTFLAG', 'RECORDDATE', 'SALEDATE', 'SALEPRICE',
                              'SALECODE', 'SALEDESC', 'DEEDBOOK', 'DEEDPAGE', 'PREVSALEDATE',
                              'PREVSALEPRICE', 'PREVSALEDATE2', 'PREVSALEPRICE2',
                              'CHANGENOTICEADDRESS1', 'CHANGENOTICEADDRESS2', 'CHANGENOTICEADDRESS3',
                              'CHANGENOTICEADDRESS4', 'COUNTYBUILDING', 'COUNTYLAND', 'COUNTYTOTAL',
                              'COUNTYEXEMPTBLDG', 'LOCALBUILDING', 'LOCALLAND', 'LOCALTOTAL',
                              'FAIRMARKETBUILDING', 'FAIRMARKETLAND', 'FAIRMARKETTOTAL', 'STYLE',
                              'STYLEDESC', 'STORIES', 'YEARBLT', 'EXTERIORFINISH', 'EXTFINISH_DESC',
                              'ROOF', 'ROOFDESC', 'BASEMENT', 'BASEMENTDESC', 'GRADE', 'GRADEDESC',
                              'CONDITION', 'CONDITIONDESC', 'CDU', 'CDUDESC', 'TOTALROOMS',
                              'BEDROOMS', 'FULLBATHS', 'HALFBATHS', 'HEATINGCOOLING',
                              'HEATINGCOOLINGDESC', 'FIREPLACES', 'BSMTGARAGE', 'FINISHEDLIVINGAREA',
                              'CARDNUMBER', 'ALT_ID', 'TAXYEAR', 'ASOFDATE']

    assessments_columns_radio_buttons = mo.ui.radio(options=assessments_df_columns,
                                                    on_change=handle_column_radio_buttons)

    FOUR_FAMILY_CHECKBOX = mo.ui.checkbox(label='FOUR FAMILY')
    CONDOMINIUM_CHECKBOX = mo.ui.checkbox(label='CONDOMINIUM')
    CONDOMINIUM_COMMON_PROPERTY_CHECKBOX = mo.ui.checkbox(label='CONDOMINIUM COMMON PROPERTY')
    OWNED_BY_COLLEGE_CHECKBOX = mo.ui.checkbox(label='OWNED BY COLLEGE/UNIV/ACADEMY')
    ROWHOUSE_CHECKBOX = mo.ui.checkbox(label='ROWHOUSE')
    MOBILE_HOME_CHECKBOX = mo.ui.checkbox(label='MOBILE HOME')
    usedesc_value_checkbox_7 = mo.ui.checkbox(label='VACANT LAND')
    usedesc_value_checkbox_8 = mo.ui.checkbox(label='VACANT COMMERCIAL LAND')
    usedesc_value_checkbox_9 = mo.ui.checkbox(label='RIGHT OF WAY - RESIDENTIAL')
    usedesc_value_checkbox_10 = mo.ui.checkbox(label='OTHER COMMERCIAL')
    usedesc_value_checkbox_11 = mo.ui.checkbox(label='APART: 5-19 UNITS')
    MOBILE_HOME_IN_PARK_CHECKBOX = mo.ui.checkbox(label='MOBILE HOME (IN PARK)')
    usedesc_value_checkbox_13 = mo.ui.checkbox(label='THREE FAMILY')
    usedesc_value_checkbox_14 = mo.ui.checkbox(label='RETENTION POND - RESIDENTIAL')
    usedesc_value_checkbox_15 = mo.ui.checkbox(label='BUILDERS LOT')
    usedesc_value_checkbox_16 = mo.ui.checkbox(label='RESIDENTIAL VACANT LAND')
    TOWNHOUSE_CHECKBOX = mo.ui.checkbox(label='TOWNHOUSE')
    SINGLE_FAMILY_CHECKBOX = mo.ui.checkbox(label='SINGLE FAMILY')
    usedesc_value_checkbox_19 = mo.ui.checkbox(label='COMMON AREA OR GREENBELT')
    usedesc_value_checkbox_20 = mo.ui.checkbox(label='H.O.A RECREATIONS AREA')
    usedesc_value_checkbox_21 = mo.ui.checkbox(label='OTHER RESIDENTIAL STRUCTURE')
    usedesc_value_checkbox_22 = mo.ui.checkbox(label='RES AUX BUILDING (NO HOUSE)')
    usedesc_value_checkbox_23 = mo.ui.checkbox(label='COMM AUX BUILDING')
    usedesc_value_checkbox_24 = mo.ui.checkbox(label='COMMON AREA')
    usedesc_value_checkbox_25 = mo.ui.checkbox(label='CONDO GARAGE UNITS')
    usedesc_value_checkbox_26 = mo.ui.checkbox(label='CONDO DEVELOPMENTAL LAND')
    usedesc_value_checkbox_27 = mo.ui.checkbox(label='FORESTRY W/BUILDINGS')
    usedesc_value_checkbox_28 = mo.ui.checkbox(label='UNLOCATED PARCEL')
    usedesc_value_checkbox_29 = mo.ui.checkbox(label='CONDEMNED/BOARDED-UP')
    usedesc_value_checkbox_30 = mo.ui.checkbox(label='COAL RIGHTS, WORKING INTERESTS')
    usedesc_value_checkbox_31 = mo.ui.checkbox(label='TWO FAMILY')

    usedesc_value_checkbox_form = mo.md(
        "{FOUR_FAMILY_CHECKBOX}<br>{CONDOMINIUM_CHECKBOX}<br>{CONDOMINIUM_COMMON_PROPERTY_CHECKBOX}<br>{OWNED_BY_COLLEGE_CHECKBOX}<br>{ROWHOUSE_CHECKBOX}<br>{MOBILE_HOME_CHECKBOX}<br>{usedesc_value_checkbox_7}<br>{usedesc_value_checkbox_8}<br>{usedesc_value_checkbox_9}<br>{usedesc_value_checkbox_10}<br>{usedesc_value_checkbox_11}<br>{MOBILE_HOME_IN_PARK_CHECKBOX}<br>{usedesc_value_checkbox_13}<br>{usedesc_value_checkbox_14}<br>{usedesc_value_checkbox_15}<br>{usedesc_value_checkbox_16}<br>{TOWNHOUSE_CHECKBOX}<br>{SINGLE_FAMILY_CHECKBOX}<br>{usedesc_value_checkbox_19}<br>{usedesc_value_checkbox_20}<br>{usedesc_value_checkbox_21}<br>{usedesc_value_checkbox_22}<br>{usedesc_value_checkbox_23}<br>{usedesc_value_checkbox_24}<br>{usedesc_value_checkbox_25}<br>{usedesc_value_checkbox_26}<br>{usedesc_value_checkbox_27}<br>{usedesc_value_checkbox_28}<br>{usedesc_value_checkbox_29}<br>{usedesc_value_checkbox_30}<br>{usedesc_value_checkbox_31}<br>").batch(
        FOUR_FAMILY_CHECKBOX=FOUR_FAMILY_CHECKBOX, CONDOMINIUM_CHECKBOX=CONDOMINIUM_CHECKBOX,
        CONDOMINIUM_COMMON_PROPERTY_CHECKBOX=CONDOMINIUM_COMMON_PROPERTY_CHECKBOX,
        OWNED_BY_COLLEGE_CHECKBOX=OWNED_BY_COLLEGE_CHECKBOX, ROWHOUSE_CHECKBOX=ROWHOUSE_CHECKBOX,
        MOBILE_HOME_CHECKBOX=MOBILE_HOME_CHECKBOX, usedesc_value_checkbox_7=usedesc_value_checkbox_7,
        usedesc_value_checkbox_8=usedesc_value_checkbox_8, usedesc_value_checkbox_9=usedesc_value_checkbox_9,
        usedesc_value_checkbox_10=usedesc_value_checkbox_10, usedesc_value_checkbox_11=usedesc_value_checkbox_11,
        MOBILE_HOME_IN_PARK_CHECKBOX=MOBILE_HOME_IN_PARK_CHECKBOX, usedesc_value_checkbox_13=usedesc_value_checkbox_13,
        usedesc_value_checkbox_14=usedesc_value_checkbox_14, usedesc_value_checkbox_15=usedesc_value_checkbox_15,
        usedesc_value_checkbox_16=usedesc_value_checkbox_16, TOWNHOUSE_CHECKBOX=TOWNHOUSE_CHECKBOX,
        SINGLE_FAMILY_CHECKBOX=SINGLE_FAMILY_CHECKBOX, usedesc_value_checkbox_19=usedesc_value_checkbox_19,
        usedesc_value_checkbox_20=usedesc_value_checkbox_20, usedesc_value_checkbox_21=usedesc_value_checkbox_21,
        usedesc_value_checkbox_22=usedesc_value_checkbox_22, usedesc_value_checkbox_23=usedesc_value_checkbox_23,
        usedesc_value_checkbox_24=usedesc_value_checkbox_24, usedesc_value_checkbox_25=usedesc_value_checkbox_25,
        usedesc_value_checkbox_26=usedesc_value_checkbox_26, usedesc_value_checkbox_27=usedesc_value_checkbox_27,
        usedesc_value_checkbox_28=usedesc_value_checkbox_28, usedesc_value_checkbox_29=usedesc_value_checkbox_29,
        usedesc_value_checkbox_30=usedesc_value_checkbox_30, usedesc_value_checkbox_31=usedesc_value_checkbox_31).form(
        on_change=set_residential_path_usedesc_checkbox, clear_on_submit=True)

    good_usedesc_guesses = {"SINGLE_FAMILY_CHECKBOX": "SINGLE FAMILY", "TOWNHOUSE_CHECKBOX": "TOWNHOUSE",
                            "MOBILE_HOME_IN_PARK_CHECKBOX": "MOBILE HOME (IN PARK)",
                            "MOBILE_HOME_CHECKBOX": "MOBILE HOME", "ROWHOUSE_CHECKBOX": "ROWHOUSE",
                            "CONDOMINIUM_CHECKBOX": "CONDOMINIUM"}
    return (
        assessments_columns_radio_buttons,
        good_usedesc_guesses,
        usedesc_value_checkbox_form,
    )


@app.cell
def _(good_usedesc_guesses, usedesc_value_checkbox_form):
    def lists_of_usedesc_checkbox_answers():
        if usedesc_value_checkbox_form.value:
            true_usedesc_checkbox_keys = [k for k, v in usedesc_value_checkbox_form.value.items() if v == True]
            good_answers = [good_usedesc_guesses[item] for item in true_usedesc_checkbox_keys if
                            item in good_usedesc_guesses]
            missed_answers = [good_usedesc_guesses[item] for item in good_usedesc_guesses if
                              good_usedesc_guesses[item] not in good_answers]
            return good_answers, missed_answers
    return (lists_of_usedesc_checkbox_answers,)


@app.cell
def residential_path_radio_buttons(
    mo,
    set_residential_path_four_classdesc_b,
    set_residential_path_four_classdesc_d,
):
    options_dict = {
        "A full dataframe where every row has the CLASSDESC value of `RESIDENTIAL`": "full",
        "Only the CLASSDESC column, and every value is 'RESIDENTIAL'": "column",
        "A list of True and False values equal to the number of rows in the dataframe": "true_false"
    }

    classdesc_filter_radio_buttons = mo.ui.radio(options=options_dict).form(label="What will the output look like?",
                                                                            on_change=set_residential_path_four_classdesc_b)

    classdesc_filter_radio_buttons_two = mo.ui.radio(options=options_dict).form(
        label="NOW what will the output look like?", on_change=set_residential_path_four_classdesc_d)
    return classdesc_filter_radio_buttons, classdesc_filter_radio_buttons_two


@app.cell
def residential_path_getters_setters(mo, strip_string):
    filter_on_classdesc = "assessments_df[assessments_df['CLASSDESC']=='RESIDENTIAL']"
    residential_classdesc_and_usedesc_code_snippet = "assessments_df[assessments_df['CLASSDESC']=='RESIDENTIAL' & assessments_df['USEDESC']=='SINGLE FAMILY']"

    get_column_text_box_false_count, set_column_text_box_false_count = mo.state(0)
    get_column_text_box_success, set_column_text_box_success = mo.state(False)
    get_column_text_box_non_column, set_column_text_box_non_column = mo.state(False)
    get_column_boolean_explanation_box, set_column_boolean_explanation_box = mo.state(False)
    get_residential_post_chat_move_on, set_residential_post_chat_move_on = mo.state(False)

    get_residential_path_zero, set_residential_path_zero = mo.state(False)
    get_residential_path_one, set_residential_path_one = mo.state(False)
    get_residential_path_two, set_residential_path_two = mo.state(False)
    get_residential_path_three, set_residential_path_three = mo.state(False)

    get_residential_path_four_classdesc_a, set_residential_path_four_classdesc_a = mo.state(False)
    get_residential_path_four_classdesc_b, set_residential_path_four_classdesc_b = mo.state(False)
    get_residential_path_four_classdesc_c, set_residential_path_four_classdesc_c = mo.state(False)
    get_residential_path_four_classdesc_d, set_residential_path_four_classdesc_d = mo.state(False)
    get_residential_path_usedesc_checkbox, set_residential_path_usedesc_checkbox = mo.state(False)

    get_residential_path_four_usedesc_a, set_residential_path_four_usedesc_a = mo.state(False)
    get_residential_path_four_usedesc_b, set_residential_path_four_usedesc_b = mo.state(False)

    get_residential_path_five, set_residential_path_five = mo.state(False)

    get_residential_filter_incorrect_count, set_residential_filter_incorrect_count = mo.state(0)
    get_residential_filter_state, set_residential_filter_state = mo.state(False)

    def handle_residential_filter(value):
        set_residential_filter_state(True)
        if strip_string(value) != strip_string(residential_classdesc_and_usedesc_code_snippet):
            set_residential_filter_incorrect_count(lambda x: x + 1)

    def handle_column_radio_buttons(value):
        set_residential_path_three(True)
        if value not in ['CLASSDESC', 'USEDESC']:
            set_column_text_box_false_count(lambda x: x + 1)
            return value
        return value

    def reset_classdesc_path_setters():
        set_residential_path_four_classdesc_a(False)
        set_residential_path_four_classdesc_b(False)

    def reset_usedesc_path_setters():
        set_residential_path_four_usedesc_a(False)
    return (
        get_column_text_box_false_count,
        get_residential_filter_incorrect_count,
        get_residential_filter_state,
        get_residential_path_five,
        get_residential_path_four_classdesc_a,
        get_residential_path_four_classdesc_b,
        get_residential_path_four_classdesc_c,
        get_residential_path_four_classdesc_d,
        get_residential_path_four_usedesc_a,
        get_residential_path_four_usedesc_b,
        get_residential_path_one,
        get_residential_path_three,
        get_residential_path_two,
        get_residential_path_zero,
        get_residential_post_chat_move_on,
        handle_column_radio_buttons,
        handle_residential_filter,
        residential_classdesc_and_usedesc_code_snippet,
        set_column_boolean_explanation_box,
        set_residential_filter_state,
        set_residential_path_five,
        set_residential_path_four_classdesc_a,
        set_residential_path_four_classdesc_b,
        set_residential_path_four_classdesc_c,
        set_residential_path_four_classdesc_d,
        set_residential_path_four_usedesc_a,
        set_residential_path_four_usedesc_b,
        set_residential_path_one,
        set_residential_path_two,
        set_residential_path_usedesc_checkbox,
        set_residential_path_zero,
        set_residential_post_chat_move_on,
    )


@app.cell(hide_code=True)
def residential_path_cell_0(
    begin_residential_path,
    mo,
    residential_start_button,
):
    mo.stop(not begin_residential_path)
    if begin_residential_path:
        mo.output.replace(
            mo.vstack(
                [
                    mo.md(f"""##Ready to begin looking for residential parcels?""").center(),
                    mo.md(f"""Click the button below...""").center(),
                    residential_start_button.center()
                ]
            )
        )
    else:
        mo.output.clear()
    return


@app.cell(hide_code=True)
def residential_path_files_to_load(
    assessments_df,
    get_residential_path_zero,
    mo,
    set_residential_path_one,
):
    mo.stop(not get_residential_path_zero())
    if get_residential_path_zero():
        assessments_df_classdesc_slice = assessments_df[assessments_df['CLASSDESC'] == 'RESIDENTIAL']
        set_residential_path_one(True)
    return


@app.cell(hide_code=True)
def residential_path_cell_1(
    assessments_df,
    get_residential_path_one,
    mo,
    set_residential_path_two,
):
    mo.stop(not get_residential_path_one())

    if get_residential_path_one():
        mo.output.replace(
            mo.vstack(
                [
                    mo.md(f"""###Finding Residential Parcels"""),
                    mo.md(f"""Another important factor in finding suitable parcels for consideration is to find residential parcels. Local governments categorize parcels into different categories: residential (e.g. homes), commercial (e.g. stores), industrial (e.g. steel furnaces), and more.<br>

        This seems like the sort of information that would be contained in the `assessments` file: remember, that file contains descriptive elements about the parcels in the county.<br> 

        Let's take a quick look at the `assessments_df` dataframe again."""),
                    mo.md(f"""###assessments_df"""),
                    assessments_df,
                ]
            )
        )
        set_residential_path_two(True)
    else:
        mo.output.clear()
    return


@app.cell(hide_code=True)
def residential_path_cell_two(
    assessments_columns_radio_buttons,
    get_residential_path_two,
    mo,
):
    mo.stop(not get_residential_path_two())

    if get_residential_path_two():
        mo.output.replace(
            mo.vstack(
                [
                    mo.md(f"""At least one of these columns likely contains information about whether or not a property is a single-family residence or not. But which one?<br><br>
                Here is a list of the 86 columns contained in the dataframe. Select which one you think has the information we're looking for to get a few more details."""),
                    assessments_columns_radio_buttons.style({"columns": "3"})
                ]
            )
        )
    else:
        mo.output.clear()
    return


@app.cell
def residential_path_cell_three(
    assessments_columns_radio_buttons,
    assessments_df,
    get_column_text_box_false_count,
    get_residential_path_three,
    mo,
    set_residential_path_four_classdesc_a,
):
    mo.stop(not get_residential_path_three())

    usedesc_ten = ["CONDOMINIUM", "OFFICE-ELEVATOR -3 + STORIES", "COUNTY GOVERNMENT", "BANK", "CONDOMINIUM UNIT",
                   "ROWHOUSE", "STATE GOVERNMENT", "PARKING GARAGE/LOTS", "APART:40+ UNITS", "OFFICE/APARTMENTS OVER"]

    residential_moving_on_text = f"""<br><br>Let's take a look at the column CLASSDESC. If you scroll back up to the dataframe, and scroll to the right, you'll get to CLASSDESC about halfway along the scrollbar's length. Notice that the column CLASSDESC has several `COMMERCIAL` values in the first few rows; commercial was one of the classification types briefly mentioned during the introduction, so that column may hold the key. Let's isolate that column and look at the unique values."""

    classdesc_choice_text = f"""<br><br>Look closely at that output: one of those values is 'RESIDENTIAL'!<br><br> Let's see what happens when we filter the dataset so it only contains rows where the value in the CLASSDESC column is 'RESIDENTIAL'.<br><br>"""

    usedesc_choice_text = f"""<br><br> Those are different types of buildings. And notice that two of the list items are `CONDOMINIUM` and `ROWHOUSE`: those are two types of homes! This could be the column that we're looking for.<br><br>
    170 is a lot of different values to sift through to find what we're looking for. Maybe there's a way we can filter this down further..."""

    incorrect_choice_response_text_a = f"""<br><br>It doesn't look like those values tell us anything definitive about whether or not the property would be a single-family home."""

    incorrect_choice_response_text_b = f""" See if there's another column that looks promising. Enter the column's name into the text box and press 'Submit'."""

    if get_residential_path_three():
        if assessments_columns_radio_buttons.value:
            column_selection_output_text = f""""""
            residential_colname = assessments_columns_radio_buttons.value
            values = [str(item) for item in set(assessments_df[residential_colname])]
            if assessments_columns_radio_buttons.value == 'USEDESC':
                ten_values = "<br>".join(usedesc_ten)
            else:
                ten_values = "<br>".join(list(values)[:10])
            intro_text = f"""The {residential_colname} column has {len(values)} separate values in it."""
            column_selection_output_text += intro_text
            if len(values) > 10:
                ten_values_text = f""" Here are the first 10 of them.<br><br>{ten_values}"""
            else:
                ten_values_text = f':<br><br>{ten_values}'
            if residential_colname not in ['CLASSDESC', 'USEDESC']:
                column_selection_output_text = intro_text + ten_values_text + incorrect_choice_response_text_a
                if get_column_text_box_false_count() < 3:
                    column_selection_output_text += incorrect_choice_response_text_b
                elif get_column_text_box_false_count() >= 3:
                    column_selection_output_text += residential_moving_on_text
                    set_residential_path_four_classdesc_a(True)
            else:
                if residential_colname == 'CLASSDESC':
                    column_selection_output_text = intro_text + ten_values_text + classdesc_choice_text
                if residential_colname == 'USEDESC':
                    column_selection_output_text = intro_text + ten_values_text + usedesc_choice_text + residential_moving_on_text
                set_residential_path_four_classdesc_a(True)
        mo.output.replace(
            mo.md(column_selection_output_text)
        )
    else:
        mo.output.clear()
    return


@app.cell
def _(
    classdesc_filter_radio_buttons,
    get_residential_path_four_classdesc_a,
    mo,
    set_residential_path_four_classdesc_b,
):
    mo.stop(not get_residential_path_four_classdesc_a())

    if get_residential_path_four_classdesc_a():
        mo.output.replace(
            mo.vstack(
                [
                    mo.md(f"""Since we know we're only looking for residential, single-family properties, we can see what happens when we filter the dataframe to show only residential properties. We found that the column `CLASSDESC` separates rows into `RESIDENTIAL`, `COMMERCIAL`, and other types of structures, so why don't we take a look at how the dataframe looks if it only has rows where the value for the column `CLASSDESC` is `RESIDENTIAL`.<br><br>
                    Thankfully, pandas makes this easy. There is a command you can enter to return a dataframe that's filtered on a column's value or values. The format for that command is as follows: <br><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**filtered_dataframe = dataframe_name [ dataframe_name['COLUMN_NAME']=='VALUE'&nbsp;&nbsp;]**
                    <br><br>That's lot of text! Let's break that down for a second. We'll start with the last section of that line of code. <br><br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**dataframe_name['COLUMN_NAME']=='VALUE'**<br><br>
                    If you were to run just that piece of code on `assessments_df` and the `CLASSDESC` column, what do you think the output would look like?"""
                          ),
                    classdesc_filter_radio_buttons,
                ]
            )
        )
        if classdesc_filter_radio_buttons.value:
            set_residential_path_four_classdesc_b(True)
    else:
        mo.output.clear()
    return


@app.cell
def residential_path_four_classdesc_b(
    assessments_df,
    classdesc_filter_radio_buttons,
    column_boolean_explanation_box,
    get_residential_path_four_classdesc_b,
    mo,
    set_residential_path_four_classdesc_c,
):
    mo.stop(not get_residential_path_four_classdesc_b())

    if classdesc_filter_radio_buttons.value == 'true_false':
        classdesc_b_answer_response = f"""That's right!"""
    else:
        classdesc_b_answer_response = f"""Unfortunately, that's not quite right."""
    classdesc_b_intro_text = classdesc_b_answer_response + f"""  Here's what happens when we run just **assessments_df['CLASSDESC']=='VALUE'**:"""
    if get_residential_path_four_classdesc_b():
        mo.output.replace(
            mo.vstack(
                [
                    mo.md(classdesc_b_intro_text),
                    assessments_df['CLASSDESC'] == 'VALUE',
                    mo.md(
                        f"""<br>Why do you think the output looks like that? Enter your thoughts in the text box below."""),
                    column_boolean_explanation_box,
                ]
            )
        )
        if column_boolean_explanation_box.value:
            set_residential_path_four_classdesc_c(True)
    else:
        mo.output.clear()
    return


@app.cell(hide_code=True)
def _(
    classdesc_filter_radio_buttons_two,
    get_residential_path_four_classdesc_c,
    mo,
):
    mo.stop(not get_residential_path_four_classdesc_c())

    if get_residential_path_four_classdesc_c():
        mo.output.replace(
            mo.vstack(
                [
                    mo.md(f"""The output is true and false because the line of code we used created a boolean index. It evaluated each row of the dataframe and asked itself, "Is the value for the column 'CLASSDESC' in this row 'RESIDENTIAL'?" If so, it returned true; if not, it returned false.<br><br>
                    Let's now take a look at the next part of that equation:<br><br> 
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**dataframe_name [ dataframe_name['COLUMN_NAME']=='VALUE'&nbsp;&nbsp;]**
                    <br><br>If we were to run this portion of code on the `assessments_df` dataframe, what do you think the output would look like now? Select the option below and hit "Submit".           
                    """),
                    classdesc_filter_radio_buttons_two
                ]
            )
        )
    else:
        mo.output.clear()
    return


@app.cell(hide_code=True)
def _(
    assessments_df,
    classdesc_filter_radio_buttons_two,
    get_residential_path_four_classdesc_d,
    mo,
    set_residential_path_four_usedesc_a,
):
    mo.stop(not get_residential_path_four_classdesc_d())

    correct_response = f"""That's right! T"""
    incorrect_response = f"""Actually, this time, t"""
    remainder_of_text = f"""he function returned a dataframe that contains all of the data, so long as the value in the boolean index from the last step was true (or, in other words, as long as the value of "CLASSDESC" is "RESIDENTIAL")."""

    if get_residential_path_four_classdesc_d():
        if classdesc_filter_radio_buttons_two.value == 'full':
            first_output_text = correct_response + remainder_of_text
        else:
            first_output_text = incorrect_response + remainder_of_text
        mo.output.replace(
            mo.vstack(
                [
                    mo.md(first_output_text),
                    assessments_df[assessments_df['CLASSDESC'] == 'RESIDENTIAL'],
                    mo.md(
                        f"""If you again scroll over to the CLASSDESC column on the above output dataframe, you'll see that all of the values appear to be "RESIDENTIAL". This seems to be what we were looking for! And if you look two more columns over to the right, you'll see that the first few values in the column "USEDESC" are "SINGLE FAMILY"!""")
                ]
            )
        )
        set_residential_path_four_usedesc_a(True)
    else:
        mo.output.clear()
    return


@app.cell(hide_code=True)
def _(
    assessments_columns_radio_buttons,
    get_residential_path_four_usedesc_a,
    mo,
    set_residential_path_four_usedesc_b,
    usedesc_value_checkbox_form,
):
    mo.stop(not get_residential_path_four_usedesc_a())

    if assessments_columns_radio_buttons.value == 'USEDESC':
        usedesc_bonus_text = f"""That's much more manageable than the 170 we found earlier!  """
    else:
        usedesc_bonus_text = f""""""

    if get_residential_path_four_usedesc_a():
        usedesc_introduction_text = f"""Now let's take a look at the unique values in the USEDESC column when "CLASSDESC" is "RESIDENTIAL". It looks like there are 32 different values.  {usedesc_bonus_text}<br><br>
        Select the values you think represent single family homes, and click "Submit"."""
        mo.output.replace(
            mo.vstack(
                [
                    mo.md(usedesc_introduction_text),
                    usedesc_value_checkbox_form,
                ]
            )
        )
        if usedesc_value_checkbox_form.value:
            set_residential_path_four_usedesc_b(True)
    else:
        mo.output.clear()
    return


@app.cell
def _(
    generate_usedesc_incorrect_singular_or_plural_text,
    get_residential_path_four_usedesc_b,
    lists_of_usedesc_checkbox_answers,
    mo,
    set_residential_path_five,
    usedesc_value_checkbox_form,
):
    mo.stop(not get_residential_path_four_usedesc_b())

    if get_residential_path_four_usedesc_b():
        if usedesc_value_checkbox_form.value:
            good_answers, missing_answers = lists_of_usedesc_checkbox_answers()
            if len(good_answers) > 0:
                good_answers_output_text = f"""Nice work! Values like `{good_answers[0]}` make sense as single-family residences.<br><br>"""
            else:
                singular_or_plural_text = generate_usedesc_incorrect_singular_or_plural_text(usedesc_value_checkbox_form.value)
                good_answers_output_text = f"""Hm...I'm not sure if {singular_or_plural_text} sense as descriptions of single-family residences.  """
            if len(missing_answers) > 0:
                missing_answers_output_text = f"""What about `{missing_answers[0]}`, though? Could that be considered a single-family residence?  """
            else:
                missing_answers_output_text = f""""""
            rest_of_text = f"""Could there be others that we've missed? Is there a way to tell what TriCOG's director wants when she asks for 'single-family' houses simply by looking at the dataframe?<br><br>
            Unfortunately not. Because TriCOG didn't create this dataframe, the definition they use for certain items might differ from the definition the county used when creating the dataframe, even if they're using the same words. Because there is a lot of uncertainty and no way to resolve it by looking at the dataframe, it might be best to ask a `clarifying question`.<br>

                    We've set up a connection for you to your supervisor at TriCOG using their internal chat client. Ask your supervisor `which filters should be used to find suitable residential properties`? (You can also type "/" to have the question filled in as a prompt.)"""
            usedesc_b_output_text = good_answers_output_text + missing_answers_output_text + rest_of_text
        mo.output.replace(
            mo.vstack(
                [
                    mo.md(usedesc_b_output_text)
                ]
            )
        )
        set_residential_path_five(True)
    else:
        mo.output.clear()
    return


@app.cell
def _(
    get_residential_path_five,
    mo,
    response_message,
    set_residential_post_chat_move_on,
):
    mo.stop(not get_residential_path_five())

    prompts = ["Which filters should be used to find residential properties?"]
    responses = []

    def residential_parcel_chat_session(messages):
        if len(responses) == 0 and (messages[-1].content.lower() == 'hi' or 'hello' in messages[-1].content.lower()):
            responses.append("Hi! What's up?")
            return responses[-1]
        for appreciation in ['thanks', 'thank you']:
            if appreciation in messages[-1].content.lower():
                responses.append("You're welcome!")
                return responses[-1]
        if response_message in responses:
            set_residential_post_chat_move_on(True)
            responses.append(
                "I'm sorry, I'm a bit busy. Did that answer your question? Look for rows where CLASSDESC=='RESIDENTIAL' and USEDESC=='SINGLE FAMILY'")
            return responses[-1]
        if response_message not in responses:
            responses.append(response_message)
            set_residential_post_chat_move_on(True)
        return response_message

    chat = mo.ui.chat(residential_parcel_chat_session, prompts=prompts)

    if get_residential_path_five():
        mo.output.replace(chat)
    else:
        mo.output.clear()
    return


@app.cell(hide_code=True)
def _(
    assessments_df,
    get_residential_filter_incorrect_count,
    get_residential_post_chat_move_on,
    incorrect_answer_text_generator,
    mo,
    residential_classdesc_and_usedesc_code_snippet,
    residential_text_box_final_classdesc_usedesc_filter,
    set_residential_filter_state,
    strip_string,
):
    mo.stop(not get_residential_post_chat_move_on())
    residential_parcels = None

    if get_residential_post_chat_move_on():
        mo.output.replace(
            mo.vstack(
                [
                    mo.md(f"""Great! Now that we know for certain which values to use, let's find the residential parcels with single family homes.<br><br>
                    Remember the filtering command that we used earlier? **filtered_dataframe = dataframe_name [ dataframe_name['COLUMN_NAME']=='VALUE'  ]**
                    <br><br>When we saw it earlier, we used it with one filtering condition **assessments_df['CLASSDESC']=='RESIDENTIAL'**. But the director gave us two conditionals. Can we use both conditionals at once? <br><br>
                    Go ahead and try it! Use the above equation, but chain the two conditionals together in between the brackets using an ampersand ('&'). We'll set the equation equal to the variable `residential_parcels`."""),
                    mo.hstack(
                        [mo.md(f"""**residential_parcels=**"""), residential_text_box_final_classdesc_usedesc_filter],
                        gap=0, justify="space-around", align='center', widths=[1, 7])
                ]
            )
        )
        if residential_text_box_final_classdesc_usedesc_filter.value:
            stripped_residential_final_response = strip_string(residential_classdesc_and_usedesc_code_snippet)
            if strip_string(
                    residential_text_box_final_classdesc_usedesc_filter.value) == stripped_residential_final_response:
                residential_parcels = assessments_df[
                    (assessments_df['CLASSDESC'] == 'RESIDENTIAL') & (assessments_df['USEDESC'] == 'SINGLE FAMILY')]
                mo.output.replace_at_index(f"""Correct!""", 1)
                set_residential_filter_state(True)
            else:
                set_residential_filter_state(False)
                residential_filtering_response = incorrect_answer_text_generator(
                    residential_text_box_final_classdesc_usedesc_filter.value,
                    residential_classdesc_and_usedesc_code_snippet, get_residential_filter_incorrect_count())
                mo.output.replace_at_index(f"""{residential_filtering_response[0]}""", 1)

        #         We can combine both of these conditions into one statement to be more straightforward.<br><br>

        #             Type the following code into the text box.<br>
        #             `{residential_classdesc_and_usedesc_code_snippet}`"""),
        #             residential_text_box_final_classdesc_usedesc_filter
        #         ]
        #     )
        # )
        #     if residential_text_box_final_classdesc_usedesc_filter.value:
        #         if residential_text_box_final_classdesc_usedesc_filter.value == residential_classdesc_and_usedesc_code_snippet:
        #             residential_parcels = assessments_df[(assessments_df['CLASSDESC']=='RESIDENTIAL') & (assessments_df['USEDESC']=='SINGLE FAMILY')]
        #             mo.output.replace_at_index("Correct!", 1)
        #             residential_path_five = True
        #         else:
        #             mo.output.append("Sorry, please try again")
    else:
        mo.output.clear()
    return (residential_parcels,)


@app.cell
def residential_path_end(
    get_attempted_text_first,
    get_residential_filter_state,
    mo,
    residential_parcels,
    set_abandoned_path_0,
):
    mo.stop(not get_residential_filter_state())
    abandoned_path_zero = False

    if get_residential_filter_state():
        residential_path_end_text = f"""You did it! Now we have `residential_parcels`, a dataframe that contains all of the residential, single-family properties in the county."""
        if get_attempted_text_first():
            additional_text = f"""If you wanted to perform an additional check on your own, you could think about the functions we used previously while performing the text analysis of dataframes to look for parcels in TriCOG's boundaries. The text analysis was not successful, but it did teach us that we can access dataframe columns' values using the `dataframe.COLUMN` construction, and that we can use the `set()` function to see only unique values."""
        else:
            additional_text = f"""If you wanted to perform an additional check on your own, you could examine the values in the CLASSDESC and USEDESC columns by generating a set of the columns' values. The resulting set for each column would only have one item in it."""
        residential_path_end_text = residential_path_end_text + f"""<br><br>""" + additional_text
        mo.output.replace(
            mo.vstack(
                [
                    mo.md(f"""###residential_parcels"""),
                    residential_parcels,
                    mo.md(residential_path_end_text),
                ]
            )
        )
        set_abandoned_path_0(True)
    else:
        mo.output.clear()
    return


@app.cell
def abandoned_getters_setters(mo):
    get_abandoned_path_0, set_abandoned_path_0 = mo.state(False)
    get_abandoned_path_1, set_abandoned_path_1 = mo.state(False)
    get_abandoned_path_2, set_abandoned_path_2 = mo.state(False)
    get_abandoned_path_3, set_abandoned_path_3 = mo.state(False)

    get_abandoned_path_iteration_0, set_abandoned_path_iteration_0 = mo.state(False)
    get_abandoned_path_iteration_1, set_abandoned_path_iteration_1 = mo.state(False)
    get_abandoned_path_iteration_2, set_abandoned_path_iteration_2 = mo.state(False)
    get_abandoned_path_iteration_3, set_abandoned_path_iteration_3 = mo.state(False)
    get_abandoned_path_iteration_4, set_abandoned_path_iteration_4 = mo.state(False)
    get_abandoned_path_iteration_5, set_abandoned_path_iteration_5 = mo.state(False)
    get_abandoned_path_iteration_6, set_abandoned_path_iteration_6 = mo.state(False)
    get_abandoned_path_iteration_7, set_abandoned_path_iteration_7 = mo.state(False)
    get_abandoned_path_iteration_parcels_counter, set_abandoned_path_iteration_parcels_counter = mo.state(0)
    get_abandoned_path_iteration_lien_column_counter, set_abandoned_path_iteration_lien_column_counter = mo.state(0)

    get_abandoned_path_join_0, set_abandoned_path_join_0 = mo.state(False)
    get_abandoned_path_join_1, set_abandoned_path_join_1 = mo.state(False)
    get_abandoned_path_join_2, set_abandoned_path_join_2 = mo.state(False)
    get_abandoned_path_join_3, set_abandoned_path_join_3 = mo.state(False)
    get_abandoned_path_join_4, set_abandoned_path_join_4 = mo.state(False)
    get_abandoned_path_iteration_first, set_abandoned_path_iteration_first = mo.state(False)
    get_abandoned_path_join_first, set_abandoned_path_join_first = mo.state(False)
    get_abandoned_path_successful_tricog_join, set_abandoned_path_successful_tricog_join = mo.state(False)

    get_abandoned_iteration_path_1, set_abandoned_iteration_path_1 = mo.state(False)
    get_abandoned_join_path_1, set_abandoned_join_path_1 = mo.state(False)

    get_abandoned_file_selection_state, set_abandoned_file_selection_state = mo.state(False)

    def handle_abandoned_drop_down_path_selection(value):
        if value["abandoned_drop_down_variable_selection"] == 'iteration':
            reset_abandoned_paths('iteration')
            set_abandoned_path_iteration_0(True)
            if not get_abandoned_path_join_first() and not get_abandoned_path_iteration_first():
                set_abandoned_path_iteration_first(True)
        if value["abandoned_drop_down_variable_selection"] == 'join':
            set_abandoned_path_join_0(True)
            reset_abandoned_paths('join')
            if not get_abandoned_path_iteration_first() and not get_abandoned_path_join_first():
                set_abandoned_path_join_first(True)

    def reset_abandoned_paths(pathname: str):
        if pathname == 'iteration':
            set_abandoned_path_join_0(False)
            set_abandoned_path_join_1(False)
            set_abandoned_path_join_2(False)
            set_abandoned_path_join_3(False)
            set_abandoned_path_join_4(False)
        elif pathname == 'join':
            set_abandoned_path_iteration_0(False)
            set_abandoned_path_iteration_1(False)
            set_abandoned_path_iteration_2(False)
            set_abandoned_path_iteration_3(False)
            set_abandoned_path_iteration_4(False)
            set_abandoned_path_iteration_5(False)
            set_abandoned_path_iteration_6(False)
            set_abandoned_path_iteration_7(False)
        else:
            pass

    def abandoned_path_check_join(join_response_dict: dict[str:str])-> None: 
        if join_response_dict['leftdrop'] != join_response_dict['rightdrop']: 
            if join_response_dict['left_on_cols_drop'].lower().startswith('pin') and join_response_dict['right_on_cols_drop'].lower().startswith('pin'): 
                if join_response_dict['join_type_drop'] == 'inner': 
                    set_abandoned_path_successful_tricog_join(True)
                    return None
        set_abandoned_path_successful_tricog_join(False)
        return None
    return (
        abandoned_path_check_join,
        get_abandoned_file_selection_state,
        get_abandoned_iteration_path_1,
        get_abandoned_join_path_1,
        get_abandoned_path_0,
        get_abandoned_path_1,
        get_abandoned_path_2,
        get_abandoned_path_3,
        get_abandoned_path_iteration_0,
        get_abandoned_path_iteration_1,
        get_abandoned_path_iteration_2,
        get_abandoned_path_iteration_3,
        get_abandoned_path_iteration_4,
        get_abandoned_path_iteration_5,
        get_abandoned_path_iteration_6,
        get_abandoned_path_iteration_lien_column_counter,
        get_abandoned_path_iteration_parcels_counter,
        get_abandoned_path_join_0,
        get_abandoned_path_join_1,
        get_abandoned_path_join_2,
        get_abandoned_path_join_3,
        get_abandoned_path_successful_tricog_join,
        handle_abandoned_drop_down_path_selection,
        reset_abandoned_paths,
        set_abandoned_file_selection_state,
        set_abandoned_iteration_path_1,
        set_abandoned_join_path_1,
        set_abandoned_path_0,
        set_abandoned_path_1,
        set_abandoned_path_2,
        set_abandoned_path_3,
        set_abandoned_path_iteration_1,
        set_abandoned_path_iteration_2,
        set_abandoned_path_iteration_3,
        set_abandoned_path_iteration_4,
        set_abandoned_path_iteration_5,
        set_abandoned_path_iteration_6,
        set_abandoned_path_iteration_lien_column_counter,
        set_abandoned_path_iteration_parcels_counter,
        set_abandoned_path_join_0,
        set_abandoned_path_join_1,
        set_abandoned_path_join_2,
        set_abandoned_path_join_3,
    )


@app.cell(hide_code=True)
def abandoned_text_box(mo, set_combining_files_0):
    abandoned_post_join_selector_reflection = mo.ui.text_area(
        label=f"""**What differences did you notice in different joins? Why?**""", full_width=True).form(
        clear_on_submit=True, on_change=set_combining_files_0)
    return (abandoned_post_join_selector_reflection,)


@app.cell(hide_code=True)
def abandoned_radio_buttons(mo, set_abandoned_file_selection_state):
    def handle_file_selection_radio(value):
        if value == 'parcels_df':
            set_abandoned_file_selection_state(True)
        else:
            set_abandoned_file_selection_state(False)

    abandoned_file_selection_radio = mo.ui.radio(options=['assessments_df', 'parcels_df', 'tricog_df'],
                                                 on_change=handle_file_selection_radio)
    return (abandoned_file_selection_radio,)


@app.cell(hide_code=True)
def abandoned_drop_down_form(
    handle_abandoned_drop_down_path_selection,
    mo,
    set_abandoned_path_iteration_6,
):
    abandoned_analysis_form = (mo.md("""**Select a process to begin using:**    {abandoned_drop_down_variable_selection}<br><br>
    **Explain why you chose that process:**{abandoned_drop_down_text_box}""").batch(
        abandoned_drop_down_variable_selection=mo.ui.dropdown(options=['iteration', 'join']),
        abandoned_drop_down_text_box=mo.ui.text_area())).form(on_change=handle_abandoned_drop_down_path_selection,
                                                              clear_on_submit=True)

    abandoned_end_of_iteration_form = (mo.md(
        """**Why did this seem to take so long?** {abandoned_iteration_time_text}<br> **Can you think of a way we could have made it go faster?** {abandoned_iteration_improvement_text}""").batch(
        abandoned_iteration_time_text=mo.ui.text_area(full_width=True),
        abandoned_iteration_improvement_text=mo.ui.text_area(full_width=True))).form(
        on_change=set_abandoned_path_iteration_6, clear_on_submit=True)
    return abandoned_analysis_form, abandoned_end_of_iteration_form


@app.cell
def abandoned_path_prep(
    filtered_parcels_df_liens_col_copy,
    get_abandoned_path_0,
    liens_df,
    mo,
    reset_abandoned_paths,
    set_abandoned_iteration_path_1,
    set_abandoned_join_path_1,
    set_abandoned_path_1,
    set_abandoned_path_iteration_2,
    set_abandoned_path_iteration_3,
    set_abandoned_path_iteration_4,
    set_abandoned_path_iteration_6,
    set_abandoned_path_iteration_lien_column_counter,
    set_abandoned_path_iteration_parcels_counter,
    set_abandoned_path_join_0,
    strip_string,
    time,
):
    mo.stop(not get_abandoned_path_0())

    def handle_parcels_with_liens(value):
        if strip_string(value) == strip_string(parcels_with_liens):
            set_abandoned_path_iteration_2(True)
        else:
            set_abandoned_path_iteration_parcels_counter(lambda x: x + 1)

    def handle_adding_liens_column(value):
        if strip_string(value) == strip_string(abandoned_iteration_generate_empty_lien_column_code_snippet):
            set_abandoned_path_iteration_3(True)
        else:
            set_abandoned_path_iteration_lien_column_counter(lambda x: x + 1)

    def handle_iteration_code_block(value):
        if strip_string(value) == strip_string(abandoned_iteration_iteration_code_block_no_spaces):
            set_abandoned_path_iteration_4(True)

    # abandoned section prep

    # buttons
    abandoned_begin_button = mo.ui.run_button(label="Click to Begin", on_change=set_abandoned_path_1)


    # code snippets
    parcels_with_liens = "parcels_df[parcels_df['PIN'].isin(liens_df['pin'])]"
    abandoned_pd_merge_code_snippet = "pd.merge(left=parcels_df, right=liens_df, left_on='PIN', right_on='pin', how='inner')"
    abandoned_iteration_generate_empty_lien_column_code_snippet = "filtered_parcels_df.assign(lien_amount='')"
    abandoned_iteration_iteration_code_block_no_spaces = "for idx, row in parcels_df_with_liens.iterrows(): amount = liens_df[liens_df['pin']==row.PIN].total_amount.values[0] parcels_df_with_liens.at[idx, 'lien_amount']= amount"
    abandoned_iteration_iteration_code_block_with_spaces = "for idx, row in parcels_df_with_liens.iterrows():`<br>            &nbsp;&nbsp;&nbsp;&nbsp;`amount = liens_df[liens_df['pin']==row.PIN].total_amount.values[0]`<br>            &nbsp;&nbsp;&nbsp;&nbsp;`parcels_df_with_liens.at[idx, 'lien_amount']= amount"

    # text boxes
    abandoned_iteration_text_box_parcels_with_liens = mo.ui.text(full_width=True).form(clear_on_submit=True,
                                                                                       on_change=handle_parcels_with_liens)
    abandoned_join_text_box = mo.ui.text(full_width=True).form(clear_on_submit=True)
    abandoned_iteration_text_box_adding_lien_column = mo.ui.text(full_width=True).form(clear_on_submit=True,
                                                                                       on_change=handle_adding_liens_column)
    abandoned_iteration_text_box_code_block = mo.ui.text_area(full_width=True).form(clear_on_submit=True,
                                                                                    on_change=handle_iteration_code_block)

    # other
    miscellany = {'iteration_move_along': False}

    def handle_abandoned_path_selection(value):
        if (value == "JOIN"):
            set_abandoned_path_iteration_6(False)
            set_abandoned_path_join_0(True)
            reset_abandoned_paths('join')
            return "JOIN"
        if (value == "ITERATION"):
            set_abandoned_iteration_path_1(True)
            set_abandoned_join_path_1(False)
            reset_abandoned_paths('iteration')
            return "ITERATION"

    abandoned_iteration_button = mo.ui.button(
        label="Iteration",
        value="ITERATION",
        on_click=handle_abandoned_path_selection
    )
    abandoned_join_button = mo.ui.button(
        label="Use Joins to Combine Dataframes",
        value="JOIN",
        on_click=handle_abandoned_path_selection
    )

    abandoned_join_button_with_link = mo.md(
        f"""<a href=#joins>""""""{abj}</a>"""
    ).batch(
        abj=abandoned_join_button
    )

    def fake_iteration():
        mo.output.append("Iteration has begun...")
        seconds_counter = 0
        next_out = 10
        start_time = time.time()
        for _idx, _row in filtered_parcels_df_liens_col_copy.iterrows():
            amount = liens_df[liens_df['pin'] == _row.PIN].total_amount.values[0]
            filtered_parcels_df_liens_col_copy.at[_idx, 'lien_amount'] = amount
            seconds_counter = time.time() - start_time
            if seconds_counter > next_out:
                mo.output.append(f'{seconds_counter:.0f} seconds have passed...')
                next_out += 10
            if seconds_counter > 40:
                break
    return (
        abandoned_begin_button,
        abandoned_iteration_generate_empty_lien_column_code_snippet,
        abandoned_iteration_iteration_code_block_no_spaces,
        abandoned_iteration_text_box_adding_lien_column,
        abandoned_iteration_text_box_code_block,
        abandoned_iteration_text_box_parcels_with_liens,
        abandoned_join_button_with_link,
        fake_iteration,
        parcels_with_liens,
    )


@app.cell(hide_code=True)
def abandoned_exp_builder(
    get_abandoned_path_0,
    liens_df,
    mo,
    parcels_df,
    parcels_df_df,
    set_abandoned_path_join_2,
):
    mo.stop(not get_abandoned_path_0())

    parcels_cols_list = [f"{item} (parcels_df)" for item in list(parcels_df.columns)]
    liens_cols_list = [f"{item} (liens_df)" for item in list(liens_df.columns)]

    function_builder_columns = parcels_cols_list + liens_cols_list

    join_expression_builder = (mo.md(
        """**Select the values to test how the merge works.**<br>pd.merge ( {leftdrop},&ensp;{rightdrop},&ensp; {left_on_cols_drop},&ensp; {right_on_cols_drop},&ensp;{join_type_drop})<br><br>**What do you expect the output to look like?** {join_expression_textbox}""").batch(
        leftdrop=mo.ui.dropdown(label="left =", options=['parcels_df', 'liens_df']),
        rightdrop=mo.ui.dropdown(label="right = ", options=['parcels_df', 'liens_df']),
        left_on_cols_drop=mo.ui.dropdown(label="left_on = ", options=function_builder_columns),
        right_on_cols_drop=mo.ui.dropdown(label="right_on = ", options=function_builder_columns),
        join_type_drop=mo.ui.dropdown(label="how =", options=['left', 'right', 'inner']),
        join_expression_textbox=mo.ui.text_area())).form(clear_on_submit=False, on_change=set_abandoned_path_join_2)

    join_expression_output_dict = {'parcels_df': parcels_df_df, 'liens_df': liens_df}
    return join_expression_builder, join_expression_output_dict


@app.cell
def abandoned_file_prep(
    copy,
    get_abandoned_path_0,
    liens_df,
    mo,
    parcels_df,
    parcels_df_df,
    pd,
):
    mo.stop(not get_abandoned_path_0())

    filtered_parcels_df = parcels_df_df[parcels_df_df["PIN"].isin(liens_df['pin'])]
    filtered_parcels_df_liens_col = filtered_parcels_df.assign(lien_amount='')
    filtered_parcels_df_liens_col_copy = copy.deepcopy(filtered_parcels_df_liens_col)
    parcels_df_with_joined_liens = pd.DataFrame(
        pd.merge(left=parcels_df, right=liens_df, left_on='PIN', right_on='pin', how='inner'))
    return (
        filtered_parcels_df,
        filtered_parcels_df_liens_col,
        filtered_parcels_df_liens_col_copy,
        parcels_df_with_joined_liens,
    )


@app.cell
def abandoned_path_0(abandoned_begin_button, get_abandoned_path_0, mo):
    mo.stop(not get_abandoned_path_0())

    if get_abandoned_path_0():
        mo.output.replace(
            mo.vstack(
                [
                    mo.md(f"""##Ready to look into finding abandoned properties?""").center(),
                    abandoned_begin_button.center()
                ]
            )
        )
    else:
        mo.output.clear()
    return


@app.cell
def abandoned_path_1(
    get_abandoned_iteration_path_1,
    get_abandoned_join_path_1,
    get_abandoned_path_1,
    mo,
    set_abandoned_path_2,
):
    mo.stop(not get_abandoned_path_1())
    abandoned_iteration_path_1 = get_abandoned_iteration_path_1()
    abandoned_join_path_1 = get_abandoned_join_path_1()

    if get_abandoned_path_1():
        mo.output.replace(
            mo.vstack(
                [
                    mo.md(f"""##Finding Abandoned Properties"""),
                    mo.md(f"""In this section, we're trying to find homes that have been abandoned. This can be difficult to do using data because there is no registry of abandoned homes in the county. We'll have to use a different dataset as a proxy for abandoned homes. 

        This is where tax delinquent property data comes in. Remember that tax delinquency is when an individual stops paying taxes. If a person has stopped paying taxes on their house, it's possible that they're having money problems. But it's also possible that it is a sign they have decided to abandon the property.

        This step again highlights one of the challenges of working with geospatial data: some datasets contain geospatial data, while other datasets will only contain text-based data about the same locations."""),
                ]
            )
        )
        set_abandoned_path_2(True)

        #

        #         mo.md(f"""In order to make use of this data, we'll have to connect the `pin` column to the `pin` column in our other files. There are a few ways we could do this. We could do this by **iterating** over the datasets and combining them when the field matches, or we could perform a **join.**

        #         Which would you like to try?"""),
        #             mo.hstack([abandoned_iteration_button, abandoned_join_button],justify='space-around')
        #         ]
        #     )
        # )
    else:
        mo.output.clear()
    return


@app.cell
def abandoned_path_2(get_abandoned_path_2, liens_df, mo, set_abandoned_path_3):
    mo.stop(not get_abandoned_path_2())

    if get_abandoned_path_2():
        mo.output.replace(
            mo.vstack(
                [
                    mo.md(f"""Let's take another look at the tax liens summary file."""),
                    mo.md(f"""###liens_df"""),
                    liens_df,
                    mo.md(f"""The dataset is fairly easy to interpret, thanks to the small number of columns. The dataset contains an ID row, the parcel ID Number ('pin'), the number of liens against the property ('number'), and the total amount owed in taxes ('total_amount'). 

                    This file gives us IDs for parcels with liens against them, but it doesn't tell us where they are. Which of our other files should we try to join this with?"""),
                ]
            )
        )
        set_abandoned_path_3(True)
    else:
        mo.output.clear()
    return


@app.cell
def abandoned_path_3(
    abandoned_file_selection_radio,
    get_abandoned_path_3,
    mo,
    set_abandoned_file_selection_state,
):
    mo.stop(not get_abandoned_path_3())

    abandoned_path_3_output_text = f""""""

    if abandoned_file_selection_radio.value == 'assessments_df':
        abandoned_path_3_output_text = f"""Sorry, no -- `assessments_df` doesn't have any geospatial data in the file. It does have a parcel ID column ("PARID") that can be matched to the `liens_df` "pin" column, so some data can be matched, but you won't be able to know where the parcels belong on a map after matching the two."""
    elif abandoned_file_selection_radio.value == 'tricog_df':
        abandoned_path_3_output_text = f"""Sorry, no -- `tricog_df` does have geospatial data, but it does not have any parcel data. There is no column that matches with the "pin" column from the `liens_df` dataframe, so we cannot match the two files directly."""
    elif abandoned_file_selection_radio.value == 'parcels_df':
        abandoned_path_3_output_text = f"""Yes! `parcels_df` has both a parcel ID column ("PIN") and geospatial data ("geometry"). We will be able to match the rows from `liens_df` to rows from `parcels_df` and then know where they fall on a map."""
    if get_abandoned_path_3():
        mo.output.replace(
            mo.vstack(
                [
                    abandoned_file_selection_radio,
                    mo.md(f"""<br>{abandoned_path_3_output_text}""")
                ]
            )
        )
        if abandoned_file_selection_radio.value:
            if abandoned_file_selection_radio.value == 'parcels_df':
                set_abandoned_file_selection_state(True)
    else:
        mo.output.clear()
    return


@app.cell
def _(abandoned_analysis_form, get_abandoned_file_selection_state, mo):
    mo.stop(not get_abandoned_file_selection_state())

    if get_abandoned_file_selection_state():
        mo.output.replace(
            mo.vstack(
                [
                    mo.md(f"""Now that we know which files we want to use, we need to decide how to match the data from the two together. Two possible methods are `iteration` and `join`.<br><br>
                    The process of `iteration` involves moving through an object one piece at a time. Once you've performed your action, you move on to the next object and repeat the process. In this specific example, we would `iterate` over the `parcels_df` dataframe by going through it row by row: we would ask, "is the "pin" from this row found in the `liens_df` dataframe? If so, we could add the lien amount to `parcels_df`; if not, we would move on to the next row in `parcels_df` and ask the question again. This would have less contextual data from `liens_df` in the output, but also may not take up much more space than the initial `parcels_df` object (since we are only adding one additional column).<br><br>
                    With `joins`, we combine the data from two dataframes together. In this process, we would wind up with a new dataframe that has all of the columns from both dataframes. We would retain the context from both dataframes, but the object may wind up being rather large to accommodate the data from both original dataframes.<br><br>
                    Having said that, which process do you think we should start with, and why? Don't worry too much about your choice if you are unfamiliar with these methods -- we can discuss them further after you've made a selection. You can always go back and switch your choice if you'd like. For now, it's just important to set out your initial thoughts about the choice."""),
                    abandoned_analysis_form,
                ]
            )
        )
    else:
        mo.output.clear()
    return


@app.cell
def _(mo):
    mo.Html("<div id='joins'></div>")
    return


@app.cell
def _(
    get_abandoned_path_iteration_0,
    get_abandoned_path_join_0,
    mo,
    set_abandoned_path_iteration_1,
    set_abandoned_path_join_1,
):
    mo.stop(not get_abandoned_path_join_0() and not get_abandoned_path_iteration_0())

    if get_abandoned_path_join_0():
        mo.output.replace(
            mo.vstack(
                [
                    mo.md(f"""###Joins"""),
                    mo.md(f"""Let's talk a little bit more about joins!<br><br>
                    Joins are commonly performed when you have two datasets that contain different types of data about the same object(s). If there's a column that repeats across the various datasets, you can use that column as a link to join the data together in one resulting file.<br>

                    Imagine for a second that you are a parent, and you've been keeping track of your child's height and weight every year on their birthday: you saved their height in a file named 'height', and their weight in a file named 'weight'. If you wanted, you could perform a join on these two files to create a new file, 'height and weight'. In this exaple, the object that is the same across the two files is the child, and the column that is the same in both files is the child's birthday. If 'weight' says that the child weighed 35 lbs on their 4th birthday, and 'height' says the child was 3 ft tall, you would use the 4th birthday as the link, and 'height and weight' file would say the child was 35 lbs, 3 ft tall. <br><br>"""),
                    mo.md(f"""###Left, Right, and Inner Joins"""),
                    mo.md(f"""There are a number of different types of joins, but three common types are left, right, and inner joins.<br>

                    One way to think about the types of joins is to think about folding socks. Any time you wash socks, you need to pair them up and put them away. But it's easy for socks to get lost in the process, so you might have some left and right socks that no longer have a mate. If you were to perform an inner join on your socks, you would only keep socks that still form a pair. A left join on the socks would mean you keep all of the matches as well as any left sock that's lost its match. A right join would mean you keep all of the matched socks, as well as all of the right socks that have lost their mate.<br>

            With data, an inner join returns a dataframe that only contains rows where there was a match on your specified column. Left joins would return all rows from the "left" dataframe; matched rows will have the data from the "right" dataframe, and the other rows will have null values in those columns. Right joins return the opposite: all rows from the "right" dataframe are returned, and matched rows will contain the data from the "left" dataframe.<br><br>"""),
                    mo.md(f"""###Joins in pandas"""),
                    mo.md(f"""To perform joins in pandas, you can use the `pd.merge()` function. When using the function, you can specify the two dataframes you want to join, the name of the columns to be used to join the two dataframes, and whether the join should be left, right, or inner. There are additional parameters that you can read about in pandas' docs, but these paramaters, at a minimum, can get you started.<br><br>
                    The function looks something like this: <br><br>
                    _output_dataframe_ = **pd.merge(**  left_dataframe,&ensp; right_dataframe,&ensp; left_column_name,&ensp; right_column_names,&ensp; join_type  **)**<br><br>
                    That's a bit long and awkward to look at -- let's try using that equation with the `parcels_df` and the `liens_df`."""),

                ]
            )
        )
        set_abandoned_path_join_1(True)
    elif get_abandoned_path_iteration_0():
        mo.output.replace(
            mo.vstack(
                [
                    mo.md(f"""###Iteration"""),
                    mo.md(f"""As we previously said, iteration is a process whereby you move step-by-step through an object, pausing to perform some sort of check or operation as you go. The steps you make can depend on the object you are iterating across: for example, if you were to iterate over the string "test", the iterator would pause after each letter of the string (e.g., "t", "e", "s", "t"). If you were iterating over a dataframe (as we are doing here), you would move row by row over the dataframe, stopping at each row.<br><br>
                    The work of iteration is often done with loops. When you use a for loop on a list (for example), you say "for every item in this list, _do something_." That process, of looking at every item, is iteration.<br><br>
                    Since we have decided we are going to use `parcels_df` and `liens_df` as our files, our plan will be to iterate over `parcels_df`, check if the parcel with that ID number has any liens listed in `liens_df`, and if so, copy the lien amount from `liens_df` to `parcels_df` so we have both the lien amount and the geospatial location for relevant parcels in the same dataframe.<br><br>"""),
                    mo.md(
                        f"""That said...moving row by row through the `parcels_df` dataframe sounds like it's going to take a while. Before we try that, we can try and reduce the number of rows to check in `parcels_df` """)
                ]
            )
        ),
        set_abandoned_path_iteration_1(True)
    else:
        mo.output.clear()
    return


@app.cell
def _(
    abandoned_iteration_text_box_parcels_with_liens,
    get_abandoned_path_iteration_1,
    get_abandoned_path_iteration_parcels_counter,
    get_abandoned_path_join_1,
    incorrect_answer_text_generator,
    join_expression_builder,
    mo,
    parcels_with_liens,
    strip_string,
):
    mo.stop(not get_abandoned_path_join_1() and not get_abandoned_path_iteration_1())

    if get_abandoned_path_join_1():
        mo.output.replace(
            join_expression_builder
        )
    elif get_abandoned_path_iteration_1():
        mo.output.replace(
            mo.vstack(
                [
                    mo.md(f"""###Pandas Filtering"""),
                    mo.md(f"""In the residential parcel section, we discussed how pandas dataframes can be filtered with the following expression: <br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**dataframe["COLUMN_NAME"]=="VALUE"** """),
                    mo.md(f"""This works if you have a singular value you're looking for (such as "RESIDENTIAL"), but what about when there's a variety of values you're searching for? Thankfully pandas has an answer for that, too. In the above expression, instead of setting the column equal to a value, you can use an **.isin()** function. It looks like this: <br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**dataframe[dataframe["COLUMN_NAME"].isin(list_of_values)]**"""),
                    mo.md(
                        f"""In this instance, our dataframe is `parcels_df`, its column is "PIN", and the list of values is "liens_df["pin"]". See if you can put that together based on the above example to filter `parcels_df` down to a dataframe of parcels that are also in `liens_df`.<br><br>"""),
                    mo.hstack(
                        [mo.md(f"""<br>**filtered_parcels_df =**"""), abandoned_iteration_text_box_parcels_with_liens],
                        gap=0, justify="space-around", align='center', widths=[1, 7]),
                ]
            )
        )
        if abandoned_iteration_text_box_parcels_with_liens.value:
            if strip_string(abandoned_iteration_text_box_parcels_with_liens.value) == strip_string(parcels_with_liens):
                mo.output.replace_at_index("Correct!", 1)
            else:
                parcels_with_liens_incorrect_response = incorrect_answer_text_generator(
                    abandoned_iteration_text_box_parcels_with_liens.value, parcels_with_liens,
                    get_abandoned_path_iteration_parcels_counter())
                mo.output.replace_at_index(f"""{parcels_with_liens_incorrect_response[0]}""", 1)
    return


@app.cell
def _(
    abandoned_iteration_generate_empty_lien_column_code_snippet,
    abandoned_iteration_text_box_adding_lien_column,
    abandoned_path_check_join,
    get_abandoned_path_iteration_2,
    get_abandoned_path_iteration_lien_column_counter,
    get_abandoned_path_join_2,
    get_abandoned_path_successful_tricog_join,
    incorrect_answer_text_generator,
    join_expression_builder,
    join_expression_output_dict,
    mo,
    pd,
    set_abandoned_path_join_3,
    strip_string,
):
    mo.stop(not get_abandoned_path_join_2() and not get_abandoned_path_iteration_2())

    if get_abandoned_path_join_2():
        join_expression_error_text = ""
        sample_output = None
        if join_expression_builder.value:
            join_exp_responses = join_expression_builder.value
            for key in join_exp_responses:
                if join_exp_responses[key] is None:
                    join_expression_error_text = f"""One of the elements in the expression is empty -- make sure you select a value for every 
                    parameter and hit "Submit" again."""
            if join_exp_responses['leftdrop'] not in join_exp_responses['left_on_cols_drop'] or join_exp_responses[
                'rightdrop'] not in join_exp_responses['right_on_cols_drop']:
                join_expression_error_text = f"""Try again -- make sure that the "left_on" value is a column in the dataframe you selected for 
                the "left" parameter, and that the "right_on" value is a column in the "right" parameter's dataframe."""
            try:
                sample_output = pd.merge(left=join_expression_output_dict[join_exp_responses['leftdrop']],
                                         right=join_expression_output_dict[join_exp_responses['rightdrop']],
                                         left_on=join_exp_responses['left_on_cols_drop'].split(' (')[0],
                                         right_on=join_exp_responses['right_on_cols_drop'].split(' (')[0],
                                         how=join_exp_responses['join_type_drop'])
            except Exception as e:
                join_expression_error_text = f"""Hm...that expression generated an error. The error text that was output was the following: <br><br>{e.args}<br><br>
                Perhaps check and make sure that the columns selected in the `left_on` and `right_on` parameters are able to be matched together?"""
            if join_expression_error_text == "":
                set_abandoned_path_join_3(True)
                abandoned_path_check_join(join_exp_responses)
                sample_output_header = mo.md(f"""##parcels_with_liens""") if get_abandoned_path_successful_tricog_join() else mo.md(f"""""")
                mo.output.replace(
                    mo.vstack(
                        [
                            sample_output_header,
                            sample_output
                        ]
                    )
                )
            else:
                set_abandoned_path_join_3(False)
                mo.output.replace(
                    mo.vstack(
                        [
                            mo.md(join_expression_error_text),
                        ]
                    )
                )
    elif get_abandoned_path_iteration_2():
        mo.output.replace(
            mo.vstack(
                [
                    mo.md(f"""Well done!<br><br>
            Our next step is to add a "lien_amount" column to our new, filtered dataframe. This way, when we do the iteration and find the lien value owed on each of the parcels, we'll have a place to copy the information to.<br><br>
            Pandas has an "assign" function that allows you to add a new column and declare the value for all rows of that new column in one fell swoop. The format looks like this: <br><br>
            **dataframe = dataframe.assign(new_column_name="")**<br><br>
            [**Note**: This is how the function would look to add an empty column.]<br><br>
            Now you try: assign an empty column called "lien_amount" to our newly-created dataframe, "filtered_parcels_df"."""),
                    mo.hstack(
                        [mo.md(f"""**filtered_parcels_df  =** """), abandoned_iteration_text_box_adding_lien_column],
                        gap=0, justify='space-around', align='center', widths=[1, 7])
                ]
            )
        )
        if abandoned_iteration_text_box_adding_lien_column.value:
            if strip_string(abandoned_iteration_text_box_adding_lien_column.value) == strip_string(
                    abandoned_iteration_generate_empty_lien_column_code_snippet):
                mo.output.replace_at_index("Correct!", 1)
            else:
                liens_column_incorrect_response = incorrect_answer_text_generator(
                    abandoned_iteration_text_box_adding_lien_column.value,
                    abandoned_iteration_generate_empty_lien_column_code_snippet,
                    get_abandoned_path_iteration_lien_column_counter())
                mo.output.replace_at_index(f"""{liens_column_incorrect_response[0]}""", 1)
    else:
        mo.output.clear()
    return


@app.cell
def _(
    abandoned_post_join_selector_reflection,
    filtered_parcels_df_liens_col,
    get_abandoned_path_iteration_3,
    get_abandoned_path_join_3,
    get_abandoned_path_successful_tricog_join,
    mo,
):
    mo.stop(not get_abandoned_path_join_3() and not get_abandoned_path_iteration_3())

    if get_abandoned_path_join_3():
        if get_abandoned_path_successful_tricog_join(): 
            abandoned_path_successful_join_final_text = mo.vstack(
                [
                    mo.md(f"""Congratulations! You did it! You performed a join that created a dataframe meeting TriCOG's needs (a set of parcels that have liens assessed against them).<br><br>
            Now that you've successfully constructed the expression to perform a merge, play around with the parameters a bit. See what happens when you change them, and how that impacts the output. For example, the length changes if you switch the type of join.<br><br>
                    Feel free to make whatever changes you want, but take a second to write some of your thoughts about what changes you made and how the changes impact the output in the box below."""),
                    abandoned_post_join_selector_reflection,
                ]
            )
        else: 
            abandoned_path_successful_join_final_text = mo.md(f"""You created a join between the two files that did not create any errors. Well done!<br><br> 
            Look carefully at this join though -- is this what TriCOG is looking for? Does it look like a dataframe that only contains parcels with liens assessed against them? Or is it a list of every parcel, with lien data added to some of them? Or is it a list of every lien, with parcel data attached to some of them? Is it showing something else?<br><br>
            Go back and reconsider the various parameters and think about how each one might alter the output. Continue to tweak them until you arrive at the output that TriCOG is looking for.""")
        mo.output.replace(
            abandoned_path_successful_join_final_text
        )
    elif get_abandoned_path_iteration_3():
        mo.output.replace(
            mo.vstack(
                [
                    filtered_parcels_df_liens_col,
                    mo.md(f"""Here is the output from the code you just entered. If you scroll to the last column of the dataframe, you can see that the 'lien_amount' column has been added. Now we can begin the work of iterating through the dataframe and adding the lien amounts to the dataframe.<br><br>
                    While pandas usually simplifies processes and calculations, its iterations are a bit more complex than the average for loop. Their docs can give you a better explanation, but for now, type the following rows of text into the text entry box below and press 'Submit' and watch the output while it processes.<br><br>
                `for idx, row in parcels_df_with_liens.iterrows():`<br>
                &nbsp;&nbsp;&nbsp;&nbsp;`amount = liens_df[liens_df['pin']==row.PIN].total_amount.values[0]`<br>
                &nbsp;&nbsp;&nbsp;&nbsp;`parcels_df_with_liens.at[idx, 'lien_amount']= amount`"""),
                ]
            )
        )
    else:
        mo.output.clear()
    return


@app.cell
def _(
    abandoned_iteration_iteration_code_block_no_spaces,
    abandoned_iteration_text_box_code_block,
    get_abandoned_path_iteration_3,
    mo,
    strip_string,
):
    mo.stop(not get_abandoned_path_iteration_3())

    if get_abandoned_path_iteration_3(): 
        mo.output.replace(
            abandoned_iteration_text_box_code_block
        )
        if abandoned_iteration_text_box_code_block.value:
            if strip_string(abandoned_iteration_text_box_code_block.value) == strip_string(
                    abandoned_iteration_iteration_code_block_no_spaces):
                mo.output.replace_at_index("Correct!", 1)
            else:
                mo.output.append("Hm...that's not quite right. Perhaps try copying and pasting for now?")
    else:
        mo.output.clear()
    return


@app.cell(hide_code=True)
def _(
    fake_iteration,
    get_abandoned_path_iteration_4,
    mo,
    set_abandoned_path_iteration_5,
):
    mo.stop(not get_abandoned_path_iteration_4())

    if get_abandoned_path_iteration_4():
        mo.output.replace(
            fake_iteration()
        ),
        set_abandoned_path_iteration_5(True)
    else:
        mo.output.clear()
    return


@app.cell(hide_code=True)
def _(abandoned_end_of_iteration_form, get_abandoned_path_iteration_5, mo):
    mo.stop(not get_abandoned_path_iteration_5())

    if get_abandoned_path_iteration_5():
        mo.output.append(
            mo.vstack(
                [
                    mo.md(
                        f"""Sorry, but I stopped that function -- it was taking too long! That seemed much longer than some of the other transformations we've done in the last few steps. Why do you think that took so long? What could we have done to make that faster?"""),
                    abandoned_end_of_iteration_form
                ]
            )
        )
    else:
        mo.output.clear()
    return


@app.cell(hide_code=True)
def _(
    abandoned_join_button_with_link,
    filtered_parcels_df,
    get_abandoned_path_iteration_6,
    liens_df,
    mo,
):
    mo.stop(not get_abandoned_path_iteration_6())

    if get_abandoned_path_iteration_6():
        mo.output.replace(
            mo.vstack(
                [
                    mo.md(
                        f"""Even though we filtered `parcels_df` to get rid of extra rows, our filtered version still had {len(filtered_parcels_df)}. The `liens_df` had {len(liens_df)} rows. That means that for every one of the {len(filtered_parcels_df)} rows in `filtered_parcels_df`, it had to check {len(liens_df)} rows to make sure the value wasn't there."""),
                    mo.md(
                        f"""And while there are a number of different things we could do to try and speed that process up, using a join is a good alternative to iterating through a dataframe. Click the button below to learn more about joins and how to implement them on these dataframes."""),
                    abandoned_join_button_with_link.center()
                ]
            )
        )
    else:
        mo.output.clear()
    return


@app.cell
def _(
    mo,
    set_clipped_residential_count,
    set_combining_files_2,
    set_combining_files_3,
    set_final_output_join_count,
    strip_string,
):
    def handle_clipped_residential_count(value):
        if strip_string(value) == strip_string(combining_path_clipped_and_single_family_join):
            set_combining_files_2(True)
        else:
            set_clipped_residential_count(lambda x: x + 1)

    def handle_final_output_join_count(value):
        if strip_string(value) == strip_string(combining_path_final):
            set_combining_files_3(True)
        else:
            set_final_output_join_count(lambda x: x + 1)

    # combining files prep

    # code snippets
    combining_path_clipped_and_single_family_join = "pd.merge(left=clipped_parcels, right=residential_parcels[['PARID', 'CLASSDESC', 'USEDESC']], left_on='PIN', right_on='PARID')"
    combining_path_final = "pd.merge(left=clipped_and_residential_parcels, right=parcels_with_liens[['PIN', 'total_amount']], left_on='PIN', right_on='PIN')"

    # text boxes
    combining_path_text_box_clipped_and_residential = mo.ui.text(full_width=True).form(
        on_change=handle_clipped_residential_count, clear_on_submit=True)
    combining_final_text_box = mo.ui.text(full_width=True).form(clear_on_submit=True,
                                                                on_change=handle_final_output_join_count)
    return (
        combining_final_text_box,
        combining_path_clipped_and_single_family_join,
        combining_path_final,
        combining_path_text_box_clipped_and_residential,
    )


@app.cell
def combining_files_getters_setters(mo):
    def handle_start_of_combining(value):
        set_combining_files_1(True)
        return value

    get_combining_files_0, set_combining_files_0 = mo.state(False)
    get_combining_files_1, set_combining_files_1 = mo.state(False)
    get_combining_files_2, set_combining_files_2 = mo.state(False)
    get_combining_files_3, set_combining_files_3 = mo.state(False)
    get_combining_files_4, set_combining_files_4 = mo.state(False)
    get_combining_files_5, set_combining_files_5 = mo.state(False)
    get_combining_files_6, set_combining_files_6 = mo.state(False)
    get_combining_files_7, set_combining_files_7 = mo.state(False)
    get_combining_files_8, set_combining_files_8 = mo.state(False)
    get_combining_files_9, set_combining_files_9 = mo.state(False)
    get_combining_files_10, set_combining_files_10 = mo.state(False)
    get_combining_files_11, set_combining_files_11 = mo.state(False)
    get_combining_files_12, set_combining_files_12 = mo.state(False)
    get_combining_files_13, set_combining_files_13 = mo.state(False)

    get_clipped_residential_count, set_clipped_residential_count = mo.state(0)
    get_final_output_join_count, set_final_output_join_count = mo.state(0)
    return (
        get_clipped_residential_count,
        get_combining_files_0,
        get_combining_files_1,
        get_combining_files_2,
        get_combining_files_3,
        get_final_output_join_count,
        handle_start_of_combining,
        set_clipped_residential_count,
        set_combining_files_0,
        set_combining_files_2,
        set_combining_files_3,
        set_final_output_join_count,
    )


@app.cell
def combining_files_text_boxes(handle_start_of_combining, mo):
    combining_files_length_prediction_text_box = mo.ui.text_area(
        label="**How many rows will our final dataframe have?**", full_width=True)

    combining_files_lien_prediction_text_box = mo.ui.text_area(
        label="**What do you think the lowest lien amount in the dataframe will be?**", full_width=True)

    combining_files_survey_form = (
        mo.md("{combining_files_length_prediction_text_box}<br>{combining_files_lien_prediction_text_box}")).batch(
        combining_files_length_prediction_text_box=combining_files_length_prediction_text_box,
        combining_files_lien_prediction_text_box=combining_files_lien_prediction_text_box).form(clear_on_submit=True,
                                                                                                on_change=handle_start_of_combining)
    return (combining_files_survey_form,)


@app.cell
def _(combining_files_survey_form, get_combining_files_0, mo):
    mo.stop(not get_combining_files_0())
    combining_files_path_1 = False

    if get_combining_files_0():
        mo.output.replace(
            mo.vstack(
                [
                    mo.md(f"""##Combining the Data"""),
                    mo.md(f"""We now have three datasets, and each dataset meets one of the criteria set forth by TriCOG land bank:
                    <ul>
                    <li>`clipped_parcels` <i>(parcels within TriCOG's boundaries)</i></li>
                    <li>`residential_parcels` <i>(residential parcels zoned for single-family homes)</i></li>
                    <li>`parcels_with_liens` <i>(parcels that have liens against them, our proxy for abandonment)</i></li>
                    </ul>
                    To get our final result, we need to combine them so our final dataframe only has parcels that meet all three criteria. 
        <br><br>Before we do that though, let's think about what we expect the final dataframe to look like. Answer the following questions in the boxes below.<br>"""),
                    combining_files_survey_form
                ]
            )
        )
    else:
        mo.output.clear()
    return


@app.cell
def _(get_combining_files_1, mo):
    mo.stop(not get_combining_files_1())

    if get_combining_files_1():
        mo.output.replace(
            mo.vstack(
                [
                    mo.md(f"""Now that we've made some predictions, it's time to make some joins! We can manage this using the joins that we learned about while looking for abandoned properties in the previous step.<br><br>
                    First, let's perform a left join to find the parcels within TriCOG's boundaries (`clipped_parcels`, our left dataframe) and the residential, single-family home parcels in the county (`residential_parcels`, our right dataframe).<br><br>
        Remember, the expression format is: <br><br>
        _output_dataframe_ = **pd.merge(**left=**left_df**, right=**right_df**, left_on=**left_column**, right_on=**right_column**)<br><br>

        **Three Notes**:<br> 
        **1.** We'll be using a left join in this step, which is the default. You don't need to use the 'how' parameter.<br>
        **2.** Because 'residential_parcels' has an excessive amount of columns we don't need, we can subset it. You can do that by entering "residential_parcels[['PARID', 'CLASSDESC', 'USEDESC']]" for the right dataframe.<br>
        **3.** The column we'll use for joining from `clipped_parcels` is "PIN". The column we'll need from `residential_parcels` is "PARID".<br><br>

        Type the code into the box below and hit 'Submit'.<br>"""),
                ]
            )
        )
    else:
        mo.output.clear()
    return


@app.cell
def _(
    clipped_parcels,
    combining_path_clipped_and_single_family_join,
    combining_path_text_box_clipped_and_residential,
    get_clipped_residential_count,
    get_combining_files_1,
    incorrect_answer_text_generator,
    mo,
    pd,
    residential_parcels,
    strip_string,
):
    mo.stop(not get_combining_files_1())

    if get_combining_files_1(): 
        mo.output.replace(
            mo.hstack(
                [
                    mo.md(f"""**clipped_and_residential_parcels  =**"""),
                    combining_path_text_box_clipped_and_residential
                ], 
                gap=0, 
                justify='space-around',
                align='center', 
                widths=[1, 4]
            )
        )
        if combining_path_text_box_clipped_and_residential.value:
            clipped_residential_input = combining_path_text_box_clipped_and_residential.value
            if strip_string(clipped_residential_input) == strip_string(combining_path_clipped_and_single_family_join):
                clipped_and_residential = pd.merge(left=clipped_parcels,
                                                   right=residential_parcels[['PARID', 'CLASSDESC', 'USEDESC']],
                                                   left_on='PIN', right_on='PARID')
                mo.output.replace_at_index("Correct!", 1)
            else:
                clipped_residential_incorrect_output = incorrect_answer_text_generator(clipped_residential_input,
                                                                                       combining_path_clipped_and_single_family_join,
                                                                                       get_clipped_residential_count())
                mo.output.replace_at_index(f"""{clipped_residential_incorrect_output[0]}""", 1)
    else: 
        mo.output.clear()
    return


@app.cell
def _(
    clipped_parcels,
    get_combining_files_0,
    mo,
    parcels_df_with_joined_liens,
    pd,
    residential_parcels,
):

    mo.stop(not get_combining_files_0())

    clipped_and_residential_parcels = pd.merge(left=clipped_parcels,
                                               right=residential_parcels[['PARID', 'CLASSDESC', 'USEDESC']],
                                               left_on='PIN', right_on='PARID')
    final_output = pd.merge(left=clipped_and_residential_parcels,
                            right=parcels_df_with_joined_liens[['PIN', 'total_amount']], left_on='PIN', right_on='PIN').astype({"geometry":"str"})
    return (final_output,)


@app.cell
def _(
    combining_final_text_box,
    combining_path_final,
    get_combining_files_2,
    get_final_output_join_count,
    incorrect_answer_text_generator,
    mo,
    strip_string,
):
    mo.stop(not get_combining_files_2())
    reflections = False

    if get_combining_files_2():
        mo.output.replace(
            mo.vstack(
                [
                    mo.md(f"""Great! Now we can join the `clipped_and_residential_parcels` dataframe with our `parcels_with_liens` dataframe to give us our final list.<br><br>

                    Once again, we'll perform a left join (so no `how` parameter is needed), and once again, we'll use a subset of our right dataframe. In this case, our right dataframe will be `parcels_with_liens[['PIN', 'total_amount']]` (it will join on its 'PIN' column).

                    See if you can enter this last bit of code into the box below and you should be set!<br>"""),
                    mo.hstack([mo.md(f"""**final_output  =**"""), combining_final_text_box], gap=0,
                              justify='space-around', align='center', widths=[1, 7])
                ]
            )
        )
        if combining_final_text_box.value:
            if strip_string(combining_final_text_box.value) == strip_string(combining_path_final):
                mo.output.replace_at_index("Correct!", 1)
            else:
                final_output_incorrect_output = incorrect_answer_text_generator(combining_final_text_box.value,
                                                                                combining_path_final,
                                                                                get_final_output_join_count())
                mo.output.replace_at_index(f"""{final_output_incorrect_output[0]}""", 1)
    else:
        mo.output.clear()

        #     final_output = pd.merge(left=clipped_and_residential, right=parcels_df_with_joined_liens[['PIN', 'total_amount']], left_on='PIN', right_on='PIN')
        #     mo.output.replace_at_index("Correct!", 1)
        #     reflections = True
        # else:
        #     mo.output.append("Almost there! Try again!")
    return


@app.cell
def _(final_output, mo):
    # reflections prep

    lien_slider = mo.ui.slider.from_series(final_output['total_amount'], stop=10000, label="Lien Cutoff Amount")
    return (lien_slider,)


@app.cell
def _(final_output, get_combining_files_3, lien_slider, mo):
    mo.stop(not get_combining_files_3())

    if get_combining_files_3():
        mo.output.replace(
            mo.vstack(
                [
                    mo.md(f"""###final_output"""),
                    final_output,
                    mo.md(f"""##Reflections"""),
                    mo.md(f"""After much work, we have arrived at this dataframe.<br><br> 
                    One of the difficult questions of working with large data is knowing whether or not an end product is correct. Take this dataframe, for example: is this output what we were looking for? Does it contain only properties that meet the stated requirements?<br><br>
                    Perhaps counterintuitively, these are two distinct questions. The values within the output dataframe do meet the requirements -- they are all parcels within TriCOG's operating boundaries that are single-family homes with liens against them. This may not be what we were looking for, though. <br><br>
                    Remember that we are trying to identify abandoned properties, and we are using tax liens as a proxy. However, liens can be assessed against a property for a number of reasons (not just abandonment). Take a look at the range of lien values: the lowest lien amount in the dataframe is `${list(final_output.total_amount.sort_values())[0]}.` This hardly feels like the result of abandonment; it could just be clerical or human error instead.

                    Take a look at the slider below. The slider adjusts the amount we consider as the lower-bound lien amount for considering that a house is possibly "abandoned". As we move the slider, we can see how this impacts the total number of houses that would be included in our output dataframe. Try it for yourself; move the slider to various amounts and look at how many houses remain at that level. """),
                    lien_slider.center(),
                    mo.md(f"""Lowest Allowable Amount: ${lien_slider.value:.02f}<br>
                    Number of Properties above Lien Threshhold: {len(final_output[final_output["total_amount"] > lien_slider.value])}""").center(),
                    mo.md(f"""<br><br>Note that as we adjust the slider to around $1000, we've already eliminated roughly 3,000 houses from consideration. And while you would eventually realize the houses were not abandoned if you actually attempted to purchase them, the act of doing so could create stress for individuals and make them feel as if their housing is insecure. The role of your organization is to find homes for people and build community; making people feel uncertain about their current housing goes against the broader work you're trying to do. <br><br>
                    It would be impossible to come up with a dataframe that reflects the real world housing situation 100% accurately, so an important task of yours is to consider what distortions and tradeoffs are being made to represent the real world as data, and how to balance those tradeoffs while creating the least amount of harm.""")
                ]
            )
        )
    return


if __name__ == "__main__":
    app.run()
