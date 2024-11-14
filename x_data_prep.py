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
    from sklearn.model_selection import train_test_split
    return (
        LinearRegression,
        mean_squared_error,
        mo,
        np,
        os,
        pd,
        train_test_split,
    )


@app.cell
def __():
    from keras.models import Sequential
    from keras.layers import LSTM, Dense, Dropout, Input
    from tensorflow.keras.optimizers import Adam

    from tensorflow.keras.models import Model
    from tensorflow.keras.layers import Input, LSTM, Dense, Dropout, Concatenate
    from keras.preprocessing.sequence import pad_sequences
    return (
        Adam,
        Concatenate,
        Dense,
        Dropout,
        Input,
        LSTM,
        Model,
        Sequential,
        pad_sequences,
    )


@app.cell
def __():
    import seaborn as sns
    import matplotlib.pyplot as plt
    return plt, sns


@app.cell
def __():
    import ast
    return ast,


@app.cell
def __(pd):
    # Import Steph Avalanche prediction data as well

    df_dataforavalanchedaymodeldevelopment = pd.read_csv('data/slf/mayer2023/dataforavalanchedaymodeldevelopment.csv')

    df_dataforavalanchedaymodeldevelopment
    return df_dataforavalanchedaymodeldevelopment,


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
def __(df_layers_swiss_thickness):
    df_layers_swiss_thickness
    return


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
    column_names_layers = df_layers_swiss.columns.tolist()

    grouped_layers_dav = df_layers_dav_thickness_density.groupby('profID').agg(lambda x: list(x)).reset_index()
    grouped_layers_swiss = df_layers_swiss_thickness_density.groupby('profID').agg(lambda x: list(x)).reset_index()

    # Print dataframe to check
    grouped_layers_dav
    grouped_layers_swiss
    return column_names_layers, grouped_layers_dav, grouped_layers_swiss


@app.cell
def __(grouped_layers_dav):
    grouped_layers_dav
    return


@app.cell
def __(
    df_properties_observed_and_simulated_dav,
    df_properties_observed_and_simulated_swiss,
    grouped_layers_dav,
    grouped_layers_swiss,
    pd,
):
    # Step 1: Check data types of profID columns
    print("Data types before conversion:")
    print("Swiss Grouped Layers:", grouped_layers_swiss['profID'].dtype)
    print("Swiss Properties:", df_properties_observed_and_simulated_swiss['profID'].dtype)
    print("Davos Grouped Layers:", grouped_layers_dav['profID'].dtype)
    print("Davos Properties:", df_properties_observed_and_simulated_dav['profID'].dtype)

    # Step 2: Convert profID to string in all DataFrames for consistency
    grouped_layers_swiss['profID'] = grouped_layers_swiss['profID'].astype(str)
    df_properties_observed_and_simulated_swiss['profID'] = df_properties_observed_and_simulated_swiss['profID'].astype(str)

    grouped_layers_dav['profID'] = grouped_layers_dav['profID'].astype(str)
    df_properties_observed_and_simulated_dav['profID'] = df_properties_observed_and_simulated_dav['profID'].astype(str)

    # Check data types again after conversion
    print("\nData types after conversion:")
    print("Swiss Grouped Layers:", grouped_layers_swiss['profID'].dtype)
    print("Swiss Properties:", df_properties_observed_and_simulated_swiss['profID'].dtype)
    print("Davos Grouped Layers:", grouped_layers_dav['profID'].dtype)
    print("Davos Properties:", df_properties_observed_and_simulated_dav['profID'].dtype)

    # Step 3: Perform the merges
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
    return df_combined_dav, df_combined_swiss


@app.cell
def __(df_combined_dav):
    df_combined_dav
    return


