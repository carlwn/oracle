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
    return app, ast, mo, mpimg, np, os, pd, plt, time, weac


@app.cell
def __(mo):
    mo.md(
        """
        # Updates
        1. Start a new branch
        2. Crack entire length
        3. Use the new Valle-envelope
        4. Replace discrete with continuous x_tau and root search
        5. Actually implement the second stage criterion


        # Questions / Issues
        1. The algorithm will not converge unless the length to thickness ratio is within specific bounds. Currently running at 100x thickness, but standardized lengths results in us moving outside of the stress envelope quickly (too high then way too low and we are dead), for all snowprofiles
        2. Incremental energy released is always just below 1, never 1 exactly
        3. Need convergence limit of 0.002, otherwise we bounce around
        4. ^(-1/11) fixes some convergence issues where we otherwise would scale ourselves below the envelope
        5. The crack length issue of discretization to continuous length


        # ToDo
        3. Create_skier_object does not need crack_length as an input
        4. Check cases where crack_length is zero (six entries) fixed 3
        5. Check cases on non-convergence (25 entries) fixed 22
        6. Run through rest of datapoints and fix issues as we go

        # Proposed way of solving convergence
        1. Added dampened version
        """
    )
    return


@app.cell
def __():
    # This sheet will contain solely methods
    return


@app.cell
def __(ast, check_first_criterion_v2):
    # Function to apply for extracting skier_weight and crack_length
    def apply_check_first_criterion(row):

        inclination = row['slopeangle']
        # skier_weight = row['approximate_critical_loads']
        snow_profile = ast.literal_eval(row['snow_profiles'])

        # REMEMBER THAT WE NEED TO REVERSE

        # print(snow_profile)

        snow_profile_reversed = snow_profile[::-1]

        print(snow_profile_reversed)

        convergence_check, crack_length, skier_weight, _, _, _, _, _, _, iterations, elapsed_times, skier_weights, crack_lengths = check_first_criterion_v2(
            snow_profile=snow_profile_reversed, inclination=inclination, skier_weight=1000, envelope='no_cap'
        )

        if convergence_check:
            print(f"\033[91m CONVERGENCE: WE FOUND A SOLUTION AND WILL NOW LOOK AT THE NEXT DATA POINT \033[0m")
        else:
            print(f"\033[91m ALGORITHM DID NOT CONVERGE \033[0m")

        return convergence_check, skier_weight, crack_length, iterations, elapsed_times, skier_weights, crack_lengths
    return apply_check_first_criterion,


