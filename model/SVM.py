from sklearn.svm import SVC
import argparse
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from dataset import Dataset, Utterance
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("--trigrams", action="store_true")
ap.add_argument("-s", type=int)
ap.add_argument("-e", type=int)
ap.add_argument("--include_gold", action="store_true")
ap.add_argument("--model")
args = ap.parse_args()

data_count = 1000
train_coef = 0.85
train_size = int(data_count * train_coef)
d = Dataset(length=args.s, dataset_path="dataset.dump", trigrams=args.trigrams)
d.load_data(size=4, include_gold=args.include_gold, pickled_data="dataset_binary.dump")
#d.load_data(size=4, include_gold=args.include_gold)
data_X, data_y = d.get_data()
train_X, train_y = d.get_train()
valid_X, valid_y = d.get_valid()
test_X, test_y = d.get_test()
mdl = args.model
if mdl == "svcl":
    model = SVC(kernel="linear")
elif mdl == "svcr":
    model = SVC(kernel="rbf")
elif mdl == "svcp":
    model = SVC(kernel="poly")
elif mdl == "rf":
    model = RandomForestClassifier(n_estimators=1000)
elif mdl == "lr":
    model = LogisticRegression()
print(train_X.shape)
X, y = d.get_data()
print(np.bincount(y)/len(y))
model.fit(train_X, train_y)
valid_predictions = model.predict(valid_X)
test_predictions = model.predict(test_X)
valid_diff = abs(valid_y - valid_predictions != 0)
test_diff = abs(test_y - test_predictions != 0)
print(1 - ((sum(valid_diff))/len(valid_diff)))
print(1 - ((sum(test_diff))/len(test_diff)))