@app.cell
def __():
    # Function to find the interval index for a given height within a list
    def find_interval(layer_tops, height):
        sorted_heights = sorted(layer_tops)

        # We have two special cases to begin with: observation at zero, or observation at full height
        if height==sorted_heights[-1] or height < sorted_heights[0]:
            # This is most often the special case of RB7 or RB1, which then gives the full height of the snowpack, so should include all layers
            return -1

        for i in range(len(sorted_heights) - 1):
            if sorted_heights[i] <= height < sorted_heights[i + 1]:
                return i  # Return the index of the interval

        return None  # Return None if no interval is found

    def get_wl_index(row):
        layer_tops = row['layer_top']
        height = row['RB_height_obs']
        index = find_interval(layer_tops, height)
        return int(index) if index is not None else -1000  # Convert to int or return -1 for invalid
    return find_interval, get_wl_index


@app.cell
def __(df_combined_dav, df_combined_swiss, get_wl_index):
    # For the weird cases we get index=-1000, otherwise -1 for full_length observations

    # Apply the function to find the interval index for each row
    df_combined_dav['wl_index'] = df_combined_dav.apply(get_wl_index, axis=1)
    df_combined_swiss['wl_index'] = df_combined_swiss.apply(get_wl_index, axis=1)
    return


@app.cell
def __(df_combined_swiss):
    df_combined_swiss
    return


@app.cell
def __(pd):
    # I would now like to create a new function, that takes for each row in the dataframe the wl_index to splice the layer_thickness column

    # 1:st step is to find the layer_thickness[wl_index] value and place this in a new column called 'wl_thickness'

    # 2nd step is to move all of the layer_thickness values for all indices greater than wl_index to a new column called 'layers_above_wl'

    # New function to extract wl_thickness and layers_above_wl
    def extract_thickness(row, overwrite = False):

        if overwrite:
            if row['final_proposed_wl']==-1:
                wl_index = row['wl_index']
            else:
                wl_index = row['final_proposed_wl']
        else:
            wl_index = row['wl_index']

        RB_score = row['RB_score']

        # Ensure wl_index is a valid integer and within bounds
        if wl_index == -1 and RB_score == 7:
            # This is for cases when we observe failures, which are most often non_failures at the full height, and we should include all layers (often RB_score 7)

            wl_density = None
            wl_thickness = None  # We technically do not have a weak layer 
            layers_above_wl = row['layer_thickness'] # ALL layers
            layers_float = map(float, layers_above_wl)
            layers_mm = list(map(lambda x: x * 10, layers_above_wl))
            density_above_wl = row['density_combined']
            density_float = map(float, density_above_wl)

            snow_profile = list(zip(density_float,layers_mm))

        elif wl_index == -1 and RB_score < 7:
            # This is the case when the first layer is the weak_layer, but we record RB_height observation at zero height. Could be fair to assume that the first layer is the weak one. Note that this is slightly different from observing at 3mm (which for sure makes the observation as part of the first layer)

            wl_thickness = row['layer_thickness'][0]  # Get thickness at wl_index
            layers_above_wl = row['layer_thickness'][1:]  # Get all thickness values above the wl_index
            # Convert all elements of the list to float
            layers_float = map(float, layers_above_wl)
            layers_mm = list(map(lambda x: x * 10, layers_above_wl))

            wl_density = row['density_combined'][0] 
            density_above_wl = row['density_combined'][1:] 
            density_float = map(float, density_above_wl)

            snow_profile = list(zip(density_float,layers_mm))


        elif wl_index >= 0:
            wl_thickness = row['layer_thickness'][wl_index]  # Get thickness at wl_index
            layers_above_wl = row['layer_thickness'][wl_index + 1:]  # Get all thickness values above the wl_index
            # Convert all elements of the list to float
            layers_float = map(float, layers_above_wl)
            layers_mm = list(map(lambda x: x * 10, layers_above_wl))

            wl_density = row['density_combined'][wl_index] 
            density_above_wl = row['density_combined'][wl_index + 1:] 
            density_float = map(float, density_above_wl)

            snow_profile = list(zip(density_float,layers_mm))

        else:
            # We have strange exception cases 
            wl_density = None
            wl_thickness = None  # We technically do not have a weak layer 
            layers_above_wl = []
            density_above_wl = []
            snow_profile = []

        return pd.Series([wl_density,wl_thickness, layers_above_wl,density_above_wl,snow_profile])
    return extract_thickness,


