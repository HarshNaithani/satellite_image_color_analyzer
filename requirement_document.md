# Requirement Document

## Functional requirements

### FR-01 Image input
The application shall accept JPG, JPEG, PNG, WEBP, TIFF and TIFF-compatible image files.

### FR-02 Preprocessing
The application shall convert uploaded images to RGB and resize them while preserving aspect ratio.

### FR-03 Feature representation
The prototype shall use RGB values and derived HSV values as pixel-level features.

### FR-04 Classification
The prototype shall classify pixels into:
- Vegetation
- Water
- Urban/Built-up
- Other/Land

### FR-05 Statistics
The application shall calculate pixel counts and percentage distribution.

### FR-06 Visualization
The application shall display the original image, classified image and distribution chart.

### FR-07 Report
The application shall generate a PDF report containing the input name, statistics, images, chart and limitations.

## Non-functional requirements

- Explainable rules
- Beginner-readable code
- Reproducible installation
- No fabricated test results
- Clear distinction between image-pixel percentages and geographic area
- Clear distinction between RGB/HSV processing and multispectral remote sensing
