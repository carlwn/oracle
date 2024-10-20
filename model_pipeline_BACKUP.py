import marimo

__generated_with = "0.8.15"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import pandas as pd
    import numpy as np
    import os

    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg


    import app
    return app, mo, mpimg, np, os, pd, plt


@app.cell
def __():
    # This does not work for now: will pin it and just use a dummy layer from the demo of weac
    return


@app.cell
def __(mo):
    mo.md(
        """
        # Questions

        1. What does calc_segements do? Calculate all things under eigensystem? What difference does crack vs no-crack do? Does nocrack let us analyse stress criterion first?

        2. What are the free constants we are solving for in assemble_and_solve?

        3. The properties of the weak layer should have a significant impact - how do we account for this? Believe we should specify when defining calc-segments but does not make a difference to outcome. Also: should different weak-layers be with different Young-Modulus and Poisson ratio. Standard of 0.25, 0.25 works for which types? 

        4. What means by rasterizing a solution? Know from images it is vector to pixels, but do not understand quite here?

        5. How do we connect the shear and compresive stresses as depicted by the model to the stress criterion envelope? Failure outside boundaries? Sign of force?

        6. What snowpack data should we chang
        """
    )
    return


@app.cell
def __():
    # Testing out the weac model as defined by intro
    import weac
    return weac,


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
def __(myprofile, weac):
    # We define a new layered system not defined by any of the standard test-types
    skier = weac.Layered(system='skier', layers=myprofile)
    skier.set_foundation_properties(t=10,update=True)

    # Input
    totallength = 100*(sum(layer[1] for layer in myprofile))                    # Total length (mm)
    cracklength = 0                         # Crack length (mm)
    inclination = 35                       # Slope inclination (°)
    skierweight = 120                      # Skier weigth (kg)

    # 20/300 gets us past but increasing inclination decreases the g_delta
    # Also interesting that we increase by
    # We try out a few different steps of accessing values
    segments = skier.calc_segments(
        L=totallength, a=cracklength, m=skierweight)['nocrack']

    C = skier.assemble_and_solve(phi=inclination, **segments)

    xsl_skier, z_skier, xwl_skier = skier.rasterize_solution(C=C, phi=inclination, **segments)

    # Visualize deformations as a contour plot
    weac.plot.deformed(skier, xsl=xsl_skier, xwl=xwl_skier, z=z_skier,
                       phi=inclination, window=200, scale=200,
                       field='principal')

    # Plot slab displacements (using x-coordinates of all segments, xsl)
    weac.plot.displacements(skier, x=xsl_skier, z=z_skier, **segments)

    # Plot weak-layer stresses (using only x-coordinates of bedded segments, xwl)
    weac.plot.stresses(skier, x=xwl_skier, z=z_skier, **segments)
    return (
        C,
        cracklength,
        inclination,
        segments,
        skier,
        skierweight,
        totallength,
        xsl_skier,
        xwl_skier,
        z_skier,
    )


@app.cell
def __():
    return


@app.cell
def __():
    return


@app.cell
def __():
    return


@app.cell
def __(
    C,
    create_skier_object,
    energy_criterion,
    inclination,
    myprofile,
    np,
    skierweight,
):
    # Playing around with ginc
    g_delta=1

    # We now create a cracked solution with cracklength
    c_skier, c_C, c_segments, c_x_cm, c_sigma_kPa, c_tau_kPa = create_skier_object(myprofile, g_delta, skierweight, inclination, crack_case='crack') 

    li = c_segments['li']
    mi = c_segments['mi']
    ki = c_segments['ki']
    print(c_segments)

    k0=[True, True, True, True]
    mode_I = 1000*c_skier.ginc(C0=C, C1=c_C, phi=inclination,**c_segments,k0=k0)

    print(mode_I)

    # VERY WELL

    # What are negative shear stresses?

    delta = energy_criterion(mode_I[1],mode_I[2])

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
def __(create_skier_object_v2, is_outside_stress_envelope, myprofile):
    # Defining a skiers object
    q_crack_length = 0
    q_skier_weight = 200
    q_inclination = 45
    q_li= [24000, 0, 0, 24000]
    q_ki = [True, True, True, True]

    q_skier, q_C, q_segments, q_x_cm, q_sigma_kPa, q_tau_kPa = create_skier_object_v2(
        myprofile, q_crack_length, q_skier_weight, q_inclination, q_li, q_ki, crack_case='nocrack') 

    # Check if we are outside the stress envelope
    q_checker, q_dist_to_failure = is_outside_stress_envelope(q_sigma_kPa, -q_tau_kPa, envelope='no_cap')
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
def __(
    failure_envelope,
    failure_envelope_present_no_cap,
    failure_envelope_smooth,
    find_intersect,
    np,
    plt,
    q_sigma_kPa,
    q_tau_kPa,
    vectorized_point,
    x_cm,
):
    # Define the points
    sigma_reiweger = [-3,-2.75, 0.25]
    tau_reiweger = [0,1, 0]

    # Create the plot
    fig_3, ax_3 = plt.subplots()

    # Normalize x_cm to map it to a colormap
    norm = plt.Normalize(vmin=x_cm.min(), vmax=x_cm.max())
    cmap = plt.cm.viridis  # You can choose other colormaps like 'plasma', 'coolwarm', etc.

    # Create a scatter plot where color represents the value of x_cm
    scatter = ax_3.scatter(q_sigma_kPa, -q_tau_kPa, c=x_cm, cmap=cmap, label='weac')

    # Add a color bar to show the mapping of colors to x_cm values
    cbar = plt.colorbar(scatter, ax=ax_3)

    # Plot the approximate Reiweger curve
    ax_3.plot(sigma_reiweger, tau_reiweger, label='Reiweger', color='blue')


    # Vector to point
    tau_value= 1
    sigma_value = -2.74
    slope_vector = tau_value/sigma_value
    sigma_axis = np.linspace(sigma_value,0,100)

    # Create separate x_values to plot the entire
    x_values = np.linspace(min(sigma_value,-3),0,100)

    # Have two functions
    vect_point = vectorized_point(sigma_axis,slope_vector)
    envelope = failure_envelope(sigma_axis)

    # Find the intersect of these two
    intersect_sigma = find_intersect(sigma_axis,vect_point,envelope)
    intersect_tau = vectorized_point(intersect_sigma,slope_vector)

    # print(intersect_sigma)

    new_env = np.linspace(-3,3,1000)

    # Plotting vectorized point, failure envelope and intersect
    # ax_3.plot(sigma_axis, vect_point, label='Vector to point', color='orange') 
    # ax_3.plot(x_values, failure_envelope(x_values), label='Alternate envelope', color='red')
    # ax_3.plot(intersect_sigma, intersect_tau, label='Vector to point', color='orange',marker='o')
    ax_3.plot(new_env, failure_envelope_present_no_cap(new_env), label='No-cap envelope', color='green')
    ax_3.fill_between(new_env, failure_envelope_present_no_cap(new_env), color='lightgreen', alpha=0.1)
    ax_3.plot(new_env, failure_envelope_smooth(new_env), label='Smooth envelope', color='yellow')


    # Set axis limits and labels
    ax_3.set_xlim([-4, 1])
    ax_3.set_ylim([0, 1.5])
    ax_3.set_xlabel('σ [kPa]')
    ax_3.set_ylabel('τ [kPa]')

    # Add gridlines
    ax_3.grid(True)

    # Add legend
    ax_3.legend()

    # Add title
    plt.title('Weak-layer Failure Envelopes with Experimental Data')

    # Show the plot
    plt.tight_layout()
    plt.show()
    return (
        ax_3,
        cbar,
        cmap,
        envelope,
        fig_3,
        intersect_sigma,
        intersect_tau,
        new_env,
        norm,
        scatter,
        sigma_axis,
        sigma_reiweger,
        sigma_value,
        slope_vector,
        tau_reiweger,
        tau_value,
        vect_point,
        x_values,
    )