@app.cell
def __(df_combined_dav, df_combined_swiss, extract_thickness):
    # Apply the new function to both DataFrames
    df_combined_dav[['wl_density','wl_thickness', 'layers_above_wl', 'density_above_wl','snow_profiles']] = df_combined_dav.apply(extract_thickness, axis=1)
    df_combined_swiss[['wl_density','wl_thickness', 'layers_above_wl', 'density_above_wl','snow_profiles']] = df_combined_swiss.apply(extract_thickness, axis=1)
    return


@app.cell
def __(df_combined_dav, df_combined_swiss):
    # Now we have our final raw_data_dataframes with all information

    df_combined_dav
    df_combined_swiss
    #df_combined_swiss['snow_profiles'][0]
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
def __(df_RB_scores):
    approximate_skier_weights = df_RB_scores['approximate_skier_weights'].tolist()
    return approximate_skier_weights,


@app.cell
def __(approximate_skier_weights, pd):
    # Step 2: Define a function to calculate 'approximate_critical_loads'
    def translate_RB_to_critical_load(rb_score):
        if pd.notna(rb_score) and 1 <= rb_score <= 7:
            return approximate_skier_weights[int(rb_score) - 1]  # -1 to adjust for 0-based indexing
        return None
    return translate_RB_to_critical_load,


@app.cell
def __(df_combined_dav, df_combined_swiss, translate_RB_to_critical_load):
    # Step 3: Apply this function to the 'RB_score' column in df_combined_swiss and df_combined_dav

    # For df_combined_swiss
    df_combined_swiss['approximate_critical_loads'] = df_combined_swiss['RB_score'].apply(translate_RB_to_critical_load)

    # For df_combined_dav
    df_combined_dav['approximate_critical_loads'] = df_combined_dav['RB_score'].apply(translate_RB_to_critical_load)
    return


@app.cell
def __():
    # Now we would like to create a smaller dataframe with all the columns we primarily will use
    # Specify the desired columns in the required order
    columns_to_include = [
        'profID', 'layer_thickness', 'density_combined', 'wl_index', 
        'wl_thickness', 'layers_above_wl', 'layer_top', 'layer_bottom', 
        'hardness', 'gt1', 'gt2', 'gs1', 'gs2', 'crust', 
        'datetime', 'slopeangle', 'RB_score', 'RB_releasetype', 
        'RB_height_obs', 'RB_class', 'localNowcast', 'approximate_critical_loads',  'density_above_wl','snow_profiles', 'RB_class', 'region', 'nbr_layers', 'layers_above_wl', 'density_above_wl'
    ]
    return columns_to_include,


@app.cell
def __(df_combined_dav, df_combined_swiss, pd):
    df_combined_dav['region'] = 1
    df_combined_swiss['region'] = 2

    # Having marked which region both belong to, we proceed to define the final raw_file with all information

    df_raw = pd.concat([df_combined_dav, df_combined_swiss], ignore_index=True)
    return df_raw,


@app.cell
def __(df_raw):
    # Define number of layers in each snow profile
    df_raw['nbr_layers'] = df_raw['layers_above_wl'].apply(lambda x: len(x))
    return


@app.cell
def __(df_raw):
    # Extracting all layers which lack a profile above the weak layer
    df_empty_profile = df_raw[df_raw['layers_above_wl'].apply(lambda x: isinstance(x, list) and len(x) == 0)]

    df_empty_profile

    # Only contains profID 81579, solved now!
    return df_empty_profile,


@app.cell
def __(df_raw):
    df_raw
    return


@app.cell
def __(df_raw, np):
    # Now understand how many layers we should truncate
    # How many layers should we have in out truncated version
    avg_nbr_layers = np.average(df_raw['nbr_layers'])

    truncate = int(avg_nbr_layers)

    truncate
    return avg_nbr_layers, truncate


