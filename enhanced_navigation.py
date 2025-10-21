# -*- coding: utf-8 -*-
"""
Enhanced Navigation System for LaptopTester
Hệ thống điều hướng nâng cao với breadcrumb và quick access
"""

import customtkinter as ctk
import tkinter as tk
from typing import List, Callable, Optional, Dict, Any

# Import theme and utilities
try:
    from laptoptester import Theme, get_text
    from intro_guide_frames import create_home_button
except ImportError:
    # Fallback theme
    class Theme:
        BACKGROUND = "#FAFBFC"
        FRAME = "#FFFFFF"
        ACCENT = "#4299E1"
        SUCCESS = "#38A169"
        WARNING = "#D69E2E"
        ERROR = "#E53E3E"
        TEXT = "#1A202C"
        TEXT_SECONDARY = "#718096"
        HEADING_FONT = ("Segoe UI", 24, "bold")
        SUBHEADING_FONT = ("Segoe UI", 18, "bold")
        BODY_FONT = ("Segoe UI", 14)
        SMALL_FONT = ("Segoe UI", 12)
        CORNER_RADIUS = 12
        BUTTON_HEIGHT = 40
    
    def get_text(key):
        return key
    
    def create_home_button(parent, command, **kwargs):
        return ctk.CTkButton(parent, text="🏠 HOME", command=command, **kwargs)

class BreadcrumbNavigation(ctk.CTkFrame):
    """Breadcrumb navigation component"""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.breadcrumbs: List[Dict[str, Any]] = []
        self.setup_ui()
    
    def setup_ui(self):
        self.grid_columnconfigure(0, weight=1)
        
        # Breadcrumb container
        self.breadcrumb_frame = ctk.CTkFrame(self, fg_color=Theme.FRAME, 
                                           corner_radius=Theme.CORNER_RADIUS,
                                           border_width=1, border_color="#E5E7EB")
        self.breadcrumb_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        
        # Home icon
        self.home_label = ctk.CTkLabel(self.breadcrumb_frame, text="🏠", 
                                      font=("Segoe UI", 16))
        self.home_label.pack(side="left", padx=(15, 5), pady=10)
    
    def add_breadcrumb(self, title: str, callback: Optional[Callable] = None, 
                      icon: str = "", is_current: bool = False):
        """Thêm breadcrumb mới"""
        breadcrumb_data = {
            "title": title,
            "callback": callback,
            "icon": icon,
            "is_current": is_current
        }
        
        if is_current:
            # Mark all others as not current
            for crumb in self.breadcrumbs:
                crumb["is_current"] = False
        
        self.breadcrumbs.append(breadcrumb_data)
        self.refresh_breadcrumbs()
    
    def set_breadcrumbs(self, breadcrumbs: List[Dict[str, Any]]):
        """Đặt toàn bộ breadcrumb path"""
        self.breadcrumbs = breadcrumbs
        self.refresh_breadcrumbs()
    
    def refresh_breadcrumbs(self):
        """Refresh breadcrumb display"""
        # Clear existing breadcrumbs (keep home)
        for widget in self.breadcrumb_frame.winfo_children()[1:]:
            widget.destroy()
        
        for i, crumb in enumerate(self.breadcrumbs):
            # Separator
            if i > 0 or len(self.breadcrumbs) > 0:
                separator = ctk.CTkLabel(self.breadcrumb_frame, text="›", 
                                       font=Theme.BODY_FONT, text_color=Theme.TEXT_SECONDARY)
                separator.pack(side="left", padx=5, pady=10)
            
            # Breadcrumb item
            text = f"{crumb['icon']} {crumb['title']}" if crumb['icon'] else crumb['title']
            
            if crumb['is_current']:
                # Current page - not clickable
                label = ctk.CTkLabel(self.breadcrumb_frame, text=text, 
                                   font=("Segoe UI", 12, "bold"), 
                                   text_color=Theme.ACCENT)
                label.pack(side="left", padx=5, pady=10)
            else:
                # Clickable breadcrumb
                if crumb['callback']:
                    btn = ctk.CTkButton(self.breadcrumb_frame, text=text,
                                      font=Theme.SMALL_FONT, height=25,
                                      fg_color="transparent", 
                                      text_color=Theme.TEXT_SECONDARY,
                                      hover_color="#F3F4F6",
                                      command=crumb['callback'])
                    btn.pack(side="left", padx=2, pady=10)
                else:
                    label = ctk.CTkLabel(self.breadcrumb_frame, text=text,
                                       font=Theme.SMALL_FONT,
                                       text_color=Theme.TEXT_SECONDARY)
                    label.pack(side="left", padx=5, pady=10)

