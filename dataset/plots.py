import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.patches as mpatches

plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

# Push test

def define_box_properties(plot_name, color_code, label):
    for k, v in plot_name.items():
        plt.setp(plot_name.get(k), color=color_code)
    
    plt.plot([], c=color_code, label=label)
    plt.legend()

def annotate_special_lines(data, color="white", line_idx=[0]):
    def annotation_func(x, y):
        if x in line_idx:
            return f"{data[x, y]:d}", {"color": color, "fontweight": "bold"}
        else:
            return f"{data[x, y]:d}", {"color": "black"}
    return annotation_func

s_prefix = "./ctrllogs/"
b_prefix = "./benchlogs/"
u_prefix = "./usrlogs/"
cat_prefix = "throughput/"

locs = ["atlanta-lz/", "atlanta-wz/", "chicago-lz/", "chicago-wz/", "nyc-lz/", "nyc-wz/", "denver-lz/", "denver-wz/", "seattle-lz/", "seattle-wz/", "la-lz/", "la-wz/", "toronto/", "berlin/", "london/", "perth/", "tokyo/", "seoul/"]

locsusr = ["atllz/", "atlwz/", "chilz/", "chiwz/", "nyclz/", "nycwz/", "dnvlz/", "dnvwz/", "sealz/", "seawz/", "lalz/", "lawz/", "toronto/", "berlin/", "london/", "perth/", "tokyo/", "seoul/"]

locbench = ["ATLLZ/", "ATLWZ/", "CHILZ/", "CHIWZ/", "NYCLZ/", "NYCWZ/", "DVLZ/", "DVWZ/", "SEALZ/", "SEAWZ/", "LAXLZ/", "LAXWZ/", "TRWZ/", "BEWZ/", "LDNWZ/", "PELZ/", "TOWZ/", "SEOWZ/"]

caseusr = ["fortnitev3/", "netflixv3/", "oculusv3/", "tiktokv3/", "zoomv3/"]

varbenchlat = ["Mon00LAT.txt", "Mon12LAT.txt", "Tue00LAT.txt", "Tue12LAT.txt", "Wed00LAT.txt", "Wed12LAT.txt", "Thur00LAT.txt", "Thur12LAT.txt", "Fri00LAT.txt", "Fri12LAT.txt", "Sat00LAT.txt", "Sat12LAT.txt", "Sun00LAT.txt"]

varbenchthr = ["Mon00TCP.txt", "Mon12TCP.txt", "Tue00TCP.txt", "Tue12TCP.txt", "Wed00TCP.txt", "Wed12TCP.txt", "Thur00TCP.txt", "Thur12TCP.txt", "Fri00TCP.txt", "Fri12TCP.txt", "Sat00TCP.txt", "Sat12TCP.txt", "Sun00TCP.txt"]

varbenchpl = ["Mon00UDP.txt", "Mon12UDP.txt", "Tue00UDP.txt", "Tue12UDP.txt", "Wed00UDP.txt", "Wed12UDP.txt", "Thur00UDP.txt", "Thur12UDP.txt", "Fri00UDP.txt", "Fri12UDP.txt", "Sat00UDP.txt", "Sat12UDP.txt", "Sun00UDP.txt"]

locnames = ["Atlanta-LZ", "Atlanta-WZ", "Chicago-LZ", "Chicago-WZ", "New York City-LZ", "New York City-WZ", "Denver-LZ", "Denver-WZ", "Seattle-LZ", "Seattle-WZ", "Los Angeles-LZ", "Los Angeles-WZ", "Toronto-WZ", "Berlin-WZ", "London-WZ", "Perth-LZ", "Tokyo-WZ", "Seoul-WZ"]

