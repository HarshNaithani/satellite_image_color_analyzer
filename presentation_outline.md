# PPT Outline

## Slide 1 — Title
Satellite Image Color Analyzer using Python

## Slide 2 — Motivation
- Satellite imagery contains useful visual information about land cover.
- Manual inspection is time-consuming.
- A simple explainable baseline can demonstrate image-processing concepts.

## Slide 3 — Problem Statement
Estimate approximate pixel distribution of vegetation, water, urban/built-up and other/land from an input image.

## Slide 4 — Objectives
- image loading
- preprocessing
- RGB/HSV analysis
- pixel classification
- statistics
- visualization
- PDF report

## Slide 5 — Architecture
Input → UI → preprocessing → RGB/HSV → rules → statistics → outputs.

## Slide 6 — Classification Logic
Explain the RGB/HSV thresholds and why they are only a baseline.

## Slide 7 — Results
Insert results from real satellite test images only.

## Slide 8 — Limitations
- color ambiguity
- shadows
- seasonal variation
- sensor differences
- no geographic area
- no true multispectral indices yet

## Slide 9 — Remote Sensing Upgrade
NDVI / NDWI / NDBI using appropriate bands.

## Slide 10 — Future Work
GeoTIFF, georeferencing, area estimation, labeled validation data and ML.

## Slide 11 — Conclusion
Explainable baseline + clear path toward a proper remote-sensing workflow.