@app.cell
def __(
    check_first_criterion_damped,
    check_first_criterion_damped_outside_envelope,
    create_skier_object_v2,
    energy_criterion,
    find_minimum_force_v2,
    find_new_crack_length_v2,
    is_outside_stress_envelope,
    np,
    time,
):
    def check_first_criterion_v2(snow_profile, inclination, skier_weight, envelope='reiweger'):
        # Assuming nocrack case to begin with and create a skier-object
        crack_length = 0
        length = 100 * (sum(layer[1] for layer in snow_profile))  # Total length (mm)
        # length = 100 * 100 * 10  # Total length (mm) (one hundred meters in mm)
        # length = 100 * (sum(layer[1] for layer in snow_profile)) 
        # length = sum(li)

        k0 = [True, True, True, True]  # Support boolean for uncracked solution
        li = [length / 2, 0, 0, length / 2]  # Support boolean for uncracked solution
        ki = [True, True, True, True]  # Length of segments with foundations as specified by ki

        skier, C, segments, x_cm, sigma_kPa, tau_kPa = create_skier_object_v2(snow_profile, crack_length, skier_weight, inclination, li, ki, crack_case='nocrack')

        # For the initial skier object, check if we are outside the stress envelope at any point
        checker, dist_to_failure = is_outside_stress_envelope(sigma_kPa, -tau_kPa, envelope=envelope)

        # Time tracker
        start_time = time.time()
        elapsed_times = []

        # Tracker lists for skier weights and crack lengths
        skier_weights = []
        crack_lengths = []


        # Initialize iteration variables
        iteration_count = 0
        max_iterations = 25

        if checker.any() and not checker.all():
            # Find the weight associated with minimum critical force to initialize our algorithm (BASE CASE)
            skier_weight, *_ = find_minimum_force_v2(snow_profile, inclination, li, ki, envelope=envelope) 

            initial_skier_weight = skier_weight

            # Initialize variables for algorithm
            init_crack_length = 1  # Initial crack length
            err = 1000  # Error margin
            li = [length / 2 - init_crack_length / 2, init_crack_length / 2, init_crack_length / 2, length / 2 - init_crack_length / 2]
            ki = [True, False, False, True]


            while np.abs(err) > 0.002 and iteration_count < max_iterations and any(ki):
                # ki.any() ensures we move out in case we are outside the envelope in all points

                # Increment iteration counter
                iteration_count += 1


                # Track skier weight and crack length for each iteration
                skier_weights.append(skier_weight)
                crack_lengths.append(crack_length)

                # Time tracking for each iteration
                elapsed_times.append(time.time() - start_time)

                # Create the base_case with correct number of segments
                skier, C, segments, x_cm, sigma_kPa, tau_kPa = create_skier_object_v2(snow_profile, crack_length, skier_weight, inclination, li, ki, crack_case='nocrack')

                # Solving a cracked solution
                c_skier, c_C, c_segments, c_x_cm, c_sigma_kPa, c_tau_kPa = create_skier_object_v2(snow_profile, crack_length, skier_weight, inclination, li, ki, crack_case='crack')

                # print(f" Solution: {c_segments}")

                # Section to keep track of distance to failure
                checker_2, dist_to_failure_2 = is_outside_stress_envelope(sigma_kPa, -tau_kPa, envelope=envelope)
                # WHY IS THIS NOT THE SAME DISTANCE TO FAILURE AS THE LAST ONE IN find_min_force

                print(f" START OF ITERATION {iteration_count}: cracklength: {crack_length} mm, Skier Weight: {skier_weight} kg, Max Distance to Failure: {np.max(dist_to_failure_2)}")


                # The uncracked solution will have True for all values
                k0 = np.full(len(ki), True)

                # Calculate incremental energy released compared to (BASE CASE) solution above
                incr_energy = c_skier.ginc(C0=C, C1=c_C, phi=inclination, **c_segments, k0=k0)

                # Evaluate energy envelope (scaling by 1000 to convert kJ to J)
                g_delta = energy_criterion(1000 * incr_energy[1], 1000 * incr_energy[2])

                scaling = (g_delta**(-1/12))

                # For any scaling below 1, we are not outside the energy envelope and must increase the force
                current_normal_force, current_tangential_force = c_skier.get_skier_load(skier_weight, inclination)
                current_gravitational_force = np.sqrt(current_normal_force ** 2 + current_tangential_force ** 2)
                updated_gravitational_force = scaling * (current_gravitational_force)



                # Updating error margin
                err = np.abs(updated_gravitational_force - current_gravitational_force) / updated_gravitational_force

                # For errors > margin we scale skier weight according to g_delta calculated above, and find new crack length
                if np.abs(err) > 0.002:
                    new_skier_weight = skier_weight * scaling

                    # For the updated skier force, we find all points where the weak layer is overloaded and use this as 

                    # the crack length in the next iteration (with li and ki specifying how the crack is positioned in the weak layer)

                    new_crack_length, li, ki = find_new_crack_length_v2(snow_profile, skier_weight, inclination, li, ki, envelope=envelope)
                    crack_length = new_crack_length
                    print(f" END OF ITERATION: g_delta: {g_delta} J/m^2, Old skier weight: {skier_weight} kg, Scaling: {scaling} kg, New skier weight: {new_skier_weight} kg, cracklength: {crack_length} mm,")

                    skier_weight = new_skier_weight

            # End of loop, i.e., convergence or max iteration reached
            if iteration_count < max_iterations and any(ki):
                print(f" CONVERGENCE: cracklength: {crack_length} mm, Critical Skier Weight: {skier_weight} kg, Distance to energy envelope: {g_delta} J/m^2, Max Distance to Stress Envelope: {np.max(dist_to_failure_2)}")

                if crack_length>0:
                    return True, crack_length, skier_weight, c_skier, c_C, c_segments, c_x_cm, c_sigma_kPa, c_tau_kPa, iteration_count, elapsed_times, skier_weights, crack_lengths
                else:
                    print(f" Cracklength is zero and we redo the algorithm with the dampened version")
                    skier_weight_average = np.average(skier_weights)
                    variance = np.var(np.asarray(skier_weights), ddof=1)

                    return check_first_criterion_damped_outside_envelope(snow_profile, inclination, skier_weight_average, variance, envelope=envelope)


            elif not any(ki):
                print("We are outside the envelope in all points")
                return True, crack_length, skier_weight, None, None, None, None, None, None, iteration_count, elapsed_times, skier_weights, crack_lengths
            else:
                # The issue of non-convergence is often bouncing too far above and too far below the solution. If we take the average of the approxima

                print("Maximum iterations reached without convergence.")
                skier_weight_average = np.average(skier_weights)

                variance = np.var(np.asarray(skier_weights), ddof=1)


                return check_first_criterion_damped(snow_profile, inclination, skier_weight_average, variance, envelope=envelope)

        elif checker.all():
            # Extreme case (i) we are outside the boundary at all points: the entire solution is cracked
            crack_length = length
            skier_weight = 0

            return True, crack_length, skier_weight, None, None, None, None, None, None, iteration_count, elapsed_times, skier_weights, crack_lengths

        else:
            # Extreme case (ii) We do not fulfill the stress criterion in any point, and will therefore not be able to trigger an avalanche
            return False, 0, skier_weight, None, None, None, None, None, None, iteration_count, elapsed_times, skier_weights, crack_lengths
    return check_first_criterion_v2,


