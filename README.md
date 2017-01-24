# DetermineIrreducible

[![Python Version](https://img.shields.io/badge/python-2.7-blue.svg)](https://www.python.org/)

DetermineIrreducible is a program to generate even irreducible triangulations on the Klein bottle, written in Python.

## Requirement

- Python 2.7.x

## Installation

If you have a github account, run the following command in your terminal.

```console
git clone https://github.com/shotaYNU/DetermineIrreducible.git
```

Otherwise, download this repository from download button.

## Usage

To obtain even irreducible triangulations on the Klein bottle, run the following command in your terminal.

```console
python generate.py
sh to_images.sh
```
After running the command, the following directories is created.

```
|--results
|  |--datas
|  |  |--graph0_1.json
|  |  |--graph1_1.json
|  |  |...
|  |--layouts
|  |  |--graph0_1.json
|  |  |--graph1_1.json
|  |  |...
|  |--images
|  |  |--graph0_1.eps
|  |  |--graph1_1.eps
|  |  |...
```

- The datas directory has several graph datas before facilitating visualization, written in json.
- The layouts directory has several graph datas after facilitating visualization, written in json.
- The images directory has several graph images of graph datas in the layouts directory.

## Author

[shotaYNU](https://github.com/shotaYNU)
