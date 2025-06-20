#!/usr/bin/env python3
"""
Script to make all REEP presentation slides responsive
Converts fixed pixel dimensions to viewport-relative units
"""

import re
import glob
import os

def make_responsive(file_path):
    """Convert a slide file to be responsive"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Update main slide container
    content = re.sub(
        r'\.slide\s*{[^}]*width:\s*1920px;[^}]*height:\s*1080px;[^}]*}',
        lambda m: m.group(0)
            .replace('width: 1920px;', 'width: 100vw; max-width: 1920px;')
            .replace('height: 1080px;', 'height: 100vh; max-height: 1080px;')
            .replace('margin: 40px auto;', 'margin: 0 auto;')
            .replace('padding: 50px;', 'padding: clamp(20px, 3vw, 50px);')
            .replace('padding: 45px;', 'padding: clamp(20px, 3vw, 45px);')
            .replace('padding: 60px;', 'padding: clamp(20px, 3vw, 60px);')
            + '\n            aspect-ratio: 16/9;',
        content,
        flags=re.DOTALL
    )
    
    # Update body styles
    content = re.sub(
        r'body\s*{[^}]*}',
        lambda m: m.group(0).replace('}', '\n            margin: 0;\n            padding: 0;\n            overflow-x: hidden;\n        }'),
        content,
        flags=re.DOTALL
    )
    
    # Update slide-number positioning
    content = re.sub(
        r'\.slide-number\s*{[^}]*}',
        '''        .slide-number {
            position: absolute;
            top: clamp(15px, 1.5vw, 30px);
            left: clamp(15px, 1.5vw, 30px);
            font-size: clamp(12px, 0.8vw, 16px);
            color: #999;
            font-weight: 500;
        }''',
        content,
        flags=re.DOTALL
    )
    
    # Update h1 headings to be responsive
    content = re.sub(
        r'h1\s*{[^}]*font-size:\s*(\d+)px;[^}]*}',
        lambda m: m.group(0).replace(
            f'font-size: {m.group(1)}px;',
            f'font-size: clamp({max(24, int(m.group(1))//2)}px, {int(m.group(1))/19.2:.1f}vw, {m.group(1)}px);'
        ),
        content,
        flags=re.DOTALL
    )
    
    # Update h2 headings
    content = re.sub(
        r'h2\s*{[^}]*font-size:\s*(\d+)px;[^}]*}',
        lambda m: m.group(0).replace(
            f'font-size: {m.group(1)}px;',
            f'font-size: clamp({max(18, int(m.group(1))//2)}px, {int(m.group(1))/19.2:.1f}vw, {m.group(1)}px);'
        ),
        content,
        flags=re.DOTALL
    )
    
    # Update h3 headings
    content = re.sub(
        r'h3\s*{[^}]*font-size:\s*(\d+)px;[^}]*}',
        lambda m: m.group(0).replace(
            f'font-size: {m.group(1)}px;',
            f'font-size: clamp({max(16, int(m.group(1))//2)}px, {int(m.group(1))/19.2:.1f}vw, {m.group(1)}px);'
        ),
        content,
        flags=re.DOTALL
    )
    
    # Update h4 headings
    content = re.sub(
        r'h4\s*{[^}]*font-size:\s*(\d+)px;[^}]*}',
        lambda m: m.group(0).replace(
            f'font-size: {m.group(1)}px;',
            f'font-size: clamp({max(14, int(m.group(1))//2)}px, {int(m.group(1))/19.2:.1f}vw, {m.group(1)}px);'
        ),
        content,
        flags=re.DOTALL
    )
    
    # Update .subtitle class
    content = re.sub(
        r'\.subtitle\s*{[^}]*font-size:\s*(\d+)px;[^}]*}',
        lambda m: m.group(0).replace(
            f'font-size: {m.group(1)}px;',
            f'font-size: clamp({max(14, int(m.group(1))//2)}px, {int(m.group(1))/19.2:.1f}vw, {m.group(1)}px);'
        ),
        content,
        flags=re.DOTALL
    )
    
    # Update navigation container
    content = re.sub(
        r'\.nav-container\s*{[^}]*}',
        '''        .nav-container {
            position: fixed;
            top: clamp(10px, 1vw, 20px);
            left: 50%;
            transform: translateX(-50%);
            z-index: 1000;
            display: flex;
            align-items: center;
            gap: clamp(8px, 0.8vw, 15px);
            background: rgba(255, 255, 255, 0.95);
            padding: clamp(8px, 0.6vw, 12px) clamp(12px, 1vw, 20px);
            border-radius: clamp(15px, 1.3vw, 25px);
            box-shadow: 0 0.4vw 1.3vw rgba(0, 0, 0, 0.15);
            backdrop-filter: blur(10px);
        }''',
        content,
        flags=re.DOTALL
    )
    
    # Update slide-counter
    content = re.sub(
        r'\.slide-counter\s*{[^}]*}',
        '''        .slide-counter {
            font-size: clamp(11px, 0.7vw, 14px);
            font-weight: 600;
            color: #0047AB;
            min-width: clamp(60px, 4vw, 80px);
            text-align: center;
        }''',
        content,
        flags=re.DOTALL
    )
    
    # Update slide-select
    content = re.sub(
        r'\.slide-select\s*{[^}]*}',
        '''        .slide-select {
            padding: clamp(6px, 0.4vw, 8px) clamp(8px, 0.6vw, 12px);
            border: 1px solid #ddd;
            border-radius: clamp(4px, 0.3vw, 6px);
            font-size: clamp(11px, 0.7vw, 14px);
            background: white;
            cursor: pointer;
            outline: none;
        }''',
        content,
        flags=re.DOTALL
    )
    
    # Update nav-btn
    content = re.sub(
        r'\.nav-btn\s*{[^}]*}',
        '''        .nav-btn {
            position: fixed;
            top: 50%;
            transform: translateY(-50%);
            z-index: 1000;
            background: rgba(0, 71, 171, 0.9);
            color: white;
            border: none;
            width: clamp(35px, 2.6vw, 50px);
            height: clamp(35px, 2.6vw, 50px);
            border-radius: 50%;
            font-size: clamp(14px, 1vw, 20px);
            cursor: pointer;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 0.2vw 0.8vw rgba(0, 71, 171, 0.3);
        }''',
        content,
        flags=re.DOTALL
    )
    
    # Update nav-btn positioning
    content = re.sub(
        r'\.nav-btn\.prev\s*{\s*left:\s*30px;\s*}',
        '        .nav-btn.prev {\n            left: clamp(15px, 1.5vw, 30px);\n        }',
        content
    )
    
    content = re.sub(
        r'\.nav-btn\.next\s*{\s*right:\s*30px;\s*}',
        '        .nav-btn.next {\n            right: clamp(15px, 1.5vw, 30px);\n        }',
        content
    )
    
    # Update shadow and border-radius values to be relative
    content = re.sub(r'box-shadow: 0 (\d+)px (\d+)px', 
                    lambda m: f'box-shadow: 0 {int(m.group(1))/19.2:.1f}vw {int(m.group(2))/19.2:.1f}vw', 
                    content)
    
    content = re.sub(r'border-radius: (\d+)px', 
                    lambda m: f'border-radius: clamp({max(4, int(m.group(1))//2)}px, {int(m.group(1))/19.2:.1f}vw, {m.group(1)}px)', 
                    content)
    
    # Add enhanced responsive media queries if not present
    if '@media (max-width: 1366px)' not in content:
        responsive_css = '''
        /* Enhanced Responsive Design */
        @media (max-width: 1366px) {
            .slide {
                padding: clamp(15px, 2.5vw, 40px);
            }
        }

        @media (max-width: 768px) {
            .slide {
                padding: clamp(10px, 2vw, 25px);
            }
            
            h1 {
                font-size: clamp(24px, 5vw, 48px) !important;
            }
            
            h2 {
                font-size: clamp(20px, 4vw, 36px) !important;
            }
            
            h3 {
                font-size: clamp(18px, 3.5vw, 28px) !important;
            }
        }

        @media (max-width: 480px) {
            .nav-container {
                padding: 6px 10px;
                gap: 6px;
            }
            
            .slide-counter {
                min-width: 50px;
                font-size: 10px;
            }
            
            .slide-select {
                font-size: 10px;
                padding: 4px 6px;
            }
        }'''
        
        # Insert before closing </style>
        content = content.replace('</style>', responsive_css + '\n    </style>')
    
    # Write updated content back to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    """Process all HTML slide files"""
    
    # Get all HTML files
    html_files = glob.glob('*.html')
    
    processed = 0
    
    for file_path in html_files:
        try:
            print(f"Processing {file_path}...")
            make_responsive(file_path)
            processed += 1
            print(f"✓ {file_path} made responsive")
        except Exception as e:
            print(f"✗ Error processing {file_path}: {e}")
    
    print(f"\nProcessed {processed} files successfully!")

if __name__ == "__main__":
    main()