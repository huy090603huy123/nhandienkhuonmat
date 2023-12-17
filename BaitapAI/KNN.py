import numpy as np
from sklearn.neighbors import KNeighborsClassifier

def classification_regression(X_train, y_train_class, X_test, k):
    
    knn_classifier = KNeighborsClassifier(n_neighbors=k)
    knn_classifier.fit(X_train, y_train_class)
    class_predictions = knn_classifier.predict(X_test)
     
    return class_predictions


if __name__ == '__main__':
    X_train = np.array([[20, 200], [15, 100], [34, 600]])
    y_train_class = np.array([1, 2, 3])
    X_test = np.array([[30, 500]])
    k = 3

    class_pred = classification_regression(X_train, y_train_class, X_test, k)  
    print("KNN:", class_pred)
   