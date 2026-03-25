# High-Resolution Spatial Transcriptomics Analysis: Xenium & MERSCOPE

## 🔬 Project Overview
This repository showcases the processing and visualization of **Spatial Transcriptomics (ST)** data using the highly scalable `spatialdata` ecosystem. By analyzing datasets from two leading commercial ST platforms—**10x Genomics Xenium** and **Vizgen MERSCOPE**—this project demonstrates the ability to integrate and visualize complex multi-modal spatial data, including morphology images, cell boundaries (polygons), and subcellular transcript localizations.

## 🎯 Key Objectives
- **Multi-Platform Integration:** Standardize and process data from different ST vendors using a unified `spatialdata` framework.
- **Morphology & Spatial Mapping:** Overlay physical cell boundaries and multi-channel tissue images.
- **Gene-Specific Localization:** Query and visualize the exact spatial distribution of specific biomarker genes (e.g., *AGER*, *MET*) at subcellular resolution.

---

## 🛠 Technical Implementation & Workflows

### 1. Vizgen MERSCOPE Analysis (`vizgen_analysis.ipynb`)
MERFISH-based technology provides massive spatial mapping capabilities.
* **Data Handling:** Loaded large-scale MERSCOPE output using `spatialdata`.
* **Spatial Rendering:** Rendered physical cell shapes and boundaries over the tissue coordinate space using `spatialdata_plot`.
* **Coordinate Mapping:** Managed complex spatial transformations and bounding boxes to focus on specific regions of interest (ROI).

### 2. 10x Genomics Xenium Analysis (`xenium_analysis.ipynb`)
In Situ Sequencing (ISS) based technology for high-throughput targeted gene expression.
* **Targeted Gene Query:** Filtered the dataset to specifically locate transcripts for **AGER** (Alveolar Type 1 cell marker) and **MET** (Hepatocyte growth factor receptor).
* **Multi-Layer Visualization:** - Rendered `morphology_focus` (DAPI/Tissue images).
  - Overlayed `cell_circles` to define cellular contexts.
  - Mapped specific transcript coordinates directly onto the morphology images, demonstrating subcellular resolution.

---

## 📊 Visualizations

*(Note: Add the output images from your Jupyter notebooks to an `images/` folder to display them below)*

### Vizgen MERSCOPE: Cell Segmentation Map
![Vizgen MERSCOPE Map](./images/vizgen_output.png)
> *Figure 1: Spatial representation of cell boundaries across the tissue section using MERSCOPE data.*

### 10x Xenium: Subcellular Transcript Localization (AGER & MET)
![Xenium AGER/MET Expression](./images/xenium_output.png)
> *Figure 2: Overlay of cell morphology and individual transcript spots for AGER and MET genes using Xenium data.*

---

## 💻 Tech Stack
* **Core Framework:** `spatialdata`, `spatialdata_plot`
* **Data Processing:** `dask` (for out-of-core computation of large arrays), `geopandas` (for polygon/shape handling), `anndata`
* **Visualization:** `matplotlib`, `seaborn`

## 🚀 Environment Setup
Due to the heavy dependencies required for handling massive spatial images (e.g., OME-Zarr, Dask), `uv` is recommended for fast environment creation.

```bash
uv venv
source .venv/bin/activate
uv add spatialdata spatialdata-plot dask geopandas matplotlib
