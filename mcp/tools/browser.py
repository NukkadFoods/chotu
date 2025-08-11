# mcp/tools/browser.py
import subprocess
import re

def open_url(url):
    try:
        # Check if the URL is in the format of a website (e.g. apple.com)
        if re.match(r"^(http|https)://", url):
            subprocess.run(["open", url])
            return "✅ URL opened successfully"
        else:
            # Open the specified URL directly
            subprocess.run(["open", "http://" + url])
            return "✅ URL opened successfully"
    except Exception as e:
        return "❌ Error while opening URL: {}".format(str(e))

def open_browser(url, browser="Google Chrome"):
    try:
        # Open specified browser with the specified URL
        subprocess.run(["open", "-a", browser, url])
        return "✅ Browser opened successfully"
    except Exception as e:
        return "❌ Error while opening browser: {}".format(str(e))