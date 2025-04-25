# DoubleColorProgressBar

DoubleColorProgressBar is a custom progress bar widget built with PySide6 that displays both a primary progress (bar1) and an animated overlay (animation bar). It efficiently updates only the necessary portions when the progress changes and supports custom text formatting.

## Features

- **Dual Progress Display**: Shows a static progress bar with an animated overlay.
- **Optimized Redrawing**: Uses Qt's clipping region (via `event.region()`) to repaint only the changed areas.
- **Customizable Format**: Custom text formatting with `%p` for percentage and `%v` for the current value.
- **Smooth Animation**: Leverages QTimer to drive the animation.
- **Responsive Design**: Automatically adjusts animation dimensions on widget resize.

## Installation

1. Ensure Python is installed.
2. Install PySide6 via pip:

    ````bash
    pip install PySide6
    ````

## Usage

Clone the repository and run the demo:

````bash
python [double_progress_bar.py](http://_vscodecontentref_/0)