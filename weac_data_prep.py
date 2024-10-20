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
            density_above_wl = []
            snow_profile = []
        else:
            wl_thickness = row['layer_thickness'][wl_index]  # Get thickness at wl_index

            layers_above_wl = row['layer_thickness'][wl_index + 1:]  # Get all thickness values above the wl_index
            # Convert all elements of the list to float
            layers_float = map(float, layers_above_wl)
            layers_mm = list(map(lambda x: x * 10, layers_above_wl))

            density_above_wl = row['density_combined'][wl_index + 1:] 
            density_float = map(float, density_above_wl)

            snow_profile = list(zip(density_float,layers_mm))

        return pd.Series([wl_thickness, layers_above_wl,density_above_wl,snow_profile])

    # Apply the new function to both DataFrames
    df_combined_dav[['wl_thickness', 'layers_above_wl', 'density_above_wl','snow_profiles']] = df_combined_dav.apply(extract_thickness, axis=1)
    df_combined_swiss[['wl_thickness', 'layers_above_wl', 'density_above_wl','snow_profiles']] = df_combined_swiss.apply(extract_thickness, axis=1)
    return extract_thickness,


@app.cell
def __(df_combined_dav, df_combined_swiss):
    # Now we have our final raw_data_dataframes with all information
    df_combined_swiss
    df_combined_dav

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
def __(df_raw, np):
    # Now understand how many layers we should truncate
    # How many layers should we have in out truncated version
    avg_nbr_layers = np.average(df_raw['nbr_layers'])

    truncate = int(avg_nbr_layers)
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
def __(
    Dense,
    Dropout,
    LSTM,
    Sequential,
    df_raw,
    mean_squared_error,
    np,
    pad_sequences,
    pd,
    plt,
    sns,
    train_test_split,
):
    # Step 1: Prepare the data
    max_length = 15  # Define the maximum length for padding

    # Pad the `trunc_layers_above_wl` and `trunc_density_above_wl` arrays for input
    X_layers = pad_sequences(df_raw['trunc_layers_above_wl'].tolist(), maxlen=max_length, padding='post', value=0.0)
    X_density = pad_sequences(df_raw['trunc_density_above_wl'].tolist(), maxlen=max_length, padding='post', value=0.0)

    # Stack the two input features into one 3D array (samples, timesteps, features)
    X_combined = np.stack((X_layers, X_density), axis=2)

    # Rename target variable
    target_rb_score = df_raw['RB_score_grouped'].values  # Unique name for the target variable

    # Split data into 70% training and 30% validation
    X_train, X_test, y_train, y_test = train_test_split(X_combined, target_rb_score, test_size=0.3, random_state=42)

    # Step 2: Define the LSTM model
    model = Sequential()
    model.add(LSTM(64, input_shape=(X_train.shape[1], X_train.shape[2]), return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(32, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(1))  # Output layer for regression

    # Compile the model
    model.compile(optimizer='adam', loss='mean_squared_error')

    # Step 3: Train the model
    history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test))

    # Step 4: Predict on the test data
    y_pred = model.predict(X_test)

    # Step 5: Evaluate the model
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)

    print(f'Root Mean Squared Error: {rmse}')

    # Step 6: Plot Loss Graph - Show how loss decreases over epochs
    plt.figure(figsize=(10, 6))
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('Training and Validation Loss over Epochs')
    plt.xlabel('Epochs')
    plt.ylabel('Loss (Mean Squared Error)')
    plt.legend()
    plt.show()

    # Step 7: Predicted vs Actual Values - Scatter plot
    plt.figure(figsize=(8, 6))
    plt.scatter(y_test, y_pred, c='blue', marker='o', label='Predictions')
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)  # Diagonal line for perfect prediction
    plt.title('Predicted vs Actual RB_score')
    plt.xlabel('Actual RB_score')
    plt.ylabel('Predicted RB_score')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Step 8: Convert y_test to numeric if it's categorical or object
    y_test = pd.to_numeric(y_test, errors='coerce')

    # Make sure y_pred is a flat array for subtraction
    y_pred = y_pred.flatten()

    # Step 9: Residual Plot - Errors between predicted and actual values
    residuals = y_test - y_pred

    plt.figure(figsize=(8, 6))
    sns.histplot(residuals, bins=20, kde=True)
    plt.title('Distribution of Residuals')
    plt.xlabel('Residuals (Actual - Predicted)')
    plt.ylabel('Frequency')
    plt.show()

    # Optionally: Residuals vs Predicted Values
    plt.figure(figsize=(8, 6))
    plt.scatter(y_pred, residuals, c='blue', marker='o', label='Residuals')
    plt.axhline(y=0, color='r', linestyle='--')
    plt.title('Residuals vs Predicted RB_score')
    plt.xlabel('Predicted RB_score')
    plt.ylabel('Residuals')
    plt.grid(True)
    plt.show()

    return (
        X_combined,
        X_density,
        X_layers,
        X_test,
        X_train,
        history,
        max_length,
        model,
        mse,
        residuals,
        rmse,
        target_rb_score,
        y_pred,
        y_test,
        y_train,
    )