@app.cell
def __(
    create_skier_object_v2,
    energy_criterion,
    find_minimum_force_v2,
    find_new_crack_length_v2,
    is_outside_stress_envelope,
    np,
    time,
):
    # This method is specifically used in instances when the original algorithm converges, but with a crack_length of zero

    def check_first_criterion_damped_outside_envelope(snow_profile, inclination, skier_weight, variance, envelope='reiweger'):

        # We use the variance to determine a suitable coefficient to scale
        standardized_std = np.sqrt(variance)/skier_weight*100

        print(f" STANDARDIZED STD: {standardized_std}")
        # Assuming nocrack case to begin with and create a skier-object
        crack_length = 0
        length = 100 * (sum(layer[1] for layer in snow_profile))  # Total length (mm)
        # length = 100 * 100 * 10  # Total length (mm) (one hundred meters in mm)
        # length = 100 * (sum(layer[1] for layer in snow_profile)) 
        # length = sum(li)

        k0 = [True, True, True, True]  # Support boolean for uncracked solution
        li = [length / 2, 0, 0, length / 2]  # Support boolean for uncracked solution
        ki = [True, True, True, True]  # Length of segments with foundations as specified by ki

        skier, C, segments, x_cm, sigma_kPa, tau_kPa = create_skier_object_v2(snow_profile, crack_length, skier_weight, inclination, li, ki, crack_case='nocrack')

        # For the initial skier object, check if we are outside the stress envelope at any point
        checker, dist_to_failure = is_outside_stress_envelope(sigma_kPa, -tau_kPa, envelope=envelope)

        # Time tracker
        start_time = time.time()
        elapsed_times = []

        # Tracker lists for skier weights and crack lengths
        skier_weights = []
        crack_lengths = []

        # Initialize iteration variables
        iteration_count = 0
        max_iterations = 40

        if checker.any() and not checker.all():
            # Find the weight associated with minimum critical force to initialize our algorithm (BASE CASE)
            skier_weight, *_ = find_minimum_force_v2(snow_profile, inclination, li, ki, envelope=envelope) 

            # Initialize variables for algorithm
            init_crack_length = 1  # Initial crack length
            err = 1000  # Error margin
            li = [length / 2 - init_crack_length / 2, init_crack_length / 2, init_crack_length / 2, length / 2 - init_crack_length / 2]
            ki = [True, False, False, True]





            while np.abs(err) > 0.001 and iteration_count < max_iterations and any(ki):
                # ki.any() ensures we move out in case we are outside the envelope in all points

                # Increment iteration counter
                iteration_count += 1


                # Track skier weight and crack length for each iteration
                skier_weights.append(skier_weight)
                crack_lengths.append(crack_length)

                # Time tracking for each iteration
                elapsed_times.append(time.time() - start_time)

                # Create the base_case with correct number of segments
                skier, C, segments, x_cm, sigma_kPa, tau_kPa = create_skier_object_v2(snow_profile, crack_length, skier_weight, inclination, li, ki, crack_case='nocrack')

                # Solving a cracked solution
                c_skier, c_C, c_segments, c_x_cm, c_sigma_kPa, c_tau_kPa = create_skier_object_v2(snow_profile, crack_length, skier_weight, inclination, li, ki, crack_case='crack')

                # print(f" Solution: {c_segments}")

                # Section to keep track of distance to failure
                checker_2, dist_to_failure_2 = is_outside_stress_envelope(sigma_kPa, -tau_kPa, envelope=envelope)
                # WHY IS THIS NOT THE SAME DISTANCE TO FAILURE AS THE LAST ONE IN find_min_force

                print(f" START OF ITERATION {iteration_count}: cracklength: {crack_length} mm, Skier Weight: {skier_weight} kg, Max Distance to Failure: {np.max(dist_to_failure_2)}")


                # The uncracked solution will have True for all values
                k0 = np.full(len(ki), True)

                # Calculate incremental energy released compared to (BASE CASE) solution above
                incr_energy = c_skier.ginc(C0=C, C1=c_C, phi=inclination, **c_segments, k0=k0)

                # Evaluate energy envelope (scaling by 1000 to convert kJ to J)
                g_delta = energy_criterion(1000 * incr_energy[1], 1000 * incr_energy[2])


                scaling = (g_delta**(-1/10))


                # We weight scaling to dampen the behavior
                # Greater standard deviations put more emphasis on dampening

                scaling = (standardized_std+scaling)/(standardized_std+1)


                # For any g_delta below 1, we are not outside the energy envelope and must increase the force
                current_normal_force, current_tangential_force = c_skier.get_skier_load(skier_weight, inclination)
                current_gravitational_force = np.sqrt(current_normal_force ** 2 + current_tangential_force ** 2)
                updated_gravitational_force = scaling * (current_gravitational_force)





                # We have now dampened the behavior

                # Updating error margin
                err = np.abs(updated_gravitational_force - current_gravitational_force) / updated_gravitational_force

                # For errors > margin we scale skier weight according to g_delta calculated above, and find new crack length
                if np.abs(err) > 0.001:
                    new_skier_weight = skier_weight * scaling

                    # For the updated skier force, we find all points where the weak layer is overloaded and use this as 

                    # the crack length in the next iteration (with li and ki specifying how the crack is positioned in the weak layer)

                    new_crack_length, li, ki = find_new_crack_length_v2(snow_profile, skier_weight, inclination, li, ki, envelope=envelope)
                    crack_length = new_crack_length
                    print(f" END OF ITERATION: g_delta: {g_delta} J/m^2, Old skier weight: {skier_weight} kg, Scaling: {scaling} kg, New skier weight: {new_skier_weight} kg, cracklength: {crack_length} mm,")

                    skier_weight = new_skier_weight

            # End of loop, i.e., convergence or max iteration reached
            if iteration_count < max_iterations and any(ki):
                print(f" CONVERGENCE: cracklength: {crack_length} mm, Critical Skier Weight: {skier_weight} kg, Distance to energy envelope: {g_delta} J/m^2, Max Distance to Stress Envelope: {np.max(dist_to_failure_2)}")
                return True, crack_length, skier_weight, c_skier, c_C, c_segments, c_x_cm, c_sigma_kPa, c_tau_kPa, iteration_count, elapsed_times, skier_weights, crack_lengths
            elif not any(ki):
                print("We are outside the envelope in all points")
                return True, crack_length, skier_weight, None, None, None, None, None, None, iteration_count, elapsed_times, skier_weights, crack_lengths
            else:
                # The issue of non-convergence is often bouncing too far above and too far below the solution. If we take the average of the approxima

                print("Maximum iterations reached without convergence.")
                skier_weight = np.average(skier_weights)

                return False, crack_length, skier_weight, None, None, None, None, None, None, iteration_count, elapsed_times, skier_weights, crack_lengths

        elif checker.all():
            # Extreme case (i) we are outside the boundary at all points
            crack_length = length
            skier_weight = 0

            # Elapsed time is zero

            return True, crack_length, skier_weight, None, None, None, None, None, None, iteration_count, elapsed_times, skier_weights, crack_lengths

        else:
            # Extreme case (ii) We do not fulfill the stress criterion in any point, and will therefore not be able to trigger an avalanche
            return False, 0, skier_weight, None, None, None, None, None, None, iteration_count, elapsed_times, skier_weights, crack_lengths
    return check_first_criterion_damped_outside_envelope,


