import os
import pickle

from img2vec_pytorch import Img2Vec
from PIL import Image

img2vec = Img2Vec(cuda=False)

data_path = "data/images"

imgs = sorted(
    [f for f in os.listdir(data_path) if os.path.isfile(os.path.join(data_path, f))]
)
processed = []
vectors = []

for img in imgs:
    try:
        pimg = Image.open(os.path.join(data_path, img))
        vec = list(img2vec.get_vec(pimg, tensor=False))
        vectors.append(vec)
        processed.append(img)
    except Exception as e:
        print(img)
        continue

print(len(processed), len(vectors))

with open("data/img_vecs.p", "wb") as outfile:
    pickle.dump([vectors, processed], outfile)