class QuickAccessPanel(ctk.CTkFrame):
    """Quick access panel for common actions"""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=Theme.FRAME, 
                        corner_radius=Theme.CORNER_RADIUS, **kwargs)
        self.actions: List[Dict[str, Any]] = []
        self.setup_ui()
    
    def setup_ui(self):
        # Title
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.pack(fill="x", padx=15, pady=(15, 10))
        
        ctk.CTkLabel(title_frame, text="⚡ Quick Access", 
                    font=Theme.SUBHEADING_FONT, text_color=Theme.ACCENT).pack(anchor="w")
        
        # Actions container
        self.actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.actions_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
    
    def add_action(self, title: str, icon: str, callback: Callable, 
                  color: str = Theme.ACCENT, description: str = ""):
        """Thêm quick action"""
        action_data = {
            "title": title,
            "icon": icon,
            "callback": callback,
            "color": color,
            "description": description
        }
        self.actions.append(action_data)
        self.refresh_actions()
    
    def refresh_actions(self):
        """Refresh actions display"""
        # Clear existing actions
        for widget in self.actions_frame.winfo_children():
            widget.destroy()
        
        for action in self.actions:
            action_btn = ctk.CTkButton(
                self.actions_frame,
                text=f"{action['icon']} {action['title']}",
                font=Theme.BODY_FONT,
                height=Theme.BUTTON_HEIGHT,
                fg_color=action['color'],
                hover_color=self.get_darker_color(action['color']),
                command=action['callback'],
                corner_radius=8
            )
            action_btn.pack(fill="x", pady=3)
            
            if action['description']:
                desc_label = ctk.CTkLabel(
                    self.actions_frame,
                    text=action['description'],
                    font=("Segoe UI", 10),
                    text_color=Theme.TEXT_SECONDARY
                )
                desc_label.pack(anchor="w", padx=10, pady=(0, 5))
    
    def get_darker_color(self, color: str) -> str:
        """Get darker shade for hover effect"""
        color_map = {
            Theme.ACCENT: "#3182CE",
            Theme.SUCCESS: "#2F855A",
            Theme.WARNING: "#B7791F",
            Theme.ERROR: "#C53030"
        }
        return color_map.get(color, "#374151")

class EnhancedNavigationBar(ctk.CTkFrame):
    """Enhanced navigation bar with breadcrumbs and actions"""
    
    def __init__(self, master, home_callback: Callable, **kwargs):
        super().__init__(master, fg_color=Theme.FRAME, height=80, **kwargs)
        self.home_callback = home_callback
        self.pack_propagate(False)
        self.setup_ui()
    
    def setup_ui(self):
        self.grid_columnconfigure(1, weight=1)
        
        # Home button
        self.home_btn = create_home_button(
            self, 
            command=self.home_callback,
            width=100,
            height=35
        )
        self.home_btn.grid(row=0, column=0, padx=20, pady=22, sticky="w")
        
        # Breadcrumb navigation
        self.breadcrumb_nav = BreadcrumbNavigation(self)
        self.breadcrumb_nav.grid(row=0, column=1, sticky="ew", padx=10, pady=22)
        
        # Action buttons container
        self.actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.actions_frame.grid(row=0, column=2, padx=20, pady=22, sticky="e")
    
    def add_breadcrumb(self, title: str, callback: Optional[Callable] = None, 
                      icon: str = "", is_current: bool = False):
        """Add breadcrumb to navigation"""
        self.breadcrumb_nav.add_breadcrumb(title, callback, icon, is_current)
    
    def set_breadcrumbs(self, breadcrumbs: List[Dict[str, Any]]):
        """Set complete breadcrumb path"""
        self.breadcrumb_nav.set_breadcrumbs(breadcrumbs)
    
    def add_action_button(self, text: str, command: Callable, **kwargs):
        """Add action button to navigation bar"""
        default_kwargs = {
            "font": Theme.BODY_FONT,
            "height": 35,
            "corner_radius": 18
        }
        default_kwargs.update(kwargs)
        
        btn = ctk.CTkButton(self.actions_frame, text=text, command=command, **default_kwargs)
        btn.pack(side="right", padx=5)
        return btn