locnamesabbr = ["Atl-LZ", "Atl-WZ", "Chi-LZ", "Chi-WZ", "NYC-LZ", "NYC-WZ", "Dnv-LZ", "Dnv-WZ", "Sea-LZ", "Sea-WZ", "LA-LZ", "LA-WZ", "Trn-WZ", "Be-WZ", "Ldn-WZ", "Pe-LZ", "Tky-WZ", "Seo-WZ"]

strategies = ["str1.xlsx", "str2.xlsx", "str3.xlsx"]

x_axis_labels = ["5G-AKA", "Session", "NRF Reg."]
y_axis_labels = ["URLLC User", "Static MCS", "Mobile MCS"]


#------------------------------------------------------------------------------------------
#-----------------------------------------Cost Logs----------------------------------------
#------------------------------------------------------------------------------------------





#------------------------------------------------------------------------------------------
#------------------------------------Benchmark Logs----------------------------------------
#------------------------------------------------------------------------------------------
x = np.array([0,1,2,3,4,5,6,7,8,9,10,11,12])

xticksdays = ['Apr24-00h','Apr24-12h','Apr25-00h','Apr25-12h','Apr26-00h','Apr26-12h','Apr27-00h','Apr27-12h','Apr28-00h','Apr28-12h','Apr29-00h','Apr29-12h','Apr30-00h']

benchlatmat = np.zeros((18,13))	
benchthrmat = np.zeros((18,13))	
benchplmat = np.zeros((18,13))	

benchlatAll = []
benchthrAll = []
benchplAll = []

l = 0
for i in locbench:
	r = 0
	for j in varbenchlat:
		b_loc = i
		b_case_lat = j
		b_case_thr = varbenchthr[r]
		b_case_pl = varbenchpl[r]
		b_end_lat = b_prefix + b_loc + b_case_lat
		b_end_thr = b_prefix + b_loc + b_case_thr
		b_end_pl = b_prefix + b_loc + b_case_pl
		benchlatmat[l,r] = np.mean(np.loadtxt(b_end_lat))
		benchthrmat[l,r] = np.mean(np.loadtxt(b_end_thr))
		benchplmat[l,r] = np.mean(np.loadtxt(b_end_pl))
		r+=1
	
	l+=1	

#benchlatmat = np.transpose(benchlatmat)
#benchthrmat = np.transpose(benchthrmat)
#benchplmat = np.transpose(benchplmat)

benchthrmatr = np.round(benchthrmat).astype(int)
benchlatmatr = np.round(benchlatmat).astype(int)



fb = 20
fs=1.3
vmin, vmax = 0, 60
dec = '.1f'
#colschem = "Blues"
colschem = "YlOrBr"

textcolor_map = sns.color_palette(["black", "black", "white", "black", "black", "black", "black", "black", "black", "black", "black", "black", "black", "black", "black", "black", "black", "black"], n_colors=18)

fig, ax = plt.subplots(figsize=(18, 9.5))
sns.set(font_scale=fs)

s = sns.heatmap(data=benchlatmat, annot=True, cmap=colschem, fmt=dec, center=(vmin + vmax) / 2., vmax=vmax, vmin=vmin,
                  square=True, xticklabels=xticksdays, yticklabels=locnamesabbr, linewidths=.5, cbar=True, ax=ax,
                  annot_kws={"weight": "bold", "color": "black", "size": 15}, cbar_kws={'label': 'Latency (ms)', "shrink": 0.8})

for tick in ax.xaxis.get_major_ticks():
    tick.label.set_fontsize(fb)

for tick in ax.yaxis.get_major_ticks():
    tick.label.set_fontsize(fb)

ax.figure.axes[-1].yaxis.label.set_size(fb)
plt.tight_layout()

fig.subplots_adjust(right=0.48)

plt.savefig('./benchplots/benchlat.png', format='png')
plt.savefig('./benchplots/benchlat.eps', format='eps')
plt.savefig('./benchplots/benchlat.pdf', format='pdf')


plt.clf()
dec = '.0f'
vmin, vmax = 50, 600
fig, ax = plt.subplots(figsize=(18, 9.5))
sns.set(font_scale=fs)

