# Satellite Image Color Analyzer using Python

A beginner-friendly, explainable prototype for approximate pixel-based land-cover analysis of satellite images.

## What it does

1. Loads a satellite image.
2. Converts it to RGB.
3. Resizes it while preserving aspect ratio.
4. Converts pixel information to RGB/HSV features.
5. Applies transparent rule-based thresholds.
6. Assigns each pixel to:
   - Vegetation
   - Water
   - Urban/Built-up
   - Other/Land
7. Calculates pixel counts and percentages.
8. Creates a classified visualization.
9. Creates a distribution chart.
10. Generates a PDF report.

## Important scientific limitation

This version is an **RGB/HSV prototype**, not a true multispectral remote-sensing classifier.

The reported percentages are:

> percentage of image pixels assigned to each class

They are **not** geographic area in m² or hectares.

True NDVI/NDWI/NDBI requires the relevant spectral bands. Geographic area calculations require spatial resolution and georeferencing metadata, typically available in suitable GeoTIFF or equivalent remote-sensing products.

## Project architecture

```text
Satellite Image
      |
      v
Streamlit UI
      |
      v
Input Validation + RGB Conversion
      |
      v
Preprocessing / Resize
      |
      v
RGB + HSV Features
      |
      v
Explainable Rule-based Classifier
      |
      +--> Vegetation
      +--> Water
      +--> Urban/Built-up
      +--> Other/Land
      |
      v
Pixel Counts + Percentages
      |
      +--> Classified Image
      +--> Chart
      +--> PDF Report
```

## Installation on Windows

Open the project in VS Code.

In the VS Code terminal:

```bash
python --version
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

A browser tab should open with the application.

## Testing

Use real satellite imagery for project testing. Do not treat ordinary photographs as satellite validation data.

For each test image, record:

- source
- image format
- image dimensions
- visual scene description
- predicted percentages
- obvious classification errors
- observations

Suggested test scenes:

1. vegetation-dominant
2. water-dominant
3. urban-dominant
4. mixed land cover

## Future work

- stronger preprocessing
- systematic threshold calibration
- multispectral GeoTIFF support
- NDVI
- NDWI
- NDBI
- georeferencing
- actual area calculation in m²/hectares
- labeled reference data
- confusion matrix and accuracy metrics
- ML-based classification

## Academic honesty

The project deliberately starts with an interpretable baseline. Advanced remote-sensing indices and ML should only be added when the required data and validation are available.
