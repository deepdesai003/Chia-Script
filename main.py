import requests
import time
import os
import sys

# API and Webhook URLs from environment variables
API_URL = os.getenv("API_URL")
DISCORD_WEBHOOK_ALERT = os.getenv("DISCORD_WEBHOOK_ALERT")
DISCORD_WEBHOOK_STATS = os.getenv("DISCORD_WEBHOOK_STATS")

# Interval between checks (in seconds)
CHECK_INTERVAL = 300  # 5 minutes

def fetch_farmer_data():
    """Fetch data from the Chia farmer API."""
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json()  # Parse JSON response
    except Exception as e:
        error_message = f"❌ Error fetching farmer data: {e}"
        print(error_message)
        send_discord_notification(DISCORD_WEBHOOK_ALERT, error_message)
        return None

def send_discord_notification(webhook_url, message):
    """Send a notification to the specified Discord webhook."""
    payload = {"content": message}
    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
        print("Notification sent successfully.")
    except Exception as e:
        print(f"Error sending notification to {webhook_url}: {e}")

def main():
    """Main function to check and send farmer stats periodically."""
    while True:
        run_once = "--once" in sys.argv
        try:
            data = fetch_farmer_data()
            if data:
                # Extract farmer attributes
                farmer_name = data["data"]["attributes"]["farmer_name"]
                points_24h = data["data"]["attributes"]["points_24h"]
                tib_24h = data["data"]["attributes"]["tib_24h"]
                current_effort = data["data"]["attributes"]["current_effort"]
                estimated_win_seconds = data["data"]["attributes"].get("estimated_win_seconds")

                # Handle missing estimated win time
                if estimated_win_seconds is None:
                    estimated_win_message = "Unknown"
                else:
                    estimated_win_message = f"{estimated_win_seconds // 3600} hours"

                # Format stats message
                stats_message = (
                    f"📊 Farmer Stats 📊\n"
                    f"Farmer: {farmer_name}\n"
                    f"Points (24h): {points_24h}\n"
                    f"Tib (24h): {tib_24h}\n"
                    f"Current Effort: {current_effort}%\n"
                    f"Estimated Win Time: {estimated_win_message}\n"
                )

                # Send periodic stats to Webhook 2
                send_discord_notification(DISCORD_WEBHOOK_STATS, stats_message)

                # Alert if tib_24h is less than 10
                if tib_24h < 10:
                    alert_message = (
                        f"⚠️ Alert: Low Tib! ⚠️\n"
                        f"Farmer: {farmer_name}\n"
                        f"Tib (24h): {tib_24h}\n"
                        "Action may be required! 🚨"
                    )
                    send_discord_notification(DISCORD_WEBHOOK_ALERT, alert_message)

        except Exception as e:
            error_message = f"🔥 Unexpected error: {e}"
            print(error_message)
            send_discord_notification(DISCORD_WEBHOOK_ALERT, error_message)

        if run_once:
            break
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
