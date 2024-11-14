import marimo

__generated_with = "0.8.15"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import pandas as pd
    import numpy as np
    import os
    import ast
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg
    import app
    import time
    import weac
    import x_functions_pure as f
    return app, ast, f, mo, mpimg, np, os, pd, plt, time, weac


@app.cell
def __(pd):
    # Define the path to the saved files
    load_path = 'data/slf/mayer2022/'

    # Load the DataFrames from the CSV files
    df_raw = pd.read_csv(load_path + 'df_raw_weak_layers_exist.csv')

    df_raw
    return df_raw, load_path


@app.cell
def __(df_raw):
    # We should for clarity of results always prepare this dataset as only layers have weak_layers_exist should be tested
    df = df_raw[df_raw['weak_layer_potential_exists'] == True]

    df

    print(len(df))
    return df,


@app.cell
def __(df):
    # Pick ten random indices that we will test performance with
    random_rows = df.sample(n=15, random_state=38)
    return random_rows,


@app.cell
def __(random_rows):
    random_rows
    return


@app.cell(disabled=True)
def __(f, random_rows):
    random_rows[['convergence_check','skier_weight', 'crack_length','nbr_iterations', 'elapsed_times', 'skier_weights', 'crack_lengths','starting_outside_stress_envelope', 'starting_outside_energy_envelope', 'critical_skier_weight', 'distance_to_energy_envelope', 'distance_to_stress_envelope', 'g_delta_diff','second_criterion_check']]= random_rows.apply(
        lambda row: f.apply_check_first_criterion(row, envelope='no_cap', scaling_factor=1, manually_overwritten_wl = True, scale_envelope_with_density=True, testing_level = 200), 
        axis=1, result_type='expand'
    )
    return


@app.cell
def __(plt, random_rows):
    # Define variables for the plot
    x_axis = 'RB_score'  # X-axis
    y_axis = 'skier_weight'  # Y-axis
    descriptor = 'scatter_plot'  # Descriptor for the plot
    manual_status = 'TRUE'  # Replace with 'TRUE' or 'FALSE' based on the data
    rescaled_status = 'TRUE'  # Replace with 'TRUE' or 'FALSE' based on the data
    title = f"Coupled criteria for crack initiation: {x_axis} vs critical {y_axis} \n Manual: {manual_status}, Rescaled: {rescaled_status}"

    # Create the scatter plot
    plt.figure(figsize=(8, 6))

    # Plot all points in blue as the base layer
    plt.scatter(random_rows[x_axis], random_rows[y_axis], color='b', alpha=0.5, label='Within Envelopes')

    # Highlight points starting outside the stress envelope in orange
    plt.scatter(
        random_rows.loc[random_rows['starting_outside_stress_envelope'] == True, x_axis],
        random_rows.loc[random_rows['starting_outside_stress_envelope'] == True, y_axis],
        color='orange', label='Outside Stress Envelope'
    )

    # Highlight points starting outside the energy envelope in red
    plt.scatter(
        random_rows.loc[random_rows['starting_outside_energy_envelope'] == True, x_axis],
        random_rows.loc[random_rows['starting_outside_energy_envelope'] == True, y_axis],
        color='red', label='Outside Energy Envelope'
    )

    # Mark points where convergence_check is False with a red cross
    plt.scatter(
        random_rows.loc[random_rows['convergence_check'] == False, x_axis],
        random_rows.loc[random_rows['convergence_check'] == False, y_axis],
        color='red', marker='x', s=100, label='Convergence Check Failed'
    )

    # Annotate the 'g_delta_diff' values for each point in the plot
    for i in range(len(random_rows)):
        plt.annotate(
            f"{random_rows['g_delta_diff'].iloc[i]:.2f}",  # Format g_delta_diff to 2 decimal places
            (random_rows[x_axis].iloc[i], random_rows[y_axis].iloc[i]),
            textcoords="offset points",  # Position the text slightly offset from the point
            xytext=(5, 5),  # Offset for text (5, 5)
            ha='center',  # Horizontal alignment
            fontsize=8,  # Text size
            color='black',  # Text color
        )

    # Add labels, title, and legend
    plt.xlabel('RB Score')
    plt.ylabel("Critical " + y_axis.replace('_', ' ').title() + " (kg)")
    plt.title(title)
    plt.legend()

    # Save and show the plot
    plt.show()
    return (
        descriptor,
        i,
        manual_status,
        rescaled_status,
        title,
        x_axis,
        y_axis,
    )


@app.cell
def __(df_manually_FALSE_scaled_TRUE, df_raw, f, os):
    # Define the save directory (make sure this is the correct path where you want to save files)
    save_directory = 'data/slf/mayer2022/analysed_layers/TRUE_TRUE'
    # Ensure the directory exists (creates it if it doesn’t)
    os.makedirs(save_directory, exist_ok=True)

    # Define the list of columns you want to keep in the saved dataframe
    selected_columns = [
        'convergence_check', 'skier_weight', 'crack_length', 'nbr_iterations', 
        'elapsed_times', 'skier_weights', 'crack_lengths', 
        'starting_outside_stress_envelope', 'starting_outside_energy_envelope',
        'critical_skier_weight', 'distance_to_energy_envelope', 
        'distance_to_stress_envelope', 'g_delta_diff', 'second_criterion_check'
    ]

    # Loop through each testing level's results
    for testing_level in range(200, 1100, 100):  # Testing levels from 200 to 1000
        # Copy df_raw to create a new dataframe
        df_manually_TRUE_scaled_TRUE = df_raw.copy()

        # Apply the function to get the results, adding the results as new columns
        df_manually_TRUE_scaled_TRUE[selected_columns] = df_manually_TRUE_scaled_TRUE.apply(
            lambda row: f.apply_check_first_criterion(
                row,
                envelope='no_cap', 
                scaling_factor=1, 
                manually_overwritten_wl=True, 
                scale_envelope_with_density=True, 
                testing_level=testing_level
            ), 
            axis=1, 
            result_type='expand'
        )
        
        # Create the filename reflecting the testing level
        filename_6 = f'applying_criterion_ALL_rows_manually_overwritten_wl_FALSE_scale_with_density_TRUE_testing_level_{testing_level}.csv'
        
        # Define the full save path with the filename
        save_path_6 = os.path.join(save_directory, filename_6)

        # Save the DataFrame to the specified path
        df_manually_FALSE_scaled_TRUE.to_csv(save_path_6, index=False)

        print(f"Saved: {filename_6}")  # Confirmation that the file has been saved

    return (
        df_manually_TRUE_scaled_TRUE,
        filename_6,
        save_directory,
        save_path_6,
        selected_columns,
        testing_level,
    )


if __name__ == "__main__":
    app.run()