s = sns.heatmap(data=benchthrmatr, annot=True, cmap=colschem, fmt=dec, center=(vmin + vmax) / 2., vmax=vmax, vmin=vmin,
                  square=True, xticklabels=xticksdays, yticklabels=locnamesabbr, linewidths=.3, cbar=True, ax=ax,
                  annot_kws={"weight": "bold", "color": "black", "size": 15}, cbar_kws={'label': 'TCP Throughput (Mbps)', "shrink": 0.8})

for tick in ax.xaxis.get_major_ticks():
    tick.label.set_fontsize(fb)

for tick in ax.yaxis.get_major_ticks():
    tick.label.set_fontsize(fb)

ax.figure.axes[-1].yaxis.label.set_size(fb)
plt.tight_layout()

fig.subplots_adjust(right=0.48)

plt.savefig('./benchplots/benchthr.png', format='png')
plt.savefig('./benchplots/benchthr.eps', format='eps')
plt.savefig('./benchplots/benchthr.pdf', format='pdf')

plt.clf()
dec = '.1f'
vmin, vmax = 20, 50
fig, ax = plt.subplots(figsize=(18, 9.5))
sns.set(font_scale=fs)

s = sns.heatmap(data=benchplmat, annot=True, cmap=colschem, fmt=dec, center=(vmin + vmax) / 2., vmax=vmax, vmin=vmin,
                  square=True, xticklabels=xticksdays, yticklabels=locnamesabbr, linewidths=.3, cbar=True, ax=ax,
                  annot_kws={"weight": "bold", "color": "black", "size": 15}, cbar_kws={'label': 'Packet Loss Rate (%)', "shrink": 0.8})

for tick in ax.xaxis.get_major_ticks():
    tick.label.set_fontsize(fb)

for tick in ax.yaxis.get_major_ticks():
    tick.label.set_fontsize(fb)

ax.figure.axes[-1].yaxis.label.set_size(fb)
plt.tight_layout()

fig.subplots_adjust(right=0.48)

plt.savefig('./benchplots/benchpl.png', format='png')
plt.savefig('./benchplots/benchpl.eps', format='eps')
plt.savefig('./benchplots/benchpl.pdf', format='pdf')

#------------------------------------------------------------------------------------------
#------------------------------------User Plane Logs---------------------------------------
#------------------------------------------------------------------------------------------

usr_thr = ["throughput.TCP40.log.txt", "throughput.TCP80.log.txt"]
usr_pl = ["pl.UDP40.log.txt", "pl.UDP80.log.txt"]

loc_usr_thr = []
loc_usr_pl = []
for i in locsusr:
	r = 0
	locstrthr = np.zeros((20,5,2), dtype=float)	
	locstrpl = np.zeros((20,5,2), dtype=float)	
	for j in caseusr:
		a = 0
		for k in usr_thr:
			u_loc = i 
			u_case = j
			u_end_thr = u_prefix + u_loc + u_case + cat_prefix + usr_thr[a]
			u_end_pl = u_prefix + u_loc + u_case + cat_prefix + usr_pl[a]
			locstrthr[:,r,a] = np.loadtxt(u_end_thr) 
			locstrpl[:,r,a] = np.loadtxt(u_end_pl) 
			a+=1
		r+=1
	loc_usr_thr.append(locstrthr)
	loc_usr_pl.append(locstrpl)
			
#------------------------------------------------------------------------------------------
#------------------------------------User Plane Plots--------------------------------------
#------------------------------------------------------------------------------------------

plt.rcParams['axes.facecolor']='white'

ticks = ['Fortnite', 'Netflix', 'Oculus', 'Tiktok', 'Zoom']
x = np.array([0,1,2,3,4])

fig, axs = plt.subplots(nrows=3, ncols=6, figsize=(18, 7.5), gridspec_kw={'width_ratios': [1]*6})

