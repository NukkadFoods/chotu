#!/usr/bin/env python3
"""
💾 CODE UPDATER
==============
Handles versioned backups, atomic updates, rollback capability, and dependency management
"""

import os
import shutil
import json
import hashlib
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from pathlib import Path

class CodeUpdater:
    """Advanced code updating with versioning and rollback capabilities"""
    
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.backups_dir = os.path.join(self.base_dir, "backups")
        self.tools_dir = os.path.join(self.base_dir, "tools")
        self.version_file = os.path.join(self.backups_dir, "versions.json")
        
        # Ensure directories exist
        os.makedirs(self.backups_dir, exist_ok=True)
        os.makedirs(self.tools_dir, exist_ok=True)
        
        # Initialize version tracking
        self.versions = self._load_versions()
    
    def _load_versions(self) -> Dict:
        """Load version tracking information"""
        if os.path.exists(self.version_file):
            try:
                with open(self.version_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Failed to load versions: {e}")
        
        return {
            "files": {},
            "global_version": 0,
            "last_update": None
        }
    
    def _save_versions(self):
        """Save version tracking information"""
        try:
            with open(self.version_file, 'w') as f:
                json.dump(self.versions, f, indent=2)
        except Exception as e:
            print(f"⚠️ Failed to save versions: {e}")
    
    def _calculate_file_hash(self, file_path: str) -> str:
        """Calculate SHA256 hash of a file"""
        sha256_hash = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception:
            return ""
    
    def create_backup(self, file_path: str, backup_reason: str = "manual") -> Optional[str]:
        """
        Create a versioned backup of a file
        
        Args:
            file_path: Path to the file to backup
            backup_reason: Reason for the backup
        
        Returns:
            str: Path to the backup file or None if failed
        """
        
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            return None
        
        try:
            file_name = os.path.basename(file_path)
            file_hash = self._calculate_file_hash(file_path)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Create backup filename
            backup_name = f"{file_name}_{timestamp}_{file_hash[:8]}.bak"
            backup_path = os.path.join(self.backups_dir, backup_name)
            
            # Copy file to backup location
            shutil.copy2(file_path, backup_path)
            
            # Update version tracking
            if file_name not in self.versions["files"]:
                self.versions["files"][file_name] = {
                    "current_version": 0,
                    "backups": []
                }
            
            backup_info = {
                "version": self.versions["files"][file_name]["current_version"] + 1,
                "timestamp": timestamp,
                "hash": file_hash,
                "backup_path": backup_path,
                "reason": backup_reason,
                "size": os.path.getsize(file_path)
            }
            
            self.versions["files"][file_name]["backups"].append(backup_info)
            self.versions["files"][file_name]["current_version"] = backup_info["version"]
            self.versions["global_version"] += 1
            self.versions["last_update"] = datetime.now().isoformat()
            
            self._save_versions()
            
            print(f"✅ Backup created: {backup_path}")
            return backup_path
            
        except Exception as e:
            print(f"❌ Backup failed: {e}")
            return None
    
    def atomic_update(self, file_path: str, new_content: str, update_reason: str = "auto_update") -> bool:
        """
        Perform atomic file update with backup
        
        Args:
            file_path: Path to the file to update
            new_content: New content for the file
            update_reason: Reason for the update
        
        Returns:
            bool: True if update successful
        """
        
        # Create backup if file exists
        backup_path = None
        if os.path.exists(file_path):
            backup_path = self.create_backup(file_path, f"before_{update_reason}")
            if not backup_path:
                print("❌ Failed to create backup, aborting update")
                return False
        
        # Create temporary file for atomic write
        temp_path = f"{file_path}.tmp"
        
        try:
            # Write to temporary file
            with open(temp_path, 'w') as f:
                f.write(new_content)
            
            # Verify the temporary file
            if not os.path.exists(temp_path):
                raise Exception("Temporary file was not created")
            
            # Atomic move
            shutil.move(temp_path, file_path)
            
            # Verify the update
            if not os.path.exists(file_path):
                raise Exception("File was not updated properly")
            
            print(f"✅ File updated atomically: {file_path}")
            
            # Log the update
            self._log_update(file_path, update_reason, backup_path)
            
            return True
            
        except Exception as e:
            print(f"❌ Atomic update failed: {e}")
            
            # Clean up temporary file
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except:
                    pass
            
            # Restore from backup if update failed and backup exists
            if backup_path and os.path.exists(backup_path):
                try:
                    shutil.copy2(backup_path, file_path)
                    print(f"🔄 Restored from backup: {backup_path}")
                except Exception as restore_error:
                    print(f"❌ Failed to restore from backup: {restore_error}")
            
            return False
    
    def _log_update(self, file_path: str, reason: str, backup_path: Optional[str]):
        """Log update information"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "file_path": file_path,
            "reason": reason,
            "backup_path": backup_path,
            "new_hash": self._calculate_file_hash(file_path)
        }
        
        log_file = os.path.join(self.backups_dir, "update_log.json")
        
        try:
            if os.path.exists(log_file):
                with open(log_file, 'r') as f:
                    log_data = json.load(f)
            else:
                log_data = {"updates": []}
            
            log_data["updates"].append(log_entry)
            
            # Keep only last 100 entries
            if len(log_data["updates"]) > 100:
                log_data["updates"] = log_data["updates"][-100:]
            
            with open(log_file, 'w') as f:
                json.dump(log_data, f, indent=2)
                
        except Exception as e:
            print(f"⚠️ Failed to log update: {e}")
    
    def rollback_file(self, file_path: str, version: Optional[int] = None) -> bool:
        """
        Rollback a file to a previous version
        
        Args:
            file_path: Path to the file to rollback
            version: Specific version to rollback to (latest if None)
        
        Returns:
            bool: True if rollback successful
        """
        
        file_name = os.path.basename(file_path)
        
        if file_name not in self.versions["files"]:
            print(f"❌ No version history found for {file_name}")
            return False
        
        file_versions = self.versions["files"][file_name]
        backups = file_versions["backups"]
        
        if not backups:
            print(f"❌ No backups found for {file_name}")
            return False
        
        # Find the backup to restore
        if version is None:
            # Use the latest backup
            backup_to_restore = backups[-1]
        else:
            # Find specific version
            backup_to_restore = None
            for backup in backups:
                if backup["version"] == version:
                    backup_to_restore = backup
                    break
            
            if not backup_to_restore:
                print(f"❌ Version {version} not found for {file_name}")
                return False
        
        backup_path = backup_to_restore["backup_path"]
        
        if not os.path.exists(backup_path):
            print(f"❌ Backup file not found: {backup_path}")
            return False
        
        try:
            # Create backup of current state before rollback
            if os.path.exists(file_path):
                self.create_backup(file_path, f"before_rollback_to_v{backup_to_restore['version']}")
            
            # Restore the backup
            shutil.copy2(backup_path, file_path)
            
            print(f"✅ Rolled back {file_name} to version {backup_to_restore['version']}")
            
            # Log the rollback
            self._log_update(file_path, f"rollback_to_v{backup_to_restore['version']}", backup_path)
            
            return True
            
        except Exception as e:
            print(f"❌ Rollback failed: {e}")
            return False
    
    def list_versions(self, file_name: Optional[str] = None) -> Dict:
        """
        List version history for a file or all files
        
        Args:
            file_name: Specific file to list versions for (all files if None)
        
        Returns:
            Dict: Version information
        """
        
        if file_name:
            if file_name in self.versions["files"]:
                return {file_name: self.versions["files"][file_name]}
            else:
                return {}
        else:
            return self.versions["files"]
    
    def cleanup_old_backups(self, keep_count: int = 10) -> int:
        """
        Clean up old backups, keeping only the most recent ones
        
        Args:
            keep_count: Number of recent backups to keep per file
        
        Returns:
            int: Number of backups removed
        """
        
        removed_count = 0
        
        for file_name, file_info in self.versions["files"].items():
            backups = file_info["backups"]
            
            if len(backups) > keep_count:
                # Sort by version and keep the most recent
                backups.sort(key=lambda x: x["version"])
                backups_to_remove = backups[:-keep_count]
                
                for backup in backups_to_remove:
                    backup_path = backup["backup_path"]
                    if os.path.exists(backup_path):
                        try:
                            os.remove(backup_path)
                            removed_count += 1
                            print(f"🗑️ Removed old backup: {backup_path}")
                        except Exception as e:
                            print(f"⚠️ Failed to remove backup {backup_path}: {e}")
                
                # Update version tracking
                file_info["backups"] = backups[-keep_count:]
        
        self._save_versions()
        print(f"✅ Cleanup completed. Removed {removed_count} old backups.")
        
        return removed_count
    
    def validate_integrity(self) -> Dict:
        """
        Validate integrity of all tracked files and backups
        
        Returns:
            Dict: Integrity report
        """
        
        report = {
            "valid": True,
            "files_checked": 0,
            "backups_checked": 0,
            "missing_files": [],
            "corrupted_backups": [],
            "hash_mismatches": []
        }
        
        for file_name, file_info in self.versions["files"].items():
            report["files_checked"] += 1
            
            # Check if current file exists
            current_file_path = os.path.join(self.tools_dir, file_name)
            if not os.path.exists(current_file_path):
                report["missing_files"].append(file_name)
                report["valid"] = False
            
            # Check backups
            for backup in file_info["backups"]:
                report["backups_checked"] += 1
                backup_path = backup["backup_path"]
                
                if not os.path.exists(backup_path):
                    report["corrupted_backups"].append({
                        "file": file_name,
                        "version": backup["version"],
                        "backup_path": backup_path,
                        "reason": "file_missing"
                    })
                    report["valid"] = False
                else:
                    # Verify hash
                    actual_hash = self._calculate_file_hash(backup_path)
                    if actual_hash != backup["hash"]:
                        report["hash_mismatches"].append({
                            "file": file_name,
                            "version": backup["version"],
                            "backup_path": backup_path,
                            "expected_hash": backup["hash"],
                            "actual_hash": actual_hash
                        })
                        report["valid"] = False
        
        return report
    
    def create_system_checkpoint(self, checkpoint_name: str) -> bool:
        """
        Create a full system checkpoint of all tools
        
        Args:
            checkpoint_name: Name for the checkpoint
        
        Returns:
            bool: True if checkpoint created successfully
        """
        
        checkpoint_dir = os.path.join(self.backups_dir, f"checkpoint_{checkpoint_name}_{int(time.time())}")
        
        try:
            os.makedirs(checkpoint_dir, exist_ok=True)
            
            # Backup all tool files
            tools_backup_dir = os.path.join(checkpoint_dir, "tools")
            shutil.copytree(self.tools_dir, tools_backup_dir)
            
            # Backup version information
            shutil.copy2(self.version_file, os.path.join(checkpoint_dir, "versions.json"))
            
            # Create checkpoint metadata
            checkpoint_info = {
                "name": checkpoint_name,
                "created_at": datetime.now().isoformat(),
                "tools_count": len([f for f in os.listdir(self.tools_dir) if f.endswith('.py')]),
                "total_size": self._get_directory_size(tools_backup_dir),
                "checkpoint_path": checkpoint_dir
            }
            
            with open(os.path.join(checkpoint_dir, "checkpoint_info.json"), 'w') as f:
                json.dump(checkpoint_info, f, indent=2)
            
            print(f"✅ System checkpoint created: {checkpoint_dir}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to create system checkpoint: {e}")
            return False
    
    def _get_directory_size(self, directory: str) -> int:
        """Get total size of a directory"""
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                total_size += os.path.getsize(filepath)
        return total_size
    
    def restore_system_checkpoint(self, checkpoint_path: str) -> bool:
        """
        Restore system from a checkpoint
        
        Args:
            checkpoint_path: Path to the checkpoint directory
        
        Returns:
            bool: True if restore successful
        """
        
        if not os.path.exists(checkpoint_path):
            print(f"❌ Checkpoint not found: {checkpoint_path}")
            return False
        
        try:
            # Create backup of current state
            current_backup = self.create_system_checkpoint("before_restore")
            if not current_backup:
                print("⚠️ Failed to backup current state, proceeding anyway...")
            
            # Restore tools
            tools_backup_path = os.path.join(checkpoint_path, "tools")
            if os.path.exists(tools_backup_path):
                # Remove current tools directory
                if os.path.exists(self.tools_dir):
                    shutil.rmtree(self.tools_dir)
                
                # Restore from checkpoint
                shutil.copytree(tools_backup_path, self.tools_dir)
            
            # Restore version information
            checkpoint_versions = os.path.join(checkpoint_path, "versions.json")
            if os.path.exists(checkpoint_versions):
                shutil.copy2(checkpoint_versions, self.version_file)
                self.versions = self._load_versions()
            
            print(f"✅ System restored from checkpoint: {checkpoint_path}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to restore system checkpoint: {e}")
            return False
