from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import os
import subprocess as sp
import sys
import json
import bioservices
from xml.etree import ElementTree
from xml.dom.minidom import parseString

from bioservices import EUtils



def tail(f, lines=1, _buffer=4098):
    """Tail a file and get X lines from the end"""
    # place holder for the lines found
    lines_found = []

    # block counter will be multiplied by buffer
    # to get the block size from the end
    block_counter = -1

    # loop until we find X lines
    while len(lines_found) < lines:
        try:
            f.seek(block_counter * _buffer, os.SEEK_END)
        except IOError:  # either file is too small, or too many lines requested
            f.seek(0)
            lines_found = f.readlines()
            break

        lines_found = f.readlines()

        # we found enough lines, get out
        # Removed this line because it was redundant the while will catch
        # it, I left it for history
        # if len(lines_found) > lines:
        #    break

        # decrement the block counter to get the
        # next X bytes
        block_counter -= 1

    return lines_found[-lines:]


# Link to NCBI EServices

s = EUtils()	
N = 21 
bottom = 1	
max_height = 4
theta = range(0,21) #np.linspace(0.0, 2 * np.pi, N, endpoint=False)
my_xticks = ['BB','A','C','D','E','F','G','H','I','K','L','M','N','P',
'Q','R','S','T','V','W','Y']


	
for f in os.listdir("."):
	fname=f.split(".")
	
	# plot SASA from freesasa calculation
	
	if ".sasa" in f:
		print f
		try:
			f_res=f.replace("sasa", "res")
			figname=fname[0]+".avg"
			radii=[]
			resii=[]
			with open(f, 'rb') as a:
				last_lines = tail(a, 21)
				for i in last_lines:
					data = i.split(":")
					rad=data[1].replace("\n","")
					radii.append(float(rad))
			
			with open(f_res, 'rb') as r:
				last_lines = tail(r, 20)
				for i in last_lines:
					data = i.split(" ")
					res=data[1].replace("\n","")
					resii.append(float(res))
				tot_res=sum(resii)
				resii.insert(0,tot_res)
				tot_sasa=sum(radii)
			norm_byresnum = [sasa/res for sasa, res in zip(radii, resii)]
			norm_bysasa = [y / int(tot_sasa) for y in radii]
					
		except Exception as e:
			print("In SASA: Some unknown error occured: %s"%(str(e)))		
			
		try:	
			ax = plt.subplot(111, polar=False)
			fig = plt.gcf();
			fig.set_size_inches(12,3)
			bars = ax.bar(theta, norm_byresnum, width=1)#, bottom=bottom)
			plt.xticks(theta, my_xticks)
			plt.ylim( 0, 100 )
			for item in [ax]:
				item.patch.set_visible(False)
			ax.axes.get_xaxis().set_visible(True)
			ax.tick_params(axis='x', which='major', pad=-22)
			ax.tick_params(axis='y', which='major', pad=-22)
			ax.axes.yaxis.grid(color='g', linestyle='--', linewidth=0.5)
			ax.axes.get_yaxis().set_visible(True)
			fig.tight_layout()
			# Use custom colors and opacity
			for r, bar in zip(norm_byresnum, bars):
				if (r > 100):
					bar.set_facecolor('g')
				else:
					bar.set_facecolor(plt.cm.cool(int(256*(r/100))))
				bar.set_alpha(0.8)
				bar.set_edgecolor("white")
			for tic in ax.xaxis.get_major_ticks():
				tic.tick1On = tic.tick2On = False
				tic.label1On = True
			for tic in ax.yaxis.get_major_ticks():
				tic.tick1On = tic.tic2On = False
				tic.label1On = True
			for spine in ax.spines.values():
				spine.set_visible(False)		
#			plt.show()
			plt.savefig(figname, transparent = True, bbox_inches = 'tight', pad_inches = 0)
			plt.close(fig)

		except Exception as e:
				print("In plot: Some unknown error occured: %s"%(str(e)))


