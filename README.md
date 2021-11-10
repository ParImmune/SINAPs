#######################################################################################################################~
#
# Copyright Par'Immune 2021 - GPL-3.0-only
#
# SINAPs is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
#
#######################################################################################################################~


################
# Requirements #
################

- Required OS for SINAPs software = Linux (tested under Ubuntu 18.04 LTS and 20.04 LTS), but can work under Windows and Mac using Anaconda
- Required OS for SINAPs visualization plugin = Windows, Linux, Mac (tested under Windows 10, MacOS Catalina, Ubuntu 18.04 LTS and 20.04 LTS)

- Required Python 3 version = Python 3.7
- Required Python 3 packages = Pytraj via ambermd, Biopython
- No UCSF Chimera version required, but a recent build is recommended (1.14 or 1.15)


################
# Installation #
################

Recommended installation (via conda) :
> conda create --name SINAPs python=3.7
> source activate SINAPs
> conda install -c ambermd pytraj
> conda install biopython

Before launching the SINAPs software, activate first the SINAPs conda environment:
> source activate SINAPs
> python3 ....../SINAPs.py

It is also possible to add a command in the .bashrc file to launch the program with the command "SINAPs":
> alias SINAPs="source activate SINAPs ; python3 /data/SINAPs/SINAPs_V1/SINAPs.py"

Implementation of the SINAPs visualization plugin in UCSF Chimera:
> Tools >> Additional Tools >> Add third-party plugin location >> Add..
> Specify the path to the SINAPs folder (/!\ Do not specify the SINAPs_Visualizer folder, but the previous one /!\)


#######################
# General information #
#######################

- Input files:
	- AMBER trajectories (parm7/nc but other format are tolerated)
	- GROMACS trajectories (pdb/xtc, or top/trr with the addition of all itp files in the folder as well as the forcefield folder used)
	- PDB files (simple files or PDB trajectories)
- Add all the hydrogen.
- The structures must have exactly the same number of amino acids positionned in the same place (the type of the amino acids is not important). In case of difference, it is mandatory to remove all amino acids without correspondance.
- Only the 20 proteinogenic amino acids were tested.


################
# Using SINAPs #
################

Using SINAPs :
- Information to be specified:
	- Input files
	- Output folder created beforehand (an option to create the output folder automatically will be added in the future).
- The output folder must be unique for each analysis.
- The representative frame can take "first", "last", or the key frame number as argument.
- "Frequency min cutoff (%)" allows you to only keep in the output the interactions with a frequency greater than or equal to the argument. However, it is not recommended to change it.
- It is possible to study interaction networks in a single simulation/structure by specifying the same file twice. The observation in UCSF Chimera allows to highlight the main interactions realized in this single case, without comparison.

Using UCSF Chimera SINAPs plugin:
- Tools >> SINAPs >> SINAPs Visualizer
- Specify the folder containing the output files, then load data
- The frequency bar allows you to display only the bonds with a frequency greater than or equal to the chosen cutoff
- For the moment, only the backbone can be displayed (to simplify the representation as much as possible). However, it is possible to overcome this choice by manually loading a PDB structure with side chains, and aligning it to the structures opened by SINAPs.


