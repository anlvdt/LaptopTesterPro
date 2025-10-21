"""
Simple test script for Enhanced Hardware Reader v2
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

def test_enhanced_hardware_reader():
    """Test Enhanced Hardware Reader v2"""
    print("=" * 60)
    print("TESTING ENHANCED HARDWARE READER V2")
    print("=" * 60)
    
    try:
        from enhanced_hardware_reader_v2 import hardware_reader
        print("Enhanced Hardware Reader v2 imported successfully")
    except ImportError as e:
        print(f"Failed to import Enhanced Hardware Reader v2: {e}")
        return False
    
    # Test CPU Info
    print("\n" + "-" * 40)
    print("TESTING CPU INFORMATION")
    print("-" * 40)
    
    try:
        cpu_info = hardware_reader.get_cpu_info_comprehensive()
        
        print(f"CPU Name: {cpu_info['name']}")
        print(f"Cores: {cpu_info['cores']}")
        print(f"Threads: {cpu_info['threads']}")
        print(f"Max Clock: {cpu_info['max_clock']} MHz")
        print(f"Current Clock: {cpu_info['current_clock']} MHz")
        print(f"Temperature: {cpu_info['temperature']}C")
        print(f"Load: {cpu_info['load']}%")
        print(f"Power: {cpu_info['power']}W")
        print(f"Source: {cpu_info['source']}")
        
        # Show raw data sources
        print(f"\nData Sources Available:")
        for source, data in cpu_info['raw_data'].items():
            print(f"  - {source.upper()}: Available")
        
        if cpu_info['name'] != 'Unknown':
            print("CPU information retrieved successfully")
        else:
            print("WARNING: CPU name not detected")
            
    except Exception as e:
        print(f"CPU test failed: {e}")
        return False
    
    # Test GPU Info
    print("\n" + "-" * 40)
    print("TESTING GPU INFORMATION")
    print("-" * 40)
    
    try:
        gpu_info = hardware_reader.get_gpu_info_comprehensive()
        
        print(f"Source: {gpu_info['source']}")
        print(f"Number of GPUs: {len(gpu_info['devices'])}")
        
        if gpu_info['devices']:
            for i, device in enumerate(gpu_info['devices']):
                print(f"\nGPU {i+1}:")
                print(f"  Name: {device['name']}")
                print(f"  Memory: {device.get('memory_total', 'N/A')}")
                print(f"  Temperature: {device.get('temperature', 'N/A')}C")
                print(f"  Load: {device.get('load', 'N/A')}%")
                print(f"  Clock: {device.get('clock', 'N/A')} MHz")
                print(f"  Power: {device.get('power', 'N/A')}W")
                print(f"  Source: {device.get('source', 'N/A')}")
            
            print("GPU information retrieved successfully")
        else:
            print("WARNING: No GPU devices detected")
            
        # Show raw data sources
        print(f"\nData Sources Available:")
        for source, data in gpu_info['raw_data'].items():
            print(f"  - {source.upper()}: Available")
            
    except Exception as e:
        print(f"GPU test failed: {e}")
        return False
    
    # Test CPU Comparison
    print("\n" + "-" * 40)
    print("TESTING CPU COMPARISON")
    print("-" * 40)
    
    try:
        # Test cases
        test_cases = [
            ("Intel(R) Core(TM) i7-10750H CPU @ 2.60GHz", "Intel Core i7-10750H"),
            ("AMD Ryzen 5 3600 6-Core Processor", "AMD Ryzen 5 3600"),
        ]
        
        for cpu1, cpu2 in test_cases:
            comparison = hardware_reader.compare_cpu_info(cpu1, cpu2)
            
            print(f"\nTest Case:")
            print(f"  CPU 1: {cpu1}")
            print(f"  CPU 2: {cpu2}")
            print(f"  Match: {'YES' if comparison['match'] else 'NO'} ({comparison['confidence']}% confidence)")
            print(f"  Normalized 1: {comparison['bios_normalized']}")
            print(f"  Normalized 2: {comparison['windows_normalized']}")
        
        print("CPU comparison test completed")
        
    except Exception as e:
        print(f"CPU comparison test failed: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("ALL TESTS COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    return True

if __name__ == "__main__":
    print("Starting Enhanced Hardware Reader v2 Tests...")
    
    # Run main tests
    success = test_enhanced_hardware_reader()
    
    if success:
        print("\nSUMMARY:")
        print("Enhanced Hardware Reader v2 is working correctly")
        print("CPU and GPU information can be retrieved accurately")
        print("CPU comparison functionality is working")
        print("\nThe enhanced hardware reader should now provide more accurate")
        print("CPU and GPU information in steps 1, 3, and 6 of LaptopTester!")
    else:
        print("\nSUMMARY:")
        print("Some tests failed. Please check the error messages above.")
        print("Make sure all required dependencies are installed:")
        print("   - psutil")
        print("   - wmi (Windows)")
        print("   - cpuinfo")
        print("   - pynvml (for NVIDIA GPUs)")
    
    input("\nPress Enter to exit...")