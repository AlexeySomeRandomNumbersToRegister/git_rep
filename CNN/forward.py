import numpy as np

def convolution(image, filt, bias, s=1):

    (n_f, n_c_f, f, _) = filt.shape # размеры фильтра
    n_c, in_dim, _ = image.shape # размеры входного изображения
    
    out_dim = int((in_dim - f)/s)+1 # расчет выходного размера изображения
    
    out = np.zeros((n_f,out_dim,out_dim))
    
    # сворачиваем фильтр по каждой части изображения, добавляя смещение на каждом этапе 
    for curr_f in range(n_f):
        curr_y = out_y = 0
        while curr_y + f <= in_dim:
            curr_x = out_x = 0
            while curr_x + f <= in_dim:
                out[curr_f, out_y, out_x] = np.sum(filt[curr_f] * image[:,curr_y:curr_y+f, curr_x:curr_x+f]) + bias[curr_f]
                curr_x += s
                out_x += 1
            curr_y += s
            out_y += 1
        
    return out

def maxpool(image, f=2, s=2):

    n_c, h_prev, w_prev = image.shape
    
    h = int((h_prev - f)/s)+1
    w = int((w_prev - f)/s)+1
    
    downsampled = np.zeros((n_c, h, w))
    for i in range(n_c):
        # перемещает окно maxpool по изображению и передает только максимальное значение выходным данным
        curr_y = out_y = 0
        while curr_y + f <= h_prev:
            curr_x = out_x = 0
            while curr_x + f <= w_prev:
                downsampled[i, out_y, out_x] = np.max(image[i, curr_y:curr_y+f, curr_x:curr_x+f])
                curr_x += s
                out_x += 1
            curr_y += s
            out_y += 1
    return downsampled

# преобразовывает вывод модели в вероятности
def softmax(X):
    out = np.exp(X)
    return out/np.sum(out)

# вычисляет категориальную кросс-энтропию между предсказанными вероятностями (probs) и истинными метками (label).
def categoricalCrossEntropy(probs, label):
    return -np.sum(label * np.log(probs))

