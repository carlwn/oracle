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
    df_raw = pd.read_csv(load_path + 'df_raw.csv')

    df_raw
    return df_raw, load_path


@app.cell
def __(c_C, c_skier, inclination, ki, li, np):
    #### Fetching the exact tau and sigma
    length_summed = np.sum(li)
    x_continuous = np.linspace(0,length_summed,1000)

    solution_vector = c_skier.z(x_continuous,c_C,li,inclination,ki)
    return length_summed, solution_vector, x_continuous


@app.cell
def __(pd):
    # Define the path to the saved files
    load_path_2 = 'data/analysed_layers/'

    # Load the DataFrames from the CSV files - the updated version
    df_100st = pd.read_csv(load_path_2 + 'applying_criterion_ALL_rows_vZ.csv')
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
def __():
    # Four of these still converge to zero crack_length:
    # [22691, 43772, 49770, 57270]

    # 49770 Weirdly drops below although weight is increasing

    # 22691 Decreases weight and swings back outside the envelope
    return


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
        snow_profile_xx, 10, inclination_xx, segment_lengths_xx, segment_foundation_xx, crack_case='nocrack'
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
    plt.plot(new_env, f.failure_envelope_present_no_cap(new_env), label='No_cap envelope', color='green')
    plt.fill_between(new_env, f.failure_envelope_present_no_cap(new_env), color='lightgreen', alpha=0.1)

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


@app.cell
def __(df_100st, f, plt):
    # List of profID values to process - We now have convergence on twelve of these
    # profID_list = [12590, 13330, 13731, 14990, 15952, 20092, 22391, 22890, 43790, 44290, 44331, 44334, 44350, 45771, 46110, 54510, 58010]

    profID_list = [12590, 13330, 22890]
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
        df_profID_x[[f'convergence_check_{profID_x}', f'skier_weight_{profID_x}', f'crack_length_{profID_x}', f'nbr_iterations_{profID_x}', f'elapsed_times_{profID_x}', f'skier_weights_{profID_x}', f'crack_lengths_{profID_x}']] = df_profID_x.apply(f.apply_check_first_criterion, axis=1, result_type='expand')

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
def __():
    # No good explanation for the behavior above. There seems to be an issue of the switch between one uniform crack and two of them, separated by a non-cracked segment
    return


@app.cell
def __():
    # We get close but can't zone in on the solution, and 25 iterations go by. Maybe it needed more time...
    return


@app.cell
def __():
    # Custom profile
    myprofile = [[170, 100],  # (1) surface layer
                 [290,  40],  # (2) 2nd layer
                 [130, 130],  #  :
                 [150,  20],  #  :
                 [310,  70],  # (i) i-th layer
                 [280,  20],  #  :
                 [180, 100]]  # (N) last slab layer above weak layer
    return myprofile,


@app.cell
def __():
    myprofile_2 = [
                 [210,  70],  # (i) i-th layer
                 [200,  20],  #  :
                 [190, 100]]
    return myprofile_2,


@app.cell
def __(myprofile):
    # We define a new layered system not defined by any of the standard test-types

    # Input
    totallength = 100*(sum(layer[1] for layer in myprofile))                    # Total length (mm)
    cracklength = 0                         # Crack length (mm)
    inclination = 35                       # Slope inclination (°)
    skierweight = 120                      # Skier weigth (kg)
    return cracklength, inclination, skierweight, totallength


@app.cell
def __(C, f, inclination, myprofile, np, skierweight):
    # Playing around with ginc
    g_delta=1

    # We now create a cracked solution with cracklength
    c_skier, c_C, c_segments, c_x_cm, c_sigma_kPa, c_tau_kPa = f.create_skier_object(myprofile, g_delta, skierweight, inclination, crack_case='crack') 

    li = c_segments['li']
    mi = c_segments['mi']
    ki = c_segments['ki']
    print(c_segments)

    k0=[True, True, True, True]
    mode_I = 1000*c_skier.ginc(C0=C, C1=c_C, phi=inclination,**c_segments,k0=k0)

    print(mode_I)

    # VERY WELL

    # What are negative shear stresses?

    delta = f.energy_criterion(mode_I[1],mode_I[2])

    print(np.sqrt(1/delta))
    return (
        c_C,
        c_segments,
        c_sigma_kPa,
        c_skier,
        c_tau_kPa,
        c_x_cm,
        delta,
        g_delta,
        k0,
        ki,
        li,
        mi,
        mode_I,
    )


