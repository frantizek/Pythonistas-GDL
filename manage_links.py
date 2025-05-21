#!/usr/bin/env python3
"""
Pythonistas GDL Linktr.ee Page Manager

This script helps manage your Linktr.ee style page by providing functions to:
- Add new links
- Update existing links
- Reorder links
- Disable/enable links
- Generate the HTML file

Usage:
    python linktr_manager.py
"""

import json
import os
import re
from datetime import datetime
from typing import Dict, List, Optional, Union

# Base configuration
CONFIG = {
    "title": "print(\"Hola Pythonistas GDL!\")",
    "description": "Comunidad de desarrolladores Python en Guadalajara. Comparte conocimiento, haz networking y crece profesionalmente.",
    "logo_text": "Pythonistas GDL",
    "footer": "© {} Pythonistas GDL - Comunidad de Python en Guadalajara".format(datetime.now().year),
    "theme": {
        "bg_color": "#FFE566",
        "primary_color": "#D83B3B",
        "secondary_color": "#4391C1",
        "tertiary_color": "#4D9457",
        "highlight_color": "#EFCA2F",
        "text_color": "#000000",
        "logo_bg": "#4D9457"
    },
    "output_file": "index.html"
}

# Default links structure
DEFAULT_LINKS = [
    {
        "title": "Próximo Evento: TBD",
        "url": "https://pythonistas-gdl.org",
        "icon": "📅",
        "style": "primary",
        "badge": "Nuevo",
        "enabled": True,
        "id": "evento"
    },
    {
        "title": "Registrate: pythonistas-gdl.org",
        "url": "https://pythonistas-gdl.org",
        "icon": "🎟️",
        "style": "highlight",
        "badge": None,
        "enabled": True,
        "id": "registro"
    },
    {
        "title": "Poetry: Package Manager por Daniel Delgado",
        "url": "https://pythonistas-gdl.org",
        "icon": "👨‍💻",
        "style": "secondary",
        "badge": None,
        "enabled": True,
        "id": "poetry"
    },
    {
        "title": "Conoce Pythonistas GDL - Únete a la comunidad",
        "url": "https://pythonistas-gdl.org",
        "icon": "🐍",
        "style": "tertiary",
        "badge": None,
        "enabled": True,
        "id": "comunidad"
    },
    {
        "title": "Síguenos en Facebook",
        "url": "https://www.facebook.com/PythonistasGdl/",
        "icon": "📘",
        "style": "default",
        "badge": None,
        "enabled": True,
        "id": "facebook"
    },
    {
        "title": "Instagram",
        "url": "https://www.instagram.com/pythonistas_gdl/",
        "icon": "📷",
        "style": "default",
        "badge": None,
        "enabled": True,
        "id": "instagram"
    },
    {
        "title": "Twitter/X",
        "url": "https://x.com/pythonistas_gdl/",
        "icon": "🐦",
        "style": "default",
        "badge": None,
        "enabled": True,
        "id": "twitter"
    },
    {
        "title": "YouTube",
        "url": "https://www.youtube.com/@PythonistasGDL",
        "icon": "🎬",
        "style": "default",
        "badge": None,
        "enabled": True,
        "id": "youtube"
    },
    {
        "title": "TikTok",
        "url": "https://www.tiktok.com/@pythonistas_gdl",
        "icon": "🎵",
        "style": "default",
        "badge": None,
        "enabled": True,
        "id": "tiktok"
    },
    {
        "title": "LinkedIn",
        "url": "https://www.linkedin.com/groups/13193010/",
        "icon": "💼",
        "style": "default",
        "badge": None,
        "enabled": True,
        "id": "linkedin"
    },
    {
        "title": "Discord",
        "url": "https://discord.gg/HcvW3r2Wfu",
        "icon": "💬",
        "style": "default",
        "badge": None,
        "enabled": True,
        "id": "discord"
    }
]

