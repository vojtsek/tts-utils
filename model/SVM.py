from sklearn.svm import SVC
import argparse
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from dataset import Dataset, Utterance

ap = argparse.ArgumentParser()
ap.add_argument("-l", type=int)
ap.add_argument("-s", type=int)
ap.add_argument("-e", type=int)
ap.add_argument("--include_gold", action="store_true")
ap.add_argument("--model")
args = ap.parse_args()

data_count = 1000
train_coef = 0.85
train_size = int(data_count * train_coef)
d = Dataset(length=args.s, dataset_path="dataset.dump")
d.load_data(size=4, include_gold=args.include_gold)
data_X, data_y = d.get_data()
train_X, train_y = d.get_train()
valid_X, valid_y = d.get_valid()
mdl = args.model
if mdl == "svc":
    model = SVC(kernel="linear")
elif mdl == "rf":
    model = RandomForestClassifier(n_estimators=100)
elif mdl == "lr":
    model = LogisticRegression()
model.fit(train_X, train_y)
predictions = model.predict(valid_X)
diff = abs(valid_y - predictions)
print(1 - ((sum(diff))/len(diff)))