@app.cell
def __(delta, inclination, np, skier):
    forces = skier.get_skier_load(112,inclination)

    print(forces)
    new_force = np.sqrt(np.abs(forces)/delta)
    # We should scale this

    print(new_force)
    return forces, new_force


@app.cell
def __(c_C, c_segments, inclination, skier):
    # Trying to find energy release rate at crack tips
    energy_released_differential = skier.gdif(C=c_C, phi=inclination, **c_segments, unit='J/m^2')

    print(energy_released_differential)

    # Guess it is mode I, mode II and mode III

    # Or is it the total potential? Only pst implemented at the moment
    # total_pot = skier.total_potential(C=C, phi=inclination,L=totallength, **segments)

    # Just testing with valle envelope

    compression_toughness = 0.56
    n = 1/0.2
    energy_released_mode_I = energy_released_differential[1]

    shear_toughness = 0.79
    m=1/0.45
    energy_released_mode_II_III = energy_released_differential[2]

    energy_released_mode_II_III

    g_delta_1 = (energy_released_mode_I/compression_toughness)**n + (energy_released_mode_II_III / shear_toughness)**m 

    print(g_delta_1)
    return (
        compression_toughness,
        energy_released_differential,
        energy_released_mode_I,
        energy_released_mode_II_III,
        g_delta_1,
        m,
        n,
        shear_toughness,
    )


@app.cell
def __():
    return


@app.cell
def __(mpimg, plt):
    # Assuming the plot is saved as 'testing.png' (or some other image file)
    image_path = 'plots/cont.png'  # Adjust file extension if necessary

    # Load the image
    img = mpimg.imread(image_path)

    # Display the image
    plt.imshow(img)
    plt.axis('off')  # Optionally turn off axes
    plt.show()
    return image_path, img


@app.cell
def __(c_skier, xsl_skier, xwl_skier, z_skier):
    # Slab deflections (using x-coordinates of all segments, xsl)
    x_cm, w_um = c_skier.get_slab_deflection(x=xsl_skier, z=z_skier, unit='um')

    # Weak-layer shear stress (using only x-coordinates of bedded segments, xwl)
    x_cm, tau_kPa = c_skier.get_weaklayer_shearstress(x=xwl_skier, z=z_skier, unit='kPa')

    # Trying to find weak-layer compression
    x_cm, sigma_kPa = c_skier.get_weaklayer_normalstress(x=xwl_skier, z=z_skier, unit='kPa')
    return sigma_kPa, tau_kPa, w_um, x_cm


@app.cell
def __(f, myprofile):
    # Defining a skiers object
    q_crack_length = 0
    q_skier_weight = 200
    q_inclination = 45
    q_li= [24000, 0, 0, 24000]
    q_ki = [True, True, True, True]

    q_skier, q_C, q_segments, q_x_cm, q_sigma_kPa, q_tau_kPa = f.create_skier_object_v2(
        myprofile, q_crack_length, q_skier_weight, q_inclination, q_li, q_ki, crack_case='nocrack') 

    # Check if we are outside the stress envelope
    q_checker, q_dist_to_failure = f.is_outside_stress_envelope(q_sigma_kPa, -q_tau_kPa, envelope='no_cap')
    return (
        q_C,
        q_checker,
        q_crack_length,
        q_dist_to_failure,
        q_inclination,
        q_ki,
        q_li,
        q_segments,
        q_sigma_kPa,
        q_skier,
        q_skier_weight,
        q_tau_kPa,
        q_x_cm,
    )


@app.cell
def __():
    # Now lets understand when we are outside both
    return


