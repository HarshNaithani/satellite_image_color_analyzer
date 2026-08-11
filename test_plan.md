# Test Plan

## Test categories

| ID | Test | Expected outcome |
|---|---|---|
| T01 | Start application | Streamlit UI loads |
| T02 | Upload JPG | Image displayed |
| T03 | Upload PNG | Image displayed |
| T04 | Upload TIFF | Image displayed if supported by Pillow |
| T05 | Analyze image | Four category percentages appear |
| T06 | Percentages | Sum is approximately 100% |
| T07 | Classified image | Output image is displayed |
| T08 | Chart | Distribution chart is displayed |
| T09 | PDF report | Report downloads successfully |
| T10 | Real satellite image | Results are recorded as observed test data |

## Real-data evaluation

For every real test image, record:

- source
- date downloaded
- sensor/product if known
- bands available
- image format
- dimensions
- scene description
- output percentages
- visually obvious errors

Do not invent expected percentages. This project needs actual test observations.

## Acceptance criteria

The prototype is considered operational when:

1. the app starts without import/runtime errors;
2. a valid image can be uploaded;
3. analysis completes;
4. all four categories receive counts;
5. percentages sum to approximately 100%;
6. classified image is produced;
7. chart is produced;
8. PDF report is produced.