data = loc_usr_thr[0][:,:,0]

u1 = 1.2 * np.arange(len(data))
u2 = [x + 0.5  for x in u1]
u3 = [x + 0.5 for x in u2]
u4 = [len(ticks)]


nouserplace = [0, 0, 0, 0, 0, 10]

handles = []
labels = []
c=0

plt.yticks(fontsize=20)


for i, ax in enumerate(axs.flat):
	if c < 12:
		ticks = ['', '', '', '', '', '']
	else:
		ticks = ['Fortnite', 'Netflix', 'Oculus', 'Tiktok', 'Zoom', '']
	
		
	data40t = loc_usr_thr[c][:,:,0]
	data80t = loc_usr_thr[c][:,:,1]
	nouser_data = np.array([benchthrmat[c, :]]).T
	usr40tplot = ax.violinplot(data40t, showmedians=False, showmeans=True, positions=x*2.0-0.35, widths=0.6)
	usr80tplot = ax.violinplot(data80t, showmedians=False, showmeans=True, positions=x*2.0+0.35, widths=0.6)
	nouser_plot = ax.violinplot(nouser_data, positions=[10], showmeans=True, widths=0.6)
	define_box_properties(usr40tplot, '#D7191C', '40 Users')
	define_box_properties(usr80tplot, '#2C7BB6', '80 Users')
	define_box_properties(nouser_plot, '#000000', 'No Users')
	ax.set(ylim =(0, 500))
	ax.set_xticks(np.arange(0, len(ticks) * 2, 2), ticks, fontsize=20, rotation=85)
	ax.set_xlim(-2, len(ticks)*2)
	ax.legend().set_visible(False)
	ax.spines['top'].set_color('black')
	ax.spines['bottom'].set_color('black')
	ax.spines['left'].set_color('black')
	ax.spines['right'].set_color('black')
	ax.spines['top'].set_linewidth(2)
	ax.spines['bottom'].set_linewidth(2)
	ax.spines['left'].set_linewidth(2)
	ax.spines['right'].set_linewidth(2)
	
	#nouser = np.mean(benchthrmat[c,:])
	
	#ax.bar(10, nouser, 0.5, alpha=0.8, color='black', edgecolor='black', linewidth=0.5, label='0 users')

	
	yerr = [ [np.mean(benchthrmat[c,:]) - np.min(benchthrmat[c,:])] , 
		 [np.max(benchthrmat[c,:]) - np.mean(benchthrmat[c,:])] ]
	
	#ax.errorbar(10, nouser, yerr=yerr, fmt='none', ecolor='r', capsize=2)

		
	ax.grid(True, color='gray', linestyle='dashed', linewidth=0.5)	
	if c == 10:
		ax.set(ylim =(600, 1010))

	if c==6:
		ax.set_ylabel("TCP Throughput (Mbps)", fontsize=20)
	
	ax.title.set_text(locnames[c])
	ax.title.set_size(20)


	c+=1


u40 = mpatches.Patch(color='#D7191C', label='40 users - 4 slices')
u80 = mpatches.Patch(color='#2C7BB6', label='80 users - 8 slices')
u0 = mpatches.Patch(color='#000000', label='no users - weekly average')
fig.legend(handles=[u40, u80, u0], loc='upper center', ncol=3, fontsize=20)

fig.subplots_adjust(wspace=0.5, hspace=1, left=0.1, right=0.9, bottom=0.1, top=0.8)

plt.tight_layout()

fig.subplots_adjust(top=0.85)

plt.savefig('./usrplots/thrAll.png', format='png')
plt.savefig('./usrplots/thrAll.eps', format='eps')
plt.savefig('./usrplots/thrAll.pdf', format='pdf')


fig2, axs2 = plt.subplots(nrows=3, ncols=6, figsize=(18, 7.5), gridspec_kw={'width_ratios': [1]*6})
c=0

