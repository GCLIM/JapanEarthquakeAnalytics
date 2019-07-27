import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.animation import FuncAnimation
from mpl_toolkits.basemap import Basemap

#read datasets to dataframes
df = pd.read_csv('Japan earthquakes 2001 - 2018.csv')
df['time'] = pd.to_datetime(df['time'])
df.sort_values(by=['time'], ascending=True, inplace=True)

#slice dataframes to March 2011
df = df[df['time'].dt.year == 2011]
df = df[df['time'].dt.month == 3]

#initiate E dataframes
E = np.zeros(len(df), dtype=[('time', datetime, 1),
                             ('position',  float, 2),
                             ('magnitude', float, 1)])

E['time'] = pd.to_datetime(df['time'])
E['position'][:,0] = df['longitude']
E['position'][:,1] = df['latitude']
E['magnitude'] = df['mag']

fig = plt.figure(figsize=(10, 10), constrained_layout=True)
ax = plt.subplot(1,1,1)

#draw map
my_map = Basemap(resolution='l',
                 llcrnrlon=df['longitude'].min()+3, llcrnrlat=df['latitude'].min()+5,
                 urcrnrlon=df['longitude'].max()-6, urcrnrlat=df['latitude'].max())
my_map.bluemarble(alpha=0.42)
my_map.drawcoastlines(color='#555566', linewidth=1)

#initiates P dataframes
P = np.zeros(100, dtype=[('time', datetime, 1),
                         ('position', float, 2),
                         ('size',     float, 1),
                         ('growth',   float, 1),
                         ('color',    float, 4)])

#scatter plot
scat = ax.scatter(P['position'][:,0], P['position'][:,1], P['size'], lw=0.5, edgecolors = P['color'], facecolors='None', zorder=10)

#
time_text = ax.text(0.05, 0.90, 'text', fontsize=40, transform = ax.transAxes)

def update(frame):
    current = frame % len(E)
    i = frame % len(P)

    P['color'][:,3] = np.maximum(0, P['color'][:,3] - 1.0/len(P))
    P['size'] += P['growth']

    magnitude = E['magnitude'][current]
    P['position'][i] = my_map(*E['position'][current])
    P['size'][i] = 5
    P['growth'][i] = np.exp(magnitude) * 0.1
    P['time'][i] = E['time'][current]

    if magnitude < 6:
        P['color'][i] = 0,0,1,1
    else:
        P['color'][i] = 1,0,0,1
    scat.set_edgecolors(P['color'])
    scat.set_facecolors(P['color']*(1,1,1,0.25))
    scat.set_sizes(P['size'])
    scat.set_offsets(P['position'])

    timestampStr = P['time'][i].strftime("%d-%b-%Y (%H:%M:%S) UTC")
    #timestampStr = P['time'][i].strftime("%d-%b-%Y")
    time_text.set_text(timestampStr)
    return scat, time_text

#set True to save animation
save = False

if save:
    animation = FuncAnimation(fig, update, interval=10, blit=True, save_count=len(E))
    animation.save('JapanQuakes2011March.mp4', fps=30, extra_args=['-vcodec', 'libx264'])
else:
    animation = FuncAnimation(fig, update, interval=10, blit=True)

plt.show()