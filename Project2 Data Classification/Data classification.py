# ── imports ──────────────────────────────────────────
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (classification_report,
                             confusion_matrix,
                             f1_score)

# ── 1. LOAD DATA ──────────────────────────────────────
iris = load_iris()
X = iris.data        # features: sepal length, sepal width, petal length, petal width
y = iris.target      # labels: 0=setosa, 1=versicolor, 2=virginica

print("Dataset shape:", X.shape)   # (150, 4)
print("Classes:", iris.target_names)

# peek at the data
df = pd.DataFrame(X, columns=iris.feature_names)
df['species'] = [iris.target_names[i] for i in y]
print(df.head())

# ── 2. FEATURE SCALING ────────────────────────────────
# KNN uses distance — unscaled features give biased results
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ── 3. TRAIN-TEST SPLIT ───────────────────────────────
# 80% train, 20% test — shuffle=True removes order bias
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y,
    test_size=0.2,
    random_state=42,
    shuffle=True
)

print(f"\nTraining samples: {len(X_train)}")
print(f"Testing samples:  {len(X_test)}")

# ── 4. TRAIN KNN MODEL ────────────────────────────────
# k=5 — majority vote among 5 nearest neighbors
model = KNeighborsClassifier(n_neighbors=5)
model.fit(X_train, y_train)

# ── 5. PREDICT ────────────────────────────────────────
predictions = model.predict(X_test)

# ── 6. EVALUATE ───────────────────────────────────────
print("\n── Classification Report ──")
print(classification_report(y_test, predictions,
                             target_names=iris.target_names))

f1 = f1_score(y_test, predictions, average='weighted')
print(f"F1 Score (weighted): {f1:.4f}")

# ── 7. CONFUSION MATRIX ───────────────────────────────
cm = confusion_matrix(y_test, predictions)

plt.figure(figsize=(6, 4))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=iris.target_names,
            yticklabels=iris.target_names)
plt.title('Confusion Matrix — KNN (k=5)')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.tight_layout()
plt.savefig('confusion_matrix.png')   # saves as image for submission
plt.show()

print("\nDone! Confusion matrix saved.")
# find optimal K
error_rates = []

for k in range(1, 21):
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X_train, y_train)
    preds = knn.predict(X_test)
    error_rates.append(1 - f1_score(preds, y_test, average='weighted'))

plt.figure(figsize=(8, 4))
plt.plot(range(1, 21), error_rates, marker='o', color='navy')
plt.title('Elbow Method — Optimal K')
plt.xlabel('K Value')
plt.ylabel('Error Rate')
plt.tight_layout()
plt.savefig('elbow_curve.png')
plt.show()