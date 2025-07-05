from fastapi import FastAPI, Request, HTTPException, Form, File, UploadFile, Depends, status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse, JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import uvicorn
import json
import os
import secrets
from datetime import datetime
from typing import Optional
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv not installed, skip loading .env file
    pass

app = FastAPI(title="Business Website", version="1.0.0")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Security
security = HTTPBasic()

# Admin credentials (in production, use environment variables)
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "barbarossa2024")

# Email configuration
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")  # Default to Gmail SMTP
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME", "")  # Your email username
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")  # Your email password or app password
EMAIL_FROM = os.getenv("EMAIL_FROM", "noreply@yourdomain.com")
EMAIL_TO = "montebruce@proton.me"  # Where contact form messages will be sent

# Configure logging
logging.basicConfig(level=logging.INFO)

# Session storage (in production, use Redis or database)
admin_sessions = {}

def verify_admin_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    """Verify admin credentials"""
    is_username_correct = secrets.compare_digest(credentials.username, ADMIN_USERNAME)
    is_password_correct = secrets.compare_digest(credentials.password, ADMIN_PASSWORD)
    
    if not (is_username_correct and is_password_correct):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

def get_session_token(request: Request) -> Optional[str]:
    """Get session token from cookies"""
    return request.cookies.get("admin_session")

def verify_admin_session(request: Request):
    """Verify admin session is valid"""
    session_token = get_session_token(request)
    if not session_token or session_token not in admin_sessions:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Admin session required",
            headers={"WWW-Authenticate": "Basic"},
        )
    return session_token

def create_admin_session(username: str) -> str:
    """Create a new admin session"""
    session_token = secrets.token_urlsafe(32)
    admin_sessions[session_token] = {
        "username": username,
        "created_at": datetime.now(),
        "last_activity": datetime.now()
    }
    return session_token

def load_blog_posts():
    """Load blog posts from JSON file"""
    try:
        with open("data/blog_posts.json", "r") as f:
            data = json.load(f)
            # Convert to dictionary with ID as key for easier lookup
            posts_dict = {post["id"]: post for post in data["posts"] if post.get("published", True)}
            return posts_dict, data.get("categories", []), data.get("tags", [])
    except FileNotFoundError:
        print("Warning: blog_posts.json not found. Using empty blog data.")
        return {}, [], []
    except json.JSONDecodeError:
        print("Warning: Invalid JSON in blog_posts.json. Using empty blog data.")
        return {}, [], []

def save_blog_data(posts_dict, categories, tags):
    """Save blog data to JSON file"""
    os.makedirs("data", exist_ok=True)
    data = {
        "posts": list(posts_dict.values()),
        "categories": categories,
        "tags": tags
    }
    with open("data/blog_posts.json", "w") as f:
        json.dump(data, f, indent=2)

def get_next_post_id(posts_dict):
    """Get the next available post ID"""
    if not posts_dict:
        return 1
    return max(posts_dict.keys()) + 1

def create_slug(title: str) -> str:
    """Create a URL-friendly slug from title"""
    return title.lower().replace(' ', '-').replace(':', '').replace('!', '').replace('?', '').replace('.', '')

# Load blog data
BLOG_POSTS, BLOG_CATEGORIES, BLOG_TAGS = load_blog_posts()

