from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from pathlib import Path
import markdown2
from ..utils.i18n import get_text, TRANSLATIONS

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/")
async def home(request: Request, lang: str = "en"):
    """Render the main page with markdown content"""
    # Read and convert markdown content
    markdown_path = Path("project.md")
    with open(markdown_path) as f:
        content = f.read()
        
    html_content = markdown2.markdown(content)
    
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "lang": lang,
            "translations": {k: get_text(k, lang) for k in TRANSLATIONS["en"].keys()},
            "markdown_content": html_content
        }
    ) 