@app.cell
def __(
    create_skier_object_v2,
    energy_criterion,
    find_minimum_force_v2,
    find_new_crack_length_v2,
    is_outside_stress_envelope,
    np,
    time,
):
    # This method is specifically used in instances when the original algorithm will not converge, as we bounce between solutions 

    def check_first_criterion_damped(snow_profile, inclination, skier_weight, variance, envelope='reiweger'):

        # We use the variance to determine a suitable coefficient to scale
        standardized_std = np.sqrt(variance)/skier_weight*100

        print(f" STANDARDIZED STD: {standardized_std}")
        # Assuming nocrack case to begin with and create a skier-object
        crack_length = 0
        length = 100 * (sum(layer[1] for layer in snow_profile))  # Total length (mm)
        # length = 100 * 100 * 10  # Total length (mm) (one hundred meters in mm)
        # length = 100 * (sum(layer[1] for layer in snow_profile)) 
        # length = sum(li)

        k0 = [True, True, True, True]  # Support boolean for uncracked solution
        li = [length / 2, 0, 0, length / 2]  # Support boolean for uncracked solution
        ki = [True, True, True, True]  # Length of segments with foundations as specified by ki

        skier, C, segments, x_cm, sigma_kPa, tau_kPa = create_skier_object_v2(snow_profile, crack_length, skier_weight, inclination, li, ki, crack_case='nocrack')

        # For the initial skier object, check if we are outside the stress envelope at any point
        checker, dist_to_failure = is_outside_stress_envelope(sigma_kPa, -tau_kPa, envelope=envelope)

        # Time tracker
        start_time = time.time()
        elapsed_times = []

        # Tracker lists for skier weights and crack lengths
        skier_weights = []
        crack_lengths = []

        # Initialize iteration variables
        iteration_count = 0
        max_iterations = 40

        if checker.any() and not checker.all():
            # Find the weight associated with minimum critical force to initialize our algorithm (BASE CASE)
            skier_weight, *_ = find_minimum_force_v2(snow_profile, inclination, li, ki, envelope=envelope) 

            # Initialize variables for algorithm
            init_crack_length = 1  # Initial crack length
            err = 1000  # Error margin
            li = [length / 2 - init_crack_length / 2, init_crack_length / 2, init_crack_length / 2, length / 2 - init_crack_length / 2]
            ki = [True, False, False, True]





            while np.abs(err) > 0.001 and iteration_count < max_iterations and any(ki):
                # ki.any() ensures we move out in case we are outside the envelope in all points

                # Increment iteration counter
                iteration_count += 1


                # Track skier weight and crack length for each iteration
                skier_weights.append(skier_weight)
                crack_lengths.append(crack_length)

                # Time tracking for each iteration
                elapsed_times.append(time.time() - start_time)

                # Create the base_case with correct number of segments
                skier, C, segments, x_cm, sigma_kPa, tau_kPa = create_skier_object_v2(snow_profile, crack_length, skier_weight, inclination, li, ki, crack_case='nocrack')

                # Solving a cracked solution
                c_skier, c_C, c_segments, c_x_cm, c_sigma_kPa, c_tau_kPa = create_skier_object_v2(snow_profile, crack_length, skier_weight, inclination, li, ki, crack_case='crack')

                # print(f" Solution: {c_segments}")

                # Section to keep track of distance to failure
                checker_2, dist_to_failure_2 = is_outside_stress_envelope(sigma_kPa, -tau_kPa, envelope=envelope)
                # WHY IS THIS NOT THE SAME DISTANCE TO FAILURE AS THE LAST ONE IN find_min_force

                print(f" START OF ITERATION {iteration_count}: cracklength: {crack_length} mm, Skier Weight: {skier_weight} kg, Max Distance to Failure: {np.max(dist_to_failure_2)}")


                # The uncracked solution will have True for all values
                k0 = np.full(len(ki), True)

                # Calculate incremental energy released compared to (BASE CASE) solution above
                incr_energy = c_skier.ginc(C0=C, C1=c_C, phi=inclination, **c_segments, k0=k0)

                # Evaluate energy envelope (scaling by 1000 to convert kJ to J)
                g_delta = energy_criterion(1000 * incr_energy[1], 1000 * incr_energy[2])


                scaling = (g_delta**(-1/10))


                # We weight scaling to dampen the behavior
                # Greater standard deviations put more emphasis on dampening

                scaling = (standardized_std+scaling)/(standardized_std+1)


                # For any g_delta below 1, we are not outside the energy envelope and must increase the force
                current_normal_force, current_tangential_force = c_skier.get_skier_load(skier_weight, inclination)
                current_gravitational_force = np.sqrt(current_normal_force ** 2 + current_tangential_force ** 2)
                updated_gravitational_force = scaling * (current_gravitational_force)





                # We have now dampened the behavior

                # Updating error margin
                err = np.abs(updated_gravitational_force - current_gravitational_force) / updated_gravitational_force

                # For errors > margin we scale skier weight according to g_delta calculated above, and find new crack length
                if np.abs(err) > 0.001:
                    new_skier_weight = skier_weight * scaling

                    # For the updated skier force, we find all points where the weak layer is overloaded and use this as 

                    # the crack length in the next iteration (with li and ki specifying how the crack is positioned in the weak layer)

                    new_crack_length, li, ki = find_new_crack_length_v2(snow_profile, skier_weight, inclination, li, ki, envelope=envelope)
                    crack_length = new_crack_length
                    print(f" END OF ITERATION: g_delta: {g_delta} J/m^2, Old skier weight: {skier_weight} kg, Scaling: {scaling} kg, New skier weight: {new_skier_weight} kg, cracklength: {crack_length} mm,")

                    skier_weight = new_skier_weight

            # End of loop, i.e., convergence or max iteration reached
            if iteration_count < max_iterations and any(ki):
                print(f" CONVERGENCE: cracklength: {crack_length} mm, Critical Skier Weight: {skier_weight} kg, Distance to energy envelope: {g_delta} J/m^2, Max Distance to Stress Envelope: {np.max(dist_to_failure_2)}")
                return True, crack_length, skier_weight, c_skier, c_C, c_segments, c_x_cm, c_sigma_kPa, c_tau_kPa, iteration_count, elapsed_times, skier_weights, crack_lengths
            elif not any(ki):
                print("We are outside the envelope in all points")
                return True, crack_length, skier_weight, None, None, None, None, None, None, iteration_count, elapsed_times, skier_weights, crack_lengths
            else:
                # The issue of non-convergence is often bouncing too far above and too far below the solution. If we take the average of the approxima

                print("Maximum iterations reached without convergence.")
                skier_weight = np.average(skier_weights)

                return False, crack_length, skier_weight, None, None, None, None, None, None, iteration_count, elapsed_times, skier_weights, crack_lengths

        elif checker.all():
            # Extreme case (i) we are outside the boundary at all points
            crack_length = length
            skier_weight = 0

            # Elapsed time is zero

            return True, crack_length, skier_weight, None, None, None, None, None, None, iteration_count, elapsed_times, skier_weights, crack_lengths

        else:
            # Extreme case (ii) We do not fulfill the stress criterion in any point, and will therefore not be able to trigger an avalanche
            return False, 0, skier_weight, None, None, None, None, None, None, iteration_count, elapsed_times, skier_weights, crack_lengths
    return check_first_criterion_damped,


