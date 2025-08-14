# CGCNN for Band gap prediction from Matminer data

This repository contains a complete machine learning pipeline for predicting the **Band Gap** of materials using atomic features.

## Summary

- Dataset: 10611 materials with Band gap data.
- Features: Using CGCNN
- Targets: Band Gap
- Models: CGCNN

## Key Results

Test:
MAE: 0.2719 eV
RMSE: 0.4992 eV

## 📁 Project Structure

```
cgcnn_bandgap/
├── data/
│   ├── raw/                     
│       ├── matbench_mp_gap.csv        # Generated upon running datagetter.py
│   ├── processed/
│       ├── id_prop.csv                # Contains id, target             
│       ├── cif/                       # Contains all the cif files
│           ├── id_prop.csv            # Contains id, target
│           ├── atom_init.json         # element embeddings for CGCNN
│           ├── matbench_000000.cif    # cif for structure 000000
│           ├── ...
│           ├── ...
│           ├── matbench_010610.cif    # cif for structure 010610
├── external/
│   ├── cgcnn/                         # CGCNN code
│       ├── test_results.csv           # Generated after training
│       ├── parity_plot.png            # Generated after postprocessing
│       ├── metrics.json               # Generated after postprocessing
│       ├── model_best.pth.tar         # Generated after training
│       ├── checkpoint.pth.tar         # Generated after training
├── src/
│   ├── evaluate.py                    # postprocessing code
│   ├── prepare_matbench_mp_gap.py     # preprocessing code
├── datagetter.py                      # code to load data from Matminer and store locally 
├── environment.yml                    # Environment dependencies
├── LICENSE                            # MIT License
└── README.md                          # This file
```

## How to Run

After cloning, install dependencies:

```bash
conda env create -f environment.yml
conda activate cgcnn-env
```

Obtain data and preprocess it:

```bash
python3 datagetter.py
python3 src/prepare_matbench_mp_gap.py
```

Move some files around (required for CGCNN):

```bash
cp data/processed/id_prop.csv data/processed/cif/.
cp external/cgcnn/data/sample-regression/atom_init.json data/processed/cif/.
```

Run training step (takes a few hours on GPU)

```bash
cd external/cgcnn
python3 main.py --train-ratio 0.8 --val-ratio 0.1 --test-ratio 0.1 -b 128 --epochs 100 --atom-fea-len 64 --h-fea-len 128 --n-conv 3 --n-h 1 ../../data/processed/cif
```

Postprocess data to obtain fit and parity plot

```bash
cd ../../
python3 src/evaluate.py
```
Open external/cgcnn to obtain metrics.json and parity_plot.png


## Author

Created by Asmita Jana (asmitajana[at]gmail[dot]com)
This project was built as a scientific benchmark for CGCNN on band gap datasets.
Please cite Xie and Grossman (2018): Xie, T., & Grossman, J. C. (2018). Crystal graph convolutional neural networks for an accurate and interpretable prediction of material properties. Physical review letters, 120(14), 145301.

---

Feel free to use this as a template or baseline for your own ML materials science projects!