@app.cell
def __(f, np, plt, q_sigma_kPa, q_tau_kPa, tau_kPa, x_cm):
    ## PLOTTING

    # Create a figure and axis
    fig, ax = plt.subplots()


    # Plot tau_kPa (shear stress) and sigma_kPa (normal stress) on the same y-axis
    ax.plot(x_cm, q_tau_kPa, label='Weak-layer Shear Stress (τ)', color='tab:blue')
    ax.plot(x_cm, q_sigma_kPa, label='Weak-layer Normal Stress (σ)', color='tab:red')

    failure_distance = np.zeros_like(tau_kPa)

    # HÄR BLIR DET FEL
    x_val = np.linspace(-3,0,100)

    for i, (tau, sigma) in enumerate(zip(-q_tau_kPa, q_sigma_kPa)):
        point_axis = np.linspace(-3,0,100)
        slope = tau/sigma
        intersect = f.find_intersect(point_axis,
                                   f.vectorized_point(point_axis, slope),
                                   f.failure_envelope_present_no_cap(point_axis)
                                  )
        failure_distance[i] = f.distance_to_failure(intersect,
                                                  sigma,
                                                  tau
                                                 )


    # Create a second y-axis that shares the same x-axis
    ax2 = ax.twinx()

    # Plot failure_distance on the second y-axis
    ax2.plot(x_cm, failure_distance, label='Distance to failure', color='tab:orange')

    # Set the y-axis range for failure_distance between 0 and 3
    ax2.set_ylim(0, 3)

    # Set the label for the second y-axis
    ax2.set_ylabel('Distance to failure', color='tab:orange')

    # Set color for the second y-axis labels to match the failure_distance plot
    ax2.tick_params(axis='y', labelcolor='tab:orange')

    # Add a title
    plt.title('Shear Stress (τ) and Normal Stress (σ) vs Distance to Failure')

    # Add legends for both y-axes
    ax.legend(loc='upper left')
    ax2.legend(loc='upper right')

    # Show the plot with tight layout to prevent overlap
    plt.tight_layout()
    plt.show()
    return (
        ax,
        ax2,
        failure_distance,
        fig,
        i,
        intersect,
        point_axis,
        sigma,
        slope,
        tau,
        x_val,
    )


@app.cell
def __(f, myprofile):
    # WEIRD:
    # For 150 we converge for all inclinations below 29 to 38, and all inclinations above 29 to 76, but 29 itself does not converge

    f.check_first_criterion_v2(snow_profile=myprofile, inclination=35, skier_weight=150, envelope='no_cap')

    # 42 wont converge

    # 48 all are outside: fix
    return


@app.cell
def __(f, myprofile, plt, skier):
    # Initialize lists to store results
    # Over 45 we get weird results right now

    inclinations = list(range(15, 36))  # Range of inclinations from 15 to 50
    crack_lengths = []
    skier_weights = []
    ERRs = []

    # Run the method for each inclination and save the results
    for inclination_var in inclinations:
        check_2nd, crack_length_2nd, skier_weight_2nd, c_skier_2nd, c_C_2nd, c_segments_2nd, c_x_cm_2nd, c_sigma_kPa_2nd, c_tau_kPa_2nd, iteration_count_2nd, elapsed_times_2nd, skier_weights_2nd, crack_lengths_2nd = f.check_first_criterion_v2(myprofile, inclination=inclination_var, skier_weight=150, envelope='no_cap')

        # True, crack_length, skier_weight, c_skier, c_C, c_segments, c_x_cm, c_sigma_kPa, c_tau_kPa, iteration_count, elapsed_times, skier_weights, crack_lengths

        # Calculating energy and ERR at crack tips
        energy_second_criterion = skier.gdif(C=c_C_2nd, phi=inclination_var, **c_segments_2nd, unit='J/m^2')
        ERR_2nd = f.energy_criterion(1000*energy_second_criterion[1], 1000*energy_second_criterion[2])
        # We get it in joule but need it in kPa to compare properly within our envelope --> must scale

        # This is new, and could be the reason we had such weird results previously

        # Store the results
        ERRs.append(ERR_2nd)
        crack_lengths.append(crack_length_2nd)
        skier_weights.append(skier_weight_2nd)
        print(f"\033[91m INCLINE converged: {str(inclination_var)}  \033[0m")

    # Create the plot
    fig_xx, axx1 = plt.subplots(figsize=(10, 6))

    # Plot crack length on the first y-axis
    axx1.scatter(skier_weights, crack_lengths, color='blue', label='Crack Length')
    for ii, inclination_var in enumerate(inclinations):
        axx1.text(skier_weights[ii], crack_lengths[ii], str(inclination_var), fontsize=9, ha='right')

    # Label for the first y-axis
    axx1.set_xlabel('Skier Weight (kg)')
    axx1.set_ylabel('Crack Length', color='blue')
    axx1.tick_params(axis='y', labelcolor='blue')
    axx1.grid(True)

    # Create a second y-axis
    axx2 = axx1.twinx()

    # Plot ERR on the second y-axis
    axx2.scatter(skier_weights, ERRs, color='red', label='ERR')
    for ii, inclination_var in enumerate(inclinations):
        axx2.text(skier_weights[ii], ERRs[ii], str(inclination_var), fontsize=9, ha='right', color='red')

    # Label for the second y-axis
    axx2.set_ylabel('ERR (J/m^2)', color='red')
    axx2.tick_params(axis='y', labelcolor='red')

    # Title of the plot
    plt.title('Crack Length and ERR vs Skier Weight with Inclinations')

    # Show the plot
    plt.show()
    return (
        ERR_2nd,
        ERRs,
        axx1,
        axx2,
        c_C_2nd,
        c_segments_2nd,
        c_sigma_kPa_2nd,
        c_skier_2nd,
        c_tau_kPa_2nd,
        c_x_cm_2nd,
        check_2nd,
        crack_length_2nd,
        crack_lengths,
        crack_lengths_2nd,
        elapsed_times_2nd,
        energy_second_criterion,
        fig_xx,
        ii,
        inclination_var,
        inclinations,
        iteration_count_2nd,
        skier_weight_2nd,
        skier_weights,
        skier_weights_2nd,
    )


