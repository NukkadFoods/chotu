#!/usr/bin/env python3
"""
🔧 DEPENDENCY MANAGER
====================
CLI tool for managing dependencies and updating the schema
"""

import sys
import argparse
from schema_manager import SchemaManager

def main():
    parser = argparse.ArgumentParser(description="Manage dependencies and update schema")
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Add package command
    add_pkg = subparsers.add_parser('add-pkg', help='Add Python package')
    add_pkg.add_argument('package', help='Package name')
    add_pkg.add_argument('--version', help='Package version')
    
    # Remove package command
    remove_pkg = subparsers.add_parser('remove-pkg', help='Remove Python package')
    remove_pkg.add_argument('package', help='Package name')
    
    # Add tool command
    add_tool = subparsers.add_parser('add-tool', help='Add system tool')
    add_tool.add_argument('tool', help='Tool name')
    add_tool.add_argument('--install-cmd', help='Installation command')
    
    # Remove tool command
    remove_tool = subparsers.add_parser('remove-tool', help='Remove system tool')
    remove_tool.add_argument('tool', help='Tool name')
    
    # Verify command
    subparsers.add_parser('verify', help='Verify all dependencies')
    
    # Update command
    subparsers.add_parser('update', help='Update system information')
    
    # Status command
    subparsers.add_parser('status', help='Show schema status')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    manager = SchemaManager()
    
    if args.command == 'add-pkg':
        manager.add_python_package(args.package, args.version)
    
    elif args.command == 'remove-pkg':
        manager.remove_python_package(args.package)
    
    elif args.command == 'add-tool':
        manager.add_system_tool(args.tool, args.install_cmd)
    
    elif args.command == 'remove-tool':
        manager.remove_system_tool(args.tool)
    
    elif args.command == 'verify':
        manager.verify_dependencies()
    
    elif args.command == 'update':
        manager.update_system_info()
    
    elif args.command == 'status':
        summary = manager.get_schema_summary()
        print("📋 Schema Status:")
        print("=" * 30)
        for key, value in summary.items():
            print(f"{key.replace('_', ' ').title()}: {value}")

if __name__ == "__main__":
    main()
