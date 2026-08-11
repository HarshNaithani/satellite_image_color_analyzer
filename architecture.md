# Flowchart

```text
START
  |
  v
Upload Satellite Image
  |
  v
Is image readable?
  |---- No ----> Show error ----> END
  |
 Yes
  |
  v
Convert to RGB
  |
  v
Resize / preprocess
  |
  v
Calculate RGB + HSV values
  |
  v
Apply classification rules
  |
  +--> Vegetation
  +--> Water
  +--> Urban/Built-up
  +--> Other/Land
  |
  v
Count pixels
  |
  v
Calculate percentages
  |
  +--> Classified image
  +--> Chart
  +--> PDF report
  |
  v
END
```
