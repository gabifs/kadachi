# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 10:05:34 2019

@author: Rinny

LEMBRE DE INSTALAR AS SEGUINTES LIBS:
Pillow
Requests
"""

import tkinter as tk
from tkinter.ttk import Button
import errno
import requests
import gc
from pprint import pprint
from tkinter import ttk
from PIL import Image, ImageTk
from io import BytesIO
from objects import *
import threading
import time
import os


# import mhw_objects


def testprint():
    print("clicked a button")


# noinspection PyCallByClass
class mainWindow:

    def start_delete(self):
        string = str(self.deleteEntry.get())

        removeitem(string,self.db,self.a_list,self.s_list)

        self.reloadfiles()

        self.deleteW.destroy()

    def deleteWindow(self):
        # TODO DELETE WINDOW

        self.deleteW = tk.Toplevel()
        self.deleteW.title("Delete Item")

        self.deleteLabel = ttk.Label(self.deleteW,text="Enter name of item to be deleted\n(names are case sensitive)")
        self.deleteLabel.configure(justify = 'center')
        self.deleteLabel.grid(column=0,row=0,sticky=tk.N)

        self.deleteEntry = tk.Entry(self.deleteW)
        self.deleteEntry.grid(column=0,row=1)

        self.deleteB = ttk.Button(self.deleteW, text = "Confirm", command = lambda: self.start_delete())
        self.deleteB.grid(column=0,row=2,sticky=tk.E)

        self.cancelDel = ttk.Button(self.deleteW, text="Cancel", command=lambda: self.deleteW.destroy())
        self.cancelDel.grid(column=0, row=2, sticky=tk.W)

        for child in self.deleteW.winfo_children(): child.grid_configure(padx=5, pady=5)

        windowWidth = self.deleteW.winfo_reqwidth()
        windowHeight = self.deleteW.winfo_reqheight()
        positionRight = int(self.deleteW.winfo_screenwidth() / 3 - windowWidth / 3)
        positionDown = int(self.deleteW.winfo_screenheight() / 3 - windowHeight / 3)
        self.deleteW.geometry("+{}+{}".format(positionRight, positionDown))

        return

    def reloadfiles(self):
        s_file = open('assets/skill_list.bin', 'rb')
        a_file = open('assets/armor_list.bin', 'rb')
        db_file = open('assets/database.bin', 'rb')

        self.s_list = pickle.load(s_file)
        self.a_list = pickle.load(a_file)
        self.db = pickle.load(db_file)

        s_file.close()
        a_file.close()
        db_file.close()

    def startadd(self):
        # db,armorlist,s_list,itemname,itemdef,itemrank,skillname,skillrank,slot


        itemname = self.nameEntryAdd.get()
        defense = int(self.defEntryAdd.get())
        rank = self.selrankAdd.get().lower()
        skl_name = self.selskillAdd.get()
        skl_rank = int(self.selsrankAdd.get()) - 1
        slot = self.selslotAdd.get().lower()

        additem(self.db, self.a_list,self.s_list,itemname,defense,rank,skl_name,skl_rank,slot)

        self.reloadfiles()

        self.add.destroy()



    def getranks(self, skl_name):

        skl = self.s_list.search_name(skl_name).data

        max_rank = skl.max_lvl

        ranks = []

        for i in range(0,max_rank):
            ranks.append(i+1)

        '''skl = list(filter(lambda oneskl: oneskl["name"] == name, skill))
        ranklist = [sub['ranks'] for sub in skl]
        ranks = []
        if ranklist:
            maxlevel = len(ranklist.pop())

            for i in range(1, maxlevel + 1):
                ranks.append(i)'''

        return ranks

    def rank_refresh(self, skl):

        if skl != 'None':
            self.srankEntryAdd['state'] = "readonly"
            self.srankEntryAdd['values'] = tuple(self.getranks(skl))
            self.srankEntryAdd.current(0)
        else:
            self.srankEntryAdd['state'] = "disabled"
            self.srankEntryAdd['values'] = [None]
            self.srankEntryAdd.current(0)

    def nothing(self):
        pass

    def reenable_buttons(self):

        self.addB['state'] = 'normal'
        self.removeB['state'] = 'normal'
        self.rankEntry['state'] = 'readonly'
        self.skillEntry['state'] = 'readonly'
        self.autocheck['state'] = 'normal'
        self.searchB['state'] = 'normal'
        self.updateB['state'] = 'normal'

        self.itemwindow.destroy()


    def displayitem(self,slot):

        self.addB['state'] = 'disabled'
        self.removeB['state'] = 'disabled'
        self.rankEntry['state'] = 'disabled'
        self.skillEntry['state'] = 'disabled'
        self.autocheck['state'] = 'disabled'
        self.searchB['state'] = 'disabled'
        self.updateB['state'] = 'disabled'

        if slot == 'head':
            self.item = self.player1.head
        elif slot == 'chest':
            self.item = self.player1.chest
        elif slot == 'gloves':
            self.item = self.player1.gloves
        elif slot == 'waist':
            self.item = self.player1.waist
        elif slot == 'legs':
            self.item = self.player1.legs

        self.itemwindow = tk.Toplevel()
        self.itemwindow.title("Item Data")
        #self.itemwindow.attributes('-disabled', True)
        self.itemwindow.overrideredirect(True)
        #self.itemwindow.protocol("WM_DELETE_WINDOW", self.nothing())

        self.dataframe = ttk.Frame(self.itemwindow)

        self.text = tk.Text(self.dataframe, height=14, width=70)
        self.text.pack(side=tk.LEFT, fill=tk.Y)
        self.scroll = ttk.Scrollbar(self.dataframe)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.scroll.config(command=self.text.yview)
        self.text.config(yscrollcommand=self.scroll.set)

        self.dataframe.grid(column=1, row=0, sticky=tk.W)

        self.icoframe = ttk.Frame(self.itemwindow)

        img = self.item.image
        if img is not None:
            try:
                img = Image.open(img).resize((self.IMGSIZE, self.IMGSIZE), Image.ANTIALIAS)
                img = ImageTk.PhotoImage(img)
            except:
                imgname = img
                imgname = imgname[11:]
                url = self.imgurl + imgname
                self.download_image(url, self.img_path)
                img = Image.open(img).resize((self.IMGSIZE, self.IMGSIZE), Image.ANTIALIAS)
                img = ImageTk.PhotoImage(img)

            self.itemICO = ttk.Label(self.icoframe, image=img)
            self.itemICO.grid(column=0, row=0)

        stat = "Item Name: {}\nDefense: {}\nResistances:\n\n   Fire: {}\n   Water: {}\n   Ice: {}\n   Thunder: {}\n   Dragon: {}\n\nSkills:\n".format(
            self.item.name, self.item.defense, self.item.fire_res, self.item.water_res,
            self.item.ice_res, self.item.thunder_res,
            self.item.dragon_res)
        if self.item.skills:
            for i in range(0, len(self.item.skills)):
                temp_skl = self.item.skills[i]
                # print(temp_skl.name)
                temp_str = ''.join(
                    "\nName: {}\nDescription: {}\nLevel: {}\nEffects: {}\nModifiers: {}\n".format(temp_skl.name,
                                                                                                  temp_skl.description,
                                                                                                  temp_skl.level,
                                                                                                  temp_skl.effects,
                                                                                                  temp_skl.modifiers))
                # print(temp_str)
                stat = stat + temp_str

        self.text.config(state=tk.NORMAL)
        self.text.delete(1.0, tk.END)
        self.text.insert(tk.END, stat)
        self.text.config(state=tk.DISABLED)

        self.quitB = ttk.Button(self.itemwindow,text="Exit",command = lambda: self.reenable_buttons())
        self.quitB.grid(column=1,row=1,sticky=tk.E)

        for child in self.itemwindow.winfo_children(): child.grid_propagate(0)
        for child in self.itemwindow.winfo_children(): child.grid_configure(padx=5, pady=5)

        windowWidth = self.itemwindow.winfo_reqwidth()
        windowHeight = self.itemwindow.winfo_reqheight()
        positionRight = int(self.itemwindow.winfo_screenwidth() / 3 - windowWidth / 3)
        positionDown = int(self.itemwindow.winfo_screenheight() / 3 - windowHeight / 3)
        self.itemwindow.geometry("+{}+{}".format(positionRight, positionDown))

    def redraw_player(self):

        # TODO MAKE CHEST AND BELOW DEAL WITH CUSTOM IMAGES

        self.headName.set("None")
        self.headimg = None
        self.chestName.set("None")
        self.chestimg = None
        self.gloveName.set("None")
        self.gloveimg = None
        self.waistName.set("None")
        self.waistimg = None
        self.pantName.set("None")
        self.pantimg = None

        if self.player1.head is not None:
            self.frameHead['cursor'] = 'hand2'
            self.headName.set(self.player1.head.name)
            self.headimg = self.player1.head.image
            self.frameHead.bind("<Button-1>", lambda event: self.displayitem('head'))
            if self.headimg is not None:
                try:
                    self.headimg = Image.open(self.headimg).resize((self.IMGSIZE, self.IMGSIZE), Image.ANTIALIAS)
                    self.headimg = ImageTk.PhotoImage(self.headimg)
                except:
                    self.imgname = self.headimg
                    if self.player1.head.custom is True:
                        self.imgname = self.imgname[11:]
                        self.imgname = self.imgname.replace(".", "/", 2)
                        url = self.customurl + self.imgname
                    else:
                        self.imgname = self.imgname[11:]
                        url = self.imgurl + self.imgname
                    self.download_image(url, self.img_path,self.player1.head.custom)
                    self.headimg = Image.open(self.headimg).resize((self.IMGSIZE, self.IMGSIZE), Image.ANTIALIAS)
                    self.headimg = ImageTk.PhotoImage(self.headimg)

                self.headICO = ttk.Label(self.frameHead, image=self.headimg)
                self.headICO.grid(column=1, row=1)
                self.headICO.bind("<Button-1>", lambda event: self.displayitem('head'))
        else:
            self.frameHead['cursor'] = ''
            self.frameHead.unbind("<Button-1>")

        if self.player1.chest is not None:
            self.frameChest['cursor'] = 'hand2'
            self.chestName.set(self.player1.chest.name)
            self.chestimg = self.player1.chest.image
            self.frameChest.bind("<Button-1>", lambda event: self.displayitem('chest'))
            if self.chestimg is not None:
                try:
                    self.chestimg = Image.open(self.chestimg).resize((self.IMGSIZE, self.IMGSIZE), Image.ANTIALIAS)
                    self.chestimg = ImageTk.PhotoImage(self.chestimg)
                except:
                    self.imgname = self.chestimg
                    self.imgname = self.imgname[11:]
                    url = self.imgurl + self.imgname
                    self.download_image(url, self.img_path)
                    self.chestimg = Image.open(self.chestimg).resize((self.IMGSIZE, self.IMGSIZE), Image.ANTIALIAS)
                    self.chestimg = ImageTk.PhotoImage(self.chestimg)

                self.chestICO = ttk.Label(self.frameChest, image=self.chestimg)
                self.chestICO.grid(column=1, row=1)
                self.chestICO.bind("<Button-1>", lambda event: self.displayitem('chest'))
        else:
            self.frameChest['cursor'] = ''
            self.frameChest.unbind("<Button-1>")

        if self.player1.gloves is not None:
            self.frameGlove['cursor'] = 'hand2'
            self.gloveName.set(self.player1.gloves.name)
            self.gloveimg = self.player1.gloves.image
            self.frameGlove.bind("<Button-1>", lambda event: self.displayitem('gloves'))
            if self.gloveimg is not None:
                try:
                    self.gloveimg = Image.open(self.gloveimg).resize((self.IMGSIZE, self.IMGSIZE), Image.ANTIALIAS)
                    self.gloveimg = ImageTk.PhotoImage(self.gloveimg)
                except:
                    self.imgname = self.gloveimg
                    self.imgname = self.imgname[11:]
                    url = self.imgurl + self.imgname
                    self.download_image(url, self.img_path)
                    self.gloveimg = Image.open(self.gloveimg).resize((self.IMGSIZE, self.IMGSIZE), Image.ANTIALIAS)
                    self.gloveimg = ImageTk.PhotoImage(self.gloveimg)

                self.gloveICO = ttk.Label(self.frameGlove, image=self.gloveimg)
                self.gloveICO.grid(column=1, row=1)
                self.gloveICO.bind("<Button-1>", lambda event: self.displayitem('glove'))
        else:
            self.frameGlove['cursor'] = ''
            self.frameGlove.unbind("<Button-1>")

        if self.player1.waist is not None:
            self.frameWaist['cursor'] = 'hand2'
            self.waistName.set(self.player1.waist.name)
            self.waistimg = self.player1.waist.image
            self.frameWaist.bind("<Button-1>", lambda event: self.displayitem('waist'))
            if self.waistimg is not None:
                try:
                    self.waistimg = Image.open(self.waistimg).resize((self.IMGSIZE, self.IMGSIZE), Image.ANTIALIAS)
                    self.waistimg = ImageTk.PhotoImage(self.waistimg)
                except:
                    self.imgname = self.waistimg
                    self.imgname = self.imgname[11:]
                    url = self.imgurl + self.imgname
                    self.download_image(url, self.img_path)
                    self.waistimg = Image.open(self.waistimg).resize((self.IMGSIZE, self.IMGSIZE), Image.ANTIALIAS)
                    self.waistimg = ImageTk.PhotoImage(self.waistimg)

                self.waistICO = ttk.Label(self.frameWaist, image=self.waistimg)
                self.waistICO.grid(column=1, row=1)
                self.waistICO.bind("<Button-1>", lambda event: self.displayitem('waist'))
        else:
            self.frameWaist['cursor'] = ''
            self.frameWaist.unbind("<Button-1>")

        self.waistnamelabel = ttk.Label(self.frameWaist, textvariable=self.waistName)
        self.waistnamelabel.grid(column=2, row=1, sticky=tk.N + tk.S)
        self.waistnamelabel.bind("<Button-1>", lambda event: self.displayitem('waist'))

        if self.player1.legs is not None:
            self.framePant['cursor'] = 'hand2'
            self.pantName.set(self.player1.legs.name)
            self.pantimg = self.player1.legs.image
            self.framePant.bind("<Button-1>", lambda event: self.displayitem('legs'))
            if self.pantimg is not None:
                try:
                    self.pantimg = Image.open(self.pantimg).resize((self.IMGSIZE, self.IMGSIZE), Image.ANTIALIAS)
                    self.pantimg = ImageTk.PhotoImage(self.pantimg)
                except:
                    self.imgname = self.pantimg
                    self.imgname = self.imgname[11:]
                    url = self.imgurl + self.imgname
                    self.download_image(url, self.img_path)
                    self.pantimg = Image.open(self.pantimg).resize((self.IMGSIZE, self.IMGSIZE), Image.ANTIALIAS)
                    self.pantimg = ImageTk.PhotoImage(self.pantimg)

                self.pantICO = ttk.Label(self.framePant, image=self.pantimg)
                self.pantICO.grid(column=1, row=1)
                self.pantICO.bind("<Button-1>", lambda event: self.displayitem('pant'))
        else:
            self.frameWaist['cursor'] = ''
            self.frameWaist.unbind("<Button-1>")

        #print(type(self.player1.defense))
        #print(self.player1.defense)

        self.getstats()

    def rebuild_all(self):

        self.warningW.destroy()

        #self.rebuilding_window()

        self.addB['state'] = 'disabled'
        self.removeB['state'] = 'disabled'
        self.rankEntry['state'] = 'disabled'
        self.skillEntry['state'] = 'disabled'
        self.autocheck['state'] = 'disabled'
        self.searchB['state'] = 'disabled'
        self.updateB['state'] = 'disabled'

        rebuild_database()

        print("Reloading database from file")

        s_file = open('assets/skill_list.bin', 'rb')
        a_file = open('assets/armor_list.bin', 'rb')
        db_file = open('assets/database.bin', 'rb')

        self.reloadfiles()

        print("DONE")

        #self.rebuildingW.destroy()

        self.addB['state'] = 'normal'
        self.removeB['state'] = 'normal'
        self.rankEntry['state'] = 'readonly'
        self.skillEntry['state'] = 'readonly'
        self.autocheck['state'] = 'normal'
        self.searchB['state'] = 'normal'
        self.updateB['state'] = 'normal'

        self.player1 = player()
        self.redraw_player()


    def goto_add(self):
        # self.master.withdraw()
        '''self.master.update_idletasks()
        add = addItemPg(self,self.db,self.a_list,self.s_list)'''

        #tk.Toplevel(self, first, *args, **kwargs)
        # root.withdraw()
        #self.focus_set()
        #self.first = first

        self.add = tk.Toplevel()

        self.addwin = tk.Frame(self.add)

        self.add.title("Add Item")

        self.ranklist = ['Master', 'High', 'Low']
        self.slotlist = ['Head', 'Gloves', 'Chest', 'Waist', 'Legs']
        self.skilllist = getskillnames(self.s_list)
        # sranklist = ['0']

        '''for i in range(0, len(skill)):
            skilllist.append(format(skill[i].get("name")))'''

        self.namelabelAdd = tk.Label(self.addwin, text="Item Name:")
        self.namelabelAdd.grid(column=1, row=1, sticky=tk.W)

        self.nameEntryAdd = tk.Entry(self.addwin)
        self.nameEntryAdd.grid(column=2, row=1, sticky=tk.E)

        self.rankLabelAdd = tk.Label(self.addwin, text="Rank:")
        self.rankLabelAdd.grid(column=1, row=2, sticky=tk.W)

        self.selrankAdd = tk.StringVar()
        self.rankEntryAdd = ttk.Combobox(self.addwin, state="readonly", textvariable=self.selrankAdd, values=self.ranklist)
        self.rankEntryAdd.grid(column=2, row=2, sticky=tk.E)
        self.rankEntryAdd.current(0)

        self.slotLabelAdd = tk.Label(self.addwin, text="Slot:")
        self.slotLabelAdd.grid(column=1, row=3, sticky=tk.W)

        self.selslotAdd = tk.StringVar()
        self.slotEntryAdd = ttk.Combobox(self.addwin, state="readonly", textvariable=self.selslotAdd, values=self.slotlist)
        self.slotEntryAdd.grid(column=2, row=3, sticky=tk.E)
        self.slotEntryAdd.current(0)

        self.skillLabelAdd = tk.Label(self.addwin, text="Main Skill:")
        self.skillLabelAdd.grid(column=1, row=4, sticky=tk.W)

        self.selskillAdd = tk.StringVar()
        self.skillEntryAdd = ttk.Combobox(self.addwin, state="readonly", textvariable=self.selskillAdd, values=self.skilllist)
        self.skillEntryAdd.bind('<FocusIn>', lambda event: self.rank_refresh(self.selskillAdd.get()))
        self.skillEntryAdd.grid(column=2, row=4, sticky=tk.E)
        self.skillEntryAdd.current(0)

        self.srankLabelAdd = tk.Label(self.addwin, text="Skill Rank:")
        self.srankLabelAdd.grid(column=1, row=6, sticky=tk.W)

        self.selsrankAdd = tk.StringVar()
        self.srankEntryAdd = ttk.Combobox(self.addwin, state="disabled", textvariable=self.selsrankAdd)
        self.srankEntryAdd.grid(column=2, row=6, sticky=tk.E)
        self.rank_refresh(self.selskillAdd.get())
        self.srankEntryAdd.current(0)

        self.defLabelAdd = tk.Label(self.addwin, text="Defense:")
        self.defLabelAdd.grid(column=1, row=7, sticky=tk.W)

        self.defEntryAdd = tk.Entry(self.addwin)
        self.defEntryAdd.grid(column=2, row=7, sticky=tk.E)

        self.confirmAdd = ttk.Button(self.addwin, text="Add", command=lambda: self.startadd())
        self.confirmAdd.grid(column=2, row=8, sticky=tk.E)

        self.cancelAdd = ttk.Button(self.addwin, text="Cancel", command=lambda: self.add.destroy())
        self.cancelAdd.grid(column=1, row=8, sticky=tk.W)

        for child in self.addwin.winfo_children(): child.grid_configure(padx=5, pady=5)

        self.addwin.grid(column=0, row=0)

        windowWidth = self.add.winfo_reqwidth()
        windowHeight = self.add.winfo_reqheight()
        positionRight = int(self.add.winfo_screenwidth() / 3 - windowWidth / 3)
        positionDown = int(self.add.winfo_screenheight() / 3 - windowHeight / 3)
        self.add.geometry("+{}+{}".format(positionRight, positionDown))

    def download_image(self, url, image_file_path,iscustom):
        filename = url
        print(url)
        if iscustom is True:
            filename = filename[39:]
            filename = filename.replace("/",".",2)
            filename = '/' + filename
        else:
            filename = filename[31:]
        filename = image_file_path + filename
        r = requests.get(url, timeout=4.0)
        if r.status_code != requests.codes.ok:
            assert False, 'Status code error: {}.'.format(r.status_code)

        with Image.open(BytesIO(r.content)) as im:
            im.save(filename)

    def warning_database(self):

        self.warningW = tk.Toplevel()
        self.warningW.title("WARNING")
        self.warningW.resizable(False, False)
        self.warningW.focus_set()
        self.warningLabel = ttk.Label(self.warningW,text="WARNING: All custom data will be erased. This cannot be undone.\nDo you wish to continue?")
        self.warningLabel.configure(justify="center")
        self.warningControls = ttk.Frame(self.warningW)
        self.warningControls.grid(column=0, row=1, sticky=tk.N)
        self.yesB = ttk.Button(self.warningControls, text="Yes", command=lambda: self.rebuild_all())
        self.noB = ttk.Button(self.warningControls, text="No", command=lambda: self.warningW.destroy())
        self.warningLabel.grid(column=0, row=0, sticky=tk.N)
        self.yesB.grid(column=1, row=0, sticky=tk.E)
        self.noB.grid(column=0, row=0, sticky=tk.W)

        for child in self.warningW.winfo_children(): child.grid_configure(padx=5, pady=5)

        windowWidth = self.warningW.winfo_reqwidth()
        windowHeight = self.warningW.winfo_reqheight()
        positionRight = int(self.warningW.winfo_screenwidth() / 3 - windowWidth / 3)
        positionDown = int(self.warningW.winfo_screenheight() / 3 - windowHeight / 3)
        self.warningW.geometry("+{}+{}".format(positionRight, positionDown))



    def getstats(self):

        tot_def = self.player1.defense

        stat_total = "Defense: {}\nResistances:\n\n   Fire: {}\n   Water: {}\n   Ice: {}\n   Thunder: {}\n   Dragon: {}\n\nSkills:\n".format(
            tot_def, self.player1.fire_res, self.player1.water_res,
            self.player1.ice_res, self.player1.thunder_res,
            self.player1.dragon_res)
        for i in range(0,len(self.player1.skills)):
            temp_skl = self.player1.skills[i]
            #print(temp_skl.name)
            temp_str = ''.join("\nName: {}\nDescription: {}\nLevel: {}\nEffects: {}\nModifiers: {}\n".format(temp_skl.name, temp_skl.description, temp_skl.level, temp_skl.effects, temp_skl.modifiers))
            #print(temp_str)
            stat_total = stat_total + temp_str

        self.stats.config(state=tk.NORMAL)
        self.stats.delete(1.0, tk.END)
        self.stats.insert(tk.END, stat_total)
        self.stats.config(state=tk.DISABLED)

    def go(self):

        '''self.addB['state'] = 'disabled'
        self.removeB['state'] = 'disabled'
        self.rankEntry['state'] = 'disabled'
        self.skillEntry['state'] = 'disabled'
        self.autocheck['state'] = 'disabled'
        self.searchB['state'] = 'disabled'
        self.updateB['state'] = 'disabled'''

        rank = self.selrank.get().lower()
        skill = self.selskill.get()
        autoc = self.autoc.get()
        self.found = 0
        aset = armorset()
        self.player1 = player()

        aset, self.found = makeset(skill, rank, autoc, self.db, self.a_list, self.s_list, player())
        if self.autoc == True:
            aset.autocomplete(self.a_list,rank)
        self.player1.buildplayer(aset, self.s_list)

        self.redraw_player()

        self.addB['state'] = 'normal'
        self.removeB['state'] = 'normal'
        self.rankEntry['state'] = 'readonly'
        self.skillEntry['state'] = 'readonly'
        self.autocheck['state'] = 'normal'
        self.searchB['state'] = 'normal'
        self.updateB['state'] = 'normal'

        return

    def __init__(self, master, db, s_list, a_list, *args, **kwargs):

        windowWidth = master.winfo_reqwidth()
        windowHeight = master.winfo_reqheight()
        positionRight = int(master.winfo_screenwidth() / 3 - windowWidth / 3)
        positionDown = int(master.winfo_screenheight() / 3 - windowHeight / 3)
        master.geometry("+{}+{}".format(positionRight, positionDown))

        self.db = db
        self.s_list = s_list
        self.a_list = a_list
        gc.collect()
        # tk.Tk.__init__(self, *args, **kwargs)
        self.player1 = player()
        self.img_path = "assets/img"
        self.autoc = tk.BooleanVar()
        self.imgurl = "https://assets.mhw-db.com/armor/"
        self.customurl = "https://cdn.discordapp.com/attachments/"

        self.FRAMEW = 350
        self.FRAMEH = 60
        self.IMGSIZE = 60

        self.master = master
        master.focus_set()

        # self.master=tk.Tk()
        master.resizable(False, False)

        master.title("MHW Build Calculator")

        self.top = ttk.Frame(self.master)
        self.bot = ttk.Frame(self.master)
        self.display = ttk.Frame(self.top, borderwidth=1, relief='raised')
        self.controls = ttk.Frame(self.top, borderwidth=1)
        self.statdisplay = ttk.Frame(self.bot, borderwidth=1, relief='raised')

        # WIDGETS FOR DISPLAY PAGE

        self.frameHead = ttk.Frame(self.display, height=self.FRAMEH, width=self.FRAMEW, borderwidth=2, relief='sunken')
        self.frameHead.grid(column=0, row=0, sticky=tk.W)
        #self.frameHead.bind("<Button-1>", lambda event: testprint())

        self.frameChest = ttk.Frame(self.display, height=self.FRAMEH, width=self.FRAMEW, borderwidth=2, relief='sunken')
        self.frameChest.grid(column=0, row=1, sticky=tk.W)
        self.frameChest.bind("<Button-1>", lambda event: self.displayitem('chest'))

        self.frameGlove = ttk.Frame(self.display, height=self.FRAMEH, width=self.FRAMEW, borderwidth=2, relief='sunken')
        self.frameGlove.grid(column=0, row=2, sticky=tk.W)
        self.frameGlove.bind("<Button-1>", lambda event: self.displayitem('glove'))

        self.frameWaist = ttk.Frame(self.display, height=self.FRAMEH, width=self.FRAMEW, borderwidth=2, relief='sunken')
        self.frameWaist.grid(column=0, row=3, sticky=tk.W)
        self.frameWaist.bind("<Button-1>", lambda event: self.displayitem('waist'))

        self.framePant = ttk.Frame(self.display, height=self.FRAMEH, width=self.FRAMEW, borderwidth=2, relief='sunken')
        self.framePant.grid(column=0, row=4, sticky=tk.W)
        self.framePant.bind("<Button-1>", lambda event: self.displayitem('legs'))

        ''' HEAD '''

        self.headName = tk.StringVar()
        self.headName.set("None")

        self.headnamelabel = ttk.Label(self.frameHead, textvariable=self.headName)
        self.headnamelabel.grid(column=2, row=1, sticky=tk.N + tk.S)
        #self.headnamelabel.bind("<Button-1>", lambda event: self.displayitem('head'))

        ''' CHEST '''

        self.chestName = tk.StringVar()
        self.chestName.set("None")

        self.chestnamelabel = ttk.Label(self.frameChest, textvariable=self.chestName)
        self.chestnamelabel.grid(column=2, row=1, sticky=tk.N + tk.S)
        #self.chestnamelabel.bind("<Button-1>", lambda event: self.changeitem('chest'))

        ''' GLOVE '''

        self.gloveName = tk.StringVar()
        self.gloveName.set("None")

        self.glovenamelabel = ttk.Label(self.frameGlove, textvariable=self.gloveName)
        self.glovenamelabel.grid(column=2, row=1, sticky=tk.N + tk.S)
        #self.glovenamelabel.bind("<Button-1>", lambda event: self.changeitem('glove'))

        ''' WAIST '''

        self.waistName = tk.StringVar()
        self.waistName.set("None")

        self.waistnamelabel = ttk.Label(self.frameWaist, textvariable=self.waistName)
        self.waistnamelabel.grid(column=2, row=1, sticky=tk.N + tk.S)
        #self.waistnamelabel.bind("<Button-1>", lambda event: self.changeitem('waist'))

        ''' PANT '''

        self.pantName = tk.StringVar()
        self.pantName.set("None")

        self.pantnamelabel = ttk.Label(self.framePant, textvariable=self.pantName)
        self.pantnamelabel.grid(column=2, row=1, sticky=tk.N + tk.S)
        #self.pantnamelabel.bind("<Button-1>", lambda event: self.changeitem('pant'))

        for child in self.display.winfo_children(): child.grid_propagate(0)
        for child in self.display.winfo_children(): child.grid_configure(padx=5, pady=5)

        self.display.grid(column=0, row=0, sticky=tk.W)

        '''END DISPLAY'''
        '''BEGIN STATS'''

        self.stats = tk.Text(self.statdisplay,height=12,width=63)
        self.stats.pack(side=tk.LEFT, fill=tk.Y)
        self.scrollbar = ttk.Scrollbar(self.statdisplay)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar.config(command=self.stats.yview)
        self.stats.config(yscrollcommand=self.scrollbar.set)

        self.getstats()

        self.statdisplay.grid(column=0,row=5,sticky=tk.W)

        '''END STATS'''
        '''BEGIN CONTROLS'''

        ranklist = ['Master', 'High', 'Low']
        deflist = ['Physical', 'Fire', 'Water', 'Ice', 'Thunder', 'Dragon']

        skilllist = getskillnames(self.s_list)

        self.topbuttons = ttk.Frame(self.controls)

        self.addB = ttk.Button(self.topbuttons, text="Add New Item", command=lambda: self.goto_add())
        self.addB.grid(column=0, row=0, sticky=tk.W)

        self.removeB = ttk.Button(self.topbuttons, text = "Delete Item", command=lambda: self.deleteWindow())
        self.removeB.grid(column=1,row=0,sticky=tk.E)

        self.topbuttons.grid(column=0,row=0)

        self.rankLabel = tk.Label(self.controls, text="Rank Filter:")
        self.rankLabel.grid(column=0, row=1, sticky=tk.N)

        self.selrank = tk.StringVar()
        self.rankEntry = ttk.Combobox(self.controls, state="readonly", textvariable=self.selrank, values=ranklist)
        self.rankEntry.grid(column=0, row=2, sticky=tk.N)
        self.rankEntry.current(0)

        self.skillLabel = tk.Label(self.controls, text="Skill to Prioritize:")
        self.skillLabel.grid(column=0, row=3, sticky=tk.N)

        self.selskill = tk.StringVar()
        self.skillEntry = ttk.Combobox(self.controls, state="readonly", textvariable=self.selskill, values=skilllist)
        self.skillEntry.grid(column=0, row=4, sticky=tk.N)
        self.skillEntry.current(14)

        self.autocheck = ttk.Checkbutton(self.controls, text="Autocomplete Set", variable=self.autoc, onvalue=True, offvalue=False)
        self.autocheck.grid(column=0, row=7, sticky=tk.N)

        self.searchB = ttk.Button(self.controls, text="Find Set", command=lambda: self.go())
        self.searchB.grid(column=0, row=8, sticky=tk.N)

        self.updateB = ttk.Button(self.controls, text="Rebuild Database", command=lambda: self.warning_database())
        self.updateB.grid(column=0, row=9, sticky=tk.N)


        #for child in self.controls.winfo_children(): child.grid_propagate(0)
        for child in self.controls.winfo_children(): child.grid_configure(padx=5, pady=5)

        self.controls.grid(column=1, row=0, sticky=tk.W)
        gc.collect()

        self.top.grid(column=0, row=0)
        self.bot.grid(column=0, row=1)
