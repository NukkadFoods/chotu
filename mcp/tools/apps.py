# mcp/tools/apps.py
import subprocess
import os

# Common app name mappings
APP_NAME_MAPPINGS = {
    'chrome': 'Google Chrome',
    'google chrome': 'Google Chrome',
    'safari': 'Safari',
    'firefox': 'Firefox',
    'edge': 'Microsoft Edge',
    'terminal': 'Terminal',
    'finder': 'Finder',
    'system preferences': 'System Preferences',
    'preferences': 'System Preferences',
    'settings': 'System Preferences',
    'app store': 'App Store',
    'mail': 'Mail',
    'messages': 'Messages',
    'facetime': 'FaceTime',
    'calculator': 'Calculator',
    'calendar': 'Calendar',
    'contacts': 'Contacts',
    'notes': 'Notes',
    'reminders': 'Reminders',
    'photos': 'Photos',
    'music': 'Music',
    'tv': 'TV',
    'podcast': 'Podcasts',
    'books': 'Books',
    'pages': 'Pages',
    'numbers': 'Numbers',
    'keynote': 'Keynote',
    'xcode': 'Xcode',
    'vs code': 'Visual Studio Code',
    'vscode': 'Visual Studio Code',
    'code': 'Visual Studio Code'
}

def normalize_app_name(name):
    """Normalize app name to proper application name"""
    # Remove common words and clean up