@app.cell
def __(f, inclination, myprofile):
    ## UNDERSTANDING SKIERS command
    crackl = 0
    skierw = 150
    total_length = 100 * (sum(layer[1] for layer in myprofile))  # Total length (mm)
    lii = [total_length/2-5,5,5,-5+total_length/2]
    kii = [True, True, False, True]

    cr_lii = [total_length/2-5,5,5,total_length/2-5]
    cr_kii = [True, False, False, True]


    test_skier, test_C, test_segments, test_x_cm, test_sigma_kPa, test_tau_kPa = f.create_skier_object_v2(myprofile, crackl, skierw, inclination, lii, kii, crack_case='nocrack')

    cr_lii = [total_length/2-5,5,5,total_length/2-5]
    cr_kii = [True, False, False, True]
    cr_test_skier, cr_test_C, cr_test_segments, cr_test_x_cm, cr_test_sigma_kPa, cr_test_tau_kPa = f.create_skier_object_v2(myprofile, crackl, skierw, inclination, cr_lii, cr_kii, crack_case='crack')


    test_incr_energy = cr_test_skier.ginc(C0=test_C, C1=cr_test_C, phi=inclination,**cr_test_segments,k0=kii)

    print(test_incr_energy)
    return (
        cr_kii,
        cr_lii,
        cr_test_C,
        cr_test_segments,
        cr_test_sigma_kPa,
        cr_test_skier,
        cr_test_tau_kPa,
        cr_test_x_cm,
        crackl,
        kii,
        lii,
        skierw,
        test_C,
        test_incr_energy,
        test_segments,
        test_sigma_kPa,
        test_skier,
        test_tau_kPa,
        test_x_cm,
        total_length,
    )


@app.cell
def __(myprofile, weac):
    ###### DEFINE SOME SKIERS
    skiers = weac.Layered(system='skiers', layers=myprofile)


    li_x = [24000,     5,     5, 24000]
    ki_x = [True, False, False, True]
    mi_x = [0, 150, 0]
    k0_x = [True, True, True, True]



     # Calculate segments based on crack case: 'nocrack' or 'crack'
    segments_skiers = skiers.calc_segments(
                                #L=total_length, 
                                #a=crack_length, 
                                #m=skier_weight,  # Set current skier weight
                                li=li_x,           # Use the lengths of the segments
                                ki=ki_x,
                                mi=mi_x,
                                k0=k0_x                 # Use the boolean flags
                                )['nocrack']     # Switch between 'crack' or 'nocrack'

    print(segments_skiers)
    return k0_x, ki_x, li_x, mi_x, segments_skiers, skiers


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