@app.cell
def __(
    Dense,
    Dropout,
    LSTM,
    Sequential,
    df_dav_subset,
    df_swiss_subset,
    max_length,
    mean_squared_error,
    np,
    pad_sequences,
    plt,
):
    # Step 1: Prepare the data
    # Assuming df_dav_subset and df_swiss_subset already contain padded thickness and density data
    # max_length = 15  # Define the maximum length for padding

    # Vad gör man åt längd? Pröva med genomsnittlig densitet. Skulle summera bort allt därutöver över lager fem. Prövar att exkludera alla under fyra. Alla ska få in en ekvivalent modell. 


    # Nummer två: har jag tillräckligt mycket data? Två fel: inte tillräckligt med data ELLER så är svårt att modellera. Pröva om det är mängden data som är problemet. 

    # Pröva med en linjör regression: se hur dålig den är. 


    # Vill skaffa dig ett felmått: möta felet du gör i preditkionen. Hur ofta klassar jag rätt saker, hur gör man fel? Introducera confusion matrix. Felmåtten.abs

    # Andra typer av fel: 

    # Tredje saken: pröva att komprimera ihop klasserna. 


    # Pad the layer_thickness and combined_density arrays for training
    X_train_thickness2 = pad_sequences(df_dav_subset['layers_above_wl'].tolist(), maxlen=max_length, padding='post', value=0.0)
    X_train_density2 = pad_sequences(df_dav_subset['density_above_wl'].tolist(), maxlen=max_length, padding='post', value=0.0)

    X_test_thickness2 = pad_sequences(df_swiss_subset['layers_above_wl'].tolist(), maxlen=max_length, padding='post', value=0.0)
    X_test_density2 = pad_sequences(df_swiss_subset['density_above_wl'].tolist(), maxlen=max_length, padding='post', value=0.0)

    # Stack the thickness and density arrays as two features
    X_train2 = np.stack((X_train_thickness2, X_train_density2), axis=-1)  # Shape will be (num_samples, max_length, 2)
    X_test2 = np.stack((X_test_thickness2, X_test_density2), axis=-1)

    y_train2 = df_dav_subset['RB_score'].values
    y_test2 = df_swiss_subset['RB_score'].values

    model2 = Sequential()
    model2.add(LSTM(64, input_shape=(X_train2.shape[1], X_train2.shape[2]), return_sequences=True))
    model2.add(Dropout(0.2))
    model2.add(LSTM(32, return_sequences=False))
    model2.add(Dropout(0.2))
    model2.add(Dense(1))  # Output layer for regression

    # Compile the model
    model2.compile(optimizer='adam', loss='mean_squared_error')

    # Step 3: Train the model
    history2 = model2.fit(X_train2, y_train2, epochs=50, batch_size=32, validation_split=0.2)

    # Step 4: Predict on the test data
    y_pred2 = model2.predict(X_test2)

    # Step 5: Evaluate the model
    mse2 = mean_squared_error(y_test2, y_pred2)
    rmse2 = np.sqrt(mse2)

    print(f'Root Mean Squared Error (RMSE) for Model 2: {rmse2}')

    # Step 6: Compare performance - Visualization
    # Loss Graph: Show how loss decreases over epochs
    plt.figure(figsize=(10, 6))
    plt.plot(history2.history['loss'], label='Training Loss')
    plt.plot(history2.history['val_loss'], label='Validation Loss')
    plt.title('Training and Validation Loss over Epochs (Model 2: Thickness + Density)')
    plt.xlabel('Epochs')
    plt.ylabel('Loss (Mean Squared Error)')
    plt.legend()
    plt.show()

    # Scatter plot of predicted vs actual values
    plt.figure(figsize=(8, 6))
    plt.scatter(y_test2, y_pred2, c='blue', marker='o', label='Predictions')
    plt.plot([y_test2.min(), y_test2.max()], [y_test2.min(), y_test2.max()], 'r--', lw=2)  # Diagonal line for perfect prediction
    plt.title('Predicted vs Actual RB_score (Model 2: Thickness + Density)')
    plt.xlabel('Actual RB_score')
    plt.ylabel('Predicted RB_score')
    plt.legend()
    plt.grid(True)
    plt.show()
    return (
        X_test2,
        X_test_density2,
        X_test_thickness2,
        X_train2,
        X_train_density2,
        X_train_thickness2,
        history2,
        model2,
        mse2,
        rmse2,
        y_pred2,
        y_test2,
        y_train2,
    )


