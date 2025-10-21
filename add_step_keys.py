"""Add step_key to all Step classes"""

import re

# Map step class names to their step_key values
STEP_KEYS = {
    "BIOSCheckStep": "bios_check",
    "CPUStressTestStep": "cpu_stress",
    "GPUStressTestStep": "gpu_stress",
    "BatteryHealthStep": "battery_health",
    "AudioTestStep": "audio_test",
    "WebcamTestStep": "webcam_test",
    "NetworkTestStep": "network_test",
    "ThermalMonitorStep": "thermal_monitor",
    "SystemStabilityStep": "system_stability",
}

# Read the main file
with open("main_enhanced_auto.py", "r", encoding="utf-8") as f:
    content = f.read()

# For each step class, add step_key to __init__
for class_name, step_key in STEP_KEYS.items():
    # Pattern to find: class XxxStep(BaseStepFrame):
    #                      def __init__(self, master, **kwargs):
    #                          super().__init__(...)
    # And insert kwargs["step_key"] = "xxx" before super().__init__()
    
    pattern = rf"(class {class_name}\(BaseStepFrame\):\s+def __init__\(self, master, \*\*kwargs\):)"
    
    if re.search(pattern, content):
        # Find the super().__init__ call after this pattern
        # Insert kwargs["step_key"] = "..." before it
        
        # More robust approach: find the class and insert after def __init__
        class_pattern = rf"class {class_name}\(BaseStepFrame\):\s+def __init__\(self, master, \*\*kwargs\):"
        
        match = re.search(class_pattern, content)
        if match:
            # Find the position right after this line
            end_pos = match.end()
            # Find the next line after def __init__
            next_line_start = content.find("\n", end_pos) + 1
            
            # Check if step_key is already there
            next_lines = content[next_line_start:next_line_start + 100]
            if 'kwargs["step_key"]' not in next_lines:
                # Insert the step_key line
                indent = "        "  # 8 spaces for method body
                insertion = f'{indent}kwargs["step_key"] = "{step_key}"\n'
                
                content = content[:next_line_start] + insertion + content[next_line_start:]
                print(f"✅ Added step_key to {class_name}")
            else:
                print(f"⏭️  {class_name} already has step_key")
        else:
            print(f"❌ Could not find {class_name}")
    else:
        print(f"❌ Pattern not found for {class_name}")

# Write back
with open("main_enhanced_auto.py", "w", encoding="utf-8") as f:
    f.write(content)

print("\n✅ All step_keys added successfully!")
