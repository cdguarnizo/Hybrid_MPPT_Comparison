import numpy as np
from matplotlib import pyplot as plt  # now lets make some plots
plt.style.use("ggplot")


# spc_mat (0-2), MaxInd (3), Vmax (4), Pmax(5), localMaxV (6-8), localMaxP (9-11)

dataset = np.loadtxt("dataset.csv", delimiter=",")


clas = 1
index = [[0,3],[1,4],[2,5]]


ind = dataset[:,3]==float(clas)
Xmax = dataset[ind,4:]
Xmax = Xmax[:,[0,1]]
ymax = dataset[ind,3]

Xlocal = dataset[~ind,6:]

ylocal = dataset[~ind,3]
Xlocal = Xlocal[:,index[clas]] 
ind0 = Xlocal[:,0] == 0.        #Indices donde el voltaje sea 0.0
X = np.delete(Xlocal,ind0,0)    #Se eliminan

y = np.delete(ylocal,ind0)


ind2 = y == 2.
y = np.delete(y,ind2)
X = np.delete(X,ind2,0) 


X = np.vstack((X,Xmax))
y = np.concatenate((y, ymax))

## Multi Layer Perceptron Clasiffier

from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2)
scaler = StandardScaler()
X_train_scal = scaler.fit_transform(X_train)  # fit + transform
X_test_scal = scaler.transform(X_test)        # solo transform

print("Traing dataset size: ", X_train.shape)
print("Test dataset size: ", X_test.shape)

#(4,) seed 1 -> 1.0 accu
clf = MLPClassifier(hidden_layer_sizes=(4,), activation='relu', solver='adam', validation_fraction=0.1, alpha=1e-4, random_state=1, max_iter=2000)
clf = clf.fit(X_train_scal, y_train)
y_pred = clf.predict(X_test_scal)

print('Coefficients:', clf.coefs_)
print('Bias:', clf.intercepts_)
print('Number of layers:', clf.n_layers_)
print('Number of features:', clf.n_features_in_)
print('Number of outputs:', clf.n_outputs_)
print('Classes:', clf.classes_)

print("\nResults on test:")
print(classification_report(y_test, y_pred))