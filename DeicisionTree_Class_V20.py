import numpy as np
from matplotlib import pyplot as plt  # now lets make some plots
plt.style.use("ggplot")


# spc_mat (0-2), MaxInd (3), Vmax (4), Pmax(5), localMaxV (6-8), localMaxP (9-11)

dataset = np.loadtxt("dataset.csv", delimiter=",")


clas = 1
index = [[0,3],[1,4],[2,5]]

plt.figure()
ind = dataset[:,3]==float(clas)
Xmax = dataset[ind,4:]
Xmax = Xmax[:,[0,1]]
ymax = dataset[ind,3]

Xlocal = dataset[~ind,6:]

ylocal = dataset[~ind,3]
Xlocal = Xlocal[:,index[clas]] 
ind0 = Xlocal[:,0] == 0.        #Indexes where voltage is 0.0
X = np.delete(Xlocal,ind0,0)    #are eliminated
y = np.delete(ylocal,ind0)

ind2 = y == 2.                  #Labels equals to 2 (40V)
y = np.delete(y,ind2)
X = np.delete(X,ind2,0) 

plt.plot(Xmax[:,0],Xmax[:,1], 'xg', label='25V')
plt.plot(X[:,0],X[:,1], 'or',mfc = 'none', label='12V')
plt.xlabel("Voltage [V]")
plt.ylabel("Power [W]")
plt.legend()
plt.savefig('Points25V.pdf')

X = np.vstack((X,Xmax))
y = np.concatenate((y, ymax))



## Decision trees
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2)
scaler = StandardScaler()
X_train_scal = scaler.fit_transform(X_train)  # fit + transform
X_test_scal = scaler.transform(X_test)        # solo transform

print("Traing dataset size: ", X_train.shape)
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