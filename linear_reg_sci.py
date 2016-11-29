import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
import csv

filename = 'data.csv'
output_csv = []
x_csv = []
y_csv = []

with open(filename, 'r') as csvf:
	csvreader = csv.reader(csvf, delimiter=',',lineterminator='\n')
	for row in csvreader:
		output_csv.append(row[:2])
		x_csv.append(row[3:])
		y_csv.append(row[1:3])
for row in y_csv:
	row[0] = float(row[1]) - float(row[0])
	del row[1]
print(output_csv)
#x_csv = list(map(lambda x: float(x), x_csv))
#y_csv = list(map(lambda x: float(x), y_csv))

negative = 0
for item in x_csv:
	#if float(item[0]) - 95.0 < 0:
	#	negative = 1
	item[0] = float(item[0]) - 100
	#if negative == 1:
	#	item[0] = -item[0]
	#	negative = 0
	item[1] = float(item[1]) - 100
	#item[0] = item[0] + item[1]
	#del item[1]
	item[2] = float(item[2])
for item in y_csv:
	item[0] = float(item[0])
x = np.array(x_csv)
y = np.array(y_csv)

model = Pipeline([('poly', PolynomialFeatures(degree=6)), ('linear', LinearRegression(fit_intercept=False))])
model = model.fit(x,y)
print(model.named_steps['linear'].coef_)
print(model.score(x,y))

"""plt.scatter(x,y[:, np.newaxis, np.newaxis], color='black')
plt.plot(x, model.predict(x), color='blue',
         linewidth=3)

plt.xticks(())
plt.yticks(())

plt.show()"""

list = []

for item in x:
	list.append([float(model.predict(item))])

with open('datanew.csv', 'w') as csvf:
	csvwriter = csv.writer(csvf, delimiter=',', lineterminator='\n')
	for i in range(len(list)):
		#print(output_csv[i][1])
		output_csv[i][1] = float(output_csv[i][1]) + float(list[i][0])
		csvwriter.writerow(output_csv[i])

"""poly = PolynomialFeatures(degree = 2)
poly.fit_transform(x)
reg = linear_model.LinearRegression()
reg.fit(x,y)
print('Coefficients: \n', reg.coef_)
print('Intercept: \n', reg.intercept_)
print('Variance score: %.2f' % reg.score(x,y))"""