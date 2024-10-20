import marimo

__generated_with = "0.8.15"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import pandas as pd
    import numpy as np
    import os

    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import mean_squared_error
    return LinearRegression, mean_squared_error, mo, np, os, pd


@app.cell
def __():
    from keras.models import Sequential
    from keras.layers import LSTM, Dense, Dropout
    from keras.preprocessing.sequence import pad_sequences
    return Dense, Dropout, LSTM, Sequential, pad_sequences


@app.cell
def __(pd):
    # Preparing data from "Observed and simulated snow profile data" by Stephanie Meyer et al

    # Davos data
    df_properties_observed_and_simulated_dav = pd.read_csv('data/slf/mayer2022/properties_observed_and_simulated_dav.csv')

    df_properties_observed_and_simulated_dav
    return df_properties_observed_and_simulated_dav,


@app.cell
def __(pd):
    # Swiss data
    df_properties_observed_and_simulated_swiss = pd.read_csv('data/slf/mayer2022/properties_observed_and_simulated_swiss.csv')

    df_properties_observed_and_simulated_swiss
    return df_properties_observed_and_simulated_swiss,


@app.cell
def __(df_concatenating_multiple_csv):
    # Path to your folder containing the CSV files
    folder_dav = 'data/slf/mayer2022/observed_snow_profiles/DAV'
    folder_swiss = 'data/slf/mayer2022/observed_snow_profiles/SWISS'

    df_layers_dav = df_concatenating_multiple_csv(folder_dav)
    df_layers_swiss = df_concatenating_multiple_csv(folder_swiss)
    return df_layers_dav, df_layers_swiss, folder_dav, folder_swiss


@app.cell
def __(df_layers_dav):
    df_layers_dav
    return


@app.cell
def __(df_layers_swiss):
    df_layers_swiss
    return


@app.cell
def __(df_layers_swiss):
    # Check how the crust-parameter looks like
    crust_rows = df_layers_swiss[df_layers_swiss['crust'] == 1]

    crust_rows

    # All crust-rows have primary grain type as melt, so could likely safely assume that all crusts are melt-type
    return crust_rows,


@app.cell
def __(df_layers_swiss):
    # Next check all those with melt, to see if any melts are non-crust
    melting_rows = df_layers_swiss[(df_layers_swiss['gt1'] == 7) | (df_layers_swiss['gt2'] == 7)]

    melting_rows

    # It seems as if all gt1 which are melt (7) are also crusts
    return melting_rows,


@app.cell
def __(df_layers_swiss):
    # Checking if surface hoar is always on top
    surface_rows = df_layers_swiss[(df_layers_swiss['gt1'] == 6) | (df_layers_swiss['gt2'] == 6)]

    surface_rows
    return surface_rows,


@app.cell
def __(df_layers_swiss):
    # Check this hypothesis 

    gt1_melt_no_crust = df_layers_swiss[(df_layers_swiss['gt1'] == 7) & (df_layers_swiss['crust'] == 0)]

    gt1_melt_no_crust

    # Hypothesis does not hold, we have melt-types that do not have any crust. 
    # We can either discard of these, or assume they are mixed?

    # What do we do this
    return gt1_melt_no_crust,


@app.cell
def __(df_layers_dav, df_layers_swiss):
    # Function to create thickness column and reorder
    def add_thickness_to_dataframe(df):
        # Creating the 'layer_thickness' column
        df['layer_thickness'] = df['layer_top'] - df['layer_bottom']

        # Reordering the columns with layer_thickness as second column (index 1)
        df = df[['profID', 'layer_thickness'] + [col for col in df.columns if col not in ['profID', 'layer_thickness']]]
        return df

    df_layers_swiss_thickness = add_thickness_to_dataframe(df_layers_swiss)
    df_layers_dav_thickness = add_thickness_to_dataframe(df_layers_dav)
    return (
        add_thickness_to_dataframe,
        df_layers_dav_thickness,
        df_layers_swiss_thickness,
    )


@app.cell
def __(grainform_table_view):
    grainform_table_view
    return


