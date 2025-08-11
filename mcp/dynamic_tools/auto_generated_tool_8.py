import subprocess

def list_wifi_networks() -> dict:
    """Scan for available WiFi networks."""
    try:
        result = subprocess.run(
            ['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '-s'],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            return {
                'status': 'success',
                'message': 'WiFi networks listed successfully',
                'data': result.stdout.strip().split('\n')
            }
        else:
            return {
                'status': 'error',
                'message': f'Command failed: {result.stderr.strip()}',
                'data': None
            }
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error: {str(e)}',
            'data': None
        }

def check_bluetooth_status() -> dict:
    """Check Bluetooth status."""
    try:
        result = subprocess.run(
            ['system_profiler', 'SPBluetoothDataType', '-json'],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            return {
                'status': 'success',
                'message': 'Bluetooth status retrieved successfully',
                'data': result.stdout.strip()
            }
        else:
            return {
                'status': 'error',
                'message': f'Command failed: {result.stderr.strip()}',
                'data': None
            }
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error: {str(e)}',
            'data': None
        }

def toggle_bluetooth(turn_on: bool) -> dict:
    """Toggle Bluetooth on or off."""
    command = ['/usr/local/bin/blueutil', '-p', '1' if turn_on else '0']
    try:
        result = subprocess.run(
            command,
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            return {
                'status': 'success',
                'message': 'Bluetooth toggled successfully',
                'data': None
            }
        else:
            return {
                'status': 'error',
                'message': f'Command failed: {result.stderr.strip()}',
                'data': None
            }
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error: {str(e)}',
            'data': None
        }

def test_network_quality() -> dict:
    """Test network connection quality."""
    try:
        result = subprocess.run(
            ['/usr/bin/networkQuality'],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode == 0:
            return {
                'status': 'success',
                'message': 'Network quality tested successfully',
                'data': result.stdout.strip()
            }
        else:
            return {
                'status': 'error',
                'message': f'Command failed: {result.stderr.strip()}',
                'data': None
            }
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error: {str(e)}',
            'data': None
        }

# Example usage
if __name__ == "__main__":
    print(list_wifi_networks())
    print(check_bluetooth_status())
    print(toggle_bluetooth(True))  # Turn on Bluetooth
    print(test_network_quality())
