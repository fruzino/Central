#!/usr/bin/env python3
#            ___
#           /   \
# l i n u x [^-^]
#        o  ----- o
#           O   O

import npyscreen
import os
from pathlib import Path
import shutil
from datetime import datetime
import platform

ascii_central = r"""
      ___           ___           ___                         ___           ___                   
     /\__\         /\__\         /\  \                       /\  \         /\  \                  
    /:/  /        /:/ _/_        \:\  \         ___         /::\  \       /::\  \                 
   /:/  /        /:/ /\__\        \:\  \       /\__\       /:/\:\__\     /:/\:\  \                
  /:/  /  ___   /:/ /:/ _/_   _____\:\  \     /:/  /      /:/ /:/  /    /:/ /::\  \   ___     ___ 
 /:/__/  /\__\ /:/_/:/ /\__\ /::::::::\__\   /:/__/      /:/_/:/__/___ /:/_/:/\:\__\ /\  \   /\__\
 \:\  \ /:/  / \:\/:/ /:/  / \:\~~\~~\/__/  /::\  \      \:\/:::::/  / \:\/:/  \/__/ \:\  \ /:/  /
  \:\  /:/  /   \::/_/:/  /   \:\  \       /:/\:\  \      \::/~~/~~~~   \::/__/       \:\  /:/  / 
   \:\/:/  /     \:\/:/  /     \:\  \      \/__\:\  \      \:\~~\        \:\  \        \:\/:/  /  
    \::/  /       \::/  /       \:\__\          \:\__\      \:\__\        \:\__\        \::/  /   
     \/__/         \/__/         \/__/           \/__/       \/__/         \/__/         \/__/    
""".strip("\n")

a_projtypes = ["Work", "School", "Embedded", "App", "OS", "Systems", "GamesSource", "Templates", "Resources", "Repos", "Other"]
a_subprojtypes = ["Audio", "Video", "Animation", "Other"]

current_os = platform.system()

if current_os == "Linux":
    centraldir = Path(__file__).resolve().parent.parent / "Central"
    projdir = centraldir / "Projects"
    cachedir = centraldir / "Cache"
    centraldir_str = f"{centraldir}/"
elif current_os == "Windows":
    centraldir = Path.cwd().parent.parent / "Central"
    projdir = centraldir / "Projects"
    cachedir = centraldir / "Cache"
    centraldir_str = f"{centraldir}/"
else:
    centraldir = Path.cwd().parent.parent / "Central"
    projdir = centraldir / "Projects"
    cachedir = centraldir / "Cache"
    centraldir_str = f"{centraldir}/"
    
def initapp():
    centraldir.mkdir(parents=True, exist_ok=True)
    projdir.mkdir(parents=True, exist_ok=True)
    cachedir.mkdir(parents=True, exist_ok=True)

    print("Initialized dirs!")

def rebuild(torebuild):
    torebuild.addForm("SETTINGS", IProj, name="Central")
    torebuild.addForm("MAIN", Home, name="Central")
    torebuild.addForm("PROJ", Proj, name="Central")
    torebuild.addForm("IPROJ", IProj, name="Central")

class Logger:
    def log(contenttolog = "Unknown or not defined log message."):
        with open("logs/log.txt", "a") as f:
            if not f.writable:
                print("Aw man... log.txt isn't writable!")

            f.write(f"\n[  LOG  ] {datetime.date()} | {datetime.now()} ->\n     {contenttolog}\n[  ENDLOG  ]\n")

class Settings(npyscreen.Form):
    def create(self):
        pass

class Home(npyscreen.Form):
    def create(self):
        self.add(npyscreen.Pager, values=ascii_central.splitlines(),
                 editable=False, max_height=13)
        self.nextrely += 1
        self.title = self.add(npyscreen.FixedText, value="Welcome to central!")
        self.title.display()
        self.nextrely += 2
        self.createproj = self.add(npyscreen.ButtonPress, name="Create Project", when_pressed_function=lambda: self.go("PROJ"))

        self.settings = self.add(npyscreen.ButtonPress, name="⚙ Settings", when_pressed_function=lambda: self.go("SETTINGS"))
    
    def go(self, To):
        self.parentApp.setNextForm(To)
        self.parentApp.switchFormNow()

class Proj(npyscreen.Form):
    def create(self):
        self.add(npyscreen.ButtonPress, name="< Back", when_pressed_function=lambda: self.go("MAIN"))
        self.projname = self.add(
            npyscreen.TitleText, name="Choose a name for your project:")
        self.projtype_ = self.add(npyscreen.FixedText, value="Choose a type:")
        self.projtype_.display()
        self.projtype = self.add(
            npyscreen.SelectOne, values=a_projtypes, max_height=6)

        self.projsubtype = self.add(npyscreen.SelectOne, values=a_subprojtypes, hidden=True, max_height=4)
        self.projtype.when_value_edited = self.update_subtype_visibility

        self.createbut = self.add(npyscreen.ButtonPress, name="Create Project", when_pressed_function=lambda: self.createproj())
        self.importproj = self.add(npyscreen.ButtonPress, name="Import Project", when_pressed_function=lambda: self.go("IPROJ"))

    def update_subtype_visibility(self):
        if not self.projtype.value:
            return

        selected_index = self.projtype.value[0]
        selected_text = a_projtypes[selected_index]

        if selected_text == "Work":
            self.projsubtype.hidden = False
        else:
            self.projsubtype.hidden = True

        self.display()

    def createproj(self):
        proj_type = self.projtype.get_selected_objects()[0]
        proj_name = self.projname.value
        
        proj_sub = self.projsubtype.get_selected_objects()[0] if not self.projsubtype.hidden else ""

        tomake = Path("/home/akshay/Central/Projects") / proj_type / proj_sub / proj_name

        tomake.mkdir(parents=True, exist_ok=True)
        
        self.editing = False
        npyscreen.notify_confirm(f"Created: {tomake}", title="Success")

    def go(self, To):
        self.parentApp.setNextForm(To)
        self.parentApp.switchFormNow()

class IProj(npyscreen.Form):
    def create(self):
        self.add(npyscreen.ButtonPress, name="< Back", when_pressed_function=lambda: self.go("PROJ"))
        self.projdir = self.add(
            npyscreen.TitleText, name="Enter directory of project:")
        self.todir = self.add(
            npyscreen.TitleText, name="Enter new move directory (inside the Projects folder!):")
        self.importbut = self.add(npyscreen.ButtonPress, name="Import Project", when_pressed_function=lambda: self.importproj())
        
    def importproj(self):
        try:
            shutil.move(self.projdir.value, centraldir_str+"Projects/"+self.todir.value)
            npyscreen.notify_confirm(f"Imported project to: {centraldir_str+"Projects/"+self.todir.value}", title="Success")
        except Exception as e:
            npyscreen.notify_confirm(f"Error importing \"{self.projdir.value}\" to \"{centraldir_str+"Projects/"+self.todir.value}\" Please check logs!", title="Failed")
            Logger.log(f"Unexpected error, {e}")

    def go(self, To):
        self.parentApp.setNextForm(To)
        self.parentApp.switchFormNow()

class Central(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm("SETTINGS", IProj, name="Central")
        self.addForm("MAIN", Home, name="Central")
        self.addForm("PROJ", Proj, name="Central")
        self.addForm("IPROJ", IProj, name="Central")

if __name__ == "__main__":
    initapp()

    app = Central()
    app.run()
    