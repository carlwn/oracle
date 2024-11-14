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
    df_manual_TRUE_scaled_TRUE = df_raw[df_raw['weak_layer_potential_exists'] == True]

    df_manual_TRUE_scaled_TRUE

    print(len(df_manual_TRUE_scaled_TRUE))
    # We have removed 99 layers where no weak layers exist
    return df_manual_TRUE_scaled_TRUE,


@app.cell
def __(df_manually_TRUE_scaled_TRUE, f):
    df_manually_TRUE_scaled_TRUE[['convergence_check','skier_weight', 'crack_length','nbr_iterations', 'elapsed_times', 'skier_weights', 'crack_lengths','starting_outside_stress_envelope', 'starting_outside_energy_envelope', 'critical_skier_weight', 'distance_to_energy_envelope', 'distance_to_stress_envelope', 'g_delta_diff','second_criterion_check']]= df_manually_TRUE_scaled_TRUE.apply(
        lambda row: f.apply_check_first_criterion(row, envelope='no_cap', scaling_factor=1, manually_overwritten_wl = True, scale_envelope_with_density=True), 
        axis=1, result_type='expand'
    )
    return


@app.cell
def __(df_manually_TRUE_scaled_TRUE, os, save_directory):
    filename_3 = 'applying_criterion_ALL_rows_manually_overwritten_wl_TRUE_scale_with_density_TRUE.csv'
    save_path_3 = os.path.join(save_directory, filename_3)

    df_manually_TRUE_scaled_TRUE.to_csv(save_path_3, index=False)
    return filename_3, save_path_3


@app.cell(disabled=True)
def __(df_manually_TRUE_scaled_FALSE, df_raw, f):
    df_manual_TRUE_scaled_FALSE = df_raw[df_raw['weak_layer_potential_exists'] == True]
    # Once again remove those samples where no weak layer exists

    df_manually_TRUE_scaled_FALSE[['convergence_check','skier_weight', 'crack_length','nbr_iterations', 'elapsed_times', 'skier_weights', 'crack_lengths','starting_outside_stress_envelope', 'starting_outside_energy_envelope', 'critical_skier_weight', 'distance_to_energy_envelope', 'distance_to_stress_envelope', 'g_delta_diff','second_criterion_check']] = df_manually_TRUE_scaled_FALSE.apply(
        lambda row: f.apply_check_first_criterion(row, envelope='no_cap', scaling_factor=1, manually_overwritten_wl = True, scale_envelope_with_density=False), 
        axis=1, result_type='expand'
    )
    return df_manual_TRUE_scaled_FALSE,


@app.cell
def __(df_manually_TRUE_scaled_FALSE, os, save_directory):
    filename_4 = 'applying_criterion_ALL_rows_manually_overwritten_wl_TRUE_scale_with_density_FALSE.csv'
    save_path_4 = os.path.join(save_directory, filename_4)

    # Ensure the directory exists (creates it if it doesn’t)
    os.makedirs(save_directory, exist_ok=True)

    # Save the DataFrame to the specified path
    df_manually_TRUE_scaled_FALSE.to_csv(save_path_4, index=False)
    return filename_4, save_path_4


@app.cell
def __(df_raw, f):
    df_manually_FALSE_scaled_FALSE = df_raw.copy()

    df_manually_FALSE_scaled_FALSE[['convergence_check','skier_weight', 'crack_length','nbr_iterations', 'elapsed_times', 'skier_weights', 'crack_lengths','starting_outside_stress_envelope', 'starting_outside_energy_envelope', 'critical_skier_weight', 'distance_to_energy_envelope', 'distance_to_stress_envelope', 'g_delta_diff','second_criterion_check']] = df_manually_FALSE_scaled_FALSE.apply(
        lambda row: f.apply_check_first_criterion(row, envelope='no_cap', scaling_factor=1, manually_overwritten_wl = False, scale_envelope_with_density=False), 
        axis=1, result_type='expand'
    )
    return df_manually_FALSE_scaled_FALSE,


@app.cell(disabled=True)
def __(df_manually_FALSE_scaled_FALSE, os, save_directory):
    filename_5 = 'applying_criterion_ALL_rows_manually_overwritten_wl_FALSE_scale_with_density_FALSE.csv'
    save_path_5 = os.path.join(save_directory, filename_5)

    # Ensure the directory exists (creates it if it doesn’t)
    os.makedirs(save_directory, exist_ok=True)

    # Save the DataFrame to the specified path
    df_manually_FALSE_scaled_FALSE.to_csv(save_path_5, index=False)
    return filename_5, save_path_5


@app.cell
def __(df_raw, f):
    df_manually_FALSE_scaled_TRUE = df_raw.copy()

    df_manually_FALSE_scaled_TRUE[['convergence_check','skier_weight', 'crack_length','nbr_iterations', 'elapsed_times', 'skier_weights', 'crack_lengths','starting_outside_stress_envelope', 'starting_outside_energy_envelope', 'critical_skier_weight', 'distance_to_energy_envelope', 'distance_to_stress_envelope', 'g_delta_diff','second_criterion_check']] = df_manually_FALSE_scaled_TRUE.apply(
        lambda row: f.apply_check_first_criterion(row, envelope='no_cap', scaling_factor=1, manually_overwritten_wl = False, scale_envelope_with_density=True), 
        axis=1, result_type='expand'
    )
    return df_manually_FALSE_scaled_TRUE,


@app.cell
def __(df_manually_FALSE_scaled_TRUE, os, save_directory):
    filename_6 = 'applying_criterion_ALL_rows_manually_overwritten_wl_FALSE_scale_with_density_TRUE.csv'
    save_path_6 = os.path.join(save_directory, filename_6)

    # Ensure the directory exists (creates it if it doesn’t)
    os.makedirs(save_directory, exist_ok=True)

    # Save the DataFrame to the specified path
    df_manually_FALSE_scaled_TRUE.to_csv(save_path_6, index=False)
    return filename_6, save_path_6


if __name__ == "__main__":
    app.run()
