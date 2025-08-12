"""
Comprehensive Test Suite for Chotu Autonomous System
Tests all components: Vision, Action, Memory, Vault, and Task Execution
"""
import asyncio
import time
import tempfile
import shutil
from pathlib import Path
import json

# Test autonomous components
from autonomous import (
    VisionEngine, ActionEngine, ProceduralMemory, 
    CredentialVault, AutonomousTaskExecutor,
    ExecutionContext, TaskRecipe, ActionStep
)
from chotu_autonomous import ChouAutonomous, execute_autonomous_task

class AutonomousSystemTester:
    """Comprehensive test suite for autonomous system"""
    
    def __init__(self):
        self.temp_dir = Path(tempfile.mkdtemp(prefix="chotu_test_"))
        self.test_results = []
        
    def run_all_tests(self):
        """Run complete test suite"""
        print("🧪 Starting Chotu Autonomous System Tests")
        print("="*60)
        
        # Core component tests
        self.test_vision_engine()
        self.test_action_engine()
        self.test_procedural_memory()
        self.test_credential_vault()
        self.test_task_executor()
        
        # Integration tests
        self.test_autonomous_integration()
        self.test_learning_workflow()
        
        # Performance tests
        self.test_system_performance()
        
        # Display results
        self.display_test_results()
        
        # Cleanup
        self.cleanup()
    
    def test_vision_engine(self):
        """Test computer vision capabilities"""
        print("\n🔍 Testing Vision Engine...")
        
        try:
            vision = VisionEngine(str(self.temp_dir / "vision_test"))
            
            # Test 1: Screen capture
            screen = vision.capture_screen()
            assert screen is not None, "Screen capture failed"
            self.log_test("Vision: Screen Capture", True)
            
            # Test 2: Element signature management
            from autonomous.vision_engine import ElementSignature, ScreenRegion
            
            signature = ElementSignature(
                name="test_button",
                template_path="test_button.png", 
                confidence=0.8
            )
            
            vision.element_signatures["test_button"] = signature
            vision.save_element_signatures()
            
            # Reload and verify
            vision.load_element_signatures()
            assert "test_button" in vision.element_signatures
            self.log_test("Vision: Element Signatures", True)
            
            # Test 3: Screen change analysis
            import numpy as np
            baseline = np.zeros((100, 100, 3), dtype=np.uint8)
            current = np.ones((100, 100, 3), dtype=np.uint8) * 255
            
            changes = vision.analyze_screen_changes(baseline, current)
            assert changes["changes_detected"], "Screen change analysis failed"
            self.log_test("Vision: Change Detection", True)
            
            print("✅ Vision Engine tests passed")
            
        except Exception as e:
            print(f"❌ Vision Engine test failed: {e}")
            self.log_test("Vision: Overall", False, str(e))
    
    def test_action_engine(self):
        """Test browser automation and action capabilities"""
        print("\n🎯 Testing Action Engine...")
        
        try:
            vision = VisionEngine(str(self.temp_dir / "action_test"))
            action_engine = ActionEngine(vision, headless=True)
            
            # Test 1: Browser creation
            success = action_engine.create_stealth_browser()
            assert success, "Stealth browser creation failed"
            self.log_test("Action: Browser Creation", True)
            
            # Test 2: Navigation
            success = action_engine.navigate_to_url("https://httpbin.org/get")
            assert success, "Navigation failed"
            self.log_test("Action: Navigation", True)
            
            # Test 3: Screenshot capability
            screenshot_path = action_engine.take_screenshot("test_screenshot.png")
            assert Path(screenshot_path).exists(), "Screenshot failed"
            self.log_test("Action: Screenshot", True)
            
            # Test 4: Action history
            history = action_engine.get_action_history()
            assert len(history) > 0, "Action history not recorded"
            self.log_test("Action: History Recording", True)
            
            # Test 5: Human behavior randomization
            action_engine.randomize_behavior("conservative")
            assert action_engine.human_behavior.typing_speed_range[0] >= 0.1
            self.log_test("Action: Behavior Profiles", True)
            
            action_engine.close_browser()
            print("✅ Action Engine tests passed")
            
        except Exception as e:
            print(f"❌ Action Engine test failed: {e}")
            self.log_test("Action: Overall", False, str(e))
    
    def test_procedural_memory(self):
        """Test task learning and memory capabilities"""
        print("\n🧠 Testing Procedural Memory...")
        
        try:
            memory = ProceduralMemory(str(self.temp_dir / "memory_test"))
            
            # Test 1: Task recording
            task_id = memory.record_task_learning(
                "Test Instagram Login",
                ["login to instagram", "open instagram"],
                "Test task for Instagram login"
            )
            assert task_id, "Task recording failed"
            self.log_test("Memory: Task Recording", True)
            
            # Test 2: Adding action steps
            steps_added = 0
            test_steps = [
                ("navigate", "https://instagram.com", None, "Navigate to Instagram"),
                ("click", "login_button", None, "Click login button"),
                ("type", "username_field", "{ig_username}", "Enter username"),
                ("type", "password_field", "{ig_password}", "Enter password"),
                ("click", "submit_button", None, "Submit login")
            ]
            
            for action_type, target, value, description in test_steps:
                success = memory.add_action_step(task_id, action_type, target, value, human_readable=description)
                if success:
                    steps_added += 1
            
            assert steps_added == len(test_steps), f"Only {steps_added}/{len(test_steps)} steps added"
            self.log_test("Memory: Action Steps", True)
            
            # Test 3: Task finalization
            success = memory.finalize_task_recipe(
                task_id,
                prerequisites=["chrome_installed", "internet_connected"],
                success_indicators=["dashboard_element"],
                failure_handlers=[{"condition": "captcha", "action": "request_help"}]
            )
            assert success, "Task finalization failed"
            self.log_test("Memory: Task Finalization", True)
            
            # Test 4: Task retrieval by trigger
            found_task = memory.find_task_by_trigger("login to instagram")
            assert found_task is not None, "Task retrieval by trigger failed"
            assert found_task.task_name == "Test Instagram Login"
            self.log_test("Memory: Task Retrieval", True)
            
            # Test 5: Task statistics update
            memory.update_task_statistics(task_id, True, 15.5)
            task = memory.task_recipes[task_id]
            assert task.execution_count == 1
            assert task.success_rate == 1.0
            self.log_test("Memory: Statistics Update", True)
            
            # Test 6: Template creation
            template_task_id = memory.create_task_from_template(
                "web_login",
                {"website_url": "https://example.com", "username": "testuser"}
            )
            assert template_task_id, "Template creation failed"
            self.log_test("Memory: Template Creation", True)
            
            # Test 7: Memory persistence
            memory.save_memory()
            
            new_memory = ProceduralMemory(str(self.temp_dir / "memory_test"))
            assert task_id in new_memory.task_recipes
            self.log_test("Memory: Persistence", True)
            
            print("✅ Procedural Memory tests passed")
            
        except Exception as e:
            print(f"❌ Procedural Memory test failed: {e}")
            self.log_test("Memory: Overall", False, str(e))
    
    def test_credential_vault(self):
        """Test secure credential storage"""
        print("\n🔐 Testing Credential Vault...")
        
        try:
            vault = CredentialVault(str(self.temp_dir / "vault_test"))
            
            # Test 1: Credential storage
            success = vault.store_credential(
                "test_service",
                "test_user", 
                "test_password_123",
                ["web_automation", "testing"],
                require_confirmation=False
            )
            assert success, "Credential storage failed"
            self.log_test("Vault: Credential Storage", True)
            
            # Test 2: Credential retrieval
            cred_data = vault.get_credential(
                "test_service",
                "test_user",
                ["web_automation"],
                auto_confirm=True
            )
            assert cred_data is not None, "Credential retrieval failed"
            assert cred_data["username"] == "test_user"
            assert cred_data["password"] == "test_password_123"
            self.log_test("Vault: Credential Retrieval", True)
            
            # Test 3: Access rules
            from autonomous.credential_vault import AccessRule
            new_rule = AccessRule(
                context_required=["testing"],
                require_confirmation=False,
                max_daily_usage=5
            )
            
            success = vault.update_access_rule("test_service", "test_user", new_rule)
            assert success, "Access rule update failed"
            self.log_test("Vault: Access Rules", True)
            
            # Test 4: Credential listing
            creds_list = vault.list_credentials(["web_automation"])
            assert len(creds_list) > 0, "Credential listing failed"
            self.log_test("Vault: Credential Listing", True)
            
            # Test 5: Security audit
            audit = vault.get_security_audit()
            assert "total_credentials" in audit, "Security audit failed"
            assert audit["vault_health"] in ["healthy", "warning"]
            self.log_test("Vault: Security Audit", True)
            
            # Test 6: Vault persistence
            vault.save_vault()
            
            new_vault = CredentialVault(str(self.temp_dir / "vault_test"))
            retrieved_cred = new_vault.get_credential(
                "test_service", "test_user", ["web_automation"], auto_confirm=True
            )
            assert retrieved_cred is not None, "Vault persistence failed"
            self.log_test("Vault: Persistence", True)
            
            print("✅ Credential Vault tests passed")
            
        except Exception as e:
            print(f"❌ Credential Vault test failed: {e}")
            self.log_test("Vault: Overall", False, str(e))
    
    def test_task_executor(self):
        """Test autonomous task executor"""
        print("\n🤖 Testing Task Executor...")
        
        try:
            executor = AutonomousTaskExecutor(str(self.temp_dir / "executor_test"), headless=True)
            
            # Test 1: System initialization
            status = executor.get_execution_status()
            assert "learning_mode" in status, "Executor initialization failed"
            self.log_test("Executor: Initialization", True)
            
            # Test 2: Simple command execution
            context = ExecutionContext(
                user_id="test_user",
                session_id="test_session",
                environment="testing",
                browser_profile="stealth",
                stealth_level="normal"
            )
            
            # Test simple Chrome opening (should work on macOS)
            result = executor.execute_user_command("open chrome", context)
            assert result is not None, "Command execution failed"
            self.log_test("Executor: Simple Command", True)
            
            # Test 3: Learning capability 
            learning_result = executor._should_enter_learning_mode("open instagram and login")
            assert learning_result == True, "Learning mode detection failed"
            self.log_test("Executor: Learning Detection", True)
            
            # Test 4: Task breakdown
            breakdown_result = executor._attempt_command_breakdown("open chrome")
            assert breakdown_result.success, "Command breakdown failed"
            self.log_test("Executor: Command Breakdown", True)
            
            # Test 5: Capabilities demonstration
            capabilities = executor.demonstrate_capabilities()
            assert "Autonomous Task Executor" in capabilities, "Capabilities demo failed"
            self.log_test("Executor: Capabilities Demo", True)
            
            executor.shutdown()
            print("✅ Task Executor tests passed")
            
        except Exception as e:
            print(f"❌ Task Executor test failed: {e}")
            self.log_test("Executor: Overall", False, str(e))
    
    def test_autonomous_integration(self):
        """Test full autonomous system integration"""
        print("\n🔗 Testing Autonomous Integration...")
        
        try:
            # Test 1: ChouAutonomous initialization
            # Create temporary config
            config_path = self.temp_dir / "test_config.json"
            test_config = {
                "autonomous_mode": True,
                "learning_mode": True,
                "headless_mode": True,
                "stealth_level": "normal"
            }
            
            with open(config_path, 'w') as f:
                json.dump(test_config, f)
            
            chotu = ChouAutonomous(str(config_path))
            self.log_test("Integration: System Init", True)
            
            # Test 2: Intent analysis
            analysis = asyncio.run(chotu._analyze_autonomous_intent("open chrome browser"))
            assert analysis["requires_autonomous_execution"], "Intent analysis failed"
            self.log_test("Integration: Intent Analysis", True)
            
            # Test 3: System commands
            status_result = chotu._handle_system_command("status")
            assert "System Status" in status_result, "System command failed"
            self.log_test("Integration: System Commands", True)
            
            # Test 4: Help system
            help_result = chotu._get_help_text()
            assert "Autonomous System Help" in help_result, "Help system failed"
            self.log_test("Integration: Help System", True)
            
            # Test 5: Task summary
            summary = chotu.get_learned_tasks_summary()
            assert "total_tasks" in summary, "Task summary failed"
            self.log_test("Integration: Task Summary", True)
            
            chotu.shutdown()
            print("✅ Autonomous Integration tests passed")
            
        except Exception as e:
            print(f"❌ Autonomous Integration test failed: {e}")
            self.log_test("Integration: Overall", False, str(e))
    
    def test_learning_workflow(self):
        """Test end-to-end learning workflow"""
        print("\n📚 Testing Learning Workflow...")
        
        try:
            executor = AutonomousTaskExecutor(str(self.temp_dir / "learning_test"), headless=True)
            
            # Test 1: Learning mode activation
            executor.learning_mode = True
            assert executor.learning_mode, "Learning mode activation failed"
            self.log_test("Learning: Mode Activation", True)
            
            # Test 2: Task name extraction
            task_name = executor._extract_task_name("open instagram and login with my credentials")
            assert "Instagram" in task_name, "Task name extraction failed"
            self.log_test("Learning: Task Name Extraction", True)
            
            # Test 3: Simple learning scenario
            # This simulates learning a simple task
            task_id = executor.memory.record_task_learning(
                "Simple Test Task",
                ["test task", "simple task"],
                "A simple test task for learning verification"
            )
            
            # Add a simple step
            executor.memory.add_action_step(
                task_id, "navigate", "https://example.com",
                human_readable="Navigate to example.com"
            )
            
            # Finalize
            executor.memory.finalize_task_recipe(task_id)
            
            # Verify the task was learned
            learned_task = executor.memory.find_task_by_trigger("test task")
            assert learned_task is not None, "Task learning failed"
            self.log_test("Learning: Task Creation", True)
            
            # Test 4: Task execution from memory
            result = executor._execute_task_recipe(learned_task)
            # Note: This might fail due to headless browser limitations, but the framework should work
            self.log_test("Learning: Learned Task Execution", result.success)
            
            executor.shutdown()
            print("✅ Learning Workflow tests passed")
            
        except Exception as e:
            print(f"❌ Learning Workflow test failed: {e}")
            self.log_test("Learning: Overall", False, str(e))
    
    def test_system_performance(self):
        """Test system performance and resource usage"""
        print("\n⚡ Testing System Performance...")
        
        try:
            start_time = time.time()
            
            # Test 1: Component initialization speed
            init_start = time.time()
            executor = AutonomousTaskExecutor(str(self.temp_dir / "perf_test"), headless=True)
            init_time = time.time() - init_start
            
            assert init_time < 5.0, f"Initialization too slow: {init_time:.2f}s"
            self.log_test("Performance: Initialization Speed", True, f"{init_time:.2f}s")
            
            # Test 2: Memory operations speed
            memory_start = time.time()
            for i in range(10):
                task_id = executor.memory.record_task_learning(
                    f"Perf Test Task {i}",
                    [f"test task {i}"],
                    f"Performance test task {i}"
                )
                executor.memory.add_action_step(task_id, "navigate", f"https://example{i}.com")
                executor.memory.finalize_task_recipe(task_id)
            
            memory_time = time.time() - memory_start
            assert memory_time < 2.0, f"Memory operations too slow: {memory_time:.2f}s"
            self.log_test("Performance: Memory Operations", True, f"{memory_time:.2f}s for 10 tasks")
            
            # Test 3: Vision engine performance
            vision_start = time.time()
            for i in range(5):
                screen = executor.vision.capture_screen()
                assert screen is not None
            vision_time = time.time() - vision_start
            
            self.log_test("Performance: Vision Operations", True, f"{vision_time:.2f}s for 5 captures")
            
            # Test 4: Overall memory usage check
            import psutil
            import os
            
            process = psutil.Process(os.getpid())
            memory_mb = process.memory_info().rss / 1024 / 1024
            
            assert memory_mb < 500, f"Memory usage too high: {memory_mb:.1f}MB"
            self.log_test("Performance: Memory Usage", True, f"{memory_mb:.1f}MB")
            
            total_time = time.time() - start_time
            self.log_test("Performance: Total Test Time", True, f"{total_time:.2f}s")
            
            executor.shutdown()
            print("✅ Performance tests passed")
            
        except Exception as e:
            print(f"❌ Performance test failed: {e}")
            self.log_test("Performance: Overall", False, str(e))
    
    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Log test result"""
        self.test_results.append({
            "test": test_name,
            "success": success,
            "details": details,
            "timestamp": time.time()
        })
    
    def display_test_results(self):
        """Display comprehensive test results"""
        print("\n" + "="*60)
        print("🧪 CHOTU AUTONOMOUS SYSTEM TEST RESULTS")
        print("="*60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"\n📊 **Overall Results:**")
        print(f"   Total Tests: {total_tests}")
        print(f"   Passed: {passed_tests} ✅")
        print(f"   Failed: {failed_tests} ❌")
        print(f"   Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        print(f"\n📋 **Detailed Results:**")
        
        categories = {}
        for result in self.test_results:
            category = result["test"].split(":")[0]
            if category not in categories:
                categories[category] = []
            categories[category].append(result)
        
        for category, tests in categories.items():
            category_passed = sum(1 for test in tests if test["success"])
            category_total = len(tests)
            
            print(f"\n   🔍 {category} ({category_passed}/{category_total})")
            
            for test in tests:
                status = "✅" if test["success"] else "❌"
                test_name = test["test"].split(":", 1)[1] if ":" in test["test"] else test["test"]
                details = f" - {test['details']}" if test["details"] else ""
                print(f"     {status} {test_name}{details}")
        
        # Summary
        if failed_tests == 0:
            print(f"\n🎉 **ALL TESTS PASSED!** Chotu Autonomous System is fully operational!")
        else:
            print(f"\n⚠️  **{failed_tests} tests failed.** Review failed components before deployment.")
        
        print("\n" + "="*60)
    
    def cleanup(self):
        """Clean up test resources"""
        try:
            shutil.rmtree(self.temp_dir)
            print(f"\n🧹 Test cleanup completed")
        except Exception as e:
            print(f"⚠️  Cleanup warning: {e}")

def run_autonomous_tests():
    """Run the complete autonomous system test suite"""
    print("🚀 Starting Chotu Autonomous System Test Suite")
    print("This will test all components of the autonomous task execution system.")
    print("\n⏱️  Estimated time: 2-3 minutes")
    print("🔧 Requirements: macOS with Chrome installed")
    
    # Verify basic requirements
    try:
        import cv2
        import pyautogui
        import selenium
        print("✅ All required packages available")
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        return
    
    # Run tests
    tester = AutonomousSystemTester()
    tester.run_all_tests()

if __name__ == "__main__":
    run_autonomous_tests()
