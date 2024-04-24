import numpy as np

class MeanShift:
    def __init__(self, bandwidth=1.0, max_iter=300):
        self.bandwidth = bandwidth
        self.max_iter = max_iter

    def fit(self, X):
        self.centroids = []

        for x in X:
            centroid = self._find_centroid(X, x)
            if not any(np.array_equal(centroid, c) for c in self.centroids):
            #if centroid not in self.centroids:
                self.centroids.append(centroid)

    def _find_centroid(self, X, x):
        for _ in range(self.max_iter):
            old_x = x
            x = self._shift_point(X, x)
            if np.linalg.norm(x - old_x) < 1e-3:  # Convergence criteria
                break
        return x

    def _shift_point(self, X, x):
        weights = self._kernelize(X, x)
        shifted_point = np.dot(weights, X) / weights.sum()
        return shifted_point

    def _kernelize(self, X, x):
        distances = np.linalg.norm(X - x, axis=1)
        weights = np.exp(-0.5 * (distances / self.bandwidth) ** 2)
        return weights

# Beispielanwendung
if __name__ == "__main__":
    # Generieren von Beispiel-Daten
    np.random.seed(0)
    X = np.random.randn(100, 2) * 2 + np.array([5, 5])

    # Mean Shift Clustering
    mean_shift = MeanShift(bandwidth=0.70)

    import time
    start_time = time.time()
    mean_shift.fit(X)
    print("--- %s seconds ---" % (time.time() - start_time))

    print("Clusterzentren:", len(mean_shift.centroids))
    for centroid in mean_shift.centroids:
        print(centroid)

    import matplotlib.pyplot as plt

    plt.figure(figsize=(8, 6))
    #for index, item in enumerate(X):
    #    plt.scatter(item[0], item[1], color='blue', s=30, alpha=0.5)
    plt.scatter(X[:,0], X[:,1], color='blue', s=30, alpha=0.5)
    centroids = np.array(mean_shift.centroids)
    plt.scatter(centroids[:,0], centroids[:,1], color='red', s=30, alpha=0.5)
    plt.title('Punktwolke')
    plt.xlabel('X-Achse')
    plt.ylabel('Y-Achse')
    plt.grid(True)
    plt.show()
