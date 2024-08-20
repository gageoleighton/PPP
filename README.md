Protein Param Pro (PPP) is a simple program for storing and retrieving protein sequences as a way for me to learn how to code in Python with the PyQt/PySide package.

All user data is only stored on your local device. However, errors are reported to sentry so that I can assess needed bugfixes. This may pass along protein name and sequence.

# Usage

## Screenshots
![Input](/screenshots/Protein_Input.PNG)
![Summary](/screenshots/Protein_Summary.PNG)
![Concentration](/screenshots/Protein_Concentration.PNG)

## Quirks
* Since I'm a newbie at coding using PySide there are likely bugs.
* Critically, calculations and protein concentration have been extensively tested.
* Double click list view to deselect all entries
* Select and ctrl+C summary table element to copy.
  * Note: you must first deselect the row headers then reselect to properly copy.

## Roadmap
* Detect when updates are available.
* Option to use program without sentry integration.
* Arrange and show list in collapsable folders.
* On "Export" only export entries that are selected.
* Add notification on sucessful copy of summary table items.
* Additional display of protein information including:
 * Rolling isoelectric point plot.
 * Disorder/order plot.
 * Summary of amino acids and distribution.

# Installation

## Linux
To be released.

## MacOS
PPP should run on any macOS with Ventura (13) or newer. Support for older macs is being considered.

Due to the requirements set by Apple for code signing apps ($99/year) a message will probably appear reporting PPP as "corrupt".
If so, please run the following command in terminal before mounting the dmg:

`xattr -cr /path/to/protein.param.pro.dmg`

On subsequent launches you should not need to do this again unless updating to a newer version.

## Windows
Provided as a standalone program (portable) or as an installer to -> Program Files.
This should work natively on all Windows devices but I have not done extensive testing. Please leave an issue if you have any trouble.

# Acknowledgements

## Lab
Thanks to all the beta testers at NIEHS!

## Python packages
* Largely based on [BioPython](https://biopython.org/) for calculation of various protein parameters.
* Build on [PySide6](https://doc.qt.io/qtforpython-6/)
* Additionally, using [PyQtDarkTheme](https://pypi.org/project/pyqtdarktheme/)
* Errors are automatically reported using [sentry](https://sentry.io)
