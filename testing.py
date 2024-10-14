import marimo

__generated_with = "0.8.15"
app = marimo.App(width="medium")


@app.cell
def __():
    import numpy as np

    # Example input
    x_cm_test = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 11.5,11.75, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22])
    dist_to_fail_test = np.array([0.5, 0.5, 0.5, 0.5, 0.5, 1.5, 1.0, 1.5, 0.5, 0.5, 1.5, 1.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5,0.5,0.5])
    checker_test = np.array([False, False, False, False, False, True, True, True, False, False, True, True, False, False, False, False, False, False, False, False, False, False, False,False,False])
    return checker_test, dist_to_fail_test, np, x_cm_test


@app.cell
def __(checker_test, dist_to_fail_test, np, x_cm_test):
    # Now we will create a simplified script

    switches = np.where(np.diff(np.sign(dist_to_fail_test - 0.999)))[0]
    ki = checker_test[switches+1]

    x_cm_test[0]

    segment_boundaries = np.concatenate((np.array(x_cm_test[0]), np.array(x_cm_test[switches+1]), np.array([len(x_cm_test)])))
    li = np.diff(segment_boundaries)

    print(switches)

    print(ki)

    print(segment_boundaries)


    print(li)



    return ki, li, segment_boundaries, switches


if __name__ == "__main__":
    app.run()
