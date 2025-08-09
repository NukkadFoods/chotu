#!/bin/bash

echo "🤖 Starting Enhanced Chotu AI Assistant..."
echo "============================================"

# Check if we're in the right directory
if [ ! -f "chotu.py" ]; then
    echo "❌ Error: chotu.py not found in current directory"
    echo "Please run this script from the chotu project directory"
    exit 1
fi

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed or not in PATH"
    exit 1
fi

echo "✅ Python 3 found"

# Check basic dependencies
echo "🔍 Checking dependencies..."
python3 -c "
import sys
required_packages = ['requests', 'asyncio', 'pathlib', 'json']
missing = []

for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        missing.append(package)

if missing:
    print(f'❌ Missing packages: {missing}')
    sys.exit(1)
else:
    print('✅ Core dependencies available')
"

if [ $? -ne 0 ]; then
    echo "❌ Please install missing dependencies"
    exit 1
fi

echo "🎯 Enhanced Features:"
echo "   • Self-learning MCP server"
echo "   • 3-stage confidence system"
echo "   • Dynamic tool generation"
echo "   • Voice activation support"
echo "============================================"

echo "🚀 Launching Enhanced Chotu AI Assistant..."
echo "   (MCP server will start automatically)"
echo ""

# Start Chotu (it will start the MCP server automatically)
python3 chotu.py

echo "👋 Chotu AI Assistant has been shut down. Goodbye!"
