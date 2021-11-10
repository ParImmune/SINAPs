# --- UCSF Chimera Copyright ---
# Copyright (c) 2000 Regents of the University of California.
# All rights reserved.  This software provided pursuant to a
# license agreement containing restrictions on its disclosure,
# duplication and use.  This notice must be embedded in or
# attached to all copies, including partial copies, of the
# software or any revisions or derivations thereof.
# --- UCSF Chimera Copyright ---

import chimera.extension
from chimera.dialogs import display

class SINAPs_EMO(chimera.extension.EMO):
	def name(self):
		return 'SINAPs Visualizer'
	def description(self):
		return 'SINAPs Visualizer'
	def categories(self):
		return ['SINAPs']
	def icon(self):
		return self.path('SINAPs_icon.png')
	def activate(self):
		display(self.module("gui").SINAPs_GUI_loader.name)
		return None

chimera.extension.manager.registerExtension(SINAPs_EMO(__file__))
