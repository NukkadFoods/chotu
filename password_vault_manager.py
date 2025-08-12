#!/usr/bin/env python3
"""
Simple command-line tool to manage passwords in Chotu's vault
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from autonomous.password_manager import PasswordManager

def main():
    pm = PasswordManager()
    
    print("🔐 Chotu Password Vault Manager")
    print("=" * 40)
    
    while True:
        print("\nOptions:")
        print("1. List all stored credentials")
        print("2. Add new credentials")
        print("3. Get credentials for a service")
        print("4. Delete credentials")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            services = pm.list_services()
            if services:
                print("\n📋 Stored credentials:")
                for i, service in enumerate(services, 1):
                    print(f"   {i}. {service}")
            else:
                print("\n📭 No credentials stored yet")
                
        elif choice == "2":
            service = input("Service (e.g., instagram.com): ").strip()
            username = input("Username/Email: ").strip()
            password = input("Password: ").strip()
            
            if service and username and password:
                if pm.save_credentials(service, username, password):
                    print(f"✅ Credentials saved for {service}")
                else:
                    print(f"❌ Failed to save credentials for {service}")
            else:
                print("❌ All fields are required")
                
        elif choice == "3":
            service = input("Service name: ").strip()
            if service:
                creds = pm.get_credentials(service)
                if creds:
                    username, password = creds
                    print(f"✅ Found credentials for {service}:")
                    print(f"   Username: {username}")
                    print(f"   Password: {'*' * len(password)}")
                else:
                    print(f"❌ No credentials found for {service}")
            else:
                print("❌ Service name is required")
                
        elif choice == "4":
            service = input("Service to delete: ").strip()
            if service:
                if pm.delete_credentials(service):
                    print(f"✅ Credentials deleted for {service}")
                else:
                    print(f"❌ No credentials found for {service}")
            else:
                print("❌ Service name is required")
                
        elif choice == "5":
            print("👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
