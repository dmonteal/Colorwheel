# -*- coding: utf-8 -*-
"""
Created on Wed May  3 09:46:07 2023

@author: dmont
"""

import PySimpleGUI as sg
import traceback
from pathlib import Path
import pylab as py

MAX_ROWS = MAX_COL = 5
stps = [[1,1],[3,1],[1,3],[3,3]]
hand = 3

iconpath = str(Path.cwd())+'\icons\\'

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
    return [[sg.Frame('',[[sg.Column(grids(0,MAX_ROWS,MAX_COL)),
               sg.Image(iconpath+"colorwheel.PNG",size=(320,320))]])],
              [[sg.Image(iconpath+"P1.PNG",size=(87,30))]+grids(1,1,hand)[0]+\
               [sg.Image(iconpath+"P2.PNG",size=(87,30))]+grids(2,1,hand)[0]],
              [[sg.Image("",size=(87,1))]+gridsim(3,1,hand)[0]+\
               [sg.Image("",size=(87,1))]+gridsim(4,1,hand)[0]],
              [sg.Button(button_text='Reset',key='reset',size=(20,1))]]
def enlay():
    return [[sg.Text('Hi',key='score')],
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
                    if not (1+(-bv-6+1-1)%6 == nc or 1+(-bv-6-1-1)%6 == nc):
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
                if not (1+(-bv-6+1-1)%6 == nc or 1+(-bv-6-1-1)%6 == nc):
                    poss = False
            
            if poss:
                window[(0,r,c)].update(image_size=(80,80), image_filename=tpos[-bv])
            else:
                window[(0,r,c)].update(image_size=(80,80), image_filename=tpos[0])
    return 0
    
sg.theme('Black')

cp = 1
ccs = [0,0]

def setup(window=None):
    try:
        window.close()
    except:
        print('new game')
    
    vals = py.ones((MAX_ROWS,MAX_COL),dtype=int)*-13
    
    p1han = [0]*hand
    p2han = [0]*hand
    
    # Create the Window
    window = sg.Window('Color Wheel (David Montealegre)', lay(),finalize=True, element_justification='c',icon=r''+iconpath+"colorwheel.ico")
        
    for h in range(hand):
        p1han[hand-h-1] = py.randint(6)+1
        p2han[hand-h-1] = py.randint(6)+1
        window[(1,0,hand-h-1)].update(image_size=(80,80), image_filename=tcol[p1han[hand-h-1]-1],button_color='Black')
        window[(2,0,hand-h-1)].update(image_size=(80,80), image_filename=tcol[p2han[hand-h-1]-1],button_color='Black')
    window[(cp,0,ccs[cp-1])].update(button_color='White')
    
    return window, vals, [p1han, p2han]

def randomize():
    for stp in stps:
        vals[stp[0]][stp[1]] = py.randint(6)+1
    for r in range(MAX_ROWS):
        for c in range(MAX_COL):
            if vals[r][c] < 1:
                window[(0,r,c)].update(image_size=(80,80), image_filename=tpos[-vals[r][c]])
            else:
                window[(0,r,c)].update(image_size=(80,80), image_filename=tcol[vals[r][c]-1])
                upnei((0,r,c),vals[r][c])
    
window, vals, phan = setup()
nc = phan[cp-1][ccs[cp-1]]

randomize()

while True:
    try:
        event, values = window.read(timeout=84)
        
        if event == sg.WIN_CLOSED: # if user closes window or clicks cancel
            break
        
            
        if min(vals.flatten()) >= 0 or max(chposs(phan[cp-1])) == 0:

            esw = sg.Window('', enlay(),finalize=True,element_justification='c',icon=r''+iconpath+"colorwheel.ico")
            esw['score']\
                ("P%i Wins!!!"%(3-cp))
            while True:
                eevent, evalues = esw.read()
                if eevent == sg.WIN_CLOSED or eevent == 'Yes': # if user closes window or clicks cancel
                    break
                if eevent == 'No':
                    break
            esw.close()
            
            if eevent == 'No':
                break
            
            window,vals,phan = setup(window)
            randomize()
            nc = phan[cp-1][ccs[cp-1]]
        
        if event == 'reset':
            window,vals,phan = setup(window)
            randomize()
            nc = phan[cp-1][ccs[cp-1]]
        
        if event[0] == 0:
            
            bv = vals[event[1],event[2]]
            if bv < 0:
                val = nc
                if bv > -7 and not -bv == nc: continue
                if bv > -13 and bv <-6:
                    if not (1+(-bv-6+1-1)%6 == nc or 1+(-bv-6-1-1)%6 == nc):
                       continue
                          
                window[event].update(image_size=(80,80), image_filename=tcol[val-1])
                vals[event[1],event[2]] = val
                upnei(event,val)
                
                phan[cp-1][ccs[cp-1]] = 1+nc%6
                window[(cp,0,ccs[cp-1])].update(image_size=(80,80), image_filename=tcol[phan[cp-1][ccs[cp-1]]-1], button_color = 'Black')
                
                possible = chposs(phan[cp-1])
                for i in range(len(possible)):
                    window[(cp+2,0,i)].update(tposo[possible[i]==0],size=(70,10))
                
                cp = 3 - cp
                window[(cp,0,ccs[cp-1])].update(button_color = 'White')
                
                nc = phan[cp-1][ccs[cp-1]]
                
        if event[0] == cp:
            
            window[(cp,0,ccs[cp-1])].update(button_color='Black')
            ccs[cp-1] = event[2]
            nc = phan[cp-1][ccs[cp-1]]
            window[(cp,0,ccs[cp-1])].update(button_color='White')
    except Exception as e:
        tb = traceback.format_exc()
        sg.popup_error(f'AN EXCEPTION OCCURRED!', e, tb)
        break

window.close()