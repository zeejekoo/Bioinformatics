# Gene Regulatory Network (GRN) Construction & WGCNA Implementation

## 🧬 Project Overview
This repository demonstrates the manual construction of a **Gene Regulatory Network (GRN)** using the core mathematical principles of **Weighted Gene Co-expression Network Analysis (WGCNA)**. 

Instead of relying on automated black-box packages, this project implements the step-by-step matrix calculations (Correlation, Adjacency, TOM) from scratch using single-cell RNA-seq data. The goal is to identify and visualize tightly regulated gene modules within a specific cell type.

## 🎯 Key Objectives & Analytical Workflow

### 1. Data Preprocessing & Targeted Selection
* **Target Cell Isolation:** Extracted `Endothelial` cells from the `brain_small.h5ad` dataset to analyze cell-type-specific regulatory mechanisms.
* **Dimensionality Reduction:** Selected the **Top 500 Highly Variable Genes (HVG)** to reduce computational noise and focus on biologically significant expression variance.

### 2. Co-expression & Adjacency Calculation
* **Correlation Matrix:** Computed pairwise gene expression relationships using Pearson correlation (`numpy.corrcoef`).
* **Soft-Thresholding:** Applied WGCNA's power-law transformation ($\beta = 3$) to the correlation matrix ($|correlation\_matrix|^\beta$) to construct a weighted **Adjacency Matrix**, penalizing weak correlations and emphasizing strong regulatory links.
* **Connectivity:** Calculated network connectivity (restricted to positive correlations) to identify potential hub genes.

### 3. Topological Overlap Matrix (TOM)
* **TOM Calculation:** Computed the Topological Overlap Matrix to measure the interconnectedness of gene pairs based on their shared neighbors.
* **Distance Matrix:** Derived the **DistTOM** ($1 - TOM$) matrix, which serves as a robust dissimilarity metric for clustering.

### 4. Module Identification
* **Hierarchical Clustering:** Applied `AgglomerativeClustering` (via `scikit-learn`) on the DistTOM matrix to dynamically group the 500 genes into functional co-expression modules.

### 5. Network Visualization
* **Graph Construction:** Utilized **NetworkX** to build a complex graph mapping the topological structure of the gene network.
* **Centrality Mapping:** Scaled node sizes based on **Degree Centrality** to visually highlight the most influential "hub" genes within the endothelial regulatory network.

---

## 📊 Visual Results

*(Note: Add your output images to an `images/` folder in this repository to display them below)*

### Gene Regulatory Network (GRN)
![GRN Visualization](./images/network_plot.png)
> *Figure 1: High-resolution network graph of the top 500 HVGs in Endothelial cells. Node sizes correspond to degree centrality, highlighting key regulatory hub genes.*

### Correlation & TOM Heatmaps
![TOM Matrix](./images/tom_heatmap.png)
> *Figure 2: Heatmap representation of the Topological Overlap Matrix (TOM) showing clustered gene modules.*

---

## 💻 Tech Stack
* **Language:** Python
* **Bioinformatics Core:** Scanpy, AnnData
* **Mathematics & Clustering:** NumPy, SciPy, Scikit-learn
* **Network Analysis:** NetworkX
* **Visualization:** Matplotlib, Seaborn

## 🚀 How to Run
1. Clone this repository to your local machine.
2. Ensure you have the required environment set up (managed via `uv` or standard `pip`).
   ```bash
   pip install scanpy numpy pandas matplotlib seaborn networkx scikit-learn
