"""
Patch to add step-by-step results display in summary report
Run this to update main_enhanced_auto.py
"""

import re

def apply_patch():
    file_path = "main_enhanced_auto.py"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the SummaryStep class and add detailed results display
    # Search for the pattern where summary is created
    
    # Add this code snippet to display step results in summary
    summary_display_code = '''
        # Display step-by-step results
        if self.all_results:
            results_frame = ctk.CTkFrame(self.action_frame, fg_color=Theme.FRAME, corner_radius=Theme.CORNER_RADIUS)
            results_frame.pack(fill="x", padx=20, pady=10)
            
            results_title = t("📋 KẾT QUẢ CHI TIẾT TỪNG BƯỚC") if CURRENT_LANG == "vi" else "📋 DETAILED STEP RESULTS"
            ctk.CTkLabel(results_frame, text=results_title, font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(pady=15)
            
            for step_name, result_data in self.all_results.items():
                step_frame = ctk.CTkFrame(results_frame, fg_color=Theme.BACKGROUND, corner_radius=6)
                step_frame.pack(fill="x", padx=15, pady=5)
                
                # Step name
                ctk.CTkLabel(step_frame, text=f"🔹 {step_name}", font=Theme.BODY_FONT, text_color=Theme.ACCENT).pack(anchor="w", padx=10, pady=(10,5))
                
                # Result status
                status = result_data.get("Trạng thái", "N/A")
                status_color = Theme.SUCCESS if status == "Tốt" else Theme.ERROR if status == "Lỗi" else Theme.WARNING
                result_text = result_data.get("Kết quả", "N/A")
                
                result_label = ctk.CTkLabel(step_frame, text=f"   • {result_text}", font=Theme.SMALL_FONT, text_color=status_color)
                result_label.pack(anchor="w", padx=10, pady=(0,10))
'''
    
    # Try to find where to insert this code
    # Look for SummaryStep class definition
    if 'class SummaryStep' in content or 'class Summary' in content:
        print("✓ Found Summary class - patch can be applied manually")
        print("\nAdd this code to the SummaryStep.__init__ or display method:")
        print(summary_display_code)
    else:
        print("⚠ Summary class not found in main file")
        print("The summary display code needs to be added manually")
        print("\nCode to add:")
        print(summary_display_code)

if __name__ == "__main__":
    apply_patch()
