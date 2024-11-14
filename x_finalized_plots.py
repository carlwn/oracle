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
    load_path_2 = 'data/analysed_layers/'

    # Load the DataFrames from the CSV files - the updated version
    df_100st = pd.read_csv(load_path_2 + 'applying_criterion_XXXrows_vZ.csv')
    return df_100st, load_path_2


@app.cell
def __(df_100st):
    # Now we have the copy so that we do not need to rerun everything, and can check the weird cases at once
    df_100st

    # Non-convergent - [12590, 13330, 22890]

    # Zero crack_length: - [22691, 43772, 49770, 57270]
    # 49770 Weirdly drops below although weight is increasing
    # 22691 Decreases weight and swings back outside the envelope
    return


@app.cell
def __(df_100st, f, plt):
    # List of profID values to process - We now have convergence on twelve of these
    # profID_list = [12590, 13330, 13731, 14990, 15952, 20092, 22391, 22890, 43790, 44290, 44331, 44334, 44350, 45771, 46110, 54510, 58010]

    profID_list = [22691, 43772, 49770, 57270]
    # Dictionary to store data for the final combined plot
    combined_data = {}
    convergence_summary = []  # List to store convergence information for each profID

    # Define colors for each profID
    colors = plt.cm.tab10(range(len(profID_list)))  # Use a colormap to generate unique colors for each profID

    # Loop through each profID and create a separate figure for each
    for idx, profID_x in enumerate(profID_list):
        # Filter the DataFrame for the current profID_x
        df_profID_x = df_100st.loc[df_100st['profID'] == profID_x, ['snow_profiles', 'slopeangle']]

        # Apply the criterion check and expand the result into new columns
        df_profID_x[[f'convergence_check_{profID_x}', f'skier_weight_{profID_x}', f'crack_length_{profID_x}', f'nbr_iterations_{profID_x}', f'elapsed_times_{profID_x}', f'skier_weights_{profID_x}', f'crack_lengths_{profID_x}']] = df_profID_x.apply(
        lambda row: f.apply_check_first_criterion(row, envelope='no_cap', scaling_factor=3), 
        axis=1, result_type='expand'
    )

        # Extract the relevant row for plotting
        row_zero_profID_x = df_profID_x.iloc[0]  # Assuming only one row per profID_x

        # Extract columns for plotting
        elapsed_times_x = row_zero_profID_x[f'elapsed_times_{profID_x}']
        skier_weights_x = row_zero_profID_x[f'skier_weights_{profID_x}']
        crack_lengths_x = row_zero_profID_x[f'crack_lengths_{profID_x}']

        # Check for convergence and record the result
        converged = row_zero_profID_x[f'convergence_check_{profID_x}']

        # Add crack_length and skier_weight to the convergence summary
        convergence_summary.append(f"profID {profID_x}: {'Converged' if converged else 'Did Not Converge'}, "
                                   f"Crack Length: {crack_lengths_x[-1]:.2f} mm, Skier Weight: {skier_weights_x[-1]:.2f} kg")

        # Store data for the combined plot
        combined_data[profID_x] = (elapsed_times_x, skier_weights_x, crack_lengths_x, colors[idx])

        # Create a new figure specifically for this profID_x
        fig_profID_x, ax1_profID_x = plt.subplots()

        # Plot elapsed_times_x vs skier_weights_x on the left y-axis with a solid line
        ax1_profID_x.set_xlabel('Elapsed Time (s)')
        ax1_profID_x.set_ylabel('Skier Weight (kg)', color='tab:blue')
        ax1_profID_x.plot(elapsed_times_x, skier_weights_x, color=colors[idx], linestyle='-', label=f'profID {profID_x}')
        ax1_profID_x.tick_params(axis='y', labelcolor='tab:blue')

        # Create another y-axis to plot crack lengths with unique axis variable, with a dashed line
        ax2_profID_x = ax1_profID_x.twinx()
        ax2_profID_x.set_ylabel('Crack Length (mm)', color='tab:red')
        ax2_profID_x.plot(elapsed_times_x, crack_lengths_x, color=colors[idx], linestyle='--')
        ax2_profID_x.tick_params(axis='y', labelcolor='tab:red')

        # Add title
        fig_profID_x.suptitle(f'Converging Loop for profID {profID_x}')

        # Show the plot for this profID_x (it will display each figure separately)
        plt.show()

    # Create a separate combined plot for all profIDs
    fig_combined, ax1_combined = plt.subplots()

    # Plot data for each profID_x in the combined plot
    for profID_x, (elapsed_times_x, skier_weights_x, crack_lengths_x, color) in combined_data.items():
        # Solid line for skier weight
        ax1_combined.plot(elapsed_times_x, skier_weights_x, color=color, linestyle='-', label=f'profID {profID_x}')

    # Set properties for the first y-axis (skier weight)
    ax1_combined.set_xlabel('Elapsed Time (s)')
    ax1_combined.set_ylabel('Skier Weight (kg)', color='tab:blue')
    ax1_combined.tick_params(axis='y', labelcolor='tab:blue')

    # Create second y-axis for crack lengths
    ax2_combined = ax1_combined.twinx()
    for profID_x, (elapsed_times_x, _, crack_lengths_x, color) in combined_data.items():
        # Dashed line for crack length
        ax2_combined.plot(elapsed_times_x, crack_lengths_x, color=color, linestyle='--')

    # Set properties for the second y-axis (crack length)
    ax2_combined.set_ylabel('Crack Length (mm)', color='tab:red')
    ax2_combined.tick_params(axis='y', labelcolor='tab:red')

    # Single legend indicating profIDs with unique colors
    fig_combined.legend(
        handles=[plt.Line2D([0], [0], color=color, label=f'profID {pid}', linestyle='-') for pid, color in zip(profID_list, colors)],
        loc='upper left',
        bbox_to_anchor=(1.05, 1),
        title="profID (Solid: Weight, Dashed: Crack Length)"
    )

    fig_combined.suptitle('Converging Loop for All profIDs')

    # Show the combined plot
    plt.show()

    # Print the convergence summary as plain text
    print("Convergence Summary for Each profID:")
    for summary in convergence_summary:
        print(summary)
    return (
        ax1_combined,
        ax1_profID_x,
        ax2_combined,
        ax2_profID_x,
        color,
        colors,
        combined_data,
        converged,
        convergence_summary,
        crack_lengths_x,
        df_profID_x,
        elapsed_times_x,
        fig_combined,
        fig_profID_x,
        idx,
        profID_list,
        profID_x,
        row_zero_profID_x,
        skier_weights_x,
        summary,
    )


