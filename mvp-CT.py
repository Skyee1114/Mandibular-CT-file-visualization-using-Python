import os
import numpy as np
import matplotlib.pyplot as plt
import pydicom
from matplotlib.widgets import Slider, Button

path_to_dicom_file = "./CT/1.dcm"

# Read the DICOM file
dicom_file = pydicom.dcmread(path_to_dicom_file)

# Get the pixel data
pixel_data = dicom_file.pixel_array

# Get the dimensions of the pixel array
num_rows, num_cols, num_slices = np.shape(pixel_data)

# Get the window/level values from the DICOM file
window = dicom_file.WindowWidth
level = dicom_file.WindowCenter
Rescale_intercept = dicom_file.RescaleIntercept
Rescale_slope = dicom_file.RescaleSlope

# Set up the figure and subplots
fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(8, 8))
axs[0, 0].axis('off')
axs[0, 1].axis('off')
axs[1, 0].axis('off')
axs[1, 1].axis('off')

# Display the first slice of the CT scan in all subplots
im_sagittal = axs[0, 0].imshow(pixel_data[:, :, 0], cmap=plt.cm.gray, vmin=0, vmax=np.max(pixel_data)-1000)
im_coronal = axs[0, 1].imshow(pixel_data[:, 0, :], cmap=plt.cm.gray, vmin=0, vmax=np.max(pixel_data)-1000)
im_axial = axs[1, 0].imshow(pixel_data[0, :, :], cmap=plt.cm.gray, vmin=0, vmax=np.max(pixel_data)-1000)

# Set up the slider for scrolling through slices
ax_slider = plt.axes([0.2, 0.02, 0.6, 0.03])
slider = Slider(ax_slider, 'Slice Number', 0, num_slices-1, valinit=0, valstep=1)

# Set up the vertical slider for adjusting vmin from 0 to max
ax_vslider = plt.axes([0.92, 0.2, 0.03, 0.6])
vslider = Slider(ax_vslider, 'Density', -1000, np.max(pixel_data)- 1000, valinit= -1000, orientation='vertical')

# Define the function to update the image when the slider is moved
def update(val):
    slice_index = int(slider.val)
    im_sagittal.set_data(pixel_data[:, :, slice_index])
    im_coronal.set_data(pixel_data[:, slice_index, :])
    im_axial.set_data(pixel_data[slice_index, :, :])
    axs[0, 0].set_title(f"Sagittal Slice {slice_index+1}")
    axs[0, 1].set_title(f"Coronal Slice {slice_index+1}")
    axs[1, 0].set_title(f"Axial Slice {slice_index+1}")
    fig.canvas.draw_idle()

def update_vslider(val):
    vmin = vslider.val
    im_sagittal.set_clim(vmin=vmin + 1000, vmax=np.max(pixel_data))
    im_coronal.set_clim(vmin=vmin + 1000, vmax=np.max(pixel_data))
    im_axial.set_clim(vmin=vmin + 1000, vmax=np.max(pixel_data))
    fig.canvas.draw_idle()

slider.on_changed(update)
vslider.on_changed(update_vslider)

# Define the function to show the density (HU) of each part when mouse hovers over image
def hover(event):
    
    if event.inaxes == axs[0, 0]:
        x, y = int(event.xdata), int(event.ydata)
        density = pixel_data[y, x, int(slider.val)] - 1000
        axs[0, 0].set_title(f"Sagittal Slice {int(slider.val)+1} - Density: {density} HU")
        for line in axs[0, 0].lines:
            line.remove()
        axs[0, 0].axhline(y=y, color='b', linestyle='--')
        axs[0, 0].axvline(x=x, color='g', linestyle='--')
    elif event.inaxes == axs[0, 1]:
        x, y = int(event.xdata), int(event.ydata)
        density = pixel_data[y, int(slider.val), x] - 1000
        axs[0, 1].set_title(f"Coronal Slice {int(slider.val)+1} - Density: {density} HU")
        for line in axs[0, 1].lines:
            line.remove()
        axs[0, 1].axhline(y=y, color='b', linestyle='--')
        axs[0, 1].axvline(x=x, color='g', linestyle='--')
    elif event.inaxes == axs[1, 0]:
        x, y = int(event.xdata), int(event.ydata)
        density = pixel_data[int(slider.val), y, x] - 1000
        axs[1, 0].set_title(f"Axial Slice {int(slider.val)+1} - Density: {density} HU")
        for line in axs[1, 0].lines:
            line.remove()
        axs[1, 0].axhline(y=y, color='b', linestyle='--')
        axs[1, 0].axvline(x=x, color='g', linestyle='--')

    fig.canvas.draw_idle()

fig.canvas.mpl_connect("motion_notify_event", hover)

plt.show()
