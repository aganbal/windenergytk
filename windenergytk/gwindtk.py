#!/usr/bin/env python
# -*- coding: utf-8 -*-

################################################################################
# gwindetk.py                                                                  #
#                                                                              #
# Part of UMass Amherst's Wind Energy Engineering Toolbox of Mini-Codes        #
#                   (or Mini-Codes for short)                                  #
#                                                                              #
# Python code by Alec Koumjian  -   akoumjian@gmail.com                        #
#                                                                              #
# This code adapted from the original Visual Basic code at                     #
# http://www.ceere.org/rerl/projects/software/mini-code-overview.html          #
#                                                                              #
# These tools can be used in conjunction with the textbook                     #
# "Wind Energy Explained" by J.F. Manwell, J.G. McGowan and A.L. Rogers        #
# http://www.ceere.org/rerl/rerl_windenergytext.html                           #
#                                                                              #
################################################################################
#   Copyright 2009 Alec Koumjian                                               #
#                                                                              #
#   This program is free software: you can redistribute it and/or modify       #
#   it under the terms of the GNU General Public License as published by       #
#   the Free Software Foundation, either version 3 of the License, or          #
#   (at your option) any later version.                                        #
#                                                                              #
#    This program is distributed in the hope that it will be useful,           #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of            #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the             #
#    GNU General Public License for more details.                              #
#                                                                              #
#    You should have received a copy of the GNU General Public License         #
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.     #
################################################################################

import wxversion
wxversion.select('2.8')
import wx
import wx.lib.intctrl as intctrl
import wxmpl
import os
import analysis
import synthesis
import file_ops


