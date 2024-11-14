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
    from scipy.optimize import root_scalar
    return app, ast, f, mo, mpimg, np, os, pd, plt, root_scalar, time, weac


@app.cell
def __():
    # Custom profile
    myprofile = [[170, 100],  # (1) surface layer
                 [290,  40],  # (2) 2nd layer
                 [130, 130],  #  :
                 [150,  20]]  # (N) last slab layer above weak layer
    return myprofile,


@app.cell
def __(myprofile):
    # Input
    totallength = 100*(sum(layer[1] for layer in myprofile))                    # Total length (mm)
    crack_length = 0                         # Crack length (mm)
    inclination = 25                       # Slope inclination (°)
    skier_weight = 1000                      # Skier weigth (kg)

    half = totallength/2
    li = [half,0,0,half]
    ki = [True,True,True,True]
    return (
        crack_length,
        half,
        inclination,
        ki,
        li,
        skier_weight,
        totallength,
    )


@app.cell
def __(f, inclination, ki, li, myprofile, skier_weight):
    skier, C, segments, x_cm, sigma_kPa, tau_kPa = f.create_skier_object_v2(myprofile, skier_weight, inclination, li, ki, crack_case='nocrack')
    return C, segments, sigma_kPa, skier, tau_kPa, x_cm


@app.cell
def __(segments):
    print(segments['li'])
    return


@app.cell
def __(C):
    print(C)
    return


@app.cell
def __(C, half, inclination, li, skier):
    # The greatest stress should be close to center, have a look at x_coordinate in the middle of the interval
    x = half

    # C is the segment solution at 
    Z = skier.z(2500, C, li[2], inclination, bed=True)
    t = skier.tau(Z, unit='kPa')
    s = skier.sig(Z, unit='kPa')
    return Z, s, t, x


@app.cell
def __(Z):
    print(Z)
    return


@app.cell
def __(np, s, t):
    np.set_printoptions(threshold=np.inf)
    print(t)
    print(s)
    return


@app.cell
def __(s, t):
    sigma = s[2]
    tau = -t[2]
    return sigma, tau


@app.cell
def __(t, x_cm):
    print(len(x_cm))
    print(len(t))

    # Why are they different lengths?
    return


@app.cell
def __(f, sigma, tau):
    print(sigma)

    distance = f.distance_to_failure_2(sigma,tau,envelope='no_cap')

    print(distance)
    return distance,


@app.cell
def __(f, np, plt, sigma, tau, x):
    # Create the plot
    plt.figure(figsize=(10, 6))

    # Plot tau (shear stress) vs x_center_of_mass
    plt.plot(x, -tau, label=r'$\tau$ (shear stress)', color='r', linestyle='-', marker='o')

    # Plot sigma (normal stress) vs x_center_of_mass
    plt.plot(x, sigma, label=r'$\sigma$ (normal stress)', color='b', linestyle='-', marker='x')

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
    plt.scatter(sigma, tau, label=r'$\tau$ (shear stress) vs $\sigma$ (normal stress)', color='r', marker='o')

    new_env = np.linspace(-8,8,1000)
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
    return new_env,


@app.cell
def __(distance):
    distance

    # Looks to be correct
    return


@app.cell
def __(np):
    def envelope_function(sigma,tau):
        sigma = np.asarray(sigma)
        tau = np.asarray(tau)

        sigma_c = 6.16       # (kPa) 6.16 / 2.6
        tau_c = 5.09         # (kPa) 5.09 /  0.7

        return ( (sigma/sigma_c)**2 + (tau/tau_c)**2 )
    return envelope_function,


@app.cell
def __():
    #tau = lambda x: weac.tau(C,x)
    return


