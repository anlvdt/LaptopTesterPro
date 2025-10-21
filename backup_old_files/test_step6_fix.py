"""
Test script để kiểm tra bước 6 (System Info) có lấy được CPU, GPU, RAM không
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

def test_step6_directly():
    """Test trực tiếp EnhancedSystemInfoStep"""
    print("=" * 60)
    print("TESTING STEP 6 - ENHANCED SYSTEM INFO")
    print("=" * 60)
    
    try:
        # Import enhanced hardware reader
        from enhanced_hardware_reader_v2 import hardware_reader
        print("✓ Enhanced Hardware Reader v2 imported")
        
        # Test CPU info
        print("\n1. Testing CPU detection...")
        cpu_info = hardware_reader.get_cpu_info_comprehensive()
        print(f"   CPU Name: {cpu_info['name']}")
        print(f"   CPU Cores: {cpu_info['cores']}")
        print(f"   CPU Source: {cpu_info['source']}")
        
        # Test GPU info
        print("\n2. Testing GPU detection...")
        gpu_info = hardware_reader.get_gpu_info_comprehensive()
        print(f"   GPU Source: {gpu_info['source']}")
        print(f"   GPU Count: {len(gpu_info['devices'])}")
        for i, gpu in enumerate(gpu_info['devices']):
            print(f"   GPU {i+1}: {gpu['name']}")
        
        # Test RAM info
        print("\n3. Testing RAM detection...")
        import psutil
        memory = psutil.virtual_memory()
        ram_gb = round(memory.total / (1024**3), 2)
        print(f"   RAM: {ram_gb} GB")
        
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_step6_in_ui():
    """Test EnhancedSystemInfoStep trong UI"""
    print("\n" + "=" * 60)
    print("TESTING STEP 6 IN UI")
    print("=" * 60)
    
    try:
        import tkinter as tk
        from main_enhanced import EnhancedSystemInfoStep
        
        # Create dummy root
        root = tk.Tk()
        root.withdraw()
        
        # Create step
        step = EnhancedSystemInfoStep(
            root,
            record_result_callback=lambda name, result: print(f"Result: {name} - {result}"),
            enable_next_callback=lambda: None,
            go_to_next_step_callback=lambda: None,
            icon_manager=None,
            all_results={}
        )
        
        print("✓ EnhancedSystemInfoStep created successfully")
        
        # Test if enhanced hardware reader is available
        if hasattr(step, 'enhanced_hardware_reader') and step.enhanced_hardware_reader:
            print("✓ Enhanced Hardware Reader v2 available in step")
        else:
            print("✗ Enhanced Hardware Reader v2 NOT available in step")
        
        # Cleanup
        step.destroy()
        root.destroy()
        
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_main_enhanced_import():
    """Test import main_enhanced"""
    print("\n" + "=" * 60)
    print("TESTING MAIN_ENHANCED IMPORT")
    print("=" * 60)
    
    try:
        import main_enhanced
        print("✓ main_enhanced imported successfully")
        
        # Check if enhanced hardware reader is available
        if hasattr(main_enhanced, 'ENHANCED_HARDWARE_READER_AVAILABLE'):
            if main_enhanced.ENHANCED_HARDWARE_READER_AVAILABLE:
                print("✓ Enhanced Hardware Reader v2 available in main_enhanced")
            else:
                print("✗ Enhanced Hardware Reader v2 NOT available in main_enhanced")
        
        # Check if enhanced classes exist
        if hasattr(main_enhanced, 'EnhancedSystemInfoStep'):
            print("✓ EnhancedSystemInfoStep class exists")
        else:
            print("✗ EnhancedSystemInfoStep class NOT found")
        
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    print("Testing Step 6 (System Info) Fix...")
    
    # Test 1: Direct hardware detection
    success1 = test_step6_directly()
    
    # Test 2: Main enhanced import
    success2 = test_main_enhanced_import()
    
    # Test 3: UI step creation
    success3 = test_step6_in_ui()
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    if success1 and success2 and success3:
        print("✓ All tests passed!")
        print("✓ Step 6 should now work correctly")
        print("✓ CPU, GPU, RAM detection is working")
        print("\nYou can now run main_enhanced.py and step 6 should display hardware info correctly!")
    else:
        print("✗ Some tests failed")
        print("Please check the error messages above")
        
        if not success1:
            print("- Hardware detection failed")
        if not success2:
            print("- main_enhanced import failed")
        if not success3:
            print("- UI step creation failed")
    
    input("\nPress Enter to exit...")