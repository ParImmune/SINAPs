#! /usr/bin/env python3

#######################################################################################################################~
#
# SINAPs V1.0 - Analyzer
#
#######################################################################################################################~

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

from tkinter import filedialog
from tkinter import ttk
import tkinter.font as tkFont
from tkinter import *

import SINAPs_functions

#######################################################################################################################~

class SINAPs_GUI(Frame):
    def __init__(self, gui):
        Frame.__init__(self)
        self.pack()

        global initdir
        initdir = "~/"

        ###############~

        global font1 ; global font1_bold ; global font2

        baseFont = tkFont.nametofont("TkDefaultFont")
        baseFont.configure(family="Arial", size="10")
        baseFont_bold = tkFont.Font(family="Arial", size="10", weight="bold")

        textFont = tkFont.nametofont("TkTextFont")
        textFont.configure(family="Arial", size="10")

        notebook_style = ttk.Style()
        notebook_style.configure("Custom.TNotebook.Tab", font="Arial 12 bold")

        font1 = tkFont.Font(family="Arial", size="12")
        font1_bold = tkFont.Font(family="Arial", size="12", weight="bold")

        font2 = tkFont.Font(family="Arial", size="8")
        font2_bold = tkFont.Font(family="Arial", size="8", weight="bold")

        ###############~

        SINAPs_parameters = ["SINAPs_results", "first", 1, 3.5, 135, 5.0, 135, 3.0, 5.0, 30, 4.5, 7.0]

        ###############~

        ##### NOTEBOOK TABS #####
        self.tabs = ttk.Notebook(self, style = "Custom.TNotebook")
        self.tabs.grid()

        # AMBER TRAJECTORY TAB
        self.ambertrajectory = Frame(self)
        self.ambertrajectory.grid()
        self.tabs.add(self.ambertrajectory, text="Amber trajectories")

        # GROMACS TRAJECTORY TAB
        self.gmxtrajectory = Frame(self)
        self.gmxtrajectory.grid()
        self.tabs.add(self.gmxtrajectory, text="GROMACS trajectories")
        
        # PDB FILES TAB
        self.pdbfiles = Frame(self)
        self.pdbfiles.grid()
        self.tabs.add(self.pdbfiles, text="PDB files")


        ##### AMBER TRAJECTORIES #####~
        # 1ST BLOCK
        self.amb_firstblock = LabelFrame(self.ambertrajectory, text = "Amber Trajectory #1", font = baseFont_bold)
        self.amb_firstblock.grid(row = 0, sticky = 'W', padx = 5, pady = 5, ipadx = 5, ipady = 5)
        self.amb_firstblock.grid_columnconfigure(0, weight = 1)

        # 2ND BLOCK
        self.amb_secondblock = LabelFrame(self.ambertrajectory, text = "Amber Trajectory #2", font = baseFont_bold)
        self.amb_secondblock.grid(row = 1, sticky = 'W', padx = 5, pady = 5, ipadx = 5, ipady = 5)
        self.amb_secondblock.grid_columnconfigure(0, weight=1)


        ##### PDB TRAJECTORIES #####~
        self.pdb_firstblock = LabelFrame(self.pdbfiles, text = "PDB files", font = baseFont_bold)
        self.pdb_firstblock.grid(row = 0, sticky = 'W', padx = 5, pady = 5, ipadx = 5, ipady = 5)
        self.pdb_firstblock.grid_columnconfigure(0, weight = 1)


        ##### GROMACS TRAJECTORIES #####~
        self.gmx_firstblock = LabelFrame(self.gmxtrajectory, text = "GROMACS Trajectory #1", font = baseFont_bold)
        self.gmx_firstblock.grid(row = 0, sticky = 'W', padx = 5, pady = 5, ipadx = 5, ipady = 5)
        self.gmx_firstblock.grid_columnconfigure(0, weight = 1)

        # 2ND BLOCK
        self.gmx_secondblock = LabelFrame(self.gmxtrajectory, text = "GROMACS Trajectory #2", font = baseFont_bold)
        self.gmx_secondblock.grid(row = 1, sticky = 'W', padx = 5, pady = 5, ipadx = 5, ipady = 5)
        self.gmx_secondblock.grid_columnconfigure(0, weight=1)

        ##### OUTPUT PARAMETERS #####~
        self.outputblock = LabelFrame(self, text = "Output parameters", font = font1_bold, width = 600, height = 70)
        self.outputblock.grid(row = 2, column = 0, sticky = 'W', padx = 5, pady = 5, ipadx = 5, ipady = 5)
        self.outputblock.grid_propagate(0)

        ##### ADVANCED PARAMETERS #####~
        self.advancedblock = LabelFrame(self, text = "Advanced parameters", font = font1_bold, width = 683, height = 200)
        self.advancedblock.grid(row = 3, sticky = 'W', padx = 5, pady = 5, ipadx = 5, ipady = 5)
        self.advancedblock.grid_propagate(0)

        self.generalblock = LabelFrame(self.advancedblock, text = "General parameters", font = baseFont_bold, width = 210, height = 75)
        self.generalblock.grid(row = 0, column = 0, sticky = 'W', padx = 5, pady = 5, ipadx = 5, ipady = 5)
        self.generalblock.grid_propagate(0)

        self.HBblock = LabelFrame(self.advancedblock, text = "Hydrogen bonds parameters", font = baseFont_bold, width = 210, height = 75)
        self.HBblock.grid(row = 0, column = 1, sticky = 'W', padx = 5, pady = 5, ipadx = 5, ipady = 5)
        self.HBblock.grid_propagate(0)
        
        self.SBblock = LabelFrame(self.advancedblock, text = "Salt bridges parameters", font = baseFont_bold, width = 210, height = 75)
        self.SBblock.grid(row = 0, column = 2, sticky = 'W', padx = 5, pady = 5, ipadx = 5, ipady = 5)
        self.SBblock.grid_propagate(0)

        self.Pblock = LabelFrame(self.advancedblock, text = "Pi-Stacking parameters", font = baseFont_bold, width = 210, height = 75)
        self.Pblock.grid(row = 1, column = 0, sticky = 'W', padx = 5, pady = 5, ipadx = 5, ipady = 5)
        self.Pblock.grid_propagate(0)

        self.TLblock = LabelFrame(self.advancedblock, text = "T/L-Shapes parameters", font = baseFont_bold, width = 210, height = 75)
        self.TLblock.grid(row = 1, column = 1, sticky = 'W', padx = 5, pady = 5, ipadx = 5, ipady = 5)
        self.TLblock.grid_propagate(0)

        ##### FOOTER #####~
        self.footer = LabelFrame(self)
        self.footer.grid(row=6)

        self.footer2 = LabelFrame(self)
        self.footer2.grid(row = 7)

        ################################################################################################################

        ##### AMBER TRAJECTORIES #####~
        # TRAJECTORY #1 - PARM
        self.file1_ambparm_label = Label(self.amb_firstblock, text = "Topology:", width = 10)
        self.file1_ambparm_label.grid(row = 0, column = 0)

        self.file1_ambparm_entry = Entry(self.amb_firstblock, width = 50)
        self.file1_ambparm_entry.grid(row = 0, column = 1)

        self.file1_ambparm_browse = Button(self.amb_firstblock, text = "Browse", command=self.file1_ambparm_browsing)
        self.file1_ambparm_browse.grid(row = 0, column = 2)

        # TRAJECTORY #1 - TRAJ
        self.file1_ambtraj_label = Label(self.amb_firstblock, text = "Trajectory:", width = 10)
        self.file1_ambtraj_label.grid(row = 1, column = 0)

        self.file1_ambtraj_entry = Entry(self.amb_firstblock, width = 50)
        self.file1_ambtraj_entry.grid(row = 1, column = 1)

        self.file1_ambtraj_browse = Button(self.amb_firstblock, text = "Browse", command=self.file1_ambtraj_browsing)
        self.file1_ambtraj_browse.grid(row = 1, column = 2)

        # TRAJECTORY #2 - PARM
        self.file2_ambparm_label = Label(self.amb_secondblock, text = "Topology:", width = 10)
        self.file2_ambparm_label.grid(row = 0, column = 0)

        self.file2_ambparm_entry = Entry(self.amb_secondblock, width = 50)
        self.file2_ambparm_entry.grid(row = 0, column = 1)

        self.file2_ambparm_browse = Button(self.amb_secondblock, text = "Browse", command=self.file2_ambparm_browsing)
        self.file2_ambparm_browse.grid(row = 0, column = 2)

        # TRAJECTORY #2 - TRAJ
        self.file2_ambtraj_label = Label(self.amb_secondblock, text = "Trajectory:", width = 10)
        self.file2_ambtraj_label.grid(row = 1, column = 0)

        self.file2_ambtraj_entry = Entry(self.amb_secondblock, width = 50)
        self.file2_ambtraj_entry.grid(row = 1, column = 1)

        self.file2_ambtraj_browse = Button(self.amb_secondblock, text = "Browse", command=self.file2_ambtraj_browsing)
        self.file2_ambtraj_browse.grid(row = 1, column = 2)

        ##### GROMACS TRAJECTORIES #####~
        # TRAJECTORY #1 - PARM
        self.file1_gmxparm_label = Label(self.gmx_firstblock, text = "Topology:", width = 10)
        self.file1_gmxparm_label.grid(row = 0, column = 0)

        self.file1_gmxparm_entry = Entry(self.gmx_firstblock, width = 50)
        self.file1_gmxparm_entry.grid(row = 0, column = 1)

        self.file1_gmxparm_browse = Button(self.gmx_firstblock, text = "Browse", command=self.file1_gmxparm_browsing)
        self.file1_gmxparm_browse.grid(row = 0, column = 2)

        # TRAJECTORY #1 - TRAJ
        self.file1_gmxtraj_label = Label(self.gmx_firstblock, text = "Trajectory:", width = 10)
        self.file1_gmxtraj_label.grid(row = 1, column = 0)

        self.file1_gmxtraj_entry = Entry(self.gmx_firstblock, width = 50)
        self.file1_gmxtraj_entry.grid(row = 1, column = 1)

        self.file1_gmxtraj_browse = Button(self.gmx_firstblock, text = "Browse", command=self.file1_gmxtraj_browsing)
        self.file1_gmxtraj_browse.grid(row = 1, column = 2)

        # TRAJECTORY #2 - PARM
        self.file2_gmxparm_label = Label(self.gmx_secondblock, text = "Topology:", width = 10)
        self.file2_gmxparm_label.grid(row = 0, column = 0)

        self.file2_gmxparm_entry = Entry(self.gmx_secondblock, width = 50)
        self.file2_gmxparm_entry.grid(row = 0, column = 1)

        self.file2_gmxparm_browse = Button(self.gmx_secondblock, text = "Browse", command=self.file2_gmxparm_browsing)
        self.file2_gmxparm_browse.grid(row = 0, column = 2)

        # TRAJECTORY #2 - TRAJ
        self.file2_gmxtraj_label = Label(self.gmx_secondblock, text = "Trajectory:", width = 10)
        self.file2_gmxtraj_label.grid(row = 1, column = 0)

        self.file2_gmxtraj_entry = Entry(self.gmx_secondblock, width = 50)
        self.file2_gmxtraj_entry.grid(row = 1, column = 1)

        self.file2_gmxtraj_browse = Button(self.gmx_secondblock, text = "Browse", command=self.file2_gmxtraj_browsing)
        self.file2_gmxtraj_browse.grid(row = 1, column = 2)

        ##########################################################
        ##### PDB TRAJECTORIES #####~
        # FILE #1 - PDB
        self.file1_pdb_label = Label(self.pdb_firstblock, text = "File #1:", width = 13)
        self.file1_pdb_label.grid(row = 0, column = 0)

        self.file1_pdb_entry = Entry(self.pdb_firstblock, width = 50)
        self.file1_pdb_entry.grid(row = 0, column = 1)

        self.file1_pdb_browse = Button(self.pdb_firstblock, text = "Browse", command=self.file1_pdb_browsing)
        self.file1_pdb_browse.grid(row = 0, column = 2)

        # FILE #2 - PDB
        self.file2_pdb_label = Label(self.pdb_firstblock, text = "File #2:", width = 13)
        self.file2_pdb_label.grid(row = 1, column = 0)

        self.file2_pdb_entry = Entry(self.pdb_firstblock, width = 50)
        self.file2_pdb_entry.grid(row = 1, column = 1)

        self.file2_pdb_browse = Button(self.pdb_firstblock, text = "Browse", command=self.file2_pdb_browsing)
        self.file2_pdb_browse.grid(row = 1, column = 2)


        ##########################################################
        # OUTPUT PARAMETERS
        self.outputdir_label = Label(self.outputblock, text = "Output directory:", width = 15, anchor = "e")
        self.outputdir_label.grid(row = 0, column = 0)

        self.outputdir_entry = Entry(self.outputblock, width = 45)
        self.outputdir_entry.grid(row = 0, column = 1)

        self.outputdir_folder = Button(self.outputblock, text="Browse", command=self.outputdir_browsing)
        self.outputdir_folder.grid(row=0, column=2)

        #####
        self.outputsuffix_label = Label(self.outputblock, text="Results suffix:", width = 15, anchor = "e")
        self.outputsuffix_label.grid(row=1, column=0)
        self.outputsuffix_entry = Entry(self.outputblock, width = 25)
        self.outputsuffix_entry.grid(row = 1, column = 1, sticky="W")
        self.outputsuffix_entry.insert(0, SINAPs_parameters[0])

        ##########################################################
        # ADVANCED PARAMETERS
        ##### GENERAL #####
        self.general_repr_label = Label(self.generalblock, text="Representative frame:", width = 20, anchor = "e")
        self.general_repr_label.grid(row=0, column=0)
        self.general_repr_entry = Entry(self.generalblock, width = 5)
        self.general_repr_entry.grid(row = 0, column = 1)
        self.general_repr_entry.insert(0, SINAPs_parameters[1])

        self.general_water_label = Label(self.generalblock, text="Take water into account:", width = 20, anchor = "e")
        # self.general_water_label.grid(row=1, column=0)
        self.water_var = IntVar() ; self.water_var.set(0)
        self.general_water_button = Checkbutton(self.generalblock, variable = self.water_var, onvalue = 1, offvalue = 0)
        # self.general_water_button.grid(row = 1, column = 1, sticky="WE")

        self.general_cutoff_label = Label(self.generalblock, text="Frequency min cutoff (%):", width = 20, anchor = "e")
        self.general_cutoff_label.grid(row=2, column=0)
        self.general_cutoff_entry = Entry(self.generalblock, width = 5)
        self.general_cutoff_entry.grid(row = 2, column = 1)
        self.general_cutoff_entry.insert(0, SINAPs_parameters[2])

        ##### HB #####
        self.HB_dist_label = Label(self.HBblock, text="Maximum distance (A):", width = 20)
        self.HB_dist_label.grid(row=0, column=0)
        self.HB_dist_entry = Entry(self.HBblock, width = 5)
        self.HB_dist_entry.grid(row = 0, column = 1)
        self.HB_dist_entry.insert(0, SINAPs_parameters[3])

        self.HB_angle_label = Label(self.HBblock, text="Minimum angle (deg):", width = 20)
        self.HB_angle_label.grid(row=1, column=0)
        self.HB_angle_entry = Entry(self.HBblock, width = 5)
        self.HB_angle_entry.grid(row = 1, column = 1)
        self.HB_angle_entry.insert(0, SINAPs_parameters[4])

        ##### SB #####
        self.SB_dist_label = Label(self.SBblock, text="Maximum distance (A):", width = 20)
        self.SB_dist_label.grid(row=0, column=0)

        self.SB_dist_entry = Entry(self.SBblock, width = 5)
        self.SB_dist_entry.grid(row = 0, column = 1)
        self.SB_dist_entry.insert(0, SINAPs_parameters[5])

        self.SB_angle_label = Label(self.SBblock, text="Minimum angle (deg):", width = 20)
        self.SB_angle_label.grid(row=1, column=0)

        self.SB_angle_entry = Entry(self.SBblock, width = 5)
        self.SB_angle_entry.grid(row = 1, column = 1)
        self.SB_angle_entry.insert(0, SINAPs_parameters[6])

        ##### PI-STACKING #####
        self.P_mindist_label = Label(self.Pblock, text="Minimum distance (A):", width = 20)
        self.P_mindist_label.grid(row = 0, column=0)
        self.P_mindist_entry = Entry(self.Pblock, width = 5)
        self.P_mindist_entry.grid(row = 0, column = 1)
        self.P_mindist_entry.insert(0, SINAPs_parameters[7])
        
        self.P_maxdist_label = Label(self.Pblock, text="Maximum distance (A):", width = 20)
        self.P_maxdist_label.grid(row = 1, column=0)
        self.P_maxdist_entry = Entry(self.Pblock, width = 5)
        self.P_maxdist_entry.grid(row = 1, column = 1)
        self.P_maxdist_entry.insert(0, SINAPs_parameters[8])
        
        self.P_angle_label = Label(self.Pblock, text="Maximum angle (deg):", width = 20)
        self.P_angle_label.grid(row = 2, column=0)
        self.P_angle_entry = Entry(self.Pblock, width = 5)
        self.P_angle_entry.grid(row = 2, column = 1)
        self.P_angle_entry.insert(0, SINAPs_parameters[9])
        
        ##### TL-SHAPES #####
        self.TL_mindist_label = Label(self.TLblock, text="Minimum distance (A):", width=20)
        self.TL_mindist_label.grid(row=0, column=0)
        self.TL_mindist_entry = Entry(self.TLblock, width=5)
        self.TL_mindist_entry.grid(row=0, column=1)
        self.TL_mindist_entry.insert(0, SINAPs_parameters[10])

        self.TL_maxdist_label = Label(self.TLblock, text="Maximum distance (A):", width=20)
        self.TL_maxdist_label.grid(row=1, column=0)
        self.TL_maxdist_entry = Entry(self.TLblock, width=5)
        self.TL_maxdist_entry.grid(row=1, column=1)
        self.TL_maxdist_entry.insert(0, SINAPs_parameters[11])
        
        ##########################################################
        # FOOTER
        self.progress_label = Label(self.footer, text = "Waiting")
        self.progress_label.grid(row = 0, columnspan = 2)

        self.Apply = Button(self.footer, text = "Apply", command = self.apply)
        self.Apply.grid(row = 1)

        self.CloseButton = Button(self.footer, text = "Close", command = self.close)


    ##########################################################
    ##### AMBER TRAJECTORIES #####~
    def file1_ambparm_browsing(self):
        global initdir
        file1_parm_filename = filedialog.askopenfilename(initialdir=initdir, title="Select Amber topology", filetypes=(("Amber parameter file", "*.parm7"), ("all files", "*.*")))
        self.file1_ambparm_entry.delete(0, END)
        self.file1_ambparm_entry.insert(0, file1_parm_filename)
        if "red" in self.file1_ambparm_entry.config()["background"]:
            self.file1_ambparm_entry.config({"background": "white"})
        initdir = "/".join(file1_parm_filename.split("/")[:-1])

    def file1_ambtraj_browsing(self):
        global initdir
        file1_traj_filename = filedialog.askopenfilename(initialdir=initdir, title="Select Amber trajectory", filetypes=(("Amber trajectory file", "*.nc"), ("all files", "*.*")))
        self.file1_ambtraj_entry.delete(0, END)
        self.file1_ambtraj_entry.insert(0, file1_traj_filename)
        if "red" in self.file1_ambtraj_entry.config()["background"]:
            self.file1_ambtraj_entry.config({"background": "white"})
        initdir = "/".join(file1_traj_filename.split("/")[:-1])

    def file2_ambparm_browsing(self):
        global initdir
        file2_parm_filename = filedialog.askopenfilename(initialdir=initdir, title="Select Amber topology", filetypes=(("Amber parameter file", "*.parm7"), ("all files", "*.*")))
        self.file2_ambparm_entry.delete(0, END)
        self.file2_ambparm_entry.insert(0, file2_parm_filename)
        if "red" in self.file2_ambparm_entry.config()["background"]:
            self.file2_ambparm_entry.config({"background": "white"})
        initdir = "/".join(file2_parm_filename.split("/")[:-1])

    def file2_ambtraj_browsing(self):
        global initdir
        file2_traj_filename = filedialog.askopenfilename(initialdir=initdir, title="Select AMBER trajectory", filetypes=(("Amber trajectory file", "*.nc"), ("all files", "*.*")))
        self.file2_ambtraj_entry.delete(0, END)
        self.file2_ambtraj_entry.insert(0, file2_traj_filename)
        if "red" in self.file2_ambtraj_entry.config()["background"]:
            self.file2_ambtraj_entry.config({"background": "white"})
        initdir = "/".join(file2_traj_filename.split("/")[:-1])


    ##### GROMACS TRAJECTORIES #####~
    def file1_gmxparm_browsing(self):
        global initdir
        file1_parm_filename = filedialog.askopenfilename(initialdir=initdir, title="Select GROMACS topology", filetypes=(("GROMACS parameter file", "*.pdb *.top"), ("all files", "*.*")))
        self.file1_gmxparm_entry.delete(0, END)
        self.file1_gmxparm_entry.insert(0, file1_parm_filename)
        if "red" in self.file1_gmxparm_entry.config()["background"]:
            self.file1_gmxparm_entry.config({"background": "white"})
        initdir = "/".join(file1_parm_filename.split("/")[:-1])

    def file1_gmxtraj_browsing(self):
        global initdir
        file1_traj_filename = filedialog.askopenfilename(initialdir=initdir, title="Select GROMACS trajectory", filetypes=(("GROMACS trajectory file", "*.xtc *.trr"), ("all files", "*.*")))
        self.file1_gmxtraj_entry.delete(0, END)
        self.file1_gmxtraj_entry.insert(0, file1_traj_filename)
        if "red" in self.file1_gmxtraj_entry.config()["background"]:
            self.file1_gmxtraj_entry.config({"background": "white"})
        initdir = "/".join(file1_traj_filename.split("/")[:-1])

    def file2_gmxparm_browsing(self):
        global initdir
        file2_parm_filename = filedialog.askopenfilename(initialdir=initdir, title="Select GROMACS topology", filetypes=(("GROMACS parameter file", "*.pdb *.top"), ("all files", "*.*")))
        self.file2_gmxparm_entry.delete(0, END)
        self.file2_gmxparm_entry.insert(0, file2_parm_filename)
        if "red" in self.file2_gmxparm_entry.config()["background"]:
            self.file2_gmxparm_entry.config({"background": "white"})
        initdir = "/".join(file2_parm_filename.split("/")[:-1])

    def file2_gmxtraj_browsing(self):
        global initdir
        file2_traj_filename = filedialog.askopenfilename(initialdir=initdir, title="Select GROMACS trajectory", filetypes=(("GROMACS trajectory file", "*.xtc *.trr"), ("all files", "*.*")))
        self.file2_gmxtraj_entry.delete(0, END)
        self.file2_gmxtraj_entry.insert(0, file2_traj_filename)
        if "red" in self.file2_gmxtraj_entry.config()["background"]:
            self.file2_gmxtraj_entry.config({"background": "white"})
        initdir = "/".join(file2_traj_filename.split("/")[:-1])


    ##########################################################
    ##### PDB TRAJECTORIES #####~
    def file1_pdb_browsing(self):
        global initdir
        file1_pdb_filename = filedialog.askopenfilename(initialdir=initdir, title="Select PDB file #1", filetypes=(("PDB file", "*.pdb"), ("all files", "*.*")))
        self.file1_pdb_entry.delete(0, END)
        self.file1_pdb_entry.insert(0, file1_pdb_filename)
        if "red" in self.file1_pdb_entry.config()["background"]:
            self.file1_pdb_entry.config({"background": "white"})
        initdir = "/".join(file1_pdb_filename.split("/")[:-1])

    def file2_pdb_browsing(self):
        global initdir
        file2_pdb_filename = filedialog.askopenfilename(initialdir=initdir, title="Select PDB file #2", filetypes=(("PDB file", "*.pdb"), ("all files", "*.*")))
        self.file2_pdb_entry.delete(0, END)
        self.file2_pdb_entry.insert(0, file2_pdb_filename)
        if "red" in self.file2_pdb_entry.config()["background"]:
            self.file2_pdb_entry.config({"background": "white"})
        initdir = "/".join(file2_pdb_filename.split("/")[:-1])


    ##########################################################

    def outputdir_browsing(self):
        global initdir
        outfolder = filedialog.askdirectory(initialdir=initdir, title="Select output directory")
        self.outputdir_entry.delete(0, END)
        self.outputdir_entry.insert(0, outfolder)
        if "red" in self.outputdir_entry.config()["background"]:
            self.outputdir_entry.config({"background": "white"})
        initdir = outfolder

    ##########################################################

    def label_update(self, text):
        self.progress_label["text"] = text
        self.progress_label.update()

    ##########################################################

    def entries_checking(self):
        count_temp = 0

        # Check trajectories
        if self.tabs.index(self.tabs.select()) == 0:
            if len(self.file1_ambtraj_entry.get()) == 0: self.file1_ambtraj_entry.config({"background": "red"}) ; count_temp+=1
            if len(self.file1_ambparm_entry.get()) == 0: self.file1_ambparm_entry.config({"background": "red"}) ; count_temp+=1
            if len(self.file2_ambtraj_entry.get()) == 0: self.file2_ambtraj_entry.config({"background": "red"}) ; count_temp+=1
            if len(self.file2_ambparm_entry.get()) == 0: self.file2_ambparm_entry.config({"background": "red"}) ; count_temp+=1

        elif self.tabs.index(self.tabs.select()) == 1:
            if len(self.file1_gmxtraj_entry.get()) == 0: self.file1_gmxtraj_entry.config({"background": "red"}) ; count_temp+=1
            if len(self.file1_gmxparm_entry.get()) == 0: self.file1_gmxparm_entry.config({"background": "red"}) ; count_temp+=1
            if len(self.file2_gmxtraj_entry.get()) == 0: self.file2_gmxtraj_entry.config({"background": "red"}) ; count_temp+=1
            if len(self.file2_gmxparm_entry.get()) == 0: self.file2_gmxparm_entry.config({"background": "red"}) ; count_temp+=1

        elif self.tabs.index(self.tabs.select()) == 2:
            if len(self.file1_pdb_entry.get()) == 0: self.file1_pdb_entry.config({"background": "red"}) ; count_temp+=1
            if len(self.file2_pdb_entry.get()) == 0: self.file2_pdb_entry.config({"background": "red"}) ; count_temp+=1

        # Check output parameters
        if len(self.outputdir_entry.get()) == 0: self.outputdir_entry.config({"background": "red"}) ; count_temp+=1
        if len(self.outputsuffix_entry.get()) == 0: self.outputsuffix_entry.config({"background": "red"}) ; count_temp+=1

        # Check advanced parameters
        if len(self.general_repr_entry.get()) == 0: self.general_repr_entry.config({"background": "red"}) ; count_temp+=1
        if len(self.HB_dist_entry.get()) == 0: self.HB_dist_entry.config({"background": "red"}) ; count_temp+=1
        if len(self.HB_angle_entry.get()) == 0: self.HB_angle_entry.config({"background": "red"}) ; count_temp+=1

        return count_temp

    ##########################################################

    def close(self):
        self.destroy()
        exit()

    ##########################################################

    def apply(self):
        continue_script = self.entries_checking()
        if continue_script == 0:
            self.Apply.grid_forget()
            self.CloseButton.grid_forget()
            # AMBER Trajectories loading
            if self.tabs.index(self.tabs.select()) == 0:
                # Trajectory #1
                self.label_update("Loading - Amber trajectory #1")
                trajectory1 = SINAPs_functions.TRAJ_loader(self.file1_ambtraj_entry.get(), self.file1_ambparm_entry.get())
                trajectory1_name = self.file1_ambtraj_entry.get().split("/")[-1].split(".")[0]

                # Trajectory #2
                self.label_update("Loading - Amber trajectory #2")
                trajectory2 = SINAPs_functions.TRAJ_loader(self.file2_ambtraj_entry.get(), self.file2_ambparm_entry.get())
                trajectory2_name = self.file2_ambtraj_entry.get().split("/")[-1].split(".")[0]

            # AMBER Trajectories loading
            if self.tabs.index(self.tabs.select()) == 1:
                # Trajectory #1
                self.label_update("Loading - GROMACS trajectory #1")
                trajectory1 = SINAPs_functions.TRAJ_loader(self.file1_gmxtraj_entry.get(), self.file1_gmxparm_entry.get())
                trajectory1_name = self.file1_gmxtraj_entry.get().split("/")[-1].split(".")[0]

                # Trajectory #2
                self.label_update("Loading - GROMACS trajectory #2")
                trajectory2 = SINAPs_functions.TRAJ_loader(self.file2_gmxtraj_entry.get(), self.file2_gmxparm_entry.get())
                trajectory2_name = self.file2_gmxtraj_entry.get().split("/")[-1].split(".")[0]

            # PDB Trajectories loading
            if self.tabs.index(self.tabs.select()) == 2:
                # Trajectory #1
                self.label_update("Loading - PDB file #1")
                trajectory1 = SINAPs_functions.PDB_loader(self.file1_pdb_entry.get())
                trajectory1_name = self.file1_pdb_entry.get().split("/")[-1].split(".")[0]

                # Trajectory #2
                self.label_update("Loading - PDB file #2")
                trajectory2 = SINAPs_functions.PDB_loader(self.file2_pdb_entry.get())
                trajectory2_name = self.file2_pdb_entry.get().split("/")[-1].split(".")[0]

            ##### Representatives #####
            SINAPs_functions.representative_SINAPs(trajectory1, trajectory1_name, self.general_repr_entry.get(), 0, self.outputdir_entry.get() + "/", "Representative1")
            SINAPs_functions.representative_SINAPs(trajectory2, trajectory2_name, self.general_repr_entry.get(), 0,self.outputdir_entry.get() + "/", "Representative2")
            SINAPs_functions.alignment_SINAPs(self.outputdir_entry.get() + "/")

            ##### HB #####
            self.label_update("Hydrogen bonds #1")
            HB1 = SINAPs_functions.SINAPs_HB(trajectory1, self.HB_dist_entry.get(), self.HB_angle_entry.get(), self.general_cutoff_entry.get(), self.water_var.get())

            self.label_update("Hydrogen bonds #2")
            HB2 = SINAPs_functions.SINAPs_HB(trajectory2, self.HB_dist_entry.get(), self.HB_angle_entry.get(), self.general_cutoff_entry.get(), self.water_var.get())

            self.label_update("Hydrogen bonds - Processing comparisons")
            SINAPs_functions.SINAPs_output_HB(trajectory1, trajectory2, HB1, HB2, self.outputdir_entry.get() + "/", self.outputsuffix_entry.get())

            ##### SB #####
            self.label_update("Salt bridges #1")
            SB1 = SINAPs_functions.SINAPs_SB(trajectory1, self.SB_dist_entry.get(), self.SB_angle_entry.get(), self.general_cutoff_entry.get())

            self.label_update("Salt bridges #2")
            SB2 = SINAPs_functions.SINAPs_SB(trajectory2, self.SB_dist_entry.get(), self.SB_angle_entry.get(), self.general_cutoff_entry.get())

            self.label_update("Salt bridges - Processing comparisons")
            SINAPs_functions.SINAPs_output_SB(trajectory1, trajectory2, SB1, SB2, self.outputdir_entry.get() + "/", self.outputsuffix_entry.get())

            ##### ARO #####
            self.label_update("Aromatics #1")
            ARO1 = SINAPs_functions.SINAPs_aro_aro(trajectory1, self.P_mindist_entry.get(), self.P_maxdist_entry.get(), self.P_angle_entry.get(), self.TL_mindist_entry.get(), self.TL_maxdist_entry.get())
            self.label_update("Aromatics #2")
            ARO2 = SINAPs_functions.SINAPs_aro_aro(trajectory2, self.P_mindist_entry.get(), self.P_maxdist_entry.get(), self.P_angle_entry.get(), self.TL_mindist_entry.get(), self.TL_maxdist_entry.get())

            self.label_update("Aromatics - Processing comparisons")
            SINAPs_functions.output_aro_SINAPs(ARO1, ARO2, trajectory1, trajectory2, self.outputdir_entry.get() + "/", self.outputsuffix_entry.get())

            self.label_update(">> FINISHED <<")
            self.Apply.grid(row=1, column=0)
            self.CloseButton.grid(row=1, column=1)

        else:
            self.label_update("No information")


#######################################################################################################################~

frame = Tk()
frame.geometry("700x600")
frame.title("SINAPs - Analyzer")

gui = SINAPs_GUI(frame)

gui.mainloop()
gui.destroy()

#######################################################################################################################~
