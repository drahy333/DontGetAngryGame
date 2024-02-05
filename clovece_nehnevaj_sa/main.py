import tkinter
from PIL import Image, ImageTk
import random
import time


class Figurka:
    def __init__(self, canvas, id, pozicia, obrazok, farba, spawn, hp):
        self.id = id
        self.spawn = 0
        self.canvas = canvas
        self.farba = farba
        self.pozicia = pozicia
        self.spawn_x = spawn.x
        self.spawn_y = spawn.y
        self.hp = hp
        self.pozicia_v_hernej_ploche = self.hp[self.pozicia]
        self.obrazok = self.canvas.create_image(self.spawn_x, self.spawn_y, image=obrazok, tags=(self.farba, self.id))
        self.je_v_domceku = 0


class Hrac:
    def __init__(self, canvas, id, farba, obrazok, herna_plocha, spawny, po_pohnuti_figurky, text, c):

        self.id = id
        self.canvas = canvas
        self.herna_plocha = herna_plocha
        self.farba = farba
        self.figurky = []
        self.spawny = spawny
        self.po_pohnuti_figurky = po_pohnuti_figurky
        self.text = text
        self.pocitadla = []
        self.c = c
        for i in range(4):
            self.figurky.append(Figurka(self.canvas, i, 0, obrazok, self.farba, spawny[i], self.herna_plocha))

    def pohni_figurku_hraca(self, posun, item, index_figurky):
        self.posun = posun
        self.item = item
        self.index_figurky = index_figurky
        self.testik = 0

        aktualna_figurka = self.figurky[self.index_figurky]
        aktualna_pozicia_figurky_v_ploche = aktualna_figurka.pozicia
        buduca_pozicia_figurky = aktualna_pozicia_figurky_v_ploche + self.posun
        if buduca_pozicia_figurky < len(self.herna_plocha) and self.pozicia_je_volna(buduca_pozicia_figurky) == 1:
            self.pohni_figurku_s_animaciou(aktualna_figurka)
            if buduca_pozicia_figurky > len(self.herna_plocha) - 5:
                aktualna_figurka.je_v_domceku = 1
                aktualna_figurka.spawn = 0
        else:
            self.po_pohnuti_figurky(aktualna_figurka)

    def pozicia_je_volna(self, buduca_pozicia_figurky):
        for figurka in self.figurky:
            if figurka.pozicia == buduca_pozicia_figurky:
                return 0
        return 1

    def pohni_figurku_s_animaciou(self, aktualna_figurka):
        if self.testik != self.posun:
            self.testik += 1

            poz = aktualna_figurka.pozicia + 1
            aktualna_figurka.pozicia = poz
            aktualna_figurka.pozicia_v_hernej_ploche = aktualna_figurka.hp[poz]

            self.canvas.coords(self.item, self.herna_plocha[poz].x, self.herna_plocha[poz].y)
            self.canvas.after(300, self.pohni_figurku_s_animaciou, aktualna_figurka)
        else:
            self.testik = 0
            self.po_pohnuti_figurky(aktualna_figurka)

    def spawnni_figurku(self, i, d=0):
        # print(self.figurky[i].spawn_x, self.figurky[i].spawn_y, self.herna_plocha[0], self.figurky[i].pozicia_v_hernej_ploche)
        self.canvas.coords(self.figurky[i].obrazok, self.herna_plocha[d].x, self.herna_plocha[d].y)
        if d < len(self.herna_plocha) - 5:
            self.figurky[i].spawn = 1

    def despawnni_figurku(self, i):
        self.figurky[i].spawn = 0
        self.figurky[i].pozicia = 0
        self.figurky[i].pozicia_v_hernej_ploche = self.figurky[i].hp[0]
        self.canvas.coords(self.figurky[i].obrazok, self.figurky[i].spawn_x, self.figurky[i].spawn_y)

    def je_volny_spawn(self, i):
        for figurka in self.figurky:
            if self.figurky[i] != figurka:
                if self.figurky[i].spawn == 0 and figurka.spawn == 1 and figurka.pozicia_v_hernej_ploche == \
                        self.herna_plocha[0]:
                    return 0
        return 1


