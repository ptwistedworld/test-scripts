import tbselenium.common as cm
from tbselenium.tbdriver import TorBrowserDriver
import os
import time

# --- Configuration ---
# IMPORTANT: Replace this with the actual path to your Tor Browser directory
# On Windows, it might be something like: r"C:\Users\YourUser\Desktop\Tor Browser"
# On macOS, it might be something like: "/Applications/Tor Browser.app/Contents/MacOS"
# On Linux, it will be the extracted 'tor-browser' directory: "/path/to/extracted/tor-browser_en-US"
TOR_BROWSER_PATH = "/home/root/.local/share/torbrowser/tbb/x86_64/tor-browser/" # <--- **UPDATE THIS PATH**

# The URL you want to visit
TARGET_URL = " http://om6q4a6cyipxvt7ioudxt24cw4oqu4yodmqzl25mqd2hgllymrgu4aqd.onion/" # A good URL to test Tor connectivity
# TARGET_URL = "https://www.example.com" # Replace with your desired website

# --- Script ---
def visit_website_via_tor(tor_browser_path, url):
    print(f"Attempting to launch Tor Browser from: {tor_browser_path}")
    try:
        # Initialize TorBrowserDriver
        # tor_cfg=cm.USE_STEM can be used to control Tor process via Stem,
        # but for simplicity, we'll assume Tor Browser handles its own connection.
        # Ensure Tor Browser is not already running.
        with TorBrowserDriver(tor_browser_path) as driver:
            print("Tor Browser launched successfully. Connecting to Tor network...")
            # Tor Browser automatically connects to the Tor network on launch.
            # You might need to wait a bit for it to establish a circuit.
            time.sleep(300) # Give it some time to connect (adjust as needed)

            print(f"Visiting: {url}")
            driver.get(url)

            # Optional: Print the current URL and page title to confirm
            print(f"Current URL: {driver.current_url}")
            print(f"Page Title: {driver.title}")

            # Optional: Take a screenshot
            screenshot_path = "tor_website_screenshot.png"
            driver.save_screenshot(screenshot_path)
            print(f"Screenshot saved to: {screenshot_path}")

            print("Script completed. Tor Browser will close shortly.")

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure:")
        print(f"1. Tor Browser is installed at: {tor_browser_path}")
        print("2. Geckodriver is installed and accessible (in PATH or specified in TorBrowserDriver).")
        print("3. Tor Browser is not already running when the script attempts to launch it.")

if __name__ == "__main__":
    # Ensure you've updated TOR_BROWSER_PATH above before running!
    if not os.path.exists(TOR_BROWSER_PATH):
        print(f"Error: Tor Browser path does not exist: {TOR_BROWSER_PATH}")
        print("Please download and install Tor Browser, then update the 'TOR_BROWSER_PATH' variable in the script.")
    else:
        visit_website_via_tor(TOR_BROWSER_PATH, TARGET_URL)