import numpy as np
from sklearn.cluster import KMeans, DBSCAN
import matplotlib.pyplot as plt

def unsupervised_kmeans_dbscan(X, k, eps, min_samples):
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(X)
    labels = kmeans.labels_
    centroids = kmeans.cluster_centers_

    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    dbscan_labels = dbscan.fit_predict(X)
    n_clusters_ = len(set(dbscan_labels)) - (1 if -1 in dbscan_labels else 0)

    fig, axs = plt.subplots(1, 2, figsize=(16, 6))
    axs[0].scatter(X[:, 0], X[:, 1], c=labels, cmap='viridis', edgecolors='k', s=50)
    axs[0].scatter(centroids[:, 0], centroids[:, 1], c='red', marker='X', s=200, label='Centroids')
    axs[0].set_title(f'Unsupervised K-Means Clustering (k={k})')
    axs[0].set_xlabel('X 1')
    axs[0].set_ylabel('Y 2')
    axs[0].legend()

    axs[1].scatter(X[:, 0], X[:, 1], c=dbscan_labels, cmap='viridis', edgecolors='k', s=50)
    axs[1].set_title(f'Unsupervised DBSCAN (eps={eps}, min_samples={min_samples})')
    axs[1].set_xlabel('X 1')
    axs[1].set_ylabel('Y 2')
    plt.show()

    return n_clusters_

if __name__ == '__main__':
    np.random.seed(42)
    X = np.random.rand(100, 2) * 10
    k = 3
    eps = 0.3
    min_samples = 5
    n_clusters_ = unsupervised_kmeans_dbscan(X, k, eps, min_samples)