class Policko:
    def __init__(self, x, y, index):
        self.x = x
        self.y = y
        self.index = index

    def __str__(self):
        j = str(self.x) + ' ' + str(self.y)
        return j


class Konzola:
    def __init__(self, meno):
        subor = open(meno, 'r', encoding='utf-8')
        for riadok in subor:
            print(riadok)
        subor.close()


class Program:
    def __init__(self):
        root = tkinter.Tk()
        root.geometry('1100x1000')
        konzola = Konzola('rules.txt')
        self.canvas = tkinter.Canvas(root, width=1100, height=1000, bg='bisque2')
        self.canvas.pack()

        self.nacitanie_herneho_modu()
        self.pocetHracov = 0
        root.mainloop()

    def nacitanie_herneho_modu(self):
        self.startovac1 = self.canvas.create_text(550, 100, text='Enter the number of players if you want to start a new game.',
                                                  font='arial 30')
        if self.je_ulozena_hra() == 1:
            self.startovac2 = self.canvas.create_text(550, 550,
                                                      text='If you want to play saved game, click this button',
                                                      font='arial 30')
            self.ulozenahra = self.canvas.create_rectangle(300, 700, 800, 800, fill="red", outline="black",
                                                           tags=('save'))
            self.canvas.tag_bind(self.ulozenahra, '<ButtonPress>', self.spustenie_hry)

        self.jedenhrac = self.canvas.create_rectangle(200, 300, 300, 400, fill="grey40", outline="grey60", tags=('1'))
        self.jedenhracT = self.canvas.create_text(250, 350, text="1", font='arial 30', tags=('1'))
        self.dvajahraci = self.canvas.create_rectangle(400, 300, 500, 400, fill="grey40", outline="grey60", tags=('2'))
        self.dvajahraciT = self.canvas.create_text(450, 350, text="2", font='arial 30', tags=('2'))
        self.trajahraci = self.canvas.create_rectangle(600, 300, 700, 400, fill="grey40", outline="grey60", tags=('3'))
        self.trajahraciT = self.canvas.create_text(650, 350, text="3", font='arial 30', tags=('3'))
        self.styriahraci = self.canvas.create_rectangle(800, 300, 900, 400, fill="grey40", outline="grey60", tags=('4'))
        self.styriahraciT = self.canvas.create_text(850, 350, text="4", font='arial 30', tags=('4'))

        self.canvas.tag_bind(self.jedenhrac, '<ButtonPress>', self.spustenie_hry)
        self.canvas.tag_bind(self.jedenhracT, '<ButtonPress>', self.spustenie_hry)
        self.canvas.tag_bind(self.dvajahraci, '<ButtonPress>', self.spustenie_hry)
        self.canvas.tag_bind(self.dvajahraciT, '<ButtonPress>', self.spustenie_hry)
        self.canvas.tag_bind(self.trajahraciT, '<ButtonPress>', self.spustenie_hry)
        self.canvas.tag_bind(self.styriahraci, '<ButtonPress>', self.spustenie_hry)
        self.canvas.tag_bind(self.styriahraciT, '<ButtonPress>', self.spustenie_hry)

    def je_ulozena_hra(self):
        subor = open('save.txt', 'r')
        if len(subor.read()) != 0:
            return 1
        return 0

    def spustenie_hry(self, event):
        self.chcem_hrat_zo_savu = 0
        item = self.canvas.find_closest(event.x, event.y)
        if '1' in self.canvas.gettags(item):
            self.pocetHracov = 1
        elif '2' in self.canvas.gettags(item):
            self.pocetHracov = 2
        elif '3' in self.canvas.gettags(item):
            self.pocetHracov = 3
        elif '4' in self.canvas.gettags(item):
            self.pocetHracov = 4
        elif 'save' in self.canvas.gettags(item):
            self.pocet_hracov_pri_save()
            self.chcem_hrat_zo_savu = 1
        self.zacni_hru()

    def pocet_hracov_pri_save(self):
        subor = open('save.txt', 'r')
        x = 0
        for riadok in subor:
            x += 1
            if len(riadok) == 2:
                self.index_aktualneho_hraca = int(riadok)

        self.pocetHracov = x // 4
        subor.close()

    def nacitanie_stavu(self):
        subor = open('save.txt', 'r')
        pandrlaci = ()
        for riadok in subor:
            y = riadok.split()
            pandrlaci += (y,)
        for i in range(len(pandrlaci) - 1):
            hrac = int(pandrlaci[i][0])
            i_f = int(pandrlaci[i][1])

            if int(pandrlaci[i][4]) != 0:
                self.zoznam_hracov[hrac].figurky[i_f].pozicia = int(pandrlaci[i][4])
                self.zoznam_hracov[hrac].figurky[i_f].pozicia_v_hernej_ploche = \
                self.zoznam_hracov[hrac].figurky[i_f].hp[int(pandrlaci[i][4])]
                self.zoznam_hracov[hrac].spawnni_figurku(i_f, int(pandrlaci[i][4]))
            elif int(pandrlaci[i][4]) == 0 and int(pandrlaci[i][5]) == 1:
                self.zoznam_hracov[hrac].spawnni_figurku(i_f, int(pandrlaci[i][4]))

        subor.close()

    def zacni_hru(self):
        self.canvas.delete('all')
        self.vykresli_plochu()

        self.obrazky_kocky = []
        self.obrazky_figuriek = []
        self.miesta = []
        for i in range(1, 7):
            self.obrazky_kocky.append(tkinter.PhotoImage(file=f'images/{i}.gif'))
        for j in 'r', 'y', 'm', 'g':
            obr = tkinter.PhotoImage(file=f'images/{j}.png')
            self.obrazky_figuriek.append(obr)
        self.counter_miest = 1
        self.kliknutie = 0
        self.pridaj_hracov(self.pocetHracov)
        self.pridaj_kocku()
        if self.chcem_hrat_zo_savu == 1:
            self.nacitanie_stavu()
        else:
            self.index_aktualneho_hraca = 0
        self.aktualny_hrac = self.zoznam_hracov[self.index_aktualneho_hraca]
        self.aktualny_hrac_text = self.canvas.create_text(310, 100, text=f'{self.aktualny_hrac.text} move',
                                                          font='Arial 14', fill=self.aktualny_hrac.c)
        self.aktualny_stav_hry = self.canvas.create_text(300, 200, text=f' click on playing dice', font='Arial 14',
                                                         fill='blue')
        self.ulozenie_hry = self.canvas.create_rectangle(700, 800, 820, 850, fill="grey40", outline="grey60",
                                                         tags=('uloz'))
        self.ulozenie_hryT = self.canvas.create_text(760, 825, text="save game", font='arial 15', tags=('uloz'))
        self.canvas.tag_bind(self.ulozenie_hry, '<ButtonPress>', self.ulozit_hru)
        self.canvas.tag_bind(self.ulozenie_hryT, '<ButtonPress>', self.ulozit_hru)

    def ulozit_hru(self, event):
        item = self.canvas.find_closest(event.x, event.y)
        if 'uloz' in self.canvas.gettags(item):
            subor = open('save.txt', 'w', encoding='utf-8')
            for i in range(len(self.zoznam_hracov)):
                for j in range(len(self.zoznam_hracov[i].figurky)):
                    print(i, j, self.zoznam_hracov[i].figurky[j].pozicia_v_hernej_ploche,
                          self.zoznam_hracov[i].figurky[j].pozicia, self.zoznam_hracov[i].figurky[j].spawn, file=subor)
            print(self.index_aktualneho_hraca, file=subor)

    def updatni_aktualneho_hraca(self):
        pocetHracov = len(self.zoznam_hracov)
        if pocetHracov != 0:
            self.index_aktualneho_hraca = (self.index_aktualneho_hraca + 1) % pocetHracov
            self.aktualny_hrac = self.zoznam_hracov[self.index_aktualneho_hraca]
            self.canvas.itemconfig(self.aktualny_hrac_text, text=f'{self.aktualny_hrac.text} move',
                                   fill=self.aktualny_hrac.c)
        else:
            self.canvas.delete('all')
            x, y = 550, 300
            for i in range(len(self.miesta)):
                self.canvas.create_text(x, y, text=self.miesta[i][0], font='Arial 30', fill=self.miesta[i][1])
                y += 100

    def vykresli_spawny(self, zoznam, x1, y1, r, posun, farba):
        s = 0
        for i in range(2):
            self.canvas.create_oval(x1 - r, y1 - r, x1 + r, y1 + r, fill=farba, width=4)
            zoznam.append(Policko(x1, y1, s))
            x1 += posun
            s += 1
        y1 += posun
        x1 -= 2 * posun
        for i in range(2):
            self.canvas.create_oval(x1 - r, y1 - r, x1 + r, y1 + r, fill=farba, width=4)
            zoznam.append(Policko(x1, y1, s))
            x1 += posun
            s += 1

    def pridaj_hracov(self, pocet_hracov):
        self.zoznam_hracov = []
        for i in range(int(pocet_hracov)):
            if i == 0:
                hp = self.policka + self.policka_c
                sp = self.spawny_cervenych
                farba = 'r'
                text = 'red'
                c = 'tomato'
            elif i == 1:
                hp = self.policka[10:] + self.policka[:10] + self.policka_zl
                sp = self.spawny_zltych
                farba = 'y'
                text = 'yellow'
                c = 'yellow'
            elif i == 3:
                hp = self.policka[30:] + self.policka[:30] + self.policka_ze
                sp = self.spawny_zelenych
                farba = 'g'
                text = 'green'
                c = 'green'
            elif i == 2:
                hp = self.policka[20:] + self.policka[:20] + self.policka_mo
                sp = self.spawny_modrych
                farba = 'b'
                text = 'blue'
                c = 'blue'
            hrac1 = Hrac(self.canvas, i, farba, self.obrazky_figuriek[i], hp, sp, self.po_pohnuti_figurky, text, c)
            self.zoznam_hracov.append(hrac1)

            for figurka in hrac1.figurky:
                self.canvas.tag_bind(figurka.obrazok, '<ButtonPress>', self.pohni_figurku)

    def pridaj_kocku(self):
        self.kocka = self.canvas.create_image(535, 495, image=self.obrazky_kocky[0], tags=('kocka'))
        self.canvas.tag_bind(self.kocka, '<ButtonPress>', self.kliknutie_na_kocku)

    def miesanie_kocky(self):
        if self.testik != 10:
            self.testik += 1
            self.canvas.itemconfig(self.kocka, image=self.obrazky_kocky[self.testik % 6])
            self.canvas.after(100, self.miesanie_kocky)
        else:
            index = random.randrange(0, 6)
            self.posun = index + 1
            self.canvas.itemconfig(self.kocka, image=self.obrazky_kocky[index])
            if self.posun != 6 and (self.ma_spawnutu_figurku() == 0 or self.ma_sa_kam_pohnut() == 0):
                self.kliknutie = 0
                self.canvas.itemconfig(self.aktualny_stav_hry, text=f'click on playing dice')
                self.updatni_aktualneho_hraca()

    def ma_sa_kam_pohnut(self):
        c = 0
        for figurka in self.aktualny_hrac.figurky:
            if (figurka.spawn == 1 and self.aktualny_hrac.pozicia_je_volna(
                    figurka.pozicia + self.posun) == 0) or figurka.spawn == 0:
                c += 1
        if c == 4:
            return 0
        return 1

    def kliknutie_na_kocku(self, event):
        item = self.canvas.find_closest(event.x, event.y)

        if self.kliknutie == 0 and 'kocka' in self.canvas.gettags(item):
            self.kliknutie = 1
            self.testik = 0
            self.miesanie_kocky()
            self.canvas.itemconfig(self.aktualny_stav_hry, text=f'click on figure')

    def pohni_figurku(self, event):
        item = self.canvas.find_closest(event.x, event.y)
        farba, i = self.canvas.gettags(item)[0], int(self.canvas.gettags(item)[1])
        if self.aktualny_hrac.farba == farba:
            if self.kliknutie == 1 and self.aktualny_hrac.figurky[i].spawn == 1:

                self.aktualny_hrac.pohni_figurku_hraca(self.posun, item, i)
            elif self.kliknutie == 1 and self.posun == 6 and (
                    self.ma_spawnutu_figurku() == 0 or self.aktualny_hrac.figurky[i].spawn == 0) and \
                    self.aktualny_hrac.figurky[i].je_v_domceku == 0:
                if self.aktualny_hrac.je_volny_spawn(i) == 1:
                    self.aktualny_hrac.spawnni_figurku(i)
                    self.aktualny_hrac.figurky[i].spawn = 1
                    self.po_pohnuti_figurky(self.aktualny_hrac.figurky[i])

    def po_pohnuti_figurky(self, figurka):
        if figurka != None:
            self.je_na_pozicii_iny_hrac(figurka)
        self.kliknutie = 0
        self.skontroluj_ci_aktualny_hrac_nedohral()
        if self.posun != 6:
            self.updatni_aktualneho_hraca()

        self.canvas.itemconfig(self.aktualny_stav_hry, text=f'click on playing dice')

    def skontroluj_ci_aktualny_hrac_nedohral(self):
        c = 0
        for figurka in self.aktualny_hrac.figurky:
            if figurka.je_v_domceku == 1:
                c += 1
        if c == 4:
            self.miesta.append((f'{self.aktualny_hrac.text} is on  {self.counter_miest}. place', self.aktualny_hrac.c))
            self.zoznam_hracov.pop(self.zoznam_hracov.index(self.aktualny_hrac))
            self.counter_miest += 1

    def je_na_pozicii_iny_hrac(self, figurka):
        for i in range(len(self.zoznam_hracov)):
            if self.aktualny_hrac != self.zoznam_hracov[i]:
                druhy_hrac = self.zoznam_hracov[i]
                for j in range(len(druhy_hrac.figurky)):
                    if druhy_hrac.figurky[j].spawn == 1:
                        x, y = druhy_hrac.figurky[j].pozicia_v_hernej_ploche, figurka.pozicia_v_hernej_ploche
                        if (druhy_hrac.figurky[j].pozicia_v_hernej_ploche == figurka.pozicia_v_hernej_ploche):
                            druhy_hrac.despawnni_figurku(j)

    def ma_spawnutu_figurku(self):
        for figurka in self.aktualny_hrac.figurky:
            if figurka.spawn == 1:
                return 1
        return 0

    def vykresli_plochu(self):
        ## vykreslenie plochy
        x1, y1, r, posun = 85, 405, 40, 90
        index = 0
        self.policka = []
        self.policka_c = []
        self.policka_zl = []
        self.policka_ze = []
        self.policka_mo = []
        for i in range(1, 13):
            # self.policka.append(Policko(x1, y1, x2, y2, i))
            if i == 1 or i == 3 or i == 5:
                if i == 1:
                    x = 4
                elif i == 3:
                    x = 2
                elif i == 5:
                    x = 4
                for j in range(x):
                    if i == 1 and j == 0:
                        self.canvas.create_oval(x1 - r, y1 - r, x1 + r, y1 + r, fill='tomato', width=4)
                        self.canvas.create_line(x1 - r + 10, y1, x1 + r - 10, y1, arrow='last', width=3)
                    else:

                        self.canvas.create_oval(x1 - r, y1 - r, x1 + r, y1 + r, fill='white', width=4)
                    self.policka.append(Policko(x1, y1, index))
                    index += 1
                    x, y = x1 + r, y1
                    x1 += posun
                    self.canvas.create_line(x, y, x1, y1, width=5)
                    if j == 0 and i == 1:
                        self.canvas.create_line(x - r, y + r, x - r, y + 2 * r, width=5)

                    if j == 1 and i == 3:

                        x2 = x1 - posun
                        y2 = y1 + posun

                        for i in range(4):
                            self.canvas.create_oval(x2 - r, y2 - r, x2 + r, y2 + r, fill='yellow', width=4)
                            self.policka_zl.append(Policko(x2, y2, i))
                            y2 += posun

            elif i == 2 or i == 10 or i == 12:
                if i == 2:
                    x = 4
                elif i == 10:
                    x = 4
                elif i == 12:
                    x = 2
                for j in range(x):
                    if i == 10 and j == 0:
                        self.canvas.create_oval(x1 - r, y1 - r, x1 + r, y1 + r, fill='green', width=4)
                        self.canvas.create_line(x1, y1 - r + 10, x1, y1 + r - 10, arrow='first', width=3)
                    else:
                        self.canvas.create_oval(x1 - r, y1 - r, x1 + r, y1 + r, fill='white', width=4)
                    self.policka.append(Policko(x1, y1, index))
                    index += 1
                    x, y = x1, y1 - r
                    y1 -= posun
                    if j == 1 and i == 12:
                        pass
                    else:
                        self.canvas.create_line(x, y, x1, y1, width=5)

                    if i == 12 and j == 1:
                        y1 += posun
                        x1 += posun
                        for i in range(4):
                            self.canvas.create_oval(x1 - r, y1 - r, x1 + r, y1 + r, fill='tomato', width=4)
                            self.policka_c.append(Policko(x1, y1, i))
                            x1 += posun


            elif i == 4 or i == 6 or i == 8:
                if i == 4:
                    x = 4
                elif i == 6:
                    x = 2
                elif i == 8:
                    x = 4
                for j in range(x):
                    if i == 4 and j == 0:
                        self.canvas.create_oval(x1 - r, y1 - r, x1 + r, y1 + r, fill='yellow', width=4)
                        self.canvas.create_line(x1, y1 - r + 10, x1, y1 + r - 10, arrow='last', width=3)
                    else:
                        self.canvas.create_oval(x1 - r, y1 - r, x1 + r, y1 + r, fill='white', width=4)
                    self.policka.append(Policko(x1, y1, index))
                    index += 1
                    x, y = x1, y1 + r
                    y1 += posun
                    self.canvas.create_line(x, y, x1, y1, width=5)
                    if i == 6 and j == 1:
                        x2 = x1 - posun
                        y2 = y1 - posun

                        for i in range(4):
                            self.canvas.create_oval(x2 - r, y2 - r, x2 + r, y2 + r, fill='blue', width=4)
                            self.policka_mo.append(Policko(x2, y2, i))
                            x2 -= posun
            elif i == 7 or i == 9 or i == 11:
                if i == 7:
                    x = 4
                elif i == 9:
                    x = 2
                elif i == 11:
                    x = 4
                for j in range(x):
                    if i == 7 and j == 0:
                        self.canvas.create_oval(x1 - r, y1 - r, x1 + r, y1 + r, fill='blue', width=4)
                        self.canvas.create_line(x1 - r + 10, y1, x1 + r - 10, y1, arrow='first', width=3)
                    else:
                        self.canvas.create_oval(x1 - r, y1 - r, x1 + r, y1 + r, fill='white', width=4)
                    self.policka.append(Policko(x1, y1, index))
                    index += 1
                    x, y = x1 - r, y1
                    x1 -= posun
                    self.canvas.create_line(x, y, x1, y1, width=5)
                    if i == 9 and j == 1:
                        x2 = x1 + posun
                        y2 = y1 - posun

                        for i in range(4):
                            self.canvas.create_oval(x2 - r, y2 - r, x2 + r, y2 + r, fill='green', width=4)
                            self.policka_ze.append(Policko(x2, y2, i))
                            y2 -= posun

        ## vykreslenie spawnov

        self.spawny_zelenych = []
        self.spawny_cervenych = []
        self.spawny_modrych = []
        self.spawny_zltych = []
        self.vykresli_spawny(self.spawny_zelenych, 85, 805, 40, 90, 'green')
        self.vykresli_spawny(self.spawny_cervenych, 85, 105, 40, 90, 'tomato')
        self.vykresli_spawny(self.spawny_modrych, 895, 805, 40, 90, 'blue')
        self.vykresli_spawny(self.spawny_zltych, 895, 105, 40, 90, 'yellow')


Program()
