import pickle

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.mixture import GaussianMixture


l = pickle.load(open("data/img_vecs.p", "rb"))
X, filenames = l[0], l[1]

n_components = np.arange(1, 31)
models = [GaussianMixture(n, covariance_type='full', random_state=0).fit(X)
          for n in n_components]

plt.plot(n_components, [m.bic(np.asarray(X)) for m in models], label='BIC')
plt.plot(n_components, [m.aic(np.asarray(X)) for m in models], label='AIC')
plt.legend(loc='best')
plt.xlabel('n_components')
plt.savefig("adas.png")
# looks like 4 is OK
best_model = models[3]
labels = best_model.predict(X)

filename_label = zip(filenames, labels)


def get_cluster(img):
    if img in filenames:
        idx = filenames.index(img)
        return labels[idx]
    else:
        return -1


def get_decade(d):
    d = str(d)
    if d[:-1].isnumeric():
        if d.endswith("s"):
            return d[:-1]
        elif d.endswith("0"):
            return d
        else:
            return d[:-1] + "0"
    else:
        return "NA"


df = pd.read_csv("data/image_metadata.tsv", sep="\t")
df["Cluster"] = [get_cluster(e) for e in df["File"]]
df["Correct decade"] = [get_decade(d) for d in df["Decade"]]

df.to_csv("data/image_data_with_clusters.tsv", sep="\t", index=False)