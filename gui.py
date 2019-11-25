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
from tkinter import ttk
from PIL import Image, ImageTk
from io import BytesIO
import os
#import mhw_objects


def testprint():
    print("clicked a button")


# noinspection PyCallByClass
class addItemPg(tk.Tk):

    def goback(self):
        # self.first.update()
        # self.first.deiconify()
        self.destroy()

    def getranks(self, oneskl):

        name = oneskl

        skl = list(filter(lambda oneskl: oneskl["name"] == name, skill))
        ranklist = [sub['ranks'] for sub in skl]
        ranks = []
        if ranklist:
            maxlevel = len(ranklist.pop())

            for i in range(1, maxlevel + 1):
                ranks.append(i)

        return ranks

    def rank_refresh(self, oneskl):

        if oneskl != 'None':
            self.srankEntry['state'] = "readonly"
            self.srankEntry['values'] = tuple(self.getranks(oneskl))
            self.srankEntry.current(0)
        else:
            self.srankEntry['state'] = "disabled"
            self.srankEntry['values'] = [None]
            self.srankEntry.current(0)

    def __init__(self, first, *args, **kwargs):
        tk.Toplevel.__init__(self, first, *args, **kwargs)
        # root.withdraw()
        self.focus_set()
        self.first = first

        addwin = tk.Frame(self)

        self.title("Add Item")

        ranklist = ['Master', 'High', 'Low']
        slotlist = ['Head', 'Gloves', 'Chest', 'Waist', 'Boots']
        skilllist = ['None']
        # sranklist = ['0']

        for i in range(0, len(skill)):
            skilllist.append(format(skill[i].get("name")))

        namelabel = tk.Label(addwin, text="Item Name:")
        namelabel.grid(column=1, row=1, sticky=tk.W)

        nameEntry = tk.Entry(addwin)
        nameEntry.grid(column=2, row=1, sticky=tk.E)

        rankLabel = tk.Label(addwin, text="Rank:")
        rankLabel.grid(column=1, row=2, sticky=tk.W)

        selrank = tk.StringVar()
        rankEntry = ttk.Combobox(addwin, state="readonly", textvariable=selrank, values=ranklist)
        rankEntry.grid(column=2, row=2, sticky=tk.E)

        slotLabel = tk.Label(addwin, text="Slot:")
        slotLabel.grid(column=1, row=3, sticky=tk.W)

        selslot = tk.StringVar()
        slotEntry = ttk.Combobox(addwin, state="readonly", textvariable=selslot, values=slotlist)
        slotEntry.grid(column=2, row=3, sticky=tk.E)

        skillLabel = tk.Label(addwin, text="Main Skill:")
        skillLabel.grid(column=1, row=4, sticky=tk.W)

        selskill = tk.StringVar()
        skillEntry = ttk.Combobox(addwin, state="readonly", textvariable=selskill, values=skilllist)
        skillEntry.bind('<FocusIn>', lambda event: self.rank_refresh(selskill.get()))
        skillEntry.grid(column=2, row=4, sticky=tk.E)
        skillEntry.current(0)

        srankLabel = tk.Label(addwin, text="Skill Rank:")
        srankLabel.grid(column=1, row=6, sticky=tk.W)

        selsrank = tk.StringVar()
        self.srankEntry = ttk.Combobox(addwin, state="disabled", textvariable=selsrank)
        self.srankEntry.grid(column=2, row=6, sticky=tk.E)
        # self.srankEntry.current(0)

        defLabel = tk.Label(addwin, text="Defense:")
        defLabel.grid(column=1, row=7, sticky=tk.W)

        defEntry = tk.Entry(addwin)
        defEntry.grid(column=2, row=7, sticky=tk.E)

        confirm = ttk.Button(addwin, text="Add", command=lambda: testprint())
        confirm.grid(column=2, row=8, sticky=tk.E)

        cancel = ttk.Button(addwin, text="Cancel", command=lambda: self.goback())
        cancel.grid(column=1, row=8, sticky=tk.W)

        for child in addwin.winfo_children(): child.grid_configure(padx=5, pady=5)

        addwin.grid(column=0, row=0)

        # print(type(srankEntry['values']))


