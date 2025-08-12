# 🔒 Network Security Testing Tools

Educational tools for testing the security of your own WiFi networks.

## ⚠️ LEGAL DISCLAIMER

**IMPORTANT: These tools are for educational purposes only.**

- ✅ **ONLY** use on networks you own
- ✅ **ONLY** use with explicit written permission
- ❌ **NEVER** use on networks you don't own
- ❌ **Unauthorized access to networks is illegal**

## 🛠️ Tools Included

### 1. Network Security Tester (`network_security_tester.py`)
Tests your WiFi network against common password attacks.

**Features:**
- Scans for available networks
- Tests common password patterns
- Dictionary-based attacks
- Real-time progress monitoring
- Educational simulation mode

### 2. Wordlist Generator (`wordlist_generator.py`)
Generates custom password lists for testing.

**Features:**
- Common password patterns
- Keyboard walk patterns
- Date-based patterns
- Custom word variations
- Brute force patterns (limited)

## 📋 Requirements

### macOS Setup:
```bash
# Install aircrack-ng suite
brew install aircrack-ng

# Or using MacPorts
sudo port install aircrack-ng
```

### Linux Setup:
```bash
# Ubuntu/Debian
sudo apt-get install aircrack-ng

# CentOS/RHEL
sudo yum install aircrack-ng
```

## 🚀 Usage

### Step 1: Generate Custom Wordlist (Optional)
```bash
python3 wordlist_generator.py
```

This will:
1. Ask for custom words (names, places, etc.)
2. Generate various password patterns
3. Save to `custom_wordlist.txt`

### Step 2: Test Network Security
```bash
python3 network_security_tester.py
```

This will:
1. Scan for available WiFi networks
2. Let you select your network
3. Test common passwords
4. Show results and recommendations

### Advanced Usage with Custom Wordlist:
```bash
# Generate wordlist first
python3 wordlist_generator.py

# Then test with generated wordlist
python3 network_security_tester.py
```

## 🔍 What Gets Tested

### Common Password Patterns:
- `password`, `admin123`, `wifi123`
- `router`, `internet`, `network`
- Keyboard patterns: `qwerty123`, `asdf1234`
- Date patterns: `password2025`, `admin2024`
- Number sequences: `12345678`, `87654321`

### Custom Patterns:
- Your network name + numbers
- Common words + years
- Keyboard walks
- Dictionary words (if available)

## 📊 Understanding Results

### ✅ Strong Security:
- No weak passwords found
- Test completed without success
- **Your network is secure**

### ⚠️ Weak Security:
- Common password detected
- **Recommendation: Change to stronger password**

### 🔒 Strong Password Guidelines:
- At least 12 characters long
- Mix of uppercase, lowercase, numbers, symbols
- Avoid dictionary words
- Avoid personal information
- Use unique passphrase

## 🛡️ Security Recommendations

### For Your Network:
1. **Use WPA3** (or WPA2 if WPA3 unavailable)
2. **Strong Password**: 12+ characters, mixed case, numbers, symbols
3. **Regular Updates**: Change password periodically
4. **Disable WPS**: Turn off WiFi Protected Setup
5. **Hide SSID**: Don't broadcast network name (optional)

### Password Examples:
- ✅ Good: `MyH0use$WiFi2025!`
- ✅ Good: `Sunset-Beach-Walking-2025`
- ❌ Bad: `password123`
- ❌ Bad: `wifi2025`
- ❌ Bad: `[your-name]123`

## 🔧 Troubleshooting

### "Missing required tools" Error:
```bash
# Install aircrack-ng
brew install aircrack-ng

# Verify installation
aircrack-ng --help
```

### "Permission denied" Error:
```bash
# Run with administrator privileges
sudo python3 network_security_tester.py
```

### "No networks found" Error:
- Check WiFi is enabled
- Try running with sudo
- Verify network interface name

## 📚 Educational Resources

### Learn More About:
- **WiFi Security Protocols**: WEP, WPA, WPA2, WPA3
- **Password Security**: Entropy, complexity, length
- **Network Monitoring**: Packet capture, analysis
- **Ethical Hacking**: Responsible disclosure, legal frameworks

### Recommended Reading:
- OWASP Testing Guide
- NIST Cybersecurity Framework
- WiFi Alliance Security Documentation

## ⚖️ Legal and Ethical Use

### Legal Use Cases:
- ✅ Testing your home network
- ✅ Authorized penetration testing
- ✅ Educational research (controlled environment)
- ✅ Security auditing (with permission)

### Illegal Use Cases:
- ❌ Testing neighbor's networks
- ❌ Unauthorized access attempts
- ❌ Commercial espionage
- ❌ Any unauthorized testing

### Best Practices:
1. **Always get written permission**
2. **Document your testing scope**
3. **Report findings responsibly**
4. **Respect privacy and property**

## 🆘 Support

If you encounter issues:
1. Check the troubleshooting section
2. Verify tool installation
3. Ensure you have proper permissions
4. Review legal requirements

---

**Remember: With great power comes great responsibility. Use these tools ethically and legally!**