@app.cell
def __(create_skier_object_v2, is_outside_stress_envelope, np):
    def find_new_crack_length_v2(snow_profile, skier_weight_z, inclination, li, ki, envelope='reiweger'):

        # This version assumes a full-crack from first to last, without the uncracked segment in the middle


        crack_length = 0

        print("INSIDE FIND NEW CRACK LENGTH METHOD")
        skier, C, segments, x_cm, sigma_kPa, tau_kPa = create_skier_object_v2(
            snow_profile, crack_length, skier_weight_z, inclination, li, ki, crack_case='nocrack') 

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

        print("Switches Indices:", switches, x_cm[switches+1], dist_to_fail_array[switches+1])
        #print("Switches Indices:", switches, x_cm[switches+1], dist_to_fail_array[switches+1])

        # This new version just takes the first and last instances



        # Ensure switches + 1 are within bounds
        if switches.size > 0:

            start_crack = switches[0]
            end_crack = switches[-1]

            switches_short = np.array([start_crack, end_crack])
            print(type(switches_short)) 
            print(switches_short) 



            # OLD
            # ki = [foundations[0]]
            # ki.extend(foundations[switches + 1])

            # NEW
            ki = [foundations[0]]

            ki.extend(foundations[switches_short+1])
            # ki.extend(foundations[switches_short])

            # Constructing segment boundaries

            # OLD
            # segment_boundaries = [x_cm_array[0]]  # Start with the first point
            #segment_boundaries.extend(x_cm_array[switches+1])  # Append the points where switches occur
            #segment_boundaries.append(x_cm_array[-1])  # End with the last point

            # NEW - only two points of interest
            segment_boundaries = [x_cm_array[0]]  # Start with the first point
            segment_boundaries.extend(x_cm_array[switches_short+1])
            #segment_boundaries.extend(x_cm_array[switches_short])  # Append the 
            segment_boundaries.append(x_cm_array[-1]) # Last point


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

        else:
            ki = [foundations[0],foundations[0], foundations[-1], foundations[-1]]  # If there are no switches, we are on the same side of the envelope in all points

            # This should mean that we are outside the envelope in all places
            total_length = np.sum(li)
            midpoint = total_length / 2

            li = [total_length/2,0,0, total_length/2] # We just make sure to split the segment in half



        # Calculate new crack length
        new_crack_length = sum(length for length, foundation in zip(li, ki) if not foundation)

        return new_crack_length, li, ki
    return find_new_crack_length_v2,


@app.cell
def __(
    create_skier_object,
    create_skier_object_v2,
    is_outside_stress_envelope,
    np,
):
    def find_minimum_force_v2(snow_profile, inclination, li, ki, envelope='reiweger'):
        # Initial parameters
        crack_length = 0
        crack_case = 'nocrack'
        skier_weight = 1  # Starting weight of skier

        #ToDo: make this use v2

        # Create a skier object with no weight and check if it is already outside the envelope
        skier, C, segments, x_cm, sigma_kPa, tau_kPa = create_skier_object_v2(snow_profile, crack_length, skier_weight, inclination, li, ki, crack_case='nocrack') 

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
    return find_minimum_force_v2,


@app.cell
def __(np, weac):
    def create_skier_object_v2(snow_profile, crack_length, skier_weight_x, inclination, li_x, ki_x, crack_case='nocrack'):

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

        mi_x[median_index] = skier_weight_x  # Assign skier_weight to the median index

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


if __name__ == "__main__":
    app.run()
