import requests
import time

# API and Webhook URLs
API_URL = "https://spacefarmers.io/api/farmers/5f4c3f61bee614aeea52db9108646e9e500e13b42d86b8566eaa414e65a263ad"
DISCORD_WEBHOOK_ALERT = "https://discord.com/api/webhooks/1332880011727868024/NbTXtXlC9ncuXplhuaPBbPPy-7NRElIftXNQ40-2lY3YceZvm02UngsIw2DRHmYpvfZG"  # Webhook 1
DISCORD_WEBHOOK_STATS = "https://discord.com/api/webhooks/1332879227854520370/ramgXI2jFl4Ie1cE70E2ifJSOjhLsrZx1tZi1JD5YpwwdZUaFB846GpewlHDkaxHtpnC"  # Webhook 2

# Interval between checks (in seconds)
CHECK_INTERVAL = 300  # 5 minutes


def fetch_farmer_data():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json()  # Parse JSON response
    except Exception as e:
        print(f"Error fetching farmer data: {e}")
        return None


def send_discord_notification(webhook_url, message):
    payload = {"content": message}
    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
        print("Notification sent successfully.")
    except Exception as e:
        print(f"Error sending notification to {webhook_url}: {e}")


def main():
    while True:
        data = fetch_farmer_data()
        if data:
            # Extract farmer attributes
            farmer_name = data["data"]["attributes"]["farmer_name"]
            points_24h = data["data"]["attributes"]["points_24h"]
            tib_24h = data["data"]["attributes"]["tib_24h"]
            current_effort = data["data"]["attributes"]["current_effort"]
            estimated_win_seconds = data["data"]["attributes"][
                "estimated_win_seconds"]

            # Format stats message
            stats_message = (
                f"📊 Farmer Stats 📊\n"
                f"Farmer: {farmer_name}\n"
                f"Points (24h): {points_24h}\n"
                f"Tib (24h): {tib_24h}\n"
                f"Current Effort: {current_effort}%\n"
                f"Estimated Win Time: {estimated_win_seconds // 3600} hours\n")

            # Send periodic stats to Webhook 2
            send_discord_notification(DISCORD_WEBHOOK_STATS, stats_message)

            # Alert if tib_24h is less than 10
            if tib_24h < 10:
                alert_message = (f"⚠️ Alert: Low Tib! ⚠️\n"
                                 f"Farmer: {farmer_name}\n"
                                 f"Tib (24h): {tib_24h}\n"
                                 "Action may be required! 🚨")
                send_discord_notification(DISCORD_WEBHOOK_ALERT, alert_message)

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()


I want to reply this script to heroku
