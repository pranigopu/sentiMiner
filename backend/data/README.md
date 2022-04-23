# Data for text mining and sentiment analysis
This data directory is meant to contain the following files statically (such that their data is constant):

- Stopword list ("stopwords.txt")

This data directory is meant to contain the following dynamically generated files:

- Scraped data ("_scraped.csv")
- Cleaned data ("_cleaned.csv")
- Normalized data ("_normalized.csv")
- Analyzed data ("_analyzed.csv")

You can add your own CSV files under the same corresponding file name (given in brackets) to analyze the data in it. However, know that your data will be overwritten if you run the view functions for new URLS.