@app.cell
def __(df_raw, truncate):
    # Create a truncated version of all layers
    df_raw['trunc_layers_above_wl'] = df_raw['layers_above_wl'].apply(
        lambda x: x[:truncate] + [sum(x[truncate:])] if len(x) > truncate else x + [0]*(1+truncate - len(x))
    )
    return


@app.cell
def __(df_raw, np):
    # Compute the weighted average of densities using layers_above_wl as weights
    df_raw['one_density_above_wl'] = df_raw.apply(
        lambda row: np.average(
            row['density_above_wl'], 
            weights=row['layers_above_wl']
        ) if len(row['density_above_wl']) > 0 and len(row['layers_above_wl']) > 0 else 0,
        axis=1
    )
    return


@app.cell
def __(df_raw):
    df_raw['one_layers_above_wl'] = df_raw['layers_above_wl'].apply(
        lambda x: sum(x))
    return


@app.cell
def __(df_raw):
    df_raw['proxy_mass_above_wl'] = df_raw['one_layers_above_wl']*df_raw['one_density_above_wl']
    return


@app.cell
def __(df_raw, np, truncate):
    # And its corresponding densities                                         
    df_raw['trunc_density_above_wl'] = df_raw['density_above_wl'].apply(lambda x: x[:truncate] + [np.average(x[truncate:])] if len(x) > truncate else x + [0]*(1+truncate - len(x)))

    # Could make this to weighted average as well
    return


@app.cell
def __(df_raw):
    df_raw
    return


@app.cell
def __(df_raw, pd):
    # Also add grouped scores here
    bins = [0, 3, 6, 7]  # Define bins
    labels = [1, 2, 3]  # Define corresponding labels for the bins

    # Create RB_score_grouped using pd.cut
    df_raw['RB_score_grouped'] = pd.cut(df_raw['RB_score'], bins=bins, labels=labels, right=True)

    # Second grouping
    bins_4 = [0, 2, 4, 6, 7]  # Define bins
    labels_4 = [1, 2, 3, 4]  # Define corresponding labels for the bins
    df_raw['RB_score_grouped_4'] = pd.cut(df_raw['RB_score'], bins=bins_4, labels=labels_4, right=True)
    return bins, bins_4, labels, labels_4


@app.cell
def __(df_raw, np):
    # And finally, pad the columns
    max_len_layers = df_raw['trunc_layers_above_wl'].apply(len).max()
    max_len_density = df_raw['trunc_density_above_wl'].apply(len).max()

    # Get the maximum length
    max_len = max(max_len_layers, max_len_density)

    print(max_len)

    # Pad each entry in the `trunc_layers_above_wl` column to the maximum length with zeros
    df_raw['trunc_layers_above_wl_padded'] = df_raw['trunc_layers_above_wl'].apply(lambda x: np.pad(x, (0, max_len - len(x)), 'constant', constant_values=0.0))

    # Pad each entry in the `trunc_density_above_wl` column to the maximum length with zeros
    df_raw['trunc_density_above_wl_padded'] = df_raw['trunc_density_above_wl'].apply(lambda x: np.pad(x, (0, max_len - len(x)), 'constant', constant_values=0.0))

    df_raw
    return max_len, max_len_density, max_len_layers


@app.cell
def __(columns_to_include, df_raw):
    df_subset = df_raw[columns_to_include].copy()
    return df_subset,


@app.cell
def __(df_subset):
    df_subset
    return


@app.cell
def __(df_raw, df_subset, os):
    # Define the path to save the new files
    save_path = 'data/slf/mayer2022/'

    # Save the DataFrames in the specified directory
    df_subset.to_csv(os.path.join(save_path, 'df_subset.csv'), index=False)
    df_raw.to_csv(os.path.join(save_path, 'df_raw.csv'), index=False)
    return save_path,


@app.cell
def __(df_subset):
    df_subset
    return


