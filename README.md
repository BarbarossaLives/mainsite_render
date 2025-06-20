# Business Website

A modern, responsive business website built with FastAPI and Jinja2 templates.

## Features

- 🚀 **FastAPI Backend** - High-performance Python web framework
- 🎨 **Modern UI/UX** - Beautiful, responsive design with Bootstrap 5
- 📱 **Mobile-First** - Optimized for all device sizes
- ⚡ **Interactive Elements** - Smooth animations and hover effects
- 🔧 **Easy Customization** - Modular template structure
- 📧 **Contact Forms** - Ready-to-use contact functionality
- 🎯 **SEO Friendly** - Clean HTML structure and meta tags

## Project Structure

```
mainsite_render/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── templates/             # Jinja2 HTML templates
│   ├── base.html          # Base template with navigation and footer
│   └── index.html         # Home page template
├── static/                # Static assets
│   ├── css/
│   │   └── style.css      # Custom CSS styles
│   ├── js/
│   │   └── main.js        # JavaScript functionality
│   └── images/            # Image assets (add your images here)
└── .gitignore             # Git ignore file
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd mainsite_render
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. **Start the development server**
   ```bash
   python main.py
   ```
   Or using uvicorn directly:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Open your browser**
   Navigate to `http://localhost:8000`

## Development

### Adding New Pages

1. Create a new template in `templates/` directory
2. Add a route in `main.py`
3. Update navigation in `templates/base.html`

Example new page:
```python
@app.get("/services", response_class=HTMLResponse)
async def services(request: Request):
    return templates.TemplateResponse("services.html", {"request": request})
```

### Customizing Styles

- Edit `static/css/style.css` for custom styling
- Modify `templates/base.html` for layout changes
- Update `static/js/main.js` for interactive features

### Adding Content

- **Images**: Place in `static/images/` and reference with `{{ url_for('static', path='/images/filename.jpg') }}`
- **New CSS**: Add to `static/css/style.css`
- **New JS**: Add to `static/js/main.js`

## Customization Guide

### Business Information
Update the following in your templates:
- Company name: Replace "Your Business" throughout templates
- Contact information: Update footer and contact page
- Services: Modify the services section in `index.html`
- Social media links: Update in `base.html` footer

### Colors and Branding
Modify the CSS variables in `static/css/style.css`:
```css
:root {
    --primary-color: #667eea;
    --secondary-color: #764ba2;
    --accent-color: #ffc107;
}
```

### Content Sections
The home page includes:
- Hero section with call-to-action
- Services showcase
- Features/benefits
- Contact call-to-action

## Deployment

### Production Setup
1. Set environment variables:
   ```bash
   export ENVIRONMENT=production
   ```

2. Use a production WSGI server:
   ```bash
   pip install gunicorn
   gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

### Docker Deployment
Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## API Documentation

FastAPI automatically generates API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the repository
- Contact: [your-email@example.com]

---

**Built with ❤️ using FastAPI and Jinja2** 