class NavigationManager:
    """Manager class for handling navigation state and history"""
    
    def __init__(self):
        self.history: List[Dict[str, Any]] = []
        self.current_index: int = -1
        self.navigation_bar: Optional[EnhancedNavigationBar] = None
        self.quick_access: Optional[QuickAccessPanel] = None
    
    def set_navigation_bar(self, nav_bar: EnhancedNavigationBar):
        """Set the navigation bar reference"""
        self.navigation_bar = nav_bar
    
    def set_quick_access(self, quick_access: QuickAccessPanel):
        """Set the quick access panel reference"""
        self.quick_access = quick_access
    
    def navigate_to(self, title: str, callback: Callable, icon: str = "", 
                   breadcrumbs: Optional[List[Dict[str, Any]]] = None):
        """Navigate to a new page"""
        page_data = {
            "title": title,
            "callback": callback,
            "icon": icon,
            "breadcrumbs": breadcrumbs or []
        }
        
        # Add to history
        self.current_index += 1
        self.history = self.history[:self.current_index]  # Remove forward history
        self.history.append(page_data)
        
        # Update navigation bar
        if self.navigation_bar:
            if breadcrumbs:
                # Add current page to breadcrumbs
                current_breadcrumbs = breadcrumbs + [{
                    "title": title,
                    "callback": None,
                    "icon": icon,
                    "is_current": True
                }]
                self.navigation_bar.set_breadcrumbs(current_breadcrumbs)
            else:
                self.navigation_bar.add_breadcrumb(title, None, icon, True)
    
    def can_go_back(self) -> bool:
        """Check if can go back in history"""
        return self.current_index > 0
    
    def can_go_forward(self) -> bool:
        """Check if can go forward in history"""
        return self.current_index < len(self.history) - 1
    
    def go_back(self):
        """Go back in navigation history"""
        if self.can_go_back():
            self.current_index -= 1
            current_page = self.history[self.current_index]
            if current_page['callback']:
                current_page['callback']()
    
    def go_forward(self):
        """Go forward in navigation history"""
        if self.can_go_forward():
            self.current_index += 1
            current_page = self.history[self.current_index]
            if current_page['callback']:
                current_page['callback']()
    
    def get_current_page(self) -> Optional[Dict[str, Any]]:
        """Get current page data"""
        if 0 <= self.current_index < len(self.history):
            return self.history[self.current_index]
        return None

