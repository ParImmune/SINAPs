# coding: utf-8

#######################################################################################################################~
#
# GUI - SINAPs visualization
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

import os
from Tkinter import *
import tkFileDialog
import tkFont

import chimera
from chimera import runCommand as rc
from chimera.baseDialog import ModelessDialog
from chimera.extension import manager
from chimera.widgets import DisclosureFrame

from CGLtk.color.ColorWell import ColorWell
from chimera import MaterialColor

#######################################################################################################################~

global HBcolors ; global SBcolors ; global Arocolors

HBcolors = {"commonBB" : (255/255.0, 255/255.0, 238/255.0, 1.0), "commonBC" : (255/255.0, 255/255.0, 153/255.0, 1.0), "commonCC" : (255/255.0, 255/255.0, 0/255.0, 1.0),
            "exclu1BB" : (245/255.0, 190/255.0, 184/255.0, 1.0), "exclu1BC" : (235/255.0, 124/255.0, 112/255.0, 1.0), "exclu1CC" : (220/255.0, 50/255.0, 32/255.0, 1.0),
            "exclu2BB" : (112/255.0, 184/255.0, 255/255.0, 1.0), "exclu2BC" : (10/255.0, 133/255.0, 255/255.0, 1.0), "exclu2CC" : (0/255.0, 90/255.0, 181/255.0, 1.0)}

SBcolors = {"commonSB" : (184/255.0, 184/255.0, 0/255.0, 1.0), "exclu1SB" : (161/255.0, 37/255.0, 23/255.0, 1.0), "exclu2SB" : (0/255.0, 51/255.0, 102/255.0, 1.0)}

Arocolors = {"commonAro" : (255/255.0, 255/255.0, 153/255.0, 1.0), "exclu1Aro" : (235/255.0, 124/255.0, 112/255.0, 1.0), "exclu2Aro" : (10/255.0, 133/255.0, 255/255.0, 1.0),
             "commonP" : (255/255.0, 255/255.0, 153/255.0, 1.0), "exclu1P" : (235/255.0, 124/255.0, 112/255.0, 1.0), "exclu2P" : (10/255.0, 133/255.0, 255/255.0, 1.0),
             "commonTL" : (255/255.0, 255/255.0, 153/255.0, 1.0), "exclu1TL" : (235/255.0, 124/255.0, 112/255.0, 1.0), "exclu2TL" : (10/255.0, 133/255.0, 255/255.0, 1.0),
             "commonT" : (255/255.0, 255/255.0, 153/255.0, 1.0), "exclu1T" : (235/255.0, 124/255.0, 112/255.0, 1.0), "exclu2T" : (10/255.0, 133/255.0, 255/255.0, 1.0),
             "commonL" : (255/255.0, 255/255.0, 153/255.0, 1.0), "exclu1L" : (235/255.0, 124/255.0, 112/255.0, 1.0), "exclu2L" : (10/255.0, 133/255.0, 255/255.0, 1.0)}

#######################################################################################################################~

global SINAPs_loaded ; global default_folder

SINAPs_loaded = 0 ; default_folder = "~/"

#######################################################################################################################~

global HB_common_BB ; global HB_common_BC ; global HB_common_CC

HB_common_BB = {} ; HB_common_BC = {} ; HB_common_CC = {}

#######################################################################################################################~

global font1 ; global font1b ; global font2

font1 = tkFont.Font(family="Arial", size="12")
font1b = tkFont.Font(family="Arial", size="10", weight="bold")
font2 = tkFont.Font(family="Arial", size="8")

#######################################################################################################################~
class SINAPsColorWell:
    def __init__(CWE, parent, dico, wellcolor):
        CWE.wellcolor = wellcolor
        CWE.dico = dico
        CWE.well = ColorWell(parent, width = 35, height = 35, color = wellcolor, callback = CWE.colorwell_callback)

        CWE.well.grid()

        # winfo_depth
    def colorwell_callback(CWE, self):
        newcolor = self
        dicotemp = eval(CWE.dico)

        for Bond in dicotemp:
            if dicotemp[Bond][0] != -1: dicotemp[Bond][0].color = MaterialColor(newcolor[0], newcolor[1], newcolor[2], newcolor[3])
            if dicotemp[Bond][1] != -1: dicotemp[Bond][1].color = MaterialColor(newcolor[0], newcolor[1], newcolor[2], newcolor[3])

    def get(CWE):
        return(MaterialColor(CWE.well._rgba[0], CWE.well._rgba[1], CWE.well._rgba[2], CWE.well._rgba[3]))

        
#######################################################################################################################~