plt.yticks(fontsize=20)

for i, ax in enumerate(axs2.flat):
	if c < 12:
		ticks = ['', '', '', '', '', '']
	else:
		ticks = ['Fortnite', 'Netflix', 'Oculus', 'Tiktok', 'Zoom', '']
		
	data40p = loc_usr_pl[c][:,:,0]
	data80p = loc_usr_pl[c][:,:,1]
	nouser_data = np.array([benchplmat[c, :]]).T
	usr40pplot = ax.violinplot(data40p, showmedians=False, showmeans=True, positions=x*2.0-0.35, widths=0.6)
	usr80pplot = ax.violinplot(data80p, showmedians=False, showmeans=True, positions=x*2.0+0.35, widths=0.6)
	nouser_plot = ax.violinplot(nouser_data, positions=[10], showmeans=True, widths=0.6)
	define_box_properties(usr40pplot, '#D7191C', '40 Users')
	define_box_properties(usr80pplot, '#2C7BB6', '80 Users')
	define_box_properties(nouser_plot, '#000000', 'No Users')
	ax.set(ylim =(10, 100))
	ax.set_xticks(np.arange(0, len(ticks) * 2, 2), ticks, fontsize=20, rotation=85)
	ax.set_xlim(-2, len(ticks)*2)
	ax.legend().set_visible(False)
	ax.spines['top'].set_color('black')
	ax.spines['bottom'].set_color('black')
	ax.spines['left'].set_color('black')
	ax.spines['right'].set_color('black')
	ax.spines['top'].set_linewidth(2)
	ax.spines['bottom'].set_linewidth(2)
	ax.spines['left'].set_linewidth(2)
	ax.spines['right'].set_linewidth(2)
	
	#nouser = np.mean(benchplmat[c,:])
	
	#ax.bar(10, nouser, 0.5, alpha=0.8, color='black', edgecolor='black', linewidth=0.5, label='0 users')

	
	yerr = [ [np.mean(benchplmat[c,:]) - np.min(benchplmat[c,:])] , 
		 [np.max(benchplmat[c,:]) - np.mean(benchplmat[c,:])] ]
	
	#ax.errorbar(10, nouser, yerr=yerr, fmt='none', ecolor='r', capsize=2)
	
	ax.grid(True, color='gray', linestyle='dashed', linewidth=0.5)

	if c == 10:
		ax.set(ylim =(0, 10))
		
	if c == 6:
		ax.set_ylabel("UDP Packet Loss Rate (%)", fontsize=20)
	
	ax.title.set_text(locnames[c])
	ax.title.set_size(20)

	c+=1



u40 = mpatches.Patch(color='#D7191C', label='40 users - 4 slices')
u80 = mpatches.Patch(color='#2C7BB6', label='80 users - 8 slices')
u0 = mpatches.Patch(color='#000000', label='no users - weekly average')
fig2.legend(handles=[u40, u80, u0], loc='upper center', ncol=3, fontsize=20)

fig2.subplots_adjust(wspace=0.5, hspace=1, left=0.1, right=0.9, bottom=0.1, top=0.8)

plt.tight_layout()

fig2.subplots_adjust(top=0.85)

plt.savefig('./usrplots/plAll.png', format='png')
plt.savefig('./usrplots/plAll.eps', format='eps')
plt.savefig('./usrplots/plAll.pdf', format='pdf')



