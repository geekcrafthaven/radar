import random
#import numpy as np
import matplotlib.pyplot as plt

class DBSCAN:
    def __init__(self, eps, min_samples):
        self.eps = eps
        self.min_samples = min_samples
        self.labels = None
        self.__visited = None
        
    def fit(self, X):
        #self.labels = np.zeros(len(X))  # Alle Punkte als nicht besucht markieren
        #self.__visited = np.zeros(len(X))  # Alle Punkte als nicht besucht markieren

        self.labels = [0] * len(X)  # Alle Punkte als nicht besucht markieren
        self.__visited = [0] * len(X)  # Alle Punkte als nicht besucht markieren

        cluster_label = 1
        
        for i, point in enumerate(X):
            if self.__visited[i]:
                continue  # Punkt bereits besucht
            self.__visited[i] = 1
                
            neighbors = self._query_neighbors(X, i)
            
            if len(neighbors) < self.min_samples:
                self.labels[i] = -1  # Punkt als Ausreißer markieren
            else:
                self._expand_cluster(X, i, neighbors, cluster_label)
                cluster_label += 1
                
    def _query_neighbors(self, X, index):
        import math
        vector_norm = lambda a,b: math.sqrt()

        neighbors = []
        for i, point in enumerate(X):
            aa = [ai -bi for ai,bi in zip(point, X[index])]
            #aa = point - X[index]
            if math.sqrt(aa[0]**2 + aa[1]**2) < self.eps and i != index:
            #if np.linalg.norm(point - X[index]) < self.eps and i != index:
                neighbors.append(i)
        return neighbors
    
    def _expand_cluster(self, X, index, neighbors, cluster_label):
        self.labels[index] = cluster_label
        
        i = 0
        while i < len(neighbors):
            neighbor_index = neighbors[i]
            
            if not self.__visited[neighbor_index]:
                self.__visited[neighbor_index] = 1
                new_neighbors = self._query_neighbors(X, neighbor_index)
                
                if len(new_neighbors) >= self.min_samples:
                    neighbors.extend(new_neighbors)
            
            if self.labels[neighbor_index] == 0 or self.labels[neighbor_index] == -1:
                self.labels[neighbor_index] = cluster_label
            
            i += 1

def get_color(_value):
    colors = [
"blue",
"green",
"magenta",
"purple",
"cyan",
"brown",
"olive",
"plum",
"violet",
"azure",
 ]
    
    color = int(_value)

    if not color < len(colors):
        return 'red'
    
    if color == -1:
        return 'gray'
    else:
        return colors[color]

# Beispielverwendung:
# Generiere zufällige Punkte
#np.random.seed(0)
#X = np.random.rand(500, 2)

mu=100
sigma=50
X=[]
for i in range(100):
    #X.append([random.gauss(mu,sigma), random.gauss(mu,sigma)])
    X.append([random.uniform(0,1), random.uniform(0,1)])

# Führe DBSCAN durch
dbscan = DBSCAN(eps=0.12, min_samples=5)

import time
start_time = time.time()
dbscan.fit(X)
print("--- %s seconds ---" % (time.time() - start_time))

# Ausgabe der Clusterzugehörigkeiten
print("Cluster Labels:")
print(dbscan.labels, len(dbscan.labels))

plt.figure(figsize=(8, 6))
for index, item in enumerate(X):
    plt.scatter(item[0], item[1], color=get_color(dbscan.labels[index]), s=30, alpha=0.5)
plt.title('Punktwolke')
plt.xlabel('X-Achse')
plt.ylabel('Y-Achse')
plt.grid(True)
plt.show()