class LinkTreeManager:
    """Manager for a Linktr.ee style page"""
    
    def __init__(self, config_file="linktree_config.json"):
        self.config_file = config_file
        self.config = CONFIG.copy()
        self.links = []
        self.load_config()
        
    def load_config(self):
        """Load configuration from file if exists, otherwise use default"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.config.update(data.get('config', {}))
                    self.links = data.get('links', DEFAULT_LINKS)
            except Exception as e:
                print(f"Error loading config file: {e}")
                print("Using default configuration instead.")
                self.links = DEFAULT_LINKS
        else:
            print("No config file found. Using default configuration.")
            self.links = DEFAULT_LINKS
    
    def save_config(self):
        """Save current configuration to file"""
        data = {
            'config': self.config,
            'links': self.links
        }
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Configuration saved to {self.config_file}")
    
    def add_link(self, title, url, icon="🔗", style="default", badge=None, enabled=True, id=None):
        """Add a new link to the list"""
        if id is None:
            # Generate an ID from the title
            id = re.sub(r'[^a-z0-9]', '', title.lower())
            
        # Check if ID already exists
        existing_ids = [link['id'] for link in self.links]
        if id in existing_ids:
            id = f"{id}_{len(self.links)}"
            
        new_link = {
            "title": title,
            "url": url,
            "icon": icon,
            "style": style,
            "badge": badge,
            "enabled": enabled,
            "id": id
        }
        
        self.links.append(new_link)
        print(f"Added new link: {title}")
    
    def update_link(self, id, **kwargs):
        """Update an existing link by ID"""
        for i, link in enumerate(self.links):
            if link['id'] == id:
                for key, value in kwargs.items():
                    if key in link:
                        link[key] = value
                print(f"Updated link: {link['title']}")
                return True
        print(f"Link with ID '{id}' not found")
        return False
    
    def disable_link(self, id):
        """Disable a link by ID"""
        return self.update_link(id, enabled=False)
    
    def enable_link(self, id):
        """Enable a link by ID"""
        return self.update_link(id, enabled=True)
    
    def delete_link(self, id):
        """Delete a link by ID"""
        for i, link in enumerate(self.links):
            if link['id'] == id:
                del self.links[i]
                print(f"Deleted link with ID: {id}")
                return True
        print(f"Link with ID '{id}' not found")
        return False
    
    def reorder_links(self, id_list):
        """Reorder links based on a list of IDs"""
        if len(id_list) != len(self.links):
            print("Error: Number of IDs does not match number of links")
            return False
            
        # Check if all IDs exist
        existing_ids = [link['id'] for link in self.links]
        for id in id_list:
            if id not in existing_ids:
                print(f"Error: ID '{id}' not found")
                return False
        
        # Create a new ordered list
        new_links = []
        for id in id_list:
            for link in self.links:
                if link['id'] == id:
                    new_links.append(link)
                    break
        
        self.links = new_links
        print("Links reordered successfully")
        return True
    
    def get_link_ids(self):
        """Return a list of all link IDs with their titles"""
        return [(link['id'], link['title']) for link in self.links]
    
    def update_theme(self, **kwargs):
        """Update theme colors"""
        for key, value in kwargs.items():
            if key in self.config['theme']:
                self.config['theme'][key] = value
        print("Theme updated")
    
    def update_config(self, **kwargs):
        """Update basic configuration"""
        for key, value in kwargs.items():
            if key in self.config and key != 'theme':
                self.config[key] = value
        print("Configuration updated")
    
    def generate_html(self):
        """Generate HTML for the Linktr.ee style page"""
        # HTML template with placeholders
        html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.config['logo_text']}</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Poppins', sans-serif;
        }}
        
        body {{
            background-color: {self.config['theme']['bg_color']};
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 2rem 1rem;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 600px;
            width: 100%;
        }}
        
        .profile {{
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-bottom: 2rem;
        }}
        
        .logo {{
            width: 120px;
            height: 120px;
            border-radius: 50%;
            background-color: {self.config['theme']['bg_color']};
            display: flex;
            justify-content: center;
            align-items: center;
            margin-bottom: 1rem;
            position: relative;
            overflow: hidden;
            border: 3px solid {self.config['theme']['text_color']};
        }}
        
        .logo-text {{
            position: absolute;
            bottom: 0;
            background-color: rgba(0, 0, 0, 0.7);
            color: white;
            width: 100%;
            text-align: center;
            padding: 4px;
            font-size: 12px;
        }}
        
        h1 {{
            font-size: 1.8rem;
            margin-bottom: 0.5rem;
            text-align: center;
            color: {self.config['theme']['text_color']};
        }}
        
        .description {{
            text-align: center;
            margin-bottom: 2rem;
            max-width: 500px;
            color: {self.config['theme']['text_color']};
        }}
        
        .links {{
            display: flex;
            flex-direction: column;
            gap: 1rem;
            width: 100%;
        }}
        
        .link {{
            display: flex;
            align-items: center;
            justify-content: center;
            background-color: white;
            border: 2px solid {self.config['theme']['text_color']};
            border-radius: 25px;
            padding: 12px;
            text-decoration: none;
            color: {self.config['theme']['text_color']};
            font-size: 1.1rem;
            font-weight: 600;
            transition: transform 0.2s, background-color 0.2s, color 0.2s;
            width: 100%;
            box-sizing: border-box;
        }}
        
        .link:hover {{
            transform: scale(1.05);
            box-shadow: 0 5px 10px rgba(0, 0, 0, 0.2);
        }}
        
        .link.primary {{
            background-color: {self.config['theme']['primary_color']};
            border-color: {self.config['theme']['primary_color']};
            color: white;
        }}
        
        .link.primary:hover {{
            background-color: #b93030; /* Darkened primary color for hover */
            border-color: #b93030;
            color: white;
        }}
        
        .link.secondary {{
            background-color: {self.config['theme']['secondary_color']};
            border-color: {self.config['theme']['secondary_color']};
            color: white;
        }}
        
        .link.secondary:hover {{
            background-color: #397ca3; /* Darkened secondary color for hover */
            border-color: #397ca3;
            color: white;
        }}
        
        .link.tertiary {{
            background-color: {self.config['theme']['tertiary_color']};
            border-color: {self.config['theme']['tertiary_color']};
            color: white;
        }}
        
        .link.tertiary:hover {{
            background-color: #407a49; /* Darkened tertiary color for hover */
            border-color: #407a49;
            color: white;
        }}
        
        .link.highlight {{
            background-color: {self.config['theme']['highlight_color']};
            border-color: {self.config['theme']['highlight_color']};
            color: {self.config['theme']['text_color']};
        }}
        
        .link.highlight:hover {{
            background-color: #d6b326; /* Darkened highlight color for hover */
            border-color: #d6b326;
            color: {self.config['theme']['text_color']};
        }}
        
        .link-icon {{
            width: 24px;
            height: 24px;
            margin-right: 10px;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 1rem;
        }}
        
        .footer {{
            margin-top: 3rem;
            text-align: center;
            font-size: 0.8rem;
            opacity: 0.7;
            color: {self.config['theme']['text_color']};
        }}
        
        .snake-decoration {{
            position: absolute;
            top: 10px;
            right: 10px;
            width: 150px;
            height: 150px;
            opacity: 0.1;
            z-index: -1;
        }}
        
        @media (max-width: 600px) {{
            h1 {{
                font-size: 1.5rem;
            }}
            
            .link {{
                font-size: 1rem;
                padding: 10px;
            }}
            
            .snake-decoration {{
                width: 100px;
                height: 100px;
            }}
        }}
        
        .badge {{
            position: absolute;
            top: -8px;
            right: -8px;
            background-color: {self.config['theme']['primary_color']};
            color: white;
            font-size: 0.7rem;
            padding: 4px 8px;
            border-radius: 10px;
            border: 1px solid white;
        }}
    </style>
</head>
<body>
    <!-- Snake decoration -->
    <div class="snake-decoration">
        <!-- SVG of a Python-like snake -->
        <svg width="100%" height="100%" viewBox="0 0 100 100">
            <path d="M50,15 C70,15 80,25 80,40 C80,55 70,65 50,65 C30,65 20,55 20,40 C20,25 30,15 50,15 Z" fill="{self.config['theme']['logo_bg']}" />
            <path d="M35,40 Q50,20 65,40" stroke="black" stroke-width="4" fill="none" />
            <circle cx="35" cy="40" r="5" fill="{self.config['theme']['primary_color']}" />
            <circle cx="65" cy="40" r="5" fill="{self.config['theme']['primary_color']}" />
        </svg>
    </div>
    
    <div class="container">
        <div class="profile">
            <div class="logo">
                <svg width="80" height="80" viewBox="0 0 100 100">
                    <path d="M50,15 C70,15 80,25 80,40 C80,55 70,65 50,65 C30,65 20,55 20,40 C20,25 30,15 50,15 Z" fill="{self.config['theme']['logo_bg']}" />
                    <path d="M35,40 Q50,20 65,40" stroke="black" stroke-width="4" fill="none" />
                    <circle cx="35" cy="40" r="5" fill="{self.config['theme']['primary_color']}" />
                    <circle cx="65" cy="40" r="5" fill="{self.config['theme']['primary_color']}" />
                </svg>
                <div class="logo-text">{self.config['logo_text']}</div>
            </div>
            <h1>{self.config['title']}</h1>
            <p class="description">{self.config['description']}</p>
        </div>
        
        <div class="links">
"""
        
        # Add each enabled link
        for link in self.links:
            if link['enabled']:
                # Add class based on style
                style_class = f" {link['style']}" if link['style'] != "default" else ""
                
                # Add badge if exists
                badge_html = f'<span class="badge">{link["badge"]}</span>' if link['badge'] else ''
                
                html += f"""            <a href="{link['url']}" class="link{style_class}" id="{link['id']}">
                <div class="link-icon">{link['icon']}</div>
                {link['title']}
                {badge_html}
            </a>
            
"""
        
        # Close HTML
        html += f"""        </div>
        
        <div class="footer">
            {self.config['footer']}
        </div>
    </div>
</body>
</html>"""
        
        # Write to file
        with open(self.config['output_file'], 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"HTML generated and saved to {self.config['output_file']}")
        return html