@app.cell
def __(
    Concatenate,
    Dense,
    Dropout,
    Input,
    LSTM,
    Model,
    df_dav_subset,
    df_swiss_subset,
    max_length,
    mean_squared_error,
    np,
    pad_sequences,
    plt,
):
    # MODEL 3 now with slopeangle as well

    # Pad the layer_thickness and combined_density arrays for training
    X_train_thickness3 = pad_sequences(df_dav_subset['layers_above_wl'].tolist(), maxlen=max_length, padding='post', value=0.0)
    X_train_density3 = pad_sequences(df_dav_subset['density_above_wl'].tolist(), maxlen=max_length, padding='post', value=0.0)
    X_train_slopeangle3 = df_dav_subset['slopeangle'].values.reshape(-1, 1)  # Reshape for compatibility

    X_test_thickness3 = pad_sequences(df_swiss_subset['layers_above_wl'].tolist(), maxlen=max_length, padding='post', value=0.0)
    X_test_density3 = pad_sequences(df_swiss_subset['density_above_wl'].tolist(), maxlen=max_length, padding='post', value=0.0)
    X_test_slopeangle3 = df_swiss_subset['slopeangle'].values.reshape(-1, 1)

    # Stack the thickness and density arrays as two features
    X_train_sequence3 = np.stack((X_train_thickness3, X_train_density3), axis=-1)  # Shape will be (num_samples, max_length, 2)
    X_test_sequence3 = np.stack((X_test_thickness3, X_test_density3), axis=-1)

    y_train3 = df_dav_subset['RB_score'].values
    y_test3 = df_swiss_subset['RB_score'].values

    # Input for sequence data (layer_thickness + combined_density)
    sequence_input3 = Input(shape=(X_train_sequence3.shape[1], X_train_sequence3.shape[2]))
    x = LSTM(64, return_sequences=True)(sequence_input3)
    x = Dropout(0.2)(x)
    x = LSTM(32, return_sequences=False)(x)
    x = Dropout(0.2)(x)

    # Input for slopeangle data (singular value)
    slopeangle_input3 = Input(shape=(1,))
    y = Dense(16, activation='relu')(slopeangle_input3)

    # Combine both sequence and slopeangle inputs
    combined3 = Concatenate()([x, y])

    # Output layer for regression
    z = Dense(1)(combined3)

    # Step 3: Create the model
    model3 = Model(inputs=[sequence_input3, slopeangle_input3], outputs=z)

    # Compile the model
    model3.compile(optimizer='adam', loss='mean_squared_error')

    # Step 4: Train the model
    history3 = model3.fit([X_train_sequence3, X_train_slopeangle3], y_train3, epochs=50, batch_size=32, validation_split=0.2)

    # Step 5: Predict on the test data
    y_pred3 = model3.predict([X_test_sequence3, X_test_slopeangle3])

    # Step 6: Evaluate the model
    mse3 = mean_squared_error(y_test3, y_pred3)
    rmse3 = np.sqrt(mse3)

    print(f'Root Mean Squared Error (RMSE) for Model 3: {rmse3}')

    # Step 7: Compare performance - Visualization
    # Loss Graph: Show how loss decreases over epochs
    plt.figure(figsize=(10, 6))
    plt.plot(history3.history['loss'], label='Training Loss')
    plt.plot(history3.history['val_loss'], label='Validation Loss')
    plt.title('Training and Validation Loss over Epochs (Model 3: Thickness + Density + Slopeangle)')
    plt.xlabel('Epochs')
    plt.ylabel('Loss (Mean Squared Error)')
    plt.legend()
    plt.show()

    # Scatter plot of predicted vs actual values
    plt.figure(figsize=(8, 6))
    plt.scatter(y_test3, y_pred3, c='blue', marker='o', label='Predictions')
    plt.plot([y_test3.min(), y_test3.max()], [y_test3.min(), y_test3.max()], 'r--', lw=2)  # Diagonal line for perfect prediction
    plt.title('Predicted vs Actual RB_score (Model 3: Thickness + Density + Slopeangle)')
    plt.xlabel('Actual RB_score')
    plt.ylabel('Predicted RB_score')
    plt.legend()
    plt.grid(True)
    plt.show()
    return (
        X_test_density3,
        X_test_sequence3,
        X_test_slopeangle3,
        X_test_thickness3,
        X_train_density3,
        X_train_sequence3,
        X_train_slopeangle3,
        X_train_thickness3,
        combined3,
        history3,
        model3,
        mse3,
        rmse3,
        sequence_input3,
        slopeangle_input3,
        x,
        y,
        y_pred3,
        y_test3,
        y_train3,
        z,
    )