@app.cell
def __():
    # Now lets understand when we are outside both
    return


@app.cell
def __(
    distance_to_failure,
    failure_envelope_present_no_cap,
    find_intersect,
    np,
    plt,
    q_sigma_kPa,
    q_tau_kPa,
    tau_kPa,
    vectorized_point,
    x_cm,
):
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
        intersect = find_intersect(point_axis,
                                   vectorized_point(point_axis, slope),
                                   failure_envelope_present_no_cap(point_axis)
                                  )
        failure_distance[i] = distance_to_failure(intersect,
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
def __(check_first_criterion, myprofile):
    # WEIRD:
    # For 150 we converge for all inclinations below 29 to 38, and all inclinations above 29 to 76, but 29 itself does not converge

    check_first_criterion(snow_profile=myprofile, inclination=43, skier_weight=150, envelope='no_cap')

    # 42 wont converge

    # 48 all are outside: fix
    return


@app.cell
def __(create_skier_object_v3, is_outside_stress_envelope, np):
    def find_new_crack_length_v3(snow_profile, skier_weight, inclination, li, ki, envelope='reiweger'):
        crack_length = 0
        skier, C, segments, x_cm, sigma_kPa, tau_kPa = create_skier_object_v3(
            snow_profile, crack_length, skier_weight, inclination, li, ki, crack_case='nocrack') 

        # Check if we are outside the stress envelope
        checker, dist_to_failure = is_outside_stress_envelope(sigma_kPa, -tau_kPa, envelope=envelope) 

        # Flattening arrays
        x_cm_array = np.array(x_cm).flatten()
        dist_to_fail_array = np.array(dist_to_failure).flatten()
        checker_array = np.array(checker).flatten()

        print("Distance to Failure Array:", dist_to_fail_array)
        print("X cm Array:", x_cm_array)

        # Create a foundation object
        foundations = ~checker_array

        # Finding switch indices
        switches = np.where(np.diff(np.sign(dist_to_fail_array - 0.999)))[0]
        print("Switches Indices:", switches)

        # Ensure switches + 1 are within bounds
        if switches.size > 0:
            ki = [foundations[0]]
            ki.extend(foundations[switches + 1])
        else:
            ki = np.array([])  # If there are no switches, ki would be empty


        print("Foundation States at Switches:", ki)

        # Constructing segment boundaries
        segment_boundaries = [x_cm_array[0]]  # Start with the first point
        segment_boundaries.extend(x_cm_array[switches + 1])  # Append the points where switches occur
        segment_boundaries.append(x_cm_array[-1])  # End with the last point

        print("Segment Boundaries:", segment_boundaries)

        # Calculate lengths between segment boundaries
        li = np.diff(segment_boundaries)
        print("Lengths between segment boundaries (li):", li)

        # Calculate new crack length
        new_crack_length = sum(length for length, foundation in zip(li, ki) if not foundation)

        return new_crack_length, li, ki
    return find_new_crack_length_v3,


@app.cell
def __(create_skier_object_v2, is_outside_stress_envelope, np):
    def find_new_crack_length_v2(snow_profile, skier_weight, inclination, li, ki, envelope='reiweger'):

        crack_length = 0

        skier, C, segments, x_cm, sigma_kPa, tau_kPa = create_skier_object_v2(
            snow_profile, crack_length, skier_weight, inclination, li, ki, crack_case='nocrack') 

        # Check if we are outside the stress envelope
        checker, dist_to_failure = is_outside_stress_envelope(sigma_kPa, -tau_kPa, envelope=envelope) 

        # Flattening arrays
        x_cm_array = np.array(10*x_cm).flatten()
        dist_to_fail_array = np.array(dist_to_failure).flatten()
        checker_array = np.array(checker).flatten()

        print("Distance to Failure Array:", dist_to_fail_array)
        #print("X cm Array:", x_cm_array)

        # Create a foundation object
        foundations = ~checker_array

        # Finding switch indices
        switches = np.where(np.diff(np.sign(dist_to_fail_array - 0.999)))[0]
        #print("Switches Indices:", switches)

        # Ensure switches + 1 are within bounds
        if switches.size > 0:
            ki = [foundations[0]]
            ki.extend(foundations[switches + 1])
        else:
            ki = np.array([])  # If there are no switches, ki would be empty

        #print("Foundation States at Switches:", ki)

        # Constructing segment boundaries
        segment_boundaries = [x_cm_array[0]]  # Start with the first point
        segment_boundaries.extend(x_cm_array[switches + 1])  # Append the points where switches occur
        segment_boundaries.append(x_cm_array[-1])  # End with the last point

        #print("Segment Boundaries:", segment_boundaries)

        # Calculate lengths between segment boundaries
        li = np.diff(segment_boundaries)
       # print("Lengths between segment boundaries (li):", li)

        # Calculate total length of li
        total_length = np.sum(li)
        midpoint = total_length / 2
        #print("Total Length of li:", total_length)
        #print("Midpoint of Total Length:", midpoint)

        # Locate the segment that brings the cumulative sum to the midpoint
        cumulative_length = np.cumsum(li)
        #print("Cumulative Lengths of li:", cumulative_length)

        # Find the index of the segment containing the midpoint
        segment_index = np.where(cumulative_length >= midpoint)[0][0]  # First segment to exceed midpoint
        #print("Segment Index at Midpoint:", segment_index)

        # If the segment index is valid, split that segment
        if segment_index < len(li):
            segment_start = cumulative_length[segment_index - 1] if segment_index > 0 else 0
            segment_to_split_length = li[segment_index]

            # Calculate the length to split
            split_length = midpoint - segment_start

            # Adjust the lengths
            li = np.insert(li, segment_index, [split_length, segment_to_split_length - split_length])
            li = np.delete(li, segment_index + 2)  # Remove the original segment that was split

            # Split the ki array accordingly
            # Duplicate the foundation state of the original segment
            ki = np.insert(ki, segment_index, ki[segment_index])  # Insert the existing boolean value twice
            print("New ki after splitting:", ki)

            print("New Lengths after Splitting Segment:", li)

        # Calculate new crack length
        new_crack_length = sum(length for length, foundation in zip(li, ki) if not foundation)

        return new_crack_length, li, ki
    return find_new_crack_length_v2,


@app.cell(disabled=True)
def __(
    ERR_2nd,
    c_segments_2nd,
    check_first_criterion,
    energy_criterion,
    myprofile,
    skier,
):
    # NOW WE CHECK THE SECOND CRITERION
    xcheck_2nd, xcrack_length_2nd, xskier_weight_2nd, xc_skier_2nd, xc_C_2nd, xc_segments_2nd, xc_x_cm_2nd, xc_sigma_kPa_2nd, xc_tau_kPa_2nd = check_first_criterion(snow_profile=myprofile, inclination=30, skier_weight=150, envelope='new')

    energy_2nd = skier.gdif(C=xc_C_2nd, phi=30, **c_segments_2nd, unit='J/m^2')
    print(energy_2nd)

    xERR_2nd = energy_criterion(energy_2nd[1],energy_2nd[2])

    print(ERR_2nd)

    # Do we apply the energy criterion here as well? Will we ever not fulfill the energy criterion here if we have done it as part of step#1
    return (
        energy_2nd,
        xERR_2nd,
        xc_C_2nd,
        xc_segments_2nd,
        xc_sigma_kPa_2nd,
        xc_skier_2nd,
        xc_tau_kPa_2nd,
        xc_x_cm_2nd,
        xcheck_2nd,
        xcrack_length_2nd,
        xskier_weight_2nd,
    )


@app.cell
def __(check_first_criterion, energy_criterion, myprofile, plt, skier):
    # Initialize lists to store results
    # Over 45 we get weird results right now

    inclinations = list(range(15, 35))  # Range of inclinations from 15 to 50
    crack_lengths = []
    skier_weights = []
    ERRs = []

    # Run the method for each inclination and save the results
    for inclination_var in inclinations:
        check_2nd, crack_length_2nd, skier_weight_2nd, c_skier_2nd, c_C_2nd, c_segments_2nd, c_x_cm_2nd, c_sigma_kPa_2nd, c_tau_kPa_2nd = check_first_criterion(myprofile, inclination=inclination_var, skier_weight=150, envelope='no_cap')

        # Calculating energy and ERR at crack tips
        energy_second_criterion = skier.gdif(C=c_C_2nd, phi=inclination_var, **c_segments_2nd, unit='J/m^2')
        
        # THIS IS THE ONLY CHANGE I HAVE DONE
        ERR_2nd = energy_criterion(energy_second_criterion[1]/1000, energy_second_criterion[2]/1000)

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
        energy_second_criterion,
        fig_xx,
        ii,
        inclination_var,
        inclinations,
        skier_weight_2nd,
        skier_weights,
    )


