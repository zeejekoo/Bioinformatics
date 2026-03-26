# Cell-Type Deconvolution & Gene Regulatory Network (GRN) Analysis

## 🧬 Project Overview
This repository contains two interconnected analyses on single-cell 
RNA-seq brain data:

1. **Cell-Type Deconvolution** — Estimating cell-type proportions 
   from bulk expression data using GLM regression, CIBERSORT (NuSVR), 
   and NMF, validated against ground truth distributions.
2. **Gene Regulatory Network (GRN) via WGCNA-inspired approach** — 
   Manual implementation of weighted gene co-expression network 
   analysis from scratch, computing Correlation, Adjacency, and TOM 
   matrices to identify co-expression modules in Endothelial cells.

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


## 💻 Tech Stack
* **Language:** Python
* **Bioinformatics Core:** Scanpy, AnnData
* **Mathematics & Clustering:** NumPy, SciPy, Scikit-learn
* **Network Analysis:** NetworkX
* **Visualization:** Matplotlib, Seaborn