@app.cell
def __():
    ## HERE is where additional data is fetched

    # Create function to extract weak_layer grain type

    # I would like to create a method that takes a row in a dataframe and its wl_index(a column entry), and returns two new columns called wl_gt1 and wl_gt2 that takes the column gt_1 [at wl_index] and gt_2 [at _wl_index]
    return


@app.cell
def __(add_gt_gs_columns_from_row, df_raw):
    df_raw_1 = df_raw.apply(add_gt_gs_columns_from_row, axis=1)
    return df_raw_1,


@app.cell
def __():
    # Method to add 'wl_gt1', 'wl_gt2', 'wl_gs1', and 'wl_gs2' based on the 'wl_index' column from the row
    def add_gt_gs_columns_from_row(row):
        # Use the wl_index value from the row to access the corresponding index
        wl_index = row['wl_index']

        # Extract gt1, gt2, gs1, and gs2 values at wl_index position (assuming they're lists)
        gt1_value = row['gt1'][wl_index] if isinstance(row['gt1'], list) else None
        gt2_value = row['gt2'][wl_index] if isinstance(row['gt2'], list) else None
        gs1_value = row['gs1'][wl_index] if isinstance(row['gs1'], list) else None
        gs2_value = row['gs2'][wl_index] if isinstance(row['gs2'], list) else None
        wl_hand_hardness = row['hardness'][wl_index] if isinstance(row['gs2'], list) else None

        # Add new columns to the row
        row['wl_gt1'] = gt1_value
        row['wl_gt2'] = gt2_value
        row['wl_gs1'] = gs1_value
        row['wl_gs2'] = gs2_value
        row['wl_hardness'] = wl_hand_hardness

        return row
    return add_gt_gs_columns_from_row,


@app.cell
def __():
    # Next, I would like to add a method that checks for each row if the identified wl is actually weak. The column primary_is_weak returns true if gs_1 >=1 and wl_hardness == 1 and gt_1 = 4 / 5 / 6

    # The method should do the same for gs_2 and gt_2 and return secondary_is_weak

    # A third column either_is_weak returns true if either secondary_is_weak or first_is_weak is True
    return


@app.cell
def __():
    def check_weak_layer(row):
        # Ensure gs1, gs2, gt1, gt2, and wl_hardness are interpreted as singular integer values (handle lists)
        gs1_value = row['gs1'][0] if isinstance(row['gs1'], list) else row['gs1']
        gs2_value = row['gs2'][0] if isinstance(row['gs2'], list) else row['gs2']
        gt1_value = row['gt1'][0] if isinstance(row['gt1'], list) else row['gt1']
        gt2_value = row['gt2'][0] if isinstance(row['gt2'], list) else row['gt2']
        wl_hardness_value = row['wl_hardness'][0] if isinstance(row['wl_hardness'], list) else row['wl_hardness']

        # Check primary_is_weak conditions
        primary_is_weak = (
            gs1_value >= 1 and 
            wl_hardness_value < 2 and 
            gt1_value in [4, 5, 6]
        )

        # Check secondary_is_weak conditions
        secondary_is_weak = (
            gs2_value >= 1 and 
            wl_hardness_value < 2 and 
            gt2_value in [4, 5, 6]
        )

        # Either_is_weak is true if either primary_is_weak or secondary_is_weak is True
        either_is_weak = primary_is_weak or secondary_is_weak

        # Add the columns to the row
        row['primary_is_weak'] = primary_is_weak
        row['secondary_is_weak'] = secondary_is_weak
        row['either_is_weak'] = either_is_weak

        return row
    return check_weak_layer,


@app.cell
def __(check_weak_layer, df_raw_1):
    df_raw_2 = df_raw_1.apply(check_weak_layer, axis=1)
    return df_raw_2,


@app.cell
def __(df_raw_2):
    df_raw_2
    return


