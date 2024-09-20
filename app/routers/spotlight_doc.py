from fastapi import APIRouter, Request
from starlette.responses import HTMLResponse

router = APIRouter()


@router.get("", include_in_schema=False)
def api_documentation(request: Request):
    """
    Stoplight Documentation
    """
    return HTMLResponse(
        """
        <!doctype html>
        <html lang="en">
          <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
            <title>Elements in HTML</title>
        
            <script src="https://unpkg.com/@stoplight/elements/web-components.min.js"></script>
            <link rel="stylesheet" href="https://unpkg.com/@stoplight/elements/styles.min.css">
          </head>
          <body>
        
            <elements-api
              apiDescriptionUrl="openapi.json"
              router="hash"
            />
        
          </body>
        </html>"""
    )