hdr = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}

armor2 = [
    {
        "id": 1,
        "name": "Leather Headgear",
        "rank": "low",
        "defense": 68,
        "image": "assets/img/e7cfa0acf10c8439b78639a0f59c2eb9ee9e2923.c8685d97610f608eae4850d6f53b9226.png",
        "resistances": {
            "fire": 2,
            "water": 0,
            "ice": 0,
            "thunder": 0,
            "dragon": 0
        },
    },
    {
        "id": 11,
        "name": "Hunter's Headgear",
        "rank": "low",
        "defense": 72,
        "image": "assets/img/fd20b2ac4e0c0fe92dceffc8bf67f2b737497307.600620ad32b8010116855be16c44059f.png",
        "resistances": {
            "fire": 2,
            "water": 0,
            "ice": 0,
            "thunder": 0,
            "dragon": 0
        },
    }, ]

setskills = [{
            "name": "Hunger Resistance",
            "level": 1,
            "description" : "Extends the time until your stamina cap decreases by 50%.",
            },
            ]

armor = [
    {
        "id": 1,
        "name": "Leather Headgear",
        "rank": "low",
        "defense": 68,
        "image": "assets/img/e7cfa0acf10c8439b78639a0f59c2eb9ee9e2923.c8685d97610f608eae4850d6f53b9226.png",
        "resistances": {
            "fire": 2,
            "water": 0,
            "ice": 0,
            "thunder": 0,
            "dragon": 0
        },
        "skills" : [67],
        "ranks" : [1],
    },
    {
        "id": 2,
        "name": "Leather Mail",
        "rank": "low",
        "defense": 68,
        "image": "assets/img/8c083e8d252d2d86456fda2135a8a16b21679ec6.4856a15b707ce6c14d2fb143c1513696.png",
        "resistances": {
            "fire": 2,
            "water": 0,
            "ice": 0,
            "thunder": 0,
            "dragon": 0
        },
        "skills": [],
        "ranks": [],
    },
    {
        "id": 3,
        "name": "Leather Gloves",
        "rank": "low",
        "defense": 68,
        "image": "assets/img/1f80c6c43da88f5977765a7c6c9baaf52e8ec5c3.4ffa6d0b149ce6f8f1c15a98ea4e22f5.png",
        "resistances": {
            "fire": 2,
            "water": 0,
            "ice": 0,
            "thunder": 0,
            "dragon": 0
        },
        "skills": [],
        "ranks": [],
    },
    {
        "id": 4,
        "name": "Leather Belt",
        "rank": "low",
        "defense": 68,
        "image": "assets/img/e41b9bc0eabf3d67a7a5641ec1403639835533a2.6e12383e9f0d117db879b90e9f7ab89c.png",
        "resistances": {
            "fire": 2,
            "water": 0,
            "ice": 0,
            "thunder": 0,
            "dragon": 0
        },
        "skills": [],
        "ranks": [],
    },
    {
        "id": 5,
        "name": "Leather Trousers",
        "rank": "low",
        "defense": 68,
        "image": "assets/img/07532b6d0922c66d3d569108506880ac1790439c.9d49413bced4ac9a9cbcda445eb29eb2.png",
        "resistances": {
            "fire": 2,
            "water": 0,
            "ice": 0,
            "thunder": 0,
            "dragon": 0
        },
        "skills": [],
        "ranks": [],
    }
]

