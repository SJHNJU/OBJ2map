import numpy as np

def crop_img(img):
    rows, cols, _ = img.shape
    mask1 = np.ones([rows, 3]) * 255
    mask2 = np.ones([cols, 3]) * 255
    
    for row in range(0, rows):
        if not np.all(img[row, :, :] == mask2):
            r_w1 = row
            break
    
    for row in range(rows-1, 0, -1):
        if not np.all(img[row, :, :] == mask2):
            r_w2 = row
            break

    for col in range(0, cols):
        if not np.all(img[:, col, :] == mask1):
            c_w1 = col
            break

    for col in range(cols-1, 0, -1):
        if not np.all(img[:, col, :] == mask1):
            c_w2 = col
            break
    
    return img[r_w1:r_w2, c_w1:c_w2, :]