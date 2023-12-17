import numpy as np
from sklearn.linear_model import LinearRegression

def classification_regression(X_train, y_train_reg, X_test, k):
       
    regression_model = LinearRegression()
    regression_model.fit(X_train, y_train_reg)
    reg_predictions = regression_model.predict(X_test)    
    return reg_predictions

if __name__ == '__main__':
    X_train = np.array([[20, 200], [15, 100], [34, 600]])
    y_train_reg = np.array([10, 20, 20])
    X_test = np.array([[20, 100]])
    k = 3
    reg_pred = classification_regression(X_train, y_train_reg, X_test, k)  
    print("Hồi Quy", reg_pred)