@app.cell
def __():
    # Method to check the possible weak layers based on given criteria and return matching indices
    def check_possible_weak_layers(row):
        # Lists of values for gt1, gt2, gs1, gs2, and hardness
        gs1_values = row['gs1']  
        gs2_values = row['gs2']
        gt1_values = row['gt1']  
        gt2_values = row['gt2']
        hardness_values = row['hardness']

        # List to store matching indices
        matching_indices_primary = []
        matching_indices_secondary = []

        # Ensure that the lists are of the same length
        length = len(hardness_values)

        # Check each index for matching criteria
        for index in range(length):
            # Check for primary weak layer (based on gt1, gs1, hardness)
            if gt1_values[index] in [4, 5, 6] and gs1_values[index] >= 1 and hardness_values[index] <= 2:
                matching_indices_primary.append(index)  # Add index to primary weak layer

            # Check for secondary weak layer (based on gt2, gs2, hardness)
            if gt2_values[index] in [4, 5, 6] and gs2_values[index] >= 1 and hardness_values[index] <= 2:
                matching_indices_secondary.append(index)  # Add index to secondary weak layer

        # Add the columns to the row
        row['weak_indices_primary'] = matching_indices_primary
        row['weak_indices_secondary'] = matching_indices_secondary
        row['weak_layer_potential_exists'] = len(matching_indices_primary)>0 or len(matching_indices_secondary)>0
        #row['either_is_weak'] = either_is_weak


        # Return the list of matching indices (primary, secondary, or both)
        return row
    return check_possible_weak_layers,


@app.cell
def __(check_possible_weak_layers, df_raw_2):
    df_raw_3 = df_raw_2.apply(check_possible_weak_layers, axis=1)
    return df_raw_3,


@app.cell
def __(df_raw_3):
    df_raw_3
    return


@app.cell
def __():
    # I now want to create a method that takes a row and for all rows where row['either_is_weak'] is false and where row['weak_layer_potential_exists'] is True, returns whichever weak_indices_primary is closest to row['wl_index'], or if weak_indices_primary is empty, whichever index in weak_indices_secondary is closest to wl_index.

    # For those where both either_is_weak and weak_layer_potential_exists are False, an empty list should be returned
    return


@app.cell
def __():
    # Method to add the closest weak layer indices to the row
    def add_closest_weak_layer_index(row):
        # Check if either_is_weak is False and weak_layer_potential_exists is True
        if row['either_is_weak'] == False and row['weak_layer_potential_exists'] == True:
            # Get the list of weak indices (primary or secondary)
            primary_indices = row['weak_indices_primary']
            secondary_indices = row['weak_indices_secondary']
            wl_index = row['wl_index']

            # Initialize the closest indices
            closest_primary = -1  # Default to -1 if no valid index is found
            closest_secondary = -1  # Default to -1 if no valid index is found

            # If weak_indices_primary is not empty, find the closest one in primary
            if primary_indices:
                closest_primary = min(primary_indices, key=lambda x: abs(x - wl_index))

            # If weak_indices_primary is empty, find the closest one in secondary
            if closest_primary == -1 and secondary_indices:
                closest_secondary = min(secondary_indices, key=lambda x: abs(x - wl_index))

            # Add the closest weak layer index columns to the row
            row['closest_weak_primary_index'] = closest_primary
            row['closest_weak_secondary_index'] = closest_secondary
            row['proposed_new_weak_layer'] = closest_primary if closest_primary > -1 else closest_secondary
            row['wl_is_overwritten'] = True
        else:
            # If either_is_weak or weak_layer_potential_exists is False, set both to -1
            row['closest_weak_primary_index'] = -1
            row['closest_weak_secondary_index'] = -1
            row['proposed_new_weak_layer'] = -1
            row['wl_is_overwritten'] = False

        # Return the row with the added columns
        return row
    return add_closest_weak_layer_index,


@app.cell
def __(add_closest_weak_layer_index, df_raw_3):
    df_raw_4 = df_raw_3.apply(add_closest_weak_layer_index, axis=1)
    return df_raw_4,


@app.cell
def __(df_raw_4):
    df_raw_4
    return


