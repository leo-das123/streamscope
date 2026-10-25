# StreamScope â€” Music Listening Analytics

A responsive editorial-style data analytics blog built as a **single-file NiceGUI application**. The project presents analytical case studies through descriptive statistics, hypothesis testing, clustering, visualization, and business recommendations.

> **Project type:** Academic / coursework portfolio  
> **Primary application:** `app.py`  
> **Framework:** NiceGUI  
> **Language:** Python

## Live Project

**Deployment platform:** Render Web Service. The live public URL is assigned by Render and is available in the service dashboard.

**GitHub repository:**  
https://github.com/leo-das123/streamscope

## Overview

**StreamScope** is designed as a practical data analytics and visualization publication rather than a traditional dashboard.

The site follows an end-to-end analytics narrative:

```text
Business Question
       â†“
Data Preparation
       â†“
Descriptive Statistics
       â†“
Hypothesis Testing
       â†“
Clustering
       â†“
Visualization
       â†“
Business Insights
       â†“
Recommendations
```

The main case study, **â€œDecoding the Playlist: How Data Analytics Reveals the Way We Really Listen to Musicâ€**, examines listener behaviour and uses a simulated music-streaming dataset to demonstrate how analytics can uncover meaningful listener segments.

## Key Features

- Responsive editorial-style blog layout
- Single Python entrypoint using NiceGUI
- Shared navigation across all pages
- Responsive desktop, tablet, and mobile layouts
- Featured case study section
- Blog archive with category filtering
- Blog search functionality
- Animated and responsive post cards
- Business Strategy case-study card
- Long-form analytical article with:
  - Table of contents
  - Reading progress indicator
  - Share/copy-link actions
  - Data tables
  - Figures and captions
  - Statistical findings
  - Clustering analysis
  - Business recommendations
  - Limitations and future scope
- Email-draft contact form and front-end-only newsletter form
- Local static image serving
- Reduced-motion support for accessibility
- Keyboard focus styling
- Mobile navigation drawer

## Topics

The blog archive is organized into four topic categories:

| Topic | Purpose |
|---|---|
| **Analytics Life Cycle** | Discovery, preparation, model planning, model building, communication, and operationalization |
| **Statistical Methods** | Descriptive statistics, distributions, group comparisons, hypothesis testing, and correlation |
| **Clustering & Machine Learning** | K-Means clustering, standardization, elbow-method selection, and listener segmentation |
| **Business Strategy** | Translating analytical segments into product, retention, recommendation, and marketing actions |

## Featured Case Study

### Decoding the Playlist

The featured article studies a representative set of **240 listener profiles** and explores four listener segments:

1. Genre Loyalists
2. Playlist Hoppers
3. Night-Owl Explorers
4. Casual Listeners

The case study combines:

- Descriptive statistics
- Independent two-sample t-test
- Correlation analysis
- K-Means clustering
- Elbow-method model selection
- Segment interpretation
- Product and marketing recommendations

The article is written as an end-to-end demonstration of how analytical outputs can move from numbers and visualizations to business decisions.

## Application Routes

The current NiceGUI application defines these routes:

```text
- `/`
- `/blog`
- `/article`
- `/about`
- `/contact`
```

| Route | Page |
|---|---|
| `/` | Home |
| `/blog` | Blog archive |
| `/article` | Full featured case study |
| `/about` | About the blog and author |
| `/contact` | Contact / dataset suggestion form |

## Project Structure

```text
streamscope/
â”‚
â”œâ”€â”€ app.py
â”œâ”€â”€ requirements.txt
â”œâ”€â”€ .gitignore
â”‚
â””â”€â”€ assets/
    â””â”€â”€ images/
        â”œâ”€â”€ image1.png
        â”œâ”€â”€ image2.png
        â”œâ”€â”€ image3.png
        â”œâ”€â”€ image4.png
        â””â”€â”€ image5.png
```

### Important architecture note

The project intentionally keeps the main application in **one Python file**.

`app.py` contains:

- page content
- shared header/footer templates
- CSS
- client-side JavaScript
- route definitions
- static asset configuration
- application startup configuration

So separate `index.html`, `blog.html`, `article.html`, `about.html`, `contact.html`, `styles.css`, and `script.js` files are not required by the deployed application.

The chart/visual assets remain separate PNG files so they can be served efficiently and retain their original quality.

## Tech Stack

### Backend / Application

- **Python**
- **NiceGUI**

### Frontend

- HTML embedded in Python templates
- CSS embedded in `app.py`
- JavaScript embedded in `app.py`

### Typography

The visual system uses:

- Fraunces
- IBM Plex Sans
- IBM Plex Mono

### Visual Design

The interface follows an editorial/data-publication aesthetic using:

- Warm ivory backgrounds
- Deep navy typography
- Teal data accents
- Amber analytical highlights
- Structured cards
- Responsive grids
- Subtle hover and entrance animations

## Requirements

- Python 3.13 recommended
- `pip`
- Internet connection during dependency installation if NiceGUI is not already installed

Dependencies are defined in:

```text
requirements.txt
```

Current dependency:

```text
nicegui
```

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/leo-das123/streamscope.git
cd streamscope
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Start the application

```powershell
python app.py
```

The local application will normally be available at:

```text
http://127.0.0.1:8080
```

The application also reads the hosting platform's `PORT` environment variable and binds to:

```text
0.0.0.0
```

which makes the same application suitable for hosted deployment.

## Render Deployment

The application is designed to run as a Render Web Service. The app reads Render's `PORT` environment variable and binds to `0.0.0.0`.

### Configure the web service

In the Render dashboard, create or open the Web Service connected to this repository and the `main` branch. Use:

- **Build command:** `pip install -r requirements.txt`
- **Start command:** `python app.py`