@app.cell
def __(envelope_function, f, new_env, plt, sigma_kPa, tau_kPa, x_cm):
    # Create the first plot (shear and normal stress vs. x position)
    plt.figure(figsize=(10, 6))

    # Plot tau_kPa (shear stress) vs x_cm
    plt.plot(x_cm, tau_kPa, label=r'$\tau$ (Shear Stress)', color='r', linestyle='-', marker='o')

    # Plot sigma_kPa (normal stress) vs x_cm
    plt.plot(x_cm, sigma_kPa, label=r'$\sigma$ (Normal Stress)', color='b', linestyle='-', marker='x')

    # Plot sigma_kPa (normal stress) vs x_cm
    plt.plot(x_cm, envelope_function(sigma_kPa,tau_kPa), label='Distance_to_failure_function', color='g', linestyle='-', marker='o')

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

    # Create the second plot (shear stress vs normal stress)
    plt.figure(figsize=(10, 6))

    # Plot tau_kPa (shear stress) vs sigma_kPa (normal stress)
    plt.scatter(sigma_kPa, -tau_kPa, label=r'$\tau$ (Shear Stress) vs $\sigma$ (Normal Stress)', color='r', marker='o')

    plt.plot(new_env, f.failure_envelope_present_no_cap(new_env), label='No_cap envelope', color='green')
    plt.fill_between(new_env, f.failure_envelope_present_no_cap(new_env), color='lightgreen', alpha=0.1)

    # Adding labels and title
    plt.xlabel(r'$\sigma$ (Normal Stress, kPa)', fontsize=12)
    plt.ylabel(r'$\tau$ (Shear Stress, kPa)', fontsize=12)
    plt.title('Shear Stress vs. Normal Stress with Failure Envelope', fontsize=14)

    # Adding grid and legend
    plt.grid(True)
    plt.legend()

    # Show the plot
    plt.tight_layout()
    plt.show()
    return


@app.cell
def __():
    return


@app.cell
def __(find_segment_index, li):
    find_segment_index(li,25000)
    return


@app.cell
def __():
    return


@app.cell
def __(envelope_function, np, root_scalar):
    def find_roots_around_x(x_value, skier, C, li, inclination, sigma_kPa, tau_kPa, x_cm):
        # Define the lambda function for the root function
        func = lambda x: root_function(x, skier, C, li, inclination)

        # Identify the segment index for the given x_value
        segment_index, coordinate_in_segment = find_segment_index(li, x_value)

        # Calculate the discrete distance to failure using the envelope function
        discrete_dist_to_fail = envelope_function(sigma_kPa, tau_kPa) - 1

        # Find indices where the envelope function transitions from positive to negative
        transition_indices = np.where(np.diff(np.sign(discrete_dist_to_fail)))[0]

        # Extract the corresponding x_cm values at those transition indices
        root_candidates = []
        for idx in transition_indices:
            # Get the x_cm values surrounding the transition
            x_left = x_cm[idx]
            x_right = x_cm[idx + 1]
            root_candidates.append((10*x_left, 10*x_right))

        # Print the root candidates
        print("Root candidates based on envelope function transitions:")
        for x_left, x_right in root_candidates:
            print(f"From x = {x_left} to x = {x_right}")

        # Search for roots within the identified candidates
        roots = []
        for x_left, x_right in root_candidates:
            try:
                root_result = root_scalar(func, bracket=[x_left, x_right], method='brentq')
                if root_result.converged:
                    roots.append(root_result.root)
                    print(f"Root found at x = {root_result.root}")
            except ValueError:
                print(f"No root found between x = {x_left} and x = {x_right}.")

        return roots

    def root_function(x_value, skier, C, li, inclination):
        sigma, tau = calculate_sigma_tau(x_value, skier, C, li, inclination)
        return envelope_function(sigma, tau) - 1

    def find_segment_index(segment_lengths, coordinate):
        # Handle the case where segment_lengths is a single integer
        if isinstance(segment_lengths, (int, float)):
            return 0, coordinate  # Return index 0 and the coordinate as the relative value

        # Convert segment_lengths to an array if it's a list
        segment_lengths = np.asarray(segment_lengths)

        # Check for singular segment
        if len(segment_lengths) == 1:
            return 0, coordinate  # Return index 0 and the coordinate as the relative value

        cumulative_length = 0

        for index, length in enumerate(segment_lengths):
            cumulative_length += length
            if coordinate <= cumulative_length:
                # Calculate the relative value within the segment
                relative_value = coordinate - (cumulative_length - length)
                return index, relative_value

        return -1, None  # Return -1 if coordinate exceeds all segments

    # Example usage would go here

    def calculate_sigma_tau(x_value, skier, C, li, inclination):
        segment_index, coordinate_in_segment = find_segment_index(li, x_value)
        Z = skier.z(coordinate_in_segment, C, li[segment_index], inclination, bed=True)
        t = skier.tau(Z, unit='kPa')
        s = skier.sig(Z, unit='kPa')

        tau = -t[segment_index]  # Remember to switch sign
        sigma = s[segment_index]
        return sigma, tau
    return (
        calculate_sigma_tau,
        find_roots_around_x,
        find_segment_index,
        root_function,
    )


