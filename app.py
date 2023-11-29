import tkinter
from tkinter import ttk
from tkinter import filedialog
import customtkinter
import re
import random
from zipfile import ZipFile
import threading
import math

import shutil
import os

from PIL import ImageTk, Image 

from settings import *
from utils import *
from vfx_class import *

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

class App():
    def __init__(self):
        # Init root
        self.root = customtkinter.CTk()
        self.root.title("LoL Mod Tools")
        self.root.iconbitmap("Image/icon.ico")
        self.root.geometry("{0}x{1}+0+0".format(int(self.root.winfo_screenwidth()), int(self.root.winfo_screenheight()*0.95)))
        
        
        # Custom Tkinter For TreeView
        self.bg_color = self.root._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkFrame"]["fg_color"])
        self.text_color = self.root._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkLabel"]["text_color"])
        self.selected_color = self.root._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkButton"]["fg_color"])
        
        
        # Tkinter Style For Treeview
        self.treestyle = ttk.Style()
        self.treestyle.theme_use('default')
        self.treestyle.configure("Treeview", background=self.bg_color, foreground=self.text_color, fieldbackground=self.bg_color, borderwidth=0)
        self.treestyle.configure('Treeview', rowheight=25)
        self.treestyle.configure('Treeview.image', rowheight=50)
        self.treestyle.map('Treeview', background=[('selected', self.bg_color)], foreground=[('selected', self.selected_color)])
        
        
        # ICON
        self.folder_icon = ImageTk.PhotoImage(Image.open("Image/folder_icon.png"))
        self.file_icon = ImageTk.PhotoImage(Image.open("Image/file_icon.png"))
        self.code_icon = ImageTk.PhotoImage(Image.open("Image/code_icon.png"))
        self.py_icon = ImageTk.PhotoImage(Image.open("Image/py_icon.png"))
        self.image_icon = ImageTk.PhotoImage(Image.open("Image/image_icon.png"))
        self.skl_icon = ImageTk.PhotoImage(Image.open("Image/skl_icon.png"))
        self.object_icon = ImageTk.PhotoImage(Image.open("Image/object_icon.png"))
        self.anm_icon = ImageTk.PhotoImage(Image.open("Image/anm_icon.png"))
        self.audio_icon = ImageTk.PhotoImage(Image.open("Image/audio_icon.png"))
        self.transparent_icon = ImageTk.PhotoImage(Image.open("Image/transparent_icon.png"))
        
        
        # VARIABLES
        self.copy_files = []
        self.copy_folders = []

        self.LCS_location = get_lol_path()
        
        self.list_top_left_bt = []
        self.list_top_right_bt = []
        
        self.list_analyze_images = []
        self.list_analyze_images2 = []
        
        self.list_errors = []
        
        self.selected_folders = []
        self.selected_files = []
        self.memory_open1 = []
        self.memory_open2 = []
        self.copy_ranges = []
        
        self.on_bin_analyze = False
        self.last_textbox_content = None
        
        self.types_dict_all = ['.troybin', '.bin', '.py', '.tex', '.skl', '.troy', '.dds', '.scb', '.sco', '.skn', '.anm',
                          '.bnk', '.tga', '.wpk', '.wgeo', '.stringtable', '.preload', '.mapgeo', '.png', '.jpg', '.client',
                          '.json', '.dat', '.luaobj', '.inibin', '.ini','.lua']
        self.code_extensions = ['.bin', '.troybin', '.inibin', '.luaobj']
        self.py_extensions = ['.py']
        self.image_extensions = ['.dds', '.tex', '.jpg', '.jpeg', '.png', '.ico', '.DDS']
        self.skl_extensions = ['.skl']
        self.object_extensions = ['.skn', '.scb', '.sco', '.tga', '.wgeo', '.mapgeo', '.glb', '.gltf']
        self.anm_extensions = ['.anm']
        self.audio_extensions = ['.bnk', '.mp3', '.wav', '.webm', '.wem', 'wpk']


        # LEFT
        
        # RIGHT
        self.right_side_panel = customtkinter.CTkFrame(self.root, fg_color="transparent", corner_radius=0)
        self.right_side_panel.pack(side=tkinter.RIGHT, fill=tkinter.BOTH, expand=True)
        
        self.top_left_side_panel = customtkinter.CTkFrame(self.right_side_panel, height=40)
        self.top_left_side_panel.pack_propagate(False)
        self.top_left_side_panel.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=False, padx=5, pady=10)
        
        self.top_right_side_panel = customtkinter.CTkFrame(self.right_side_panel, height=40)
        self.top_right_side_panel.pack_propagate(False)
        
        
        # FILE FOLDER BUTTONS
        self.bt_open_file = customtkinter.CTkButton(self.top_left_side_panel, text="open file", command=lambda: self.import_file(), width=0, fg_color="green")
        self.bt_open_file.pack(side=tkinter.LEFT, padx=(5,0), pady=0)
        
        self.bt_open_folder = customtkinter.CTkButton(self.top_left_side_panel, text="open folder", command=lambda: self.import_folder(), width=0, fg_color="green")
        self.bt_open_folder.pack(side=tkinter.LEFT, padx=(5,0), pady=0)
        
        self.bt_change_LCS_path = customtkinter.CTkButton(self.top_left_side_panel, text="change LCS path", command=lambda: self.change_LCS_location(), width=0, fg_color="green")
        self.bt_change_LCS_path.pack(side=tkinter.LEFT, padx=(5,0), pady=0)
        
        self.bt_finish = customtkinter.CTkButton(self.top_left_side_panel, text="export", command=lambda: self.finish(), width=0, fg_color="green")
        self.bt_finish.pack(side=tkinter.LEFT, padx=(5,0), pady=0)
        
        self.bt_add_to_LCS = customtkinter.CTkButton(self.top_left_side_panel, text="add to LCS", command=lambda: self.add_to_LCS(), width=0, fg_color="green")
        self.bt_add_to_LCS.pack(side=tkinter.LEFT, padx=(5,15), pady=0)
        
        self.bt_extract_client = customtkinter.CTkButton(self.top_left_side_panel, text="extract .client", command=self.extract_client, width=29, fg_color="#c25400")
        self.list_top_left_bt.append(self.bt_extract_client)
        
        self.bt_wad_make = customtkinter.CTkButton(self.top_left_side_panel, text="wad make", command=self.wad_make, width=0, fg_color="#c25400")
        self.list_top_left_bt.append(self.bt_wad_make)
        
        self.bt_convert_obj = customtkinter.CTkButton(self.top_left_side_panel, text=".scb/.sco → .gtlf", command=self.convert_obj, width=0)
        self.list_top_left_bt.append(self.bt_convert_obj)
        
        self.bt_convert_troy = customtkinter.CTkButton(self.top_left_side_panel, text=".troybin → .troy", command=self.convert_troybin, width=29)
        self.list_top_left_bt.append(self.bt_convert_troy)
        
        self.bt_convert_bin = customtkinter.CTkButton(self.top_left_side_panel, text=".bin → .py", command=self.convert_bin, width=0)
        self.list_top_left_bt.append(self.bt_convert_bin)
        
        self.bt_convert_py = customtkinter.CTkButton(self.top_left_side_panel, text=".py → .bin", command=self.convert_py, width=0)
        self.list_top_left_bt.append(self.bt_convert_py)
        
        self.bt_convert_tex = customtkinter.CTkButton(self.top_left_side_panel, text=".tex → .dds", command=self.convert_tex, width=0)
        self.list_top_left_bt.append(self.bt_convert_tex)
        
        self.bt_convert_dds = customtkinter.CTkButton(self.top_left_side_panel, text=".dds → .tex", command=self.convert_tex, width=0)
        self.list_top_left_bt.append(self.bt_convert_dds)

        self.bt_convert_inibin = customtkinter.CTkButton(self.top_left_side_panel, text=".inibin → .ini", command=self.convert_inibin, width=0)
        self.list_top_left_bt.append(self.bt_convert_inibin)

        self.bt_convert_luaobj = customtkinter.CTkButton(self.top_left_side_panel, text=".luaobj → .lua", command=self.convert_luaobj, width=0)
        self.list_top_left_bt.append(self.bt_convert_luaobj)
        
        self.bt_update_skl = customtkinter.CTkButton(self.top_left_side_panel, text="update .skl", command=self.update_skl, width=0)
        self.list_top_left_bt.append(self.bt_update_skl)
        
        self.bt_change_color = customtkinter.CTkButton(self.top_left_side_panel, text="change color", command=lambda: self.dds_RGBA_picker_frame.place(relx=0.3, rely=0), width=0)
        self.list_top_left_bt.append(self.bt_change_color)
        
        self.bt_troy_to_bin = customtkinter.CTkButton(self.top_left_side_panel, text="write troy to bin", command=lambda: self.troy_to_bin_one(self.selected_files[0]), width=0)
        self.list_top_left_bt.append(self.bt_troy_to_bin)
        
        self.bt_bin_analyze = customtkinter.CTkButton(self.top_left_side_panel, text="bin analyze", command=lambda: self.bin_analyze(self.selected_files[0], self.treeview3, True), width=0, fg_color="green")
        self.list_top_left_bt.append(self.bt_bin_analyze)
        
        self.bt_bin_analyze2 = customtkinter.CTkButton(self.top_left_side_panel, text="bin analyze 2", command=lambda: self.bin_analyze(self.selected_files[0], self.treeview4, True), width=0, fg_color="green")
        self.list_top_left_bt.append(self.bt_bin_analyze2)
        
        self.bt_edit = customtkinter.CTkButton(self.top_left_side_panel, text="edit", command=lambda: self.show_file(self.selected_files[0]), width=0)
        self.list_top_left_bt.append(self.bt_edit)
        
        self.bt_save = customtkinter.CTkButton(self.top_left_side_panel, text="save", command=lambda: self.save(self.selected_files[0]), width=0, fg_color="green")
        self.list_top_left_bt.append(self.bt_save)

        self.bt_bulk_rename = customtkinter.CTkButton(self.top_left_side_panel, text="bulk rename", command=lambda: self.bulk_rename(), width=0, fg_color="green")
        self.list_top_left_bt.append(self.bt_bulk_rename)
        
        self.bt_switch_channel = customtkinter.CTkSwitch(self.top_left_side_panel, text="RGBA", command=lambda: self.switch_channel(), width=0)
        self.bt_switch_channel.pack(side=tkinter.LEFT, padx=(5,20), pady=0)
        self.bt_switch_channel.select()
        
        self.bt_switch_preview = customtkinter.CTkSwitch(self.top_left_side_panel, text="Preview", command=lambda: self.switch_preview(), width=0)
        self.bt_switch_preview.deselect()
        
        self.bt_switch_preview2 = customtkinter.CTkSwitch(self.top_left_side_panel, text="Preview", command=lambda: self.switch_preview(), width=0)
        self.bt_switch_preview2.deselect()
        
        
        # BIN ANALYZE BUTTONS
        #self.bt_update_bin = customtkinter.CTkButton(self.top_right_side_panel, text="update link", command=self.update_bin, width=0)
        #self.list_top_right_bt.append(self.bt_update_bin)
        
        self.bt_bin_change_constant_color = customtkinter.CTkButton(self.top_right_side_panel, text="change constant color", command=lambda: self.initiate_RGBA(self.constant_color_sample), width=0)
        self.list_top_right_bt.append(self.bt_bin_change_constant_color)
        
        self.bt_bin_change_birth_color = customtkinter.CTkButton(self.top_right_side_panel, text="change birth color", command=lambda: self.initiate_RGBA(self.birth_color_sample), width=0)
        self.list_top_right_bt.append(self.bt_bin_change_birth_color)
        
        self.bt_bin_change_dynamic_color = customtkinter.CTkButton(self.top_right_side_panel, text="change dynamic color", command=lambda: self.initiate_TRGBA(), width=0)
        self.list_top_right_bt.append(self.bt_bin_change_dynamic_color)
        
        self.bt_bin_disable_emitter = customtkinter.CTkButton(self.top_right_side_panel, text="disable emitter", command=lambda: self.disable_emitter(), width=0)
        self.list_top_right_bt.append(self.bt_bin_disable_emitter)
        
        self.bt_bin_enable_emitter = customtkinter.CTkButton(self.top_right_side_panel, text="enable emitter", command=lambda: self.enable_emitter(), width=0)
        self.list_top_right_bt.append(self.bt_bin_enable_emitter)
        
        self.bt_bin_scan = customtkinter.CTkButton(self.top_right_side_panel, text="scan", command=lambda: self.scan(), width=0, fg_color="green")
        self.list_top_right_bt.append(self.bt_bin_scan)
        
        self.bt_bin_change_path = customtkinter.CTkButton(self.top_right_side_panel, text="change path", command=lambda: self.change_path_bin(), width=0)
        self.list_top_right_bt.append(self.bt_bin_change_path)
        
        self.bt_bin_accept_change_path = customtkinter.CTkButton(self.top_right_side_panel, text="save", command=lambda: self.accept_change_path_bin(), width=0, fg_color="green")
        self.list_top_right_bt.append(self.bt_bin_accept_change_path)
        
        
        # FRAMES
        self.Frame1 = customtkinter.CTkFrame(self.right_side_panel)
        self.Frame1.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True, padx=5, pady=(0,10))
        
        self.top_right_side_panel.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=False, padx=5, pady=10)
        
        self.Frame2 = customtkinter.CTkFrame(self.right_side_panel)
        self.Frame2.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True, padx=5, pady=(0,10))
        
        self.root.bind("<F1>", lambda event : self.repack_forget(1) if self.Frame1.winfo_ismapped() else self.repack())
        self.root.bind("<F2>", lambda event : self.repack_forget(2) if self.Frame2.winfo_ismapped() else self.repack())
    
        # TREEVIEW
        self.list_treeview_images = []
        self.list_treeview_images2 = []
        
        self.treeview = ttk.Treeview(self.Frame1, show="tree")
        self.ysb1 = customtkinter.CTkScrollbar(self.Frame1, orientation='vertical', command=self.treeview.yview, bg_color="transparent")
        self.treeview.configure(yscroll=self.ysb1.set)
        self.treeview.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True, padx=10, pady=10)
        self.ysb1.pack(side=tkinter.LEFT, fill=tkinter.Y)
        
        self.treeview2 = ttk.Treeview(self.Frame1, show="tree")
        self.ysb2 = customtkinter.CTkScrollbar(self.Frame1, orientation='vertical', command=self.treeview2.yview, bg_color="transparent")
        self.treeview2.configure(yscroll=self.ysb2.set)
        self.treeview2.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True, padx=10, pady=10)
        self.ysb2.pack(side=tkinter.LEFT, fill=tkinter.Y)
        
        self.treeview3 = ttk.Treeview(self.Frame2, show="tree", style="Custom3.Treeview")
        self.ysb33 = customtkinter.CTkScrollbar(self.Frame2, orientation='vertical', command=self.treeview3.yview, bg_color="transparent")
        self.treeview3.configure(yscroll=self.ysb33.set)
        self.treeview3.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True, padx=10, pady=10)
        self.ysb33.pack(side=tkinter.LEFT, fill=tkinter.Y)
        
        self.treeview4 = ttk.Treeview(self.Frame2, show="tree", style="Custom3.Treeview")
        self.ysb44 = customtkinter.CTkScrollbar(self.Frame2, orientation='vertical', command=self.treeview4.yview, bg_color="transparent")
        self.treeview4.configure(yscroll=self.ysb44.set)
        self.treeview4.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True, padx=10, pady=10)
        self.ysb44.pack(side=tkinter.LEFT, fill=tkinter.Y)
        
        self.current_treeview34 = self.treeview3
        self.treeview3_filepath = ""
        self.treeview4_filepath = ""
        self.treeview3_lines_py = []
        self.treeview4_lines_py = []
        self.current_lines_py = []
        
        self.memory_open3 = []
        self.memory_open4 = []
        self.current_bin_analyze = ""
        
        self.treeview.bind("<Control-c>", lambda event: self.copy())
        self.treeview.bind("<Control-v>", lambda event: self.paste())
        self.treeview.bind("<Control-b>", lambda event: self.paste2())
        self.treeview.bind("<Delete>", lambda event: self.delete())
        
        self.treeview2.bind("<Control-c>", lambda event: self.copy())
        self.treeview2.bind("<Control-v>", lambda event: self.paste())
        self.treeview2.bind("<Control-b>", lambda event: self.paste2())
        self.treeview2.bind("<Delete>", lambda event: self.delete())
        
        self.treeview.bind("<Button-3>", lambda event: self.rename())
        self.treeview2.bind("<Button-3>", lambda event: self.rename())
        
        self.treeview3.bind("<Control-c>", lambda event: self.copy_bin())
        self.treeview3.bind("<Control-v>", lambda event: self.paste_bin())
        self.treeview3.bind("<Delete>", lambda event: self.delete_line_bin())
        self.treeview3.bind("<Button-3>", lambda event: self.edit_bin())
        
        self.treeview4.bind("<Control-c>", lambda event: self.copy_bin())
        self.treeview4.bind("<Control-v>", lambda event: self.paste_bin())
        self.treeview4.bind("<Delete>", lambda event: self.delete_line_bin())
        self.treeview4.bind("<Button-3>", lambda event: self.edit_bin())
        
        self.treeview.bind("<<TreeviewSelect>>", lambda event: self.on_click(self.treeview))
        self.treeview2.bind("<<TreeviewSelect>>", lambda event: self.on_click(self.treeview2))
        self.treeview3.bind("<<TreeviewSelect>>", lambda event: self.on_click34(self.treeview3))
        self.treeview4.bind("<<TreeviewSelect>>", lambda event: self.on_click34(self.treeview4))
        
        self.treeview.bind("<p>", lambda event: self.open_all(self.treeview))
        self.treeview2.bind("<p>", lambda event: self.open_all(self.treeview2))
        self.treeview3.bind("<p>", lambda event: self.open_all(self.treeview3))
        self.treeview4.bind("<p>", lambda event: self.open_all(self.treeview4))

        self.treeview3.tag_configure('blue', foreground="#3399cc")
        self.treeview3.tag_configure('green', foreground="#33cc99")
        self.treeview3.tag_configure('orange', foreground="#ce834a")
        self.treeview3.tag_configure('number', foreground="#99cc99")
        self.treeview3.tag_configure('yellow', foreground="#ffd70e")
        self.treeview3.tag_configure('blue vs', foreground="#8cdcfe")
        self.treeview3.tag_configure('red', foreground="red")
        self.treeview3.tag_configure('white', foreground="white")
        self.treeview3.tag_configure('found', background='brown')
        self.treeview3.tag_configure('found_focus', background='#2b4b4b')
        
        self.treeview4.tag_configure('blue', foreground="#3399cc")
        self.treeview4.tag_configure('green', foreground="#33cc99")
        self.treeview4.tag_configure('orange', foreground="#ce834a")
        self.treeview4.tag_configure('number', foreground="#99cc99")
        self.treeview4.tag_configure('yellow', foreground="#ffd70e")
        self.treeview4.tag_configure('blue vs', foreground="#8cdcfe")
        self.treeview4.tag_configure('red', foreground="red")
        self.treeview4.tag_configure('white', foreground="white")
        self.treeview4.tag_configure('found', background='brown')
        self.treeview4.tag_configure('found_focus', background='#2b4b4b')
        
        self.open = False
        self.open2 = False
        self.open3 = False
        self.open4 = False
        
        # TEXTBOX
        self.textbox = tkinter.Text(self.Frame1, background="#2b2b2b", wrap="none", undo=True, bd=0, tabs=32)
        self.ysb3 = customtkinter.CTkScrollbar(self.Frame1, orientation='vertical', command=self.textbox.yview, bg_color="transparent")
        self.textbox.configure(yscroll=self.ysb3.set)
        self.xsb3 = customtkinter.CTkScrollbar(self.textbox, orientation='horizontal', command=self.textbox.xview, bg_color="transparent")
        self.textbox.configure(xscroll=self.xsb3.set)
        self.textbox.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True, padx=10, pady=10)
        self.xsb3.pack(side=tkinter.BOTTOM, fill=tkinter.X)
        self.ysb3.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        
        self.textbox.bind('<KeyRelease>', lambda event: self.text_edited())
        
        self.textbox.tag_configure('blue', foreground="#3399cc")
        self.textbox.tag_configure('green', foreground="#33cc99")
        self.textbox.tag_configure('orange', foreground="#ce834a")
        self.textbox.tag_configure('number', foreground="#99cc99")
        self.textbox.tag_configure('yellow', foreground="#ffd70e")
        self.textbox.tag_configure('blue vs', foreground="#8cdcfe")
        self.textbox.tag_configure('red', foreground="red")
        self.textbox.tag_configure('white', foreground="white")
        self.textbox.tag_configure('found', background='brown')
        self.textbox.tag_configure('found_focus', background='#2b4b4b')
        

        self.textbox2 = tkinter.Text(self.Frame2, background="#2b2b2b", wrap="none", undo=True, bd=0, tabs=32)
        self.ysb32 = customtkinter.CTkScrollbar(self.Frame2, orientation='vertical', command=self.textbox2.yview, bg_color="transparent")
        self.textbox2.configure(yscroll=self.ysb32.set)
        self.xsb32 = customtkinter.CTkScrollbar(self.textbox2, orientation='horizontal', command=self.textbox2.xview, bg_color="transparent")
        self.textbox2.configure(xscroll=self.xsb32.set)
        
        self.textbox2.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True, padx=10, pady=10)
        self.xsb32.pack(side=tkinter.BOTTOM, fill=tkinter.X)
        self.ysb32.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        
        self.textbox2.bind('<KeyRelease>', lambda event: self.text_edited())
        
        self.textbox2.tag_configure('blue', foreground="#3399cc")
        self.textbox2.tag_configure('green', foreground="#33cc99")
        self.textbox2.tag_configure('orange', foreground="#ce834a")
        self.textbox2.tag_configure('number', foreground="#99cc99")
        self.textbox2.tag_configure('yellow', foreground="#ffd70e")
        self.textbox2.tag_configure('blue vs', foreground="#8cdcfe")
        self.textbox2.tag_configure('red', foreground="red")
        self.textbox2.tag_configure('white', foreground="white")
        self.textbox2.tag_configure('found', background='brown')
        self.textbox2.tag_configure('found_focus', background='#2b4b4b')
        
        
        # FILTER
        self.current_find_index = 0
        self.list_find = []
        
        self.Frame_search_text = customtkinter.CTkFrame(self.Frame1)
        
        self.up_button_search = customtkinter.CTkButton(self.Frame_search_text, text = "↑", width=0, command=self.up_search)
        self.up_button_search.pack(side=tkinter.LEFT)
        
        self.down_button_search = customtkinter.CTkButton(self.Frame_search_text, text = "↓", width=0, command=self.down_search)
        self.down_button_search.pack(side=tkinter.LEFT)
        
        self.label_search = customtkinter.CTkButton(self.Frame_search_text, text = str(self.current_find_index + 1) + "/" + str(len(self.list_find)), width=0)
        self.label_search.pack(side=tkinter.LEFT)
        
        self.search_text_entry = customtkinter.CTkEntry(self.Frame_search_text)
        self.search_text_entry.pack(side=tkinter.LEFT)
        self.search_text_entry.bind('<KeyRelease>', lambda event: self.find_text())
        self.search_text_entry.bind('<Escape>', lambda event: self.forget([self.search_text_entry]))
        self.textbox.bind('<Control-f>', lambda event: self.search_text())
        
        # RENAME FILE
        self.rename_entry = customtkinter.CTkEntry(self.Frame1)
        self.rename_entry.bind('<Return>', lambda event: self.accept_rename())
        
        # EDIT BIN
        self.rename_entry_bin = customtkinter.CTkEntry(self.Frame2)
        self.rename_entry_bin.bind('<Return>', lambda event: self.accept_edit_bin())
        
        self.root.bind('<Escape>', lambda event: self.forget([self.Frame_search_text, self.rename_entry, self.rename_entry_bin]))

        
        self.channel = "RGBA"
        
        # DDS RGBA
        self.dds_RGBA_picker_frame = customtkinter.CTkFrame(self.Frame1)
        
        self.dds_varR = customtkinter.DoubleVar()
        self.dds_varG = customtkinter.DoubleVar()
        self.dds_varB = customtkinter.DoubleVar()
        self.dds_varA = customtkinter.DoubleVar()
    
        self.dds_sliderR = customtkinter.CTkSlider(self.dds_RGBA_picker_frame, progress_color="red", button_color="gray", button_hover_color="white", height=20, button_corner_radius=3, button_length=5, variable=self.dds_varR, command=lambda event:self.dds_update_labelRGBA())
        self.dds_sliderG = customtkinter.CTkSlider(self.dds_RGBA_picker_frame, progress_color="green", button_color="gray", button_hover_color="white", height=20, button_corner_radius=3, button_length=5, variable=self.dds_varG, command=lambda event:self.dds_update_labelRGBA())
        self.dds_sliderB = customtkinter.CTkSlider(self.dds_RGBA_picker_frame, progress_color="blue", button_color="gray", button_hover_color="white", height=20, button_corner_radius=3, button_length=5, variable=self.dds_varB, command=lambda event:self.dds_update_labelRGBA())
        self.dds_sliderA = customtkinter.CTkSlider(self.dds_RGBA_picker_frame, progress_color="white", button_color="gray", button_hover_color="white", height=20, button_corner_radius=3, button_length=5, variable=self.dds_varA, command=lambda event:self.dds_update_labelRGBA())
        
        self.dds_sliderR.set(0.5)
        self.dds_sliderG.set(0.5)
        self.dds_sliderB.set(0.5)
        self.dds_sliderA.set(1)
        
        self.dds_RGBAimage = PIL.Image.new('RGBA', (120, 120), (int(self.dds_sliderR.get()*255), int(self.dds_sliderG.get()*255), int(self.dds_sliderB.get()*255), int(self.dds_sliderA.get()*255)))
        self.dds_RGBAimage = ImageTk.PhotoImage(self.dds_RGBAimage)
        
        self.dds_labelRGBA = customtkinter.CTkLabel(self.dds_RGBA_picker_frame, text="", image=self.dds_RGBAimage)
        
        self.dds_bt_apply_RGBA = customtkinter.CTkButton(self.dds_RGBA_picker_frame, text="Apply", command=self.change_color, width=0)
        self.dds_bt_cancel_RGBA = customtkinter.CTkButton(self.dds_RGBA_picker_frame, text="Cancel", command=self.dds_RGBA_picker_frame.place_forget, width=0)
        
        self.dds_R_entry = customtkinter.CTkEntry(self.dds_RGBA_picker_frame, textvariable = self.dds_varR, width=50)
        self.dds_R_entry.bind('<KeyRelease>', lambda event: self.dds_update_labelRGBA())
        self.dds_G_entry = customtkinter.CTkEntry(self.dds_RGBA_picker_frame, textvariable = self.dds_varG, width=50)
        self.dds_G_entry.bind('<KeyRelease>', lambda event: self.dds_update_labelRGBA())
        self.dds_B_entry = customtkinter.CTkEntry(self.dds_RGBA_picker_frame, textvariable = self.dds_varB, width=50)
        self.dds_B_entry.bind('<KeyRelease>', lambda event: self.dds_update_labelRGBA())
        self.dds_A_entry = customtkinter.CTkEntry(self.dds_RGBA_picker_frame, textvariable = self.dds_varA, width=50)
        self.dds_A_entry.bind('<KeyRelease>', lambda event: self.dds_update_labelRGBA())
        
        self.dds_labelRGBA.grid(row=1, column=0, rowspan=3, padx = 20, columnspan=2)
        self.dds_bt_apply_RGBA.grid(row=4, column=0)
        self.dds_bt_cancel_RGBA.grid(row=4, column=1)
        self.dds_R_entry.grid(row=1, column=2)
        self.dds_G_entry.grid(row=2, column=2)
        self.dds_B_entry.grid(row=3, column=2)
        self.dds_A_entry.grid(row=4, column=2)
        self.dds_sliderR.grid(row=1, column=3, pady = 10, padx = 10)
        self.dds_sliderG.grid(row=2, column=3, pady = 10, padx = 10)
        self.dds_sliderB.grid(row=3, column=3, pady = 10, padx = 10)
        self.dds_sliderA.grid(row=4, column=3, pady = 10, padx = 10)
        
        
        #RGBA
        self.RGBA_picker_frame = customtkinter.CTkFrame(self.Frame2)
        
        self.constant_color_sample = []
        self.birth_color_sample = []
        
        self.varR = customtkinter.DoubleVar()
        self.varG = customtkinter.DoubleVar()
        self.varB = customtkinter.DoubleVar()
        self.varA = customtkinter.DoubleVar()
    
        self.sliderR = customtkinter.CTkSlider(self.RGBA_picker_frame, progress_color="red", button_color="gray", button_hover_color="white", height=20, button_corner_radius=3, button_length=5, variable=self.varR, command=lambda event: self.update_labelRGBA())
        self.sliderG = customtkinter.CTkSlider(self.RGBA_picker_frame, progress_color="green", button_color="gray", button_hover_color="white", height=20, button_corner_radius=3, button_length=5, variable=self.varG, command=lambda event:self.update_labelRGBA())
        self.sliderB = customtkinter.CTkSlider(self.RGBA_picker_frame, progress_color="blue", button_color="gray", button_hover_color="white", height=20, button_corner_radius=3, button_length=5, variable=self.varB, command=lambda event:self.update_labelRGBA())
        self.sliderA = customtkinter.CTkSlider(self.RGBA_picker_frame, progress_color="white", button_color="gray", button_hover_color="white", height=20, button_corner_radius=3, button_length=5, variable=self.varA, command=lambda event:self.update_labelRGBA())
        
        self.sliderR.set(0.5)
        self.sliderG.set(0.5)
        self.sliderB.set(0.5)
        self.sliderA.set(1)
        
        self.RGBAimage = PIL.Image.new('RGBA', (120, 120), (int(self.sliderR.get()*255), int(self.sliderG.get()*255), int(self.sliderB.get()*255), int(self.sliderA.get()*255)))
        self.RGBAimage = ImageTk.PhotoImage(self.RGBAimage)
        
        self.labelRGBA = customtkinter.CTkLabel(self.RGBA_picker_frame, text="", image=self.RGBAimage)
        
        self.color_type = " color:"
        self.bt_apply_RGBA = customtkinter.CTkButton(self.RGBA_picker_frame, text="Apply", command=self.apply_RGBA, width=0)
        self.bt_cancel_RGBA = customtkinter.CTkButton(self.RGBA_picker_frame, text="Cancel", command=self.RGBA_picker_frame.place_forget, width=0)
        
        self.R_entry = customtkinter.CTkEntry(self.RGBA_picker_frame, textvariable = self.varR, width=50)
        self.R_entry.bind('<KeyRelease>', lambda event: self.update_labelRGBA())
        self.G_entry = customtkinter.CTkEntry(self.RGBA_picker_frame, textvariable = self.varG, width=50)
        self.G_entry.bind('<KeyRelease>', lambda event: self.update_labelRGBA())
        self.B_entry = customtkinter.CTkEntry(self.RGBA_picker_frame, textvariable = self.varB, width=50)
        self.B_entry.bind('<KeyRelease>', lambda event: self.update_labelRGBA())
        self.A_entry = customtkinter.CTkEntry(self.RGBA_picker_frame, textvariable = self.varA, width=50)
        self.A_entry.bind('<KeyRelease>', lambda event: self.update_labelRGBA())
        
        self.labelRGBA.grid(row=1, column=0, rowspan=3, padx = 20, columnspan=2)
        self.bt_apply_RGBA.grid(row=4, column=0)
        self.bt_cancel_RGBA.grid(row=4, column=1)
        self.R_entry.grid(row=1, column=2)
        self.G_entry.grid(row=2, column=2)
        self.B_entry.grid(row=3, column=2)
        self.A_entry.grid(row=4, column=2)
        self.sliderR.grid(row=1, column=3, pady = 10, padx = 10)
        self.sliderG.grid(row=2, column=3, pady = 10, padx = 10)
        self.sliderB.grid(row=3, column=3, pady = 10, padx = 10)
        self.sliderA.grid(row=4, column=3, pady = 10, padx = 10)
        
        
        #TRGBA
        self.list_varTRGBA = []
        self.list_tabTRGBA = []
        self.list_imageTRGBA = []
        self.dynamic_color_sample = []
        
        self.TRGBA_picker_frame = customtkinter.CTkFrame(self.Frame2, width=450, height=335)
        self.TRGBA_picker_frame.pack_propagate(False)
        self.tab_frame = customtkinter.CTkFrame(self.TRGBA_picker_frame, width=430, height=30)
        self.TRGBA_picker_frame.pack_propagate(False)
        self.pick_frame = customtkinter.CTkFrame(self.TRGBA_picker_frame)
        
        self.DvarT = customtkinter.DoubleVar()
        self.DvarR = customtkinter.DoubleVar()
        self.DvarG = customtkinter.DoubleVar()
        self.DvarB = customtkinter.DoubleVar()
        self.DvarA = customtkinter.DoubleVar()
        
        self.DsliderT = customtkinter.CTkSlider(self.pick_frame, progress_color="transparent", button_color="gray", button_hover_color="white", height=20, button_corner_radius=3, button_length=5, variable=self.DvarT, command=lambda event: self.update_labelTRGBA())
        self.DsliderR = customtkinter.CTkSlider(self.pick_frame, progress_color="red", button_color="gray", button_hover_color="white", height=20, button_corner_radius=3, button_length=5, variable=self.DvarR, command=lambda event: self.update_labelTRGBA())
        self.DsliderG = customtkinter.CTkSlider(self.pick_frame, progress_color="green", button_color="gray", button_hover_color="white", height=20, button_corner_radius=3, button_length=5, variable=self.DvarG, command=lambda event: self.update_labelTRGBA())
        self.DsliderB = customtkinter.CTkSlider(self.pick_frame, progress_color="blue", button_color="gray", button_hover_color="white", height=20, button_corner_radius=3, button_length=5, variable=self.DvarB, command=lambda event: self.update_labelTRGBA())
        self.DsliderA = customtkinter.CTkSlider(self.pick_frame, progress_color="white", button_color="gray", button_hover_color="white", height=20, button_corner_radius=3, button_length=5, variable=self.DvarA, command=lambda event: self.update_labelTRGBA())
        
        self.DT_entry = customtkinter.CTkEntry(self.pick_frame, textvariable = self.DvarT, width=50)
        self.DT_entry.bind('<KeyRelease>', lambda: self.update_labelTRGBA())
        self.DR_entry = customtkinter.CTkEntry(self.pick_frame, textvariable = self.DvarR, width=50)
        self.DR_entry.bind('<KeyRelease>', lambda: self.update_labelTRGBA())
        self.DG_entry = customtkinter.CTkEntry(self.pick_frame, textvariable = self.DvarG, width=50)
        self.DG_entry.bind('<KeyRelease>', lambda: self.update_labelTRGBA())
        self.DB_entry = customtkinter.CTkEntry(self.pick_frame, textvariable = self.DvarB, width=50)
        self.DB_entry.bind('<KeyRelease>', lambda: self.update_labelTRGBA())
        self.DA_entry = customtkinter.CTkEntry(self.pick_frame, textvariable = self.DvarA, width=50)
        self.DA_entry.bind('<KeyRelease>', lambda: self.update_labelTRGBA())
        
        self.TRGBAimage = gradient(self.list_varTRGBA, width=20, height=430)
        self.TRGBAimage = ImageTk.PhotoImage(self.TRGBAimage)
        
        self.labelTRGBA = customtkinter.CTkLabel(self.pick_frame, text="", image=self.TRGBAimage, width=430, height=20)
        
        self.bt_add_TRGBA = customtkinter.CTkButton(self.pick_frame, text="Add", command = lambda: self.create_TRGBA(self.list_varTRGBA[self.current_color_tab][0]+((self.list_varTRGBA[self.current_color_tab+1][0]-self.list_varTRGBA[self.current_color_tab][0])*0.5), random.random(), random.random(), random.random(), random.random()), width=0)
        self.bt_delete_TRGBA = customtkinter.CTkButton(self.pick_frame, text="Delete", command=self.delete_TRGBA, width=0)
        self.bt_apply_TRGBA = customtkinter.CTkButton(self.pick_frame, text="Apply", command=self.apply_TRGBA, width=0)
        self.bt_cancel_TRGBA = customtkinter.CTkButton(self.pick_frame, text="Cancel", command=self.cancel_TRGBA, width=0)
        
        self.current_color_tab = 0
        
        if not os.path.exists('Projects'):
            os.makedirs('Projects')
        
        self.create_treeview()
        self.create_treeview2()
        self.current_treeview12 = self.treeview
        if os.listdir('Projects'):
            self.current_project = os.listdir('Projects')[0]
        else:
            self.current_project = ""
    
    
    # F1 F2 FRAME WORK
    def repack_forget(self, frame):
        if frame == 1:
            self.top_left_side_panel.pack_forget()
            self.Frame1.pack_forget()
        else:
            self.top_right_side_panel.pack_forget()
            self.Frame2.pack_forget()
    
    def repack(self):
        self.top_left_side_panel.pack_forget()
        self.Frame1.pack_forget()
        self.top_right_side_panel.pack_forget()
        self.Frame2.pack_forget()
        
        self.top_left_side_panel.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=False, padx=5, pady=10)
        self.Frame1.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True, padx=5, pady=(0,10))
        self.top_right_side_panel.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=False, padx=5, pady=10)
        self.Frame2.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True, padx=5, pady=(0,10))
        
        
    # SWITCH
    def switch_preview(self):
        self.memory_treeview12()
        self.reset_treeview()
    
    def switch_channel(self):
        if self.bt_switch_channel.get():
            self.channel = "RGBA"
            self.bt_switch_channel.configure(text="RGBA")
        else:
            self.channel = "RGB"
            self.bt_switch_channel.configure(text="RGB")
        
        if self.current_treeview12 == self.treeview:
            self.on_click(self.treeview)
        else:
            self.on_click(self.treeview2)
        
        if self.on_bin_analyze:
            if self.treeview3_filepath:
                self.memory_treeview34(self.treeview3)
                self.bin_analyze(self.treeview3_filepath, self.treeview3)
            if self.treeview4_filepath:
                self.memory_treeview34(self.treeview4)
                self.bin_analyze(self.treeview4_filepath, self.treeview4)
    
    
    # RGBA
    def initiate_RGBA(self, color_sample):
        if color_sample == self.birth_color_sample:
            self.color_type = " birthColor:"
        else:
            self.color_type = " color:"
        r, g, b, a = float(color_sample[0]), float(color_sample[1]), float(color_sample[2]), float(color_sample[3])
        self.sliderR.set(r)
        self.sliderG.set(g)
        self.sliderB.set(b)
        self.sliderA.set(a)
        self.RGBA_picker_frame.place(relx=0.3, rely=0)
        self.update_labelRGBA()
    
    def apply_RGBA(self):
        r, g, b, a = self.R_entry.get(), self.G_entry.get(), self.B_entry.get(), self.A_entry.get()
        filepath = self.current_bin_analyze
        lines_py = self.current_lines_py
        
        items = self.get_all_selected_children(self.current_treeview34)
        
        for it in items:
            item = self.current_treeview34.item(it)
            parent = self.current_treeview34.parent(it)
            values = item['values']
            name = item['text']
            if 'constantValue'.lower() in name.lower() and self.color_type.lower() in self.current_treeview34.item(parent)['values'][-1].lower():
                no = values[0] - 1
                old_line = lines_py[no]
                new_line = old_line.split("=")[0] + "= { " + f"{r}, {g}, {b}, {a} " + "}\n"
                lines_py[no] = new_line
                        
        save(filepath, lines_py)
        self.memory_treeview34(self.current_treeview34)
        self.bin_analyze(filepath, self.current_treeview34)
        self.RGBA_picker_frame.place_forget()
        self.find_text()
        
    def update_labelRGBA(self, nothing=None):     
        self.RGBAimage = PIL.Image.new('RGBA', (120, 120), (int(self.sliderR.get()*255), int(self.sliderG.get()*255), int(self.sliderB.get()*255), int(self.sliderA.get()*255)))
        self.RGBAimage = ImageTk.PhotoImage(self.RGBAimage)
        self.labelRGBA.configure(image=self.RGBAimage)
    
    
    # DDS RGBA
    def change_color(self):
        color = (int(self.dds_sliderR.get()*255), int(self.dds_sliderG.get()*255), int(self.dds_sliderB.get()*255), int(self.dds_sliderA.get()*255))

        self.dds_RGBA_picker_frame.place_forget()

        items = self.get_all_selected_children(self.current_treeview12)
        for it in items:
            item = self.current_treeview12.item(it)
            values = item['values']
            change_color(values[-1], color)
        
        if len(self.selected_files) == 1:
            self.textbox.delete("0.0", tkinter.END)
            self.show_multiple_dss(self.selected_files[0])
        
        if self.selected_folders:
            self.process_show_multiple()
        
        if self.bt_switch_preview.get():
            self.memory_treeview12()
            self.reset_treeview()
     
    def dds_update_labelRGBA(self, nothing=None):     
        self.dds_RGBAimage = PIL.Image.new('RGBA', (120, 120), (int(self.dds_sliderR.get()*255), int(self.dds_sliderG.get()*255), int(self.dds_sliderB.get()*255), int(self.dds_sliderA.get()*255)))
        self.dds_RGBAimage = ImageTk.PhotoImage(self.dds_RGBAimage)
        self.dds_labelRGBA.configure(image=self.dds_RGBAimage) 
    
    # TRGBA
    def switch_color_tab(self, tab):
        index = self.list_tabTRGBA.index(tab)
        self.DsliderT.set(self.list_varTRGBA[index][0])
        self.DsliderR.set(self.list_varTRGBA[index][1])
        self.DsliderG.set(self.list_varTRGBA[index][2])
        self.DsliderB.set(self.list_varTRGBA[index][3])
        self.DsliderA.set(self.list_varTRGBA[index][4])
        self.current_color_tab = self.list_tabTRGBA.index(tab)
        if self.current_color_tab == 0 or self.current_color_tab == len(self.list_tabTRGBA)-1:
            self.DsliderT.configure(state=tkinter.DISABLED)
            self.DT_entry.configure(state=tkinter.DISABLED)
            self.bt_delete_TRGBA.grid_forget()
        else:
            self.DsliderT.configure(state="normal")
            self.DT_entry.configure(state="normal")
            self.bt_delete_TRGBA.grid(row=6, column=1, pady = 10)
            
        if self.current_color_tab == len(self.list_tabTRGBA)-1:
            self.bt_add_TRGBA.grid_forget()
        else:
            self.bt_add_TRGBA.grid(row=6, column=0, pady = 10)
            
        for button in self.list_tabTRGBA:
            if button == tab:
                button.configure(border_width = 2)
            else:
                button.configure(border_width = 0)
    
    def initiate_TRGBA(self):
        for trgba in self.dynamic_color_sample:
            self.create_default_TRGBA(float(trgba[0]), float(trgba[1]), float(trgba[2]), float(trgba[3]), float(trgba[4]))
        self.switch_color_tab(self.list_tabTRGBA[self.current_color_tab])
        self.pack_TRGBA()
        self.update_labelTRGBA()
        pass
      
    def create_default_TRGBA(self, t, r, g, b, a):
        self.list_varTRGBA.append([t, r, g, b, a])

        self.DsliderT.set(t)
        self.DsliderR.set(r)
        self.DsliderG.set(g)
        self.DsliderB.set(b)
        self.DsliderA.set(a)
        
        tab = customtkinter.CTkButton(self.tab_frame, text = "", fg_color='#{:02x}{:02x}{:02x}'.format(int(r*255), int(g*255), int(b*255)), bg_color="transparent", hover_color="white", command=lambda: self.switch_color_tab(tab), border_color="white")
        self.list_tabTRGBA.append(tab)
    
    def create_TRGBA(self, t, r, g, b, a):
        self.DsliderT.set(t)
        self.DsliderR.set(r)
        self.DsliderG.set(g)
        self.DsliderB.set(b)
        self.DsliderA.set(a)
        
        tab = customtkinter.CTkButton(self.tab_frame, text = "", fg_color='#{:02x}{:02x}{:02x}'.format(int(r*255), int(g*255), int(b*255)), bg_color="transparent", hover_color="white", command=lambda: self.switch_color_tab(tab), border_color="white")
        for index, value in enumerate(self.list_varTRGBA):
            if self.list_varTRGBA[index-1][0] <= t <= value[0]: 
                self.list_tabTRGBA.insert(index, tab)
                self.list_varTRGBA.insert(index, [t, r, g, b, a])
                break
        self.current_color_tab = self.list_tabTRGBA.index(tab)
        self.switch_color_tab(tab)
        if self.current_color_tab > 0:
            self.TRGBA_picker_frame.place_forget()
            self.pack_TRGBA()
            self.update_labelTRGBA()
    
    def delete_TRGBA(self):
        self.list_tabTRGBA[self.current_color_tab].place_forget()
        t, r, g, b, a = self.list_varTRGBA[self.current_color_tab-1]
        self.list_tabTRGBA.pop(self.current_color_tab)
        self.list_varTRGBA.pop(self.current_color_tab)
        
        self.DsliderT.set(t)
        self.DsliderR.set(r)
        self.DsliderG.set(g)
        self.DsliderB.set(b)
        self.DsliderA.set(a)
        self.current_color_tab -= 1
        self.TRGBA_picker_frame.place_forget()
        self.pack_TRGBA()
        self.update_labelTRGBA()
        
    def clear_TRGBA(self):
        self.TRGBA_picker_frame.place_forget()
        self.list_varTRGBA = []
        self.list_tabTRGBA = []
        self.current_color_tab = 0
    
    def cancel_TRGBA(self):
        self.clear_TRGBA()
        self.TRGBA_picker_frame.place_forget()
    
    def apply_TRGBA(self):
        filepath = self.current_bin_analyze
        lines_py = self.current_lines_py
        list_time = []
        list_var = []
        for trgba in self.list_varTRGBA:
            list_time.append(trgba[0])
            list_var.append([trgba[1], trgba[2], trgba[3], trgba[4]])
        
        offset = 0
        
        items = self.get_all_selected_children(self.current_treeview34)
        
        for it in items:
            item = self.current_treeview34.item(it)
            parent = self.current_treeview34.parent(it)
            values = item['values']
            name = item['text']
            if 'dynamics'.lower() in name.lower() and " color:" in self.current_treeview34.item(parent)['values'][-1]:
                format_no_lines_time = []
                lines_time = values[2].split('} {')[0].replace("{","").replace("}","").split(" ")
                for lt in lines_time:
                    format_no_lines_time.append(int(lt))
                no_lines_time = format_no_lines_time
                number = re.findall(r"[-+]?(?:\d*\.*\d+)", lines_py[no_lines_time[0]+offset])[0]
                space = lines_py[no_lines_time[0]+offset].split(number)[0]
                for i, t in enumerate(list_time):
                    new_line = space + str(t) + "\n"
                    if i <= len(no_lines_time)-1:
                        lines_py[no_lines_time[0]+i+offset] = new_line
                    else:
                        lines_py.insert(no_lines_time[0]+i+offset, new_line)
                    if i == len(list_time) - 1 and i < len(no_lines_time) - 1:
                        gap = len(no_lines_time) - len(list_time)
                        for g in range(gap):
                            lines_py.pop(no_lines_time[0]+i+offset+1)
                    
                offset += len(list_time) - len(no_lines_time)
                
                format_no_lines_values = []
                lines_values = values[2].split('} {')[1].replace("{","").replace("}","").split(" ")
                for lv in lines_values:
                    format_no_lines_values.append(int(lv))
                no_lines_values = format_no_lines_values
                space = lines_py[no_lines_values[0]+offset].split("{")[0]
                for i, v in enumerate(list_var):
                    new_line = space + "{ " + f"{v[0]}, {v[1]}, {v[2]}, {v[3]}" + " }\n"
                    if i < len(no_lines_values):
                        lines_py[no_lines_values[0]+i+offset] = new_line
                    else:
                        lines_py.insert(no_lines_values[0]+i+offset, new_line)
                    if i == len(list_var) - 1 and i < len(no_lines_values) - 1:
                        gap = len(no_lines_values) - len(list_var)
                        for g in range(gap):
                            lines_py.pop(no_lines_values[0]+i+offset+1)
                            
                offset += len(list_var) - len(no_lines_values)
        
        save(filepath, lines_py)
        self.memory_treeview34(self.current_treeview34)
        self.bin_analyze(filepath, self.current_treeview34)
        self.clear_TRGBA()
        self.TRGBA_picker_frame.place_forget()
        self.find_text()
    
    def pack_TRGBA(self):
        self.TRGBA_picker_frame.place(relx=0.3, rely=0)
        self.tab_frame.pack(pady = (10,0))
        for index, tab in enumerate(self.list_tabTRGBA):
            if index == 0:
                tab.configure(width = 430 * (self.list_varTRGBA[1][0] * 0.5))
                tab.place(relx=0)
            elif index == len(self.list_tabTRGBA) - 1:
                tab.configure(width = 430 * ((1 - self.list_varTRGBA[-2][0]) * 0.5))
                tab.place(relx= 1 - (1 - self.list_varTRGBA[-2][0]) * 0.5)
            else:
                tab.configure(width = 430 * (((self.list_varTRGBA[index][0] - self.list_varTRGBA[index-1][0]) * 0.5) + ((self.list_varTRGBA[index+1][0] - self.list_varTRGBA[index][0]) * 0.5)))
                tab.place(relx = self.list_varTRGBA[index][0] - ((self.list_varTRGBA[index][0] - self.list_varTRGBA[index-1][0]) * 0.5))
        self.pick_frame.pack(padx = 10, pady = 10)
        self.labelTRGBA.grid(row=0, column=0, columnspan=4, pady = (0,10))
        self.bt_add_TRGBA.grid(row=6, column=0, pady = 10)
        self.bt_delete_TRGBA.grid(row=6, column=1, pady = 10)
        self.bt_apply_TRGBA.grid(row=6, column=2, pady = 10)
        self.bt_cancel_TRGBA.grid(row=6, column=3, pady = 10)
        self.DT_entry.grid(row=1, column=0)
        self.DR_entry.grid(row=2, column=0)
        self.DG_entry.grid(row=3, column=0)
        self.DB_entry.grid(row=4, column=0)
        self.DA_entry.grid(row=5, column=0)
        self.DsliderT.grid(row=1, column=1, pady = 10, padx = 10, columnspan=3)
        self.DsliderR.grid(row=2, column=1, pady = 10, padx = 10, columnspan=3)
        self.DsliderG.grid(row=3, column=1, pady = 10, padx = 10, columnspan=3)
        self.DsliderB.grid(row=4, column=1, pady = 10, padx = 10, columnspan=3)
        self.DsliderA.grid(row=5, column=1, pady = 10, padx = 10, columnspan=3)
   
    def update_labelTRGBA(self):
        trgba = [self.DsliderT.get(), self.DsliderR.get(), self.DsliderG.get(), self.DsliderB.get(), self.DsliderA.get()]
        self.list_varTRGBA[self.current_color_tab] = trgba
        self.list_tabTRGBA[self.current_color_tab].configure(fg_color='#{:02x}{:02x}{:02x}'.format(int(self.DsliderR.get()*255), int(self.DsliderG.get()*255), int(self.DsliderB.get()*255)))
        
        index = self.current_color_tab
        if index != 0 and index != len(self.list_tabTRGBA) - 1:
            if self.list_varTRGBA[index-1][0] > self.DsliderT.get():
                pre_tabTRGBA = self.list_tabTRGBA[index-1]
                current_tabTRGBA = self.list_tabTRGBA[index]
                self.list_tabTRGBA[index-1] = current_tabTRGBA
                self.list_tabTRGBA[index] = pre_tabTRGBA
                
                pre_varTRGBA = self.list_varTRGBA[index-1]
                current_varTRGBA = self.list_varTRGBA[index]
                self.list_varTRGBA[index-1] = current_varTRGBA
                self.list_varTRGBA[index] = pre_varTRGBA
                self.current_color_tab -= 1

            if self.DsliderT.get() > self.list_varTRGBA[index+1][0]:
                pre_tabTRGBA = self.list_tabTRGBA[index+1]
                current_tabTRGBA = self.list_tabTRGBA[index]
                self.list_tabTRGBA[index+1] = current_tabTRGBA
                self.list_tabTRGBA[index] = pre_tabTRGBA
                
                pre_varTRGBA = self.list_varTRGBA[index+1]
                current_varTRGBA = self.list_varTRGBA[index]
                self.list_varTRGBA[index+1] = current_varTRGBA
                self.list_varTRGBA[index] = pre_varTRGBA
                self.current_color_tab += 1
        
        for index, tab in enumerate(self.list_tabTRGBA):
            if index == 0:
                tab.configure(width = 430 * (self.list_varTRGBA[1][0] * 0.5))
                tab.place(relx=0)
            elif index == len(self.list_tabTRGBA) - 1:
                tab.configure(width = 430 * ((1 - self.list_varTRGBA[-2][0]) * 0.5))
                tab.place(relx= 1 - (1 - self.list_varTRGBA[-2][0]) * 0.5)
            else:
                tab.configure(width = 430 * (((self.list_varTRGBA[index][0] - self.list_varTRGBA[index-1][0]) * 0.5) + ((self.list_varTRGBA[index+1][0] - self.list_varTRGBA[index][0]) * 0.5)))
                tab.place(relx = self.list_varTRGBA[index][0] - ((self.list_varTRGBA[index][0] - self.list_varTRGBA[index-1][0]) * 0.5))
        
        self.TRGBAimage = gradient(self.list_varTRGBA, width=20, height=430)
        self.TRGBAimage = ImageTk.PhotoImage(self.TRGBAimage)
        
        self.labelTRGBA.configure(image=self.TRGBAimage)
    
    
    # FIND TEXT
    def find_text(self):
        self.list_find = []
        self.current_find_index = 0
        self.textbox.tag_remove('found', '1.0', tkinter.END)
        self.textbox.tag_remove('found_focus', '1.0', tkinter.END)
        s = self.search_text_entry.get()
        found = 0
        if s:
            index = '1.0'
            while True:
                index = self.textbox.search(s, index, nocase=1, stopindex=tkinter.END)
                if not index:
                    break
                last_index = '%s+%dc' % (index, len(s))
                self.textbox.tag_add('found', index, last_index)
                self.list_find.append([index, last_index])
                found += 1
                index = last_index
            self.label_search.configure(text = str(self.current_find_index + 1) + "/" + str(len(self.list_find)))
            self.textbox.see(self.list_find[self.current_find_index][0])
        else:
            self.label_search.configure(text = "0/0")
            
    def search_text(self):
        self.Frame_search_text.place(relx = 0.87, rely = 0)
        self.search_text_entry.focus()
    
    def up_search(self):
        self.textbox.tag_remove('found_focus', '1.0', tkinter.END)
        if self.current_find_index > 0:
            self.current_find_index -= 1
            self.textbox.see(self.list_find[self.current_find_index][0])
            self.textbox.tag_add('found_focus', self.list_find[self.current_find_index][0], self.list_find[self.current_find_index][1])
            self.label_search.configure(text = str(self.current_find_index + 1) + "/" + str(len(self.list_find)))
        
    def down_search(self):
        self.textbox.tag_remove('found_focus', '1.0', tkinter.END)
        if self.current_find_index < len(self.list_find) - 1:
            self.current_find_index += 1
            self.textbox.see(self.list_find[self.current_find_index][0])
            self.textbox.tag_add('found_focus', self.list_find[self.current_find_index][0], self.list_find[self.current_find_index][1])
            self.label_search.configure(text = str(self.current_find_index + 1) + "/" + str(len(self.list_find)))
    
    
    # BIN FUNCTIONS
    def bin_analyze(self, filepath, treeview, clear_memory=False):
        lines_py = read_py(filepath)
        
        for item in treeview.get_children():
            treeview.delete(item)
        root_node = treeview.insert('', 'end', text="  "+filepath, open=True, values=[1, len(lines_py), ''], image=self.code_icon)
 
        if treeview == self.treeview3:
            self.treeview3_filepath = filepath
            self.current_bin_analyze = self.treeview3_filepath
            
            self.treeview3_lines_py = lines_py
            self.current_lines_py = self.treeview3_lines_py
            
            self.list_analyze_images = []
            self.list_combine_images = []
            list_image = self.list_analyze_images
            list_combine_image = self.list_combine_images
            if clear_memory:
                self.open3 = []
        else:
            self.treeview4_filepath = filepath
            self.current_bin_analyze = self.treeview4_filepath
            
            self.treeview4_lines_py = lines_py
            self.current_lines_py = self.treeview4_lines_py
            
            self.list_analyze_images2 = []
            self.list_combine_images2 = []
            list_image = self.list_analyze_images2
            list_combine_image = self.list_combine_images2
            if clear_memory:
                self.open4 = []
        
        self.on_bin_analyze = True
        self.hide_button("right")
        
        tab = " " * 4
        
        spaces = [-2]
        nodes = [root_node]
        class_combine_image = ""
        
        for no, line in enumerate(lines_py):
            tag = []
            image = None
            open = False
            value = [no+1, line]
            name = line.replace(" = {\n", "").replace("{\n", "")
            name = name.strip()
            line_lower = line.lower()
            
            if "{\n" in line:
                name = name.split(":")[0]
                spaces.append(len(line.split(tab))-1)
                
                if "SkinCharacterDataProperties {".lower() in line_lower or "VfxSystemDefinitionData {".lower() in line_lower or "ResourceResolver {".lower() in line_lower:
                    name = name.split("=")[0].split("/")[-1].replace('"',"")
                    tag.append('yellow')
                elif "VfxEmitterDefinitionData".lower() in line_lower:
                    tag.append('green')
                elif "complexEmitterDefinitionData".lower() in line_lower:
                    tag.append('green')
                else:
                    tag.append('blue vs')
                
                if "color".lower() in line_lower or "entries:".lower() in line_lower or "complexEmitterDefinitionData".lower() in line_lower or "resourceMap".lower() in line_lower or "primitive".lower() in line_lower:
                    open = True
                
                       
                if " dynamics:" in line_lower and "color" in treeview.item(nodes[-1])['text']:
                    name = tab + name
                    treeview.item(nodes[-1], open=True)
                    space = len(line.split(tab))-1
                    list_times = []
                    list_values = []
                    list_trgba = []
                    list_time_lines = []
                    list_values_lines = []
                    for no2, line2 in enumerate(lines_py[no:]):
                        line2_lower = line2.lower()
                        if " times:" in line2_lower:
                            space2 = len(line2.split(tab))-1
                            for i in range(1,10):
                                if space2 * tab + "}\n" == lines_py[no+no2+i]:
                                    break
                                list_times.append(lines_py[no+no2+i].strip().replace("\n",""))
                                list_time_lines.append(no+no2+i)
                        elif " values:" in line2_lower:
                            space3 = len(line2.split(tab))-1
                            for i in range(1,10):
                                if space3 * tab + "}\n" == lines_py[no+no2+i]:
                                    break
                                list_values.append(lines_py[no+no2+i].strip().replace("\n",""))
                                list_values_lines.append(no+no2+i)
                        elif space * tab + "}\n" == line2:
                            break
                    for i in range(len(list_times)):
                        r, g, b, a = list_values[i].replace("{","").replace("}","").strip().split(",")
                        list_trgba.append([float(list_times[i]), float(r), float(g), float(b), float(a)])
                    image = gradient(list_trgba, width=20, height=45)
                    if self.channel == "RGB":
                        image = numpy.array(image)
                        image = image[:,:,:3]
                        image = Image.fromarray(image)
                    
                    if class_combine_image:
                        combine_image = class_combine_image.combine(image)
                        list_combine_image.append(combine_image)
                        
                    
                    image = ImageTk.PhotoImage(image)
                    list_image.append(image)
                    image = list_image[-1]
                    value = [no+1, [list_time_lines, list_values_lines], list_trgba, line]
                    
                    if class_combine_image:
                        treeview.item(class_combine_image.node, image=combine_image)
                        treeview.item(class_combine_image.node, text=tab + treeview.item(class_combine_image.node)['text'].strip())
                    
                if image is not None:
                    node = treeview.insert(nodes[-1], 'end', text=name, open=open, values=value, tags = tag, image = image)
                else:
                    node = treeview.insert(nodes[-1], 'end', text=name, open=open, values=value, tags = tag)
                nodes.append(node)
                if "VfxEmitterDefinitionData".lower() in line_lower:
                    class_combine_image = Combine_Image(node)
                
            elif len(line.split(tab)) - 1  == spaces[-1] - 1:
                treeview.insert(nodes[-1], 'end', text=name, open=False, values=value, tags = tag)
            elif line == spaces[-1] * tab + "}\n":
                old_value = treeview.item(nodes[-1])['values']
                old_value.insert(1, no+1)
                treeview.item(nodes[-1], values = old_value)
                treeview.item(nodes[-1], values = old_value)
                nodes.pop(-1)
                spaces.pop(-1)
            else:
                if "particleName:".lower() in line_lower and "0x" in treeview.item(nodes[-1])["text"]:
                    particlename = line.split("=")[-1].strip().replace('"', "")
                    old_text = treeview.item(nodes[-1])["text"]
                    treeview.item(nodes[-1], text=old_text + f"  ({particlename})")
                elif "emitterName".lower() in line_lower:
                    emitter = line.split("=")[-1].replace("\n", "")
                    emitter = emitter.replace('"',"").replace(" ","")
                    treeview.item(nodes[-1], text=emitter)
                elif ".skl" in line_lower:
                    name = tab + name
                    skeleton = line.split("=")[-1].replace("\n","")
                    path = filepath.split(".wad/")[0] + ".wad/" + skeleton.replace('"',"").strip()
                    image=self.skl_icon
                    if os.path.exists(path.lower()) or os.path.exists(path.lower().replace("yours", "riot")) or os.path.exists(filepath.split("Projects")[0]+"Default/"+skeleton.replace('"',"").strip()):
                        tag.append('orange')
                    else:
                        tag.append('red')
                    if "VfxEmitterDefinitionData".lower() not in treeview.item(nodes[-1])['values'][-1].lower() and "SkinCharacterDataProperties".lower() not in treeview.item(nodes[-1])['values'][-1].lower():
                        treeview.item(nodes[-1], open=True)
                elif ".skn".lower() in line_lower:
                    name = tab + name
                    simpleSkin = line.split("=")[-1].replace("\n","")
                    path = filepath.split(".wad/")[0] + ".wad/" + simpleSkin.replace('"',"").strip()
                    image=self.object_icon
                    if os.path.exists(path.lower()) or os.path.exists(path.lower().replace("yours", "riot")) or os.path.exists(filepath.split("Projects")[0]+"Default/"+simpleSkin.replace('"',"").strip()):
                        tag.append('orange')
                    else:
                        tag.append('red')
                    if "VfxEmitterDefinitionData".lower() not in treeview.item(nodes[-1])['values'][-1].lower() and "SkinCharacterDataProperties".lower() not in treeview.item(nodes[-1])['values'][-1].lower():
                        treeview.item(nodes[-1], open=True)
                elif ".bnk".lower() in line_lower:
                    name = tab + name
                    bnk = line.split("=")[-1].replace("\n","")
                    path = filepath.split(".wad/")[0] + ".wad/" + bnk.replace('"',"").strip()
                    image=self.audio_icon
                    tag.append('orange')
                    if "VfxEmitterDefinitionData".lower() not in treeview.item(nodes[-1])['values'][-1].lower() and "SkinCharacterDataProperties".lower() not in treeview.item(nodes[-1])['values'][-1].lower():
                        treeview.item(nodes[-1], open=True)
                elif ".wpk".lower() in line_lower:
                    name = tab + name
                    wpk = line.split("=")[-1].replace("\n","")
                    path = filepath.split(".wad/")[0] + ".wad/" + wpk.replace('"',"").strip()
                    image=self.audio_icon
                    tag.append('orange')
                    if "VfxEmitterDefinitionData".lower() not in treeview.item(nodes[-1])['values'][-1].lower() and "SkinCharacterDataProperties".lower() not in treeview.item(nodes[-1])['values'][-1].lower():
                        treeview.item(nodes[-1], open=True)
                elif ".scb".lower() in line_lower:
                    name = tab + name
                    scb = line.split("=")[-1].replace("\n","")
                    path = filepath.split(".wad/")[0] + ".wad/" + scb.replace('"',"").strip()
                    image=self.object_icon
                    if os.path.exists(path.lower()) or os.path.exists(path.lower().replace("yours", "riot")) or os.path.exists(filepath.split("Projects")[0]+"Default/"+scb.replace('"',"").strip()):
                        tag.append('orange')
                    else:
                        tag.append('red')
                    if "VfxEmitterDefinitionData".lower() not in treeview.item(nodes[-1])['values'][-1].lower() and "SkinCharacterDataProperties".lower() not in treeview.item(nodes[-1])['values'][-1].lower():
                        treeview.item(nodes[-1], open=True)
                elif ".sco".lower() in line_lower:
                    name = tab + name
                    sco = line.split("=")[-1].replace("\n","")
                    path = filepath.split(".wad/")[0] + ".wad/" + sco.replace('"',"").strip()
                    image=self.object_icon
                    if os.path.exists(path.lower()) or os.path.exists(path.lower().replace("yours", "riot")) or os.path.exists(filepath.split("Projects")[0]+"Default/"+sco.replace('"',"").strip()):
                        tag.append('orange')
                    else:
                        tag.append('red')
                    if "VfxEmitterDefinitionData".lower() not in treeview.item(nodes[-1])['values'][-1].lower() and "SkinCharacterDataProperties".lower() not in treeview.item(nodes[-1])['values'][-1].lower():
                        treeview.item(nodes[-1], open=True)
                elif ".bin".lower() in line_lower:
                    tag.append('orange')
                elif ".dds".lower() in line_lower:
                    name = tab + name
                    if "=" in line:
                        dds = line.split("=")[-1].replace("\n", "")
                    else:
                        dds = line.replace("\n", "")
                    path = filepath.split(".wad/")[0] + ".wad/" + dds.replace('"',"").strip()
                    if os.path.exists(path.lower()) or os.path.exists(path.lower().replace("yours", "riot")) or os.path.exists(filepath.split("Projects")[0]+"Default/"+dds.replace('"',"").strip()):
                        try:
                            image = Image.open(path.lower())
                        except:
                            try:
                                image = Image.open(path.lower().replace("yours", "riot"))
                            except:
                                image = Image.open(filepath.split("Projects")[0]+"Default/"+dds.replace('"',"").strip())
                        if self.channel == "RGB":
                            image = numpy.array(image)
                            image = image[:,:,:3]
                            image = Image.fromarray(image)
                        width, height = image.size
                        scale = width / height
                        image = image.resize((math.ceil(20*scale), 20))
                        
                        if class_combine_image:
                            combine_image = class_combine_image.combine(image)
                            list_combine_image.append(combine_image)
                        
                        image = ImageTk.PhotoImage(image)
                        list_image.append(image)
                        image = list_image[-1]
                        tag.append('orange')
                        
                        if class_combine_image:
                            treeview.item(class_combine_image.node, image=combine_image)
                            treeview.item(class_combine_image.node, text=tab + treeview.item(class_combine_image.node)['text'].strip())
                    else:
                        image = self.image_icon
                        tag.append('red')
                    if "VfxEmitterDefinitionData".lower() not in treeview.item(nodes[-1])['values'][-1].lower() and "SkinCharacterDataProperties".lower() not in treeview.item(nodes[-1])['values'][-1].lower():
                        treeview.item(nodes[-1], open=True)
                elif " disabled:".lower() in line_lower:
                    disable = line.split("=")[-1].replace("\n", "")
                    if "true" in disable:
                        treeview.item(nodes[-1], tags=('red',))
                        tag.append('red')
                    else:
                        tag.append('green')
                
                elif " constantValue:".lower() in line_lower and "ValueColor".lower() in treeview.item(nodes[-1])['values'][-1].lower():
                    name = tab + name
                    color = line.split("=")[-1]
                    r, g, b, a = color.replace("{","").replace("}","").strip().split(",")
                    image = PIL.Image.new('RGBA', (45, 20), (int(float(r)*255), int(float(g)*255), int(float(b)*255), int(float(a)*255)))
                    if self.channel == "RGB":
                        image = numpy.array(image)
                        image = image[:,:,:3]
                        image = Image.fromarray(image)
                    
                    if class_combine_image:
                        combine_image = class_combine_image.combine(image)
                        list_combine_image.append(combine_image)
                        
                    image = ImageTk.PhotoImage(image)
                    
                    list_image.append(image)
                    if float(a) != 0:
                        image=list_image[-1]          
                    else:
                        image=self.transparent_icon
                    value = [no+1, float(r), float(g), float(b), float(a), line]
                    
                    if class_combine_image:
                        treeview.item(class_combine_image.node, image=combine_image)
                        treeview.item(class_combine_image.node, text=tab + treeview.item(class_combine_image.node)['text'].strip())
                
                value.insert(1, no+1)
                
                if '"' == line.strip()[0] and '"' == line.strip()[-1]:
                    if "red" not in tag:
                        tag.append('orange')
                
                if image is not None:
                    treeview.insert(nodes[-1], 'end', text=name, open=open, values=value, tags = tag, image = image)
                    
                else:
                    treeview.insert(nodes[-1], 'end', text=name, open=open, values=value, tags = tag)
        
        self.reset_treeview34(treeview)
    
    def scan(self):
        self.in_use = []
        self.list_errors = []
        
        filepath = self.current_bin_analyze
        lines_py = self.current_lines_py
        case1 = [".skl", ".skn", ".scb", ".sco"]
        for select in self.select_range:
            start_line = select[0]
            end_line = select[1]
            for no, line in enumerate(lines_py[start_line-1: end_line]):
                if any(i for i in case1 if i.lower() in line.lower()):
                    shortpath = line.split("=")[-1].replace("\n","").replace('"',"").strip()
                    path = filepath.split(".wad/")[0] + ".wad/" + shortpath.replace('"',"").strip()
                    if os.path.exists(path.lower()) or os.path.exists(path.lower().replace("yours", "riot")) or os.path.exists(filepath.split("Projects")[0]+"Default/"+shortpath.replace('"',"").strip()):
                        if shortpath not in self.in_use:
                            self.in_use.append(shortpath)
                    else:
                        if shortpath not in self.list_errors:
                            self.list_errors.append(shortpath)
                elif ".dds".lower() in line.lower():
                    if "=" in line:
                        dds = line.split("=")[-1].replace("\n", "").replace('"',"").strip()
                    else:
                        dds = line.replace("\n", "").replace('"',"").strip()
                    path = filepath.split(".wad/")[0] + ".wad/" + dds.replace('"',"").strip()
                    if os.path.exists(path.lower()) or os.path.exists(path.lower().replace("yours", "riot")) or os.path.exists(filepath.split("Projects")[0]+"Default/"+dds.replace('"',"").strip()):
                        if dds not in self.in_use:
                            self.in_use.append(dds)
                    else:
                        if dds not in self.list_errors:
                            self.list_errors.append(dds)
        
        self.textbox2.delete("0.0", "end")
        self.textbox2.insert(tkinter.END, self.current_bin_analyze+"\n\n", "white")
        if self.list_errors:
            for error in self.list_errors:
                self.textbox2.insert(tkinter.END, "  "+error+"\n", "red")
        if self.in_use:
            for use in self.in_use:
                if ".dds".lower() in use.lower():
                    path = filepath.split(".wad/")[0] + ".wad/" + use.replace('"',"").strip()
                    try:
                        image = Image.open(path.lower())
                    except:
                        try:
                            image = Image.open(path.lower().replace("yours", "riot"))
                        except:
                            image = Image.open(filepath.split("Projects")[0]+"Default/"+use.replace('"',"").strip())
                    if self.channel == "RGB":
                        image = numpy.array(image)
                        image = image[:,:,:3]
                        image = Image.fromarray(image)
                    width, height = image.size
                    scale = width / height
                    image = image.resize((50, math.ceil(50/scale)))
                    image = ImageTk.PhotoImage(image)
                    self.list_multiple_dss.append(image)
                    self.textbox2.image_create(tkinter.END, image=self.list_multiple_dss[-1])
                self.textbox2.insert(tkinter.END, "  "+use+"\n\n", "green")
    
    def on_click34(self, treeview):
        has_constant = False
        has_birth = False
        has_dynamic = False
        has_disabled = False
        has_enabled = False
        self.bt_bin_change_constant_color.pack_forget()
        self.bt_bin_change_birth_color.pack_forget()
        self.bt_bin_change_dynamic_color.pack_forget()
        self.bt_bin_disable_emitter.pack_forget()
        self.bt_bin_enable_emitter.pack_forget()
        self.bt_bin_change_path.pack_forget()
        self.bt_bin_scan.pack_forget()
        
        items = self.get_all_selected_children(treeview)
        
        self.select_range = []
        select_range = [0,0]
        for it in items:
            item = treeview.item(it)
            parent = treeview.parent(it)
            name = item['text']
            color = item['tags']
            values = item['values']
            if 'constantValue'.lower() in name.lower() and " color:" in treeview.item(parent)['values'][-1]:
                has_constant = values
            elif 'constantValue'.lower() in name.lower() and " birthColor:".lower() in treeview.item(parent)['values'][-1].lower():
                has_birth = values
            elif 'dynamics'.lower() in name.lower() and " color:" in treeview.item(parent)['values'][-1]:
                has_dynamic = values
            elif 'red' in color:
                if 'VfxEmitterDefinitionData'.lower() in values[-1].lower():
                    has_enabled = True
            elif 'green' in color:
                if 'VfxEmitterDefinitionData'.lower() in values[-1].lower():
                    has_disabled = True

            start_line = values[0]
            end_line = values[1]
            if start_line not in range(select_range[0], select_range[1]) and end_line not in range(select_range[0], select_range[1]):
                select_range = [start_line, end_line]
                self.select_range.append(select_range)   
            
        if has_constant:
            self.bt_bin_change_constant_color.pack(side=tkinter.LEFT, padx=(0,5), pady=0)
            self.constant_color_sample = has_constant[2:-1]
        
        if has_birth:
            self.bt_bin_change_birth_color.pack(side=tkinter.LEFT, padx=(0,5), pady=0)
            self.birth_color_sample = has_birth[2:-1]
        
        if has_dynamic:
            self.bt_bin_change_dynamic_color.pack(side=tkinter.LEFT, padx=(0,5), pady=0)
            format_trgba = []
            for trgba in has_dynamic[3].split('} {'):
                trgba = trgba.replace("{","").replace("}","")
                t, r, g, b, a = trgba.split(" ")
                format_trgba.append([float(t), float(r), float(g), float(b), float(a)])
            self.dynamic_color_sample = format_trgba
            
        if has_disabled:
            self.bt_bin_disable_emitter.pack(side=tkinter.LEFT, padx=(0,5), pady=0)
        if has_enabled:
            self.bt_bin_enable_emitter.pack(side=tkinter.LEFT, padx=(0,5), pady=0)
        self.bt_bin_change_path.pack(side=tkinter.LEFT, padx=(0,5), pady=0)
        self.bt_bin_scan.pack(side=tkinter.LEFT, padx=(0,5), pady=0)
        
        self.current_treeview34 = treeview
        if self.current_treeview34 == self.treeview3:
            self.current_bin_analyze = self.treeview3_filepath
        else:
            self.current_bin_analyze = self.treeview4_filepath
        
        self.textbox2.delete("0.0", tkinter.END)
        lines_py = self.current_lines_py
        for r in self.select_range:
            for line in lines_py[r[0]-1:r[1]]:
                self.textbox2.insert(tkinter.END, line, "white")
        threading.Thread(target=self.format_py, args=(lines_py[r[0]-1:r[1]],)).run()
        
    def disable_emitter(self):
        filepath = self.current_bin_analyze
        lines_py = self.current_lines_py

        items = self.get_all_selected_children(self.current_treeview34)
        offset = 0
        for item in items:
            item = self.current_treeview34.item(item)
            values = item['values']
            if "emitterName".lower() in str(values[-1]).lower():
                if "disabled:" in lines_py[values[0]+offset]:
                    lines_py[values[0]+offset] = lines_py[values[0]+offset].replace("false", "true")
                else:
                    space = lines_py[values[0]+offset-1].split("emitter")[0]
                    new_line = space + "disabled: bool = true\n"
                    lines_py.insert(values[0]+offset, new_line)
                    offset += 1
        
        save(filepath, lines_py)
        self.memory_treeview34(self.current_treeview34)
        self.bin_analyze(filepath, self.current_treeview34)
    
    def enable_emitter(self):
        filepath = self.current_bin_analyze
        lines_py = self.current_lines_py
        
        items = self.get_all_selected_children(self.current_treeview34)
        offset = 0
        for item in items:
            item = self.current_treeview34.item(item)
            values = item['values']
            if " disabled:".lower() in str(values[-1]).lower():
                lines_py.pop(values[0]+offset-1)
                offset -= 1

        save(filepath, lines_py)
        self.memory_treeview34(self.current_treeview34)
        self.bin_analyze(filepath, self.current_treeview34)

    def delete_line_bin(self):
        filepath = self.current_bin_analyze
        lines_py = self.current_lines_py
        items = []
        for selected_item in self.current_treeview34.selection():
            item = self.current_treeview34.item(selected_item)
            if item not in items:
                items.append(item)
        
        offset = 0
        delete_range = [0,0]
        for item in items:
            values = item['values']
            start_line = values[0]
            end_line = values[1]
            if start_line not in range(delete_range[0], delete_range[1]) and end_line not in range(delete_range[0], delete_range[1]):
                delete_range = [start_line, end_line]
                for i in range(end_line - start_line + 1):
                    lines_py.pop(start_line + offset - 1)
                offset -= (end_line - start_line + 1) 

        save(filepath, lines_py)
        self.memory_treeview34(self.current_treeview34)
        self.bin_analyze(filepath, self.current_treeview34)
    
    def copy_bin(self):
        lines_py = self.current_lines_py
        items = []
        for selected_item in self.current_treeview34.selection():
            item = self.current_treeview34.item(selected_item)
            if item not in items:
                items.append(item)
        
        self.copy_ranges = []
        
        copy_range = [0,0]
        for item in items:
            values = item['values']
            start_line = values[0]
            end_line = values[1]
            if start_line not in range(copy_range[0], copy_range[1]) and end_line not in range(copy_range[0], copy_range[1]):
                copy_range = [start_line, end_line]
                self.copy_ranges.append(lines_py[start_line-1: end_line])
        
    def paste_bin(self):
        filepath = self.current_bin_analyze
        lines_py = self.current_lines_py
        items = []
        for selected_item in self.current_treeview34.selection():
            item = self.current_treeview34.item(selected_item)
            if item not in items:
                items.append(item)
        
        offset = 0
        for select in self.select_range:
            start_line = select[0]
            end_line = select[1]
            for copy in self.copy_ranges:
                copy_space = len(copy[0].split("    "))
                for i in range(end_line + offset, start_line-1 + offset, -1):
                    if len(lines_py[i + offset].split("    ")) == copy_space and "}" in lines_py[i + offset]:
                        for line in copy:
                            lines_py.insert(i + 1 + offset, line)
                            offset += 1
                        break

        save(filepath, lines_py)
        self.memory_treeview34(self.current_treeview34)
        self.bin_analyze(filepath,self.current_treeview34)
    
    def change_path_bin(self):
        self.list_paths = []
        
        filepath = self.current_bin_analyze
        lines_py = self.current_lines_py
        case1 = [".skl", ".skn", ".scb", ".sco", ".dds"]
        for select in self.select_range:
            start_line = select[0]
            end_line = select[1]
            for no, line in enumerate(lines_py[start_line-1: end_line]):
                if any(i for i in case1 if i.lower() in line.lower()):
                    if "=" in line:
                        shortpath = line.split("=")[-1].replace("\n", "").strip()
                    else:
                        shortpath = line.replace("\n", "").strip()
                    name = "/" + os.path.basename(shortpath.replace('"',"").strip())
                    if shortpath.replace(name, "").replace('"', "") not in self.list_paths:
                        self.list_paths.append(shortpath.replace(name, "").replace('"', ""))
        
        self.textbox2.delete("0.0", "end")
        self.textbox2.insert(tkinter.END, self.current_bin_analyze+"\n\n", "white")
        if self.list_paths:
            for path in self.list_paths:
                self.add_button_textbox2(path)
                
        self.range_change_path_bin = self.select_range
        self.file_change_path_bin = self.current_bin_analyze

    
    def add_button_textbox2(self, path):
        entry = customtkinter.CTkEntry(self.textbox2, width=400)
        entry.insert(tkinter.END, path)
        button = customtkinter.CTkButton(self.textbox2, text="change", width=0, command=lambda: self.accept_change_path_bin(path, entry))
        self.textbox2.window_create(tkinter.END, window = button)
        self.textbox2.insert(tkinter.END, "  ", "white")
        self.textbox2.window_create(tkinter.END, window = entry)
        self.textbox2.insert(tkinter.END, "\n\n", "white")
    
    def accept_change_path_bin(self, path, entry):
        lines_py = read_py(self.file_change_path_bin)
        new_path = entry.get()
        case1 = [".skl", ".skn", ".scb", ".sco", ".dds"]
        for select in self.range_change_path_bin:
            start_line = select[0]
            end_line = select[1]
            for no, line in enumerate(lines_py[start_line-1: end_line]):
                if any(i for i in case1 if i.lower() in line.lower()):
                    if path.lower() in line.lower():
                        lines_py[no+start_line-1] = lines_py[no+start_line-1].replace(path, new_path)
        
        save(self.file_change_path_bin, lines_py)
        self.memory_treeview34(self.current_treeview34)
        self.bin_analyze(self.file_change_path_bin, self.current_treeview34)
                
    
    def edit_bin(self):
        selected_item = self.current_treeview34.selection()[0]
        self.no_edit_bin = self.current_treeview34.item(selected_item)['values'][0]
        line = self.current_lines_py[self.no_edit_bin-1]
        
        self.rename_entry_bin.delete(0, tkinter.END)
        self.rename_entry_bin.place(relx = 0, rely = 0, relwidth=0.5, relheight=0.15)
        self.rename_entry_bin.lift()
        self.rename_entry_bin.insert(tkinter.END, line)

    def accept_edit_bin(self):
        filepath = self.current_bin_analyze
        lines_py = self.current_lines_py
        
        lines_py[self.no_edit_bin-1] = self.rename_entry_bin.get()
        self.rename_entry_bin.place_forget()

        save(filepath, lines_py)
        self.memory_treeview34(self.current_treeview34)
        self.bin_analyze(filepath,self.current_treeview34)
    
    def filter_bin(self):
        pass
    
    # ON CLICK
    def on_click(self, treeview):
        if treeview == self.treeview:
            self.current_treeview12 = self.treeview
            #self.bt_switch_preview.pack(side=tkinter.LEFT, padx=(5,15), pady=0)
            #self.bt_switch_preview2.pack_forget()
        if treeview == self.treeview2:
            self.current_treeview12 = self.treeview2
            #self.bt_switch_preview2.pack(side=tkinter.LEFT, padx=(5,15), pady=0)
            #self.bt_switch_preview.pack_forget()
        self.selected_folders = []
        self.selected_files = []

        for selected_item in treeview.selection():
            item = treeview.item(selected_item)
            path = item['values'][0]
            try:
                self.current_project = path.split('Projects/')[1].split('/')[0]
            except:
                pass
            if os.path.isdir(path):
                self.selected_folders.append(path)
            else:
                self.selected_files.append(path)
        
        self.forget()
        if self.selected_files:
            self.forget([self.Frame_search_text, self.rename_entry])
        
        self.list_multiple_dss = []
        self.textbox.delete("0.0", "end")
        
        if self.selected_folders:
            self.process_show_multiple()
        if len(self.selected_files) > 0:
            for file in self.selected_files:
                self.show_multiple_dss(file)
    
        self.get_types()
    
    
    # HIDE SHOW BUTTON
    def get_types(self):
        types_dict = ['.troybin', '.bin', '.py', '.tex', '.skl', '.dds', '.json', '.troy', '.DDS', '.inibin', '.ini', '.luaobj', '.lua', '.client']
        types_list = []
        for folder in self.selected_folders:
            for _, __, files in os.walk(folder):
                for file in files:
                    for type in types_dict:
                        if type not in types_list:
                            if type in '.' + file.split('.')[-1]:
                                types_list.append(type)
                    if '.' not in file:
                        types_list.append('.bin')
        
        for file in self.selected_files:
            for type in types_dict:
                if type not in types_list:
                    if type in '.' + file.split('.')[-1]:
                        types_list.append(type)
            if '.' not in os.path.basename(file):
                types_list.append('.bin')
        
        self.hide_button()
        self.show_button(types_list)
    
    def show_button(self, types=[]):
        button_name = []
        if '.troybin' in types:
            button_name.append(".troybin → .troy")
        if '.inibin' in types:
            button_name.append(".inibin → .ini")
        if '.luaobj' in types:
            button_name.append(".luaobj → .lua")
        if '.bin' in types:
            button_name.append(".bin → .py")
        if '.py' in types:
            button_name.append(".py → .bin")
            #button_name.append("update link")
            if len(self.selected_folders) == 0 and len(self.selected_files) == 1:
                button_name.append("bin analyze")
                button_name.append("bin analyze 2")
        if '.json' in types:
            if len(self.selected_folders) == 0 and len(self.selected_files) == 1:
                button_name.append("edit")
        if '.troy' in types and '.troybin' not in types:
            if len(self.selected_folders) == 0 and len(self.selected_files) == 1:
                button_name.append("edit")
                button_name.append("write troy to bin")
        if '.ini' in types:
            if len(self.selected_folders) == 0 and len(self.selected_files) == 1:
                pass
        if '.client' in types:
            button_name.append("extract .client")
        if len(self.selected_folders) == 1 and self.selected_folders[0].split('.')[-1] == 'wad':
                button_name.append("wad make")
        if '.tex' in types:
            button_name.append(".tex → .dds")
        if '.skl' in types:
            button_name.append("update .skl")
        if '.dds' in types or '.DDS' in types:
            button_name.append(".dds → .tex")
            button_name.append("change color")

        if len(self.selected_files) > 1 and not self.selected_folders:
            #button_name.append("bulk rename")
            pass
        
        for bt in self.list_top_left_bt:
            if bt.cget('text') in button_name:
                bt.pack(side=tkinter.LEFT, padx=(0,5), pady=0)
    
    def hide_button(self, button_name=""):
        if button_name == "":
            for bt in self.list_top_right_bt:
                bt.pack_forget()
            for bt in self.list_top_left_bt:
                bt.pack_forget()
        elif button_name == "left":
            for bt in self.list_top_left_bt:
                bt.pack_forget()
        elif button_name == "right":
            for bt in self.list_top_right_bt:
                bt.pack_forget()
    
    def process_show_multiple(self):
        d_list = []
        temp_f_list = []
        f_list = []
        ex_list = []
        self.textbox.delete("0.0", "end")
        root = self.selected_folders[0]
        for item in os.listdir(root):
            isdir = os.path.isdir(root + "/" + item)
            if isdir:
                d_list.append(item)
            else:
                extension = item.split('.')[-1]
                if extension not in ex_list:
                    ex_list.append(extension)
                temp_f_list.append(item)
            
        ex_list.sort()
        for ex in ex_list:
            for f in temp_f_list:
                if ex == f.split('.')[-1]:
                    f_list.append(f)
                    
        for d in d_list:
            self.show_multiple_dss(d, isdir=True)
        
        for f in f_list:
            self.show_multiple_dss(root+"/"+f)
        
    def show_file(self, filepath):
        self.hide_button("right")
        self.forget()
        if '.py' in filepath:
            self.show_py(filepath)
        elif '.json' in self.selected_files[0]:
            self.show_json(filepath)
        elif '.troy' in filepath[-5:] or '.ini' in filepath[-4:]:
            self.show_troy(filepath)
    
    
    # RENAME
    def bulk_rename(self):
        pass
    
    def rename(self):
        self.rename_entry.delete(0, tkinter.END)
        if self.selected_files:
            name = os.path.basename(self.selected_files[0])
        if self.selected_folders:
            name = os.path.basename(self.selected_folders[0])
        
        if self.selected_files or self.selected_folders:
            if self.current_treeview12 == self.treeview:
                self.rename_entry.place(relx = 0.1, rely = 0.01, relwidth=0.2, relheight=0.06)
            else:
                self.rename_entry.place(relx = 0.43, rely = 0.01, relwidth=0.2, relheight=0.06)
            self.rename_entry.insert(tkinter.END, name)
    
    def accept_rename(self):
        newname = self.rename_entry.get()
        if self.selected_files:
            os.rename(self.selected_files[0], self.selected_files[0].replace(os.path.basename(self.selected_files[0]), newname))
        if self.selected_folders:
            os.rename(self.selected_folders[0], self.selected_folders[0].replace(os.path.basename(self.selected_folders[0]), newname))
        self.rename_entry.place_forget()
        self.memory_treeview12()
        self.reset_treeview()

    
    # FORGET TEXTBOX AND ENTRY
    def forget(self, widget=[]):
        if not widget:
            self.textbox.delete("0.0", "end")
            self.Frame_search_text.place_forget()
            self.textbox.tag_remove('found', '1.0', tkinter.END)
            self.textbox.tag_remove('found_focus', '1.0', tkinter.END)
        else:
            for w in widget:
                if w == self.textbox:
                    self.textbox.delete("0.0", "end")
                elif w == self.Frame_search_text:
                    self.Frame_search_text.place_forget()
                    self.textbox.tag_remove('found', '1.0', tkinter.END)
                    self.textbox.tag_remove('found_focus', '1.0', tkinter.END)
                elif w == self.rename_entry:
                    self.rename_entry.place_forget()
                elif w == self.rename_entry_bin:
                    self.rename_entry_bin.place_forget()
                    
    
    # CREATE TREEVIEW 
    def get_all_children(self, tree, item=""):
        children = tree.get_children(item)
        for child in children:
            children += self.get_all_children(tree, child)
        return children
    
    def get_all_selected_children(self, tree):
        items = []
        for selected_item in tree.selection():
            if selected_item not in items:
                items.append(selected_item)
            for vfx_item in self.get_all_children(tree, selected_item):
                if vfx_item not in items:
                    items.append(vfx_item)
        
        return items
    
    def insert_treeview(self, parent, path, treeview):
        d_list = []
        temp_f_list = []
        f_list = []
        ex_list = []
        for p in os.listdir(path):
            abspath = os.path.join(path, p)
            isdir = os.path.isdir(abspath)
            if isdir:
                d_list.append(p)
            else:
                extension = p.split('.')[-1]
                if extension not in ex_list:
                    ex_list.append(extension)
                temp_f_list.append(p)
        
        ex_list.sort()
        for ex in ex_list:
            for f in temp_f_list:
                if ex == f.split('.')[-1]:
                    f_list.append(f)
        
        for d in d_list:
            abspath = os.path.join(path, d)
            value = [abspath.replace('\\', '/')]
            value.append(parent)
            oid = treeview.insert(parent, 'end', text="  "+d, open=False, values=value, image=self.folder_icon)
            self.insert_treeview(oid, abspath, treeview)
        
        for f in f_list:
            check = False
            image = self.file_icon
            if any(i for i in self.code_extensions if i in f):
                image = self.code_icon
            elif any(i for i in self.py_extensions if i in f):
                image = self.py_icon
            elif any(i for i in self.image_extensions if i in f) and '.tex' not in f:
                image = self.image_icon
                if self.bt_switch_preview.get() and treeview == self.treeview or self.bt_switch_preview2.get() and treeview == self.treeview2:
                    image = Image.open(path+"/"+f)
                    if self.channel == "RGB":
                        image = numpy.array(image)
                        image = image[:,:,:3]
                        image = Image.fromarray(image)
                    width, height = image.size
                    scale = width / height
                    image = image.resize((math.ceil(15*scale), 15))
                    image = ImageTk.PhotoImage(image)
                    self.list_treeview_images.append(image)
                    check = True
            elif any(i for i in self.skl_extensions if i in f):
                image = self.skl_icon
            elif any(i for i in self.object_extensions if i in f):
                image = self.object_icon
            elif any(i for i in self.anm_extensions if i in f):
                image = self.anm_icon
            elif any(i for i in self.audio_extensions if i in f):
                image = self.audio_icon
                
            abspath = os.path.join(path, f)
            value = [abspath.replace('\\', '/')]
            if check:
                oid = treeview.insert(parent, 'end', text="  "+f, open=False, values=value, image=self.list_treeview_images[-1])
            else:
                oid = treeview.insert(parent, 'end', text="  "+f, open=False, values=value, image=image)
          
    def create_treeview(self):
        for item in self.treeview.get_children():
            self.treeview.delete(item)
        abspath = os.path.abspath('Projects/')
        root_node = self.treeview.insert('', 'end', text="  "+'Projects', open=True, values=[abspath.replace('\\', '/')], image=self.folder_icon)
        self.insert_treeview(root_node, abspath, self.treeview)
    
    def create_treeview2(self):
        for item in self.treeview2.get_children():
            self.treeview2.delete(item)
        abspath = os.path.abspath('Projects/')
        root_node = self.treeview2.insert('', 'end', text="  "+'Projects', open=True, values=[abspath.replace('\\', '/')], image=self.folder_icon)
        self.insert_treeview(root_node, abspath, self.treeview2)
    
    
    # PROJECT FUNCTIONS
    def import_file(self):
        modpath = filedialog.askopenfilename(title="Select .zip/.fantome",)
        if modpath != "":
            try:
                extract_file(modpath)
            except:
                pass
            
        self.memory_treeview12()
        self.reset_treeview()
    
    def import_folder(self):
        modpath = filedialog.askdirectory()
        if modpath != "":
            try:
                extract_folder(modpath)
            except:
                pass
            
        self.memory_treeview12()
        self.reset_treeview()
    
    def finish(self):
        for root,dirs,files in os.walk('Projects/'+self.current_project):
            for file in files:
                if ".py" in file:
                    ritobin(root + '/' + file)
            
        for root,dirs,files in os.walk('Projects/'+self.current_project):
            for dir in dirs:
                if ".wad" in dir and ".client" not in dir:
                    wad_make(root + '/' + dir)
        
        if not os.path.exists('Outputs'):
            os.mkdir('Outputs')
        with ZipFile('Outputs/' + self.current_project + ".zip", 'w') as zObject2:
            zObject2.write('Projects/'+self.current_project+'/WAD', 'WAD')
            zObject2.write('Projects/'+self.current_project+'/META', 'META')
            for root,dirs,files in os.walk('Projects/'+self.current_project+'/WAD'):
                for file in files:
                    if '.wad.client' in file:       
                        zObject2.write(root + '/' + file, 'WAD/'+ file)
            for root,dirs,files in os.walk('Projects/'+self.current_project+'/META'):
                for file in files:
                    if '.json' in file:       
                        zObject2.write(root + '/' + file, 'META/'+ file)
    
    def add_to_LCS(self):
        for root,dirs,files in os.walk('Projects/'+self.current_project):
            for file in files:
                if ".py" in file:
                    ritobin(root + '/' + file)
            
        for root,dirs,files in os.walk('Projects/'+self.current_project):
            for dir in dirs:
                if ".wad" in dir and ".client" not in dir:
                    wad_make(root + '/' + dir)
        
        if os.path.exists(self.LCS_location + '/' + self.current_project):
            shutil.rmtree(self.LCS_location + '/' + self.current_project)
            
        os.makedirs(self.LCS_location + '/' + self.current_project)
        os.makedirs(self.LCS_location + '/' + self.current_project + '/WAD')
        os.makedirs(self.LCS_location + '/' + self.current_project + '/META')

        shutil.copytree('Projects/'+self.current_project+'/META', self.LCS_location + '/' + self.current_project + '/META', dirs_exist_ok = True)
        for root,dirs,files in os.walk('Projects/'+self.current_project+'/WAD'):
            for file in files:
                if '.wad.client' in file:
                    shutil.copyfile(root + '/' + file, self.LCS_location + '/' + self.current_project + '/WAD/' + file)
        
        self.memory_treeview12()
        self.reset_treeview()

    
    def change_LCS_location(self):
        LCS_location = filedialog.askopenfilename(title="Select cslol-manager.exe",)
        if LCS_location != "":
            self.LCS_location = LCS_location
            fp = open("path.txt", 'w')
            fp.write(self.LCS_location)
            fp.close()
    

    # OPEN ALL TREEVIEW
    def open_all(self, treeview):
        if treeview == self.treeview:
            self.open = not self.open
            op = self.open
            all_item = self.get_all_children(treeview)
            for it in all_item:
                if it != all_item[0]:
                    treeview.item(it, open=op)
        elif treeview == self.treeview2:
            self.open2 = not self.open2
            op = self.open2
            all_item = self.get_all_children(treeview)
            for it in all_item:
                if it != all_item[0]:
                    treeview.item(it, open=op)
        elif treeview == self.treeview3:
            self.open3 = not self.open3
            op = self.open3
            all_item = self.get_all_children(treeview)
            for it in all_item:
                if it != all_item[0]:
                    treeview.item(it, open=op)
            self.on_click34(self.treeview3)
        else:
            self.open4 = not self.open4
            op = self.open4
            all_item = self.get_all_children(treeview)
            for it in all_item:
                if it != all_item[0]:
                    treeview.item(it, open=op)
            self.on_click34(self.treeview4)
    
    
    # RESET TREEVIEW
    def memory_treeview12(self):
        for selected_item in self.get_all_children(self.treeview):
            item = self.treeview.item(selected_item)
            path = item['values'][0]
            if item['open']:
                self.memory_open1.append(path)
        
        for selected_item in self.get_all_children(self.treeview2):
            item = self.treeview2.item(selected_item)
            path = item['values'][0]
            if item['open']:
                self.memory_open2.append(path)
    
    def memory_treeview34(self, treeview):
        if treeview == self.treeview3:
            self.memory_open3 = []
            for selected_item in self.get_all_children(treeview):
                item = treeview.item(selected_item)
                line = item['values'][0]
                if item['open']:
                    self.memory_open3.append(line)
        else:
            self.memory_open4 = []
            for selected_item in self.get_all_children(treeview):
                item = treeview.item(selected_item)
                line = item['values'][0]
                if item['open']:
                    self.memory_open4.append(line)
                
                
    def reset_treeview34(self, treeview):
        if treeview == self.treeview3:
            for selected_item in self.get_all_children(treeview):
                item = treeview.item(selected_item)
                line = item['values'][0]
                if line in self.memory_open3:
                    treeview.item(selected_item, open=True)
        else:
            for selected_item in self.get_all_children(treeview):
                item = treeview.item(selected_item)
                line = item['values'][0]
                if line in self.memory_open4:
                    treeview.item(selected_item, open=True)
    
    def reset_treeview(self):
        self.selected_folders = []
        self.selected_files = []
        self.hide_button()
        self.list_treeview_images = []
        self.create_treeview()
        all_item = self.get_all_children(self.treeview)
        for it in all_item:
            item = self.treeview.item(it)
            path = item['values'][0]
            if path in self.memory_open1:
                self.treeview.item(it, open=True)
                
        self.list_treeview_images2 = []
        self.create_treeview2()
        all_item = self.get_all_children(self.treeview2)
        for it in all_item:
            item = self.treeview2.item(it)
            path = item['values'][0]
            if path in self.memory_open2:
                self.treeview2.item(it, open=True)
    
    
    # COPY PASTE FILES/FOLDERS
    def copy(self):
        self.copy_files = self.selected_files.copy()
        self.copy_folders = self.selected_folders.copy()
        self.copy_tab = self.current_project
    
    def paste(self):
        for root, dirs, files in os.walk('Projects/' + self.current_project):
            for dir in dirs:
                if ".wad" in dir:
                    rootdir = root+"/"+dir
                    break
        
        for folder in self.copy_folders:
            dstfol = rootdir + "/" + folder.split(".wad/")[-1]
            shutil.copytree(folder, dstfol, dirs_exist_ok = True)
            
        
        for file in self.copy_files:
            dstfile = rootdir + "/" + file.split(".wad/")[-1]
            dstfile_fol = dstfile.replace(os.path.basename(dstfile), "")
            
            if not os.path.exists(dstfile_fol):
                os.makedirs(dstfile_fol)
            shutil.copyfile(file, dstfile)
        
        self.memory_treeview12()
        self.reset_treeview()
    
    def paste2(self):
        for folder in self.selected_folders:
            for folder2 in self.copy_folders:
                shutil.copytree(folder2, folder + '/' + os.path.basename(folder2), dirs_exist_ok = True)
            for file in self.copy_files:
                shutil.copyfile(file, folder + '/' + os.path.basename(file))
        
        self.memory_treeview12()
        self.reset_treeview()
    
    def delete(self):
        for folder in self.selected_folders:
            if "Projects" not in os.path.basename(folder):
                try:
                    shutil.rmtree(folder)
                except:
                    pass
        for file in self.selected_files:
            try:
                os.remove(file)
            except:
                pass
        
        self.memory_treeview12()
        self.reset_treeview()      
    
    
    # SAVE FILE
    def save(self, filepath):
        self.last_textbox_content = self.textbox.get("0.0", tkinter.END)
        save(filepath, self.last_textbox_content)
        self.bt_save.pack_forget()
    
    def text_edited(self):
        if self.selected_files:
            if any(i for i in ['.py', '.json', '.troy', '.ini'] if i in self.selected_files[0]):
                if self.textbox.get("0.0", tkinter.END) != self.last_textbox_content:
                    self.bt_save.pack(side=tkinter.LEFT, padx=(0,5), pady=0)
                    if '.py' in self.selected_files[0]:
                        lines = [x+"\n" for x in self.textbox.get("0.0", tkinter.END).split("\n")]
                        #threading.Thread(target=self.format_py, args=(lines,)).run()
                    elif '.json' in self.selected_files[0]:
                        lines = [x+"\n" for x in self.textbox.get("0.0", tkinter.END).split("\n")]
                        self.format_json(lines)
                    elif '.troy' in self.selected_files[0]:
                        lines = [x+"\n" for x in self.textbox.get("0.0", tkinter.END).split("\n")]
                        self.format_troy(lines)
                else:
                    self.bt_save.pack_forget()
        self.find_text()
    
    
    # SHOW FILE
    def show_multiple_dss(self, filepath, isdir = False):
        if ".dds" in filepath:
            image = Image.open(filepath)
            if self.channel == "RGB":
                image = numpy.array(image)
                image = image[:,:,:3]
                image = Image.fromarray(image)
            width, height = image.size
            scale = width / height
            image = image.resize((75, math.ceil(75/scale)))
            image = ImageTk.PhotoImage(image)
            self.list_multiple_dss.append(image)
            self.textbox.image_create(tkinter.END, image=self.list_multiple_dss[-1])
            self.textbox.insert(tkinter.END, "    " + os.path.basename(filepath), 'white')
            self.textbox.insert(tkinter.END, f" ({width}x{height})\n\n", 'orange')
        else:
            if isdir:
                image = self.folder_icon
                self.list_multiple_dss.append(image)
                self.textbox.image_create(tkinter.END, image=self.list_multiple_dss[-1])
                self.textbox.insert(tkinter.END, "  " + os.path.basename(filepath) + "\n\n", 'white')
            else:
                f_list = [filepath]
                for f in f_list:
                    image = self.file_icon
                    if any(i for i in self.code_extensions if i in f):
                        image = self.code_icon
                    elif any(i for i in self.py_extensions if i in f):
                        image = self.py_icon
                    elif any(i for i in self.image_extensions if i in f):
                        image = self.image_icon
                    elif any(i for i in self.skl_extensions if i in f):
                        image = self.skl_icon
                    elif any(i for i in self.object_extensions if i in f):
                        image = self.object_icon
                    elif any(i for i in self.anm_extensions if i in f):
                        image = self.anm_icon
                    elif any(i for i in self.audio_extensions if i in f):
                        image = self.audio_icon
                    
                    self.textbox.image_create(tkinter.END, image=image)
                    self.textbox.insert(tkinter.END, "  " + os.path.basename(filepath) + "\n\n", 'white')
    
    def show(self, filepath):
        lines = read(filepath)
        for line in lines:
            self.textbox.insert(tkinter.END, line, 'white')
    
    def show_troy(self, filepath):
        lines_troy = read_troy(filepath)
        for line in lines_troy:
            contents = line.split("=")
            self.format_troy(contents)
        self.last_textbox_content = self.textbox.get("0.0", tkinter.END)
    
    def show_json(self, filepath):
        lines_json = read_json(filepath)
        for line in lines_json:
            self.textbox.insert(tkinter.END, line, 'white')
        self.last_textbox_content = self.textbox.get("0.0", tkinter.END)
        self.format_json(lines_json)
        
    def show_py(self, filepath):
        lines_py = read(filepath)
        for line in lines_py:
            self.textbox.insert(tkinter.END, line, "white")
        threading.Thread(target=self.format_py, args=(lines_py,)).run()
    
    def format_py(self, lines):
        self.textbox2.tag_remove('blue', '1.0', tkinter.END)
        self.textbox2.tag_remove('number', '1.0', tkinter.END)
        self.textbox2.tag_remove('orange', '1.0', tkinter.END)
        self.textbox2.tag_remove('green', '1.0', tkinter.END)
        self.textbox2.tag_add('white', '1.0', tkinter.END)
        i = 0
        for line in lines:
            index = f"{i+1}.0"
            last_index = '%s+%dc' % (index, len(line))
            
            # BLUE
            index_blue = self.textbox2.search(":", index, nocase=1, stopindex=last_index)
            if index_blue:
                last_index_blue = self.textbox2.search("=", index_blue, nocase=1, stopindex=last_index)
                if last_index_blue:
                    self.textbox2.tag_remove('white', index_blue + "+1c", last_index_blue + "-1c")
                    self.textbox2.tag_add('blue', index_blue + "+1c", last_index_blue + "-1c")
            
            # GREEN
            index_green = self.textbox2.search("=", index, nocase=1, stopindex=last_index)
            if index_green:
                last_index_green = self.textbox2.search("\n", index_green, nocase=1, stopindex=last_index)
                if last_index_green:
                    self.textbox2.tag_remove('white', index_green + "+1c", last_index_green)
                    self.textbox2.tag_add('green', index_green + "+1c", last_index_green)
            
            # NUMBER
            index_number = self.textbox2.search('{', index, nocase=1, stopindex=last_index)
            if index_number:
                last_index_number = self.textbox2.search('}', index_number, nocase=1, stopindex=last_index)
                if last_index_number:
                    self.textbox2.tag_remove('green', index_number + "+1c", last_index_number + "-1c")
                    self.textbox2.tag_remove('white', index_number + "+1c", last_index_number + "-1c")
                    self.textbox2.tag_add('number', index_number + "+1c", last_index_number + "-1c")
            
            if is_float(line.strip()):
                self.textbox2.tag_remove('green', index, last_index)
                self.textbox2.tag_remove('white', index, last_index)
                self.textbox2.tag_add('number', index, last_index)
            
            index_number = self.textbox2.search('=', index, nocase=1, stopindex=last_index)
            if index_number:
                last_index_number = self.textbox2.search('\n', index_number, nocase=1, stopindex=last_index)
                if last_index_number and is_float(self.textbox2.get(index_number + "+1c", last_index_number).strip()):
                    self.textbox2.tag_remove('green', index_number + "+1c", last_index_number)
                    self.textbox2.tag_remove('white', index_number + "+1c", last_index_number)
                    self.textbox2.tag_add('number', index_number + "+1c", last_index_number)
            
            # GREEN
            index_green = self.textbox2.search("=", index, nocase=1, stopindex=last_index)
            if index_green:
                last_index_green = self.textbox2.search("{", index_green, nocase=1, stopindex=last_index)
                if last_index_green:
                    self.textbox2.tag_remove('number', index_green + "+1c", last_index_green + "-1c")
                    self.textbox2.tag_remove('white', index_green + "+1c", last_index_green + "-1c")
                    self.textbox2.tag_add('green', index_green + "+1c", last_index_green + "-1c")
            
            index_green = self.textbox2.search("#", index, nocase=1, stopindex=last_index)
            if index_green:
                last_index_green = self.textbox2.search("\n", index_green, nocase=1, stopindex=last_index)
                if last_index_green:
                    self.textbox2.tag_remove('number', index_green, last_index_green)
                    self.textbox2.tag_remove('white', index_green, last_index_green)
                    self.textbox2.tag_add('green', index_green, last_index_green)
            
            # ORANGE
            index_orange = self.textbox2.search('"', index, nocase=1, stopindex=last_index)
            if index_orange:
                last_index_orange = self.textbox2.search('"', index_orange + "+1c", nocase=1, stopindex=last_index)
                if last_index_orange:
                    self.textbox2.tag_remove('white', index_orange, last_index_orange + "+1c")
                    self.textbox2.tag_remove('number', index_orange, last_index_orange + "+1c")
                    self.textbox2.tag_add('orange', index_orange, last_index_orange + "+1c")
            
            # TRUE FALSE
            index_blue = self.textbox2.search(" true", index, nocase=1, stopindex=last_index)
            if index_blue:
                last_index_blue = '%s+%dc' % (index_blue, len(" true"))
                self.textbox2.tag_remove('green', index_blue, last_index_blue)
                self.textbox2.tag_remove('white', index_blue, last_index_blue)
                self.textbox2.tag_remove('number', index_blue, last_index_blue)
                self.textbox2.tag_add('blue', index_blue, last_index_blue)
            
            index_blue = self.textbox2.search(" false", index, nocase=1, stopindex=last_index)
            if index_blue:
                last_index_blue = '%s+%dc' % (index_blue, len(" false"))
                self.textbox2.tag_remove('green', index_blue, last_index_blue)
                self.textbox2.tag_remove('white', index_blue, last_index_blue)
                self.textbox2.tag_remove('number', index_blue, last_index_blue)
                self.textbox2.tag_add('blue', index_blue, last_index_blue)
            
            # WHITE
            index_white = self.textbox2.search("[", index, nocase=1, stopindex=last_index)
            if index_white:
                last_index_white = '%s+%dc' % (index_white, len("["))
                self.textbox2.tag_remove('blue', index_white, last_index_white)
                self.textbox2.tag_add('white', index_white, last_index_white)
            
            index_white = self.textbox2.search("]", index, nocase=1, stopindex=last_index)
            if index_white:
                last_index_white = '%s+%dc' % (index_white, len("]"))
                self.textbox2.tag_remove('blue', index_white, last_index_white)
                self.textbox2.tag_add('white', index_white, last_index_white)
            
            index_white = self.textbox2.search("{", index, nocase=1, stopindex=last_index)
            if index_white:
                last_index_white = '%s+%dc' % (index_white, len("{"))
                self.textbox2.tag_remove('blue', index_white, last_index_white)
                self.textbox2.tag_add('white', index_white, last_index_white)
            
            index_white = self.textbox2.search("}", index, nocase=1, stopindex=last_index)
            if index_white:
                last_index_white = '%s+%dc' % (index_white, len("}"))
                self.textbox2.tag_remove('blue', index_white, last_index_white)
                self.textbox2.tag_add('white', index_white, last_index_white)
            
            index_white = self.textbox.search(",", index, nocase=1, stopindex=last_index)
            if index_white:
                last_index_white = '%s+%dc' % (index_white, len(","))
                self.textbox2.tag_remove('blue', index_white, last_index_white)
                self.textbox2.tag_add('white', index_white, last_index_white)
            
            i += 1
    
    def format_json(self, lines):
        self.textbox.tag_remove('blue', '1.0', tkinter.END)
        self.textbox.tag_remove('number', '1.0', tkinter.END)
        self.textbox.tag_remove('orange', '1.0', tkinter.END)
        self.textbox.tag_remove('green', '1.0', tkinter.END)
        self.textbox.tag_add('white', '1.0', tkinter.END)
        i = 0
        for line in lines:
            index = f"{i+1}.0"
            last_index = '%s+%dc' % (index, len(line))
            
            # BLUE VS
            index_blue = self.textbox.search('"', index, nocase=1, stopindex=last_index)
            if index_blue:
                last_index_blue = self.textbox.search(":", index_blue, nocase=1, stopindex=last_index)
                if last_index_blue:
                    self.textbox.tag_remove('white', index_blue, last_index_blue)
                    self.textbox.tag_add('blue vs', index_blue, last_index_blue)
            
            # GREEN
            index_green = self.textbox.search("=", index, nocase=1, stopindex=last_index)
            if index_green:
                last_index_green = self.textbox.search("\n", index_green, nocase=1, stopindex=last_index)
                if last_index_green:
                    self.textbox.tag_remove('white', index_green + "+1c", last_index_green)
                    self.textbox.tag_add('green', index_green + "+1c", last_index_green)
            
            # NUMBER
            index_number = self.textbox.search(':', index, nocase=1, stopindex=last_index)
            if index_number:
                last_index_number = self.textbox.search(',', index_number, nocase=1, stopindex=last_index)
                if last_index_number and is_float(self.textbox.get(index_number, last_index_number).strip()):
                    self.textbox.tag_remove('green', index_number + "+1c", last_index_number)
                    self.textbox.tag_remove('white', index_number + "+1c", last_index_number)
                    self.textbox.tag_add('number', index_number + "+1c", last_index_number)
            
            # GREEN

            
            # ORANGE
            index_orange = self.textbox.search(':', index, nocase=1, stopindex=last_index)
            if index_orange:
                last_index_orange = self.textbox.search('\n', index_orange + "+1c", nocase=1, stopindex=last_index)
                if last_index_orange:
                    self.textbox.tag_remove('white', index_orange + "+1c", last_index_orange)
                    self.textbox.tag_remove('number', index_orange + "+1c", last_index_orange)
                    self.textbox.tag_add('orange', index_orange + "+1c", last_index_orange)
            
            # TRUE FALSE
            index_blue = self.textbox.search(" true", index, nocase=1, stopindex=last_index)
            if index_blue:
                last_index_blue = '%s+%dc' % (index_blue, len(" true"))
                self.textbox.tag_remove('white', index_blue, last_index_blue)
                self.textbox.tag_remove('number', index_blue, last_index_blue)
                self.textbox.tag_add('blue', index_blue, last_index_blue)
            
            index_blue = self.textbox.search(" false", index, nocase=1, stopindex=last_index)
            if index_blue:
                last_index_blue = '%s+%dc' % (index_blue, len(" false"))
                self.textbox.tag_remove('white', index_blue, last_index_blue)
                self.textbox.tag_remove('number', index_blue, last_index_blue)
                self.textbox.tag_add('blue', index_blue, last_index_blue)
            
            # YELLOW
            index_yellow = self.textbox.search("{", index, nocase=1, stopindex=last_index)
            if index_yellow:
                last_index_yellow = '%s+%dc' % (index_yellow, len("{"))
                self.textbox.tag_remove('white', index_yellow, last_index_yellow)
                self.textbox.tag_add('yellow', index_yellow, last_index_yellow)
            
            index_yellow = self.textbox.search("}", index, nocase=1, stopindex=last_index)
            if index_yellow:
                last_index_yellow = '%s+%dc' % (index_yellow, len("}"))
                self.textbox.tag_remove('white', index_yellow, last_index_yellow)
                self.textbox.tag_add('yellow', index_yellow, last_index_yellow)
            
            
            # WHITE
            index_white = self.textbox.search(",", index, nocase=1, stopindex=last_index)
            if index_white:
                last_index_white = '%s+%dc' % (index_white, len(","))
                self.textbox.tag_remove('blue', index_white, last_index_white)
                self.textbox.tag_add('white', index_white, last_index_white)
            
            i += 1
    
    def format_troy(self, contents):
        for i, ct in enumerate(contents):
            if '[' in ct:
                self.textbox.insert(tkinter.END, ct, 'orange')
            elif i == 0 and "\n" not in ct:
                self.textbox.insert(tkinter.END, ct + "=", 'blue')
            else:
                if '"' in ct:
                    self.textbox.insert(tkinter.END, ct, 'orange')
                else:
                    ct = ct.split(" ")
                    for c in ct:
                        if is_float(c):
                            if "\n" not in c:
                                self.textbox.insert(tkinter.END, c+" ", 'number')
                            else:
                                self.textbox.insert(tkinter.END, c, 'number')
                        else:
                            if "\n" not in c:
                                self.textbox.insert(tkinter.END, c+" ", 'red')
                            else:
                                self.textbox.insert(tkinter.END, c, 'red')
    
    
    # CONVERT
    def convert_tex(self):
        items = self.get_all_selected_children(self.current_treeview12)
        for it in items:
            item = self.current_treeview12.item(it)
            values = item['values']
            tex2dds(values[-1])
        self.memory_treeview12()
        self.reset_treeview()           
    
    def extract_client(self):
        items = self.get_all_selected_children(self.current_treeview12)
        for it in items:
            item = self.current_treeview12.item(it)
            values = item['values']
            wad_extract(values[-1])
        self.memory_treeview12()
        self.reset_treeview()
    
    def convert_troybin(self):
        items = self.get_all_selected_children(self.current_treeview12)
        for it in items:
            item = self.current_treeview12.item(it)
            values = item['values']
            troybin2troy(values[-1])
        self.memory_treeview12()
        self.reset_treeview()
    
    def convert_inibin(self):
        items = self.get_all_selected_children(self.current_treeview12)
        for it in items:
            item = self.current_treeview12.item(it)
            values = item['values']
            inibin2ini(values[-1])
        self.memory_treeview12()
        self.reset_treeview()
    
    def convert_luaobj(self):
        items = self.get_all_selected_children(self.current_treeview12)
        for it in items:
            item = self.current_treeview12.item(it)
            values = item['values']
            luaobj2lua(values[-1])
        self.memory_treeview12()
        self.reset_treeview()
    
    def convert_bin(self):
        items = self.get_all_selected_children(self.current_treeview12)
        for it in items:
            item = self.current_treeview12.item(it)
            values = item['values']
            ritobin(values[-1])
        self.memory_treeview12()
        self.reset_treeview()
    
    def convert_py(self):
        items = self.get_all_selected_children(self.current_treeview12)
        for it in items:
            item = self.current_treeview12.item(it)
            values = item['values']
            ritobin(values[-1])
        self.memory_treeview12()
        self.reset_treeview()
            
    def convert_obj(self):
        pass
    
    def wad_make(self):
        wad_make(self.selected_folders[0])
        self.memory_treeview12()
        self.reset_treeview()
        
    def update_skl(self):
        items = self.get_all_selected_children(self.current_treeview12)
        
        for it in items:
            item = self.current_treeview12.item(it)
            values = item['values']
            skl_convert(values[-1])

    
    # UPDATE
    def troy_to_bin_one(self, filepath):
        path = "ASSETS" + filepath.split("assets")[-1].replace(os.path.basename(filepath),"").replace("particles", "Particles")
        py_path = filedialog.askopenfilename(title="Select .py")
        if ".py" in py_path:
            lines_py = read_py(py_path)
            vfx = os.path.basename(filepath).split(".")[0]
            vfx = update_vfx_name(vfx)
            lines_troy = read_troy(filepath)
            
            start = 0
            end = 0
            for no, line in enumerate(lines_py):
                if vfx.lower() in line.lower() and "VfxSystemDefinitionData".lower() in line.lower():
                    start = no
                    for no2, line2 in enumerate(lines_py[no+1:]):
                        if "VfxSystemDefinitionData".lower() in line2.lower():
                            end = no + 1 + no2
                            break
                    break
                
            print(vfx)
            print(start, end)
            
            for no, line in enumerate(lines_troy):
                if "[" in line and "]" in line and "system" not in line.lower():
                    emitter = line.strip()[1:-2]
                    for no2, line2 in enumerate(lines_troy[no+1:]):
                        if "p-mesh=" in line2:
                            value = line2.split("=")[-1].replace(".tga", ".scb").replace("\n", "")
                            value = '"' + path + value[1:]
                            lines_py = self.take_change(lines_py, start, end, emitter, "mSimpleMeshName:", value)
                        elif "p-meshtex=" in line2:
                            value = line2.split("=")[-1].replace(".tga", ".dds").replace("\n", "")
                            value = '"' + path + value[1:]
                            lines_py = self.take_change(lines_py, start, end, emitter, " texture:", value)
                        elif "p-rgba=" in line2:
                            value = line2.split("=")[-1].replace(".tga", ".dds").replace("\n", "")
                            value = '"' + path + value[1:]
                            lines_py = self.take_change(lines_py, start, end, emitter, " particleColorTexture:", value)
                        elif "p-texture=" in line2:
                            value = line2.split("=")[-1].replace(".tga", ".dds").replace("\n", "")
                            value = '"' + path + value[1:]
                            lines_py = self.take_change(lines_py, start, end, emitter, " texture:", value)
                        elif "[" in line2 and "]" in line2:
                            break
            save(py_path, lines_py)
                        
    def take_change(self, lines_py, start, end, emitter, type, value):
        if start != 0 and end != 0:
            check = False
            for no, line in enumerate(lines_py[start:end]):
                if emitter in line:
                    check = True
                elif check:
                    if type.lower() in line.lower():
                        old_value = lines_py[no+start].split("=")[-1].replace(" ", "").replace("\n", "")
                        lines_py[no+start] = lines_py[no+start].replace(old_value, value)
                        print(lines_py[no+start])
                    elif "emitterName:".lower() in line.lower():
                        break
        return lines_py
    
    def take_change_vfx(self, lines_py_yours, lines_py_riot, vfx, emitter, type, no_line):
        start = 0
        end = 0
        for no, line in enumerate(lines_py_riot):
            if vfx.lower() in line.lower() and "VfxSystemDefinitionData".lower() in line.lower():
                start = no
                for no2, line2 in enumerate(lines_py_riot[no+1:]):
                    if "VfxSystemDefinitionData".lower() in line2.lower():
                        end = no + 1 + no2
                        break
                break
        if start != 0 and end != 0:
            check = False
            for no, line in enumerate(lines_py_riot[start:end]):
                if emitter in line:
                    check = True
                elif check:
                    if type.lower() in line.lower():
                        correct_value = lines_py_riot[no+start].split("=")[-1].replace(" ", "").replace("\n", "")
                        lines_py_yours[no_line] = lines_py_yours[no_line].replace(lines_py_yours[no_line].split("=")[-1].replace(" ", "").replace("\n", ""), correct_value)
                    elif "emitterName:".lower() in line.lower():
                        break
        return lines_py_yours
    
    def take_change_base(self, lines_py_yours, lines_py_riot, base, type, no_line):
        start = 0
        end = 0
        for no, line in enumerate(lines_py_riot):
            if base.lower() in line.lower() and "SkinCharacterDataProperties".lower() in line.lower():
                start = no
                for no2, line2 in enumerate(lines_py_riot[no+1:]):
                    if "VfxSystemDefinitionData".lower() in line2.lower():
                        end = no + 1 + no2
                        break
                break
        if start != 0 and end != 0:
            for no, line in enumerate(lines_py_riot[start:end]):
                if type == " iconCircle:" or type == " iconSquare:":
                    if type.lower() in line.lower():
                        correct_value = lines_py_riot[no+start+1].split('"')[1]
                        lines_py_yours[no_line] = lines_py_yours[no_line].replace(lines_py_yours[no_line].split('"')[1], correct_value)
                elif type.lower() in line.lower():
                    correct_value = lines_py_riot[no+start].split("=")[-1].replace(" ", "").replace("\n", "")
                    lines_py_yours[no_line] = lines_py_yours[no_line].replace(lines_py_yours[no_line].split("=")[-1].replace(" ", "").replace("\n", ""), correct_value)
        return lines_py_yours
        
    def update_bin(self):
        if self.list_errors:
            self.bin_analyze(self.selected_files[0])

            filepath = self.selected_files[0]
            path_riot = filepath.replace("Yours", "Riot")
            for file in self.selected_files:
                ritobin(file.replace("Yours", "Riot").replace(".py", ".bin"))
            lines_py_riot = read_py(path_riot)
            lines_py_yours = read_py(filepath)

            for i in range(len(self.list_errors)):
                if hasattr(self.list_errors[i], "vfx"):
                    vfx = self.list_errors[i].vfx
                    emitter = self.list_errors[i].emitter
                    type = self.list_errors[i].type
                    no_line = self.list_errors[i].no_line
                    
                    lines_py_yours = self.take_change_vfx(lines_py_yours, lines_py_riot, vfx, emitter, type, no_line)
                else:
                    base = self.list_errors[i].base
                    type = self.list_errors[i].type
                    no_line = self.list_errors[i].no_line
                    
                    lines_py_yours = self.take_change_base(lines_py_yours, lines_py_riot, base, type, no_line)
                
            save(filepath, lines_py_yours)
            self.memory_treeview34(self.current_treeview34)
            self.bin_analyze(filepath)
            
           
a = App()
a.root.mainloop()