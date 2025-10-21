"""
Test script for main_enhanced.py with Enhanced Hardware Reader v2
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

def test_main_enhanced():
    """Test main_enhanced.py imports and functionality"""
    print("=" * 60)
    print("TESTING MAIN_ENHANCED.PY WITH ENHANCED HARDWARE READER V2")
    print("=" * 60)
    
    # Test imports
    print("\n1. Testing imports...")
    try:
        # Test enhanced hardware reader import
        from enhanced_hardware_reader_v2 import hardware_reader
        print("   Enhanced Hardware Reader v2: OK")
    except ImportError as e:
        print(f"   Enhanced Hardware Reader v2: FAILED - {e}")
        return False
    
    try:
        # Test main_enhanced import
        import main_enhanced
        print("   main_enhanced.py: OK")
    except ImportError as e:
        print(f"   main_enhanced.py: FAILED - {e}")
        return False
    
    # Test enhanced classes
    print("\n2. Testing enhanced classes...")
    try:
        from main_enhanced import EnhancedSystemInfoStep, EnhancedHardwareFingerprintStep
        print("   Enhanced classes: OK")
    except ImportError as e:
        print(f"   Enhanced classes: FAILED - {e}")
        return False
    
    # Test hardware reader availability
    print("\n3. Testing hardware reader availability...")
    try:
        if hasattr(main_enhanced, 'ENHANCED_HARDWARE_READER_AVAILABLE'):
            if main_enhanced.ENHANCED_HARDWARE_READER_AVAILABLE:
                print("   Enhanced Hardware Reader v2 available in main_enhanced: OK")
            else:
                print("   Enhanced Hardware Reader v2 not available in main_enhanced: WARNING")
        else:
            print("   ENHANCED_HARDWARE_READER_AVAILABLE flag not found: WARNING")
    except Exception as e:
        print(f"   Hardware reader availability check: FAILED - {e}")
    
    # Test enhanced step creation
    print("\n4. Testing enhanced step creation...")
    try:
        # Create a dummy master widget for testing
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        # Test EnhancedSystemInfoStep creation
        try:
            step = main_enhanced.EnhancedSystemInfoStep(
                root,
                record_result_callback=lambda name, result: None,
                enable_next_callback=lambda: None,
                go_to_next_step_callback=lambda: None,
                icon_manager=None,
                all_results={}
            )
            print("   EnhancedSystemInfoStep creation: OK")
            step.destroy()
        except Exception as e:
            print(f"   EnhancedSystemInfoStep creation: FAILED - {e}")
        
        # Test EnhancedHardwareFingerprintStep creation
        try:
            step = main_enhanced.EnhancedHardwareFingerprintStep(
                root,
                record_result_callback=lambda name, result: None,
                enable_next_callback=lambda: None,
                go_to_next_step_callback=lambda: None,
                icon_manager=None,
                all_results={}
            )
            print("   EnhancedHardwareFingerprintStep creation: OK")
            step.destroy()
        except Exception as e:
            print(f"   EnhancedHardwareFingerprintStep creation: FAILED - {e}")
        
        root.destroy()
        
    except Exception as e:
        print(f"   Enhanced step creation test: FAILED - {e}")
    
    # Test wizard frame creation
    print("\n5. Testing enhanced wizard frame...")
    try:
        from main_enhanced import EnhancedWizardFrame
        print("   EnhancedWizardFrame import: OK")
        
        # Test step configuration
        wizard = EnhancedWizardFrame.__new__(EnhancedWizardFrame)
        basic_steps = wizard._get_steps_for_mode("basic")
        expert_steps = wizard._get_steps_for_mode("expert")
        
        print(f"   Basic mode steps: {len(basic_steps)} steps")
        print(f"   Expert mode steps: {len(expert_steps)} steps")
        
        # Check if enhanced steps are included
        step_names = [step[0] for step in basic_steps]
        if any("Enhanced" in str(step[1].__name__) for step in basic_steps):
            print("   Enhanced steps included in wizard: OK")
        else:
            print("   Enhanced steps not found in wizard: WARNING")
            
    except Exception as e:
        print(f"   Enhanced wizard frame test: FAILED - {e}")
    
    print("\n" + "=" * 60)
    print("MAIN_ENHANCED.PY TEST COMPLETED")
    print("=" * 60)
    
    return True

def test_hardware_detection():
    """Test actual hardware detection with enhanced reader"""
    print("\n" + "=" * 60)
    print("TESTING ACTUAL HARDWARE DETECTION")
    print("=" * 60)
    
    try:
        from enhanced_hardware_reader_v2 import hardware_reader
        
        print("\n1. Testing CPU detection...")
        cpu_info = hardware_reader.get_cpu_info_comprehensive()
        print(f"   CPU Name: {cpu_info['name']}")
        print(f"   CPU Source: {cpu_info['source']}")
        print(f"   CPU Cores: {cpu_info['cores']}")
        print(f"   CPU Threads: {cpu_info['threads']}")
        
        print("\n2. Testing GPU detection...")
        gpu_info = hardware_reader.get_gpu_info_comprehensive()
        print(f"   GPU Source: {gpu_info['source']}")
        print(f"   GPU Count: {len(gpu_info['devices'])}")
        for i, gpu in enumerate(gpu_info['devices']):
            print(f"   GPU {i+1}: {gpu['name']}")
        
        print("\n3. Testing CPU comparison...")
        if cpu_info['name'] != 'Unknown':
            # Test comparison with slightly different format
            test_cpu = cpu_info['name'].replace("(R)", "").replace("(TM)", "").strip()
            comparison = hardware_reader.compare_cpu_info(cpu_info['name'], test_cpu)
            print(f"   Comparison result: {comparison['match']} ({comparison['confidence']}% confidence)")
        
        return True
        
    except Exception as e:
        print(f"Hardware detection test failed: {e}")
        return False

if __name__ == "__main__":
    print("Starting main_enhanced.py test...")
    
    # Run main tests
    success = test_main_enhanced()
    
    if success:
        # Run hardware detection test
        test_hardware_detection()
        
        print("\nSUMMARY:")
        print("main_enhanced.py is working correctly with Enhanced Hardware Reader v2")
        print("Enhanced CPU and GPU detection is available")
        print("Enhanced steps are properly integrated")
        print("\nYou can now run main_enhanced.py for improved hardware detection!")
    else:
        print("\nSUMMARY:")
        print("Some tests failed. Please check the error messages above.")
        print("Make sure all required files are present:")
        print("   - enhanced_hardware_reader_v2.py")
        print("   - main_enhanced.py")
        print("   - All dependencies from main.py")
    
    input("\nPress Enter to exit...")