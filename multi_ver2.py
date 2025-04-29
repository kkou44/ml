from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.metrics import accuracy_score
import multiprocessing as mp
import matplotlib.pyplot as plt
import warnings
import time
from itertools import product

# 警告無視
warnings.filterwarnings("ignore")

# データロード
data = load_breast_cancer()
X, y = data.data, data.target

# データ分割
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# モデルごとのハイパーパラメータリスト（探索範囲を広げた）
param_grid = {
    'SVM': {
        'C': [0.01, 0.1, 1, 10, 100],
        'gamma': ['scale', 'auto', 0.001, 0.01, 0.1],
        'kernel': ['rbf', 'linear']
    },
    'Random Forest': {
        'n_estimators': [50, 100, 200],
        'max_depth': [5, 10, None],
        'min_samples_split': [2, 5]
    },
    'AdaBoost': {
        'n_estimators': [50, 100, 200],
        'learning_rate': [0.1, 0.5, 1.0]
    },
    'Gaussian Process': {
        'length_scale': [0.1, 0.5, 1.0, 2.0]
    }
}

# モデル作成
def create_models():
    configs = []
    # SVM
    for C, gamma, kernel in product(param_grid['SVM']['C'], param_grid['SVM']['gamma'], param_grid['SVM']['kernel']):
        name = f"SVM (C={C}, gamma={gamma}, kernel={kernel})"
        model = SVC(C=C, gamma=gamma, kernel=kernel)
        configs.append((name, model))
    # Random Forest
    for n_estimators, max_depth, min_samples_split in product(param_grid['Random Forest']['n_estimators'],
                                                               param_grid['Random Forest']['max_depth'],
                                                               param_grid['Random Forest']['min_samples_split']):
        name = f"RF (n_estimators={n_estimators}, max_depth={max_depth}, min_samples_split={min_samples_split})"
        model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth,
                                       min_samples_split=min_samples_split, random_state=42)
        configs.append((name, model))
    # AdaBoost
    for n_estimators, learning_rate in product(param_grid['AdaBoost']['n_estimators'], param_grid['AdaBoost']['learning_rate']):
        name = f"AdaBoost (n_estimators={n_estimators}, learning_rate={learning_rate})"
        model = AdaBoostClassifier(n_estimators=n_estimators, learning_rate=learning_rate, random_state=42)
        configs.append((name, model))
    # Gaussian Process
    for length_scale in param_grid['Gaussian Process']['length_scale']:
        name = f"GP (length_scale={length_scale})"
        model = GaussianProcessClassifier(kernel=RBF(length_scale=length_scale))
        configs.append((name, model))
    return configs

# 並列実行用
def train_and_evaluate(config):
    name, model = config
    start_time = time.time()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    elapsed_time = time.time() - start_time
    return (name, acc, elapsed_time)

if __name__ == '__main__':
    model_configs = create_models()

    # プロセスプール
    with mp.Pool(processes=mp.cpu_count()) as pool:
        results = pool.map(train_and_evaluate, model_configs)

    # 精度順にソート
    results.sort(key=lambda x: x[1], reverse=True)

    # 結果表示
    print(f"{'Model':<80} {'Accuracy':<10} {'Time (s)':<10}")
    print("-" * 110)
    for name, acc, elapsed in results:
        print(f"{name:<80} {acc:<10.4f} {elapsed:<10.2f}")

    # データ準備
    model_names = [r[0] for r in results]
    accuracies = [r[1] for r in results]
    times = [r[2] for r in results]

    # --- Accuracyをbarhグラフ ---
    plt.figure(figsize=(12, len(model_names) * 0.1))
    plt.barh(model_names, accuracies, color='skyblue')
    plt.xlabel('Accuracy')
    plt.title('Model Accuracy Comparison')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # --- Timeをbarhグラフ ---
    plt.figure(figsize=(12, len(model_names) * 0.1))
    plt.barh(model_names, times, color='lightcoral')
    plt.xlabel('Training and Prediction Time (seconds)')
    plt.title('Model Training Time Comparison')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

