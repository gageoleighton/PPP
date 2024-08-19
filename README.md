Protein Param Pro (PPP) is a simple program for storing and retrieving protein sequences as a way for me to lear how to code in Python with PyQt/PySide paackage.

# Usage

## Screenshots
![Input](/screenshots/Protein_Input.PNG)
![Summary](/screenshots/Protein_Summary.PNG)
![Concentration](/screenshots/Protein_Concentration.PNG)

## Quirks
* Since I'm a newbie at coding using PySide there are likely bugs.
* Critically, calculations or protein concentration have been extensively tested.
* Double click list view to deselect all entries
* Select and ctrl+C summary table element to copy.
  * Note: you must first deselect the row headers then reselect to properly copy.

#Installation

## Linux
It should run on all Linux distros but is largely untested.
Eventually I will migrate to install and update using native package manager.

## MacOS
PPP should run on macOS running Ventura (13) or newer. Support for older macs is being considered.

Due to the requirements set by Apple for code signing apps ($99/year) a message will probably appear reporting it as "corrupt".
If so, please run the following command in terminal:
`xattr -cr /path/to/application.app`

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
