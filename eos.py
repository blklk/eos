import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse
from scipy.optimize import curve_fit


# Birch-Murnaghan equation of state
def birch_murnaghan(V, V0, K0, K0_prime):
    """
    Birch-Murnaghan 3rd order equation of state.
    """
    K0=160
    #K0_prime=5
    return (3/2) * K0 * ((V0/V)**(7/3) - (V0/V)**(5/3)) * (1 + 3/4 * (K0_prime - 4) * ((V0/V)**(2/3) - 1))


def vinet(V, V0, K0, K0_prime):
    """
    Vinet equation of state.
    """
    x = (V/V0)**(1/3)
    eta = 3/2 * (K0_prime - 1)
    return 3*K0*(1-x)*np.exp(eta*(1-x))


def read_data(filename, columns):
    """
    Function to read data from .xlsx file.
    """
    try:
        df = pd.read_excel(filename, usecols=columns)
        return df
    except Exception as e:
        print(f"Error reading file: {e}")
        exit()


def main():
    # Define command line arguments
    parser = argparse.ArgumentParser(description="Calculate the Birch-Murnaghan and Vinet EOS from multiple .xlsx data.")
    parser.add_argument('figure_title', type=str, help='Title of the figure')
    parser.add_argument('output_file', type=str, help='Name of the output figure file')
    parser.add_argument('filename', type=str, help='Path to the .xlsx file')
    parser.add_argument('--pressures', nargs='+', help='Names of the pressure columns')
    parser.add_argument('--volumes', nargs='+', help='Names of the volume columns')
    parser.add_argument('--colors', nargs='+', default=['mediumblue', 'red', 'green', 'purple'], help='Plot colors for each dataset')
    args = parser.parse_args()

    # Ensure that the number of pressure and volume columns are equal
    if len(args.pressures) != len(args.volumes):
        print(f"Error: Number of pressure columns and volume columns must be equal.")
        exit()

    # Read the data from the file
    data = read_data(args.filename, args.pressures + args.volumes)
    data = data.interpolate()

    # Process each pressure-volume pair
    for i in range(len(args.pressures)):
        # Ensure required columns exist in the dataframe
        if not {args.pressures[i], args.volumes[i]}.issubset(data.columns):
            print(f"Error: not all columns {args.pressures[i]}, {args.volumes[i]} exist in the data.")
            exit()

        P = np.array(data[args.pressures[i]])
        V = np.array(data[args.volumes[i]])

        # Skip the data if there are missing values
        if np.isnan(P).any() or np.isnan(V).any():
            print(
                f"Warning: missing values in data for pressure column {args.pressures[i]} and volume column {args.volumes[i]}. Skipping this data.")
            continue

        # Initial guesses for V0, K0, K0_prime
        initial_guess =  [V[0], 160, 5]


        # Fit the Birch-Murnaghan equation to the data
        try:
            popt_bm, pcov_bm = curve_fit(birch_murnaghan, V, P, p0=initial_guess, maxfev = 5000)
            print(
                f"Birch-Murnaghan optimized parameters for pressure column {args.pressures[i]} and volume column {args.volumes[i]}: V0={popt_bm[0]}, K0={popt_bm[1]}, K0_prime={popt_bm[2]}")
        except Exception as e:
            print(
                f"Error in Birch-Murnaghan curve fitting for pressure column {args.pressures[i]} and volume column {args.volumes[i]}: {e}")
            exit()

        # Fit the Vinet equation to the data
        try:
            popt_vinet, pcov_vinet = curve_fit(vinet, V, P, p0=initial_guess)
            print(
                f"Vinet optimized parameters for pressure column {args.pressures[i]} and volume column {args.volumes[i]}: V0={popt_vinet[0]}, K0={popt_vinet[1]}, K0_prime={popt_vinet[2]}")
        except Exception as e:
            print(
                f"Error in Vinet curve fitting for pressure column {args.pressures[i]} and volume column {args.volumes[i]}: {e}")
            exit()

        plt.plot(birch_murnaghan(V, *popt_bm), V, ':', color=args.colors[i % len(args.colors)],
                 label=f'Birch-Murnaghan Fit:\nV0=%5.3f\nK0=%5.3f\nK0_prime=%5.3f' % tuple(popt_bm))
        #plt.plot(vinet(V, *popt_vinet), V, ':', color='blue',
         #        label=f'Vinet Fit:\nV0=%5.3f\nK0=%5.3f\nK0_prime=%5.3f' % tuple(popt_vinet))
        plt.plot(P, V, 'o', ms=5, color=args.colors[i % len(args.colors)], markeredgecolor='black', label=f'{args.volumes[i]}')

        plt.ylabel('Volume')
        plt.xlabel('Pressure')
        plt.title(args.figure_title)
        plt.legend(bbox_to_anchor=(1., 1), loc='upper left')
        plt.tight_layout()
        plt.savefig(args.output_file, dpi=800)

if __name__ == "__main__":
    main()