@app.cell
def __(
    C,
    find_roots_around_x,
    half,
    inclination,
    li,
    sigma_kPa,
    skier,
    tau_kPa,
    x_cm,
):
    print(half)
    initial_x = half  # Replace with numeric value for 'half'
    # Replace skier, C, totallength, and inclination with actual values or objects
    roots_x = find_roots_around_x(initial_x, skier, C, li, inclination, sigma_kPa, tau_kPa, x_cm)
    return initial_x, roots_x


@app.cell
def __(roots_x):
    print(roots_x)
    return


@app.cell
def __(
    envelope_function,
    f,
    find_roots_around_x,
    np,
    split_segments_at_midpoint,
):
    def find_new_crack_length_v3(snow_profile, skier_weight, inclination, li, ki, envelope='reiweger'):
        crack_length = 0
        total_length = np.sum(li)
        midpoint = total_length / 2

        print("INSIDE FIND NEW CRACK LENGTH METHOD")
        print(f"Total Length: {total_length}")
        print(f"Midpoint: {midpoint}")

        skier, C, segments, x_cm, sigma_kPa, tau_kPa = f.create_skier_object_v2(
            snow_profile, skier_weight, inclination, li, ki, crack_case='nocrack') 

        all_points_are_outside = np.min(envelope_function(sigma_kPa, tau_kPa)) > 1
        print(f"All Points Are Outside Envelope: {all_points_are_outside}")

        roots_x = find_roots_around_x(midpoint, skier, C, li, inclination, sigma_kPa, tau_kPa, x_cm)
        print(f"Roots Found: {roots_x}")

        if len(roots_x) > 0:
            segment_boundaries = [0] + roots_x + [total_length]
            li_temp = np.diff(segment_boundaries).tolist()  # Convert to a list
            ki_temp = [True] * (len(segment_boundaries) - 1) 

            print(f"Segment Boundaries: {segment_boundaries}")
            print(f"li_temp: {li_temp}")
            print(f"Initial ki_temp: {ki_temp}")

            # Create a boolean list indicating root positions
            is_root = [False] * len(segment_boundaries)
            for root in roots_x:
                is_root[segment_boundaries.index(root)] = True

            print(f"Root Positions (is_root): {is_root}")

            # Iterate over the roots to determine cracked segments
            nbr_roots = len(roots_x)
            for i in range(1, len(is_root)):  # Start from the second root
                # Check if the current and previous boundaries are both roots
                if is_root[i] and is_root[i - 1]:
                    ki_temp[i - 1] = False  # Mark the segment as cracked

            print(f"Updated ki_temp After Checking Roots: {ki_temp}")

            # Proceed to split li and ki at the midpoint
            li, ki = split_segments_at_midpoint(li_temp, ki_temp)
            print(f"Split li: {li}")
            print(f"Split ki: {ki}")

        elif all_points_are_outside:
            print("All points are outside the envelope. No cracks.")
            ki = [False] * len(ki)
        else:
            print("No roots found. Returning original segments.")
            # No changes to li and ki
            li = li
            ki = [True]*len(ki)

        # Calculate new crack length
        new_crack_length = sum(length for length, foundation in zip(li, ki) if not foundation)
        print(f"New Crack Length: {new_crack_length}")

        return new_crack_length, li, ki
    return find_new_crack_length_v3,


