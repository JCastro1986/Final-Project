# Analysis of Real Estate Prices in Mexico
**Bootcamp Final Project**

![PricingUp](/Resources/PricingUp.png)

## Overview

### Topic

Given the importance and growth that the real estate has shown in Mexico in the last few years, we´ll analyze and measure the prices of housing and commercial properties considering important features like location, ground and construction surface, age, number of rooms, bathrooms, and parking, etc., by creating a model that will predict the downs and rises of the real estate prices.

### Justification

After analyzing several options, we decided to select this topic for the following reasons:
`1` To develop the analysis we’ll use almost all topics covered in the Bootcamp Course, from web scraping, ETL, working with Pandas, SQL, reading CSV, visualization, and machine learning.
`2` Also, we think it could be useful for people looking into buying a new home or simply for those seeking to maximize investing in real estate in Mexico. 
`3` Finally, this analysis could expand in determining price changes over time by scrapping information periodically, and from many other sources.

### Source of data

In this first stage of the project, we’ll download the data from `metroscubicos.com`, the third most visited webpage in Mexico which is associated with `Mercadolibre.com`, according to the marketing agency “Impactum”

![metcu](/Resources/metcu.png)


### Questions to answer

Considering the features before mentioned, the model will answer the following questions: 

**1.** Where are the places in Mexico with the highest and lowest prices per square meter by asset type (house, apartment, land)?
**2.** According to the predicted prices, where are the best opportunities for undervalued assets?

### Project steps

To achieve our goal, we’ll develop and code at least the next steps.
`1.` **Webscraping**. Create a python code with beautiful soup and splinter to retrieve asset data from several webpages, such as metroscubicos.com, and create a raw data CSV.
`2.` **ETL**. Raw data needs to be cleaned, transformed, and add new information from other sources to generate a final SQL database.
`3.` **ML model**. We will use a supervised linear regression machine learning model that helps us determine the price target variable based on features such as location, type, land size, construction square meters, number of rooms, number of bathrooms, etc.
`4.` **Dashboard**. We will create visualizations and interactions to display our results in Tableau.

## Team Members and roles

|Avatar                         |Member        |Role: Segment 1| Icon                               |
|:-----------------------------:|:------------:|:-------------:|:----------------------------------:|
![Brenda](/Resources/Brenda.png)|Brenda Treviño|ML model       |![triangle](/Resources/triangle.png)|
![Luis](/Resources/Luis.png)    |Luis Carmona  |Technology     |![x](/Resources/x.png)              |
![Carlos](/Resources/Carlos.png)|Carlos Acosta |Database       |![circle](/Resources/circle.png)    |
![Jorge](/Resources/Jorge.png)  |Jorge Castro  |Repository     |![square](/Resources/square.png)    |