class NavigationMixin:
    """Mixin class to add navigation capabilities to frames"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nav_manager = NavigationManager()
    
    def setup_navigation(self, home_callback: Callable):
        """Setup navigation components"""
        # Navigation bar
        self.nav_bar = EnhancedNavigationBar(self, home_callback)
        self.nav_bar.pack(fill="x", padx=20, pady=(20, 10))
        
        # Set navigation manager reference
        self.nav_manager.set_navigation_bar(self.nav_bar)
        
        return self.nav_bar
    
    def setup_quick_access(self, **kwargs):
        """Setup quick access panel"""
        self.quick_access = QuickAccessPanel(self, **kwargs)
        self.nav_manager.set_quick_access(self.quick_access)
        return self.quick_access
    
    def navigate_to(self, title: str, callback: Callable, icon: str = "", 
                   breadcrumbs: Optional[List[Dict[str, Any]]] = None):
        """Navigate to a new page"""
        self.nav_manager.navigate_to(title, callback, icon, breadcrumbs)
    
    def add_quick_action(self, title: str, icon: str, callback: Callable, 
                        color: str = Theme.ACCENT, description: str = ""):
        """Add quick access action"""
        if hasattr(self, 'quick_access') and self.quick_access:
            self.quick_access.add_action(title, icon, callback, color, description)

# Example usage frame
class ExampleNavigationFrame(ctk.CTkFrame, NavigationMixin):
    """Example frame showing navigation usage"""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.setup_example()
    
    def setup_example(self):
        # Setup navigation
        nav_bar = self.setup_navigation(home_callback=self.go_home)
        
        # Add some action buttons to nav bar
        nav_bar.add_action_button("📊 Reports", self.show_reports, fg_color=Theme.SUCCESS)
        nav_bar.add_action_button("⚙️ Settings", self.show_settings, fg_color=Theme.WARNING)
        
        # Main content area
        content_frame = ctk.CTkFrame(self, fg_color=Theme.BACKGROUND)
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        content_frame.grid_columnconfigure(1, weight=1)
        
        # Quick access panel
        quick_access = self.setup_quick_access(width=200)
        quick_access.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=0)
        
        # Add quick actions
        self.add_quick_action("🚀 Start Test", "🚀", self.start_test, Theme.SUCCESS, "Begin comprehensive test")
        self.add_quick_action("📋 View Results", "📋", self.view_results, Theme.ACCENT, "Check test results")
        self.add_quick_action("🔧 Individual Tests", "🔧", self.individual_tests, Theme.WARNING, "Run specific tests")
        self.add_quick_action("📖 Help", "📖", self.show_help, "#6B7280", "Get help and guides")
        
        # Main content
        main_content = ctk.CTkFrame(content_frame, fg_color=Theme.FRAME)
        main_content.grid(row=0, column=1, sticky="nsew", pady=0)
        
        ctk.CTkLabel(main_content, text="🏠 Main Dashboard", 
                    font=Theme.HEADING_FONT, text_color=Theme.ACCENT).pack(pady=50)
        
        # Example navigation buttons
        btn_frame = ctk.CTkFrame(main_content, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        ctk.CTkButton(btn_frame, text="Go to Tests", 
                     command=self.go_to_tests).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Go to Settings", 
                     command=self.go_to_settings).pack(side="left", padx=10)
    
    def go_home(self):
        print("Going home...")
    
    def show_reports(self):
        print("Showing reports...")
    
    def show_settings(self):
        print("Showing settings...")
    
    def start_test(self):
        print("Starting test...")
    
    def view_results(self):
        print("Viewing results...")
    
    def individual_tests(self):
        print("Individual tests...")
    
    def show_help(self):
        print("Showing help...")
    
    def go_to_tests(self):
        # Example navigation with breadcrumbs
        breadcrumbs = [
            {"title": "Dashboard", "callback": self.go_home, "icon": "🏠", "is_current": False}
        ]
        self.navigate_to("Tests", self.show_tests_page, "🧪", breadcrumbs)
    
    def go_to_settings(self):
        breadcrumbs = [
            {"title": "Dashboard", "callback": self.go_home, "icon": "🏠", "is_current": False}
        ]
        self.navigate_to("Settings", self.show_settings_page, "⚙️", breadcrumbs)
    
    def show_tests_page(self):
        print("Showing tests page...")
    
    def show_settings_page(self):
        print("Showing settings page...")

if __name__ == "__main__":
    # Test the navigation system
    app = ctk.CTk()
    app.title("Navigation System Test")
    app.geometry("1200x800")
    
    frame = ExampleNavigationFrame(app)
    frame.pack(fill="both", expand=True)
    
    app.mainloop()