@app.get("/favicon.ico")
async def favicon():
    """Serve favicon"""
    return FileResponse("static/images/logoTransparentNoWords.png")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page route"""
    # Get the latest 3 published blog posts, sorted by date descending
    blog_posts = sorted(BLOG_POSTS.values(), key=lambda p: p["date"], reverse=True)[:3]
    return templates.TemplateResponse("index.html", {"request": request, "blog_posts": blog_posts})

@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    """About page route"""
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/contact", response_class=HTMLResponse)
async def contact(request: Request):
    """Contact page route"""
    return templates.TemplateResponse("contact.html", {"request": request})

async def send_email(subject: str, body: str, to_email: str = EMAIL_TO):
    """Send email using SMTP"""
    try:
        # Create message
        message = MIMEMultipart()
        message["From"] = EMAIL_FROM
        message["To"] = to_email
        message["Subject"] = subject

        # Add body to email
        message.attach(MIMEText(body, "html"))

        # Send email
        await aiosmtplib.send(
            message,
            hostname=EMAIL_HOST,
            port=EMAIL_PORT,
            start_tls=True,
            username=EMAIL_USERNAME,
            password=EMAIL_PASSWORD,
        )
        return True
    except Exception as e:
        logging.error(f"Failed to send email: {str(e)}")
        return False

@app.post("/contact/submit")
async def submit_contact_form(
    firstName: str = Form(...),
    lastName: str = Form(...),
    email: str = Form(...),
    phone: str = Form(default=""),
    company: str = Form(default=""),
    subject: str = Form(...),
    message: str = Form(...)
):
    """Handle contact form submission"""
    try:
        # Create email subject
        email_subject = f"Contact Form: {subject}"

        # Create email body
        email_body = f"""
        <html>
        <body>
            <h2>New Contact Form Submission</h2>
            <p><strong>Name:</strong> {firstName} {lastName}</p>
            <p><strong>Email:</strong> {email}</p>
            <p><strong>Phone:</strong> {phone if phone else 'Not provided'}</p>
            <p><strong>Company:</strong> {company if company else 'Not provided'}</p>
            <p><strong>Subject:</strong> {subject}</p>
            <p><strong>Message:</strong></p>
            <div style="background-color: #f5f5f5; padding: 15px; border-left: 4px solid #007bff;">
                {message.replace('\n', '<br>')}
            </div>
            <hr>
            <p><small>This message was sent from the contact form on your website.</small></p>
        </body>
        </html>
        """

        # Send email
        email_sent = await send_email(email_subject, email_body)

        if email_sent:
            return JSONResponse(
                status_code=200,
                content={"success": True, "message": "Thank you for your message! We'll get back to you soon."}
            )
        else:
            return JSONResponse(
                status_code=500,
                content={"success": False, "message": "Sorry, there was an error sending your message. Please try again later."}
            )

    except Exception as e:
        logging.error(f"Contact form error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": "Sorry, there was an error processing your request. Please try again later."}
        )

@app.get("/games", response_class=HTMLResponse)
async def games(request: Request):
    """Games page route"""
    return templates.TemplateResponse("games.html", {"request": request})

@app.get("/games/rule-beyton", response_class=HTMLResponse)
async def rule_beyton(request: Request):
    """Rule Beyton project page route"""
    return templates.TemplateResponse("rule_beyton.html", {"request": request})

@app.get("/business-solutions", response_class=HTMLResponse)
async def business_solutions(request: Request):
    """Business Solutions page route"""
    return templates.TemplateResponse("business_solutions.html", {"request": request})

@app.get("/blog", response_class=HTMLResponse)
async def blog(request: Request):
    """Blog page route"""
    # Convert dictionary to list for template
    blog_posts = list(BLOG_POSTS.values())
    
    return templates.TemplateResponse("blog.html", {
        "request": request,
        "blog_posts": blog_posts,
        "categories": BLOG_CATEGORIES,
        "tags": BLOG_TAGS
    })

@app.get("/blog/{post_id}", response_class=HTMLResponse)
async def blog_post(request: Request, post_id: int):
    """Individual blog post route"""
    if post_id not in BLOG_POSTS:
        raise HTTPException(status_code=404, detail="Blog post not found")
    
    post = BLOG_POSTS[post_id]
    
    # Get related posts (excluding current post)
    related_posts = [p for p in BLOG_POSTS.values() if p["id"] != post_id][:3]
    
    return templates.TemplateResponse("blog_post.html", {
        "request": request,
        "post": post,
        "related_posts": related_posts
    })

@app.get("/blog/category/{category_slug}", response_class=HTMLResponse)
async def blog_category(request: Request, category_slug: str):
    """Blog posts by category"""
    # Find category
    category = next((cat for cat in BLOG_CATEGORIES if cat["slug"] == category_slug), None)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Filter posts by category
    category_posts = [post for post in BLOG_POSTS.values() if post["category"] == category["name"]]
    
    return templates.TemplateResponse("blog.html", {
        "request": request,
        "blog_posts": category_posts,
        "categories": BLOG_CATEGORIES,
        "tags": BLOG_TAGS,
        "current_category": category
    })

@app.get("/blog/tag/{tag}", response_class=HTMLResponse)
async def blog_tag(request: Request, tag: str):
    """Blog posts by tag"""
    if tag not in BLOG_TAGS:
        raise HTTPException(status_code=404, detail="Tag not found")
    
    # Filter posts by tag
    tag_posts = [post for post in BLOG_POSTS.values() if tag in post.get("tags", [])]
    
    return templates.TemplateResponse("blog.html", {
        "request": request,
        "blog_posts": tag_posts,
        "categories": BLOG_CATEGORIES,
        "tags": BLOG_TAGS,
        "current_tag": tag
    })

# Admin authentication route
@app.get("/admin/login", response_class=HTMLResponse)
async def admin_login_page(request: Request):
    """Admin login page"""
    return templates.TemplateResponse("admin/login.html", {"request": request})

@app.post("/admin/login")
async def admin_login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    """Handle admin login"""
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        session_token = create_admin_session(username)
        response = RedirectResponse(url="/admin", status_code=303)
        response.set_cookie(
            key="admin_session",
            value=session_token,
            httponly=True,
            secure=False,  # Set to True in production with HTTPS
            samesite="lax",
            max_age=3600  # 1 hour
        )
        return response
    else:
        return templates.TemplateResponse("admin/login.html", {
            "request": request,
            "error": "Invalid username or password"
        })

@app.get("/admin/logout")
async def admin_logout(request: Request):
    """Handle admin logout"""
    session_token = get_session_token(request)
    if session_token in admin_sessions:
        del admin_sessions[session_token]
    
    response = RedirectResponse(url="/admin/login", status_code=303)
    response.delete_cookie("admin_session")
    return response

# Admin routes (protected)
@app.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(request: Request, session_token: str = Depends(verify_admin_session)):
    """Admin dashboard overview"""
    blog_posts = list(BLOG_POSTS.values())
    return templates.TemplateResponse("admin/dashboard.html", {
        "request": request,
        "blog_posts": blog_posts,
        "categories": BLOG_CATEGORIES,
        "tags": BLOG_TAGS
    })

@app.get("/admin/blog", response_class=HTMLResponse)
async def admin_blog_list(request: Request, session_token: str = Depends(verify_admin_session)):
    """Admin blog listing page"""
    blog_posts = list(BLOG_POSTS.values())
    return templates.TemplateResponse("admin/blog_list.html", {
        "request": request,
        "blog_posts": blog_posts,
        "categories": BLOG_CATEGORIES
    })

@app.get("/admin/blog/new", response_class=HTMLResponse)
async def admin_new_post(request: Request, session_token: str = Depends(verify_admin_session)):
    """New blog post form"""
    return templates.TemplateResponse("admin/blog_form.html", {
        "request": request,
        "post": None,
        "categories": BLOG_CATEGORIES,
        "tags": BLOG_TAGS
    })

@app.post("/admin/blog/new")
async def admin_create_post(
    request: Request,
    session_token: str = Depends(verify_admin_session),
    title: str = Form(...),
    excerpt: str = Form(...),
    content: str = Form(...),
    category: str = Form(...),
    image: str = Form(default="game_tool_full.png"),
    read_time: str = Form(default="5 min read"),
    tags: str = Form(default=""),
    published: bool = Form(default=True)
):
    """Create new blog post"""
    global BLOG_POSTS, BLOG_TAGS
    
    # Parse tags
    tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
    
    # Add new tags to global list
    for tag in tag_list:
        if tag not in BLOG_TAGS:
            BLOG_TAGS.append(tag)
    
    # Create new post
    new_post = {
        "id": get_next_post_id(BLOG_POSTS),
        "title": title,
        "slug": create_slug(title),
        "excerpt": excerpt,
        "content": content,
        "author": "Barbarossa Lives",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "category": category,
        "read_time": read_time,
        "image": image,
        "tags": tag_list,
        "published": published
    }
    
    BLOG_POSTS[new_post["id"]] = new_post
    save_blog_data(BLOG_POSTS, BLOG_CATEGORIES, BLOG_TAGS)
    
    return RedirectResponse(url="/admin/blog", status_code=303)

@app.get("/admin/blog/{post_id}/edit", response_class=HTMLResponse)
async def admin_edit_post(request: Request, post_id: int, session_token: str = Depends(verify_admin_session)):
    """Edit blog post form"""
    if post_id not in BLOG_POSTS:
        raise HTTPException(status_code=404, detail="Blog post not found")
    
    post = BLOG_POSTS[post_id]
    return templates.TemplateResponse("admin/blog_form.html", {
        "request": request,
        "post": post,
        "categories": BLOG_CATEGORIES,
        "tags": BLOG_TAGS
    })

@app.post("/admin/blog/{post_id}/edit")
async def admin_update_post(
    request: Request,
    post_id: int,
    session_token: str = Depends(verify_admin_session),
    title: str = Form(...),
    excerpt: str = Form(...),
    content: str = Form(...),
    category: str = Form(...),
    image: str = Form(...),
    read_time: str = Form(...),
    tags: str = Form(...),
    published: bool = Form(default=True)
):
    """Update blog post"""
    global BLOG_POSTS, BLOG_TAGS
    
    if post_id not in BLOG_POSTS:
        raise HTTPException(status_code=404, detail="Blog post not found")
    
    # Parse tags
    tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
    
    # Add new tags to global list
    for tag in tag_list:
        if tag not in BLOG_TAGS:
            BLOG_TAGS.append(tag)
    
    # Update post
    BLOG_POSTS[post_id].update({
        "title": title,
        "slug": create_slug(title),
        "excerpt": excerpt,
        "content": content,
        "category": category,
        "image": image,
        "read_time": read_time,
        "tags": tag_list,
        "published": published
    })
    
    save_blog_data(BLOG_POSTS, BLOG_CATEGORIES, BLOG_TAGS)
    
    return RedirectResponse(url="/admin/blog", status_code=303)

@app.post("/admin/blog/{post_id}/delete")
async def admin_delete_post(request: Request, post_id: int, session_token: str = Depends(verify_admin_session)):
    """Delete blog post"""
    global BLOG_POSTS
    
    if post_id not in BLOG_POSTS:
        raise HTTPException(status_code=404, detail="Blog post not found")
    
    del BLOG_POSTS[post_id]
    save_blog_data(BLOG_POSTS, BLOG_CATEGORIES, BLOG_TAGS)
    
    return RedirectResponse(url="/admin/blog", status_code=303)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 