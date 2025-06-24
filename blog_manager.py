#!/usr/bin/env python3
"""
Blog Manager for Barbarossa Lives Game Studio
A simple script to manage blog posts in JSON format
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any

BLOG_FILE = "data/blog_posts.json"

def load_blog_data() -> Dict[str, Any]:
    """Load blog data from JSON file"""
    if not os.path.exists(BLOG_FILE):
        # Create default structure
        default_data = {
            "posts": [],
            "categories": [
                {"name": "Game Development", "slug": "game-development", "description": "Tutorials and tips for game development"},
                {"name": "Industry Insights", "slug": "industry-insights", "description": "Market trends and industry analysis"},
                {"name": "Development", "slug": "development", "description": "Technical guides and development strategies"},
                {"name": "Creative Process", "slug": "creative-process", "description": "Design ideas and creative workflows"}
            ],
            "tags": []
        }
        save_blog_data(default_data)
        return default_data
    
    try:
        with open(BLOG_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {BLOG_FILE}")
        return {"posts": [], "categories": [], "tags": []}

def save_blog_data(data: Dict[str, Any]) -> None:
    """Save blog data to JSON file"""
    os.makedirs(os.path.dirname(BLOG_FILE), exist_ok=True)
    with open(BLOG_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_next_post_id(posts: List[Dict[str, Any]]) -> int:
    """Get the next available post ID"""
    if not posts:
        return 1
    return max(post["id"] for post in posts) + 1

def create_slug(title: str) -> str:
    """Create a URL-friendly slug from title"""
    return title.lower().replace(' ', '-').replace(':', '').replace('!', '').replace('?', '').replace('.', '')

def add_new_post() -> None:
    """Add a new blog post"""
    print("\n=== Add New Blog Post ===\n")
    
    data = load_blog_data()
    
    # Get post details
    title = input("Post title: ").strip()
    if not title:
        print("Title is required!")
        return
    
    excerpt = input("Post excerpt (brief description): ").strip()
    if not excerpt:
        print("Excerpt is required!")
        return
    
    print("\nAvailable categories:")
    for i, cat in enumerate(data["categories"], 1):
        print(f"{i}. {cat['name']}")
    
    try:
        cat_choice = int(input("Choose category (number): ")) - 1
        category = data["categories"][cat_choice]["name"]
    except (ValueError, IndexError):
        print("Invalid category choice!")
        return
    
    image = input("Image filename (from static/images/): ").strip()
    if not image:
        image = "game_tool_full.png"  # Default image
    
    read_time = input("Estimated read time (e.g., '5 min read'): ").strip()
    if not read_time:
        read_time = "5 min read"
    
    tags_input = input("Tags (comma-separated): ").strip()
    tags = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
    
    # Add new tags to the global tags list
    for tag in tags:
        if tag not in data["tags"]:
            data["tags"].append(tag)
    
    print("\nEnter the post content (HTML format). Type 'END' on a new line when finished:")
    content_lines = []
    while True:
        line = input()
        if line.strip() == 'END':
            break
        content_lines.append(line)
    
    content = '\n'.join(content_lines)
    
    # Create new post
    new_post = {
        "id": get_next_post_id(data["posts"]),
        "title": title,
        "slug": create_slug(title),
        "excerpt": excerpt,
        "content": content,
        "author": "Barbarossa Lives",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "category": category,
        "read_time": read_time,
        "image": image,
        "tags": tags,
        "published": True
    }
    
    data["posts"].append(new_post)
    save_blog_data(data)
    
    print(f"\n✅ Post '{title}' added successfully!")
    print(f"Post ID: {new_post['id']}")
    print(f"URL: /blog/{new_post['id']}")

def list_posts() -> None:
    """List all blog posts"""
    data = load_blog_data()
    
    print("\n=== Blog Posts ===\n")
    
    if not data["posts"]:
        print("No posts found.")
        return
    
    for post in data["posts"]:
        status = "✅ Published" if post.get("published", True) else "❌ Draft"
        print(f"ID: {post['id']} | {status}")
        print(f"Title: {post['title']}")
        print(f"Category: {post['category']}")
        print(f"Date: {post['date']}")
        print(f"URL: /blog/{post['id']}")
        print("-" * 50)

def edit_post() -> None:
    """Edit an existing blog post"""
    data = load_blog_data()
    
    if not data["posts"]:
        print("No posts to edit.")
        return
    
    list_posts()
    
    try:
        post_id = int(input("\nEnter post ID to edit: "))
        post = next((p for p in data["posts"] if p["id"] == post_id), None)
        
        if not post:
            print("Post not found!")
            return
        
        print(f"\nEditing post: {post['title']}")
        print("Leave blank to keep current value.\n")
        
        # Edit fields
        new_title = input(f"Title [{post['title']}]: ").strip()
        if new_title:
            post['title'] = new_title
            post['slug'] = create_slug(new_title)
        
        new_excerpt = input(f"Excerpt [{post['excerpt']}]: ").strip()
        if new_excerpt:
            post['excerpt'] = new_excerpt
        
        new_category = input(f"Category [{post['category']}]: ").strip()
        if new_category:
            post['category'] = new_category
        
        new_image = input(f"Image [{post['image']}]: ").strip()
        if new_image:
            post['image'] = new_image
        
        new_read_time = input(f"Read time [{post['read_time']}]: ").strip()
        if new_read_time:
            post['read_time'] = new_read_time
        
        new_tags = input(f"Tags [{', '.join(post['tags'])}]: ").strip()
        if new_tags:
            post['tags'] = [tag.strip() for tag in new_tags.split(',') if tag.strip()]
        
        save_blog_data(data)
        print("✅ Post updated successfully!")
        
    except ValueError:
        print("Invalid post ID!")

def delete_post() -> None:
    """Delete a blog post"""
    data = load_blog_data()
    
    if not data["posts"]:
        print("No posts to delete.")
        return
    
    list_posts()
    
    try:
        post_id = int(input("\nEnter post ID to delete: "))
        post = next((p for p in data["posts"] if p["id"] == post_id), None)
        
        if not post:
            print("Post not found!")
            return
        
        confirm = input(f"Are you sure you want to delete '{post['title']}'? (y/N): ").strip().lower()
        if confirm == 'y':
            data["posts"] = [p for p in data["posts"] if p["id"] != post_id]
            save_blog_data(data)
            print("✅ Post deleted successfully!")
        else:
            print("Deletion cancelled.")
            
    except ValueError:
        print("Invalid post ID!")

def main():
    """Main menu"""
    while True:
        print("\n" + "="*50)
        print("BLOG MANAGER - Barbarossa Lives Game Studio")
        print("="*50)
        print("1. Add new post")
        print("2. List all posts")
        print("3. Edit post")
        print("4. Delete post")
        print("5. Exit")
        print("-"*50)
        
        choice = input("Choose an option (1-5): ").strip()
        
        if choice == '1':
            add_new_post()
        elif choice == '2':
            list_posts()
        elif choice == '3':
            edit_post()
        elif choice == '4':
            delete_post()
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main() 