def interactive_menu():
    """Interactive menu for managing the Linktr.ee page"""
    manager = LinkTreeManager()
    
    while True:
        print("\n===== Pythonistas GDL Linktr.ee Manager =====")
        print("1. View all links")
        print("2. Add new link")
        print("3. Update existing link")
        print("4. Reorder links")
        print("5. Enable/disable link")
        print("6. Delete link")
        print("7. Update theme colors")
        print("8. Update basic configuration")
        print("9. Generate HTML")
        print("10. Save configuration")
        print("0. Exit")
        
        try:
            choice = input("\nEnter your choice (0-10): ")
        except EOFError:
            print("\nEOF detected. Exiting...")
            break
        
        if choice == '0':
            break
        
        elif choice == '1':
            print("\n--- Current Links ---")
            for i, (id, title) in enumerate(manager.get_link_ids()):
                # Find the link
                link = next((l for l in manager.links if l['id'] == id), None)
                status = "✅" if link and link['enabled'] else "❌"
                print(f"{i+1}. [{status}] {title} (ID: {id})")
        
        elif choice == '2':
            print("\n--- Add New Link ---")
            try:
                title = input("Enter link title: ")
                if not title:  # Handle empty input
                    print("Title cannot be empty. Returning to menu.")
                    continue
                url = input("Enter URL: ")
                if not url:  # Handle empty input
                    print("URL cannot be empty. Returning to menu.")
                    continue
                icon = input("Enter emoji icon (default 🔗): ") or "🔗"
                
                print("\nSelect style:")
                print("1. Default (white)")
                print("2. Primary (red)")
                print("3. Secondary (blue)")
                print("4. Tertiary (green)")
                print("5. Highlight (yellow)")
                
                style_choice = input("Enter style choice (1-5): ")
                style_map = {
                    '1': 'default',
                    '2': 'primary',
                    '3': 'secondary',
                    '4': 'tertiary',
                    '5': 'highlight'
                }
                style = style_map.get(style_choice, 'default')
                
                badge = input("Enter badge text (leave empty for none): ")
                if badge == "":
                    badge = None
                    
                manager.add_link(title, url, icon, style, badge)
            except EOFError:
                print("\nEOF detected. Returning to menu...")
                continue
        
        elif choice == '3':
            print("\n--- Update Link ---")
            for i, (id, title) in enumerate(manager.get_link_ids()):
                print(f"{i+1}. {title} (ID: {id})")
            
            try:
                idx = int(input("\nEnter the number of the link to update: ")) - 1
                if 0 <= idx < len(manager.links):
                    link_id = manager.links[idx]['id']
                    
                    print("\nEnter new values (leave empty to keep current):")
                    title = input(f"Title [{manager.links[idx]['title']}]: ") or manager.links[idx]['title']
                    url = input(f"URL [{manager.links[idx]['url']}]: ") or manager.links[idx]['url']
                    icon = input(f"Icon [{manager.links[idx]['icon']}]: ") or manager.links[idx]['icon']
                    
                    print("\nSelect style:")
                    print("1. Default (white)")
                    print("2. Primary (red)")
                    print("3. Secondary (blue)")
                    print("4. Tertiary (green)")
                    print("5. Highlight (yellow)")
                    print(f"Current: {manager.links[idx]['style']}")
                    
                    style_choice = input("Enter style choice (1-5, leave empty to keep current): ")
                    style_map = {
                        '1': 'default',
                        '2': 'primary',
                        '3': 'secondary',
                        '4': 'tertiary',
                        '5': 'highlight'
                    }
                    style = style_map.get(style_choice, manager.links[idx]['style'])
                    
                    current_badge = manager.links[idx]['badge'] or "None"
                    badge = input(f"Badge text [{current_badge}]: ")
                    if badge == "":
                        badge = manager.links[idx]['badge']
                    elif badge.lower() == "none":
                        badge = None
                        
                    manager.update_link(link_id, title=title, url=url, icon=icon, style=style, badge=badge)
                else:
                    print("Invalid selection.")
            except (ValueError, EOFError):
                print("Invalid input or EOF detected. Returning to menu...")
                continue
        
        elif choice == '4':
            print("\n--- Reorder Links ---")
            current_ids = []
            for i, (id, title) in enumerate(manager.get_link_ids()):
                print(f"{i+1}. {title} (ID: {id})")
                current_ids.append(id)
            
            print("\nEnter the new order as a comma-separated list of numbers.")
            print("Example: 3,1,2 would move the third item to first, first to second, etc.")
            
            try:
                order_input = input("New order: ")
                new_order = [int(x.strip()) for x in order_input.split(',')]
                
                # Convert to zero-based and validate
                new_order = [x-1 for x in new_order]
                if min(new_order) < 0 or max(new_order) >= len(current_ids):
                    print("Invalid input: numbers must be between 1 and", len(current_ids))
                else:
                    # Create new ID order
                    new_id_order = [current_ids[i] for i in new_order]
                    manager.reorder_links(new_id_order)
            except (ValueError, EOFError):
                print("Invalid input or EOF detected. Returning to menu...")
                continue
        
        elif choice == '5':
            print("\n--- Enable/Disable Link ---")
            for i, (id, title) in enumerate(manager.get_link_ids()):
                # Find the link status
                link = next((l for l in manager.links if l['id'] == id), None)
                status = "Enabled" if link and link['enabled'] else "Disabled"
                print(f"{i+1}. {title} - {status} (ID: {id})")
            
            try:
                idx = int(input("\nEnter the number of the link to toggle: ")) - 1
                if 0 <= idx < len(manager.links):
                    link_id = manager.links[idx]['id']
                    if manager.links[idx]['enabled']:
                        manager.disable_link(link_id)
                    else:
                        manager.enable_link(link_id)
                else:
                    print("Invalid selection.")
            except (ValueError, EOFError):
                print("Invalid input or EOF detected. Returning to menu...")
                continue
        
        elif choice == '6':
            print("\n--- Delete Link ---")
            for i, (id, title) in enumerate(manager.get_link_ids()):
                print(f"{i+1}. {title} (ID: {id})")
            
            try:
                idx = int(input("\nEnter the number of the link to delete: ")) - 1
                if 0 <= idx < len(manager.links):
                    link_id = manager.links[idx]['id']
                    confirm = input(f"Are you sure you want to delete '{manager.links[idx]['title']}'? (y/n): ")
                    if confirm.lower() == 'y':
                        manager.delete_link(link_id)
                else:
                    print("Invalid selection.")
            except (ValueError, EOFError):
                print("Invalid input or EOF detected. Returning to menu...")
                continue
                
        elif choice == '7':
            print("\n--- Update Theme Colors ---")
            print(f"1. Background Color [{manager.config['theme']['bg_color']}]")
            print(f"2. Primary Color [{manager.config['theme']['primary_color']}]")
            print(f"3. Secondary Color [{manager.config['theme']['secondary_color']}]")
            print(f"4. Tertiary Color [{manager.config['theme']['tertiary_color']}]")
            print(f"5. Highlight Color [{manager.config['theme']['highlight_color']}]")
            print(f"6. Text Color [{manager.config['theme']['text_color']}]")
            print(f"7. Logo Background Color [{manager.config['theme']['logo_bg']}]")
            
            try:
                idx = int(input("\nEnter the number of the color to update (1-7): "))
                if 1 <= idx <= 7:
                    color_keys = ['bg_color', 'primary_color', 'secondary_color', 'tertiary_color', 
                                'highlight_color', 'text_color', 'logo_bg']
                    color_key = color_keys[idx-1]
                    
                    new_color = input(f"Enter new {color_key} (hex format, e.g. #FFE566): ")
                    # Simple hex color validation
                    if re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', new_color):
                        manager.update_theme(**{color_key: new_color})
                    else:
                        print("Invalid color format. Please use hex format (e.g. #FFE566)")
                else:
                    print("Invalid selection.")
            except (ValueError, EOFError):
                print("Invalid input or EOF detected. Returning to menu...")
                continue
                
        elif choice == '8':
            print("\n--- Update Basic Configuration ---")
            print(f"1. Title [{manager.config['title']}]")
            print(f"2. Description")
            print(f"3. Logo Text [{manager.config['logo_text']}]")
            print(f"4. Footer")
            print(f"5. Output Filename [{manager.config['output_file']}]")
            
            try:
                idx = int(input("\nEnter the number of the setting to update (1-5): "))
                if 1 <= idx <= 5:
                    config_keys = ['title', 'description', 'logo_text', 'footer', 'output_file']
                    config_key = config_keys[idx-1]
                    
                    if config_key == 'description':
                        print(f"Current description: {manager.config['description']}")
                        new_value = input("Enter new description: ")
                    elif config_key == 'footer':
                        print(f"Current footer: {manager.config['footer']}")
                        new_value = input("Enter new footer: ")
                    else:
                        new_value = input(f"Enter new {config_key}: ")
                        
                    if new_value:
                        manager.update_config(**{config_key: new_value})
                else:
                    print("Invalid selection.")
            except (ValueError, EOFError):
                print("Invalid input or EOF detected. Returning to menu...")
                continue
                
        elif choice == '9':
            print("\n--- Generating HTML ---")
            manager.generate_html()
            print(f"HTML file generated as {manager.config['output_file']}")
            
        elif choice == '10':
            print("\n--- Saving Configuration ---")
            manager.save_config()
        
        else:
            print("Invalid choice. Please try again.")
    
    # Final save prompt
    try:
        save = input("\nSave configuration before exiting? (y/n): ")
        if save.lower() == 'y':
            manager.save_config()
    except EOFError:
        print("\nEOF detected. Saving configuration and exiting...")
        manager.save_config()
    
    print("Thank you for using Pythonistas GDL Linktr.ee Manager!")

if __name__ == "__main__":
    print("Welcome to Pythonistas GDL Linktr.ee Manager!")
    interactive_menu()