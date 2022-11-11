from . import cv2, np, pickle


def prepare_img(img_path, width=512, height=512):
    img = cv2.imread(img_path)
    resized_img = cv2.resize(img, (width, height))
    nx, ny, nz = np.array(resized_img).shape
    img_final = np.array(resized_img).reshape(1 * (nx * ny * nz))
    return img_final


def load_model(model_path):
    model = pickle.load(open(model_path, "rb"))
    return model
