import numpy as np
from sklearn.decomposition import PCA
import editdistance as ed
import itertools
import pickle
import sys

used_ipa=set("ɑɑæʌɔaʊaɪbt͡ʃdðɛɹ̩eɪfɡhɪid͡ʒklmnŋoʊɔɪpɹsʃtθʊuvwjzʒabcdefghijklmnopqrstuvwxyz")


class Utterance:
    def __init__(self):
        self.hypothesis = []
        self.gold_trn = None
        self.gold_orig = None
        self.gold_idx = None


class Dataset:

    def __init__(self, batch_size=10, length=3000, dataset_path=None, train_q = 0.7, valid_q = 0.2, trigrams=False):

        self.dataset_path = dataset_path
        self.data_X = None
        self.data_Y = None
        bigrs = []
        trigrs = []
        for comb in itertools.product(used_ipa, repeat=2):
            bigrs.append(comb[0] + comb[1])
        for comb in itertools.product(used_ipa, repeat=3):
            trigrs.append(comb[0] + comb[1] + comb[2])
        bigrs = set(bigrs)
        trigrs = set(trigrs)
        self.unigram_map = {y: x for x,y in list(enumerate(used_ipa))}
        self.bigram_map = {y: (x + len(used_ipa)) for x, y in list(enumerate(bigrs))}
        self.trigram_map = {y: (x + len(used_ipa) + len(bigrs)) for x, y in list(enumerate(trigrs))}
        self.batch_size = batch_size
        self.idx = 0
        self.length = length
        self.train_q = train_q
        self.train_size = int(train_q * length)
        self.valid_size = int(valid_q * length)
        self.test_size = length - self.train_size - self.valid_size
        self.trigrams = trigrams
        np.random.seed(42)
        self.perm = np.random.permutation(self.train_size)

    def get_original_gold(self, size=100):
        perm = np.random.permutation(self.length)
        with open(self.dataset_path, "rb") as f:
                utterances = pickle.load(f)
        i=0
        output = []
        utterances = np.array(utterances)
        for utt in utterances[perm[:size]]:
            output.append((utt.gold_trn, utt.gold_orig, utt.hypothesis[self.compute_gold_idx(utt.hypothesis, utt.gold_trn)]))

        return output

    def load_data(self, size, pickled_data=None, include_gold=False, save=False):
        if pickled_data is not None:
            with open(pickled_data, "rb") as f:
                self.data_X, self.data_Y = pickle.load(f)
        else:
            with open(self.dataset_path, "rb") as f:
                utterances = pickle.load(f)
            i=0
            for utt in utterances[:self.length]:
                i+= 1
                vec, label = self.vectorize_utt(utt, size, include_gold)
                if self.data_X is None:
                    self.data_X = np.array([vec])
                    self.data_Y = np.array([label])
                else:
                    self.data_X = np.concatenate((self.data_X, [vec]), axis=0)
                    self.data_Y = np.concatenate((self.data_Y, [label]))

            with open("dataset_binary.dump", "wb") as f:
                pickle.dump((self.data_X, self.data_Y), f)

        # pca = PCA(n_components=9000)
        # print(self.data_X.shape)
        # pca.fit(self.data_X)
        # self.data_X = pca.transform(self.data_X)
        # print(self.data_X.shape)
        self.train_X, self.train_Y = self.data_X[:self.train_size], self.data_Y[:self.train_size]
        self.valid_X, self.valid_Y = self.data_X[self.train_size:(self.train_size + self.valid_size)], self.data_Y[self.train_size:(self.train_size + self.valid_size)]
        self.test_X, self.test_Y = self.data_X[(self.train_size + self.valid_size):self.length], self.data_Y[(self.train_size + self.valid_size):self.length]

    def compute_gold_idx(self, hypothesis, gold):
        distances = []
        for hyp in hypothesis:
            distances.append(ed.eval(gold, hyp))
        return np.argmin(distances)

    def vectorize_utt(self, utt, size, include_gold):
        acc = None
        transcriptions = np.array(utt.hypothesis)[:size]
        perm = np.random.permutation(len(transcriptions))
        # perm = range(len(transcriptions))
        if include_gold:
            transcriptions = np.concatenate((transcriptions[:(size-1)],[utt.gold_trn]))
            perm = np.random.permutation(size)
        # last is the ortographic transcription
        transcriptions = np.concatenate((transcriptions[perm], [utt.gold_orig]))

        for trn in transcriptions:
            if self.trigrams:
                vec = np.zeros(len(self.unigram_map) + len(self.bigram_map) + len(self.trigram_map))
            else:
                vec = np.zeros(len(self.unigram_map) + len(self.bigram_map))
            last = None
            butlast = None
            for b in trn.strip().lower():
                if b not in used_ipa:
                    continue
                vec[self.unigram_map[b]] += 1
                if last is None:
                    last = b
                    continue
                bigr = last + b
                vec[self.bigram_map[bigr]] += 1
                if self.trigrams:
                    if butlast is None:
                        butlast = last
                    else:
                        trigr = butlast + last + b
                        vec[self.trigram_map[trigr]] += 1
                        butlast = last
                last = b
            if acc is None:
                acc = vec
                # matrix = np.array([vec])
            else:
                acc = np.concatenate((acc, vec))
                # matrix = np.concatenate((matrix, [vec]), axis=1)
        return acc, self.compute_gold_idx(transcriptions[:-1], utt.gold_trn)

    def next_batch(self):
        X, Y = self.train_X[self.perm], self.train_Y[self.perm]
        while True:
            if self.idx >= self.train_size:
                self.perm = np.random.permutation(self.train_size)
                X, Y = self.train_X[self.perm], self.train_Y[self.perm]
                self.idx = 0
            last_idx = self.idx
            self.idx += self.batch_size
            yield X[last_idx:self.idx], Y[last_idx:self.idx]

    def batch_end(self):
        return self.idx >= self.train_size


    def get_data(self):
        return self.data_X, self.data_Y

    def get_train(self):
        return self.train_X, self.train_Y

    def get_valid(self):
        return self.valid_X, self.valid_Y

    def get_test(self):
        return self.test_X, self.test_Y


if __name__ == '__main__':
    dataset = Dataset(dataset_path="dataset.dump")
    dataset.load_data(size=4, include_gold=False, save=False)
    X,y = dataset.get_data()
    print(np.bincount(y)/len(y))