k=0
l=0
for i in locnames:
	plt.clf()
	data40t = loc_usr_thr[k][:,:,0]
	data80t = loc_usr_thr[k][:,:,1]
	usr40tplot = plt.violinplot(data40t, showmedians=False, showmeans=True, positions=x*2.0-0.35, widths=0.6)
	usr80tplot = plt.violinplot(data80t, showmedians=False, showmeans=True, positions=x*2.0+0.35, widths=0.6)
	#for pc in usr40plot['bodies']:
	#    pc.set_linestyle('--')
	define_box_properties(usr40tplot, '#D7191C', '40 Users')
	define_box_properties(usr80tplot, '#2C7BB6', '80 Users')
	plt.xticks(np.arange(0, len(ticks) * 2, 2), ticks)
	plt.xlim(-2, len(ticks)*2)
	#plt.ylim([0, 1100])
	plt.grid()
	plt.title(i)
	#plt.savefig('./usrplots/' + i + 'thr.png', format='png')
	l+=1

	plt.clf()
	data40p = loc_usr_pl[k][:,:,0]
	data80p = loc_usr_pl[k][:,:,1]
	usr40pplot = plt.violinplot(data40p, showmedians=False, showmeans=True, positions=x*2.0-0.35, widths=0.6)
	usr80pplot = plt.violinplot(data80p, showmedians=False, showmeans=True, positions=x*2.0+0.35, widths=0.6)
	#for pc in usr40plot['bodies']:
	#    pc.set_linestyle('--')
	define_box_properties(usr40pplot, '#D7191C', '40 Users')
	define_box_properties(usr80pplot, '#2C7BB6', '80 Users')
	plt.xticks(np.arange(0, len(ticks) * 2, 2), ticks)
	plt.xlim(-2, len(ticks)*2)
	#plt.ylim([0, 1100])
	plt.grid()
	plt.title(i)
	#plt.savefig('./usrplots/' + i + 'pl.png', format='png')
	l+=1

	k+=1



#------------------------------------------------------------------------------------------
#------------------------------------Control Plane Logs------------------------------------
#------------------------------------------------------------------------------------------
locAll = []
heatmaps = []
sumCol1 = []
sumCol2 = []
sumCol3 = []
for i in locs:
	r = 0
	locstr = np.zeros((3,3), dtype=float)	
	for j in strategies:
		s_loc = i
		s_strategy = j
		s_end = s_prefix + s_loc + s_strategy
		df = pd.read_excel(s_end)
		dfsumcol = df.sum(axis=1)
		matsumcol = dfsumcol.to_numpy()
		if j == "str1.xlsx":
			sumCol1.append(matsumcol)
		if j == "str2.xlsx":
			sumCol2.append(matsumcol)
		if j == "str3.xlsx":
			sumCol3.append(matsumcol)
		dfm = df.mean(axis=0)
		sumall = round(df.sum().sum(),1)
		alldata = df
		aka = dfm.iloc[[0, 4]].sum()
		sesset = dfm.iloc[[2, 3, 5, 6, 10]].sum()
		nrfdisc = dfm.iloc[[1, 7, 8, 9]].sum()
		locstr[r,0:3] = [aka , sesset, nrfdisc]
		r+=1

	locAll.append(locstr)

#--------------------------------------------------------------------------------------------
#----------------------------------Operational Heatmaps--------------------------------------
#--------------------------------------------------------------------------------------------
dec = '.1f'
vmin, vmax = 5, 300

fig, axs = plt.subplots(nrows=3, ncols=6, figsize=(18, 7.5), gridspec_kw={'width_ratios': [1]*6})

c=0
for i, ax in enumerate(axs.flat):
	s = sns.heatmap(data=locAll[c], annot=True, cmap=colschem, fmt=dec, center=(vmin + vmax) / 2., vmax=vmax, 
                  square=True, xticklabels=x_axis_labels, yticklabels=y_axis_labels, linewidths=.5, cbar=False, ax=ax,
		  annot_kws={"weight": "bold", "size":14})

	heatmaps.append(s)

	for label in ax.get_yticklabels():
        	label.set_weight('bold')
	for label in ax.get_xticklabels():
        	label.set_weight('bold')


	ax.title.set_text(locnamesabbr[c])
	if c != 0 and c != 6 and c!=12: 
		s.set_yticks([]) 

	if c < 12:
		s.set_xticks([])
	c+=1