@app.cell
def __(np):
    def energy_criterion(G_sigma, G_tau):
        # Valle envelope

        compression_toughness = 0.56
        n = 1/0.2 
        shear_toughness = 0.79
        m=1/0.45

        g_delta = ( np.abs(G_sigma) / compression_toughness)**n + ( np.abs(G_tau) / shear_toughness)**m 

        return g_delta
    return energy_criterion,


@app.cell
def __():
    def two_stage_stress_criterion():
        return 0
    return two_stage_stress_criterion,


@app.cell
def __(create_skier_object_v2, inclination, myprofile):
    ## UNDERSTANDING SKIERS command
    crackl = 0
    skierw = 150
    total_length = 100 * (sum(layer[1] for layer in myprofile))  # Total length (mm)
    lii = [total_length/2,0,0,total_length/2]
    kii = [True, True, True, True]


    test_skier, test_C, test_segments, test_x_cm, test_sigma_kPa, test_tau_kPa = create_skier_object_v2(myprofile, crackl, skierw, inclination, lii, kii, crack_case='nocrack')

    cr_lii = [total_length/2-5,5,5,total_length/2-5]
    cr_kii = [True, False, False, True]
    cr_test_skier, cr_test_C, cr_test_segments, cr_test_x_cm, cr_test_sigma_kPa, cr_test_tau_kPa = create_skier_object_v2(myprofile, crackl, skierw, inclination, cr_lii, cr_kii, crack_case='crack')


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


@app.cell
def __(np, weac):
    def create_skier_object_v2(snow_profile, crack_length, skier_weight, inclination, li_x, ki_x, crack_case='nocrack'):

        # Define a skier object

        # Changing to 'skiers'
        skier = weac.Layered(system='skiers', layers=snow_profile)

        n = len(ki_x)-1
        # median_index = (n - 1) // 2  # Always gives the lower middle for both odd and even lengths

        # Calculate the total sum of the array
        mi_x = np.zeros(n)

        # Initialize cumulative sum and find median index of where to apply skier force
        cumulative_sum = 0
        median_index = -1  # Initialize median_index

        total_length = sum(li_x)
        half_sum = total_length / 2  # Half of the total sum (median point)

        for i, value in enumerate(li_x):
            cumulative_sum += value
            if cumulative_sum >= half_sum:
                median_index = i
                break

        mi_x[median_index] = skier_weight  # Assign skier_weight to the median index

        # We also need to feed k0 for uncracked solution= which is 
        k0 = np.full(len(ki_x), True)

        # Assuming 100x snow profile thickness
        # total_length = 100 * (sum(layer[1] for layer in snow_profile))  # Total length (mm)

        # Calculate segments based on crack case: 'nocrack' or 'crack'
        segments = skier.calc_segments(
                                #L=total_length, 
                                #a=crack_length, 
                                # m=skier_weight,  # Set current skier weight
                                li=li_x,           # Use the lengths of the segments
                                ki=ki_x,
                                mi=mi_x,
                                k0=k0                 # Use the boolean flags
                                )[crack_case]     # Switch between 'crack' or 'nocrack'

        print(f"SEGMENT SOLUTIONS?: {segments}")

        # Solve and rasterize the solution
        C = skier.assemble_and_solve(phi=inclination, **segments)
        xsl_skier, z_skier, xwl_skier = skier.rasterize_solution(C=C, phi=(inclination), **segments)

        # Calculate compressions and shear stress
        x_cm, tau_kPa = skier.get_weaklayer_shearstress(x=xwl_skier, z=z_skier, unit='kPa')
        x_cm, sigma_kPa = skier.get_weaklayer_normalstress(x=xwl_skier, z=z_skier, unit='kPa')

        return skier, C, segments, x_cm, sigma_kPa, tau_kPa
    return create_skier_object_v2,


