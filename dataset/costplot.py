import matplotlib.pyplot as plt
import numpy as np


locnamescost = ["US-East", "Atl-LZ", "Atl-WZ", "Chi-LZ", "Chi-WZ", "NYC-LZ", "NYC-WZ", "US-West", "Dnv-LZ", "Dnv-WZ", "Sea-LZ", "Sea-WZ", "LA-LZ", "LA-WZ","Canada", "Trn-WZ", "EU-Fra", "Be-WZ", "EU-Ldn", "Ldn-WZ", "A-P (Sydney)", "Pe-LZ", "A-P (Tokyo)", "Tky-WZ", "A-P (Seoul)", "Seo-WZ"]

ec2 = np.array([769.79, 52.45, 150.45, 41.42, 53.34, 29.08, 141.17, 281.99, 25.45, 140.62, 29.82, 41.83, 26.28, 60.37, 44.73, 29.03, 105.34, 103.73, 100.16, 86.73, 111.41, 109.5, 115.37, 109.69, 195.43, 175.22])

data = np.array([266.08, 45.32, 96.13, 32.07, 30.49, 36.89, 69.92, 227.52, 30.70, 85.42, 33.36, 32.89, 55.41, 34.24, 27.84, 34.33, 63.17, 79.64, 97.78, 110.65, 40.76, 498.8, 89.04, 102.37, 138.03, 150.37])
 

plt.figure(figsize=(10,6))
plt.bar(locnamescost, ec2, color='black', edgecolor='black', linewidth=1, width = 0.4)
plt.bar(locnamescost, data, bottom=ec2, color='white', hatch = '///', edgecolor='black', linewidth=1, width = 0.4)
plt.ylabel("Cost (USD)", fontsize=20)
plt.legend(["EC2", "Data"], fontsize=20)
plt.xticks(fontsize=16, rotation=75)
plt.yticks(fontsize=20)

plt.tight_layout()
plt.grid()

plt.savefig('totcost.eps', format='eps')
plt.savefig('totcost.png', format='png')

plt.show()

