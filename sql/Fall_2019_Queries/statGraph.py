import plotly.graph_objects as graph
#name, week, MAE, MSE, sample
X = [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15]
MAE = []
MSE = []

file = open('final_plot.txt', 'r')
file.readline(); #reading column names
i = 0;
maeRidge = []
mseRidge =[]
maeGradient = []
mseGradient =[]
maeMLP = []
mseMLP =[]
maeLinear = []
mseLinear =[]
total = file.read().strip()
lines = total.split("\n")
finalList = []
for x in lines:
	y = x.split("\t")
	finalList.append(y)

ridge = ""
ridgeData = finalList[0:14]
gradient = ""
gradientData = finalList[14:28]
mlp = ""
mlpData = finalList[28:42]
linear = ""
linearData = finalList[42:56]

for i in range(0,14):
	maeRidge.append(ridgeData[i][2])
	mseRidge.append(ridgeData[i][3])
	maeGradient.append(gradientData[i][2])
	mseGradient.append(gradientData[i][3])
	maeMLP.append(mlpData[i][2])
	mseMLP.append(mlpData[i][3])
	maeLinear.append(linearData[i][2])
	mseLinear.append(linearData[i][3])

ridge = ridgeData[0][0]
gradient = gradientData[0][0]
mlp = mlpData[0][0]
linear = linearData[0][0]


file.close()

figure = graph.Figure()
figure.add_trace(graph.Scatter(x=X, y=maeRidge, mode='lines+markers', name =ridge))
figure.add_trace(graph.Scatter(x=X, y=maeGradient, mode='lines+markers',name=gradient))
figure.add_trace(graph.Scatter(x=X, y=maeMLP, mode='lines+markers',name=mlp))
figure.add_trace(graph.Scatter(x=X, y=maeLinear, mode='lines+markers',name=linear))
figure.update_layout(
	title="MAE",
	xaxis_title="weeks",
	yaxis_title="MAE",
	font=dict(
		size=36
	)
)
figure.show()


figure2 = graph.Figure()
figure2.add_trace(graph.Scatter(x=X, y=mseRidge, mode='lines+markers', name =ridge))
figure2.add_trace(graph.Scatter(x=X, y=mseGradient, mode='lines+markers',name=gradient))
figure2.add_trace(graph.Scatter(x=X, y=mseMLP, mode='lines+markers',name=mlp))
figure2.add_trace(graph.Scatter(x=X, y=mseLinear, mode='lines+markers',name=linear))
figure2.update_layout(
	title="MSE",
	xaxis_title="weeks",
	yaxis_title="MSE",
	font=dict(
		size=36
	)
)
figure2.show()