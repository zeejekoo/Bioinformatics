# Deep Learning-based Cell Type Classifier for scRNA-seq

## 🧬 Project Overview
This repository contains a deep learning pipeline designed to automatically classify cell types from single-cell RNA sequencing (scRNA-seq) data. Built with **PyTorch Lightning**, this project implements a robust Multi-Layer Perceptron (MLP) architecture capable of learning complex, non-linear transcriptomic signatures to accurately predict cellular identities.

Unlike standard clustering approaches, this model acts as a supervised annotator, trained on reference data to perform high-throughput inference on unseen scRNA-seq datasets.

## 🎯 Key Features
* **PyTorch Lightning Integration:** Structured and scalable model training with built-in logging, validation loops, and automatic device allocation.
* **Robust Neural Architecture:** Deep MLP with Batch Normalization, ReLU activations, and Dropout to prevent overfitting on high-dimensional genomic data.
* **Class Imbalance Handling:** Implements `class_weights` within the CrossEntropyLoss function to ensure unbiased learning across rare and abundant cell populations.
* **End-to-End Pipeline:** Covers everything from data preprocessing (`LabelEncoder`, `AnnData`) to model checkpointing and inference.

---

## 🧠 Model Architecture
The core model (`SCRNAClassifier`) is a fully connected neural network structured as follows:

1. **Input Layer:** Matches the number of highly variable genes (HVGs).
2. **Hidden Block 1:** 512 units $\rightarrow$ BatchNorm1d $\rightarrow$ ReLU $\rightarrow$ Dropout (0.3)
3. **Hidden Block 2:** 256 units $\rightarrow$ BatchNorm1d $\rightarrow$ ReLU $\rightarrow$ Dropout (0.3)
4. **Hidden Block 3:** 128 units $\rightarrow$ BatchNorm1d $\rightarrow$ ReLU $\rightarrow$ Dropout (0.3)
5. **Output Layer:** Linear transformation mapping to `num_classes` (Cell Types).

---

## 🛠 Pipeline Workflow

### 1. Data Preparation & Encoding
* Loaded scRNA-seq data using `Scanpy` (`.h5ad` format).
* Converted string-based cell type annotations into categorical integer labels using `sklearn.preprocessing.LabelEncoder`.
* Split the data into Training and Validation sets.

### 2. Model Training
* **Loss Function:** `nn.CrossEntropyLoss` with custom weights for imbalanced datasets.
* **Optimizer:** Optimized via standard PyTorch optimizers configured within the Lightning module.
* **Metrics Tracking:** Real-time logging of `train_loss`, `train_acc`, `val_loss`, and `val_acc` during epochs.

### 3. Checkpointing & Inference
* **Model Checkpointing:** The pipeline saves the best model states automatically (`best_model.ckpt`).
* **Inference:** * Loaded the optimized model from the saved checkpoint.
  * Passed test set matrices (`X_test`) through the network without computing gradients (`torch.no_grad()`).
  * Used `argmax(dim=1)` to output the final predicted cell type indices and mapped them back to original biological names.

---

## 📊 Evaluation & Monitoring
*(Note: Include screenshots of your training logs or tensorboard plots here)*

* **Validation Accuracy (`val_acc`):** Monitored at each epoch to ensure the model generalizes well to unseen cells.
* **Validation Loss (`val_loss`):** Used to detect and prevent overfitting early in the training process.

---

## 💻 Tech Stack
* **Deep Learning:** PyTorch, PyTorch Lightning
* **Bioinformatics:** Scanpy, AnnData
* **Machine Learning Tools:** Scikit-learn (LabelEncoder)
* **Data Processing:** NumPy, Pandas

## 🚀 How to Run
1. Set up the virtual environment:
   ```bash
   uv venv
   source .venv/bin/activate
   uv add torch pytorch-lightning scanpy scikit-learn numpy pandas