@app.cell
def __(
    create_skier_object_v2,
    energy_criterion,
    find_minimum_force,
    find_new_crack_length_v2,
    is_outside_stress_envelope,
    np,
):
    def check_first_criterion(snow_profile, inclination, skier_weight, envelope='reiweger'):

        # Assuming nocrack case to begin with and create a skier-object
        crack_length = 0
        length = 100 * (sum(layer[1] for layer in snow_profile))  # Total length (mm)
        k0=[True, True, True, True]       # Support boolean for uncracked solution
        li=[length/2,0,0,length/2]        # Support boolean for uncracked solution
        ki= [True, True, True, True]      # Length of segments with foundations as specified by ki

        skier, C, segments, x_cm, sigma_kPa, tau_kPa = create_skier_object_v2(snow_profile, crack_length, skier_weight, inclination, li, ki, crack_case='nocrack')

        # For the initial skier object, check if we are outside the stress envelope at any point
        checker, dist_to_failure  = is_outside_stress_envelope(sigma_kPa, -tau_kPa, envelope=envelope)

        # ToDo: Would be good to see how near we are the limit - the envelope has an error margin

        if checker.any():

            # Find the weight associated with minimum critical force to initialize our algorithm (BASE CASE)
            skier_weight, *_ = find_minimum_force(snow_profile, inclination, envelope=envelope)

            # Initialize variables for algorithm
            init_crack_length=1                    # Initial crack length
            err = 1000                             # Error margin
            li = li=[length/2-init_crack_length/2, init_crack_length/2, init_crack_length/2, length/2-init_crack_length/2] 
            ki = [True,False,False,True]

            while np.abs(err)>0.002:
                # Create the base_case with correct number of segments
                #ki_no_cr = np.full(len(ki), True)
                #crack_length_no_cr = 0

                skier, C, segments, x_cm, sigma_kPa, tau_kPa = create_skier_object_v2(snow_profile, crack_length, skier_weight, inclination, li, ki, crack_case='nocrack')

                # Solving a cracked solution
                c_skier, c_C, c_segments, c_x_cm, c_sigma_kPa, c_tau_kPa = create_skier_object_v2(snow_profile, crack_length, skier_weight, inclination, li, ki, crack_case='crack')

                print(f" Solution: {c_segments}") 

                # Section to keep track of distance to failure 
                checker_2, dist_to_failure_2  = is_outside_stress_envelope(c_sigma_kPa, -c_tau_kPa, envelope=envelope)
                mask = ~np.isnan(dist_to_failure_2)           # Cracked solution gives NaN values for forces in cracked points

                filtered_checker = checker_2[mask]
                filtered_dist_to_failure = dist_to_failure_2[mask]

                print(f" START OF ITERATION: cracklength: {crack_length} mm, Skier Weight: {skier_weight} kg, Max Distance to Failure: {np.max(filtered_dist_to_failure)}")

                # The uncracked solution will have True for all values
                k0 = np.full(len(ki), True)


                # Calculate incremental energy released compared to (BASE CASE) solution above
                incr_energy = c_skier.ginc(C0=C, C1=c_C, phi=inclination, **c_segments, k0=k0)

                # Evaluate energy enveloope (scaling by 1000 to convert kJ to J)
                g_delta = energy_criterion(1000*incr_energy[1], 1000*incr_energy[2])

                # Q: do we get energy in J or kJ?

                # For any g_delta below 1, we are not outside the energy envelope and must increase the force
                current_normal_force, current_tangential_force = c_skier.get_skier_load(skier_weight,inclination)
                current_gravitational_force = np.sqrt(current_normal_force**2 + current_tangential_force**2)
                updated_gravitational_force = (g_delta**(-1/10)) * (current_gravitational_force)

                # Updating error margin
                err = np.abs(updated_gravitational_force - current_gravitational_force)/updated_gravitational_force 

                # For errors > margin we scale skier weight skier weight according to g_delta calculated above, and find new crack length
                if(np.abs(err)>0.002):
                    new_skier_weight = skier_weight * (updated_gravitational_force/current_gravitational_force)
                    skier_weight = new_skier_weight

                    # For the updated skier force, we find all points where the weak layer is overloaded and use this as 
                    # the crack length in the next iteration (with li and ki specifying how the crack is positioned in the weak layer)
                    new_crack_length, li, ki = find_new_crack_length_v2(snow_profile, skier_weight, inclination, li, ki, envelope=envelope)
                    crack_length = new_crack_length
                    print(f" END OF ITERATION: g_delta: {g_delta} J/m^2, Skier Weight: {skier_weight} kg, cracklength: {crack_length} mm,")


            # End of loop, i.e. convergence --> print solution
            print(f" CONVERGENCE: cracklength: {crack_length} mm, Critical Skier Weight: {skier_weight} kg, Distance to energy envelope: {g_delta} J/m^2, Max Distance to Stress Envelope: {np.max(filtered_dist_to_failure)}")

            return True, crack_length, skier_weight, c_skier, c_C, c_segments, c_x_cm, c_sigma_kPa, c_tau_kPa

        else:
            # We do not fulfill the stress criterion in any point, and will therefore not be able to trigger an avalanche
            return False
    return check_first_criterion,


@app.cell
def __():
    return


@app.cell
def __(create_skier_object, is_outside_stress_envelope, np):
    def find_minimum_force(snow_profile, inclination, envelope='reiweger'):
        # Initial parameters
        crack_length = 0
        crack_case = 'nocrack'
        skier_weight = 1  # Starting weight of skier

        #ToDo: make this use v2

        # Create a skier object with no weight and check if it is already outside the envelope
        skier, C, segments, x_cm, sigma_kPa, tau_kPa = create_skier_object(snow_profile, crack_length, skier_weight, inclination, crack_case='nocrack') 

        # Check if we are already outside the stress envelope
        checker, dist_to_failure = is_outside_stress_envelope(sigma_kPa, -tau_kPa, envelope='new')

        # Increment skier weight by 1kg until at least one point is outside the envelope
        while not checker.any():  # While no point is outside the envelope
            # skier_weight += 1  # Increase skier weight by 1kg

            # Recreate the skier object with the updated weight
            skier, C, segments, x_cm, sigma_kPa, tau_kPa = create_skier_object(snow_profile, crack_length, skier_weight, inclination, crack_case='nocrack')

            # Check again if we are outside the envelope with the new weight
            checker, dist_to_failure = is_outside_stress_envelope(sigma_kPa, -tau_kPa, envelope=envelope)

            print(f"Skier Weight: {skier_weight} kg, Max Distance to Failure: {np.max(dist_to_failure)}")

            if not checker.any():
                skier_weight = skier_weight * 1/np.max(dist_to_failure)

        # Once the loop exits, it means we have found the critical skier weight
        return skier_weight, skier, C, segments, x_cm, sigma_kPa, tau_kPa, dist_to_failure
    return find_minimum_force,


