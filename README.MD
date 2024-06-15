# Dia Show Program

## Description

The `dia.py` script is a dia show program that takes a directory as a parameter and displays images randomly from this directory and its subdirectories. The images are scrolled from right to left or left to right based on an optional parameter.

## Requirements

- Python 3.x
- Pillow library
- screeninfo library

## Installation

1. Clone the repository to your local machine:
   ```sh
   git clone https://github.com/wassi3/dia-show.git
   cd dia-show

2. Install requirements
   ```sh
    pip install -r requirements.txt

## Usage and command line options
   ```sh
    python dia.py <directory_path> [-m <monitor_index>] [-r]

    <directory_path>: The path to the directory containing the images you want to display.
    -m <monitor_index>: (Optional) The index of the monitor where the images will be displayed. Default is the primary monitor.
    -r: (Optional) Reverse the scroll direction from right to left.


## Examples

Display images from a directory on the primary monitor, scrolling from left to right:
    ```sh
    python dia.py "D:\path\art\"

Display images from a directory on the second monitor, scrolling from left to right:
   ```sh   
    python dia.py "D:\path\art\" -m 1

Display images from a directory on the second monitor, scrolling from right to left:
   ```sh
    python dia.py "D:\path\art\" -m 1 -r
