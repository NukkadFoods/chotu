# 🤖 Chotu - Advanced AI Assistant

Chotu is an intelligent, self-learning AI assistant built with advanced capabilities including voice recognition, web automation, system control, and autonomous learning features.

## 🚀 Features

### Core Capabilities
- **🎙️ Voice Recognition**: Natural language processing with confidence scoring
- **🌐 Web Automation**: YouTube video playing with smart ad-skipping
- **🖥️ System Control**: Brightness, volume, Bluetooth, battery monitoring
- **📱 App Management**: Launch applications, manage windows
- **🧠 Self-Learning**: Autonomous capability generation and improvement
- **🛡️ Safety Features**: Multi-layer validation and security measures

### Advanced Features
- **🎥 YouTube Automation**: Automated video search and playbook with ad-skipping
- **📚 ROM Memory System**: Permanent learning and pattern recognition
- **🔧 MCP Server**: Model Context Protocol for dynamic tool loading
- **📊 Performance Monitoring**: Learning success rates and optimization
- **🔒 Security**: Comprehensive validation and safety patterns

## 🏗️ Architecture

```
chotu/
├── chotu.py                     # Main entry point
├── chotu_ai/                    # Core AI modules
│   ├── ai_engine.py            # AI processing engine
│   ├── nlp_analyzer.py         # Natural language processing
│   └── memory/                 # Memory management
├── mcp/                        # Model Context Protocol server
│   ├── mcp_server.py          # Main MCP server
│   ├── tools/                 # Dynamic tools
│   └── self_learning/         # Autonomous learning
├── config/                    # Configuration files
│   ├── web_profiles/          # Website automation profiles
│   └── settings.json          # Core settings
├── memory/                    # Learning and memory storage
│   ├── rom.json              # Permanent memory (ROM)
│   ├── web_learnings.json    # Web automation patterns
│   └── learning_logs.json    # Learning history
└── chotu_youtube_player.py   # YouTube automation with safety
```

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- macOS (primary platform)
- Chrome browser
- OpenAI API key

### Setup
```bash
# Clone the repository
git clone https://github.com/nukkadfoods/chotu.git
cd chotu

# Install dependencies
chmod +x setup.sh
./setup.sh

# Configure OpenAI API
cp config/secrets.json.example config/secrets.json
# Edit secrets.json with your OpenAI API key

# Run Chotu
python3 chotu.py
```

## 🎯 Usage

### Voice Commands
```bash
# Start Chotu voice assistant
python3 chotu.py

# Example voice commands:
"play Bollywood music on YouTube"
"search and play kitne bechain hoke on YouTube"
"open Chrome and search YouTube"
"increase brightness to 80%"
"list Bluetooth devices"
"take a screenshot"
"check battery status"
```

### YouTube Automation
- **Safe Ad-Skipping**: Automatically detects and skips YouTube ads
- **Multi-layer Validation**: Prevents accidental clicks on ads
- **Forbidden Pattern Detection**: Blocks shopping/promotional content
- **Tab Management**: Closes unwanted advertising tabs

## 🧠 How Chotu Learns

1. **First Time**: Uses GPT to interpret commands
2. **Success**: Saves experience to ROM memory
3. **Pattern Recognition**: Identifies command patterns and automation flows
4. **Next Time**: Recognizes pattern and acts with high confidence
5. **Evolution**: Gets faster and smarter with each interaction
6. **Safety Learning**: Learns from mistakes and updates safety patterns

## 🔧 Capabilities

### System Control
- Volume adjustment and muting
- Brightness control with percentage settings
- Bluetooth device management
- Battery status monitoring
- Screenshot capture
- System information retrieval

### Web Automation
- YouTube video search and playback
- Smart ad-skipping with safety validation
- Browser control and navigation
- Website interaction patterns

### App Management
- Application launching and control
- Window management
- File and folder operations

### Learning & Memory
- Permanent ROM storage for successful patterns
- Web automation learning with safety measures
- Command pattern recognition
- Performance tracking and optimization

## 🛡️ Safety Features

### Web Automation Safety
- **Multi-layer validation**: Element class + text + URL checking
- **Forbidden pattern detection**: Blocks shopping/ad keywords like "shop now", "buy now"
- **Tab management**: Automatically closes unwanted tabs (Flipkart, Amazon, etc.)
- **Safety learning**: Learns from mistakes and updates patterns permanently

### Security Measures
- **API key protection**: Never commits secrets to repository
- **Sandbox execution**: Safe tool execution environment
- **Resource limits**: Prevents excessive resource usage
- **Validation layers**: Multiple security checks for all operations

## 📚 Learning System

### ROM (Read-Only Memory)
Permanent learning storage for:
- Web automation patterns and safety measures
- YouTube automation with ad-skipping protocols
- Command recognition patterns
- Success/failure analysis and recovery

### Adaptive Learning
- **Pattern recognition**: Learns user command patterns
- **Success tracking**: Monitors task completion rates
- **Error recovery**: Learns from failures and improves
- **Autonomous improvement**: Self-generates new capabilities

## 🔌 API & Integration

### MCP Server Endpoints
```
POST /execute          - Execute commands
GET  /health           - Health check
GET  /capabilities     - List available tools
POST /learn            - Manual learning
GET  /learning_stats   - Learning statistics
POST /autonomous_learn - Trigger autonomous learning
```

## 🏆 Recent Achievements

- ✅ **YouTube Automation**: Safe video playing with comprehensive ad-skipping
- ✅ **Safety Learning**: Permanent safety pattern recognition after Flipkart incident
- ✅ **Voice Recognition**: Natural language command processing with confidence scoring
- ✅ **System Integration**: macOS native system controls (brightness, volume, Bluetooth)
- ✅ **Self-Learning**: Autonomous capability generation with 100% success rate
- ✅ **MCP Protocol**: Dynamic tool loading with 31+ tools

## 🚀 Quick Start

1. **Install Dependencies**:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

2. **Add OpenAI API Key**:
   Edit `config/secrets.json` with your actual API key

3. **Start Chotu**:
   ```bash
   python3 chotu.py
   ```

4. **Talk to Chotu**:
   - "play Bollywood music on YouTube"
   - "open Chrome and search YouTube" 
   - "increase brightness to 80%"
   - "list Bluetooth devices"
   - "take a screenshot"

## 🐛 Troubleshooting

### Common Issues

1. **YouTube automation fails**: Check Chrome installation and Selenium setup
2. **Voice recognition issues**: Verify microphone permissions
3. **API errors**: Check OpenAI API key in secrets.json

### Debug Mode
```bash
python3 chotu.py --debug
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add comprehensive safety validations for web automation
4. Test all new capabilities thoroughly
5. Submit a Pull Request

## 📄 License

MIT License - Built with ❤️ for the future of personal AI

---

**🤖 Chotu - Your Intelligent Assistant** | Advanced AI with Learning & Safety
