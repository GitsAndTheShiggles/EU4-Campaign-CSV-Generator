# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 18:20:24 2020

@author: Scott Soldavini
"""
import re
import os

#To use this program, put each unzipped save file into a single folder somewhere on your desktop, and save the path to the folder to your clipboard.
#You can then ask it to compile a set of dictionaries for a specific variable, tying a playername to a specific value at a date.
#For example, entering 'army_tradition' will give you a list of player's army tradition.
directory=r""+input("What is the file path to the campaign folder we are parsing?")
check=input("What text proceeds the variable in question in the save file?")
with open('playerdata.csv', 'w') as f:
    f.write("Date, Player Name, " + check + "\n")
for filename in os.scandir(directory):
    line_number=0
    i=0
    u=[]
    v=[]
    dict_of_players=dict()
    checked_var=dict()

    with open(filename) as file:
        file = " ".join([l.rstrip() for l in file]) 
        r = re.split(r'players_countries={',file)
        r = re.split(r'}',r[1])
        r = re.split(r'/" 	/"',r[0])
        r = re.split(r'\t',r[0])
        r.pop(0)
    
    for x in r:
        i+=1
        x=x.strip()
        x=x.strip('"')
        if (i%2) == 0:
            u.append(x)
        else:
            v.append(x)
            
    dict_of_players=dict(zip(u,v))
    for player in dict_of_players.values():
        player=[]


    with open(filename) as file:
        file = " ".join([l.rstrip() for l in file]) 
        for tag in dict_of_players:
            temp=re.search(tag + '={ 		human=',file)
            if type(temp)==re.Match:
                term = re.search(check,file[temp.span()[0]:len(file)])
                end = re.search("\s",file[term.span()[0]+temp.span()[0]:term.span()[0]+100+temp.span()[0]])
                start = re.search("=",file[term.span()[0]+temp.span()[0]:term.span()[0]+100+temp.span()[0]])
                term = file[term.span()[0]+temp.span()[0]+start.span()[1]:end.span()[0]+temp.span()[0]+term.span()[0]]
                checked_var[dict_of_players[tag]]=term
        name=filename.name
        name=re.sub("\D","",name)
        checked_var['Date']=name[0:4]+"/"+name[4:6]+"/"+name[6:8]
        with open('playerdata.csv', 'a') as f:
            for key in checked_var.keys():
                if key != 'Date':
                    f.write("%s, %s, %s\n" % (checked_var['Date'], key, checked_var[key]))
print(dict_of_players)
