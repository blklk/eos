# eos

There are 2 Python **.py** files to choose from, both serving the same purpose. The key differences between them are outlined below. In both source codes, you can modify the initial guesses for 
*K0* and *K0'* within the **MAIN** function. Additionally, you have the option to fix *K0* and *K0'* in the **BM** and **Vinet** functions, which can be useful when dealing with low-quality data.

## eos.py
This version is simpler and more straightforward. It reads a .xlsx file, specifically one pressure column and one volume column. The resulting plot is saved.

To run the code, follow these steps:

1. Place the eos.py file in the same directory as your .xlsx data file.
2. Open your terminal.
3. Navigate to the folder containing the files.
4. Execute the following command: **'python eos.py DATA.xlsx PRESSURE_COLUMN VOLUME_COLUMN SAVEFIG_NAME.png'**

## eos_addition.py
This version is slightly more complex, but still easy to understand. It reads a **.xlsx** file, allowing you to specify multiple **pressure columns** and **volume columns** to process. The data points are plotted using the volume column headers as labels, which are extracted from the **.xlsx** file. The resulting plot is saved.

To run the code, follow these steps:

1. Place the eos_addition.py file in the same directory as your .xlsx data file.
2. Open your terminal.
3. Navigate to the folder containing the files.
4. Execute the following command: **'python eos.py DESIRED_TITLE_OF_PLOT SAVEFIG_NAME.png DATA.xlsx --pressures PRESSURE_COLUMN1 PRESSURE_COLUMN2 --volumes VOLUME_COLUMN1 VOLUME_COLUMN2'**
