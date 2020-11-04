#import Helpers

from tkinter import filedialog as fd
import tkinter as tk
import os
import json

import config

#-------------------------------------------------
# Top-level GUI
#-------------------------------------------------

class UI(tk.LabelFrame):
    '''
    Frame for basic data management commands
    Appears regardless of selected tab
    '''
    def load_from_workspace(self, workspace):
        '''
        Loads data used in workspace file for general parameters
        '''
        config.shot_run_dir = workspace
        
    def get_workspace(self):
        '''
        Returns all values needed to recreate the general parameters later
        Returns string shotrundir
        '''
        return config.shot_run_dir
    
    def __init__(self, master, workspace_load=None, workspace_save=None,
                 **options):
        tk.LabelFrame.__init__(self, master, text="General Parameters",
                               font=14, **options)
        '''
        workspace_load: list of functions to update a tab based on a json file.
        Should have parameters (self, workspace), where workspace is a
        json-friendly data type packaged by the tab's own workspace_save()
        workspace_save: list of functions to save a tab's settings into a
        json file. Should have parameters (self).
        '''

        # Workspace function handling
        def null(workspace):
            ''' Default blank function in case no functions are passed '''
            return
        if (workspace_load == None):
            self.workspace_load = [null]
        else:
            self.workspace_load = workspace_load
        if (workspace_save == None):
            self.workspace_save = [null]
        else:
            self.workspace_save = workspace_save

        self.workspace_load.append(self.load_from_workspace)
        self.workspace_save.append(self.get_workspace) 
        
        # Shot Run Directory
        if (os.path.exists("PermPathFile")):
            file = open("PermPathFile", "r")
            self.path_perm = file.read()
        else:
            self.path_perm = "./"

        def set_path_perm(self):
            '''
            Sets the directory for the permanent (destination) files
            '''
            self.path_perm = fd.askdirectory(initialdir="..",
                                        title="Set Permanent Storage Directory")
            perm_dir_file = open("PermDirFile", "w")
            perm_dir_file.write(self.path_perm)
            config.shot_run_dir = self.path_perm
        
        self.btn_path_perm = tk.Button(self, text="Select Shot Run Directory",
                                      command=lambda: set_path_perm(self))
        self.btn_path_perm.pack(pady=5)

        # Shot counters

        # Buttons
        def save_workspace(self):
            '''
            Creates list 'workspace' to store data needed to load current
            option selections. Each element in workspace is whatever data
            each tab requires. Must all be json-friendly
            Stores workspace in json file
            '''
            path_save =  fd.asksaveasfilename(initialdir="./",
                                              title="Save Workspace",
                                              defaultextension='.json',
                                              filetypes=(("json files","*.json"),))
            workspace = []
            for funct in self.workspace_save:
                workspace.append(funct())
            with open(path_save,"w") as write_file:
                json.dump(workspace,write_file)
        self.btn_save_wksp = tk.Button(self, text="Save Workspace",
                                            command=lambda:save_workspace(self))
        self.btn_save_wksp.pack(pady=2)

        def load_workspace(self):
            '''
            Pulls data from json file
            Calls load function for each tab
            '''
            path_load = fd.askopenfilename(initialdir = "./",
                                      title = "Select Workspace",
                                      filetypes = (("json files","*.json"),))
            if (path_load == ""):
                return
            with open(path_load,"r") as read_file:
                workspace = json.load(read_file)
            for wksp,funct in zip(workspace, self.workspace_load):
                funct(wksp)
        self.btn_load_wksp = tk.Button(self, text="Load Workspace",
                                            command=lambda:load_workspace(self))
        self.btn_load_wksp.pack(pady=2)
        
        # Options


def test():
    root = tk.Tk()
    gp = UI(root)
    gp.pack()
    root.mainloop()