@app.cell
def __(
    Concatenate,
    Dense,
    Dropout,
    Input,
    LSTM,
    Model,
    df_dav_subset,
    df_swiss_subset,
    max_length,
    mean_squared_error,
    np,
    pad_sequences,
    plt,
):
    # Step 1: Prepare the data

    # Pad the layer_thickness and combined_density arrays for training
    X_train_thickness4 = pad_sequences(df_dav_subset['layers_above_wl'].tolist(), maxlen=max_length, padding='post', value=0.0)
    X_train_density4 = pad_sequences(df_dav_subset['density_above_wl'].tolist(), maxlen=max_length, padding='post', value=0.0)
    X_train_slopeangle4 = df_dav_subset['slopeangle'].values.reshape(-1, 1)  # Reshape for compatibility
    X_train_local_nowcast4 = df_dav_subset['localNowcast'].values.reshape(-1, 1)  # Reshape for compatibility

    X_test_thickness4 = pad_sequences(df_swiss_subset['layers_above_wl'].tolist(), maxlen=max_length, padding='post', value=0.0)
    X_test_density4 = pad_sequences(df_swiss_subset['density_above_wl'].tolist(), maxlen=max_length, padding='post', value=0.0)
    X_test_slopeangle4 = df_swiss_subset['slopeangle'].values.reshape(-1, 1)
    X_test_local_nowcast4 = df_swiss_subset['localNowcast'].values.reshape(-1, 1)

    # Stack the thickness and density arrays as two features
    X_train_sequence4 = np.stack((X_train_thickness4, X_train_density4), axis=-1)  # Shape will be (num_samples, max_length, 2)
    X_test_sequence4 = np.stack((X_test_thickness4, X_test_density4), axis=-1)

    y_train4 = df_dav_subset['RB_score'].values
    y_test4 = df_swiss_subset['RB_score'].values

    # Step 2: Define the LSTM model with additional inputs for `local_now_cast`

    # Input for sequence data (layer_thickness + combined_density)
    sequence_input4 = Input(shape=(X_train_sequence4.shape[1], X_train_sequence4.shape[2]))
    seq_lstm1 = LSTM(64, return_sequences=True)(sequence_input4)
    seq_dropout1 = Dropout(0.2)(seq_lstm1)
    seq_lstm2 = LSTM(32, return_sequences=False)(seq_dropout1)
    seq_dropout2 = Dropout(0.2)(seq_lstm2)

    # Input for slopeangle data (singular value)
    slopeangle_input4 = Input(shape=(1,))
    slope_dense4 = Dense(16, activation='relu')(slopeangle_input4)

    # Input for local_now_cast data (singular value)
    local_nowcast_input4 = Input(shape=(1,))
    local_dense4 = Dense(16, activation='relu')(local_nowcast_input4)

    # Combine both sequence, slopeangle, and local_now_cast inputs
    combined_inputs4 = Concatenate()([seq_dropout2, slope_dense4, local_dense4])

    # Output layer for regression
    output4 = Dense(1)(combined_inputs4)

    # Step 3: Create the model
    model4 = Model(inputs=[sequence_input4, slopeangle_input4, local_nowcast_input4], outputs=output4)

    # Compile the model
    model4.compile(optimizer='adam', loss='mean_squared_error')

    # Step 4: Train the model
    history4 = model4.fit([X_train_sequence4, X_train_slopeangle4, X_train_local_nowcast4], y_train4, epochs=50, batch_size=32, validation_split=0.2)

    # Step 5: Predict on the test data
    y_pred4 = model4.predict([X_test_sequence4, X_test_slopeangle4, X_test_local_nowcast4])

    # Step 6: Evaluate the model
    mse4 = mean_squared_error(y_test4, y_pred4)
    rmse4 = np.sqrt(mse4)

    print(f'Root Mean Squared Error (RMSE) for Model 4: {rmse4}')

    # Step 7: Compare performance - Visualization
    # Loss Graph: Show how loss decreases over epochs
    plt.figure(figsize=(10, 6))
    plt.plot(history4.history['loss'], label='Training Loss')
    plt.plot(history4.history['val_loss'], label='Validation Loss')
    plt.title('Training and Validation Loss over Epochs (Model 4: Thickness + Density + Slopeangle + LocalNowcast)')
    plt.xlabel('Epochs')
    plt.ylabel('Loss (Mean Squared Error)')
    plt.legend()
    plt.show()

    # Scatter plot of predicted vs actual values
    plt.figure(figsize=(8, 6))
    plt.scatter(y_test4, y_pred4, c='blue', marker='o', label='Predictions')
    plt.plot([y_test4.min(), y_test4.max()], [y_test4.min(), y_test4.max()], 'r--', lw=2)  # Diagonal line for perfect prediction
    plt.title('Predicted vs Actual RB_score (Model 4: Thickness + Density + Slopeangle + LocalNowcast)')
    plt.xlabel('Actual RB_score')
    plt.ylabel('Predicted RB_score')
    plt.legend()
    plt.grid(True)
    plt.show()
    return (
        X_test_density4,
        X_test_local_nowcast4,
        X_test_sequence4,
        X_test_slopeangle4,
        X_test_thickness4,
        X_train_density4,
        X_train_local_nowcast4,
        X_train_sequence4,
        X_train_slopeangle4,
        X_train_thickness4,
        combined_inputs4,
        history4,
        local_dense4,
        local_nowcast_input4,
        model4,
        mse4,
        output4,
        rmse4,
        seq_dropout1,
        seq_dropout2,
        seq_lstm1,
        seq_lstm2,
        sequence_input4,
        slope_dense4,
        slopeangle_input4,
        y_pred4,
        y_test4,
        y_train4,
    )