plt.tight_layout()

fig.subplots_adjust(right=0.8)

cbar = fig.colorbar(heatmaps[0].collections[0], ax=axs.ravel().tolist(), shrink=0.9, aspect=20)
cbar.set_label('ms')
plt.savefig('./ctrlplots/op_breakdown.eps', format='eps')
plt.savefig('./ctrlplots/op_breakdown.png', format='png')

#--------------------------------------------------------------------------------------------
#-------------------------------------Bar Plot Latency---------------------------------------
#--------------------------------------------------------------------------------------------

bench = [3.53, 3.6, 17.97, 9.23, 4.97, 1.1, 3.72, 3.64, 2.2, 1.35]
benchsum = np.sum(bench)



yvalues1 = np.zeros((18), dtype=float)
yerr1 = np.zeros((18,2), dtype=float)
c=0
for i in sumCol1:
	yvalues1[c] = i.mean()
	yerr1[c,:] = (i.mean()-i.min(), i.max()-i.mean())
	c+=1


yvalues2 = np.zeros((18), dtype=float)
yerr2 = np.zeros((18,2), dtype=float)
c=0
for i in sumCol2:
	yvalues2[c] = i.mean()
	yerr2[c,:] = (i.mean()-i.min(), i.max()-i.mean())
	c+=1


yvalues3 = np.zeros((18), dtype=float)
yerr3 = np.zeros((18,2), dtype=float)
c=0
for i in sumCol3:
	yvalues3[c] = i.mean()
	yerr3[c,:] = (i.mean()-i.min(), i.max()-i.mean())
	c+=1

x = locnamesabbr
y1 = yvalues1
y2 = yvalues2
y3 = yvalues3


#print(y3)
#print(benchsum)

patterns = ['/', '.', '-']

# Min-Max Error Bars
y1_error = yerr1
y2_error = yerr2
y3_error = yerr3

fig, ax = plt.subplots()
bar_width = 0.2
opacity = 0.8

r1 = np.arange(len(y1))
r2 = [x + bar_width for x in r1]
r3 = [x + bar_width for x in r2]
r4 = [len(locnames)]

# Plot the bars
ax.bar(x, y1, bar_width, alpha=opacity, color='gray', edgecolor='black', linewidth=1, label='URLLC User Plane')
ax.bar([i + bar_width + 0.05 for i in range(len(x))], y2, bar_width, alpha=opacity, color = 'white', hatch = '///', edgecolor='black', linewidth=1, label='Static MCS Control Plane')
ax.bar([i + (2 * bar_width) + 0.1 for i in range(len(x))], y3, bar_width, alpha=opacity, color='white', edgecolor='black', linewidth=1, label='Mobile MCS Control Plane')

rects4 = ax.bar(r4, benchsum, bar_width+0.3, alpha=opacity, color='black', edgecolor='black', linewidth=0.5, label='Monolithic Slice')


#Add the min-max error bars
ax.errorbar(x, y1, yerr=np.transpose(y1_error), fmt='none', ecolor='r', capsize=2)
ax.errorbar([i + bar_width + 0.05 for i in range(len(x))], y2, yerr=np.transpose(y2_error), fmt='none', ecolor='r', capsize=2)
ax.errorbar([i + (2 * bar_width) + 0.1 for i in range(len(x))], y3, yerr=np.transpose(y3_error), fmt='none', ecolor='r', capsize=2)

plt.xticks(fontsize=14, rotation=85)
ax.set_xlabel('')
ax.set_ylabel('Total Latency (ms)', fontsize=18)
ax.set_xticks([i + (1.5 * bar_width) for i in range(len(x))])
ax.set_xticklabels(x)
ax.grid(axis='y')
plt.legend(fontsize=13)
plt.tight_layout()

plt.savefig('./ctrlplots/totlat.eps', format='eps')
plt.savefig('./ctrlplots/totlat.png', format='png')








