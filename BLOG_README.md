# Blog System - Barbarossa Lives Game Studio

This document explains how to use and manage the blog system for your FastAPI website.

## Overview

The blog system includes:
- **Blog listing page** (`/blog`) - Shows all published blog posts
- **Individual blog posts** (`/blog/{id}`) - Full blog post pages
- **Category filtering** (`/blog/category/{slug}`) - Filter posts by category
- **Tag filtering** (`/blog/tag/{tag}`) - Filter posts by tag
- **Blog management tool** - Command-line tool to manage posts

## File Structure

```
mainsite_render/
├── main.py                 # FastAPI app with blog routes
├── blog_manager.py         # Blog management script
├── data/
│   └── blog_posts.json     # Blog posts data (JSON)
├── templates/
│   ├── blog.html          # Blog listing page
│   └── blog_post.html     # Individual blog post page
└── static/
    └── images/            # Blog post images
```

## Quick Start

1. **Start the server:**
   ```bash
   python main.py
   ```

2. **Visit the blog:**
   - Blog listing: http://localhost:8000/blog
   - Individual posts: http://localhost:8000/blog/1, /blog/2, etc.

3. **Manage blog posts:**
   ```bash
   python blog_manager.py
   ```

## Blog Management

### Using the Blog Manager

Run the blog manager script:
```bash
python blog_manager.py
```

**Available options:**
1. **Add new post** - Create a new blog post
2. **List all posts** - View all existing posts
3. **Edit post** - Modify an existing post
4. **Delete post** - Remove a post
5. **Exit** - Quit the manager

### Adding a New Blog Post

1. Choose option 1 from the menu
2. Enter the post details:
   - **Title**: The post title
   - **Excerpt**: Brief description (shown in listings)
   - **Category**: Choose from available categories
   - **Image**: Filename from `static/images/` folder
   - **Read time**: Estimated reading time
   - **Tags**: Comma-separated tags
   - **Content**: HTML content (type 'END' when finished)

3. The post will be automatically published and available at `/blog/{id}`

### Blog Post Structure

Each blog post contains:
```json
{
  "id": 1,
  "title": "Post Title",
  "slug": "post-title",
  "excerpt": "Brief description",
  "content": "<h2>HTML content</h2><p>...</p>",
  "author": "Barbarossa Lives",
  "date": "2024-01-15",
  "category": "Game Development",
  "read_time": "5 min read",
  "image": "image.png",
  "tags": ["tag1", "tag2"],
  "published": true
}
```

## Categories

Default categories:
- **Game Development** - Tutorials and tips
- **Industry Insights** - Market trends and analysis
- **Development** - Technical guides
- **Creative Process** - Design ideas and workflows

## Content Guidelines

### HTML Content
Blog posts use HTML for formatting. Common elements:
- `<h2>`, `<h3>` - Headers
- `<p>` - Paragraphs
- `<ul>`, `<li>` - Lists
- `<strong>` - Bold text
- `<em>` - Italic text
- `<a href="...">` - Links

### Images
- Place images in `static/images/`
- Reference by filename only (e.g., "my-image.png")
- Recommended size: 800x400px for featured images

### Tags
Use relevant tags to help readers find your content:
- `beginner`, `advanced` - Skill level
- `tutorial`, `guide` - Content type
- `unity`, `godot`, `unreal` - Game engines
- `mobile`, `pc`, `console` - Platforms

## URL Structure

- **Blog home**: `/blog`
- **Individual post**: `/blog/{id}`
- **Category**: `/blog/category/{slug}`
- **Tag**: `/blog/tag/{tag}`

## Customization

### Adding New Categories
Edit `data/blog_posts.json` and add to the categories array:
```json
{
  "name": "New Category",
  "slug": "new-category",
  "description": "Category description"
}
```

### Styling
- Blog styles are in `templates/blog.html` and `templates/blog_post.html`
- Colors match your site theme (#653119, #58E5F7)
- Responsive design for mobile and desktop

### Features
- **Social sharing** - Twitter, Facebook, LinkedIn
- **Related posts** - Automatically shows related content
- **Comments section** - Ready for integration
- **Newsletter signup** - Email collection form
- **Search and filtering** - Category and tag filtering

## Troubleshooting

### Common Issues

1. **Post not showing up**
   - Check if `published` is set to `true`
   - Verify the JSON file is valid

2. **Images not loading**
   - Ensure image exists in `static/images/`
   - Check filename spelling

3. **JSON errors**
   - Validate JSON syntax
   - Use the blog manager to avoid syntax errors

### Validation
To check your JSON file:
```bash
python -m json.tool data/blog_posts.json
```

## Future Enhancements

Potential improvements:
- **Admin interface** - Web-based management
- **Rich text editor** - WYSIWYG content editing
- **Image upload** - Direct image uploads
- **Comments system** - Database-backed comments
- **SEO optimization** - Meta tags and sitemaps
- **RSS feeds** - Blog syndication
- **Search functionality** - Full-text search

## Support

For issues or questions about the blog system, check:
1. The JSON file syntax
2. Image file paths
3. FastAPI server logs
4. Browser developer console

The blog system is designed to be simple yet powerful, allowing you to focus on creating great content for your game development audience. 