@app.cell
def __(weac):
    # Used for initialization of algorithm to find critical force
    def create_skier_object(snow_profile, crack_length, skier_weight, inclination, crack_case='nocrack'):
        # Define a skier object
        skier = weac.Layered(system='skier', layers=snow_profile)

        # Assuming 100x snow profile thickness
        total_length = 100 * (sum(layer[1] for layer in snow_profile))  # Total length (mm)

        # Calculate segments based on crack case: 'nocrack' or 'crack'
        segments = skier.calc_segments(
                                L=total_length, 
                                a=crack_length, 
                                m=skier_weight  # Set current skier weight
                                )[crack_case]  # Switch between 'crack' or 'nocrack'

        # Solve and rasterize solution
        C = skier.assemble_and_solve(phi=inclination, **segments)
        xsl_skier, z_skier, xwl_skier = skier.rasterize_solution(C=C, phi=inclination, **segments)

        # Calculate compressions and shear stress
        x_cm, tau_kPa = skier.get_weaklayer_shearstress(x=xwl_skier, z=z_skier, unit='kPa')
        x_cm, sigma_kPa = skier.get_weaklayer_normalstress(x=xwl_skier, z=z_skier, unit='kPa')

        return skier, C, segments, x_cm, sigma_kPa, tau_kPa
    return create_skier_object,


@app.cell
def __(
    failure_envelope_new,
    failure_envelope_present_no_cap,
    failure_envelope_reiweger,
    failure_envelope_smooth,
    np,
    vectorized_point_new,
):
    def find_intersect_2(sigma, tau, envelope="reiweger"):

        # Ensure sigma and tau are arrays to handle vectors
        sigma = np.asarray(sigma)
        tau = np.asarray(tau)

        # Initialize a list to store the intersections for each pair of sigma and tau
        all_intersects = []

        # Loop over each sigma and tau pair
        for s, t in zip(sigma, tau):
            # Generate sigma values for the current sigma
            sigma_values = np.linspace(s, 3, 100)
            # Calculate the vectorized point for the current tau and sigma
            vector = vectorized_point_new(sigma_values, t / s)

            # Different cases for different envelopes
            if envelope == "reiweger":
                envelope_function = failure_envelope_reiweger(sigma_values)
            elif envelope == "new":
                envelope_function = failure_envelope_new(sigma_values)
            elif envelope == "smooth":
                envelope_function = failure_envelope_smooth(sigma_values)
            elif envelope == "no_cap":
                envelope_function = failure_envelope_present_no_cap(sigma_values)
            else:
                raise ValueError("Unsupported type of envelope")

            # Compute intersections where the vector crosses the envelope
            idx = np.argwhere(
                np.diff(np.sign(vector - envelope_function))
            ).flatten()

            # If intersections are found, extract the corresponding sigma values
            if idx.size > 0:
                intersect_sigma = sigma_values[
                    idx
                ]  # Extract sigma values at intersection indices
                all_intersects.append(
                    intersect_sigma
                )  # Add found intersections to the list
            else:
                all_intersects.append(
                    np.array([])
                )  # Append an empty array for no intersections

        # Return the list of intersections, ensuring each input pair has a corresponding output
        return all_intersects
    return find_intersect_2,


@app.cell
def __(find_intersect_2, np, vectorized_point_new):
    def distance_to_failure_2(sigma, tau, envelope='reiweger'):
        # Ensure sigma and tau are arrays to handle vectors
        sigma = np.asarray(sigma)
        tau = np.asarray(tau)

        slope = tau / sigma
        vector_abs = np.sqrt(sigma**2 + tau**2)

        # Find intersections with the envelope - first column is the actual point, second column is where the intersection happened
        intersect_sigma_list = find_intersect_2(sigma, tau, envelope=envelope)

        distance_factors = []

        # Iterate through each intersection for each (sigma, tau) pair
        for i, (intersect_sigma, current_slope) in enumerate(zip(intersect_sigma_list, slope)):

            if intersect_sigma.size > 0:  # We have found an intersect with sigma_value specified at second column
                # Compute total distance to the envelope for each intersection
                total_distance_to_envelope = np.sqrt(intersect_sigma[1]**2 + vectorized_point_new(intersect_sigma[1], slope[i])**2)
                # Calculate distance factor for this intersection
                distance_factor = vector_abs[i] / total_distance_to_envelope

                # Would also like to keep the points
                distance_factors.append(distance_factor)

            else: # We have not found an intersect, and are thus inside the envelope
                x_values = np.linspace(-3, 1, 100) # We must extrapolate the slope outside the envelope
                intersect = find_intersect_2(x_values, vectorized_point_new(x_values, current_slope), envelope=envelope)
                intersect_tau = vectorized_point_new(intersect[0][1], current_slope)
                total_distance_to_envelope = np.sqrt(intersect[0][1]**2 + intersect_tau**2)
                distance_factor = vector_abs[i] / total_distance_to_envelope

                distance_factors.append(distance_factor)

        return distance_factors  # Return all distance factors for each pair
    return distance_to_failure_2,


@app.cell
def __():
    # At this point, we would like to know if the very first stress criterion is fulfilled
    # dist_to_fail, check = is_outside_stress_envelope(sigma_kPa, tau_kPa, envelope='reiweger')
    return


@app.cell
def __(distance_to_failure, intersect_sigma, np, sigma_value, tau_value):
    test = distance_to_failure(intersect_sigma, sigma_value, tau_value)
    print(test)
    # len(intersect_sigma)

    np.any(intersect_sigma)
    return test,