@app.cell
def __(density_parametrization, df_layers_dav, df_layers_swiss, np):
    def add_density_to_dataframe(df):
        # Creating the 'gt_primary' column based on 'gt1' and 'crust' conditions
        df['gt_primary'] = np.where((df['gt1'] == 7) & (df['crust'] == 1), 7, 
                                    np.where((df['gt1'] == 7) & (df['crust'] == 0), 8, df['gt1']))

        # Creating the 'gt_secondary' column based on 'gt2' and 'crust' conditions
        df['gt_secondary'] = np.where((df['gt2'] == 7) & (df['crust'] == 1), 7, 
                                      np.where((df['gt2'] == 7) & (df['crust'] == 0), 8, df['gt2']))

        # Calculating densities using a predefined function 'density_parametrization'
        df['density_primary'] = df.apply(lambda row: density_parametrization(row['hardness'], row['gt_primary']), axis=1)
        df['density_secondary'] = df.apply(lambda row: density_parametrization(row['hardness'], row['gt_secondary']), axis=1)

        # Combine the densities (75% primary, 25% secondary)
        df['density_combined'] = df['density_primary'] * 0.75 + df['density_secondary'] * 0.25

        return df

    # Applying the function to both dataframes
    df_layers_swiss_thickness_density = add_density_to_dataframe(df_layers_swiss)
    df_layers_dav_thickness_density = add_density_to_dataframe(df_layers_dav)
    return (
        add_density_to_dataframe,
        df_layers_dav_thickness_density,
        df_layers_swiss_thickness_density,
    )


@app.cell
def __(df_layers_swiss_thickness_density):
    df_layers_swiss_thickness_density
    return


@app.cell
def __(
    df_layers_dav_thickness_density,
    df_layers_swiss,
    df_layers_swiss_thickness_density,
):
    # Having added column thickness and density, we now group all dataframe entries with the same profID
    column_names_layers = df_layers_swiss.columns.tolist()

    grouped_layers_dav = df_layers_dav_thickness_density.groupby('profID').agg(lambda x: list(x)).reset_index()
    grouped_layers_swiss = df_layers_swiss_thickness_density.groupby('profID').agg(lambda x: list(x)).reset_index()

    # Print dataframe to check
    grouped_layers_dav.columns
    grouped_layers_swiss.columns
    return column_names_layers, grouped_layers_dav, grouped_layers_swiss


@app.cell
def __(
    df_properties_observed_and_simulated_dav,
    df_properties_observed_and_simulated_swiss,
    grouped_layers_dav,
    grouped_layers_swiss,
    pd,
):
    # Check data types of profID columns
    print("Data types before conversion:")
    print("Swiss Grouped Layers:", grouped_layers_swiss['profID'].dtype)
    print("Swiss Properties:", df_properties_observed_and_simulated_swiss['profID'].dtype)
    print("Davos Grouped Layers:", grouped_layers_dav['profID'].dtype)
    print("Davos Properties:", df_properties_observed_and_simulated_dav['profID'].dtype)

    # Convert profID to string in all dataframes for consistency
    grouped_layers_swiss['profID'] = grouped_layers_swiss['profID'].astype(str)
    df_properties_observed_and_simulated_swiss['profID'] = df_properties_observed_and_simulated_swiss['profID'].astype(str)

    grouped_layers_dav['profID'] = grouped_layers_dav['profID'].astype(str)
    df_properties_observed_and_simulated_dav['profID'] = df_properties_observed_and_simulated_dav['profID'].astype(str)

    # Now perform the merges
    # Merging the Swiss dataframes based on 'profID'
    df_combined_swiss = pd.merge(
        grouped_layers_swiss, 
        df_properties_observed_and_simulated_swiss, 
        on='profID', 
        how='inner'
    )

    # Merging the Davos dataframes based on 'profID'
    df_combined_dav = pd.merge(
        grouped_layers_dav, 
        df_properties_observed_and_simulated_dav, 
        on='profID', 
        how='inner'
    )


    print("Davos_combined:", df_combined_dav.columns)
    return df_combined_dav, df_combined_swiss


@app.cell
def __(df_combined_dav):
    df_combined_dav
    return