@app.cell
def __(np):
    def split_segments_at_midpoint(segment_lengths, segment_support):
        # Calculate the cumulative lengths of segments to find the midpoint
        cumulative_lengths = np.cumsum(segment_lengths)
        total_length = cumulative_lengths[-1]
        midpoint = total_length / 2

        # Find the segment that contains the midpoint
        for i, length in enumerate(segment_lengths):
            if cumulative_lengths[i] >= midpoint:
                # Split the segment at the exact midpoint
                if i == 0:
                    # If the midpoint is in the first segment
                    new_segments = [midpoint] + segment_lengths[i:]  # split before the first segment
                    new_support = [segment_support[0]] + segment_support[i:]  # retain support value
                else:
                    # Split the found segment at the midpoint
                    segment_start = cumulative_lengths[i - 1] if i > 0 else 0
                    new_segments = (
                        segment_lengths[:i] +
                        [midpoint - segment_start] + 
                        [cumulative_lengths[i] - midpoint] + 
                        segment_lengths[i + 1:]
                    )
                    # Split support for the two new segments
                    new_support = (
                        segment_support[:i] + 
                        [segment_support[i]] + 
                        [segment_support[i]] + 
                        segment_support[i + 1:]
                    )
                break
        else:
            # If no segment contains the midpoint, return the original segments and support
            return segment_lengths, segment_support

        return new_segments, new_support
    return split_segments_at_midpoint,


@app.cell
def __(np):
    def determine_segment_cracking(roots_x, total_length):
        # Check if we have any roots
        if len(roots_x) > 0:
            # Create segment boundaries including total_length
            segment_boundaries = [0] + roots_x + [total_length]
            li_temp = np.diff(segment_boundaries)

            # Initialize the helper vector to track cracked segments
            ki_temp = [True] * (len(li_temp) - 1)  # There will be one less segment than boundaries

            # Create a boolean list indicating root positions
            is_root = [False] * len(segment_boundaries)

            # Set True for each root in the middle
            for root in roots_x:
                is_root[segment_boundaries.index(root)] = True

            # We should have at least two roots here to determine segments
            nbr_roots = len(roots_x)

            # Iterate over the roots to determine cracked segments
            for i in range(1, nbr_roots):  # Start from the second root
                # Check if the current and previous boundaries are both roots
                if is_root[i] and is_root[i - 1]:
                    ki_temp[i - 1] = False  # Mark the segment as cracked

            return ki_temp, is_root
        else:
            return [], []  # Return empty lists if no roots are found
    return determine_segment_cracking,


@app.cell
def __(determine_segment_cracking):
    # Example usage
    roots_x2 = [100, 200, 300]  # Example root coordinates
    total_length = 400  # Total length of the interval

    # Determine the cracking status of segments
    ki_temp, is_root = determine_segment_cracking(roots_x2, total_length)
    print("Segment Cracking Status:", ki_temp)
    print("Is Root List:", is_root)
    return is_root, ki_temp, roots_x2, total_length


@app.cell
def __(split_segments_at_midpoint):
    # Example usage
    segments_x = [24000, 350000, 2000]
    supports_x =[True, False, True]
    new_segments = split_segments_at_midpoint(segments_x, supports_x)
    print("Original segments:", segments_x)
    print("New segments after split:", new_segments)
    return new_segments, segments_x, supports_x


@app.cell
def __(find_new_crack_length_v3, inclination, ki, li, myprofile):
    # Testing v3
    cracker,_,_= find_new_crack_length_v3(myprofile, 1000, inclination, li, ki, envelope='no_cap')
    return cracker,


@app.cell
def __(cracker):
    print(cracker)
    return


@app.cell
def __():
    return