@app.cell(hide_code=True)
def __(
    distance_to_failure,
    failure_envelope,
    find_intersect,
    np,
    plt,
    point_axis,
    skier,
    vectorized_point,
    weac,
):
    # Trying to set up testing environment
    # Custom profile
    _myprofile = [[170, 100],  # (1) surface layer
                 [190,  40],  # (2) 2nd layer
                 [230, 130],  #  :
                 [250,  20],  #  :
                 [210,  70],  # (i) i-th layer
                 [380,  20],  #  :
                 [280, 100]]  # (N) last slab layer above weak layer


    # We define a new layered system not defined by any of the standard test-types
    _skier = weac.Layered(system='skier', layers=_myprofile)

    # Changing the height of the weakness-layer
    _skier.set_foundation_properties(t=10,update=True)

    # Input of fixed variables
    _totallength = 10*(sum(layer[1] for layer in _myprofile))                    # Total length (mm)
    _cracklength = 0                         # Crack length (mm)
    _inclination = 25                       # Slope inclination (°)


    _compression_toughness = 0.56
    _n = 1/0.2
    _shear_toughness = 0.79
    _m=1/0.45

    # The variable we are flexing
    # skierweight = 80                       # Skier weigth (kg)

    # Create an empty list to store results for each skier weight
    results = []

    # Loop through skier weight values from 1 to 150 (0 is excluded as per the range)
    for _skierweight in np.arange(1, 201, 20):  # Increments by 1, adjust as needed

        _segments = skier.calc_segments(
                            L=_totallength, 
                            a=_cracklength, 
                            m=_skierweight  # Set current skier weight
                            )['crack']

        # Solve and rasterize solution
        _C = _skier.assemble_and_solve(phi=_inclination, **_segments)
        _xsl_skier, _z_skier, _xwl_skier = skier.rasterize_solution(C=_C, phi=_inclination, **_segments)

        # Calculate compressions and shear stress
        _x_cm, _tau_kPa = _skier.get_weaklayer_shearstress(x=_xwl_skier, z=_z_skier, unit='kPa')
        _x_cm, _sigma_kPa = _skier.get_weaklayer_normalstress(x=_xwl_skier, z=_z_skier, unit='kPa')

        # Calculate distance to failure
        _failure_distance = np.zeros_like(_tau_kPa)
        _point_axis = np.linspace(-3,0,100)

        for j, (_tau, _sigma) in enumerate(zip(-_tau_kPa, _sigma_kPa)):

            # Calculate intersect between envelope and vector of point-mass
            _intersect = find_intersect(point_axis,
                                       vectorized_point(_point_axis, _tau/_sigma),
                                       failure_envelope(_point_axis)
                                      )
            # Calculate 
            _failure_distance[j] = distance_to_failure(_intersect,
                                                      _sigma,
                                                      _tau
                                                     )


        _failure_distance_intensity = np.sum(_failure_distance[_failure_distance > 1]-1)


        _energy_released_differential = skier.gdif(C=_C, phi=_inclination, **_segments, unit='J/m^2')


        # Guess it is mode I, mode II and mode III

        # Or is it the total potential? Only pst implemented at the moment
        # total_pot = skier.total_potential(C=C, phi=inclination,L=totallength, **segments)

        # Just testing with valle envelope

        # compression_toughness = 0.56
        # n = 1/0.2
        _energy_released_mode_I = _energy_released_differential[1]

        # shear_toughness = 0.79
        # m=1/0.45
        _energy_released_mode_II_III = _energy_released_differential[2]


        _g_delta = (_energy_released_mode_I/_compression_toughness)**_n + (_energy_released_mode_II_III / _shear_toughness)**_m 

        # Store results for the current skier weight
        results.append({
            'skier_weight': _skierweight,
            'normal_stress': _sigma_kPa,
            'shear_stress': _tau_kPa,
            'distance_to_failure': _failure_distance,
            'intensity_failure': _failure_distance_intensity,
            'g_delta': _g_delta,
        })



    # Plotting the resulting distances to failure
    # Create a figure and axis
    _fig, _ax = plt.subplots()

    # Iterate through results and plot distance_to_failure for each skier weight
    for result in results:
        # Extract data for the current skier weight
        skier_weight = result['skier_weight']
        _x_cm = np.linspace(0, _totallength, len(result['distance_to_failure']))  # Assuming x_cm corresponds to length
        _failure_distance = result['distance_to_failure']

        # Plot distance to failure with a label indicating skier weight
        _ax.plot(_x_cm, _failure_distance, label=f'Skier Weight = {skier_weight} kg')

    # Set the y-axis range for failure_distance between 0 and 4 (adjust as needed)
    _ax.set_ylim(0, 4)

    # Add a vertical dashed red line at distance_to_failure = 1
    _ax.axhline(y=1, color='red', linestyle='--', label='Failure Threshold (1.0)')

    # Set labels and title
    _ax.set_xlabel('Position (cm)')
    _ax.set_ylabel('Distance to Failure')
    _ax.set_title('Distance to Failure for Various Skier Weights')

    # Add a legend
    _ax.legend(loc='upper right')

    # Show grid for better visualization
    _ax.grid(True)

    # Show the plot
    plt.tight_layout()
    plt.show()
    return j, result, results, skier_weight


@app.cell(hide_code=True)
def __(plt, results, skier_weight):
    # See how energy release rate is affected
    _fig2, _ax2 = plt.subplots()

    # Iterate through results and plot distance_to_failure for each skier weight
    for result2 in results:
        # Extract data for the current skier weight
        skier_weight_2 = result2['skier_weight']
        _g_delta = result2['g_delta']

        # Plot distance to failure with a label indicating skier weight
        _ax2.plot(skier_weight_2, _g_delta, label=f'Skier Weight = {skier_weight} kg',marker='o')

    # Set the y-axis range for failure_distance between 0 and 4 (adjust as needed)
    _ax2.set_ylim(0, 5)

    # Add a vertical dashed red line at distance_to_failure = 1
    _ax2.axhline(y=1, color='red', linestyle='--', label='ERR Threshold (1.0)')

    # Set labels and title
    _ax2.set_xlabel('Weight (kg)')
    _ax2.set_ylabel('ERR')
    _ax2.set_title('ERR')

    # Add a legend
    #_ax2.legend(loc='upper right')

    # Show grid for better visualization
    _ax2.grid(True)

    # Show the plot
    plt.tight_layout()
    plt.show()
    return result2, skier_weight_2