@app.cell
def __(df_combined_dav, df_combined_swiss):
    # Function to find the interval index for a given height within a list
    def find_interval(layer_tops, height):
        sorted_heights = sorted(layer_tops)

        for i in range(len(sorted_heights) - 1):
            if sorted_heights[i] <= height < sorted_heights[i + 1]:
                return i  # Return the index of the interval

        return None  # Return None if no interval is found

    def get_wl_index(row):
        layer_tops = row['layer_top']
        height = row['RB_height_obs']
        index = find_interval(layer_tops, height)
        return int(index) if index is not None else -1  # Convert to int or return -1 for invalid


    # Apply the function to find the interval index for each row
    df_combined_dav['wl_index'] = df_combined_dav.apply(get_wl_index, axis=1)
    df_combined_swiss['wl_index'] = df_combined_swiss.apply(get_wl_index, axis=1)
    return find_interval, get_wl_index


@app.cell
def __(df_combined_swiss):
    df_combined_swiss
    return


@app.cell
def __(df_combined_dav, df_combined_swiss, pd):
    # I would now like to create a new function, that takes for each row in the dataframe the wl_index to splice the layer_thickness column

    # 1:st step is to find the layer_thickness[wl_index] value and place this in a new column called 'wl_thickness'

    # 2nd step is to move all of the layer_thickness values for all indices greater than wl_index to a new column called 'layers_above_wl'



    # New function to extract wl_thickness and layers_above_wl
    def extract_thickness(row):
        wl_index = row['wl_index']

        # Ensure wl_index is a valid integer and within bounds
        if wl_index < 0 or wl_index >= len(row['layer_thickness']):
            wl_thickness = None  # Invalid index, set to None
            layers_above_wl = []  # No layers above
        else:
            wl_thickness = row['layer_thickness'][wl_index]  # Get thickness at wl_index
            layers_above_wl = row['layer_thickness'][wl_index + 1:]  # Get all thickness values above the wl_index

        return pd.Series([wl_thickness, layers_above_wl])

    # Apply the new function to both DataFrames
    df_combined_dav[['wl_thickness', 'layers_above_wl']] = df_combined_dav.apply(extract_thickness, axis=1)
    df_combined_swiss[['wl_thickness', 'layers_above_wl']] = df_combined_swiss.apply(extract_thickness, axis=1)
    return extract_thickness,


@app.cell
def __(df_combined_dav, df_combined_swiss):
    # Now we have our final raw_data_dataframes with all information
    df_combined_swiss
    df_combined_dav
    return


@app.cell
def __(pd):
    # Data for Rutschblock Scores and Loading Steps
    data_scores = {
        "RB_score": [1, 2, 3, 4, 5, 6, 7],
        "description": [
            "Isolating the block, during digging or sawing",
            "Gently approaching or stepping onto the block",
            "Pushing downwards by dropping from straight legs",
            "First jump from above with skis/board",
            "Second or third jump from above with skis/board",
            "Jump from above without skis or board",
            "Block does not slide"
        ]
    }

    df_RB_scores = pd.DataFrame(data_scores)

    # Data for Release Types
    data_release_types = {
        "Release Type": [
            "Whole block",
            "Part of the block",
            "(Usually below skis)",
            "Only an edge"
        ]
    }

    df_release_types = pd.DataFrame(data_release_types)

    # Data for Fracture Types
    data_fracture_types = {
        "Fracture Type": ["Smooth", "Rough", "Irregular"],
        "Characteristics of Fracture Plane": ["", "", ""]
    }

    df_fracture_types = pd.DataFrame(data_fracture_types)
    return (
        data_fracture_types,
        data_release_types,
        data_scores,
        df_RB_scores,
        df_fracture_types,
        df_release_types,
    )


@app.cell
def __(calculate_implied_weight, df_RB_scores):
    df_RB_scores

    # Define some implied skier weight of snowpack loading matching RB_score
    RB_1 = 0
    RB_2 = 80
    RB_3 = calculate_implied_weight(80, 9.82, 0.05, 0.08)        # Bending knees
    RB_4 = calculate_implied_weight(80, 9.82, 0.30, 0.15)        # Jumping from above first try
    RB_5 = 1.5*RB_4                                             # Assuming second or third jump is about 50% greater than previous

    # Pressure with skis is approximately on an area of 1m*0.15*2
    # Pressure without skis woudl be 0.3*0.3
    RB_6 = RB_4*(1*0.15*2)/(0.3*0.3)
    RB_7 = 2*RB_6

    df_RB_scores['approximate_skier_weights'] = [RB_1, RB_2, RB_3, RB_4, RB_5, RB_6, RB_7]

    df_RB_scores
    return RB_1, RB_2, RB_3, RB_4, RB_5, RB_6, RB_7


