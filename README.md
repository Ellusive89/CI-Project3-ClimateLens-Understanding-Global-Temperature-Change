# Raw Dataset — Version 1

## Dataset

Climate Change: Earth Surface Temperature Data

## Source

The dataset was downloaded from Kaggle:

https://www.kaggle.com/datasets/berkeleyearth/climate-change-earth-surface-temperature-data

The original temperature records were produced by Berkeley Earth:

https://berkeleyearth.org/data/

## Date downloaded

31.08.2026

## Files used

- `GlobalTemperatures.csv`
- `GlobalLandTemperaturesByCountry.csv`

## Data handling

Files in this folder contain the original downloaded data and must not be
modified manually.

All cleaning and transformation operations will be performed in Jupyter
notebooks. Cleaned datasets will be saved in `data/processed/v1/`.

## Licence

The Kaggle dataset page identifies the dataset licence as
CC BY-NC-SA 4.0.

The project will provide appropriate attribution and will be used for an
educational, non-commercial purpose.

## Known limitations

- This is a historical snapshot and should not be presented as current data.
- Historical measurements have differing levels of uncertainty.
- Geographic coverage and measurement quality vary across time and location.
- Country names and borders may not remain consistent throughout the dataset.
- Average temperature should not be interpreted as the same thing as a
  temperature anomaly.

# Initial hypotheses

## Hypothesis 1

The mean global land-and-ocean temperature during 1986–2015 is higher than during 1956–1985.

We will evaluate this using:
- Period averages
- Temperature distributions
- Effect size
- An appropriate statistical comparison
- A plain-language conclusion

## Hypothesis 2

Average global temperature-measurement uncertainty is higher before 1900 than after 1950.

We will evaluate this using:
- Period uncertainty averages
- A time-series visualisation
- Distribution comparison
- A statistical comparison
- A discussion of changes in measurement coverage and quality

## Planned predictive model

The model will be an educational historical prediction exercise—not a professional climate forecast.

It will:
- Predict a temperature value or anomaly using historical information
- Use chronological training and test periods
- Avoid random train/test splitting
- Compare the model against a simple seasonal baseline
- Report metrics such as MAE and RMSE
- Explain limitations and intended use
This distinction is essential for ethical communication.