@app.cell(hide_code=True)
def __(
    distance_to_failure,
    failure_envelope,
    find_intersect,
    np,
    plt,
    result,
    skier,
    vectorized_point,
    weac,
):
    # Trying to set up testing environment
    # Custom profile
    v2_myprofile = [[170, 100],  # (1) surface layer
                     [190,  40],  # (2) 2nd layer
                     [230, 130],  #  :
                     [250,  20],  #  :
                     [210,  70],  # (i) i-th layer
                     [380,  20],  #  :
                     [280, 100]]  # (N) last slab layer above weak layer


    # We define a new layered system not defined by any of the standard test-types
    v2_skier = weac.Layered(system='skier', layers=v2_myprofile)

    # Changing the height of the weakness-layer
    v2_skier.set_foundation_properties(t=10, update=True)

    # Input of fixed variables
    v2_total_length = 10 * (sum(layer[1] for layer in v2_myprofile))                    # Total length (mm)
    v2_crack_length = 0                         # Crack length (mm)
    # v2_inclination = 30                       # Slope inclination (°)
    v2_skier_weight = 80

    # The variable we are flexing
    # skierweight = 80                       # Skier weight (kg)

    # Create an empty list to store results for each skier weight
    v2_results = []

    # Loop through skier weight values from 1 to 150 (0 is excluded as per the range)
    for v2_inclination in np.arange(15, 50, 5):  # Increments by 1, adjust as needed

        v2_segments = skier.calc_segments(
                            L=v2_total_length, 
                            a=v2_crack_length, 
                            m=v2_skier_weight  # Set current skier weight
                            )['nocrack']

        # Solve and rasterize solution
        v2_C = v2_skier.assemble_and_solve(phi=v2_inclination, **v2_segments)
        v2_xsl_skier, v2_z_skier, v2_xwl_skier = skier.rasterize_solution(C=v2_C, phi=v2_inclination, **v2_segments)

        # Calculate compressions and shear stress
        v2_x_cm, v2_tau_kPa = v2_skier.get_weaklayer_shearstress(x=v2_xwl_skier, z=v2_z_skier, unit='kPa')
        v2_x_cm, v2_sigma_kPa = v2_skier.get_weaklayer_normalstress(x=v2_xwl_skier, z=v2_z_skier, unit='kPa')

        # Calculate distance to failure
        v2_failure_distance = np.zeros_like(v2_tau_kPa)
        v2_point_axis = np.linspace(-3, 0, 100)

        for h, (v2_tau, v2_sigma) in enumerate(zip(-v2_tau_kPa, v2_sigma_kPa)):

            # Calculate intersect between envelope and vector of point-mass
            v2_intersect = find_intersect(v2_point_axis,
                                       vectorized_point(v2_point_axis, v2_tau / v2_sigma),
                                       failure_envelope(v2_point_axis)
                                      )
            # Calculate 
            v2_failure_distance[h] = distance_to_failure(v2_intersect,
                                                      v2_sigma,
                                                      v2_tau
                                                     )

        v2_failure_distance_intensity = np.sum(v2_failure_distance[v2_failure_distance > 1] - 1)

        # Store results for the current skier weight
        v2_results.append({
            'skier_weight': v2_skier_weight,
            'normal_stress': v2_sigma_kPa,
            'shear_stress': v2_tau_kPa,
            'distance_to_failure': v2_failure_distance,
            'intensity_failure': v2_failure_distance_intensity,
            'inclination': v2_inclination,
        })

    # Plotting the resulting distances to failure
    # Create a figure and axis
    v2_fig, v2_ax = plt.subplots()

    # Iterate through results and plot distance_to_failure for each skier weight
    for v2_result in v2_results:
        # Extract data for the current skier weight
        v2_inclination = v2_result['inclination']
        v2_x_cm = np.linspace(0, v2_total_length, len(result['distance_to_failure']))  # Assuming x_cm corresponds to length
        v2_failure_distance = v2_result['distance_to_failure']

        # Plot distance to failure with a label indicating skier weight
        v2_ax.plot(v2_x_cm, v2_failure_distance, label=f'Inclination = {v2_inclination} degrees')

    # Set the y-axis range for failure_distance between 0 and 4 (adjust as needed)
    v2_ax.set_ylim(0, 4)

    # Add a vertical dashed red line at distance_to_failure = 1
    v2_ax.axhline(y=1, color='red', linestyle='--', label='Failure Threshold (1.0)')

    # Set labels and title
    v2_ax.set_xlabel('Position (cm)')
    v2_ax.set_ylabel('Distance to Failure')
    v2_ax.set_title('Distance to Failure for Various Skier Weights')

    # Add a legend
    v2_ax.legend(loc='upper right')

    # Show grid for better visualization
    v2_ax.grid(True)

    # Show the plot
    plt.tight_layout()
    plt.show()
    return (
        h,
        v2_C,
        v2_ax,
        v2_crack_length,
        v2_failure_distance,
        v2_failure_distance_intensity,
        v2_fig,
        v2_inclination,
        v2_intersect,
        v2_myprofile,
        v2_point_axis,
        v2_result,
        v2_results,
        v2_segments,
        v2_sigma,
        v2_sigma_kPa,
        v2_skier,
        v2_skier_weight,
        v2_tau,
        v2_tau_kPa,
        v2_total_length,
        v2_x_cm,
        v2_xsl_skier,
        v2_xwl_skier,
        v2_z_skier,
    )


@app.cell
def __(failure_envelope, find_intersect, np, vectorized_point):
    def distance_to_failure(intersect_sigma, point_sigma, point_tau):

        # Would like to update this to take in the envelope we are comparing against, instead of intersect_sigma

        vector_abs = np.sqrt(point_sigma**2 + point_tau**2)
        slope = point_tau/point_sigma

        if np.any(intersect_sigma):
            #We are outside the envelope as intersect is not empty
            total_distance_to_envelope = np.sqrt(intersect_sigma**2 + vectorized_point(intersect_sigma,slope)**2)
            distance_factor = vector_abs / total_distance_to_envelope

            return distance_factor
        else:
            # We are inside the envelope: need to find the intersect of the extrapolated vector
            x_values = np.linspace(-3,0,100)

            intersect = find_intersect(x_values, vectorized_point(x_values,slope), failure_envelope(x_values))
            intersect_tau = vectorized_point(intersect, slope)

            total_distance_to_envelope = np.sqrt(intersect**2 + intersect_tau**2)

            distance_factor = vector_abs/total_distance_to_envelope

            return distance_factor
    return distance_to_failure,


@app.cell
def __(np):
    def find_intersect(x_values, vectorized_point, envelope):
        idx = np.argwhere(np.diff(np.sign(vectorized_point - envelope))).flatten()
        intersect_x = x_values[idx]

        return intersect_x
    return find_intersect,


@app.cell
def __(np):
    def failure_envelope(x):
        a = -2.75
        return np.where((x <= 0) & (x > a), np.sqrt(1 - (x**2 / a**2)),0)
    return failure_envelope,


@app.cell
def __(np):
    def failure_envelope_new(x):
        # Ensure x is treated as a NumPy array for vectorized operations
        x = np.asarray(x)

        a = -2.75
        # Apply conditions using np.where: If (x <= 0) & (x > a), compute the square root, otherwise return 0
        return np.where((x <= 0) & (x >= a), np.sqrt(1 - (x**2 / a**2)), 0)
    return failure_envelope_new,


@app.cell
def __(np):
    def failure_envelope_present_no_cap(x):
        x = np.asarray(x)

        sigma_c = 2.6        # (kPa)
        tau_c = 0.7          # (kPa)

        return np.where( ( x >= -sigma_c), np.sqrt( (1-(x**2 / sigma_c**2)) )*tau_c, 0)
    return failure_envelope_present_no_cap,


@app.cell
def __(np):
    def failure_envelope_smooth(x):
        x = np.asarray(x)

        sigma_c_plus = 0.4        # (kPa)
        sigma_c_minus = 2.6      # (kPa)
        w = 5                     # Shaprness of transition into capped region
        theta = np.pi/6                # Internal friction angle of the material

        tau_c = 0.7               # (kPa) - NOT USED

        return np.where( ( x < tau_c), (sigma_c_plus-x)*np.tan(theta)*np.tanh(w*(x-sigma_c_minus)), 0)
    return failure_envelope_smooth,


