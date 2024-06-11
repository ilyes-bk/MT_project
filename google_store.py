from google_play_scraper import reviews_all
import pandas as pd
import time

def fetch_reviews(app_id, country):
    reviews = reviews_all(
        app_id,
        sleep_milliseconds=0,
        lang='en',
        country=country 
    )
    return reviews

def clean_data(df):
    df = df.dropna(subset=['score'])
    df['score'] = df['score'].astype(int)

    df = df.dropna(subset=['content'])

    return df


app_ids = [
    'com.google.android.apps.translate',
    'com.microsoft.translator',
    'com.deepl.mobiletranslator'
]

country_codes = [
    'us',
    'gb',
    'ca',
    'au',
    'nz',
    'ie',
    'za'
]

all_reviews = []

for app_id in app_ids:
    for country in country_codes:
        reviews = fetch_reviews(app_id, country)
        for review in reviews:
            review['app_id'] = app_id
            review['country'] = country
        all_reviews.extend(reviews)
        time.sleep(10)

df = pd.DataFrame(all_reviews)

nan_counts = df.isna().sum()
print(nan_counts)

# Clean the data
cleaned_reviews_df = clean_data(df)

# Save cleaned data to CSV
cleaned_reviews_df.to_csv('cleaned_reviews_english_speaking_countries_google_play.csv', index=False)