class SINAPs_GUI_loader(ModelessDialog):
    name = "SINAPs - Visualizer"
    title = "SINAPs - Visualizer"
    help = "https://www.google.com"
    buttons = ("Apply", "Close")
    provideStatus = True

    ################################

    def __init__(self, sessionData=None, *args, **kw):
        self.optionsDialog = None
        self.closeHandler = None
        ModelessDialog.__init__(self)
        manager.registerInstance(self)
        chimera.extension.manager.registerInstance(self)
        self._closeSesHandler = chimera.triggers.addHandler(chimera.CLOSE_SESSION, self.emQuit, None)

        ################################

    def fillInUI(self, parent):
        ################################################################################################################
        # MAIN FRAMES DEFINITION
        ################################################################################################################
        self.mainframe = Frame(parent)
        self.mainframe.grid()

        self.frame1 = Frame(self.mainframe)
        self.frame1.pack()

        self.frame2 = Frame(self.mainframe)

        ##### FREQUENCY SLIDER FRAME #####
        self.slider_frame = Frame(self.frame2)
        self.slider_frame.pack(fill = X, expand = 1)


        ################################################################################################################
        # RESULTS LOADER
        ################################################################################################################
        self.loading_label = Label(self.frame1, text = "Select a directory")
        self.loading_label.grid(row = 0, columnspan = 3)

        self.loading_entry = Entry(self.frame1, width = 50)
        self.loading_entry.grid(row = 1, column = 0, columnspan = 2)

        self.loading_browse = Button(self.frame1, text = "Browse", command = self.BrowseDirectory)
        self.loading_browse.grid(row = 1, column = 2, columnspan = 1)

        self.loading_button = Button(self.frame1, text="> Loading <", command=self.Loading)
        self.loading_button.grid(row = 2, columnspan = 3)

        self.loading_error = Label(self.frame1, text="")
        self.loading_error.grid(row = 3, columnspan=3)


        ################################################################################################################
        # SLIDER
        ################################################################################################################
        self.frequency_slider = Scale(self.slider_frame, orient = HORIZONTAL, length = 450, from_=1, to=100, font = font1)
        self.frequency_slider.set(50)
        self.frequency_slider.grid(row = 1, column = 0, columnspan = 5)

        self.frequency_label = Label(self.slider_frame, text = "Lower frequency limit currently set to {0}%".format(self.frequency_slider.get()), font = font1)
        self.frequency_label.grid(row = 0, column = 0, columnspan = 6, sticky = "N")

        self.frequency_button = Button(self.slider_frame, text = "Refresh", command = self.cmd_frequency)
        self.frequency_button.grid(row = 1, column = 5, sticky = "E")


        ################################################################################################################
        # FRAMES LOADER
        ################################################################################################################
        ##### TOP LEGEND FRAME #####
        self.toplabel_frame = Frame(self.frame2)
        self.toplabel_frame.pack(fill=X, expand=1)

        self.toplabel_frame.columnconfigure(0, weight=1)
        self.toplabel_frame.columnconfigure(1, weight=1)
        self.toplabel_frame.columnconfigure(2, weight=1)

        self.common_label = Label(self.toplabel_frame, text="In common", font=font1b, width = 23) ; self.common_label.grid(row=0, column=0)
        self.exclu1_label = Label(self.toplabel_frame, text="Only in #0", font=font1b, width = 23) ; self.exclu1_label.grid(row=0, column=1)
        self.exclu2_label = Label(self.toplabel_frame, text="Only in #1", font=font1b, width = 23) ; self.exclu2_label.grid(row=0, column=2)

        ##### HYDROGEN BONDS FRAME #####
        self.HB_checklists = DisclosureFrame(self.frame2, text = "Hydrogen bonds interactions", collapsed=False)
        self.HB_checklists.pack(fill = X, expand = 1)
        self.HB_checklists_frame = self.HB_checklists.frame

        ##### SALT BRIDGES FRAME #####
        self.SB_checklists = DisclosureFrame(self.frame2, text = "Salt bridges interactions", collapsed=False)
        self.SB_checklists.pack(fill = X, expand = 1)
        self.SB_checklists_frame = self.SB_checklists.frame

        ##### AROMATICS INTERACTIONS FRAME #####
        self.Aro_checklists = DisclosureFrame(self.frame2, text = "Aromatics interactions (Experimental)", collapsed=True)
        self.Aro_checklists.pack(fill = X, expand = 1)
        self.Aro_checklists_frame = self.Aro_checklists.frame


        ################################################################################################################
        # HBONDS
        ################################################################################################################

        self.var_common_ALL = IntVar() ; self.var_common_ALL.set(0)
        self.var_common_BB = IntVar() ; self.var_common_BB.set(0)
        self.var_common_BC = IntVar() ; self.var_common_BC.set(0)
        self.var_common_CC = IntVar() ; self.var_common_CC.set(0)

        self.var_exclu1_ALL = IntVar() ; self.var_exclu1_ALL.set(0)
        self.var_exclu1_BB = IntVar() ; self.var_exclu1_BB.set(0)
        self.var_exclu1_BC = IntVar() ; self.var_exclu1_BC.set(0)
        self.var_exclu1_CC = IntVar() ; self.var_exclu1_CC.set(0)

        self.var_exclu2_ALL = IntVar() ; self.var_exclu2_ALL.set(0)
        self.var_exclu2_BB = IntVar() ; self.var_exclu2_BB.set(0)
        self.var_exclu2_BC = IntVar() ; self.var_exclu2_BC.set(0)
        self.var_exclu2_CC = IntVar() ; self.var_exclu2_CC.set(0)

        ################################################################################################################

        self.common_frame = Frame(self.HB_checklists_frame)
        self.common_frame.grid(row = 0, column = 0)

        self.exclu1_frame = Frame(self.HB_checklists_frame)
        self.exclu1_frame.grid(row = 0, column = 1)

        self.exclu2_frame = Frame(self.HB_checklists_frame)
        self.exclu2_frame.grid(row = 0, column = 2)

        ################################################################################################################

        self.common_ALL = Checkbutton(self.common_frame, text="Show all", command=self.cmd_HB_common_ALL, variable = self.var_common_ALL, font = font1, width = 10, anchor = "w")
        self.common_ALL.grid(row = 1, sticky = "w")

        self.common_BB = Checkbutton(self.common_frame, text="BB/BB", command=lambda:self.cmd_visibility(HB_common_BB, self.var_common_BB.get()), variable = self.var_common_BB, font = font1)
        self.common_BB.grid(row = 2, column = 0, padx = 20, sticky = W)
        self.common_BB_nb = Label(self.common_frame, text = "", font = font2, width = 3)
        self.common_BB_nb.grid(row = 2, column = 1)
        self.frame_color_common_BB = Frame(self.common_frame)
        self.frame_color_common_BB.grid(row = 2, column = 2)
        self.color_common_BB = SINAPsColorWell(self.frame_color_common_BB, "HB_common_BB", HBcolors["commonBB"])

        self.common_BC = Checkbutton(self.common_frame, text="BB/SC", command=lambda:self.cmd_visibility(HB_common_BC, self.var_common_BC.get()), variable = self.var_common_BC, font = font1)
        self.common_BC.grid(row = 3, column = 0, padx = 20, sticky = W)
        self.common_BC_nb = Label(self.common_frame, text = "", font = font2, width = 3)
        self.common_BC_nb.grid(row = 3, column = 1)
        self.frame_color_common_BC = Frame(self.common_frame)
        self.frame_color_common_BC.grid(row = 3, column = 2)
        self.color_common_BC = SINAPsColorWell(self.frame_color_common_BC, "HB_common_BC", HBcolors["commonBC"])

        self.common_CC = Checkbutton(self.common_frame, text="SC/SC", command=lambda:self.cmd_visibility(HB_common_CC, self.var_common_CC.get()), variable = self.var_common_CC, font = font1)
        self.common_CC.grid(row = 4, column = 0, padx = 20, sticky = W)
        self.common_CC_nb = Label(self.common_frame, text = "", font = font2, width = 3)
        self.common_CC_nb.grid(row = 4, column = 1)
        self.frame_color_common_CC = Frame(self.common_frame)
        self.frame_color_common_CC.grid(row = 4, column = 2)
        self.color_common_CC = SINAPsColorWell(self.frame_color_common_CC, "HB_common_CC", HBcolors["commonCC"])

        ################################################################################################################

        self.exclu1_ALL = Checkbutton(self.exclu1_frame, text="Show all", command=self.cmd_HB_exclu1_ALL, variable = self.var_exclu1_ALL, font = font1, width = 10, anchor = "w")
        self.exclu1_ALL.grid(row = 1, sticky = W)

        self.exclu1_BB = Checkbutton(self.exclu1_frame, text="BB/BB", command=lambda: self.cmd_visibility(HB_exclu1_BB, self.var_exclu1_BB.get()), variable = self.var_exclu1_BB, font = font1)
        self.exclu1_BB.grid(row = 2, column = 0, padx = 20, sticky = W)
        self.exclu1_BB_nb = Label(self.exclu1_frame, text = "", font = font2, width = 3)
        self.exclu1_BB_nb.grid(row = 2, column = 1)
        self.frame_color_exclu1_BB = Frame(self.exclu1_frame)
        self.frame_color_exclu1_BB.grid(row = 2, column = 2)
        self.color_exclu1_BB = SINAPsColorWell(self.frame_color_exclu1_BB, "HB_exclu1_BB", HBcolors["exclu1BB"])

        self.exclu1_BC = Checkbutton(self.exclu1_frame, text="BB/SC", command=lambda: self.cmd_visibility(HB_exclu1_BC, self.var_exclu1_BC.get()), variable = self.var_exclu1_BC, font = font1)
        self.exclu1_BC.grid(row = 3, column = 0, padx = 20, sticky = W)
        self.exclu1_BC_nb = Label(self.exclu1_frame, text = "", font = font2, width = 3)
        self.exclu1_BC_nb.grid(row = 3, column = 1)
        self.frame_color_exclu1_BC = Frame(self.exclu1_frame)
        self.frame_color_exclu1_BC.grid(row = 3, column = 2)
        self.color_exclu1_BC = SINAPsColorWell(self.frame_color_exclu1_BC, "HB_exclu1_BC", HBcolors["exclu1BC"])

        self.exclu1_CC = Checkbutton(self.exclu1_frame, text="SC/SC", command=lambda: self.cmd_visibility(HB_exclu1_CC, self.var_exclu1_CC.get()), variable = self.var_exclu1_CC, font = font1)
        self.exclu1_CC.grid(row = 4, column = 0, padx = 20, sticky = W)
        self.exclu1_CC_nb = Label(self.exclu1_frame, text = "", font = font2, width = 3)
        self.exclu1_CC_nb.grid(row = 4, column = 1)
        self.frame_color_exclu1_CC = Frame(self.exclu1_frame)
        self.frame_color_exclu1_CC.grid(row = 4, column = 2)
        self.color_exclu1_CC = SINAPsColorWell(self.frame_color_exclu1_CC, "HB_exclu1_CC", HBcolors["exclu1CC"])

        ################################################################################################################

        self.exclu2_ALL = Checkbutton(self.exclu2_frame, text="Show all", command=self.cmd_HB_exclu2_ALL, variable = self.var_exclu2_ALL, font = font1, width = 10, anchor = "w")
        self.exclu2_ALL.grid(row = 1, sticky = W)

        self.exclu2_BB = Checkbutton(self.exclu2_frame, text="BB/BB", command=lambda: self.cmd_visibility(HB_exclu2_BB, self.var_exclu2_BB.get()), variable = self.var_exclu2_BB, font = font1)
        self.exclu2_BB.grid(row = 2, column = 0, padx = 20, sticky = W)

        self.exclu2_BB_nb = Label(self.exclu2_frame, text = "", font = font2, width = 3)
        self.exclu2_BB_nb.grid(row = 2, column = 1)

        self.frame_color_exclu2_BB = Frame(self.exclu2_frame)
        self.frame_color_exclu2_BB.grid(row = 2, column = 2)
        self.color_exclu2_BB = SINAPsColorWell(self.frame_color_exclu2_BB, "HB_exclu2_BB", HBcolors["exclu2BB"])


        self.exclu2_BC = Checkbutton(self.exclu2_frame, text="BB/SC", command=lambda: self.cmd_visibility(HB_exclu2_BC, self.var_exclu2_BC.get()), variable = self.var_exclu2_BC, font = font1)
        self.exclu2_BC.grid(row = 3, column = 0, padx = 20, sticky = W)

        self.exclu2_BC_nb = Label(self.exclu2_frame, text = "", font = font2, width = 3)
        self.exclu2_BC_nb.grid(row = 3, column = 1)

        self.frame_color_exclu2_BC = Frame(self.exclu2_frame)
        self.frame_color_exclu2_BC.grid(row = 3, column = 2)
        self.color_exclu2_BC = SINAPsColorWell(self.frame_color_exclu2_BC, "HB_exclu2_BC", HBcolors["exclu2BC"])


        self.exclu2_CC = Checkbutton(self.exclu2_frame, text="SC/SC", command=lambda: self.cmd_visibility(HB_exclu2_CC, self.var_exclu2_CC.get()), variable = self.var_exclu2_CC, font = font1)
        self.exclu2_CC.grid(row = 4, column = 0, padx = 20, sticky = W)

        self.exclu2_CC_nb = Label(self.exclu2_frame, text = "", font = font2, width = 3)
        self.exclu2_CC_nb.grid(row = 4, column = 1)

        self.frame_color_exclu2_CC = Frame(self.exclu2_frame)
        self.frame_color_exclu2_CC.grid(row = 4, column = 2)
        self.color_exclu2_CC = SINAPsColorWell(self.frame_color_exclu2_CC, "HB_exclu2_CC", HBcolors["exclu2CC"])


        ################################################################################################################
        # SALT BRIDGES
        ################################################################################################################

        self.var_common_SB = IntVar() ; self.var_common_SB.set(0)
        self.var_exclu1_SB = IntVar() ; self.var_exclu1_SB.set(0)
        self.var_exclu2_SB = IntVar() ; self.var_exclu2_SB.set(0)

        ################################################################################################################

        self.common_SB_frame = Frame(self.SB_checklists_frame)
        self.common_SB_frame.grid(row = 0, column = 0)

        self.exclu1_SB_frame = Frame(self.SB_checklists_frame)
        self.exclu1_SB_frame.grid(row = 0, column = 1)

        self.exclu2_SB_frame = Frame(self.SB_checklists_frame)
        self.exclu2_SB_frame.grid(row = 0, column = 2)
        
        ################################################################################################################

        self.common_SB = Checkbutton(self.common_SB_frame, text="Show all", command=lambda: self.cmd_visibility(SB_common, self.var_common_SB.get()), variable = self.var_common_SB, font = font1, width = 10, anchor = "w")
        self.common_SB.grid(row = 1, column = 0, sticky = "W")
        self.common_SB_nb = Label(self.common_SB_frame, text = "", font = font2, width = 3)
        self.common_SB_nb.grid(row = 1, column = 1)
        self.frame_color_common_SB = Frame(self.common_SB_frame)
        self.frame_color_common_SB.grid(row = 1, column = 2)
        self.color_common_SB = SINAPsColorWell(self.frame_color_common_SB, "SB_common", SBcolors["commonSB"])
        
        self.exclu1_SB = Checkbutton(self.exclu1_SB_frame, text="Show all", command=lambda: self.cmd_visibility(SB_exclu1, self.var_exclu1_SB.get()), variable = self.var_exclu1_SB, font = font1, width = 10, anchor = "w")
        self.exclu1_SB.grid(row = 1, column = 0, sticky = W)
        self.exclu1_SB_nb = Label(self.exclu1_SB_frame, text = "", font = font2, width = 3)
        self.exclu1_SB_nb.grid(row = 1, column = 1)
        self.frame_color_exclu1_SB = Frame(self.exclu1_SB_frame)
        self.frame_color_exclu1_SB.grid(row = 1, column = 2)
        self.color_exclu1_SB = SINAPsColorWell(self.frame_color_exclu1_SB, "SB_exclu1", SBcolors["exclu1SB"])
        
        self.exclu2_SB = Checkbutton(self.exclu2_SB_frame, text="Show all", command=lambda: self.cmd_visibility(SB_exclu2, self.var_exclu2_SB.get()), variable = self.var_exclu2_SB, font = font1, width = 10, anchor = "w")
        self.exclu2_SB.grid(row = 1, column = 0, sticky = W)
        self.exclu2_SB_nb = Label(self.exclu2_SB_frame, text = "", font = font2, width = 3)
        self.exclu2_SB_nb.grid(row = 1, column = 1)
        self.frame_color_exclu2_SB = Frame(self.exclu2_SB_frame)
        self.frame_color_exclu2_SB.grid(row = 1, column = 2)
        self.color_exclu2_SB = SINAPsColorWell(self.frame_color_exclu2_SB, "SB_exclu2", SBcolors["exclu2SB"])
        

        ################################################################################################################
        # AROMATICS
        ################################################################################################################
        self.var_common_Aro = IntVar() ; self.var_common_Aro.set(0)
        self.var_common_P = IntVar() ; self.var_common_P.set(0)
        self.var_common_TL = IntVar() ; self.var_common_TL.set(0)
        self.var_common_T = IntVar() ; self.var_common_T.set(0)
        self.var_common_L = IntVar() ; self.var_common_L.set(0)

        self.var_exclu1_Aro = IntVar() ; self.var_exclu1_Aro.set(0)
        self.var_exclu1_P = IntVar() ; self.var_exclu1_P.set(0)
        self.var_exclu1_TL = IntVar() ; self.var_exclu1_TL.set(0)
        self.var_exclu1_T = IntVar() ; self.var_exclu1_T.set(0)
        self.var_exclu1_L = IntVar() ; self.var_exclu1_L.set(0)

        self.var_exclu2_Aro = IntVar() ; self.var_exclu2_Aro.set(0)
        self.var_exclu2_P = IntVar() ; self.var_exclu2_P.set(0)
        self.var_exclu2_TL = IntVar() ; self.var_exclu2_TL.set(0)
        self.var_exclu2_T = IntVar() ; self.var_exclu2_T.set(0)
        self.var_exclu2_L = IntVar() ; self.var_exclu2_L.set(0)

        ################################################################################################################

        self.common_Aro_frame = Frame(self.Aro_checklists_frame)
        self.common_Aro_frame.grid(row = 0, column = 0)

        self.exclu1_Aro_frame = Frame(self.Aro_checklists_frame)
        self.exclu1_Aro_frame.grid(row = 0, column = 1)

        self.exclu2_Aro_frame = Frame(self.Aro_checklists_frame)
        self.exclu2_Aro_frame.grid(row = 0, column = 2)

        ################################################################################################################

        self.common_Aro = Checkbutton(self.common_Aro_frame, text="All types", command=lambda: self.cmd_visibility(Aro_Aro_common, self.var_common_Aro.get()), variable = self.var_common_Aro, font = font1, width = 10, anchor = "w")
        self.common_Aro.grid(row = 1, column = 0, sticky = W)
        self.common_Aro_nb = Label(self.common_Aro_frame, text = "", font = font2, width = 3)
        self.common_Aro_nb.grid(row = 1, column = 1)
        self.frame_color_common_Aro = Frame(self.common_Aro_frame)
        self.frame_color_common_Aro.grid(row = 1, column = 2)
        self.color_common_Aro = SINAPsColorWell(self.frame_color_common_Aro, "Aro_Aro_common", Arocolors["commonAro"])

        self.common_P = Checkbutton(self.common_Aro_frame, text="Pi-Stacking", command=lambda: self.cmd_visibility(Aro_P_common, self.var_common_P.get()), variable = self.var_common_P, font = font1, width = 10, anchor = "w")
        self.common_P.grid(row = 2, column = 0, sticky = W)
        self.common_P_nb = Label(self.common_Aro_frame, text = "", font = font2, width = 3)
        self.common_P_nb.grid(row = 2, column = 1)
        self.frame_color_common_P = Frame(self.common_Aro_frame)
        self.frame_color_common_P.grid(row = 2, column = 2)
        self.color_common_P = SINAPsColorWell(self.frame_color_common_P, "Aro_P_common", Arocolors["commonP"])

        self.common_TL = Checkbutton(self.common_Aro_frame, text="T/L-Shapes", command=lambda: self.cmd_visibility(Aro_TL_common, self.var_common_TL.get()), variable = self.var_common_TL, font = font1, width = 10, anchor = "w")
        self.common_TL.grid(row = 3, column = 0, sticky = W)
        self.common_TL_nb = Label(self.common_Aro_frame, text = "", font = font2, width = 3)
        self.common_TL_nb.grid(row = 3, column = 1)
        self.frame_color_common_TL = Frame(self.common_Aro_frame)
        self.frame_color_common_TL.grid(row = 3, column = 2)
        self.color_common_TL = SINAPsColorWell(self.frame_color_common_TL, "Aro_TL_common", Arocolors["commonTL"])

        self.common_T = Checkbutton(self.common_Aro_frame, text="T-Shape", command=lambda: self.cmd_visibility(Aro_T_common, self.var_common_T.get()), variable = self.var_common_T, font = font1, width = 10, anchor = "w")
        self.common_T.grid(row = 4, column = 0, sticky = W)
        self.common_T_nb = Label(self.common_Aro_frame, text = "", font = font2, width = 3)
        self.common_T_nb.grid(row = 4, column = 1)
        self.frame_color_common_T = Frame(self.common_Aro_frame)
        self.frame_color_common_T.grid(row = 4, column = 2)
        self.color_common_T = SINAPsColorWell(self.frame_color_common_T, "Aro_T_common", Arocolors["commonT"])

        self.common_L = Checkbutton(self.common_Aro_frame, text="L-Shape", command=lambda: self.cmd_visibility(Aro_L_common, self.var_common_L.get()), variable = self.var_common_L, font = font1, width = 10, anchor = "w")
        self.common_L.grid(row = 5, column = 0, sticky = W)
        self.common_L_nb = Label(self.common_Aro_frame, text = "", font = font2, width = 3)
        self.common_L_nb.grid(row = 5, column = 1)
        self.frame_color_common_L = Frame(self.common_Aro_frame)
        self.frame_color_common_L.grid(row = 5, column = 2)
        self.color_common_L = SINAPsColorWell(self.frame_color_common_L, "Aro_L_common", Arocolors["commonL"])

        ################################################################################################################

        self.exclu1_Aro = Checkbutton(self.exclu1_Aro_frame, text="All types", command=lambda: self.cmd_visibility(Aro_Aro_exclu1, self.var_exclu1_Aro.get()), variable = self.var_exclu1_Aro, font = font1, width = 10, anchor = "w")
        self.exclu1_Aro.grid(row = 1, column = 0, sticky = W)
        self.exclu1_Aro_nb = Label(self.exclu1_Aro_frame, text = "", font = font2, width = 3)
        self.exclu1_Aro_nb.grid(row = 1, column = 1)
        self.frame_color_exclu1_Aro = Frame(self.exclu1_Aro_frame)
        self.frame_color_exclu1_Aro.grid(row = 1, column = 2)
        self.color_exclu1_Aro = SINAPsColorWell(self.frame_color_exclu1_Aro, "Aro_Aro_exclu1", Arocolors["exclu1Aro"])

        self.exclu1_P = Checkbutton(self.exclu1_Aro_frame, text="Pi-Stacking", command=lambda: self.cmd_visibility(Aro_P_exclu1, self.var_exclu1_P.get()), variable = self.var_exclu1_P, font = font1, width = 10, anchor = "w")
        self.exclu1_P.grid(row = 2, column = 0, sticky = W)
        self.exclu1_P_nb = Label(self.exclu1_Aro_frame, text = "", font = font2, width = 3)
        self.exclu1_P_nb.grid(row = 2, column = 1)
        self.frame_color_exclu1_P = Frame(self.exclu1_Aro_frame)
        self.frame_color_exclu1_P.grid(row = 2, column = 2)
        self.color_exclu1_P = SINAPsColorWell(self.frame_color_exclu1_P, "Aro_P_exclu1", Arocolors["exclu1P"])

        self.exclu1_TL = Checkbutton(self.exclu1_Aro_frame, text="T/L-Shapes", command=lambda: self.cmd_visibility(Aro_TL_exclu1, self.var_exclu1_TL.get()), variable = self.var_exclu1_TL, font = font1, width = 10, anchor = "w")
        self.exclu1_TL.grid(row = 3, column = 0, sticky = W)
        self.exclu1_TL_nb = Label(self.exclu1_Aro_frame, text = "", font = font2, width = 3)
        self.exclu1_TL_nb.grid(row = 3, column = 1)
        self.frame_color_exclu1_TL = Frame(self.exclu1_Aro_frame)
        self.frame_color_exclu1_TL.grid(row = 3, column = 2)
        self.color_exclu1_TL = SINAPsColorWell(self.frame_color_exclu1_TL, "Aro_TL_exclu1", Arocolors["exclu1TL"])

        self.exclu1_T = Checkbutton(self.exclu1_Aro_frame, text="T-Shape", command=lambda: self.cmd_visibility(Aro_T_exclu1, self.var_exclu1_T.get()), variable = self.var_exclu1_T, font = font1, width = 10, anchor = "w")
        self.exclu1_T.grid(row = 4, column = 0, sticky = W)
        self.exclu1_T_nb = Label(self.exclu1_Aro_frame, text = "", font = font2, width = 3)
        self.exclu1_T_nb.grid(row = 4, column = 1)
        self.frame_color_exclu1_T = Frame(self.exclu1_Aro_frame)
        self.frame_color_exclu1_T.grid(row = 4, column = 2)
        self.color_exclu1_T = SINAPsColorWell(self.frame_color_exclu1_T, "Aro_T_exclu1", Arocolors["exclu1T"])

        self.exclu1_L = Checkbutton(self.exclu1_Aro_frame, text="L-Shape", command=lambda: self.cmd_visibility(Aro_L_exclu1, self.var_exclu1_L.get()), variable = self.var_exclu1_L, font = font1, width = 10, anchor = "w")
        self.exclu1_L.grid(row = 5, column = 0, sticky = W)
        self.exclu1_L_nb = Label(self.exclu1_Aro_frame, text = "", font = font2, width = 3)
        self.exclu1_L_nb.grid(row = 5, column = 1)
        self.frame_color_exclu1_L = Frame(self.exclu1_Aro_frame)
        self.frame_color_exclu1_L.grid(row = 5, column = 2)
        self.color_exclu1_L = SINAPsColorWell(self.frame_color_exclu1_L, "Aro_L_exclu1", Arocolors["exclu1L"])

        ################################################################################################################

        self.exclu2_Aro = Checkbutton(self.exclu2_Aro_frame, text="All types", command=lambda: self.cmd_visibility(Aro_Aro_exclu2, self.var_exclu2_Aro.get()), variable = self.var_exclu2_Aro, font = font1, width = 10, anchor = "w")
        self.exclu2_Aro.grid(row = 1, column = 0, sticky = W)
        self.exclu2_Aro_nb = Label(self.exclu2_Aro_frame, text = "", font = font2, width = 3)
        self.exclu2_Aro_nb.grid(row = 1, column = 1)
        self.frame_color_exclu2_Aro = Frame(self.exclu2_Aro_frame)
        self.frame_color_exclu2_Aro.grid(row = 1, column = 2)
        self.color_exclu2_Aro = SINAPsColorWell(self.frame_color_exclu2_Aro, "Aro_Aro_exclu2", Arocolors["exclu2Aro"])

        self.exclu2_P = Checkbutton(self.exclu2_Aro_frame, text="Pi-Stacking", command=lambda: self.cmd_visibility(Aro_P_exclu2, self.var_exclu2_P.get()), variable = self.var_exclu2_P, font = font1, width = 10, anchor = "w")
        self.exclu2_P.grid(row = 2, column = 0, sticky = W)
        self.exclu2_P_nb = Label(self.exclu2_Aro_frame, text = "", font = font2, width = 3)
        self.exclu2_P_nb.grid(row = 2, column = 1)
        self.frame_color_exclu2_P = Frame(self.exclu2_Aro_frame)
        self.frame_color_exclu2_P.grid(row = 2, column = 2)
        self.color_exclu2_P = SINAPsColorWell(self.frame_color_exclu2_P, "Aro_P_exclu2", Arocolors["exclu2P"])

        self.exclu2_TL = Checkbutton(self.exclu2_Aro_frame, text="T/L-Shapes", command=lambda: self.cmd_visibility(Aro_TL_exclu2, self.var_exclu2_TL.get()), variable = self.var_exclu2_TL, font = font1, width = 10, anchor = "w")
        self.exclu2_TL.grid(row = 3, column = 0, sticky = W)
        self.exclu2_TL_nb = Label(self.exclu2_Aro_frame, text = "", font = font2, width = 3)
        self.exclu2_TL_nb.grid(row = 3, column = 1)
        self.frame_color_exclu2_TL = Frame(self.exclu2_Aro_frame)
        self.frame_color_exclu2_TL.grid(row = 3, column = 2)
        self.color_exclu2_TL = SINAPsColorWell(self.frame_color_exclu2_TL, "Aro_TL_exclu2", Arocolors["exclu2TL"])

        self.exclu2_T = Checkbutton(self.exclu2_Aro_frame, text="T-Shape", command=lambda: self.cmd_visibility(Aro_T_exclu2, self.var_exclu2_T.get()), variable = self.var_exclu2_T, font = font1, width = 10, anchor = "w")
        self.exclu2_T.grid(row = 4, column = 0, sticky = W)
        self.exclu2_T_nb = Label(self.exclu2_Aro_frame, text = "", font = font2, width = 3)
        self.exclu2_T_nb.grid(row = 4, column = 1)
        self.frame_color_exclu2_T = Frame(self.exclu2_Aro_frame)
        self.frame_color_exclu2_T.grid(row = 4, column = 2)
        self.color_exclu2_T = SINAPsColorWell(self.frame_color_exclu2_T, "Aro_T_exclu2", Arocolors["exclu2T"])

        self.exclu2_L = Checkbutton(self.exclu2_Aro_frame, text="L-Shape", command=lambda: self.cmd_visibility(Aro_L_exclu2, self.var_exclu2_L.get()), variable = self.var_exclu2_L, font = font1, width = 10, anchor = "w")
        self.exclu2_L.grid(row = 5, column = 0, sticky = W)
        self.exclu2_L_nb = Label(self.exclu2_Aro_frame, text = "", font = font2, width = 3)
        self.exclu2_L_nb.grid(row = 5, column = 1)
        self.frame_color_exclu2_L = Frame(self.exclu2_Aro_frame)
        self.frame_color_exclu2_L.grid(row = 5, column = 2)
        self.color_exclu2_L = SINAPsColorWell(self.frame_color_exclu2_L, "Aro_L_exclu2", Arocolors["exclu2L"])

    ###################################################################################################################~

    def cmd_HB_common_ALL(self):
        if self.var_common_ALL.get() == 0:
            self.var_common_BB.set(0) ; self.var_common_BC.set(0) ; self.var_common_CC.set(0)
        else:
            self.var_common_BB.set(1) ; self.var_common_BC.set(1) ; self.var_common_CC.set(1)
        self.cmd_visibility(HB_common_BB, self.var_common_BB.get())
        self.cmd_visibility(HB_common_BC, self.var_common_BC.get())
        self.cmd_visibility(HB_common_CC, self.var_common_CC.get())

    def cmd_HB_exclu1_ALL(self):
        if self.var_exclu1_ALL.get() == 0:
            self.var_exclu1_BB.set(0) ; self.var_exclu1_BC.set(0) ; self.var_exclu1_CC.set(0)
        else:
            self.var_exclu1_BB.set(1) ; self.var_exclu1_BC.set(1) ; self.var_exclu1_CC.set(1)
        self.cmd_visibility(HB_exclu1_BB, self.var_exclu1_BB.get())
        self.cmd_visibility(HB_exclu1_BC, self.var_exclu1_BC.get())
        self.cmd_visibility(HB_exclu1_CC, self.var_exclu1_CC.get())
        
    def cmd_HB_exclu2_ALL(self):
        if self.var_exclu2_ALL.get() == 0:
            self.var_exclu2_BB.set(0) ; self.var_exclu2_BC.set(0) ; self.var_exclu2_CC.set(0)
        else:
            self.var_exclu2_BB.set(1) ; self.var_exclu2_BC.set(1) ; self.var_exclu2_CC.set(1)
        self.cmd_visibility(HB_exclu2_BB, self.var_exclu2_BB.get())
        self.cmd_visibility(HB_exclu2_BC, self.var_exclu2_BC.get())
        self.cmd_visibility(HB_exclu2_CC, self.var_exclu2_CC.get())


    ###################################################################################################################~

    def cmd_visibility(self, dico, variable):
        global threshold
        if variable == 0:
            for Bond in dico:
                if (dico[Bond][0] != -1) & (dico[Bond][3] >= threshold): dico[Bond][0].display = 0
                if (dico[Bond][1] != -1) & (dico[Bond][4] >= threshold): dico[Bond][1].display = 0
        else:
            for Bond in dico:
                if (dico[Bond][0] != -1) & (dico[Bond][3] >= threshold): dico[Bond][0].display = 1
                if (dico[Bond][1] != -1) & (dico[Bond][4] >= threshold): dico[Bond][1].display = 1


    ################################################################################################################

    def BrowseDirectory(self):
        global default_folder

        if self.loading_error["background"] == "red":
            self.loading_error.config({"background": self.frame1["background"]})
            self.loading_error.update()

        self.directory = tkFileDialog.askdirectory(initialdir = default_folder)

        default_folder = self.directory
        self.loading_entry.delete(0, END)
        self.loading_entry.insert(0, self.directory)


    ################################################################################################################

    def Loading(self):
        filelist = os.listdir(self.loading_entry.get())

        Repr1_file = [i for i in filelist if "Representative1_" in i]
        Repr2_file = [i for i in filelist if "Representative2_" in i]
        Results_HB_file = [i for i in filelist if "Results_HB_" in i]
        Results_SB_file = [i for i in filelist if "Results_SB_" in i]
        Results_Aro_file = [i for i in filelist if "Results_Aro_" in i]

        if len(Repr1_file) != 0 and len(Repr2_file) != 0 and len(Results_HB_file) != 0 and len(Results_Aro_file) != 0 and len(Results_SB_file) != 0:
            # Chargement Representative1
            rc("open {0}/{1}".format(self.loading_entry.get(), Repr1_file[0]))
            chimera_representative1 = chimera.openModels.list()[0]
            self.exclu1_label["text"] = str(chimera_representative1.name)[16:-4]

            # Chargement Representative2
            rc("open {0}/{1}".format(self.loading_entry.get(), Repr2_file[0]))
            chimera_representative2 = chimera.openModels.list()[1]
            self.exclu2_label["text"] = str(chimera_representative2.name)[16:-4]

            ##### Chargement Pseudobonds
            # HBONDS - Creation groupe de pseudobonds + dico en var globale
            gp_HB_SINAPs = chimera.misc.getPseudoBondGroup("SINAPs - Hydrogen bonds")
            gp_HB_SINAPs.lineWidth = 10
            global hbonds_dict
            hbonds_dict = {}

            # SALT BRIDGES - Creation groupe de pseudobonds + dico en var globale
            gp_SB_SINAPs = chimera.misc.getPseudoBondGroup("SINAPs - Salt bridges")
            gp_SB_SINAPs.lineWidth = 10
            global sb_dict
            sb_dict = {}
            
            # ARO - Creation groupe de pseudobonds + dico en var globale
            gp_Aro_SINAPs = chimera.misc.getPseudoBondGroup("SINAPs - Aromatics")
            gp_Aro_SINAPs.lineWidth = 10
            global aro_dict
            aro_dict = {}


            # Lecture des resultats - HBONDS
            with open("{0}/{1}".format(self.loading_entry.get(), Results_HB_file[0]), "r") as read_results:
                HB_list = read_results.readlines()

            for line in HB_list:
                line_splitted = line[:-1].split(" ")
                HB_name = "-".join(line_splitted[0:2])

                if line_splitted[0] != line_splitted[1]:
                    if line_splitted[7] != "-1":
                        pb1 = gp_HB_SINAPs.newPseudoBond(chimera_representative1.atoms[int(line_splitted[2])], chimera_representative1.atoms[int(line_splitted[3])])
                        pb1.display = 0
                    else:
                        pb1 = -1

                    if line_splitted[8] != "-1":
                        pb2 = gp_HB_SINAPs.newPseudoBond(chimera_representative2.atoms[int(line_splitted[4])], chimera_representative2.atoms[int(line_splitted[5])])
                        pb2.display = 0
                    else:
                        pb2 = -1

                    hbonds_dict[HB_name] = (pb1, pb2, int(line_splitted[6]), float(line_splitted[7]), float(line_splitted[8]))


            # Lecture des resultats - SALT BRIDGES
            with open("{0}/{1}".format(self.loading_entry.get(), Results_SB_file[0]), "r") as read_results:
                SB_list = read_results.readlines()

            for line in SB_list:
                line_splitted = line[:-1].split(" ")
                SB_name = "-".join(line_splitted[0:2])

                if line_splitted[0] != line_splitted[1]:
                    if line_splitted[6] != "-1":
                        pb1 = gp_SB_SINAPs.newPseudoBond(chimera_representative1.atoms[int(line_splitted[2])], chimera_representative1.atoms[int(line_splitted[3])])
                        pb1.display = 0
                    else:
                        pb1 = -1

                    if line_splitted[7] != "-1":
                        pb2 = gp_SB_SINAPs.newPseudoBond(chimera_representative2.atoms[int(line_splitted[4])], chimera_representative2.atoms[int(line_splitted[5])])
                        pb2.display = 0
                    else:
                        pb2 = -1

                    sb_dict[SB_name] = (pb1, pb2, "SB", float(line_splitted[6]), float(line_splitted[7]))


            # Lecture des resultats - AROMATICS
            with open("{0}/{1}".format(self.loading_entry.get(), Results_Aro_file[0]), "r") as read_Aro:
                Aro_list = read_Aro.readlines()

            for line in Aro_list:
                line_splitted = line[:-1].split(" ")
                if line_splitted[0] == "AA1":
                    continue

                Aro_name = "-".join(line_splitted[0:2])
                temp = {}

                for case in ["ALL", "P", "TL", "T", "L"]:
                    if line_splitted[2] != "-1":
                        pb1 = gp_Aro_SINAPs.newPseudoBond(chimera_representative1.atoms[int(line_splitted[2])], chimera_representative1.atoms[int(line_splitted[3])])
                        pb1.display = 0
                    else:
                        pb1 = -1

                    if line_splitted[4] != "-1":
                        pb2 = gp_Aro_SINAPs.newPseudoBond(chimera_representative2.atoms[int(line_splitted[4])], chimera_representative2.atoms[int(line_splitted[5])])
                        pb2.display = 0
                    else:
                        pb2 = -1

                    if case == "ALL":
                        temp[case] = [pb1, pb2, case, float(line_splitted[6]), float(line_splitted[7])]
                    elif case == "P":
                        temp[case] = [pb1, pb2, case, float(line_splitted[8]), float(line_splitted[9])]
                    elif case == "TL":
                        temp[case] = [pb1, pb2, case, float(line_splitted[10]), float(line_splitted[11])]
                    elif case == "T":
                        temp[case] = [pb1, pb2, case, float(line_splitted[12]), float(line_splitted[13])]
                    elif case == "L":
                        temp[case] = [pb1, pb2, case, float(line_splitted[14]), float(line_splitted[15])]

                aro_dict[Aro_name] = temp

            global SINAPs_loaded ; SINAPs_loaded = 1
            self.cmd_frequency()
            self.frame1.pack_forget()
            self.frame2.pack(fill=X, expand = 1)

        else:
            self.loading_error["text"] = "ERROR - Wrong folder"
            self.loading_error.config({"background": "red"})
            self.loading_error.update()


    ###################################################################################################################~

    def cmd_frequency(self):
        global threshold
        threshold = float(self.frequency_slider.get()) / 100

        ##### HBONDS #####~
        global HB_common_BB ; global HB_common_BC ; global HB_common_CC
        global HB_exclu1_BB ; global HB_exclu1_BC ; global HB_exclu1_CC
        global HB_exclu2_BB ; global HB_exclu2_BC ; global HB_exclu2_CC

        HB_common_BB = {} ; HB_common_BC = {} ; HB_common_CC = {}
        HB_exclu1_BB = {} ; HB_exclu1_BC = {} ; HB_exclu1_CC = {}
        HB_exclu2_BB = {} ; HB_exclu2_BC = {} ; HB_exclu2_CC = {}

        for PB_HB in hbonds_dict:
            # COMMON
            if hbonds_dict[PB_HB][3] >= threshold and hbonds_dict[PB_HB][4] >= threshold:
                if hbonds_dict[PB_HB][2] == 1:
                    HB_common_BB[PB_HB] = hbonds_dict[PB_HB]
                    HB_common_BB[PB_HB][0].color = self.color_common_BB.get()
                    HB_common_BB[PB_HB][1].color = self.color_common_BB.get()
                elif hbonds_dict[PB_HB][2] == 2:
                    HB_common_BC[PB_HB] = hbonds_dict[PB_HB]
                    HB_common_BC[PB_HB][0].color = self.color_common_BC.get()
                    HB_common_BC[PB_HB][1].color = self.color_common_BC.get()
                elif hbonds_dict[PB_HB][2] == 3:
                    HB_common_CC[PB_HB] = hbonds_dict[PB_HB]
                    HB_common_CC[PB_HB][0].color = self.color_common_CC.get()
                    HB_common_CC[PB_HB][1].color = self.color_common_CC.get()

            # EXCLU TRAJ1
            elif hbonds_dict[PB_HB][3] >= threshold and hbonds_dict[PB_HB][4] < threshold:
                if hbonds_dict[PB_HB][2] == 1:
                    HB_exclu1_BB[PB_HB] = hbonds_dict[PB_HB]
                    HB_exclu1_BB[PB_HB][0].color = self.color_exclu1_BB.get()
                elif hbonds_dict[PB_HB][2] == 2:
                    HB_exclu1_BC[PB_HB] = hbonds_dict[PB_HB]
                    HB_exclu1_BC[PB_HB][0].color = self.color_exclu1_BC.get()
                elif hbonds_dict[PB_HB][2] == 3:
                    HB_exclu1_CC[PB_HB] = hbonds_dict[PB_HB]
                    HB_exclu1_CC[PB_HB][0].color = self.color_exclu1_CC.get()

            # EXCLU TRAJ2
            elif hbonds_dict[PB_HB][3] < threshold and hbonds_dict[PB_HB][4] >= threshold:
                if hbonds_dict[PB_HB][2] == 1:
                    HB_exclu2_BB[PB_HB] = hbonds_dict[PB_HB]
                    HB_exclu2_BB[PB_HB][1].color = self.color_exclu2_BB.get()
                elif hbonds_dict[PB_HB][2] == 2:
                    HB_exclu2_BC[PB_HB] = hbonds_dict[PB_HB]
                    HB_exclu2_BC[PB_HB][1].color = self.color_exclu2_BC.get()
                elif hbonds_dict[PB_HB][2] == 3:
                    HB_exclu2_CC[PB_HB] = hbonds_dict[PB_HB]
                    HB_exclu2_CC[PB_HB][1].color = self.color_exclu2_CC.get()


        ##### SALT BRIDGES #####~
        global SB_common ; global SB_exclu1 ; global SB_exclu2

        SB_common = {} ; SB_exclu1 = {} ; SB_exclu2 = {}

        for PB_SB in sb_dict:
            # COMMON
            if sb_dict[PB_SB][3] >= threshold and sb_dict[PB_SB][4] >= threshold:
                SB_common[PB_SB] = sb_dict[PB_SB]
                SB_common[PB_SB][0].color = self.color_common_SB.get()
                SB_common[PB_SB][1].color = self.color_common_SB.get()

            # EXCLU TRAJ1
            elif sb_dict[PB_SB][3] >= threshold and sb_dict[PB_SB][4] < threshold:
                SB_exclu1[PB_SB] = sb_dict[PB_SB]
                SB_exclu1[PB_SB][0].color = self.color_exclu1_SB.get()

            # EXCLU TRAJ2
            elif sb_dict[PB_SB][3] < threshold and sb_dict[PB_SB][4] >= threshold:
                SB_exclu2[PB_SB] = sb_dict[PB_SB]
                SB_exclu2[PB_SB][1].color = self.color_exclu2_SB.get()

        ##### AROMATICS #####~
        global Aro_Aro_common ; global Aro_P_common ; global Aro_TL_common ; global Aro_T_common ; global Aro_L_common
        global Aro_Aro_exclu1 ; global Aro_P_exclu1 ; global Aro_TL_exclu1 ; global Aro_T_exclu1 ; global Aro_L_exclu1
        global Aro_Aro_exclu2 ; global Aro_P_exclu2 ; global Aro_TL_exclu2 ; global Aro_T_exclu2 ; global Aro_L_exclu2

        Aro_Aro_common = {} ; Aro_P_common = {} ; Aro_TL_common = {} ; Aro_T_common = {} ; Aro_L_common = {}
        Aro_Aro_exclu1 = {} ; Aro_P_exclu1 = {} ; Aro_TL_exclu1 = {} ; Aro_T_exclu1 = {} ; Aro_L_exclu1 = {}
        Aro_Aro_exclu2 = {} ; Aro_P_exclu2 = {} ; Aro_TL_exclu2 = {} ; Aro_T_exclu2 = {} ; Aro_L_exclu2 = {}

        for PB_Aro in aro_dict:
            # ALL ARO
            if aro_dict[PB_Aro]["ALL"][3] >= threshold and aro_dict[PB_Aro]["ALL"][4] >= threshold:
                Aro_Aro_common[PB_Aro] = aro_dict[PB_Aro]["ALL"]
                Aro_Aro_common[PB_Aro][0].color = self.color_common_Aro.get()
                Aro_Aro_common[PB_Aro][1].color = self.color_common_Aro.get()
            elif aro_dict[PB_Aro]["ALL"][3] >= threshold and aro_dict[PB_Aro]["ALL"][4] < threshold:
                Aro_Aro_exclu1[PB_Aro] = aro_dict[PB_Aro]["ALL"]
                Aro_Aro_exclu1[PB_Aro][0].color = self.color_exclu1_Aro.get()
            elif aro_dict[PB_Aro]["ALL"][3] < threshold and aro_dict[PB_Aro]["ALL"][4] >= threshold:
                Aro_Aro_exclu2[PB_Aro] = aro_dict[PB_Aro]["ALL"]
                Aro_Aro_exclu2[PB_Aro][1].color = self.color_exclu2_Aro.get()

            # PI-STACKING
            if aro_dict[PB_Aro]["P"][3] >= threshold and aro_dict[PB_Aro]["P"][4] >= threshold:
                Aro_P_common[PB_Aro] = aro_dict[PB_Aro]["P"]
                Aro_P_common[PB_Aro][0].color = self.color_common_P.get()
                Aro_P_common[PB_Aro][1].color = self.color_common_P.get()
            elif aro_dict[PB_Aro]["P"][3] >= threshold and aro_dict[PB_Aro]["P"][4] < threshold:
                Aro_P_exclu1[PB_Aro] = aro_dict[PB_Aro]["P"]
                Aro_P_exclu1[PB_Aro][0].color = self.color_exclu1_P.get()
            elif aro_dict[PB_Aro]["P"][3] < threshold and aro_dict[PB_Aro]["P"][4] >= threshold:
                Aro_P_exclu2[PB_Aro] = aro_dict[PB_Aro]["P"]
                Aro_P_exclu2[PB_Aro][1].color = self.color_exclu2_P.get()
                
            # T/L-Shapes
            if aro_dict[PB_Aro]["TL"][3] >= threshold and aro_dict[PB_Aro]["TL"][4] >= threshold:
                Aro_TL_common[PB_Aro] = aro_dict[PB_Aro]["TL"]
                Aro_TL_common[PB_Aro][0].color = self.color_common_TL.get()
                Aro_TL_common[PB_Aro][1].color = self.color_common_TL.get()
            elif aro_dict[PB_Aro]["TL"][3] >= threshold and aro_dict[PB_Aro]["TL"][4] < threshold:
                Aro_TL_exclu1[PB_Aro] = aro_dict[PB_Aro]["TL"]
                Aro_TL_exclu1[PB_Aro][0].color = self.color_exclu1_TL.get()
            elif aro_dict[PB_Aro]["TL"][3] < threshold and aro_dict[PB_Aro]["TL"][4] >= threshold:
                Aro_TL_exclu2[PB_Aro] = aro_dict[PB_Aro]["TL"]
                Aro_TL_exclu2[PB_Aro][1].color = self.color_exclu2_TL.get()

            # T-Shape
            if aro_dict[PB_Aro]["T"][3] >= threshold and aro_dict[PB_Aro]["T"][4] >= threshold:
                Aro_T_common[PB_Aro] = aro_dict[PB_Aro]["T"]
                Aro_T_common[PB_Aro][0].color = self.color_common_T.get()
                Aro_T_common[PB_Aro][1].color = self.color_common_T.get()
            elif aro_dict[PB_Aro]["T"][3] >= threshold and aro_dict[PB_Aro]["T"][4] < threshold:
                Aro_T_exclu1[PB_Aro] = aro_dict[PB_Aro]["T"]
                Aro_T_exclu1[PB_Aro][0].color = self.color_exclu1_T.get()
            elif aro_dict[PB_Aro]["T"][3] < threshold and aro_dict[PB_Aro]["T"][4] >= threshold:
                Aro_T_exclu2[PB_Aro] = aro_dict[PB_Aro]["T"]
                Aro_T_exclu2[PB_Aro][1].color = self.color_exclu2_T.get()
                
            # L-Shape
            if aro_dict[PB_Aro]["L"][3] >= threshold and aro_dict[PB_Aro]["L"][4] >= threshold:
                Aro_L_common[PB_Aro] = aro_dict[PB_Aro]["L"]
                Aro_L_common[PB_Aro][0].color = self.color_common_L.get()
                Aro_L_common[PB_Aro][1].color = self.color_common_L.get()
            elif aro_dict[PB_Aro]["L"][3] >= threshold and aro_dict[PB_Aro]["L"][4] < threshold:
                Aro_L_exclu1[PB_Aro] = aro_dict[PB_Aro]["L"]
                Aro_L_exclu1[PB_Aro][0].color = self.color_exclu1_L.get()
            elif aro_dict[PB_Aro]["L"][3] < threshold and aro_dict[PB_Aro]["L"][4] >= threshold:
                Aro_L_exclu2[PB_Aro] = aro_dict[PB_Aro]["L"]
                Aro_L_exclu2[PB_Aro][1].color = self.color_exclu2_L.get()

        ##### FOOTER #####~
        self.refresh()
        self.frequency_label["text"] = "Lower frequency limit currently set to {0}%".format(self.frequency_slider.get())


    ###################################################################################################################~

    def label_update(self, Label, dico):
        Label["text"] = len(dico)
        Label.update()


    ###################################################################################################################~

    def refresh(self):
        # HIDE
        for PB_HB in hbonds_dict:
            if hbonds_dict[PB_HB][0] != -1: hbonds_dict[PB_HB][0].display = 0
            if hbonds_dict[PB_HB][1] != -1: hbonds_dict[PB_HB][1].display = 0

        for PB_SB in sb_dict:
            if sb_dict[PB_SB][0] != -1: sb_dict[PB_SB][0].display = 0
            if sb_dict[PB_SB][1] != -1: sb_dict[PB_SB][1].display = 0
            
        for PB_Aro in aro_dict:
            for case in ["ALL", "P", "TL", "T", "L"]:
                if aro_dict[PB_Aro][case][0] != -1: aro_dict[PB_Aro][case][0].display = 0
                if aro_dict[PB_Aro][case][1] != -1: aro_dict[PB_Aro][case][1].display = 0

        ##### REFRESH HBONDS #####
        self.cmd_visibility(HB_common_BB, self.var_common_BB.get()) ; self.label_update(self.common_BB_nb, HB_common_BB)
        self.cmd_visibility(HB_common_BC, self.var_common_BC.get()) ; self.label_update(self.common_BC_nb, HB_common_BC)
        self.cmd_visibility(HB_common_CC, self.var_common_CC.get()) ; self.label_update(self.common_CC_nb, HB_common_CC)

        self.cmd_visibility(HB_exclu1_BB, self.var_exclu1_BB.get()) ; self.label_update(self.exclu1_BB_nb, HB_exclu1_BB)
        self.cmd_visibility(HB_exclu1_BC, self.var_exclu1_BC.get()) ; self.label_update(self.exclu1_BC_nb, HB_exclu1_BC)
        self.cmd_visibility(HB_exclu1_CC, self.var_exclu1_CC.get()) ; self.label_update(self.exclu1_CC_nb, HB_exclu1_CC)

        self.cmd_visibility(HB_exclu2_BB, self.var_exclu2_BB.get()) ; self.label_update(self.exclu2_BB_nb, HB_exclu2_BB)
        self.cmd_visibility(HB_exclu2_BC, self.var_exclu2_BC.get()) ; self.label_update(self.exclu2_BC_nb, HB_exclu2_BC)
        self.cmd_visibility(HB_exclu2_CC, self.var_exclu2_CC.get()) ; self.label_update(self.exclu2_CC_nb, HB_exclu2_CC)

        ##### REFRESH SALT BRIDGES #####
        self.cmd_visibility(SB_common, self.var_common_SB.get()) ; self.label_update(self.common_SB_nb, SB_common)
        self.cmd_visibility(SB_exclu1, self.var_exclu1_SB.get()) ; self.label_update(self.exclu1_SB_nb, SB_exclu1)
        self.cmd_visibility(SB_exclu2, self.var_exclu2_SB.get()) ; self.label_update(self.exclu2_SB_nb, SB_exclu2)

        ##### REFRESH PI-PI INTERACTIONS #####
        self.cmd_visibility(Aro_Aro_common, self.var_common_Aro.get()) ; self.label_update(self.common_Aro_nb, Aro_Aro_common)
        self.cmd_visibility(Aro_Aro_exclu1, self.var_exclu1_Aro.get()) ; self.label_update(self.exclu1_Aro_nb, Aro_Aro_exclu1)
        self.cmd_visibility(Aro_Aro_exclu2, self.var_exclu2_Aro.get()) ; self.label_update(self.exclu2_Aro_nb, Aro_Aro_exclu2)
        
        self.cmd_visibility(Aro_P_common, self.var_common_P.get()) ; self.label_update(self.common_P_nb, Aro_P_common)
        self.cmd_visibility(Aro_P_exclu1, self.var_exclu1_P.get()) ; self.label_update(self.exclu1_P_nb, Aro_P_exclu1)
        self.cmd_visibility(Aro_P_exclu2, self.var_exclu2_P.get()) ; self.label_update(self.exclu2_P_nb, Aro_P_exclu2)
    
        self.cmd_visibility(Aro_TL_common, self.var_common_TL.get()) ; self.label_update(self.common_TL_nb, Aro_TL_common)
        self.cmd_visibility(Aro_TL_exclu1, self.var_exclu1_TL.get()) ; self.label_update(self.exclu1_TL_nb, Aro_TL_exclu1)
        self.cmd_visibility(Aro_TL_exclu2, self.var_exclu2_TL.get()) ; self.label_update(self.exclu2_TL_nb, Aro_TL_exclu2)

        self.cmd_visibility(Aro_T_common, self.var_common_T.get()) ; self.label_update(self.common_T_nb, Aro_T_common)
        self.cmd_visibility(Aro_T_exclu1, self.var_exclu1_T.get()) ; self.label_update(self.exclu1_T_nb, Aro_T_exclu1)
        self.cmd_visibility(Aro_T_exclu2, self.var_exclu2_T.get()) ; self.label_update(self.exclu2_T_nb, Aro_T_exclu2)
    
        self.cmd_visibility(Aro_L_common, self.var_common_L.get()) ; self.label_update(self.common_L_nb, Aro_L_common)
        self.cmd_visibility(Aro_L_exclu1, self.var_exclu1_L.get()) ; self.label_update(self.exclu1_L_nb, Aro_L_exclu1)
        self.cmd_visibility(Aro_L_exclu2, self.var_exclu2_L.get()) ; self.label_update(self.exclu2_L_nb, Aro_L_exclu2)


    ###################################################################################################################~

    def Apply(self):
        if SINAPs_loaded == 0:
            self.Loading()
        else:
            self.cmd_frequency()

    ###################################################################################################################~

    def destroy(self):
        if self._closeSesHandler:
            chimera.triggers.deleteHandler(chimera.CLOSE_SESSION, self._closeSesHandler)
            self._closeSesHandler = None
        manager.deregisterInstance(self)
        ModelessDialog.destroy(self)

    ###################################################################################################################~

    def emName(self):
        return self.title

    def emRaise(self):
        self.enter()

    def emHide(self):
        self.Close()

    def emQuit(self, *args):
        self.destroy()

#######################################################################################################################~

from chimera import dialogs
dialogs.register(SINAPs_GUI_loader.name, SINAPs_GUI_loader)

#######################################################################################################################~