@app.cell
def __(
    Concatenate,
    Dense,
    Dropout,
    Input,
    LSTM,
    Model,
    df_dav_subset,
    df_swiss_subset,
    max_length,
    mean_squared_error,
    np,
    pad_sequences,
    plt,
):
    # Handle NaN values in wl_thickness
    mean_wl_thickness = df_dav_subset['wl_thickness'].mean()  # Calculate mean, ignoring NaN
    df_dav_subset['wl_thickness'].fillna(mean_wl_thickness, inplace=True)  # Fill NaNs with the mean
    df_swiss_subset['wl_thickness'].fillna(mean_wl_thickness, inplace=True)  # Fill NaNs in test set similarly

    # Pad the layer_thickness and combined_density arrays for training
    train_thickness5 = pad_sequences(df_dav_subset['layers_above_wl'].tolist(), maxlen=max_length, padding='post', value=0.0)
    train_density5 = pad_sequences(df_dav_subset['density_above_wl'].tolist(), maxlen=max_length, padding='post', value=0.0)
    train_wl_thickness5 = df_dav_subset['wl_thickness'].values.reshape(-1, 1)  # Reshape for compatibility
    train_slopeangle5 = df_dav_subset['slopeangle'].values.reshape(-1, 1)  # Reshape for compatibility
    train_local_nowcast5 = df_dav_subset['localNowcast'].values.reshape(-1, 1)  # Reshape for compatibility

    test_thickness5 = pad_sequences(df_swiss_subset['layers_above_wl'].tolist(), maxlen=max_length, padding='post', value=0.0)
    test_density5 = pad_sequences(df_swiss_subset['density_above_wl'].tolist(), maxlen=max_length, padding='post', value=0.0)
    test_wl_thickness5 = df_swiss_subset['wl_thickness'].values.reshape(-1, 1)  # Reshape for compatibility
    test_slopeangle5 = df_swiss_subset['slopeangle'].values.reshape(-1, 1)
    test_local_nowcast5 = df_swiss_subset['localNowcast'].values.reshape(-1, 1)

    # Stack the thickness and density arrays as two features
    train_sequence5 = np.stack((train_thickness5, train_density5), axis=-1)  # Shape will be (num_samples, max_length, 2)
    test_sequence5 = np.stack((test_thickness5, test_density5), axis=-1)

    y_train5 = df_dav_subset['RB_score'].values
    y_test5 = df_swiss_subset['RB_score'].values

    # Step 2: Define the LSTM model with additional inputs for `wl_thickness`

    # Input for sequence data (layer_thickness + combined_density)
    sequence_input5 = Input(shape=(train_sequence5.shape[1], train_sequence5.shape[2]))
    seq_lstm_layer1 = LSTM(64, return_sequences=True)(sequence_input5)
    seq_dropout_layer1 = Dropout(0.2)(seq_lstm_layer1)
    seq_lstm_layer2 = LSTM(32, return_sequences=False)(seq_dropout_layer1)
    seq_dropout_layer2 = Dropout(0.2)(seq_lstm_layer2)

    # Input for slopeangle data (singular value)
    slopeangle_input5 = Input(shape=(1,))
    slope_dense_layer5 = Dense(16, activation='relu')(slopeangle_input5)

    # Input for local_now_cast data (singular value)
    local_nowcast_input5 = Input(shape=(1,))
    local_dense_layer5 = Dense(16, activation='relu')(local_nowcast_input5)

    # Input for wl_thickness data (singular value, already filled NaNs)
    wl_thickness_input5 = Input(shape=(1,))  # Reshape is not needed here as it's a singular value
    wl_thickness_dense_layer5 = Dense(16, activation='relu')(wl_thickness_input5)

    # Combine both sequence, slopeangle, local_now_cast, and wl_thickness inputs
    combined_inputs5 = Concatenate()([seq_dropout_layer2, slope_dense_layer5, local_dense_layer5, wl_thickness_dense_layer5])

    # Output layer for regression
    output_layer5 = Dense(1)(combined_inputs5)

    # Step 3: Create the model
    model5 = Model(inputs=[sequence_input5, slopeangle_input5, local_nowcast_input5, wl_thickness_input5], outputs=output_layer5)

    # Compile the model
    model5.compile(optimizer='adam', loss='mean_squared_error')

    # Step 4: Train the model
    history5 = model5.fit([train_sequence5, train_slopeangle5, train_local_nowcast5, train_wl_thickness5], 
                           y_train5, epochs=50, batch_size=32, validation_split=0.2)

    # Step 5: Predict on the test data
    y_pred5 = model5.predict([test_sequence5, test_slopeangle5, test_local_nowcast5, test_wl_thickness5])

    # Step 6: Evaluate the model
    mse5 = mean_squared_error(y_test5, y_pred5)
    rmse5 = np.sqrt(mse5)

    print(f'Root Mean Squared Error (RMSE) for Model 5: {rmse5}')

    # Step 7: Compare performance - Visualization
    # Loss Graph: Show how loss decreases over epochs
    plt.figure(figsize=(10, 6))
    plt.plot(history5.history['loss'], label='Training Loss')
    plt.plot(history5.history['val_loss'], label='Validation Loss')
    plt.title('Training and Validation Loss over Epochs (Model 5: Thickness + Density + Slopeangle + LocalNowcast + WL Thickness)')
    plt.xlabel('Epochs')
    plt.ylabel('Loss (Mean Squared Error)')
    plt.legend()
    plt.show()

    # Scatter plot of predicted vs actual values
    plt.figure(figsize=(8, 6))
    plt.scatter(y_test5, y_pred5, c='blue', marker='o', label='Predictions')
    plt.plot([y_test5.min(), y_test5.max()], [y_test5.min(), y_test5.max()], 'r--', lw=2)  # Diagonal line for perfect prediction
    plt.title('Predicted vs Actual RB_score (Model 5: Thickness + Density + Slopeangle + LocalNowcast + WL Thickness)')
    plt.xlabel('Actual RB_score')
    plt.ylabel('Predicted RB_score')
    plt.legend()
    plt.grid(True)
    plt.show()
    return (
        combined_inputs5,
        history5,
        local_dense_layer5,
        local_nowcast_input5,
        mean_wl_thickness,
        model5,
        mse5,
        output_layer5,
        rmse5,
        seq_dropout_layer1,
        seq_dropout_layer2,
        seq_lstm_layer1,
        seq_lstm_layer2,
        sequence_input5,
        slope_dense_layer5,
        slopeangle_input5,
        test_density5,
        test_local_nowcast5,
        test_sequence5,
        test_slopeangle5,
        test_thickness5,
        test_wl_thickness5,
        train_density5,
        train_local_nowcast5,
        train_sequence5,
        train_slopeangle5,
        train_thickness5,
        train_wl_thickness5,
        wl_thickness_dense_layer5,
        wl_thickness_input5,
        y_pred5,
        y_test5,
        y_train5,
    )


