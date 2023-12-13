from sklearn.tree import DecisionTreeClassifier, export_text
import numpy as np
# ban du lieue cuar nhom 10
data = np.array([
    [15, 'Học sinh', 'Thấp'],
    [20, 'Sinh viên', 'Cao'],
    [45, 'Công nhân', 'Cao'],
    [26, 'Công nhân', 'Thấp'],
    [18, 'Học sinh', 'Cao'],
    [13, 'Học sinh', 'Thấp'],
    [17, 'Học sinh', 'Thấp'],
    [19, 'Công nhân', 'Cao'],
    [37, 'Công nhân', 'Cao'],
    [22, 'Sinh viên', 'Cao']
])

X = data[:, :-1]
y = data[:, -1]

X[:, 1] = np.unique(X[:, 1], return_inverse=True)[1]

X = X.astype(int)

model = DecisionTreeClassifier()
model.fit(X, y)

tree_rules = export_text(model, feature_names=['Tuổi', 'Công việc'])
print(tree_rules)

new_person = np.array([23, 'Sinh viên']).reshape(1, -1)
new_person[:, 1] = np.unique(new_person[:, 1], return_inverse=True)[1]
new_person = new_person.astype(int)

prediction = model.predict(new_person)
print(f"Dự đoán thu nhập: {prediction[0]}")
