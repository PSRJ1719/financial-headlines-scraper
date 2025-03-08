import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import time
import schedule


def scrape_yahoo_finance_headlines():
    url = "https://finance.yahoo.com"  # Using Yahoo Finance homepage for headlines
    headers = {
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/115.0.0.0 Safari/537.36")
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    # Attempt to find headline elements. (This selector may need updating if the site changes.)
    headlines = []
    for h3 in soup.find_all('h3'):
        text = h3.get_text(strip=True)
        if text:
            headlines.append(text)

    if not headlines:
        print("No headlines found. The site structure may have changed.")
        return

    # Get current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    csv_filename = "financial_headlines.csv"

    try:
        # Append new headlines to the CSV file with a timestamp.
        with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            for headline in headlines:
                writer.writerow([timestamp, headline])
        print(f"Successfully scraped and saved {len(headlines)} headlines at {timestamp}.")
    except Exception as e:
        print(f"Error writing to CSV file: {e}")


def job():
    print("Starting daily scraping job...")
    scrape_yahoo_finance_headlines()


if __name__ == "__main__":
    # Schedule the job to run daily at a specific time (e.g., 09:00 AM)
    schedule_time = "09:00"
    schedule.every().day.at(schedule_time).do(job)
    print(f"Scheduled scraping job daily at {schedule_time}.")

    # Keep the script running and check for the scheduled job.
    while True:
        schedule.run_pending()
        time.sleep(60)
