# Drug Allergy Prediction

## For Chulalongkorn AI Academy candidate screening

* Compatible with Python 3.6 and 3.7

## Problem introduction

* All doctors want to avoid prescribing drugs that maybe allergic to the patients
* Enzyme-linked immunospot (ELISpot) is a laboratory technique that tests whether the patient's immune cells will respond to particular drugs. This allows doctor to screen whether a drug is likely to be safe for the patient.
* As with any test, ELISpot is not perfect. Drugs that the patient is allergic to sometimes do not elicit any response in ELISpot test (False Negative) and vice versa.
* Hence, we want to develop a prediction model for drug allergy based on patient information, drug information, and ELISpot result.

## Getting Started

Run the following command in your Terminal to install Project Dependencies

```sh
python install -r requirements.txt
```

This project requires the collection of owned data, run the following command to begin scraping Wat Pho and Wat Prakeaw Images from Google Image Search using FireFox Webdriver
Please download and place `geckodriver` on root-folder

```sh
python scrape.py "wat po" data/watpo --amount 500
python scrape.py "wat prakeaw" data/watprakeaw --amount 500
```

Also insert test images downloaded from Kaggle dataset to the following folders:

> data/watpo/test
> data/watprakeaw/test

### Code Walkthrough

Please open `image_recogntion.html` (or `image_recogniton.ipynb` if you have Jupyter Notebook instaalled) and follow the code walk-through there.
The project creates and saves a convolution neural network estimator for image processing, saved under `pickles/convulution_model.pkl`

Sample Accuracy of create model tested against 8 images found on Kaggle Competition Page:

```sh
[INFO] Floating Point Errors:
[INFO] R2: -0.4521
[INFO] Mean Squared Error: 0.3630
[INFO] Root Mean Squared Error: 0.6025
[INFO] Binary Classification Errors:
[INFO] R2: -0.5000
[INFO] Mean Squared Error: 0.3750
[INFO] Root Mean Squared Error: 0.6124
```