@app.cell
def __(envelope_function, f, np):
    def find_minimum_force_v3(snow_profile, inclination, li, ki, envelope='reiweger'): 
        # Initial parameters
        crack_length = 0
        crack_case = 'nocrack'
        skier_weight = 1  # Starting weight of skier

        print("Starting the minimum force calculation...")
        print(f"Initial Skier Weight: {skier_weight}")
        print(f"Initial Crack Case: {crack_case}")

        skier, C, segments, x_cm, sigma_kPa, tau_kPa = f.create_skier_object_v2(
            snow_profile,  skier_weight, inclination, li, ki, crack_case='nocrack'
        )

        # Calculate the distance to failure
        distance_to_failure = np.max(envelope_function(sigma_kPa, tau_kPa))
        print(f"Initial Distance to Failure: {distance_to_failure}")

        while distance_to_failure < 1 or np.abs(distance_to_failure - 1) > 0.02:   # While no point is outside the envelope
            print("Distance to failure is below threshold; increasing skier weight...")
            skier_weight = skier_weight / distance_to_failure
            print(f"Updated Skier Weight: {skier_weight}")

            # Recreate the skier object with the updated weight
            skier, C, segments, x_cm, sigma_kPa, tau_kPa = f.create_skier_object_v2(
                snow_profile, skier_weight, inclination, li, ki, crack_case='nocrack'
            )

            # Recalculate the distance to failure
            distance_to_failure = np.max(envelope_function(sigma_kPa, tau_kPa))
            print(f"New Distance to Failure: {distance_to_failure}")

        # Once the loop exits, it means we have found the critical skier weight
        print("Critical skier weight found. Exiting the calculation.")
        print(f"Final Skier Weight: {skier_weight}")
        print(f"Final Distance to Failure: {distance_to_failure}")

        return skier_weight, skier, C, segments, x_cm, sigma_kPa, tau_kPa, distance_to_failure
    return find_minimum_force_v3,


@app.cell
def __(find_minimum_force_v3, inclination, ki, li, myprofile):
    find_minimum_force_v3(myprofile, inclination, li, ki, envelope='no_cap')
    return


@app.cell
def __(check_first_criterion_v3, inclination, myprofile, skier_weight):
    check_first_criterion_v3(myprofile, inclination, skier_weight, envelope='no_cap')
    return


