#!/usr/bin/env python3
import os
import re
from pathlib import Path

NOTES_DIR = "notes"

def get_folder_icon(folder_name):
    """Get special icon for specific folders"""
    special_folders = {
        'QN': '📜',
        'Previous Questions': '📜'
    }
    return special_folders.get(folder_name, '📁')

def update_static_cards(content):
    """Update static file cards in HTML"""
    # Pattern for static folder cards
    pattern = r'<a href="([^"]+)" class="file-card">\s*<div class="card-header">\s*<div class="icon-wrapper">📁</div>\s*<span class="file-badge badge-folder">Folder</span>\s*</div>\s*<span class="file-name">([^<]+)</span>'
    
    def replace_folder(match):
        href, name = match.groups()
        folder_name = href.rstrip('/')
        icon = get_folder_icon(folder_name if folder_name else name)
        return f'''<a href="{href}" class="file-card">
        <div class="card-header">
          <div class="icon-wrapper">{icon}</div>
          <span class="file-badge badge-folder">Folder</span>
        </div>
        <span class="file-name">{name}</span>'''
    
    content = re.sub(pattern, replace_folder, content)
    
    # Pattern for static file cards - clean up any toolbar/download attributes
    file_pattern = r'<a href="([^"]*\.pdf)"[^>]*(download|#toolbar[^"]*)?[^>]*class="file-card">'
    
    def replace_file(match):
        href = match.group(1)
        return f'<a href="{href}" class="file-card">'
    
    content = re.sub(file_pattern, replace_file, content)
    
    return content

def update_dynamic_files(content):
    """Update dynamic file loading script"""
    # Pattern for the old script
    old_script = r"""const grid = document\.getElementById\('file-grid'\);

    // Load folders first
    fetch\('folders\.json'\)
      \.then\(res => res\.json\(\)\)
      \.then\(folders => \{
        folders\.forEach\(folder => \{
          grid\.innerHTML \+= `
            <a href="\$\{folder\}/" class="file-card">
              <div class="folder-icon">📂</div>
              <span class="file-name">\$\{folder\}</span>
            </a>`;
        \}\);
      \}\);

    // Then load files
    fetch\('files\.json'\)
      \.then\(res => res\.json\(\)\)
      \.then\(files => \{
        files\.forEach\(file => \{
          const name = file\.replace\(/\\\.\[\^\\/\.]\+\$\/, ''\);
          grid\.innerHTML \+= `
            <a href="\$\{file\}" class="file-card">
              <div class="folder-icon">📄</div>
              <span class="file-name">\$\{name\}</span>
            </a>`;
        \}\);
      \}\);"""
    
    new_script = """const grid = document.getElementById('file-grid');

    function getFileExtension(filename) {
      return filename.split('.').pop().toLowerCase();
    }

    function getFolderIcon(folderName) {
      const specialFolders = {
        'QN': '📜',
        'Previous Questions': '📜'
      };
      return specialFolders[folderName] || '📁';
    }

    function getFileIcon(ext) {
      const icons = {
        'pdf': '📄',
        'doc': '📋', 'docx': '📋',
        'xls': '📊', 'xlsx': '📊',
        'ppt': '🎯', 'pptx': '🎯',
        'zip': '📦', 'rar': '📦',
        'txt': '📝', 'md': '📝',
        'jpg': '🖼️', 'jpeg': '🖼️', 'png': '🖼️', 'gif': '🖼️',
        'mp4': '🎬', 'avi': '🎬',
        'mp3': '🎵',
        'default': '📄'
      };
      return icons[ext] || icons['default'];
    }

    // Load folders first
    fetch('folders.json')
      .then(res => res.json())
      .then(folders => {
        folders.forEach(folder => {
          const folderIcon = getFolderIcon(folder);
          grid.innerHTML += `
            <a href="${folder}/" class="file-card">
              <div class="card-header">
                <div class="icon-wrapper">${folderIcon}</div>
                <span class="file-badge badge-folder">Folder</span>
              </div>
              <span class="file-name">${folder}</span>
              <div class="file-meta">
                <span class="file-type">📂 Directory</span>
              </div>
            </a>`;
        });
      });

    // Then load files
    fetch('files.json')
      .then(res => res.json())
      .then(files => {
        files.forEach(file => {
          const name = file.replace(/\.[^\/]+$/, '');
          const ext = getFileExtension(file);
          const icon = getFileIcon(ext);
          grid.innerHTML += `
            <a href="${file}" class="file-card">
              <div class="card-header">
                <div class="icon-wrapper">${icon}</div>
                <span class="file-badge badge-file">File</span>
              </div>
              <span class="file-name">${name}</span>
              <div class="file-meta">
                <span class="file-type">${ext.toUpperCase()}</span>
              </div>
            </a>`;
        });
      });"""
    
    if re.search(old_script, content):
        content = re.sub(old_script, new_script, content)
    
    return content

