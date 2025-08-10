# MCP Tools package
"""
Collection of tools for various automation tasks including:
- Web automation (Enhanced YouTube with advanced ad skipping)
- Computer vision
- System utilities
- File operations
- Email and communication
- And many more...
"""

__version__ = "1.0.0"

# Import enhanced YouTube automation for Chotu
try:
    from .enhanced_youtube_automation import (
        enhanced_youtube_play,
        enhanced_youtube_stop, 
        enhanced_youtube_close,
        enhanced_youtube_status,
        EnhancedYouTubeAutomation
    )
    from .web_automation_tool import web_automation_tool
    
    # Export the main functions for Chotu to use
    __all__ = [
        'enhanced_youtube_play',
        'enhanced_youtube_stop', 
        'enhanced_youtube_close',
        'enhanced_youtube_status',
        'web_automation_tool',
        'EnhancedYouTubeAutomation'
    ]
    
    print("✅ Chotu MCP Tools: Enhanced YouTube automation with ad skipping ready!")
    
except ImportError as e:
    print(f"⚠️ Some MCP tools not available: {e}")
    __all__ = []