@app.cell
def __(
    checker,
    envelope_function,
    f,
    find_minimum_force_v3,
    find_new_crack_length_v3,
    np,
    time,
):
    def check_first_criterion_v3(snow_profile, inclination, skier_weight, envelope='reiweger'):

        # Time tracker
        start_time = time.time()
        elapsed_times = []

        # Trackers for skier weights and crack lengths
        skier_weights = []
        crack_lengths = []

        # Initialize parameters
        length = 100 * sum(layer[1] for layer in snow_profile)  # Total length (mm)
        k0 = [True, True, True, True]  # Support boolean for uncracked solution
        li = [length / 2, 0, 0, length / 2]  # Length segments
        ki = [True, True, True, True]  # Length of segments with foundations

        # Create initial skier object
        skier, C, segments, x_cm, sigma_kPa, tau_kPa = f.create_skier_object_v2(
            snow_profile, skier_weight, inclination, li, ki, crack_case='nocrack'
        )

        # Check if we are outside the stress envelope at any point
        distance_to_failure = envelope_function(sigma_kPa, tau_kPa)
        dist_max = np.max(distance_to_failure)
        dist_min = np.min(distance_to_failure)


        # Initialize iteration variables
        iteration_count = 0
        max_iterations = 25

        if dist_max > 1 and not dist_min > 1:
            # Find minimum critical force to initialize our algorithm (BASE CASE)
            skier_weight, *_ = find_minimum_force_v3(snow_profile, inclination, li, ki, envelope=envelope)
            max_skier_weight = 4*skier_weight
            min_skier_weight = skier_weight


            # Set initial crack length and error margin
            crack_length = 1  # Initial crack length
            err = 1000  # Error margin
            li = [length / 2 - crack_length / 2, crack_length / 2, crack_length / 2, length / 2 - crack_length / 2]
            ki = [True, False, False, True]

            while np.abs(err) > 0.002 and iteration_count < max_iterations and any(ki):

                # Track skier weight, crack length and time for each iteration
                iteration_count += 1
                skier_weights.append(skier_weight)
                crack_lengths.append(crack_length)
                elapsed_times.append(time.time() - start_time)


                # Create base_case with the correct number of segments
                skier, C, segments, x_cm, sigma_kPa, tau_kPa = f.create_skier_object_v2(
                    snow_profile, skier_weight, inclination, li, ki, crack_case='nocrack'
                )

                # Check distance to failure for uncracked solution
                distance_to_failure = envelope_function(sigma_kPa, tau_kPa)
                dist_max = np.max(distance_to_failure)
                dist_min = np.min(distance_to_failure)

                # Solving a cracked solution, to calculate incremental ERR
                c_skier, c_C, c_segments, c_x_cm, c_sigma_kPa, c_tau_kPa = f.create_skier_object_v2(
                    snow_profile, skier_weight, inclination, li, ki, crack_case='crack'
                )

                k0 = np.full(len(ki), True)



                # Calculate incremental energy released compared to uncracked solution
                incr_energy = c_skier.ginc(C0=C, C1=c_C, phi=inclination, **c_segments, k0=k0)
                g_delta = f.energy_criterion(1000*incr_energy[1], 1000*incr_energy[2])

                # scaling_in_theory = g_delta ** (-1 / 12)


                print(f"START OF ITERATION {iteration_count}: crack length: {crack_length} mm, Skier Weight: {skier_weight} kg, Max Distance to Failure: {dist_max}, Distance to energy envelope: {g_delta}")

                # Determine scaling coefficient
                # scaling = g_delta ** (-1 / 2)

                if g_delta < 1:
                    min_skier_weight = skier_weight
                else:
                    max_skier_weight = skier_weight

                new_skier_weight = (min_skier_weight + max_skier_weight) / 2 

                # scaling = g_delta ** (-1 / 12)

                scaling = new_skier_weight / skier_weight

                # Check gravitational forces
                current_normal_force, current_tangential_force = c_skier.get_skier_load(skier_weight, inclination)
                current_gravitational_force = np.sqrt(current_normal_force ** 2 + current_tangential_force ** 2)
                updated_gravitational_force = scaling * current_gravitational_force

                # Update error margin
                err = np.abs(updated_gravitational_force - current_gravitational_force) / updated_gravitational_force

                # Adjust skier weight based on error margin
                if np.abs(err) > 0.002:
                    skier_weight = new_skier_weight

                    # Find new crack length for the next iteration
                    new_crack_length, li, ki = find_new_crack_length_v3(snow_profile, skier_weight, inclination, li, ki, envelope=envelope)
                    crack_length = new_crack_length

                    print(f"END OF ITERATION: g_delta: {g_delta} J/m^2, Old skier weight: {skier_weight} kg, Scaling: {scaling} kg, New skier weight: {skier_weight} kg, crack length: {crack_length} mm")

            # End of loop: convergence or max iterations reached
            if iteration_count < max_iterations and any(ki):
                print(f"CONVERGENCE: crack length: {crack_length} mm, Critical Skier Weight: {skier_weight} kg, Distance to energy envelope: {g_delta} J/m^2, Max Distance to Stress Envelope: {dist_max}")

                if crack_length > 0:
                    return True, crack_length, skier_weight, c_skier, c_C, c_segments, c_x_cm, c_sigma_kPa, c_tau_kPa, iteration_count, elapsed_times, skier_weights, crack_lengths
                else:
                    print("Crack length is zero; redoing the algorithm with the dampened version.")
                    skier_weight_average = np.average(skier_weights)
                    variance = np.var(np.asarray(skier_weights), ddof=1)
                    return f.check_first_criterion_damped_outside_envelope(snow_profile, inclination, skier_weight_average, variance, envelope=envelope)

            elif not any(ki):
                print("We are outside the envelope at all points.")
                return True, crack_length, skier_weight, None, None, None, None, None, None, iteration_count, elapsed_times, skier_weights, crack_lengths

            else:
                print("Maximum iterations reached without convergence.")
                skier_weight_average = np.average(skier_weights)
                variance = np.var(np.asarray(skier_weights), ddof=1)
                return f.check_first_criterion_damped(snow_profile, inclination, skier_weight_average, variance, envelope=envelope)

        elif checker.all():
            # Extreme case: entire solution is cracked
            crack_length = length
            skier_weight = 0
            return True, crack_length, skier_weight, None, None, None, None, None, None, iteration_count, elapsed_times, skier_weights, crack_lengths

        else:
            # No points are overloaded
            return False, 0, skier_weight, None, None, None, None, None, None, iteration_count, elapsed_times, skier_weights, crack_lengths
    return check_first_criterion_v3,


if __name__ == "__main__":
    app.run()
