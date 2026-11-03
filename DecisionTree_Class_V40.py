import numpy as np
from matplotlib import pyplot as plt  # now lets make some plots
plt.style.use("ggplot")


# spc_mat (0-2), MaxInd (3), Vmax (4), Pmax(5), localMaxV (6-8), localMaxP (9-11)

dataset = np.loadtxt("dataset.csv", delimiter=",")

plt.figure()
ind = dataset[:,3]==2.  #maximum points of class 2 (40V)
Xmax = dataset[ind,4:]
Xmax = Xmax[:,[0,1]]
ymax = dataset[ind,3]

Xlocal = dataset[~ind,6:]  #Voltages of vlases 0 and 1

ylocal = dataset[~ind,3] #labels of class 0 and 1
Xlocal = Xlocal[:,[2,5]] #takes voltages y powes around 40v

#Clean data and delete voltages equals to 0
ind0 = Xlocal[:,0] == 0.
X = np.delete(Xlocal,ind0,0)
y = np.delete(ylocal,ind0)

#Plot data
'''
plt.plot(Xmax[:,0],Xmax[:,1], '+b', markersize=6,label='40V')
ind2 = y == 1. 
plt.plot(X[ind2,0],X[ind2,1], 'xg', markersize=6, mfc = 'none',label='25V')
ind2 = y == 0. 
plt.plot(X[ind2,0],X[ind2,1], 'or', markersize=6, mfc = 'none',label='12V')
plt.xlabel("Voltage [V]")
plt.ylabel("Power [W]")
plt.legend()
#plt.savefig('Points40V.pdf')
'''

#Data for training and test
X = np.vstack((X,Xmax))  
y = np.concatenate((y, ymax))

# plt.figure()
# ind = dataset[:,3]==1.
# Xmax = dataset[ind,4:]
# plt.plot(Xmax[:,0],Xmax[:,1], '+r')
# Xlocal = dataset[~ind,6:]
# plt.plot(Xlocal[:,1],Xlocal[:,4], 'ob',mfc = 'none')

# plt.figure()
# ind = dataset[:,3]==0.
# Xmax = dataset[ind,4:]
# plt.plot(Xmax[:,0],Xmax[:,1], '+r')
# Xlocal = dataset[~ind,6:]
# plt.plot(Xlocal[:,0],Xlocal[:,3], 'ob',mfc = 'none')

from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2)
scaler = StandardScaler()
X_train_scal = scaler.fit_transform(X_train)  # fit + transform
X_test_scal = scaler.transform(X_test)        # solo transform

print("Training dataset size: ", X_train.shape)
print("Test dataset size: ", X_test.shape)

clf = DecisionTreeClassifier()
clf = clf.fit(X_train_scal, y_train)
y_pred_t = clf.predict(X_train_scal)
y_pred = clf.predict(X_test_scal)

print("\nResults on train:")
print(classification_report(y_train, y_pred_t))

print("\nResults on test:")
print(classification_report(y_test, y_pred))

#Plot Decision Tree classification area
from matplotlib.colors import ListedColormap
cmap_light = ListedColormap(['orange', 'cyan', 'cornflowerblue'])
cmap_bold = ListedColormap(['darkorange', 'c', 'darkblue'])
h = 2.0
x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                      np.arange(y_min, y_max, h))
plt.figure()
Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)
plt.pcolormesh(xx, yy, Z, cmap=cmap_light)
# Plot also the training points
plt.scatter(X[:, 0], X[:, 1], c=y, cmap=cmap_bold,
            edgecolor='k', s=20)
plt.title("Decision tree")
plt.axis('tight')
plt.show()

fig, axes = plt.subplots(nrows = 1,ncols = 1,figsize = (4,4), dpi=300)
plot_tree(clf)
#fig.savefig('DecisionTree_new.pdf')

#imprimir el arbol en codigo de C
#from micromlgen import port
#print(port(clf))
