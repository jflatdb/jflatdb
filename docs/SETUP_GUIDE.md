# Documentation Website Setup Guide

## 📁 Structure

```
docs/
├── index.html              # Main documentation page
├── assets/
│   ├── css/style.css       # Styles
│   ├── js/script.js        # Navigation
│   └── img/logo.png        # Logo
├── README.md               # Documentation guide
└── SETUP_GUIDE.md          # This file
```

## 📄 Sections

The documentation includes 6 main sections:
1. Introduction
2. Installation
3. Quick Start
4. Contribution Guide
5. Special Thanks (Contributors)
6. Sponsors

## 🚀 Usage

### View Locally

```bash
# Direct open
xdg-open docs/index.html

# Or with server
cd docs && python -m http.server 8000
# Visit: http://localhost:8000
```

### Deploy to GitHub Pages

1. Go to repository Settings → Pages
2. Set source to `docs/` folder
3. Site will be live at `https://jflatdb.github.io/jflatdb/`

## ✏️ How to Add a New Section

### 1. Add to HTML (`index.html`)

```html
<section id="new-section" class="section">
  <h2>Section Title</h2>
  <p>Your content here...</p>
</section>
```

### 2. Add to Navigation

```html
<li><a href="#new-section" class="nav-link">Section Name</a></li>
```

### 3. Done!

JavaScript automatically handles:
- Active section highlighting
- Smooth scrolling
- URL hash updates

## 🎨 Styling

All styles in `assets/css/style.css`:

### Color Palette
```
Background: #ffffff (white)
Sidebar:    #f8f9fa (light gray)
Primary:    #2563eb (blue)
Text:       #1f2937 (dark gray)
```

### Key Classes
- `.section` - Content sections
- `.nav-link` - Navigation links
- `.contributor-card` - Contributor cards
- `.project-link` - jflatdb links (blue)

## 📱 Responsive

- **Desktop (>1024px)**: Full sidebar visible
- **Tablet (768-1024px)**: Smaller sidebar
- **Mobile (<768px)**: Collapsible sidebar with toggle

## 🔧 Features

- ✅ Smooth scroll navigation
- ✅ Active section highlighting
- ✅ Mobile sidebar toggle
- ✅ Copy code buttons
- ✅ URL hash fragments
- ✅ GitHub profile links

