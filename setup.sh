#!/bin/bash

echo "🚀 Setting up Chotu AI Agent..."

# Install Python dependencies
echo "📦 Installing Python packages..."
pip3 install -r requirements.txt

# Update MCP server with your actual username
echo "🔧 Updating file paths..."
USERNAME=$(whoami)
sed -i '' "s/yourname/$USERNAME/g" mcp/mcp_server.py

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Add your OpenAI API key to config/secrets.json"
echo "2. Run: python3 mcp/mcp_server.py (in one terminal)"
echo "3. Run: python3 chotu.py (in another terminal)"
echo ""
echo "🎯 Chotu is ready to serve!"