@app.cell
def __(np):
    def failure_envelope_reiweger(x):
        # Approximate linear interpolation for two line segments defined by a,b,c below
        a = -3
        b = -2.75
        c = 0.25

        # y-values at the specified points
        y_a = 0
        y_b = 1
        y_c = 0

        slope1 = (y_b - y_a) / (b - a)
        slope2 = (y_c - y_b) / (c - b)

        # Convert scalar inputs to an array for consistent processing
        x = np.asarray(x)

        # Initialize result array with zeros
        result = np.zeros_like(x)

        # Apply conditions
        mask1 = (x <= a)
        mask2 = (a < x) & (x < b)
        mask3 = (b <= x) & (x < c)

        result[mask1] = 0
        result[mask2] = y_a + x[mask2] * slope1
        result[mask3] = y_b + x[mask3] * slope2
        result[x >= c] = 0

        return result
    return failure_envelope_reiweger,


@app.cell
def __(np):
    def vectorized_point(x, slope):
        # Ensure x and slope are arrays to handle vectors
        x = np.asarray(x)
        slope = np.asarray(slope)

        # Return the element-wise product of x and slope
        return x * slope
    return vectorized_point,


@app.cell
def __(np):
    def vectorized_point_new(x, slope):
        # Ensure x and slope are arrays to handle vectors
        x = np.asarray(x)
        slope = np.asarray(slope)

        # Return the element-wise product of x and slope
        return np.outer(slope, x)
    return vectorized_point_new,


@app.cell
def __(distance_to_failure_2, np):
    def is_outside_stress_envelope(sigma, tau, envelope='reiweger'):
        # Ensure sigma and tau are arrays to handle vectors
        sigma = np.asarray(sigma)
        tau = np.asarray(tau)

        # Calculate the distance to failure for each point
        dist_to_fail = distance_to_failure_2(sigma, tau, envelope=envelope)

        # Convert dist_to_fail to a NumPy array if it's a list
        dist_to_fail = np.asarray(dist_to_fail)

        # Check if each distance is greater than 1 and mark as outside (True) or inside (False)
        outside_envelope = dist_to_fail >= 1  # This will now work if dist_to_fail is a NumPy array

        return outside_envelope, dist_to_fail  # Return two separate arrays
    return is_outside_stress_envelope,


@app.cell
def __():
    ## DOWN HERE ARE THROWAWAY METHODS ###
    return


@app.cell
def __(
    create_skier_object_v2,
    is_outside_stress_envelope,
    np,
    previous_end,
):
    #### NOT USED #########



    def find_new_crack_length(snow_profile, skier_weight, inclination, li, ki, envelope='reiweger'):

        # Create the skier object with the given parameters without a crack - you could do v2

        crack_length = 0
        skier, C, segments, x_cm, sigma_kPa, tau_kPa = create_skier_object_v2(
            snow_profile, crack_length, skier_weight, inclination, li, ki, crack_case='nocrack') 

        # Check if we are outside
        checker, dist_to_failure = is_outside_stress_envelope(sigma_kPa, -tau_kPa, envelope=envelope) 

        # We create a foundation object, which is False at points outside the stress envelope and True when we are inside, i.e. the inverse
        foundations = ~checker

        # Initialize lists to store segment lengths and their corresponding foundation type
        segment_lengths = []  # To hold the actual segments of x_cm
        segment_foundations = []  # To hold the boolean values for each segment
        x_mm = 10*x_cm

        # Initialize the first segment
        current_segment = [x_mm[0]]
        centerpoint = x_mm[-1]/2
        incrementals = [x_mm[i] - x_mm[i - 1] for i in range(1, len(x_mm))]

        incremental_step = x_mm[1]-x_mm[0]

        print(f"CENTERPOINT = {centerpoint}")

        # Loop through checker and group consecutive True/False values together
        for ij in range(1, len(foundations)):
            if foundations[ij] == foundations[ij - 1]:
                current_segment.append(x_mm[ij])
            else:
                # Otherwise, the segment ends; append the current segment and its foundation value
                segment_lengths.append(current_segment)
                segment_foundations.append(foundations[ij - 1])
                current_segment = [x_mm[ij]]

        # Append the final segment after the loop ends
        segment_lengths.append(current_segment)
        segment_foundations.append(foundations[-1])

        segment_foundations = [bool(item.flatten()[0]) for item in segment_foundations]

        segments_outside_envelope = [segment for segment, is_true in zip(segment_lengths, segment_foundations) if not is_true]

        print(f"\033[91m THESE ARE OUTSIDE THE ENVELOPE: {segments_outside_envelope}  \033[0m")
        # print(f"SEGMENT LENGTHS: {segment_lengths} ")
        # print(f"x_mm : {x_mm}")

        segments_combined = []
        segment_foundations_combined = []

        # Initialize variables
        segments_combined = []
        segment_foundations_combined = []


        # Iterate through each segment and its corresponding foundation, along with index i
        for i, (segment, foundation) in enumerate(zip(segment_lengths, segment_foundations)):

            # Handle the very first segment (start is segment[0])
            if i == 0:
                start = segment[0]
            else:
                # For subsequent segments, start should be the end of the previous segment
                start = previous_end


            if foundation==False: 
                # We need a different end of segment to make sure our segments are not too short
                # We approximate that all places where we are not true are false: a bit too big

                end = (segment[-1] + segment_lengths[i+1][0])/2

                # This is the start of next segment
                # Store the current end for the next iteration
                previous_end = end
            else:
                # End of the current segment
                end = segment[-1]
                # Store the current end for the next iteration
                previous_end = end

            # Check if the centerpoint is within the segment
            if start < centerpoint < end:

                # Split the segment into two parts: before and after the centerpoint
                segment_before_midpoint = centerpoint - start  # incremental ste
                segment_after_midpoint = end - centerpoint

                # Append both segments and their foundation
                segments_combined.append(segment_before_midpoint)
                segment_foundations_combined.append(foundation)

                segments_combined.append(segment_after_midpoint)
                segment_foundations_combined.append(foundation)

                # We must also make sure we 
                print(f"\033[91m MIDPOINT CASE: {segments_combined}  \033[0m")

            else:
                # If no centerpoint, just add the whole segment length
                segment_length = end - start  # incremental_step
                segments_combined.append(segment_length)
                segment_foundations_combined.append(foundation)


        li = segments_combined
        ki = segment_foundations_combined

        print(f"NEW CRACK li = {li}            //.    ki = {ki}")
        print(f"TOTAL LENGTH OF SEGMENTS = {np.sum(li)}")

        new_crack_length = sum(length for length, foundation in zip(segments_combined, segment_foundations_combined) if not foundation)


        return new_crack_length, li, ki
    return find_new_crack_length,


if __name__ == "__main__":
    app.run()
