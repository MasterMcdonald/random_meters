"""
@Author: Zelan Xiang
@Editor: Zelan Xiang
    GUI: Tkinter
    Database: MySQL
"""
#-*- coding: UTF-8 -*-

import random
from Tkinter import *
import MySQLdb

def insertvalue(value1, value2, value3, value4):
    """
    Inserte one meter's data to table
    """
    volume = float(value1)
    press = float(value2)
    rate = float(value3)
    level = float(value4)
    sql_words = "INSERT INTO TEMP1\
                 (TOTAL_VOLUME, PRESSURE, INSTANTANEOUS_FLOW_RATE, METER_LEVEL)\
                 VALUES(%s, %s, %s, %s)" % (volume, press, rate, level)
    CUR.execute(sql_words)
    CMS.commit()


def firstmeter(value1, value2, value3, value4):
    """
    Strat random all meters' data
    """
    totalvolume = float(value1)
    pressure = float(value2)
    flowrate = float(value3)
    meterlevel = list(str(value4))
    meterlist = []
    index = 1
    for item in meterlevel:
        meterlist.append(int(item))
    for i in meterlist:
        flag = 1
        if index == 1:
            insertvalue(totalvolume, pressure, flowrate, index)
        else:
            totalvolume = totalvolume - random.uniform(0, totalvolume/100)
            if random.uniform(0, 10) > 9.9998:
                totalvolume = totalvolume - random.uniform(totalvolume/10, totalvolume/2)
                flag = 2
            pressure = pressure + random.uniform(0-pressure/4, pressure/4)
            flowrate = float(200) * (1 + pressure/float(value2))
            for k in range(i+1):
                if i == 0:
                    pressure = pressure + random.uniform(0-pressure/4, pressure/4)
                    if flag == 2:
                        pressure = random.uniform(0.1, 0.8)
                    flowrate = float(200) * (1 + pressure/float(value2))
                    insertvalue(totalvolume, pressure, flowrate, index)
                elif k != i:
                    num = random.uniform(0-totalvolume/100, totalvolume/100)
                    tva = random.uniform(totalvolume/(5*(i+1)), totalvolume/(i+1)+num)
                    totalvolume = totalvolume - tva
                    pressure = pressure + random.uniform(0-pressure/4, pressure/4)
                    if flag == 2:
                        pressure = pressure + random.uniform(0-pressure/4, pressure/4)
                    flowrate = float(200) * (1 + pressure/float(value2))
                    insertvalue(tva, pressure, flowrate, index)
            flag = 1
        index = index +1
    insertvalue(0, 0, 0, 0)
    CUR.execute("SELECT * FROM TEMP1")
    exlist = CUR.fetchall()
    for item in exlist:
        print item
    VALUE1_BOX.delete(0, 6)
    VALUE2_BOX.delete(0, 6)
    VALUE3_BOX.delete(0, 6)


#READY TO CONNECT DATABASE
CMS = MySQLdb.connect('127.0.0.1', 'root', 'Xiang918', 'Chatus')
CUR = CMS.cursor()
#FIRST TABLE
CUR.execute("DROP TABLE IF EXISTS TEMP1")
CUR.execute("CREATE TABLE TEMP1\
             (ID INT PRIMARY KEY AUTO_INCREMENT, TOTAL_VOLUME FLOAT, PRESSURE FLOAT,\
             INSTANTANEOUS_FLOW_RATE FLOAT, METER_LEVEL FLOAT)")
CMS.commit()
#GUI
ROOT = Tk()
ROOT.title('GIVE VALUES')

BIGFRAME1 = Frame(ROOT)
BIGFRAME2 = Frame(ROOT)
FRAME1 = Frame(BIGFRAME1)
FRAME2 = Frame(BIGFRAME1)

LINE1 = Frame(FRAME1)
LINE2 = Frame(FRAME1)
LINE3 = Frame(FRAME2)
LINE4 = Frame(FRAME2)

VALUE1_TEXT = Label(LINE1, text='     Total:')
VALUE1_BOX = Entry(LINE1)
VALUE1_TEXT.pack(side=LEFT)
VALUE1_BOX.pack(side=RIGHT)

VALUE2_TEXT = Label(LINE2, text='Pressure:')
VALUE2_BOX = Entry(LINE2)
VALUE2_TEXT.pack(side=LEFT)
VALUE2_BOX.pack(side=RIGHT)

LINE1.pack(side=TOP)
LINE2.pack(side=BOTTOM)

VALUE3_TEXT = Label(LINE3, text='      Rate:')
VALUE3_BOX = Entry(LINE3)
VALUE3_TEXT.pack(side=LEFT)
VALUE3_BOX.pack(side=RIGHT)

VALUE4_TEXT = Label(LINE4, text='  Value 4:')
VALUE4_BOX = Entry(LINE4)
VALUE4_TEXT.pack(side=LEFT)
VALUE4_BOX.pack(side=RIGHT)

LINE3.pack(side=TOP)
LINE4.pack(side=BOTTOM)

INSERT_BUTTON = Button(BIGFRAME2,
                       text='INSERT',
                       width=10,
                       height=2,
                       font=('Arial', 13, "bold"),
                       fg='white',
                       bg='DarkOrange',
                       command=lambda:
                       firstmeter(VALUE1_BOX.get(),
                                  VALUE2_BOX.get(),
                                  VALUE3_BOX.get(),
                                  VALUE4_BOX.get())
                      )
INSERT_BUTTON.pack()

FRAME1.pack(side=TOP)
FRAME2.pack(side=BOTTOM)
BIGFRAME1.pack(side=TOP)
BIGFRAME2.pack(side=TOP)

ROOT.mainloop()
