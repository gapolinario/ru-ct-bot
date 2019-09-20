# -*- coding: utf-8 -*-
#!/usr/bin/env python4

# no display for matplotlib
import matplotlib as mpl
mpl.use('Agg')

import requests
from datetime import datetime
import re
import time
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

# input is Almoço or Jantar
meal = sys.argv[1]

if meal != "Almoco" and meal != "Jantar":
    print("Meal input is invalid")
    exit(-1)

freq = .5
dia = ('Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo')
mes = ('Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro')
now=datetime.now()
title = "{0:s}_{1:d}_{2:s}_{3:d}_{4:s}".format(now.strftime("%a"), now.day,now.strftime("%B"), now.year, meal[:3])
#human_title = u"{:s}, {:d} de {:s} de {:d}, {:s}".format(dia[now.weekday()], now.day,mes[now.month-1], now.year, meal)
human_title = "{:d} de {:s} de {:d}, {:s}".format( now.day,mes[now.month-1], now.year, meal)

if meal=="Almoco":
    num_hours = 5
    lag = 10
    meal_times = range(10,15)
    # 5*3600 s + 2 min (120 s)
    #secs = 18120 # 5 hours
    secs = 3720 # two hours, 2 min
    label = "Horario do Almoco"
elif meal=="Jantar":
    num_hours = 4
    lag = 17
    meal_times = range(17,21)
    # 4*3600 s + 2 min (120 s)
    label = "Horario do Jantar"
    #secs = 14520 # 4 hours
    secs = 3720 # one hour + 2 min

#secs = 60 # short test
samples = int(secs/freq)            # real case
#samples = 12                         # test case
times = []
sparse_vacancies = [] # raw data from website, some hours will be missing
vacancies = np.empty([num_hours,samples])
total_vacancies = np.empty([samples])
full_vacancies = np.full([num_hours,samples],np.nan)

# real time data acquisition step
for j in range(samples):
    time.sleep(freq)
    now=datetime.now()
    page = requests.get('https://ru.ct.ufrj.br/list/descriptions').text
    #page = open("data-"+str(j)+".html","r").read()
    # subseconds with only 2 digits of precision
    times.append("{0:02d}:{1:02d}:{2:02d}.{3:02d}".format(now.hour,now.minute,now.second,int(str(now.microsecond)[:2])))
    raw_vacancies = re.findall(r'(\d+):00 hrs: <b>(\d+)</b> vagas',page)
    sparse_vacancies.append( [[int(n[0]),int(n[1])] for n in raw_vacancies] )
    #total_vacancies[j] = (int(re.findall(r'(\d+) vagas totais',page)[0]))

for k in range(samples):
    j = 0
    if len(np.transpose(sparse_vacancies[k])) != 0:
        full_vacancies[:,k] = 0
        for h in np.transpose(sparse_vacancies[k])[0]:
            full_vacancies[h-lag,k] = sparse_vacancies[k][j][1]
            j += 1       

df = pd.DataFrame(full_vacancies,columns=times,index=meal_times)

df.to_csv("data/"+title+".csv")

sns.set_context("notebook", font_scale=1.2, rc={"lines.linewidth": 2.5})

p1 = sns.heatmap(df.dropna(axis=1),vmin=0,vmax=300,cmap=sns.color_palette("RdBu_r",n_colors=100))
#p1 = sns.heatmap(df.dropna(axis=1),cmap=sns.color_palette("RdBu_r",n_colors=100))
p1.set(xlabel="Horario de agendamento",ylabel=label)
p1.set_title(human_title)
#plt.show()
fig = p1.get_figure()
fig.tight_layout()
fig.savefig("data/"+title+".png")