skill = [{
    "id": 1,
    "name": "Poison Resistance",
    "description": "Reduces damage while poisoned.",
    "max rank": 3,
    "ranks": [
        {
            "id": 1,
            "skill": 1,
            "skillName": "Poison Resistance",
            "level": 1,
            "description": "Reduces the number of times you take poison damage.",
            "modifiers": {}
        },
        {
            "id": 2,
            "skill": 1,
            "skillName": "Poison Resistance",
            "level": 2,
            "description": "Greatly reduces the number of times you take poison damage.",
            "modifiers": {}
        },
        {
            "id": 3,
            "skill": 1,
            "skillName": "Poison Resistance",
            "level": 3,
            "description": "Prevents poison.",
            "modifiers": {}
        }
    ]
    },
    {
        "id": 61,
        "name": "Artillery",
        "description": "Strengthens explosive attacks like gunlance shells, Wyvern's Fire, charge blade phial attacks, and sticky ammo.",
        "ranks": [
            {
                "id": 190,
                "skill": 61,
                "skillName": "Artillery",
                "level": 1,
                "description": "Increases power of each attack by 10% and reduces Wyvern's Fire cooldown by 15%.",
                "modifiers": {}
            },
            {
                "id": 191,
                "skill": 61,
                "skillName": "Artillery",
                "level": 2,
                "description": "Increases power of each attack by 20% and reduces Wyvern's Fire cooldown by 30%.",
                "modifiers": {}
            },
            {
                "id": 192,
                "skill": 61,
                "skillName": "Artillery",
                "level": 3,
                "description": "Increases power of each attack by 30% and reduces Wyvern's Fire cooldown by 50%.",
                "modifiers": {}
            },
            {
                "id": 354,
                "skill": 61,
                "skillName": "Artillery",
                "level": 4,
                "description": "Increases power of each attack by 40% and reduces Wyvern's Fire cooldown by 60%.",
                "modifiers": {}
            },
            {
                "id": 355,
                "skill": 61,
                "skillName": "Artillery",
                "level": 5,
                "description": "Increases power of each attack by 50% and reduces Wyvern's Fire cooldown by 70%.",
                "modifiers": {}
            }
        ]
    },
    {
        "id": 67,
        "name": "Hunger Resistance",
        "description": "Reduces maximum stamina depletion over time. However, does not work against cold environments that reduce stamina.",
        "ranks": [
            {
                "id": 207,
                "skill": 67,
                "skillName": "Hunger Resistance",
                "level": 1,
                "description": "Extends the time until your stamina cap decreases by 50%.",
                "modifiers": {}
            },
            {
                "id": 208,
                "skill": 67,
                "skillName": "Hunger Resistance",
                "level": 2,
                "description": "Extends the time until your stamina cap decreases by 100%.",
                "modifiers": {}
            },
            {
                "id": 209,
                "skill": 67,
                "skillName": "Hunger Resistance",
                "level": 3,
                "description": "Prevents your stamina cap from decreasing.",
                "modifiers": {}
            }
        ]
    }
]