class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["size"] = (800, 600)
        kwds["style"] = wx.DEFAULT_FRAME_STYLE

        wx.Frame.__init__(self, *args, **kwds)
        self.active_timeseries = {}
        self.__create_objects()
        self.__set_properties()
        self.__do_layout()
        self.__set_bindings()
        self.sync_active_listbox()

    def __create_objects(self):
        # Menu Bar
        self.frame_1_menubar = wx.MenuBar()
        # File menu
        self.file_menu = wx.Menu()
        self.import_file = wx.MenuItem(self.file_menu, -1, "Import", "Import timeseries from data file")
        self.file_menu.AppendItem(self.import_file)
        self.frame_1_menubar.Append(self.file_menu, "File")
        # Help Menu
        self.help_menu = wx.Menu()
        self.help_book = wx.MenuItem(self.help_menu, -1, "Help Index", "How to use this software.")
        self.about = wx.MenuItem(self.help_menu, -1, "About","About this software.")
        self.help_menu.AppendItem(self.about)
        self.frame_1_menubar.Append(self.help_menu, "Help")
        # Set Menu Bar
        self.SetMenuBar(self.frame_1_menubar)
        # Menu Bar end
        
        # Status Bar
        self.frame_1_statusbar = self.CreateStatusBar(1, 0)
        # Status Bar end
        
        # Tool Bar
        self.frame_1_toolbar = wx.ToolBar(self, -1, style=wx.TB_HORIZONTAL|wx.TB_3DBUTTONS)
        self.SetToolBar(self.frame_1_toolbar)
        self.frame_1_toolbar.AddLabelTool(wx.NewId(), "new", wx.Bitmap("stock_new.png", wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, "", "")
        self.frame_1_toolbar.AddLabelTool(wx.NewId(), "open", wx.Bitmap("stock_open.png", wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, "", "")
        self.frame_1_toolbar.AddLabelTool(wx.NewId(), "save", wx.Bitmap("stock_save.png", wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, "", "")
        self.frame_1_toolbar.AddLabelTool(wx.NewId(), "exit", wx.Bitmap("stock_exit.png", wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, "", "")
        # Tool Bar end
        
        # Top level sizers
        self.sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer_3 = wx.BoxSizer(wx.VERTICAL)
        # Splitter
        self.splitter = wx.SplitterWindow(self, -1, style=wx.SP_3DSASH|wx.SP_3DBORDER)
        
        # TS panel widgets
        self.sizer_ts = wx.BoxSizer(wx.VERTICAL)
        self.sizer_control_ts = wx.BoxSizer(wx.HORIZONTAL)
        self.ts_control_panel = wx.Panel(self.splitter, -1)
        self.list_box_1 = wx.ListBox(self.ts_control_panel, -1, choices=[], style=wx.LB_MULTIPLE|wx.LB_NEEDED_SB)
        self.ts_plot_button = wx.Button(self.ts_control_panel, -1, 'Plot Timeseries')
        self.ts_remove_button = wx.Button(self.ts_control_panel, -1, 'Remove')
        
        # Notebook
        self.notebook_1 = wx.Notebook(self.splitter, -1, style=wx.NB_LEFT)
        self.notebook_1_pane_1 = wx.Panel(self.notebook_1, -1)
        self.notebook_1_pane_2 = wx.Panel(self.notebook_1, -1)
        self.notebook_1_pane_3 = wx.Panel(self.notebook_1, -1)
        self.notebook_1_pane_4 = wx.Panel(self.notebook_1, -1)
        self.notebook_1_pane_5 = wx.Panel(self.notebook_1, -1)
        self.notebook_1_pane_6 = wx.Panel(self.notebook_1, -1)
        
        # Text results panel
        self.results_panel = wx.Panel(self, -1, style=wx.SIMPLE_BORDER)
        self.results_panel_text = wx.StaticText(self.results_panel, -1, label="Results Here")
        
        # Graphing panel
        self.plot_panel = wxmpl.PlotPanel(self, -1)
        
        # Analysis widgets
        self.analysis_sizer = wx.BoxSizer(wx.VERTICAL)
        self.stat_button = wx.Button(self.notebook_1_pane_1, -1, 'Statistics')
        self.hist_button = wx.Button(self.notebook_1_pane_1, -1, 'Histogram')
        self.weibull_button = wx.Button(self.notebook_1_pane_1, -1, 'Weibull Params')
        self.corr_button = wx.Button(self.notebook_1_pane_1, -1, 'Correlate')
        self.corr_panel = wx.Panel(self.notebook_1_pane_1, -1, style=wx.RAISED_BORDER)
        self.corr_panel_btn = wx.Button(self.notebook_1_pane_1, -1, '>>', name='corr')
        self.corr_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.rad_autocorr = wx.RadioButton(self.corr_panel, -1, 'Auto', style=wx.RB_GROUP)
        self.rad_crosscorr = wx.RadioButton(self.corr_panel, -1, 'Cross')
        self.corr_lag_int = intctrl.IntCtrl(self.corr_panel, -1, value=15, min=0)
        self.lag_label = wx.StaticText(self.corr_panel, -1, 'No. lags')
        self.block_button = wx.Button(self.notebook_1_pane_1, -1, 'Block Average')
        self.block_panel = wx.Panel(self.notebook_1_pane_1, -1, style=wx.RAISED_BORDER)
        self.block_panel_btn = wx.Button(self.notebook_1_pane_1, -1, '>>', name='block')
        self.block_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.block_new_freq = wx.Choice(self.block_panel, -1, choices=['YEARLY','QUARTERLY','MONTHLY','WEEKLY','DAILY','HOURLY','MINUTELY'])
        self.psd_button = wx.Button(self.notebook_1_pane_1, -1, 'Power Spectral Density')
        # End Analysis widgets
        
        # Synthesis widgets
        self.mean_lbl = wx.StaticText(self.notebook_1_pane_2, -1, 'Mean:')
        self.stdev_lbl = wx.StaticText(self.notebook_1_pane_2, -1, 'STDEV:')
        self.npoints_lbl = wx.StaticText(self.notebook_1_pane_2, -1, 'No. points:')
        self.autocorr_lbl = wx.StaticText(self.notebook_1_pane_2, -1, 'Autocorr:')
        self.mean_ctrl = wx.TextCtrl(self.notebook_1_pane_2, -1, '')
        self.stdev_ctrl = wx.TextCtrl(self.notebook_1_pane_2, -1, '')
        self.npoints_ctrl = wx.TextCtrl(self.notebook_1_pane_2, -1, '')
        self.autocorr_ctrl = wx.TextCtrl(self.notebook_1_pane_2, -1, '')
        self.arma_button = wx.Button(self.notebook_1_pane_2, -1, 'ARMA')
        # End Synthesis widgets
        
    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle("Wind Energy Engineering Toolkit")
        _icon = wx.EmptyIcon()
        _icon.CopyFromBitmap(wx.Bitmap("wec.ico", wx.BITMAP_TYPE_ANY))
        self.SetIcon(_icon)
        self.frame_1_statusbar.SetStatusWidths([-1])
        # statusbar fields
        frame_1_statusbar_fields = ["The Minicodes at your service!"]
        for i in range(len(frame_1_statusbar_fields)):
            self.frame_1_statusbar.SetStatusText(frame_1_statusbar_fields[i], i)
        self.frame_1_toolbar.Realize()


    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        
        # Graph/plot panel
        self.plot_panel.SetMinSize((50,50))
        
        # Results panel
        self.results_panel_text.Move((20,10))
        
        # Add Notebook pages
        self.notebook_1.AddPage(self.notebook_1_pane_1, "Analysis")
        self.notebook_1.AddPage(self.notebook_1_pane_2, "Synthesis")
        self.notebook_1.AddPage(self.notebook_1_pane_3, "Rotor")
        self.notebook_1.AddPage(self.notebook_1_pane_4, "Electrical")
        self.notebook_1.AddPage(self.notebook_1_pane_5, "Dynamics")
        self.notebook_1.AddPage(self.notebook_1_pane_6, "System")
        
        # Analysis layout
        self.corr_sizer.Add(self.corr_button,1)
        self.corr_sizer.Add(self.corr_panel_btn,0)
        self.block_sizer.Add(self.block_button,1)
        self.block_sizer.Add(self.block_panel_btn,0)
        self.analysis_sizer.AddMany(((self.stat_button),(self.hist_button),
                                      (self.weibull_button),(self.corr_sizer),
                                      (self.corr_panel),
                                      (self.block_sizer),(self.block_panel),
                                      (self.psd_button)))
        button_size = (180,30)
        self.stat_button.SetMinSize(button_size)
        self.hist_button.SetMinSize(button_size)
        self.weibull_button.SetMinSize(button_size)
        ## corr panel layout
        self.corr_button.SetMinSize(button_size)
        self.corr_panel_btn.SetMinSize((40,30))
        self.corr_panel.Hide()
        self.rad_autocorr.Move((10,3))
        self.rad_crosscorr.Move((75,3))
        self.lag_label.Move((150,5))
        self.corr_lag_int.Move((210,0))
        self.corr_lag_int.SetSize((40,-1))
        self.notebook_1_pane_1.SetSizer(self.analysis_sizer)
        ## / corr panel layout
        ## block panel
        self.block_button.SetMinSize(button_size)
        self.block_panel_btn.SetMinSize((40,30))
#        self.block_new_freq.SetMinSize((50, -1))
        self.block_new_freq.Move((30,0))
#        self.block_new_freq.SetSize((60,-1))
        self.block_panel.Hide()
        ## / block panel
        self.psd_button.SetMinSize(button_size)
        # End Analysis layout
        
        # Synthesis Layout
        self.mean_lbl.Move((10,10))
        self.stdev_lbl.Move((60,10))
        self.npoints_lbl.Move((110,10))
        self.autocorr_lbl.Move((190, 10))
        self.mean_ctrl.SetSize((30,-1))
        self.stdev_ctrl.SetSize((30,-1))
        self.npoints_ctrl.SetSize((30,-1))
        self.autocorr_ctrl.SetSize((30,-1))
        self.arma_button.SetSize(button_size)
        self.mean_ctrl.Move((10,30))
        self.stdev_ctrl.Move((60,30))
        self.npoints_ctrl.Move((110,30))
        self.autocorr_ctrl.Move((190,30))
        self.arma_button.Move((10,60))
        # End Synthesis Layout
        
        # TS panel
        self.sizer_ts.Add(self.list_box_1, 1, wx.EXPAND, 0)
        self.sizer_ts.Add(self.sizer_control_ts, 0)
        self.sizer_control_ts.Add(self.ts_plot_button, 0)
        self.sizer_control_ts.Add(self.ts_remove_button, 0)
        self.ts_control_panel.SetSizer(self.sizer_ts)
        
        # Splitter layout
        self.splitter.SetMinimumPaneSize(50)
        self.splitter.SplitHorizontally(self.ts_control_panel, self.notebook_1, sashPosition=-300)
        
        # Top level sizers
        self.sizer_3.Add(self.plot_panel, 1, wx.EXPAND, 1)
        self.sizer_3.Add(self.results_panel, 1, wx.EXPAND, 0)
        self.sizer_1.Add(self.splitter, 1, wx.EXPAND)
        self.sizer_1.Add(self.sizer_3, 1, wx.EXPAND, 0)
        self.SetSizer(self.sizer_1)
        self.Layout()
    
    def __set_bindings(self):
        
        """Bind events to actions."""
        
        # Menu Operations
        self.Bind(wx.EVT_MENU, self.OnImport, self.import_file)
        self.Bind(wx.EVT_MENU, self.OnAboutBox, self.about)
        self.Bind(wx.EVT_MENU, self.OnHelpIndex, self.help_book)
        
        # End File Operations
        
        # TS Panel Bindings
        self.Bind(wx.EVT_BUTTON, self.OnPlotTSButton, self.ts_plot_button)
        self.Bind(wx.EVT_BUTTON, self.OnRemoveTSButton, self.ts_remove_button)
        
        # Analysis
        self.Bind(wx.EVT_BUTTON, self.OnStatButton, self.stat_button)
        self.Bind(wx.EVT_BUTTON, self.OnHistButton, self.hist_button)
        self.Bind(wx.EVT_BUTTON, self.OnWeibullButton, self.weibull_button)
        self.Bind(wx.EVT_BUTTON, self.OnCorrButton, self.corr_button)
        self.Bind(wx.EVT_BUTTON, self.OnBlockButton, self.block_button)
        self.Bind(wx.EVT_BUTTON, self.OnPSDButton, self.psd_button)
        self.Bind(wx.EVT_BUTTON, self.OnTogglePanelButton, self.corr_panel_btn)
        self.Bind(wx.EVT_BUTTON, self.OnTogglePanelButton, self.block_panel_btn)
        # End Analysis
        
        # Synthesis
        self.Bind(wx.EVT_BUTTON, self.OnARMAButton, self.arma_button)
        

    
    
    # Utility functions
    def valid_selections(self, allowed_number):
        """
        Checks number of selections in self.list_box_1
        Input: allowed_number (int) is number of allowed selections
        Output: MsgDialog if incorrect number, else passes returns True
        """
        index = self.list_box_1.GetSelections()
        message = "Please select exactly %s timeseries"
        if len(index) != allowed_number:
            dlg = wx.MessageDialog(self, message % (allowed_number), "Invalid Input", wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
            return False
        else:
            return True

    def renumber_active_timeseries(self):
        """Renumber timeseries in active_timeseries dictionary."""
        index = 0
        new_dict = {}
        for key, value in self.active_timeseries.iteritems():
            new_dict[index] = value
            index += 1
        self.active_timeseries = new_dict
    
    def sync_active_listbox(self):
        """Synchronize listbox to active_timeseries values."""
        self.list_box_1.Clear()
        string_list = []
        
        ## Add text to listbox
        for index, value in self.active_timeseries.iteritems():
            string_list.append(' '.join([str(index),str(value['name']),str(value['location']),str(value['timeseries'][0:3])]))
        self.list_box_1.Set(string_list)
    
    def refresh_timeseries(self):
        """Renumber and sync active ts to listbox."""
        self.renumber_active_timeseries()
        self.sync_active_listbox()
        
    def add_timeseries(self, timeseries_dict):
        """Add a timeseries dictionary (metadata + ts) to active_timeseries"""
        self.active_timeseries[len(self.active_timeseries)] = timeseries_dict
    
    def remove_timeseries(self, index):
        """Remove timeseries from active list"""
        self.active_timeseries.pop(index)
    
    def create_ts_dict(self, new_ts, old_ts_dict=False, prepend_str=''):
        """
        Place new timeseries inside meta_ts_dict, copy meta if applicable.
        Input: new timeseries
        Optional: old timeseries for meta_data, prepend string
        Output: new meta + ts dictionary
        """
        if old_ts_dict:
            new_ts_dict = old_ts_dict.copy()
            new_ts_dict['timeseries'] = new_ts
            new_ts_dict['name'] = prepend_str+old_ts_dict['name']
        else:
            new_ts_dict = {'elevation': 00, 'name': '', 
            'designation': 'primary', 'collector': 'synthetic','filters': {},
            'comments': 'Generated with Wind Energy Engineering Toolkit',
            'meters_above_ground': 0, 'site_name': 'None', 'coords': {},
            'location': 'none', 'time_step': 600, 'units': 'units',
            'timezone': 0, 'time_period': '','logger_sampling': 0,
            'type': 'synthetic', 'report_created': '2001-01-01'}
            new_ts_dict['timeseries'] = new_ts
            new_ts_dict['name'] = prepend_str+'synthetic'
        return new_ts_dict
    # End Utility functions
        
    
    # Handler functions
    ## Menu Operations
    def OnImport(self, event):
        """Import all timeseries from a *.dat file"""
        dlg = wx.FileDialog(self, "Choose a file", os.getcwd(), "", "Dat files|*.dat|Any files|*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            open_file = open(dlg.GetPath(), 'rb')
            meta_ts_dict = file_ops.parse_file(open_file)
            open_file.close()
            
            for meta_ts in meta_ts_dict.values():
                self.add_timeseries(meta_ts)
            
            
            self.refresh_timeseries()
            # Set statusbar text
            mypath = os.path.basename(dlg.GetPath())
            self.SetStatusText("You imported: %s" % mypath)
    
    def OnHelpIndex(self, event):
        return 0
    
    def OnAboutBox(self, event):
        description = """The Wind Energy Engineering Toolkit (aka Minicodes) is a set of functions designed to..."""
        licence = """Wind Energy Engineering Toolkit is free software; you can redistribute it and/or modify it under the terms of the 
        GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
        
        Wind Energy Engineering Toolkit is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
        without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
        
        See the GNU General Public License for more details. You should have received a copy of the 
        GNU General Public License along with Wind Energy Engineering Toolkit; 
        if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA"""


        info = wx.AboutDialogInfo()

        info.SetIcon(wx.Icon('/home/aleck/Code/minicodes/sandbox/wec.ico', wx.BITMAP_TYPE_ICO))
        info.SetName('Wind Energy Engineering Toolkit')
        info.SetVersion('0.1')
        info.SetDescription(description)
        info.SetCopyright('(C) 2009 Alec Koumjian')
        info.SetWebSite('http://www.umass.edu/windenergy/projects/software/mini-code-overview.html')
        info.SetLicence(licence)
        info.AddDeveloper('Alec Koumjian')
        info.AddDocWriter('Alec Koumjian')
        info.AddArtist('Alec Koumjian')
#        info.AddTranslator('jan bodnar')

        wx.AboutBox(info)
    ## End Menu Operations
    
    ## TS Panel Functions
    def OnPlotTSButton(self, event):
        """Plot a timeseries object using matplotlib."""
        index = self.list_box_1.GetSelections()
        
        fig = self.plot_panel.get_figure()
        fig.clear()
        axes = fig.gca()
        # Draw grids
        axes.grid(b=True)
        
        # Plot selected timeseries
        for selection in range(len(index)):
            axes.plot(self.active_timeseries[index[selection]]['timeseries'].dates.tolist(), self.active_timeseries[index[selection]]['timeseries'],  linestyle='-', marker='o', linewidth=1.0)
            axes.xaxis_date(tz=None)
            
        ## Draw plot
        self.plot_panel.draw()
        
    def OnRemoveTSButton(self, event):
        """Remove selected timeseries from the active list and listbox."""
        indexes = self.list_box_1.GetSelections()
        
        for index in indexes:
            self.remove_timeseries(index)
        self.refresh_timeseries()
    
    
    ## General events
    def OnTogglePanelButton(self, event):
        """Hide or show a panel when toggle button is pressed."""
        btn_panel_table = {'corr':self.corr_panel,'block':self.block_panel}
        name = event.GetEventObject().GetName()
        panel = btn_panel_table[name]
        if panel.IsShown():
            panel.Hide()
            event.GetEventObject().SetLabel('>>')
        else:
            event.GetEventObject().SetLabel('<<')
            panel.Show()
        
        panel.GetParent().Layout()
        
    ## Analysis Functions
    def OnStatButton(self, event):
        """Generate statistics and print to panel."""
        index = self.list_box_1.GetSelections()
        if self.valid_selections(1):
            # Fetch timeseries from dictionary
            ts = self.active_timeseries[index[0]]['timeseries']
            # Fetch ts name from dictionary
            name = self.active_timeseries[index[0]]['name']
            # Set statusbar message
            self.frame_1_statusbar.SetStatusText("Stats for "+str(name))
            # Collect stats of timeseries
            stats = analysis.get_statistics(ts.compressed())            
            # Create statictext string
            text = ""
            for field, value in stats.iteritems():
                text = ''.join(text+str(field)+": "+str(value)+"\n")
            self.results_panel_text.SetLabel(text)

    def OnHistButton(self, event):
        """Generate histogram and plot using matplotlib."""
        index = self.list_box_1.GetSelections()
        if self.valid_selections(1):
            # Fetch timeseries from dictionary
            ts = self.active_timeseries[index[0]]['timeseries']
            # Fetch ts name from dictionary
            name = self.active_timeseries[index[0]]['name']
            ## TODO, add bins field
            bins = 10
            
            # Set statusbar message
            self.frame_1_statusbar.SetStatusText("Histogram for "+str(name))
            
            fig = self.plot_panel.get_figure()
            # Clear old data
            fig.clear()
            axes = fig.gca()
            
            # Generate histogram data
            hist_values, bin_edges = analysis.get_histogram_data(ts.compressed(), bins)
            
            # Create bar graph from histogram data
            
            # Note: We do not use Matplotlib's axes.hist function
            # for the sake of consistency.  We always generate the data
            # Using Numpy's library and then generate a bar graph from it
            # Produces identical results to matplotlib.axes.hist
            histogram = axes.bar(bin_edges[:-1], hist_values, width=bin_edges[1]-bin_edges[0])
            
            axes.set_xlabel('Wind Speed')
            axes.set_ylabel('P(x)')
            axes.set_title('Histogram of %s' % (name))
            
            # Redraw graph
            self.plot_panel.draw()
            
    def OnWeibullButton(self, event):
        """Retrieve Weibull parameters from selected timeseries."""
        index = self.list_box_1.GetSelections()
        if self.valid_selections(1):
            # Fetch timeseries from dictionary
            ts = self.active_timeseries[index[0]]['timeseries']
            # Fetch ts name from dictionary
            name = self.active_timeseries[index[0]]['name']
            # Set statusbar message
            self.frame_1_statusbar.SetStatusText("Weibull Parameters for "+str(name))
            # Collect stats of timeseries
            stats = analysis.get_statistics(ts.compressed())  
            c, k = analysis.get_weibull_params(stats['mean'],stats['std'])
            # Create statictext string
            text = "C: "+str(c)+"\n"+"K: "+str(k)+"\n"
            self.results_panel_text.SetLabel(text)
    
    def OnCorrButton(self, event):
        """Generate and plot correlation values."""
        if self.rad_autocorr.GetValue():
            self.OnAutocorrButton(event)
        else:
            self.OnCrosscorrButton(event)
        
    def OnAutocorrButton(self, event):
        """Generate and plot autocorrelation values."""
        index = self.list_box_1.GetSelections()
        if self.valid_selections(1):
            # Fetch timeseries from dictionary
            ts = self.active_timeseries[index[0]]['timeseries']
            # Fetch ts name from dictionary
            name = self.active_timeseries[index[0]]['name']
            
            # Get lag value
            max_lag_increment = self.corr_lag_int.GetValue()
            
            # Set statusbar message
            self.frame_1_statusbar.SetStatusText("Autocorrelation values for "+str(name))
            
            # Collect stats of timeseries
            lag_values, autocorrelation_values = analysis.autocorrelate(ts.compressed(), max_lag_increment)
            # Get Figure
            fig = self.plot_panel.get_figure()
            # Clear old data
            fig.clear()
            axes = fig.gca()
            # Draw grids
            axes.grid(b=True)
            # Draw line at y=0
            axes.axhline(linewidth=2, color='r')
            # Draw autocorrelation values
            axes.plot(lag_values, autocorrelation_values, linestyle='-', marker='o', linewidth=1.0)
            # Set labels
            axes.set_xlabel('Lag')
            axes.set_ylabel('Autocorr')
            axes.set_title('Autocorrelation of %s' % (name))
            
            # Redraw graph
            self.plot_panel.draw()
            
    
    def OnCrosscorrButton(self, event):
        """Generate and plot crosscorrelation vaules."""
        index = self.list_box_1.GetSelections()
        if self.valid_selections(2):
            # Fetch ts1 from dictionary
            ts1 = self.active_timeseries[index[0]]['timeseries']
            # Fetch ts1 name from dictionary
            name1 = self.active_timeseries[index[0]]['name']
            
            # Fetch ts2 from dictionary
            ts2 = self.active_timeseries[index[1]]['timeseries']
            # Fetch ts2 name from dictionary
            name2 = self.active_timeseries[index[1]]['name']
            
            # Get lag value
            max_lag_increment = self.corr_lag_int.GetValue()
            
            # Set statusbar message
            self.frame_1_statusbar.SetStatusText("Crosscorrelation values for "+str(name1)+" and "+str(name2))
            # Collect stats of timeseries
            lag_values, crosscorrelation_values = analysis.crosscorrelate(ts1.compressed(),ts2.compressed(), max_lag_increment)
            # Get Figure
            fig = self.plot_panel.get_figure()
            # Clear old data
            fig.clear()
            axes = fig.gca()
            axes.grid(b=True)
            # Draw line at y=0
            axes.axhline(linewidth=2, color='r')
            # Plot correlation values
            axes.plot(lag_values, crosscorrelation_values, linestyle='-', marker='o', linewidth=1.0)
            axes.set_xlabel('Lag')
            axes.set_ylabel('Crosscorr')
            axes.set_title('Crosscorrelation of %s and %s' % (name1,name2))
            # Redraw graph
            self.plot_panel.draw()
    
    def OnBlockButton(self, event):
        """Create block average of selected timeseries and add to list_box_1"""
        index = self.list_box_1.GetSelections()
        if self.valid_selections(1):
            old_ts_dict = self.active_timeseries[index[0]]
            new_freq = str(self.block_new_freq.GetString(self.block_new_freq.GetSelection()))
            # Set statusbar message
            self.frame_1_statusbar.SetStatusText("Created block average of "+str(self.active_timeseries[index[0]]['name']+" with new frequency "+new_freq))
            # Create new timeseries
            new_timeseries = analysis.block_average(old_ts_dict['timeseries'].compressed(), new_freq)
            new_ts_dict = self.create_ts_dict(new_timeseries, old_ts_dict, new_freq+'_block_avg_of_')
            self.add_timeseries(new_ts_dict)
            
            # Set focus
            self.list_box_1.SetFocus()
            self.list_box_1.SetSelection(len(self.active_timeseries)-1)
    
    def OnPSDButton(self, event):
        """Generate power spectral density info and plot using matplotlib."""
        return 0
    ## End Analysis Functions
    
    ## Synthesis Functions
    def OnARMAButton(self, event):
        """
        Generate timeseries using autoregressive moving average method.
        Input: mean, stdev, npoints, autocorr (all from gui inputs)
        Output: Add generated timeseries to self.list_box_1
        """
        mean = float(self.mean_ctrl.GetValue())
        stdev = float(self.stdev_ctrl.GetValue())
        npoints = int(self.npoints_ctrl.GetValue())
        autocorr = float(self.autocorr_ctrl.GetValue())
        arma_ts = synthesis.gen_arma(mean, stdev, autocorr, npoints)
        new_ts_dict = self.create_ts_dict(arma_ts, prepend_str='arma_')
        self.add_timeseries(new_ts_dict)
    ## End Synthesis Functions
    # End Handler Functions

# end of class MyFrame


if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_1 = MyFrame(None, -1, "")
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()