@app.cell
def __(np):
    def calculate_implied_weight(mass, g, h, impact_time):
        """
        Function to calculate the implied weight based on jump height and impact time.

        Parameters:
        - mass (float): Mass of the person in kg.
        - g (float): Acceleration due to gravity (9.81 m/s²).
        - h (float): Height of the jump in meters.
        - impact_time (float): Impact time in seconds.

        Returns:
        - implied_weight (float): The implied weight based on the force calculation.
        """

        # Step 1: Calculate the velocity just before impact using v = sqrt(2gh)
        velocity = np.sqrt(2 * g * h)

        # Step 2: Estimate the impact force using F = (mv) / Δt
        force = (mass * velocity) / impact_time

        # Step 3: Calculate the implied weight based on the force
        implied_weight = force / g

        return implied_weight
    return calculate_implied_weight,


@app.cell
def __(df_RB_scores, df_combined_dav, df_combined_swiss, pd):
    approximate_skier_weights = df_RB_scores['approximate_skier_weights'].tolist()

    # Step 2: Define a function to calculate 'approximate_critical_loads'
    def translate_RB_to_critical_load(rb_score):
        if pd.notna(rb_score) and 1 <= rb_score <= 7:
            return approximate_skier_weights[int(rb_score) - 1]  # -1 to adjust for 0-based indexing
        return None

    # Step 3: Apply this function to the 'RB_score' column in df_combined_swiss and df_combined_dav

    # For df_combined_swiss
    df_combined_swiss['approximate_critical_loads'] = df_combined_swiss['RB_score'].apply(translate_RB_to_critical_load)

    # For df_combined_dav
    df_combined_dav['approximate_critical_loads'] = df_combined_dav['RB_score'].apply(translate_RB_to_critical_load)
    return approximate_skier_weights, translate_RB_to_critical_load


@app.cell
def __():
    # Now we would like to create a smaller dataframe with all the columns we primarily will use
    # Specify the desired columns in the required order
    columns_to_include = [
        'profID', 'layer_thickness', 'density_combined', 'wl_index', 
        'wl_thickness', 'layers_above_wl', 'layer_top', 'layer_bottom', 
        'hardness', 'gt1', 'gt2', 'gs1', 'gs2', 'crust', 
        'datetime', 'slopeangle', 'RB_score', 'RB_releasetype', 
        'RB_height_obs', 'RB_class', 'localNowcast', 'approximate_critical_loads'
    ]
    return columns_to_include,


@app.cell
def __(columns_to_include, df_combined_dav, df_combined_swiss):
    # Create a copy of the smaller subset for df_combined_dav
    df_dav_subset = df_combined_dav[columns_to_include].copy()

    # Create a copy of the smaller subset for df_combined_swiss
    df_swiss_subset = df_combined_swiss[columns_to_include].copy()
    return df_dav_subset, df_swiss_subset


@app.cell
def __(df_dav_subset):
    #### THESE ARE THE DATASETS WE WOULD LIKE TO WORK WITH ###### 
    df_dav_subset 

    # We will use the above for modelling, and df_swiss_subset for validation

    # First regression model should be taking the snow profile (only heights of layers)
    return


@app.cell
def __(os, pd):
    def df_concatenating_multiple_csv(folder_path):

        dataframes = []

        for filename in os.listdir(folder_path):
            if filename.endswith('.csv'):
                # Full file path
                file_path = os.path.join(folder_path, filename)

                # Read the CSV file into a DataFrame
                df = pd.read_csv(file_path)

                # Extract profID from the filename (without the .csv extension)
                profID = os.path.splitext(filename)[0]

                # Add the profID column to the DataFrame
                df['profID'] = profID

                # Make 'profID' the first column by rearranging the columns
                columns = ['profID'] + [col for col in df.columns if col != 'profID']
                df = df[columns]

                # Append the DataFrame to the list
                dataframes.append(df)

        # Concatenate all DataFrames into a single DataFrame
        final_df = pd.concat(dataframes, ignore_index=True)

        return final_df
    return df_concatenating_multiple_csv,


