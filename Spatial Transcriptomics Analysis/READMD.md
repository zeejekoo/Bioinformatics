# Spatial Transcriptomics Analysis: Vizgen MERFISH & 10x Xenium

## 🔬 Project Overview
This repository demonstrates spatial transcriptomics analysis using 
two leading platforms — **Vizgen MERFISH** and **10x Genomics Xenium** 
— to map gene expression within tissue spatial context.

---

## 🛠 Technical Implementation & Workflows

### 1. Vizgen MERFISH Analysis
*(Python, Scanpy, Squidpy)*
- Loaded and preprocessed large-scale MERFISH mouse brain data
- Performed QC filtering, normalization, PCA/UMAP, and Leiden clustering
- Computed spatial neighbor graphs (Delaunay triangulation) via Squidpy
- Calculated centrality scores and co-occurrence probabilities for spatial cell-type interaction analysis
- Visualized spatial scatter plots colored by Leiden clusters

### 2. 10x Xenium Analysis — Human Lung Cancer (FFPE)
*(Python, Scanpy, Squidpy, spatialdata)*
- Loaded Xenium human lung cancer FFPE dataset via spatialdata_io
- Performed QC, normalization, PCA/UMAP, and Leiden clustering
- Queried and visualized subcellular transcript localization for AGER (Alveolar Type 1 marker) and MET (HGF receptor)
- Rendered multi-layer morphology images with cell boundaries and transcript coordinates
- Computed spatial neighbor graphs, centrality scores, and co-occurrence probabilities

---

## 💻 Tech Stack
* **Spatial Analysis:** Squidpy, spatialdata, spatialdata-plot
* **Bioinformatics:** Scanpy, AnnData
* **Data Processing:** Dask, GeoPandas, NumPy, Pandas
* **Visualization:** Matplotlib, Seaborn