def process_html_file(filepath):
    """Process a single HTML file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Update static cards
    content = update_static_cards(content)
    
    # Update dynamic scripts (more flexible pattern)
    if 'file-grid' in content and 'folders.json' in content:
        # Find the script tag
        script_pattern = r'(<script>.*?)</script>'
        script_match = re.search(script_pattern, content, re.DOTALL)
        if script_match:
            old_script_content = script_match.group(1)
            # Check if it contains the old structure
            if 'folder-icon' in old_script_content:
                new_script = """<script>
    const grid = document.getElementById('file-grid');

    function getFileExtension(filename) {
      return filename.split('.').pop().toLowerCase();
    }

    function getFolderIcon(folderName) {
      const specialFolders = {
        'QN': '📜',
        'Previous Questions': '📜'
      };
      return specialFolders[folderName] || '📁';
    }

    function getFileIcon(ext) {
      const icons = {
        'pdf': '📄',
        'doc': '📋', 'docx': '📋',
        'xls': '📊', 'xlsx': '📊',
        'ppt': '🎯', 'pptx': '🎯',
        'zip': '📦', 'rar': '📦',
        'txt': '📝', 'md': '📝',
        'jpg': '🖼️', 'jpeg': '🖼️', 'png': '🖼️', 'gif': '🖼️',
        'mp4': '🎬', 'avi': '🎬',
        'mp3': '🎵',
        'default': '📄'
      };
      return icons[ext] || icons['default'];
    }

    // Load folders first
    fetch('folders.json')
      .then(res => res.json())
      .then(folders => {
        folders.forEach(folder => {
          const folderIcon = getFolderIcon(folder);
          grid.innerHTML += `
            <a href="${folder}/" class="file-card">
              <div class="card-header">
                <div class="icon-wrapper">${folderIcon}</div>
                <span class="file-badge badge-folder">Folder</span>
              </div>
              <span class="file-name">${folder}</span>
              <div class="file-meta">
                <span class="file-type">📂 Directory</span>
              </div>
            </a>`;
        });
      });

    // Then load files
    fetch('files.json')
      .then(res => res.json())
      .then(files => {
        files.forEach(file => {
          const name = file.replace(/\.[^\/]+$/, '');
          const ext = getFileExtension(file);
          const icon = getFileIcon(ext);
          grid.innerHTML += `
            <a href="${file}" class="file-card">
              <div class="card-header">
                <div class="icon-wrapper">${icon}</div>
                <span class="file-badge badge-file">File</span>
              </div>
              <span class="file-name">${name}</span>
              <div class="file-meta">
                <span class="file-type">${ext.toUpperCase()}</span>
              </div>
            </a>`;
        });
      });
  </script>"""
                
                content = re.sub(script_pattern, new_script, content, flags=re.DOTALL)
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    updated_count = 0
    
    for root, dirs, files in os.walk(NOTES_DIR):
        for file in files:
            if file == 'index.html':
                filepath = os.path.join(root, file)
                try:
                    if process_html_file(filepath):
                        updated_count += 1
                        print(f"✅ Updated: {filepath}")
                    else:
                        print(f"⏭️  Skipped (no changes): {filepath}")
                except Exception as e:
                    print(f"❌ Error processing {filepath}: {e}")
    
    print(f"\n✨ Total updated: {updated_count} files")

if __name__ == '__main__':
    main()