@app.cell
def __(df_100st, f, np, plt):
    # Define a list of scaling factors
    # scaling_factors = np.arange(1.5, 3.0, 0.2)  # Adjust as needed
    scaling_factors = [1.5]
    # Filter the DataFrame for profID 10198
    df_10198 = df_100st.loc[df_100st['profID'] == 10198, ['snow_profiles', 'slopeangle']]

    # Prepare to collect results for each scaling factor
    results = []
    summary_of_convergence = []  # List to store convergence information

    # Loop through each scaling factor
    for scaling_factor in scaling_factors:
        print(f"Running with scaling_factor: {scaling_factor}")

        # Apply the criterion check and expand the result into new columns
        df_10198[['convergence_check', 'skier_weight', 'crack_length', 'nbr_iterations', 
                   'elapsed_times', 'skier_weights', 'crack_lengths']] = df_10198.apply(
            lambda row: f.apply_check_first_criterion(row, envelope='no_cap', scaling_factor=scaling_factor), 
            axis=1, result_type='expand'
        )

        # Extract the relevant row for plotting
        row_zero_10198 = df_10198.iloc[0]  # Assuming only one row for profID 10198

        # Collect the results with the scaling factor
        results.append({
            'scaling_factor': scaling_factor,
            'elapsed_times': row_zero_10198['elapsed_times'],
            'skier_weights': row_zero_10198['skier_weights'],
            'crack_lengths': row_zero_10198['crack_lengths'],
            'convergence_check': row_zero_10198['convergence_check']
        })

        # Summarize convergence for each scaling factor
        is_converged = row_zero_10198['convergence_check']
        summary_of_convergence.append(f"Scaling Factor {scaling_factor}: {'Converged' if is_converged else 'Did Not Converge'}")

    # Create a new figure for plotting
    fig, ax1 = plt.subplots()

    # Define colors for each scaling factor using a colormap
    plot_colors = plt.cm.tab10(np.linspace(0, 1, len(results)))  # Get distinct colors

    # Plot each scaling factor's results
    for scaling_factor_index, result in enumerate(results):
        scaling_factor = result['scaling_factor']
        plot_color = plot_colors[scaling_factor_index]  # Get the corresponding color for the current scaling factor

        # Plot skier weight with a solid line
        ax1.plot(result['elapsed_times'], result['skier_weights'], 
                 label=f'Skier Weight (SF: {scaling_factor})', 
                 color=plot_color, linestyle='-', alpha=0.7)

        # Create another y-axis for crack lengths
        ax2 = ax1.twinx()
        ax2.set_ylabel('Crack Length (mm)', color='tab:red')

        # Plot crack length with a dashed line
        ax2.plot(result['elapsed_times'], result['crack_lengths'], 
                 label=f'Crack Length (SF: {scaling_factor})', 
                 color=plot_color, linestyle='--', alpha=0.7)

    # Set labels for the axes
    ax1.set_xlabel('Elapsed Time (s)')
    ax1.set_ylabel('Skier Weight (kg)', color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    # Add titles and legends
    fig.suptitle('Converging Loop for profID 10198')
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    # Show the plot
    plt.show()

    # Print the convergence summary
    print("Convergence Summary:")
    for summary_X in summary_of_convergence:
        print(summary_X)
    return (
        ax1,
        ax2,
        df_10198,
        fig,
        is_converged,
        plot_color,
        plot_colors,
        result,
        results,
        row_zero_10198,
        scaling_factor,
        scaling_factor_index,
        scaling_factors,
        summary_X,
        summary_of_convergence,
    )


@app.cell
def __():
    # No good explanation for the behavior above. There seems to be an issue of the switch between one uniform crack and two of them, separated by a non-cracked segment
    return


@app.cell
def __(df_100st, f, plt):
    # Filter the DataFrame for profID 13330
    profID = 13330

    df_13330 = df_100st.loc[df_100st['profID'] == 13330, ['snow_profiles', 'slopeangle']]

    # Apply the criterion check and expand the result into new columns
    df_13330[['convergence_check', 'skier_weight', 'crack_length', 'nbr_iterations', 'elapsed_times', 'skier_weights', 'crack_lengths']] = df_13330.apply(
        lambda row: f.apply_check_first_criterion(row, envelope='no_cap', scaling_factor=3), 
        axis=1, result_type='expand'
    )

    # Extract the relevant row for plotting
    row_zero = df_13330.iloc[0]  # Since we only have one row for profID 13330

    # Extract columns for plotting
    elapsed_times_13330 = row_zero['elapsed_times']
    skier_weights_13330 = row_zero['skier_weights']
    crack_lengths_13330 = row_zero['crack_lengths']

    # Create a new figure with a unique name
    fig_13330, ax1_13330 = plt.subplots()

    # Plot elapsed_times vs skier_weights on the left y-axis
    ax1_13330.set_xlabel('Elapsed Time (s)')
    ax1_13330.set_ylabel('Skier Weight (kg)', color='tab:blue')
    ax1_13330.plot(elapsed_times_13330, skier_weights_13330, color='tab:blue', label='Skier Weight')
    ax1_13330.tick_params(axis='y', labelcolor='tab:blue')

    # Create another y-axis to plot crack lengths with unique axis variable
    ax2_13330 = ax1_13330.twinx()
    ax2_13330.set_ylabel('Crack Length (mm)', color='tab:red')
    ax2_13330.plot(elapsed_times_13330, crack_lengths_13330, color='tab:red', label='Crack Length')
    ax2_13330.tick_params(axis='y', labelcolor='tab:red')

    # Add titles and legends
    fig_13330.suptitle(f'Converging Loop for profID {profID}')  # Updated title to reflect convergence
    ax1_13330.legend(loc='upper left')
    ax2_13330.legend(loc='upper right')

    # Show the plot
    plt.show()
    return (
        ax1_13330,
        ax2_13330,
        crack_lengths_13330,
        df_13330,
        elapsed_times_13330,
        fig_13330,
        profID,
        row_zero,
        skier_weights_13330,
    )


@app.cell
def __(df_100st, f, plt):
    # Checking another converged sample
    # Filter the DataFrame for profID 10167
    df_10167 = df_100st.loc[df_100st['profID'] == 10167, ['snow_profiles', 'slopeangle']]

    # Apply the criterixin check and expand the result into new columns
    df_10167[['convergence_check', 'skier_weight', 'crack_length', 'nbr_iterations', 'elapsed_times', 'skier_weights', 'crack_lengths']] = df_10167.apply(
        lambda row: f.apply_check_first_criterion(row, envelope='no_cap', scaling_factor=3), 
        axis=1, result_type='expand'
    )

    # Extract the relevant row for plotting
    row_zero_10167 = df_10167.iloc[0]  # Since we only have one row for profID 10167

    # Extract columns for plotting
    elapsed_times_10167 = row_zero_10167['elapsed_times']
    skier_weights_10167 = row_zero_10167['skier_weights']
    crack_lengths_10167 = row_zero_10167['crack_lengths']

    # Create a new figure with a unique name
    fig_10167, ax1_10167 = plt.subplots()

    # Plot elapsed_times vs skier_weights on the left y-axis
    ax1_10167.set_xlabel('Elapsed Time (s)')
    ax1_10167.set_ylabel('Skier Weight (kg)', color='tab:blue')
    ax1_10167.plot(elapsed_times_10167, skier_weights_10167, color='tab:blue', label='Skier Weight')
    ax1_10167.tick_params(axis='y', labelcolor='tab:blue')

    # Create another y-axis to plot crack lengths with unique axis variable
    ax2_10167 = ax1_10167.twinx()
    ax2_10167.set_ylabel('Crack Length (mm)', color='tab:red')
    ax2_10167.plot(elapsed_times_10167, crack_lengths_10167, color='tab:red', label='Crack Length')
    ax2_10167.tick_params(axis='y', labelcolor='tab:red')

    # Add titles and legends
    fig_10167.suptitle(f'Converging Loop for profID {10167}')  # Updated title to reflect convergence
    ax1_10167.legend(loc='upper left')
    ax2_10167.legend(loc='upper right')

    # Show the plot
    plt.show()
    return (
        ax1_10167,
        ax2_10167,
        crack_lengths_10167,
        df_10167,
        elapsed_times_10167,
        fig_10167,
        row_zero_10167,
        skier_weights_10167,
    )


@app.cell
def __(df_100st, f, plt):
    # Convergence in only six iterations: 

    # Filter the DataFrame for profID 17410
    df_17410 = df_100st.loc[df_100st['profID'] == 17410, ['snow_profiles', 'slopeangle']]

    # Apply the criterion check and expand the result into new columns
    df_17410[['convergence_check', 'skier_weight', 'crack_length', 'nbr_iterations', 'elapsed_times', 'skier_weights', 'crack_lengths']] = df_17410.apply(
        lambda row: f.apply_check_first_criterion(row, envelope='no_cap', scaling_factor=3), 
        axis=1, result_type='expand'
    )


    # Extract the relevant row for plotting
    row_zero_17410 = df_17410.iloc[0]  # Since we only have one row for profID 17410

    # Extract columns for plotting
    elapsed_times_17410 = row_zero_17410['elapsed_times']
    skier_weights_17410 = row_zero_17410['skier_weights']
    crack_lengths_17410 = row_zero_17410['crack_lengths']

    # Create a new figure with a unique name
    fig_17410, ax1_17410 = plt.subplots()

    # Plot elapsed_times vs skier_weights on the left y-axis
    ax1_17410.set_xlabel('Elapsed Time (s)')
    ax1_17410.set_ylabel('Skier Weight (kg)', color='tab:blue')
    ax1_17410.plot(elapsed_times_17410, skier_weights_17410, color='tab:blue', label='Skier Weight')
    ax1_17410.tick_params(axis='y', labelcolor='tab:blue')

    # Create another y-axis to plot crack lengths with unique axis variable
    ax2_17410 = ax1_17410.twinx()
    ax2_17410.set_ylabel('Crack Length (mm)', color='tab:red')
    ax2_17410.plot(elapsed_times_17410, crack_lengths_17410, color='tab:red', label='Crack Length')
    ax2_17410.tick_params(axis='y', labelcolor='tab:red')

    # Add titles and legends
    fig_17410.suptitle(f'Converging Loop for profID {17410}')  # Updated title to reflect convergence
    ax1_17410.legend(loc='upper left')
    ax2_17410.legend(loc='upper right')

    # Show the plot
    plt.show()
    return (
        ax1_17410,
        ax2_17410,
        crack_lengths_17410,
        df_17410,
        elapsed_times_17410,
        fig_17410,
        row_zero_17410,
        skier_weights_17410,
    )


@app.cell
def __(df_100st, f, plt):
    # This used to be non-convergent, but it is fixed by using the dampened version

    # Filter the DataFrame for profID 15952
    df_15952 = df_100st.loc[df_100st['profID'] == 15952, ['snow_profiles', 'slopeangle']]

    # Apply the criterion check and expand the result into new columns
    df_15952[['convergence_check', 'skier_weight', 'crack_length', 'nbr_iterations', 'elapsed_times', 'skier_weights', 'crack_lengths']] = df_15952.apply(
        lambda row: f.apply_check_first_criterion(row, envelope='no_cap', scaling_factor=3), 
        axis=1, result_type='expand'
    )


    # Extract the relevant row for plotting
    row_zero_15952 = df_15952.iloc[0]  # Since we only have one row for profID 15952

    # Extract columns for plotting
    elapsed_times_15952 = row_zero_15952['elapsed_times']
    skier_weights_15952 = row_zero_15952['skier_weights']
    crack_lengths_15952 = row_zero_15952['crack_lengths']

    # Create a new figure with a unique name
    fig_15952, ax1_15952 = plt.subplots()

    # Plot elapsed_times vs skier_weights on the left y-axis
    ax1_15952.set_xlabel('Elapsed Time (s)')
    ax1_15952.set_ylabel('Skier Weight (kg)', color='tab:blue')
    ax1_15952.plot(elapsed_times_15952, skier_weights_15952, color='tab:blue', label='Skier Weight')
    ax1_15952.tick_params(axis='y', labelcolor='tab:blue')

    # Create another y-axis to plot crack lengths with unique axis variable
    ax2_15952 = ax1_15952.twinx()
    ax2_15952.set_ylabel('Crack Length (mm)', color='tab:red')
    ax2_15952.plot(elapsed_times_15952, crack_lengths_15952, color='tab:red', label='Crack Length')
    ax2_15952.tick_params(axis='y', labelcolor='tab:red')

    # Add titles and legends
    fig_15952.suptitle(f'Converging Loop for profID {15952}')  # Updated title to reflect convergence
    ax1_15952.legend(loc='upper left')
    ax2_15952.legend(loc='upper right')

    # Show the plot
    plt.show()
    return (
        ax1_15952,
        ax2_15952,
        crack_lengths_15952,
        df_15952,
        elapsed_times_15952,
        fig_15952,
        row_zero_15952,
        skier_weights_15952,
    )


@app.cell
def __(ast, df_100st, f, np, plt):
    # Displaying a variable that does is outside the envelope in all points
    df_test = df_100st.loc[df_100st['profID'] == 44334, ['snow_profiles', 'slopeangle']]

    # Assuming df_test is your DataFrame
    inclination_xx = df_test['slopeangle'].iloc[0]  # Get the first row's slope angle
    snow_profile_xx = ast.literal_eval(df_test['snow_profiles'].iloc[0])  # Get the first row's snow profile and evaluate it

    # Reverse the snow profile
    snow_profile_reversed = snow_profile_xx[::-1]

    crack_length_xx = 0
    total_length_xx = 100 * (sum(layer[1] for layer in snow_profile_reversed))  # Total length in mm
    # total_length_xx = 100 * 100 * 10  # Uncomment if using a fixed length of 100 meters in mm

    support_boolean_xx = [True, True, True, True]  # Support boolean for uncracked solution
    segment_lengths_xx = [total_length_xx / 2, 0, 0, total_length_xx / 2]  # Support boolean for uncracked solution
    segment_foundation_xx = [True, True, True, True]  # Length of segments with foundations as specified by segment_foundation

    # Assuming skier_weight_xx and inclination_xx are defined elsewhere in your code
    skier_obj_xx, C_value_xx, segments_data_xx, x_center_of_mass_xx, sigma_kPa_values_xx, tau_kPa_values_xx = f.create_skier_object_v2(
        snow_profile_xx,  10, inclination_xx, segment_lengths_xx, segment_foundation_xx, crack_case='nocrack'
    )

    # Check if we are outside the stress envelope at any point
    stress_checker_xx, distance_to_failure_xx = f.is_outside_stress_envelope(sigma_kPa_values_xx, -tau_kPa_values_xx, envelope="no_cap")

    # Assuming that skier_obj_xx, C_value_xx, segments_data_xx, x_center_of_mass_xx, sigma_kPa_values_xx, tau_kPa_values_xx 
    # have been returned from create_skier_object_v2() as previously defined

    # Create the plot
    plt.figure(figsize=(10, 6))

    # Plot tau (shear stress) vs x_center_of_mass
    plt.plot(x_center_of_mass_xx, tau_kPa_values_xx, label=r'$\tau$ (shear stress)', color='r', linestyle='-', marker='o')

    # Plot sigma (normal stress) vs x_center_of_mass
    plt.plot(x_center_of_mass_xx, sigma_kPa_values_xx, label=r'$\sigma$ (normal stress)', color='b', linestyle='-', marker='x')

    # Adding labels and title
    plt.xlabel('X (Center of Mass, cm)', fontsize=12)
    plt.ylabel('Stress (kPa)', fontsize=12)
    plt.title('Stress vs. Position (Center of Mass)', fontsize=14)

    # Adding grid and legend
    plt.grid(True)
    plt.legend()

    # Show the plot
    plt.tight_layout()
    plt.show()

    # Create the plot
    plt.figure(figsize=(10, 6))

    # Plot tau (shear stress) vs x_center_of_mass
    plt.scatter(sigma_kPa_values_xx, -tau_kPa_values_xx, label=r'$\tau$ (shear stress) vs $\sigma$ (normal stress)', color='r', marker='o')


    new_env = np.linspace(-3,3,1000)
    plt.plot(new_env, f.failure_envelope_present_no_cap(new_env, scaling_factor=3), label='No_cap envelope', color='green')
    plt.fill_between(new_env, f.failure_envelope_present_no_cap(new_env, scaling_factor=3), color='lightgreen', alpha=0.1)

    # Adding labels and title
    plt.xlabel(r'$\sigma$ (normal stress)', fontsize=12)
    plt.ylabel(r'$\tau$ (shear stress)', fontsize=12)
    plt.title('Stress vs. Position (Center of Mass)', fontsize=14)

    # Adding grid and legend
    plt.grid(True)
    plt.legend()

    # Show the plot
    plt.tight_layout()
    plt.show()
    return (
        C_value_xx,
        crack_length_xx,
        df_test,
        distance_to_failure_xx,
        inclination_xx,
        new_env,
        segment_foundation_xx,
        segment_lengths_xx,
        segments_data_xx,
        sigma_kPa_values_xx,
        skier_obj_xx,
        snow_profile_reversed,
        snow_profile_xx,
        stress_checker_xx,
        support_boolean_xx,
        tau_kPa_values_xx,
        total_length_xx,
        x_center_of_mass_xx,
    )


if __name__ == "__main__":
    app.run()
