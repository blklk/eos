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
    parser = argparse.ArgumentParser(description="Calculate the Birch-Murnaghan and Vinet EOS from .xlsx data.")
    parser.add_argument('filename', type=str, help='Path to the .xlsx file')
    parser.add_argument('pressure_column', type=str, help='Name of the pressure column')
    parser.add_argument('volume_column', type=str, help='Name of the volume column')
    parser.add_argument('output_file', type=str, help='Name of the output figure file')
    args = parser.parse_args()

    data = read_data(args.filename, [args.pressure_column, args.volume_column])

    # Ensure required columns exist in the dataframe
    if not {args.pressure_column, args.volume_column}.issubset(data.columns):
        print(f"Error: not all columns {args.pressure_column}, {args.volume_column} exist in the data.")
        exit()

    # Convert data to numpy arrays for optimization
    V = np.array(data[args.volume_column])
    P = np.array(data[args.pressure_column])

    # Initial guesses for V0, K0, K0_prime
    initial_guess = [V[0], 1, 1]

    # Fit the Birch-Murnaghan equation to the data
    try:
        popt_bm, pcov_bm = curve_fit(birch_murnaghan, V, P, p0=initial_guess)
        print(f"Birch-Murnaghan optimized parameters: V0={popt_bm[0]}, K0={popt_bm[1]}, K0_prime={popt_bm[2]}")
    except Exception as e:
        print(f"Error in Birch-Murnaghan curve fitting: {e}")
        exit()

    # Fit the Vinet equation to the data
    try:
        popt_vinet, pcov_vinet = curve_fit(vinet, V, P, p0=initial_guess)
        print(f"Vinet optimized parameters: V0={popt_vinet[0]}, K0={popt_vinet[1]}, K0_prime={popt_vinet[2]}")
    except Exception as e:
        print(f"Error in Vinet curve fitting: {e}")
        exit()

    # Plotting the data and fitted curves
    plt.plot(birch_murnaghan(V, *popt_bm), V,  ':', color='gray',label='Birch-Murnaghan Fit:\nV0=%5.3f\nK0=%5.3f\nK0_prime=%5.3f' % tuple(popt_bm))
    #plt.plot(vinet(V, *popt_vinet), V,  ':', color='red',label='Vinet Fit: V0=%5.3f, K0=%5.3f, K0_prime=%5.3f' % tuple(popt_vinet))
    plt.plot(P, V, 'o', ms=5 ,color='mediumblue',markeredgecolor='black', label='Data')
    plt.ylabel('Volume')
    plt.xlabel('Pressure')
    plt.title('EOS: MgSiO3 Bridgmanite')
    plt.legend(loc='upper right')
    plt.savefig(args.output_file)
    plt.show()

if __name__ == "__main__":
    main()
