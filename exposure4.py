import os
import numpy as np
import matplotlib.pyplot as plt
# from matplotlib.widgets import Slider
from matplotlib.widgets import TextBox
from skimage import io


plt.close('all')
data_path = os.getcwd()

filename =  r'/' + r'chest.jfif'

im = (io.imread(data_path + filename))
im = im / np.max(im)


fig, (ax1,ax2) = plt.subplots(1,2)


im1 = ax1.imshow(im, vmin = 0, vmax = 1, cmap = 'gray')
ax1.axis('off')


im2 = ax2.imshow(im, vmin = 0, vmax = 1, cmap = 'gray')
plt.axis('off')
ax2.set_title('Original')

#%%
# fig.colorbar(im1)   
axcolor = 'lightgoldenrodyellow'

kvp_ax  = fig.add_axes([0.25, 0.15, 0.05, 0.05], facecolor = axcolor)    
# kvp = Slider(kvp_ax, 'kVp', 30, 120, valinit = 30)
kvp_box = TextBox(kvp_ax, "Enter kVp here: ")
kvp_box.text_disp.set_color('red')
kvp_box.set_val(50)

mas_ax  = fig.add_axes([0.25, 0.05, 0.05, 0.05], facecolor = axcolor)    
# mas = Slider(mas_ax, 'mAs', 0, 30, valinit = 0.0)
mas_box = TextBox(mas_ax, 'Enter mAs here: ')
mas_box.text_disp.set_color('blue')
mas_box.set_val(20)


def update(val):
    a = np.copy(im)
    [k , m] = [int(val.text) for val in [kvp_box, mas_box]]
    k = (k - 30)/48
    m = m / 30
    
    if k == 0:
        a = np.ones(im.shape)
    elif k<1:
        a[a>k] = 1
    elif k>=1:
        im1.norm.vmax = k
    b = np.copy(a)
    
    if m == 0:
        b = np.ones(im.shape)
    elif m>=0.5:
        b = b/(m+0.5)**4
    elif m<0.5:
        b = b + 3*np.random.rand(im.shape[0], im.shape[1])*(0.5-m) 
        
        
    im1.set_data(b)
    fig.canvas.draw()

for val in [kvp_box, mas_box]:
    val.on_submit(update)

plt.show()