After a successful deployment, Render displays the public service URL in the dashboard. Use that exact URL when sharing the live project; the service URL is separate from the GitHub repository URL.

If automatic deploys are enabled, a push to the configured branch triggers a new deployment. If automatic deploys are disabled, deploy the latest commit from the Render dashboard.

## Git Workflow

After making changes locally:

```powershell
git status
git add .
git commit -m "Describe the change"
git push
```

The local `main` branch is connected to:

```text
https://github.com/leo-das123/streamscope
```

## Asset Handling

The application detects common project layouts and serves the selected image directory through `/assets`.

The primary project layout is:

```text
assets/
â””â”€â”€ images/
```

The available chart assets are:

```text
- `/assets/image1.png`
- `/assets/image2.png`
- `/assets/image3.png`
- `/assets/image4.png`
- `/assets/image5.png`
```

This keeps image files outside the Python source while keeping the actual web application in one Python entrypoint.

## Blog Filtering Logic

The blog archive uses category metadata stored on each card:

```text
data-cat="lifecycle"
data-cat="stats"
data-cat="clustering"
data-cat="strategy"
```

The filtering system supports:

- All Posts
- Clustering & ML
- Statistical Methods
- Analytics Life Cycle
- Business Strategy

The search field filters posts using their searchable metadata.

Current category mapping includes a dedicated Business Strategy card:

```text
Analytics Life Cycle
    â†’ lifecycle post

Statistical Methods
    â†’ summary statistics post
    â†’ hypothesis testing post

Clustering & ML
    â†’ elbow-method post
    â†’ Decoding the Playlist post

Business Strategy
    â†’ Turning Listener Segments into Product Strategy
```

## Business Strategy Section

The Business Strategy card is intentionally separate from the K-Means category.

Its focus is the **prescriptive/business-action layer** of the case study: converting the discovered listener segments into practical product, recommendation, retention, and marketing actions.

This distinction keeps the blog taxonomy logically consistent:

```text
Clustering
= Discover the segments

Business Strategy
= Decide what to do with those segments
```

## User Experience

The UI is designed around a few principles:

### Editorial hierarchy

Large serif headings and compact metadata create a publication-style reading experience.

### Data-first presentation

Charts, statistical tables, explanatory text, and recommendations are presented together rather than separating the analysis from its interpretation.

### Responsive behavior

The layout adapts across:

```text
Desktop â†’ 3-column blog grid
Tablet  â†’ 2-column blog grid
Mobile  â†’ 1-column blog grid
```

Navigation becomes a mobile drawer on smaller screens.

### Interaction

Cards use subtle hover movement and image scaling, while the article includes a reading progress indicator and active table-of-contents navigation.

## Forms

The contact form opens the visitor's default email application with a message addressed to `sailee.gore23@pccoepune.org`; the visitor must press Send to deliver it. It does not send mail directly from the server.

The newsletter form is currently front-end-only and does not store subscriptions. A backend integration or mailing-list service would be needed for persistent signups.

## Accessibility / Usability

The application includes:

- Responsive layouts
- Visible keyboard focus states
- `aria-label` attributes on interactive controls
- Mobile navigation state management
- Reduced-motion support
- Responsive images
- Scrollable article tables on smaller screens

## Development Notes

The project intentionally keeps the visual identity close to the original static site while moving the application into NiceGUI.

When editing the application, the main areas are:

```text
app.py
â”‚
â”œâ”€â”€ PATHS / CONFIGURATION
â”œâ”€â”€ CSS
â”œâ”€â”€ JS
â”œâ”€â”€ SHARED PAGE SHELL
â”œâ”€â”€ PAGE_HOME
â”œâ”€â”€ PAGE_BLOG
â”œâ”€â”€ PAGE_ARTICLE
â”œâ”€â”€ PAGE_ABOUT
â”œâ”€â”€ PAGE_CONTACT
â”œâ”€â”€ ROUTES
â””â”€â”€ main()
```

For content changes, edit the relevant `PAGE_*` section instead of duplicating page templates.

## Current Scope

This project is primarily an **academic analytics and visualization portfolio**.

The current case study uses illustrative/simulated analytical data rather than a production streaming-platform data extract. The purpose is to demonstrate the complete reasoning workflow:

```text
Question
  â†“
Data
  â†“
Statistics
  â†“
Testing
  â†“
Clustering
  â†“
Visualization
  â†“
Business Interpretation
  â†“
Recommendation
```

## Future Improvements

Potential next improvements include:

- Real backend handling for contact submissions
- Persistent newsletter subscriptions
- Additional independent case studies
- A CMS or structured content layer
- Real analytics instrumentation
- More datasets and interactive visualizations
- Search improvements
- SEO metadata per article
- Automated testing
- CI/CD through GitHub and Render

## Author / Academic Context

**StreamScope** is presented as a Data Analytics & Visualization coursework portfolio.

The featured **â€œDecoding the Playlistâ€** case study applies the data analytics life cycle, statistical testing, and K-Means clustering to a simulated music-streaming dataset and connects the analytical findings to plausible product and marketing decisions.

## License

This repository is intended for **academic and educational portfolio use**.

Before reusing any included third-party assets, fonts, content, or external resources in another project, verify their applicable licenses and usage terms.

---

## Quick Start

```powershell
git clone https://github.com/leo-das123/streamscope.git
cd streamscope

python -m venv .venv
.\.venv\Scripts\Activate.ps1

python -m pip install -r requirements.txt
python app.py
```

Open:

```text
http://127.0.0.1:8080
```

---

**StreamScope â€” Music Listening Analytics**

Discover listening patterns. Understand listener segments.

*Data, Decoded â€” project portfolio*

