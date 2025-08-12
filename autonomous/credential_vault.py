"""
Chotu Credential Vault - Secure Storage for Sensitive Data
Implements encrypted credential storage with context-aware access control
"""
import json
import os
import time
import keyring
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import logging
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
import base64
import hashlib

@dataclass
class CredentialEntry:
    """Individual credential entry with metadata"""
    service_name: str
    username: str
    encrypted_password: str
    context: List[str]  # Contexts where this credential can be used
    created_at: str
    last_used: str = ""
    usage_count: int = 0
    encryption_key_id: str = ""
    
@dataclass
class AccessRule:
    """Rules for accessing credentials"""
    context_required: List[str]
    require_confirmation: bool = True
    max_daily_usage: int = 10
    allowed_domains: List[str] = None
    
class CredentialVault:
    """Secure credential storage with context-aware access"""
    
    def __init__(self, vault_dir: str = "autonomous/vault"):
        self.vault_dir = Path(vault_dir)
        self.vault_dir.mkdir(parents=True, exist_ok=True)
        
        self.credentials_file = self.vault_dir / "credentials.json"
        self.access_rules_file = self.vault_dir / "access_rules.json"
        self.access_log_file = self.vault_dir / "access_log.json"
        
        # Configure logging first
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # In-memory storage
        self.credentials: Dict[str, CredentialEntry] = {}
        self.access_rules: Dict[str, AccessRule] = {}
        self.access_log: List[Dict] = []
        
        # Master key for encryption
        self.master_key: Optional[bytes] = None
        self.salt: bytes = b""
        
        # Initialize vault
        self._initialize_vault()
        self.load_vault()
    
    def _initialize_vault(self):
        """Initialize vault with master key"""
        try:
            # Try to get existing master key from keyring
            master_password = keyring.get_password("chotu_vault", "master_key")
            
            if not master_password:
                # Generate new master password
                master_password = base64.urlsafe_b64encode(get_random_bytes(32)).decode()
                keyring.set_password("chotu_vault", "master_key", master_password)
                self.logger.info("New master key created and stored in system keyring")
            
            # Generate salt if not exists
            salt_file = self.vault_dir / "salt.bin"
            if salt_file.exists():
                with open(salt_file, 'rb') as f:
                    self.salt = f.read()
            else:
                self.salt = get_random_bytes(32)
                with open(salt_file, 'wb') as f:
                    f.write(self.salt)
            
            # Derive master key
            self.master_key = PBKDF2(master_password, self.salt, 32)
            
        except Exception as e:
            self.logger.error(f"Failed to initialize vault: {e}")
            raise
    
    def _encrypt_data(self, data: str) -> str:
        """Encrypt sensitive data"""
        try:
            if not self.master_key:
                raise ValueError("Master key not initialized")
            
            # Generate random IV
            iv = get_random_bytes(16)
            
            # Create cipher
            cipher = AES.new(self.master_key, AES.MODE_CBC, iv)
            
            # Pad data to multiple of 16 bytes
            pad_length = 16 - (len(data) % 16)
            padded_data = data + (chr(pad_length) * pad_length)
            
            # Encrypt
            encrypted = cipher.encrypt(padded_data.encode())
            
            # Combine IV and encrypted data
            result = iv + encrypted
            
            return base64.b64encode(result).decode()
            
        except Exception as e:
            self.logger.error(f"Encryption failed: {e}")
            raise
    
    def _decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        try:
            if not self.master_key:
                raise ValueError("Master key not initialized")
            
            # Decode base64
            data = base64.b64decode(encrypted_data.encode())
            
            # Extract IV and encrypted content
            iv = data[:16]
            encrypted = data[16:]
            
            # Create cipher
            cipher = AES.new(self.master_key, AES.MODE_CBC, iv)
            
            # Decrypt
            decrypted = cipher.decrypt(encrypted)
            
            # Remove padding
            pad_length = decrypted[-1]
            unpadded = decrypted[:-pad_length]
            
            return unpadded.decode()
            
        except Exception as e:
            self.logger.error(f"Decryption failed: {e}")
            raise
    
    def store_credential(self, service_name: str, username: str, password: str,
                        context: List[str], require_confirmation: bool = True) -> bool:
        """Store encrypted credential with context"""
        try:
            from datetime import datetime
            
            # Encrypt password
            encrypted_password = self._encrypt_data(password)
            
            # Create credential entry
            credential = CredentialEntry(
                service_name=service_name,
                username=username,
                encrypted_password=encrypted_password,
                context=context,
                created_at=datetime.now().isoformat(),
                encryption_key_id=hashlib.sha256(self.master_key).hexdigest()[:8]
            )
            
            # Create access rule
            access_rule = AccessRule(
                context_required=context,
                require_confirmation=require_confirmation
            )
            
            # Store
            credential_id = f"{service_name}:{username}"
            self.credentials[credential_id] = credential
            self.access_rules[credential_id] = access_rule
            
            # Save to disk
            self.save_vault()
            
            self.logger.info(f"Credential stored for {service_name}:{username}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to store credential: {e}")
            return False
    
    def get_credential(self, service_name: str, username: str, 
                      current_context: List[str],
                      auto_confirm: bool = False) -> Optional[Dict[str, str]]:
        """Retrieve credential with context validation"""
        try:
            credential_id = f"{service_name}:{username}"
            
            if credential_id not in self.credentials:
                self.logger.warning(f"Credential not found: {credential_id}")
                return None
            
            credential = self.credentials[credential_id]
            access_rule = self.access_rules.get(credential_id)
            
            # Validate context
            if not self._validate_access(credential, access_rule, current_context):
                return None
            
            # Check if confirmation required
            if access_rule and access_rule.require_confirmation and not auto_confirm:
                if not self._request_user_confirmation(service_name):
                    self.logger.warning(f"User denied access to {credential_id}")
                    return None
            
            # Decrypt password
            decrypted_password = self._decrypt_data(credential.encrypted_password)
            
            # Log access
            self._log_credential_access(credential_id, current_context, True)
            
            # Update usage statistics
            from datetime import datetime
            credential.last_used = datetime.now().isoformat()
            credential.usage_count += 1
            
            return {
                "username": credential.username,
                "password": decrypted_password,
                "service": service_name
            }
            
        except Exception as e:
            self.logger.error(f"Failed to retrieve credential: {e}")
            self._log_credential_access(f"{service_name}:{username}", current_context, False, str(e))
            return None
    
    def _validate_access(self, credential: CredentialEntry, access_rule: Optional[AccessRule],
                        current_context: List[str]) -> bool:
        """Validate if current context allows access to credential"""
        try:
            # Check context requirements
            if access_rule and access_rule.context_required:
                required_contexts = set(access_rule.context_required)
                current_contexts = set(current_context)
                
                if not required_contexts.intersection(current_contexts):
                    self.logger.warning(f"Context mismatch. Required: {required_contexts}, Current: {current_contexts}")
                    return False
            
            # Check daily usage limits
            if access_rule and access_rule.max_daily_usage > 0:
                today_usage = self._get_daily_usage_count(f"{credential.service_name}:{credential.username}")
                if today_usage >= access_rule.max_daily_usage:
                    self.logger.warning(f"Daily usage limit exceeded for {credential.service_name}")
                    return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Access validation failed: {e}")
            return False
    
    def _request_user_confirmation(self, service_name: str) -> bool:
        """Request user confirmation for credential access"""
        # This would integrate with the main Chotu interface
        # For now, return True for autonomous operation
        # In production, this should show a secure confirmation dialog
        self.logger.info(f"Auto-confirming credential access for {service_name}")
        return True
    
    def _log_credential_access(self, credential_id: str, context: List[str], 
                             success: bool, error_message: str = ""):
        """Log credential access attempt"""
        try:
            from datetime import datetime
            
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "credential_id": credential_id,
                "context": context,
                "success": success,
                "error_message": error_message,
                "ip_address": self._get_current_ip(),  # For security auditing
            }
            
            self.access_log.append(log_entry)
            
            # Keep only last 10000 entries
            if len(self.access_log) > 10000:
                self.access_log = self.access_log[-10000:]
            
        except Exception as e:
            self.logger.error(f"Failed to log access: {e}")
    
    def _get_current_ip(self) -> str:
        """Get current IP address for logging"""
        try:
            import socket
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                return s.getsockname()[0]
        except:
            return "127.0.0.1"
    
    def _get_daily_usage_count(self, credential_id: str) -> int:
        """Get today's usage count for a credential"""
        try:
            from datetime import datetime, date
            
            today = date.today().isoformat()
            count = 0
            
            for log_entry in self.access_log:
                if (log_entry["credential_id"] == credential_id and 
                    log_entry["success"] and
                    log_entry["timestamp"].startswith(today)):
                    count += 1
            
            return count
            
        except Exception as e:
            self.logger.error(f"Failed to get daily usage count: {e}")
            return 0
    
    def list_credentials(self, context_filter: List[str] = None) -> List[Dict[str, Any]]:
        """List available credentials (without passwords)"""
        try:
            credentials_list = []
            
            for credential_id, credential in self.credentials.items():
                # Filter by context if specified
                if context_filter:
                    if not set(context_filter).intersection(set(credential.context)):
                        continue
                
                credentials_list.append({
                    "service_name": credential.service_name,
                    "username": credential.username,
                    "context": credential.context,
                    "created_at": credential.created_at,
                    "last_used": credential.last_used,
                    "usage_count": credential.usage_count
                })
            
            return credentials_list
            
        except Exception as e:
            self.logger.error(f"Failed to list credentials: {e}")
            return []
    
    def update_access_rule(self, service_name: str, username: str, 
                          new_rule: AccessRule) -> bool:
        """Update access rule for a credential"""
        try:
            credential_id = f"{service_name}:{username}"
            
            if credential_id not in self.credentials:
                return False
            
            self.access_rules[credential_id] = new_rule
            self.save_vault()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update access rule: {e}")
            return False
    
    def delete_credential(self, service_name: str, username: str) -> bool:
        """Delete a credential from vault"""
        try:
            credential_id = f"{service_name}:{username}"
            
            if credential_id in self.credentials:
                del self.credentials[credential_id]
            
            if credential_id in self.access_rules:
                del self.access_rules[credential_id]
            
            self.save_vault()
            self.logger.info(f"Credential deleted: {credential_id}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to delete credential: {e}")
            return False
    
    def export_vault_backup(self, backup_password: str) -> Optional[str]:
        """Export encrypted vault backup"""
        try:
            # Create backup data
            backup_data = {
                "credentials": {},
                "access_rules": {},
                "export_timestamp": datetime.now().isoformat()
            }
            
            # Convert credentials to dict format
            for cred_id, credential in self.credentials.items():
                backup_data["credentials"][cred_id] = {
                    "service_name": credential.service_name,
                    "username": credential.username,
                    "encrypted_password": credential.encrypted_password,
                    "context": credential.context,
                    "created_at": credential.created_at,
                    "last_used": credential.last_used,
                    "usage_count": credential.usage_count,
                    "encryption_key_id": credential.encryption_key_id
                }
            
            # Convert access rules to dict format
            for rule_id, rule in self.access_rules.items():
                backup_data["access_rules"][rule_id] = {
                    "context_required": rule.context_required,
                    "require_confirmation": rule.require_confirmation,
                    "max_daily_usage": rule.max_daily_usage,
                    "allowed_domains": rule.allowed_domains
                }
            
            # Encrypt backup with user-provided password
            backup_json = json.dumps(backup_data)
            
            # Use a different encryption for backup
            backup_salt = get_random_bytes(32)
            backup_key = PBKDF2(backup_password, backup_salt, 32)
            
            iv = get_random_bytes(16)
            cipher = AES.new(backup_key, AES.MODE_CBC, iv)
            
            pad_length = 16 - (len(backup_json) % 16)
            padded_data = backup_json + (chr(pad_length) * pad_length)
            
            encrypted_backup = cipher.encrypt(padded_data.encode())
            
            # Combine salt, IV, and encrypted data
            final_backup = backup_salt + iv + encrypted_backup
            backup_b64 = base64.b64encode(final_backup).decode()
            
            # Save to file
            backup_file = self.vault_dir / f"vault_backup_{int(time.time())}.dat"
            with open(backup_file, 'w') as f:
                f.write(backup_b64)
            
            return str(backup_file)
            
        except Exception as e:
            self.logger.error(f"Failed to export vault backup: {e}")
            return None
    
    def get_security_audit(self) -> Dict[str, Any]:
        """Get security audit information"""
        try:
            from datetime import datetime, timedelta
            
            # Recent access attempts
            recent_accesses = [
                log for log in self.access_log
                if datetime.fromisoformat(log["timestamp"]) > datetime.now() - timedelta(days=7)
            ]
            
            # Failed access attempts
            failed_accesses = [log for log in recent_accesses if not log["success"]]
            
            # High usage credentials
            high_usage_creds = [
                cred for cred in self.credentials.values()
                if cred.usage_count > 50
            ]
            
            return {
                "total_credentials": len(self.credentials),
                "recent_accesses": len(recent_accesses),
                "failed_accesses": len(failed_accesses),
                "high_usage_credentials": len(high_usage_creds),
                "vault_health": "healthy" if len(failed_accesses) < 5 else "warning"
            }
            
        except Exception as e:
            self.logger.error(f"Failed to generate security audit: {e}")
            return {}
    
    def save_vault(self):
        """Save vault data to disk"""
        try:
            # Save credentials
            credentials_data = {}
            for cred_id, credential in self.credentials.items():
                credentials_data[cred_id] = {
                    "service_name": credential.service_name,
                    "username": credential.username,
                    "encrypted_password": credential.encrypted_password,
                    "context": credential.context,
                    "created_at": credential.created_at,
                    "last_used": credential.last_used,
                    "usage_count": credential.usage_count,
                    "encryption_key_id": credential.encryption_key_id
                }
            
            with open(self.credentials_file, 'w') as f:
                json.dump(credentials_data, f, indent=2)
            
            # Save access rules
            rules_data = {}
            for rule_id, rule in self.access_rules.items():
                rules_data[rule_id] = {
                    "context_required": rule.context_required,
                    "require_confirmation": rule.require_confirmation,
                    "max_daily_usage": rule.max_daily_usage,
                    "allowed_domains": rule.allowed_domains
                }
            
            with open(self.access_rules_file, 'w') as f:
                json.dump(rules_data, f, indent=2)
            
            # Save access log
            with open(self.access_log_file, 'w') as f:
                json.dump(self.access_log, f, indent=2)
                
        except Exception as e:
            self.logger.error(f"Failed to save vault: {e}")
    
    def load_vault(self):
        """Load vault data from disk"""
        try:
            # Load credentials
            if self.credentials_file.exists():
                with open(self.credentials_file, 'r') as f:
                    credentials_data = json.load(f)
                
                for cred_id, cred_data in credentials_data.items():
                    self.credentials[cred_id] = CredentialEntry(**cred_data)
            
            # Load access rules
            if self.access_rules_file.exists():
                with open(self.access_rules_file, 'r') as f:
                    rules_data = json.load(f)
                
                for rule_id, rule_data in rules_data.items():
                    self.access_rules[rule_id] = AccessRule(**rule_data)
            
            # Load access log
            if self.access_log_file.exists():
                with open(self.access_log_file, 'r') as f:
                    self.access_log = json.load(f)
                    
        except Exception as e:
            self.logger.error(f"Failed to load vault: {e}")