class mainWindow:

    addB: Button

    def goto_add(self):
        # self.master.withdraw()
        self.master.update_idletasks()
        add = addItemPg(self)
        # print("a")

    def changehead(self, opt, win):

        if opt == 1:
            armor[0] = armor2[0]
        else:
            armor[0] = armor2[1]

        self.headName.set(armor[0].get("name"))

        self.headimg = armor[0].get("image")

        try:
            self.headimg = Image.open(self.headimg).resize((self.IMGSIZE, self.IMGSIZE), Image.ANTIALIAS)
            self.headimg = ImageTk.PhotoImage(self.headimg)
        except:
            imgname = self.headimg
            imgname = imgname[11:]
            url = self.imgurl + imgname
            self.download_image(url, self.img_path)
            self.headimg = Image.open(self.headimg).resize((self.IMGSIZE, self.IMGSIZE), Image.ANTIALIAS)
            self.headimg = ImageTk.PhotoImage(self.headimg)

        self.headICO['image'] = self.headimg
        self.headnamelabel['textvariable'] = self.headName
        self.getstats()

    def changeitem(self, slot):

        changewin = tk.Toplevel(self.master)

        if slot != 'head':
            label1 = ttk.Label(changewin, text="changing " + slot)
            label1.grid(column=0, row=0)
        else:
            but1 = ttk.Button(changewin, text="Change to Leather", command=lambda: self.changehead(1, changewin))
            but1.grid(column=0, row=0, sticky=tk.E)
            # but1.bind("<Button-1>", lambda: changewin.destroy)
            but2 = ttk.Button(changewin, text="Change to Hunter", command=lambda: self.changehead(0, changewin))
            but2.grid(column=1, row=0, sticky=tk.W)
            # but2.bind("<Button-1>", lambda: changewin.destroy)

        cancel = ttk.Button(changewin, text="Cancel", command=lambda: changewin.destroy())
        cancel.grid(column=1, row=1, sticky=tk.E)

    def printboxvalue(self, val):
        i = val.get()

        if i == 1:
            print("Turning Off")
        else:
            print("Turning On")

    def getsetdef(self):

        tot_def = 0

        for i in range(0,len(armor)):
            tot_def += armor[i].get('defense')

        print(tot_def)
        return tot_def

    def getsetskl(self):

        tot_skl = ""
        if setskills:
            for i in range(0,len(setskills)):
                tot_skl += "Name: {}\nLevel: {}\nDescription: {}\n".format(setskills[i].get('name'), setskills[i].get('level'), setskills[i].get('description'))
        else:
            tot_skl = "No Skills in Set"
        print (tot_skl)
        return tot_skl

    def download_image(self, url, image_file_path):
        filename = url
        filename = filename[31:]
        filename = image_file_path + filename
        r = requests.get(url, timeout=4.0)
        if r.status_code != requests.codes.ok:
            assert False, 'Status code error: {}.'.format(r.status_code)

        with Image.open(BytesIO(r.content)) as im:
            im.save(filename)

    def getstats(self):

        tot_def = self.getsetdef()
        tot_skl = self.getsetskl()

        stat_total = "Defense: {}\nResistances:\n   Fire: {}\n   Water: {}\n   Ice: {}\n   Thunder: {}\n   Dragon: {}\nSkills:\n{}".format(
            tot_def, armor[0].get('resistances').get('fire'), armor[0].get('resistances').get('water'),
            armor[0].get('resistances').get('ice'), armor[0].get('resistances').get('thunder'),
            armor[0].get('resistances').get('dragon'), tot_skl)

        self.stats.config(state=tk.NORMAL)
        self.stats.delete(1.0, tk.END)
        self.stats.insert(tk.END, stat_total)
        self.stats.config(state=tk.DISABLED)

    def __init__(self, master, *args, **kwargs):

        gc.collect()
        # tk.Tk.__init__(self, *args, **kwargs)
        self.img_path = "assets/img"
        self.autoc = tk.IntVar()
        self.imgurl = "https://assets.mhw-db.com/armor/"

        self.FRAMEW = 350
        self.FRAMEH = 60
        self.IMGSIZE = 60

        self.master = master

        # self.master=tk.Tk()

        master.title("MHW Build Calculator")

        self.top = ttk.Frame(self.master)
        self.bot = ttk.Frame(self.master)
        self.display = ttk.Frame(self.top, borderwidth=1, relief='raised')
        self.controls = ttk.Frame(self.top, borderwidth=1)
        self.statdisplay = ttk.Frame(self.bot, borderwidth=1, relief='raised')


        # WIDGETS FOR DISPLAY PAGE

        self.frameHead = ttk.Frame(self.display, height=self.FRAMEH, width=self.FRAMEW, borderwidth=2, relief='sunken',
                                   cursor="hand2")
        self.frameHead.grid(column=0, row=0, sticky=tk.W)
        self.frameHead.bind("<Button-1>", lambda event: self.changeitem('head'))

        self.frameChest = ttk.Frame(self.display, height=self.FRAMEH, width=self.FRAMEW, borderwidth=2, relief='sunken',
                                    cursor="hand2")
        self.frameChest.grid(column=0, row=1, sticky=tk.W)
        self.frameChest.bind("<Button-1>", lambda event: self.changeitem('chest'))

        self.frameGlove = ttk.Frame(self.display, height=self.FRAMEH, width=self.FRAMEW, borderwidth=2, relief='sunken',
                                    cursor="hand2")
        self.frameGlove.grid(column=0, row=2, sticky=tk.W)
        self.frameGlove.bind("<Button-1>", lambda event: self.changeitem('glove'))

        self.frameWaist = ttk.Frame(self.display, height=self.FRAMEH, width=self.FRAMEW, borderwidth=2, relief='sunken',
                                    cursor="hand2")
        self.frameWaist.grid(column=0, row=3, sticky=tk.W)
        self.frameWaist.bind("<Button-1>", lambda event: self.changeitem('waist'))

        self.framePant = ttk.Frame(self.display, height=self.FRAMEH, width=self.FRAMEW, borderwidth=2, relief='sunken',
                                   cursor="hand2")
        self.framePant.grid(column=0, row=4, sticky=tk.W)
        self.framePant.bind("<Button-1>", lambda event: self.changeitem('pant'))

        ''' HEAD '''

        self.headName = tk.StringVar()
        self.headName.set(armor[0].get("name"))

        self.headimg = armor[0].get("image")

        try:
            self.headimg = Image.open(self.headimg).resize((self.IMGSIZE, self.IMGSIZE), Image.ANTIALIAS)
            self.headimg = ImageTk.PhotoImage(self.headimg)
        except:
            self.imgname = self.headimg
            self.imgname = self.imgname[11:]
            url = self.imgurl + self.imgname
            self.download_image(url, self.img_path)
            self.headimg = Image.open(self.headimg).resize((self.IMGSIZE, self.IMGSIZE), Image.ANTIALIAS)
            self.headimg = ImageTk.PhotoImage(self.headimg)

        self.headICO = ttk.Label(self.frameHead, image=self.headimg)
        self.headICO.grid(column=1, row=1)
        self.headICO.bind("<Button-1>", lambda event: self.changeitem('head'))

        self.headnamelabel = ttk.Label(self.frameHead, textvariable=self.headName)
        self.headnamelabel.grid(column=2, row=1, sticky=tk.N)
        self.headnamelabel.bind("<Button-1>", lambda event: self.changeitem('head'))

        ''' CHEST '''

        self.chestName = tk.StringVar()
        self.chestName.set(armor[1].get("name"))

        self.chestimg = armor[1].get("image")

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
        self.chestICO.bind("<Button-1>", lambda event: self.changeitem('chest'))

        self.chestnamelabel = ttk.Label(self.frameChest, textvariable=self.chestName)
        self.chestnamelabel.grid(column=2, row=1, sticky=tk.N + tk.S)
        self.chestnamelabel.bind("<Button-1>", lambda event: self.changeitem('chest'))

        ''' GLOVE '''

        self.gloveName = tk.StringVar()
        self.gloveName.set(armor[2].get("name"))

        self.gloveimg = armor[2].get("image")

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
        self.gloveICO.bind("<Button-1>", lambda event: self.changeitem('glove'))

        self.glovenamelabel = ttk.Label(self.frameGlove, textvariable=self.gloveName)
        self.glovenamelabel.grid(column=2, row=1, sticky=tk.N + tk.S)
        self.glovenamelabel.bind("<Button-1>", lambda event: self.changeitem('glove'))

        ''' WAIST '''

        self.waistName = tk.StringVar()
        self.waistName.set(armor[3].get("name"))

        self.waistimg = armor[3].get("image")

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
        self.waistICO.bind("<Button-1>", lambda event: self.changeitem('waist'))

        self.waistnamelabel = ttk.Label(self.frameWaist, textvariable=self.waistName)
        self.waistnamelabel.grid(column=2, row=1, sticky=tk.N + tk.S)
        self.waistnamelabel.bind("<Button-1>", lambda event: self.changeitem('waist'))

        ''' PANT '''

        self.pantName = tk.StringVar()
        self.pantName.set(armor[4].get("name"))

        self.pantimg = armor[4].get("image")

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
        self.pantICO.bind("<Button-1>", lambda event: self.changeitem('pant'))

        self.pantnamelabel = ttk.Label(self.framePant, textvariable=self.pantName)
        self.pantnamelabel.grid(column=2, row=1, sticky=tk.N + tk.S)
        self.pantnamelabel.bind("<Button-1>", lambda event: self.changeitem('pant'))



        for child in self.display.winfo_children(): child.grid_propagate(0)
        for child in self.display.winfo_children(): child.grid_configure(padx=5, pady=5)

        self.display.grid(column=0, row=0, sticky=tk.W)

        '''END DISPLAY'''
        '''BEGIN STATS'''

        self.stats = tk.Text(self.statdisplay,height=6,width=63)
        self.stats.pack(side=tk.LEFT, fill=tk.Y)
        self.scrollbar = ttk.Scrollbar(self.statdisplay)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar.config(command=self.stats.yview)
        self.stats.config(yscrollcommand=self.scrollbar.set)

        self.getstats()

        self.statdisplay.grid(column=0,row=5,sticky=tk.W)

        '''END STATS'''
        '''BEGIN CONTROLS'''

        skilllist = ['None']
        ranklist = ['Master', 'High', 'Low']
        deflist = ['Physical', 'Fire', 'Water', 'Ice', 'Thunder', 'Dragon']

        for i in range(0, len(skill)):
            skilllist.append(format(skill[i].get("name")))

        self.addB = ttk.Button(self.controls, text="Add New Item Data", command=lambda: self.goto_add())
        self.addB.grid(column=0, row=0, sticky=tk.N)

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
        self.skillEntry.current(0)

        self.defLabel = tk.Label(self.controls, text="Defense Filter:")
        self.defLabel.grid(column=0, row=5, sticky=tk.N)

        self.seldef = tk.StringVar()
        self.defEntry = ttk.Combobox(self.controls, state="readonly", textvariable=self.seldef, values=deflist)
        self.defEntry.grid(column=0, row=6, sticky=tk.N)
        self.defEntry.current(0)

        self.autocheck = ttk.Checkbutton(self.controls, text="Autocomplete Set", variable=self.autoc, onvalue=1, offvalue=0)
        self.autocheck.grid(column=0, row=7, sticky=tk.N)
        self.autocheck.bind("<Button-1>", lambda event: self.printboxvalue(self.autoc))

        self.searchB = ttk.Button(self.controls, text="Find Set", command=lambda: testprint())
        self.searchB.grid(column=0, row=8, sticky=tk.N)

        self.updateB = ttk.Button(self.controls, text="Check for DB Update", command=lambda: testprint())
        self.updateB.grid(column=0, row=9, sticky=tk.N)

        for child in self.controls.winfo_children(): child.grid_propagate(0)
        for child in self.controls.winfo_children(): child.grid_configure(padx=5, pady=5)

        self.controls.grid(column=1, row=0, sticky=tk.W)
        gc.collect()

        self.top.grid(column=0,row=0)
        self.bot.grid(column=0,row=1)


def main():
    path = "assets/img"

    if os.path.isdir(path) == False:
        try:
            os.makedirs(path)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
            pass
    if os.path.isdir(path) == True:
        root = tk.Tk()
        app = mainWindow(root)
        root.mainloop()


if __name__ == '__main__':
    main()
