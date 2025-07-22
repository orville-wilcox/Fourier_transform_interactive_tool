Fourier Transform Visualizer - Interactive Frequency Filtering
## Description
This project is an interactive tool for visual exploration of the Fourier Transform applied to images. Built in Python, the application allows users to load any image and apply frequency filters in real-time, facilitating the understanding of how manipulating frequency components affects the spatial domain.

## Main Features:
Interactive image selection, users can browse their file system to choose any image for analysis;

Side-by-side visualization;

Original grayscale image;

Magnitude spectrum of the image’s Fourier Transform;

Reconstructed image after filtering;

## Ring-shaped frequency filter:

Users define two radii (inner and outer) delimiting a circular frequency band in the spectrum.

The band can be used to remove (block) or isolate (pass) frequencies within this ring.

Visual overlay on spectrum: A semi-transparent red overlay highlights the filtered frequency band in the Fourier spectrum, improving understanding of the affected frequency range.

Real-time adjustment: Slider changes and filter mode toggling instantly update the reconstructed image.

Save filtered images: A button allows saving the filtered image to disk, with filenames reflecting the current filter parameters.

## Tech Used
Python 3

OpenCV (cv2) for image handling and loading

NumPy for mathematical processing and transforms

Matplotlib for interactive visualization and widgets

Tkinter for file selection dialogs

Adjust the sliders to set the inner and outer radii of the frequency ring filter.

Toggle the checkbox to switch between filter modes (remove or isolate the ring).

View the original image, the Fourier magnitude spectrum with overlay, and the filtered reconstructed image side-by-side.

Use the “Save Image” button to save the current filtered result.

Use Cases:
Teaching and learning signal and image processing concepts.

Visual exploration of low-pass, high-pass, and band-pass filtering effects.

Preprocessing images to remove noise or unwanted periodic patterns.


Contributions are welcome! Feel free to open issues or pull requests.

