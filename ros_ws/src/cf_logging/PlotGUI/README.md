# Plot GUI for SD-log-data

Plotting the data from the logging of the crazyflies on a SD card. Creating up to 3x3 plots to compare multiple dataseries.

## Usage

   1. Start the GUI with `python3 PlotGUI.py`
   2. Load a data file from the SD card from the menu bar ("File / Open File", CTRL+O)
   3. Choose the grid size for your plots ("Edit / Grid", CTRL+G)
   4. Configure your plot axes by double-clicking on the plots. Choose the corresponding label of the dataseries from the dropdown-list in the new window or enter the label directly.
   5. Move and resize your data with the toolbar at the bottom

## Convert data to .mat files

   To evaluate your data in Matlab, you can follow the steps below:
   1. Collect the log-files from the SD cards in one folder (without subfolders).
   2. Run the script `save_to_mat.py` by choosing your `input_dir` as the directory with the log-files and the `output_dir` as the directory of your matlab-files. Hereby, the output directory does not need to be existing.
   ```
      python save_to_mat.py -i input_dir -o output_dir
   ```
   3. Load the .mat-files into your Matlab working directory and start evaluating.


## Example

   The directory `/example_data` contains two examples of log-data from crazyflies. Use these to test the GUI and the script.


## Troubleshoot

   - Plot is empty after entering the labels
      Check again the correct spelling of the labels and/or if the data-file is loaded.
   - How to check, if the file is loaded?
      Check the info-window ("Edit / Info", CTRL+I), if a filename is present and correct.
   - Choose your grid before loading data into the subplots
      Changing the grid size will erase the current subplots.
