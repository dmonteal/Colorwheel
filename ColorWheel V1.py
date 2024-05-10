# -*- coding: utf-8 -*-
"""
Created on Wed May  3 09:46:07 2023

@author: dmont
"""

import PySimpleGUI as sg
import traceback
from pathlib import Path
import pylab as py

MAX_ROWS = MAX_COL = 4
hand = 3
time = 0
combo = 0

score = 0

iconpath = str(Path.cwd())+'\icons\\'
sets = sg.UserSettings(path=Path.cwd(),filename='config.ini',use_config_file=True,convert_bools_and_none=True)
HS = sets['HS']['HS'].split(',')
Names = sets['HS']['Names'].split(',')

ticon = ['P_No.png',
         'P_R.png','P_O.png','P_Y.png','P_G.png','P_B.png','P_P.png',
         'P_PO.png','P_RY.png','P_OG.png','P_YB.png','P_GP.png','P_BR.png',
         'P_All.png']
cicon = ['c_Red.png','c_Orange.png','c_Yellow.png','c_Green.png','c_Blue.png','c_Purple.png']

picon = ['P_can.png','P_cannot.png']

tpos = []
for t in ticon:
    tpos.append(iconpath+t)

tcol = []
for t in cicon:
    tcol.append(iconpath+t)

tposo = []
for t in picon:
    tposo.append(iconpath+t)

def grids(index,mr,mc):
    return [[sg.ReadFormButton(key=(index, row,col),image_filename=tpos[13],image_size=(80,80),button_color='Black', pad=(0,0), border_width=0,button_text='') for col in range(mc)] for row in range(mr)]

def gridsim(index,mr,mc):
    return [[sg.Image(tposo[0],size=(70,10),key=(index, row,col)) for col in range(mc)] for row in range(mr)]

def lay():
    return [[sg.Text('Time: 0.0',key='time',font=("Helvetica", 30)),sg.Text('',key='com',font=("Helvetica", 30))],
              [sg.Frame('',[[sg.Column(grids(0,MAX_ROWS,MAX_COL)),
               sg.Image(iconpath+"colorwheel.PNG",size=(320,320))]])],
              grids(1,1,hand),
              gridsim(3,1,hand),
              [sg.Button(button_text='Reset',key='reset',size=(20,1))]]
def enlay():
    return [[sg.Text('Hi',key='score')],
           [sg.Input('AAA',key='name')],
           [sg.Text('Do you want to play again?')],
           [sg.Button(button_text='Yes',key='Yes'),sg.Button(button_text='No',key='No')]]

def upnei(e,v):
    adj = [[-1,0],[1,0],[0,-1],[0,1]]
    for ad in adj:
        if e[1]+ad[0] >= 0 and e[1]+ad[0] < MAX_ROWS and\
           e[2]+ad[1] >= 0 and e[2]+ad[1] < MAX_COL:
               a = (e[0],e[1]+ad[0],e[2]+ad[1])
               if not vals[a[1],a[2]] > 0:
                   p = chnei(a)
                   vals[a[1],a[2]] = p
                   window[a].update(image_size=(80,80), image_filename=tpos[-p])

def chnei(e):
    pos = [1,2,3,4,5,6]
    adj = [[-1,0],[1,0],[0,-1],[0,1]]
    for ad in adj:
        if e[1]+ad[0] >= 0 and e[1]+ad[0] < MAX_ROWS and\
           e[2]+ad[1] >= 0 and e[2]+ad[1] < MAX_COL:
               a = (e[1]+ad[0],e[2]+ad[1])
               if vals[a[0],a[1]] > 0:
                   pos = [p for p in pos if abs(p-vals[a[0],a[1]]) == 1 or abs(p-vals[a[0],a[1]]) == 5]
    if len(pos) == 2:
        return -(pos[0]+1+6)*(pos[1]==pos[0]+2)\
               -(1+6)*(pos == [2,6])\
               -(6+6)*(pos == [1,5])
    elif len(pos) == 1:
        return -pos[0]
    else:
        return 0
    
def chposs(p):
    poss = [0]*len(p)
    # if min(vals.flatten()) == -13: return True
    for r in range(len(vals)):
        for c in range(len(vals[0])):
            bv = vals[r][c]
            if bv >= 0: continue
            for i,nc in enumerate(p):
                if min(vals.flatten()) == -13:
                    poss[i] += 1
                    continue
                if bv > -7 and not -bv == nc: continue
                if bv > -13 and bv <-6:
                   if bv == -7: 
                       if not (nc == 2 or nc == 6): 
                           continue
                   elif bv == -12: 
                       if not (nc == 1 or nc == 5):
                           continue
                   elif not ((-bv)-6-1 == nc or (-bv)-6+1 == nc):
                       continue
                poss[i] +=1
    return poss

