# Best Buy Auto Checkout Bot

This Python script automates the process of monitoring a Pokémon Trading Card Game product on Best Buy, adding it to the cart, proceeding to checkout, and placing the order. It includes bot evasion techniques, proxy rotation, human-like interactions, and Discord notifications.

## Features

- Monitors product availability by checking the "Add to Cart" button.
- Uses Smartproxy for automatic IP rotation.
- Human-like interactions including scrolling and randomized wait times.
- Uses JavaScript execution instead of full-page refresh to avoid detection.
- Automatically fills in CVV if required.
- Sends Discord notifications when an item is added to the cart.
- Debugging tools like printing the current IP address after each refresh.

## Requirements

Ensure you have Python installed, then install the necessary dependencies:

```sh
pip install selenium
pip install fake-useragent
pip install requests
```

## Setup Instructions

1. **Download and Install ChromeDriver:**

   - Ensure that ChromeDriver matches your Chrome version.
   - Place `chromedriver.exe` in the script directory or set it in the system PATH.

2. **Configure Smartproxy:**

   - Sign up at [Smartproxy](https://www.smartproxy.com/).
   - Get your proxy credentials and format: `http://username:password@proxy.smartproxy.com:port`.
   - Update the script with your proxy details.

3. **Modify Script Settings:**

   - Update `correct_product_url` with your desired Best Buy product.
   - Update `correct_sku` to match the SKU of the selected product.
   - Update `DISCORD_WEBHOOK_URL` with your Discord webhook for notifications.
   - Set your actual CVV number in the script (use cautiously).

## Running the Script

Run the script using:

```sh
python script.py
```

Follow the on-screen instructions to manually log in before automation begins.

## Troubleshooting

- **Browser not opening?** Ensure `chromedriver.exe` is installed and matches your Chrome version.
- **IP not rotating?** Check your Smartproxy credentials and ensure it's set up correctly in the script.
- **Element not found errors?** Inspect the Best Buy webpage, as elements might have changed.

## Disclaimer

This script is for educational purposes only. Best Buy's terms of service prohibit automated purchasing, so use at your own risk.