@app.cell
def __():
    def add_final_proposed_wl(row):
        # If either_is_weak is True, return the wl_index
        if row['either_is_weak'] == True:
            row['final_proposed_wl'] = row['wl_index']
            row['manually_overwritten_wl'] = False
        # If either_is_weak is False and weak_layer_potential_exists is True, return proposed_new_weak_layer
        elif row['either_is_weak'] == False and row['weak_layer_potential_exists'] == True:
            # Assuming proposed_new_weak_layer is one of the closest weak layer indices
            # Add the logic to find the proposed_new_weak_layer here
            # For now, using a placeholder value of -1 or whatever your logic is
            row['final_proposed_wl'] = row['proposed_new_weak_layer']
            row['manually_overwritten_wl'] = True
        # If both are False, return -1
        else:
            row['final_proposed_wl'] = -1
            row['manually_overwritten_wl'] = False
        return row
    return add_final_proposed_wl,


@app.cell
def __(add_final_proposed_wl, df_raw_4):
    df_raw_5 = df_raw_4.apply(add_final_proposed_wl, axis=1)
    return df_raw_5,


@app.cell
def __(df_raw_5):
    df_raw_5
    return


@app.cell
def __(extract_thickness):
    def conditional_extract_thickness(row):
        if row['final_proposed_wl'] > -1:
            return extract_thickness(row, overwrite = True)
        else:
            return [[], [], [], [], []]  # Return empty lists for each expected column
    return conditional_extract_thickness,


@app.cell
def __(conditional_extract_thickness, df_raw_5):
    # Apply the conditional function
    df_raw_5[['wl_density_new', 'wl_thickness_new', 'layers_above_wl_new', 'density_above_wl_new', 'snow_profiles_new']] = \
        df_raw_5.apply(conditional_extract_thickness, axis=1, result_type='expand')
    return


@app.cell
def __(df_raw_5):
    df_raw_5
    return


@app.cell
def __(df_raw_5):
    # We need a final check here, to handle cases when weak-layer potential exists, but it is in the top layer so there are no layers above it
    df_raw_5['non_empty_profile_above_manual_wl'] = (df_raw_5['manually_overwritten_wl'] == True) & (df_raw_5['layers_above_wl_new'].apply(lambda x: len(x) > 0))
    return


@app.cell
def __(categorize_stability, df_raw_5):
    # Apply the function to create the new 'stability' column
    df_raw_5['stability'] = df_raw_5.apply(categorize_stability, axis=1)
    return


@app.cell
def __(df_raw_5, np, truncate):
    df_raw_5['trunc_layers_above_wl_new'] = df_raw_5['layers_above_wl_new'].apply(
        lambda x: x[:truncate] + [sum(x[truncate:])] if len(x) > truncate else x + [0]*(1+truncate - len(x))
    )

    df_raw_5['trunc_density_above_wl_new'] = df_raw_5['density_above_wl_new'].apply(lambda x: x[:truncate] + [np.average(x[truncate:])] if len(x) > truncate else x + [0]*(1+truncate - len(x)))
    return


@app.cell
def __(df_raw_5):
    df_raw_5
    return


@app.cell
def __(df_raw_5, os, save_path):
    df_raw_5.to_csv(os.path.join(save_path, 'df_raw_weak_layers_exist.csv'), index=False)
    return


@app.cell
def __():
    def categorize_stability(row):
        if row['RB_score'] in [1, 2] or (row['RB_score'] == 3 and row['RB_releasetype'] == 1):
            return -1  # Poor stability
        elif (row['RB_score'] == 3 and row['RB_releasetype'] in [2, 3]) or \
             (row['RB_score'] == 4 and row['RB_releasetype'] in [1, 2, 3]) or \
             (row['RB_score'] == 5 and row['RB_releasetype'] == 1):
            return 0  # Fair stability
        elif (row['RB_score'] == 5 and row['RB_releasetype'] in [2, 3]) or row['RB_score'] in [6, 7]:
            return 1  # Good stability
        return None  # Default case if no conditions are met
    return categorize_stability,


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
