# Raw Dataset — Version 1

## Dataset

Climate Change: Earth Surface Temperature Data

## Sources

- [Kaggle dataset](https://www.kaggle.com/datasets/berkeleyearth/climate-change-earth-surface-temperature-data)
- [Original Berkeley Earth data](https://berkeleyearth.org/data/)

## Date downloaded

31 August 2026

## Files used

- `GlobalTemperatures.csv`
- `GlobalLandTemperaturesByCountry.csv`

## Data handling

Files in this directory contain the original downloaded data and must not be
modified manually.

Cleaning and transformation operations are documented in Jupyter notebooks.
Derived datasets are stored under `data/processed/v1/`.

## Licence

The Kaggle dataset page identifies the downloaded snapshot licence as
CC BY-NC-SA 4.0.

The data is used for an educational, non-commercial project with attribution.

## Known limitations

- This is a historical snapshot and must not be presented as current data.
- Historical measurements contain differing levels of uncertainty.
- Geographic coverage and measurement quality vary over time and location.
- Country names and boundaries may have changed.
- Country labels may include territories or historical geographical names.
- Average temperature is not the same as a temperature anomaly.