@app.cell
def __(
    mean_squared_error,
    np,
    plt,
    rmse,
    test_density5,
    test_local_nowcast5,
    test_slopeangle5,
    test_thickness5,
    test_wl_thickness5,
    train_density5,
    train_local_nowcast5,
    train_slopeangle5,
    train_thickness5,
    train_wl_thickness5,
    y_pred,
    y_test5,
    y_train5,
):
    import xgboost as xgb

    # Assume train_thickness5, train_density5, etc., are prepared and preprocessed from your original data

    # Step 1: Data Preparation
    # Flattening the thickness and density sequences into tabular data
    train_data = np.concatenate([train_thickness5, train_density5, train_slopeangle5, train_local_nowcast5, train_wl_thickness5], axis=1)
    test_data = np.concatenate([test_thickness5, test_density5, test_slopeangle5, test_local_nowcast5, test_wl_thickness5], axis=1)

    # You can also split data if you want a new train/test split:
    # X_train, X_test, y_train, y_test = train_test_split(train_data, y_train5, test_size=0.2, random_state=42)

    # Step 2: Define and Train the XGBoost Model
    xgb_model = xgb.XGBRegressor(
        n_estimators=500,       # Number of trees
        learning_rate=0.05,     # Step size shrinkage
        max_depth=6,            # Maximum depth of each tree
        subsample=0.8,          # Row subsampling
        colsample_bytree=0.8,   # Feature subsampling
        random_state=42
    )

    # Fit the model on training data
    xgb_model.fit(train_data, y_train5)

    # Step 3: Predict and Evaluate
    y_pred_xg = xgb_model.predict(test_data)

    # Calculate RMSE
    mse_xg = mean_squared_error(y_test5, y_pred_xg)
    rmse_xg = np.sqrt(mse_xg)
    print(f'Root Mean Squared Error (RMSE): {rmse}')

    # Step 4: Plot Evaluation - Scatter plot of Predicted vs Actual Values
    plt.figure(figsize=(8, 6))
    plt.scatter(y_test5, y_pred, color='blue', label='Predictions', alpha=0.6)
    plt.plot([y_test5.min(), y_test5.max()], [y_test5.min(), y_test5.max()], 'r--', lw=2)  # Diagonal line for perfect predictions
    plt.title('XGBoost: Predicted vs Actual RB_score')
    plt.xlabel('Actual RB_score')
    plt.ylabel('Predicted RB_score')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Step 5: Plot Feature Importance
    return mse_xg, rmse_xg, test_data, train_data, xgb, xgb_model, y_pred_xg