@app.cell
def __(grainform_df):
    def density_parametrization(hardness_index, grainform_index):

        grainform_row = grainform_df.loc[
            grainform_df["id"] == grainform_index
        ]
        _a = grainform_row["a"].values[0]
        _b = grainform_row["b"].values[0]

        if grainform_index == 3:  # exponential case for Rounded grains
            _density = _a + _b * (hardness_index**3.15)
        else:
            _density = _a + _b * hardness_index

        # grain_list[index] = grainform_row["abbreviation"]
        # layers[index][0] = _density

        return _density
    return density_parametrization,


@app.cell
def __(mo, pd):
    # Density parametrization
    # Hand hardness density parametrization according to Geldsetzer & Jamieson (2000) [1]
    # [1] https://arc.lib.montana.edu/snow-science/objects/issw-2000-121-127.pdf
    # These have been updated to match the following ID as defined by Mayer et al (2022)



    # Need to discuss this w. Valle

    # Layers as their thickness, with corresponding hand_hardness 

    # Questions: how can grain-types be different within the same layer? gt1 vs gt2 with their accompanying gs1 and gs2
    # How does weaklayer thickness affect the model? Should realistically become more reactive, but we have no note of this in the swiss/dav dataset. We have the entire snow profile

    # Proposed solution
    # Assume that all which have different grain types are Faceted mixed forms
    # Assume that all 

    grainforms = [
        # ID, abbrv, symbol, a, b, description
        (1, "PP", 45, 36, "Precipitation particles"), # Perfect match
        (0, "PPgp", 83, 37, "Graupel"), # Perfect match
        (2, "DF", 65, 36, "Decomposing and fragmented precipitation particles"), # Perfect match
        (3, "RG", 154, 1.51, "Rounded grains"), # Perfect match
        (9, "RGmx", 91, 42, "Rounded mixed forms"),  # We have assumed that RFMC (Mayer) matches best here
        (6, "SH", 140, 0, "Surface hoar"),
        (4, "FC", 112, 46, "Faceted crystals"), # Perfect match
        (8, "FCmx", 56, 64, "Faceted mixed forms"), # Assuming melt forms without crusts
        (5, "DH", 185, 25, "Depth hoar"), # Match
        # MFCr density is constant and takes as mean of Table 1 in [1]
        (7, "MFCr", 292.25, 0, "Melt-freeze crusts"), # Assuming melt forms with crusts
    ]

    ## ID equal to 000 does not have a pure match from the Mayer (2022) grain forms vs Geltsetzer & Jamieson (2000). 

    ## NON-MATHCES ##
    # Rounding faceted crystals (Mayer #9) could be either (i) rounded mixed forms (Geltzer #4) or (ii) faceted mixed forms (Geltzer #6). 
    # Surface hoar (Mayer #6) is likely faceted crystals but at the top of the snow-pack, and could perhaps be assumed to be similar density as buried hoar. 
    # Melt freese crusts are those that are melt forms (Mayer #7) but also marked as crusts (in a separate column in the data). Note that not all melt forms are crusts, but that all crusts are melts (Mayer #7) as their primary grain type gt1. We thus need to decide how to handle melt types which are not crusts. 

    # ID:s as defined by Mayer (2022)
    # 1: precipitation particles (OK), 2: fragmented particles (OK), 3: rounded grains (OK), 4: faceted crystals (OK), 5: depth hoar (OK), 6: surface hoar, 7: melt forms, 8: ice layer, 9: rounding faceted crystal, 0: graupel



    # Collect grainforms info in a dataframe
    grainform_df = pd.DataFrame(
        grainforms, columns=["id", "abbreviation", "a", "b", "type"]
    )

    # Provide a table view of the dataframe
    grainform_table_view = mo.ui.table(
        data=grainform_df,
        show_column_summaries=False,
        selection=None,
        label="Hand-hardness-to-density parametrization of depending on grain type",
    )

    mo.md(
        '<h2 style="font-family: Gill Sans, Tahoma;">⚖️ DENSITY PARAMETRIZATION</h2><hr>'
    )
    return grainform_df, grainform_table_view, grainforms


if __name__ == "__main__":
    app.run()
