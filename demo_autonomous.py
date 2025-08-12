"""
Chotu Autonomous System Demo
Demonstrates computer vision, stealth automation, and procedural learning
"""
import asyncio
import time
from chotu_autonomous import ChouAutonomous

async def main():
    """Main demo function"""
    print("🤖 Welcome to Chotu Autonomous System Demo!")
    print("="*60)
    
    # Initialize system
    print("🔧 Initializing autonomous system...")
    chotu = ChouAutonomous()
    
    # Show system capabilities
    print("\n" + await chotu.process_user_input("capabilities"))
    
    print("\n" + "="*60)
    print("🎮 Interactive Demo Mode")
    print("Type commands or 'quit' to exit")
    print("Examples: 'open chrome', 'status', 'help'")
    print("="*60)
    
    # Interactive loop
    while True:
        try:
            user_input = input("\n> ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                break
            
            if not user_input:
                continue
            
            # Process command
            start_time = time.time()
            response = await chotu.process_user_input(user_input)
            duration = time.time() - start_time
            
            print(f"\n{response}")
            print(f"\n⏱️ Processed in {duration:.2f} seconds")
            
        except KeyboardInterrupt:
            print("\n\n👋 Demo interrupted by user")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
    
    # Shutdown
    print("\n🔧 Shutting down autonomous system...")
    chotu.shutdown()
    print("👋 Demo completed. Thank you!")

if __name__ == "__main__":
    asyncio.run(main())