@app.cell
def __(
    Adam,
    Dense,
    Dropout,
    Sequential,
    mean_squared_error,
    np,
    plt,
    test_density5,
    test_local_nowcast5,
    test_slopeangle5,
    test_thickness5,
    test_wl_thickness5,
    train_density5,
    train_local_nowcast5,
    train_slopeangle5,
    train_test_split,
    train_thickness5,
    train_wl_thickness5,
    y_test5,
    y_train5,
):
    from sklearn.preprocessing import StandardScaler


    # Step 1: Data Preparation
    train_data_fcnn = np.concatenate([train_thickness5, train_density5, train_slopeangle5, train_local_nowcast5, train_wl_thickness5], axis=1)
    test_data_fcnn = np.concatenate([test_thickness5, test_density5, test_slopeangle5, test_local_nowcast5, test_wl_thickness5], axis=1)

    # Split the training data into train and validation sets (80/20 split)
    X_train_fcnn, X_val_fcnn, y_train_fcnn, y_val_fcnn = train_test_split(train_data_fcnn, y_train5, test_size=0.2, random_state=42)

    # Optional: Standardize features (Neural Networks usually benefit from feature scaling)
    scaler_fcnn = StandardScaler()
    X_train_fcnn_scaled = scaler_fcnn.fit_transform(X_train_fcnn)
    X_val_fcnn_scaled = scaler_fcnn.transform(X_val_fcnn)
    test_data_fcnn_scaled = scaler_fcnn.transform(test_data_fcnn)

    # Step 2: Define the Neural Network Model
    model_fcnn = Sequential()

    # Input layer with a dense layer
    model_fcnn.add(Dense(128, input_dim=X_train_fcnn_scaled.shape[1], activation='relu'))
    model_fcnn.add(Dropout(0.3))  # Dropout layer to prevent overfitting

    # Hidden layers
    model_fcnn.add(Dense(64, activation='relu'))
    model_fcnn.add(Dropout(0.3))

    model_fcnn.add(Dense(32, activation='relu'))
    model_fcnn.add(Dropout(0.2))




    # Output layer for regression (no activation function)
    model_fcnn.add(Dense(1))

    # Compile the model
    model_fcnn.compile(optimizer=Adam(learning_rate=0.001), loss='mean_squared_error')

    # Step 3: Train the Neural Network
    history_fcnn = model_fcnn.fit(X_train_fcnn_scaled, y_train_fcnn, validation_data=(X_val_fcnn_scaled, y_val_fcnn),
                                  epochs=100, batch_size=16, verbose=1)

    # Step 4: Evaluate the model on test data
    y_pred_fcnn = model_fcnn.predict(test_data_fcnn_scaled)

    # Calculate RMSE for test set
    rmse_fcnn = np.sqrt(mean_squared_error(y_test5, y_pred_fcnn))
    print(f'Root Mean Squared Error (RMSE) on test data: {rmse_fcnn}')

    # Step 5: Plot the training and validation loss
    plt.figure(figsize=(10, 6))
    plt.plot(history_fcnn.history['loss'], label='Training Loss')
    plt.plot(history_fcnn.history['val_loss'], label='Validation Loss')
    plt.title('Training and Validation Loss over Epochs (FCNN)')
    plt.xlabel('Epochs')
    plt.ylabel('Loss (Mean Squared Error)')
    plt.legend()
    plt.show()

    # Step 6: Scatter plot of Predicted vs Actual values
    plt.figure(figsize=(8, 6))
    plt.scatter(y_test5, y_pred_fcnn, color='blue', label='Predicted', alpha=0.6)
    plt.plot([y_test5.min(), y_test5.max()], [y_test5.min(), y_test5.max()], 'r--', lw=2)
    plt.title('Predicted vs Actual RB_score (FCNN)')
    plt.xlabel('Actual RB_score')
    plt.ylabel('Predicted RB_score')
    plt.legend()
    plt.grid(True)
    plt.show()
    return (
        StandardScaler,
        X_train_fcnn,
        X_train_fcnn_scaled,
        X_val_fcnn,
        X_val_fcnn_scaled,
        history_fcnn,
        model_fcnn,
        rmse_fcnn,
        scaler_fcnn,
        test_data_fcnn,
        test_data_fcnn_scaled,
        train_data_fcnn,
        y_pred_fcnn,
        y_train_fcnn,
        y_val_fcnn,
    )


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