def diposs(nc):
    for r in range(len(vals)):
        for c in range(len(vals[0])):
            bv = vals[r][c]
            if bv >= 0: continue
            
            poss = True
            if bv > -7 and not -bv == nc: poss = False
            if bv > -13 and bv <-6:
               if bv == -7: 
                   if not (nc == 2 or nc == 6): 
                       poss = False
               elif bv == -12: 
                   if not (nc == 1 or nc == 5):
                       poss = False
               elif not ((-bv)-6-1 == nc or (-bv)-6+1 == nc):
                   poss = False
            
            if poss:
                window[(0,r,c)].update(image_size=(80,80), image_filename=tpos[-bv])
            else:
                window[(0,r,c)].update(image_size=(80,80), image_filename=tpos[0])
    return 0
    
sg.theme('Black')

cc = 0

def setup(window=None):
    try:
        window.close()
    except:
        print('new game')
    
    vals = py.ones((MAX_ROWS,MAX_COL),dtype=int)*-13
    p1han = [0]*hand
    
    # Create the Window
    window = sg.Window('Color Wheel (David Montealegre)', lay(),finalize=True, element_justification='c',icon=r''+iconpath+"colorwheel.ico")
    
    for h in range(hand):
        nc = py.randint(6)+1
        p1han[hand-h-1] = nc
        window[(1,0,hand-h-1)].update(image_size=(80,80), image_filename=tcol[nc-1],button_color='Black')
        window[(1,0,cc)].update(button_color='White')
    return window, vals, p1han

window, vals, p1han = setup()
nc = p1han[cc]

while True:
    try:
        event, values = window.read(timeout=84)
        
        if event == sg.WIN_CLOSED: # if user closes window or clicks cancel
            break
        
        if time:
            time += 1
            window['time'].update('Time: %.1fs'%(time/10))
        
        if not combo:
            window['com'].update('')
            
        if min(vals.flatten()) >= 0 or max(chposs(p1han)) == 0:
            tsc = int(200/(1+time/100))
            score += tsc*(tsc>0)\
                     +25*(len(vals.flatten()[vals.flatten()>0])-int(MAX_ROWS*MAX_COL/2))\
                     +(min(vals.flatten()) > 0)*100
            esw = sg.Window('', enlay(),finalize=True,icon=r''+iconpath+"colorwheel.ico")
            esw['score']\
                ("High Scores:\n#1: %s\t%s\n#2: %s\t%s\n#3: %s\t%s\n#4: %s\t%s\n#5: %s\t%s\nYour score is %i"%(\
                  HS[0],Names[0],\
                  HS[1],Names[1],\
                  HS[2],Names[2],\
                  HS[3],Names[3],\
                  HS[4],Names[4],score))
            while True:
                eevent, evalues = esw.read()
                if eevent == sg.WIN_CLOSED or eevent == 'Yes': # if user closes window or clicks cancel
                    break
                if eevent == 'No':
                    break
            esw.close()
            for i in range(len(HS)):
                if score > int(HS[i]):
                    HS = HS[0:i]+[str(score)]+HS[i:-1]
                    name = str(evalues['name'])                    
                    Names = Names[0:i]+[name]+Names[i:-1]
                    break
            uphs = HS[0]
            upns = Names[0]
            for i in range(len(HS)-1):
                uphs += ','+HS[i+1]
                upns += ','+Names[i+1]
            sets['HS']['HS'] = uphs
            sets['HS']['Names'] = upns
            
            if eevent == 'No':
                break
            
            window,vals,p1han = setup(window)
            nc = p1han[cc]
            time,score,combo = 0,0,0
        
        if event == 'reset':
            window,vals,p1han = setup(window)
            nc = p1han[cc]
            time,score,combo = 0,0,0
        
        if event[0] == 0:
            if not time: time += 1
            combo +=1
            if combo > 1:
                window['com'].update('Combo %ix'%(combo))
            
            bv = vals[event[1],event[2]]
            if bv < 0:
                val = nc
                if bv > -7 and not -bv == nc: continue
                if bv > -13 and bv <-6:
                   if bv == -7: 
                       if not (nc == 2 or nc == 6): 
                           continue
                   elif bv == -12: 
                       if not (nc == 1 or nc == 5):
                           continue
                   elif not ((-bv)-6-1 == nc or (-bv)-6+1 == nc):
                       continue
                          
                window[event].update(image_size=(80,80), image_filename=tcol[val-1])
                vals[event[1],event[2]] = val
                upnei(event,val)
                
                nc = py.randint(6)+1
                p1han[cc] = nc
                window[(1,0,cc)].update(image_size=(80,80), image_filename=tcol[nc-1])
                
                diposs(nc)
                
                possible = chposs(p1han)
                for i in range(len(possible)):
                    window[(3,0,i)].update(tposo[possible[i]==0],size=(70,10))
        if event[0] == 1:
            if combo > 1:
                score += combo*5
            combo = 0
            
            window[(1,0,cc)].update(button_color='Black')
            cc = event[2]
            nc = p1han[cc]
            window[(1,0,cc)].update(button_color='White')
            diposs(nc)
    except Exception as e:
        tb = traceback.format_exc()
        sg.popup_error(f'AN EXCEPTION OCCURRED!', e, tb)
        break

window.close()