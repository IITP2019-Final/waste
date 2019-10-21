import numpy as np
from PIL import Image
from waste.preprocessing_waste_image import build_model


# image_size = 50
# categories = ["침대", "의자", "소파", "책상"]
# X = []
# files = []
#
# fname = '/home/thinklim/00000447.jpg'
#
# img = Image.open(fname)
# img = img.convert('RGB')
# img = img.resize((image_size, image_size))
# print(list(img.getdata()))
#
# in_data = np.asarray(img)
# X.append(in_data)
# files.append(fname)
#
# X = np.array(X)
#
# model = build_model(X.shape[1:])
# model.load_weights('data/waste-model.hdf5')
# pred = model.predict(X)
#
#
# def image_pred():
#     for i, p in enumerate(pred):
#         y = p.argmax()
#         print("+입력:", files[i])
#         print("|품목:", categories[y])

image_size = 50
categories = ["침대", "의자", "소파", "책상"]
# X = []
files = []


def image_pred(data):
    img = Image.frombytes('RGB', (image_size, image_size), data)
    # img = img.convert('RGB')
    # img = img.resize((image_size, image_size))
    print(list(img.getdata()))

    in_data = np.asarray(img)
    # X.append(in_data)
    # files.append(fname)

    X = np.array([in_data])

    model = build_model(X.shape[1:])
    model.load_weights('data/waste-model.hdf5')
    pred = model.predict(X)

    for i, p in enumerate(pred):
        y = p.argmax()
        # print("+입력:", files[i])
        print("|품목:", categories[y])

        return categories[y]

    return None
