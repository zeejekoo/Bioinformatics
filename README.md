# Automated NGS Data Quality Control and Trimming Pipeline

## Project Overview
This project provides a robust Bash-based automation script for the initial processing of Next-Generation Sequencing (NGS) data. The pipeline automatically detects paired-end FastQ files, performs quality assessment using **FastQC**, and executes precise adapter/poly-A tail trimming using **Cutadapt**.

## Key Features
- **Automated Paired-end Detection:** Automatically identifies and pairs `_R1` and `_R2` files within a directory.
- **Comprehensive QC:** Runs FastQC on all raw data to evaluate sequence quality before processing.
- **Advanced Trimming:** - Removes standard Illumina Universal Adapters.
  - Specifically targets and trims **Poly-A tails** (common in mRNA-seq).
  - Filters out short reads (length < 20bp) to ensure downstream mapping accuracy.
- **Efficiency:** Streamlines repetitive manual tasks into a single-command execution.

## Requirements
- **FastQC:** For sequence quality control.
- **Cutadapt:** For adapter trimming and sequence filtering.
- **Bash Shell:** Optimized for Linux/macOS environments.

## Pipeline Workflow
1. **Discovery:** Search for `*.fastq.gz` or `*.fq.gz` files in the source directory.
2. **Quality Control:** Execute `fastqc` on all detected raw files.
3. **Trimming (Cutadapt):**
    - **Adapter:** Illumina Universal (e.g., `-a AGATCGGAAGAG...`)
    - **Poly-A:** Using specific Cutadapt flags for homopolymer removal.
    - **Filtering:** Minimum length threshold set to 20bp.
    - **Paired-end Mode:** Synchronized trimming of R1 and R2 files.
4. **Output:** Generation of cleaned FastQ files and processing logs.

## Usage
```bash
chmod +x run_pipeline.sh
./run_pipeline.sh /path/to/fastq_directory
