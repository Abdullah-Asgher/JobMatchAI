import markdown
import os

# Read the markdown file
with open('CN7050_Final_Report.md', 'r', encoding='utf-8') as f:
    md_content = f.read()

# Convert markdown to HTML
html_content = markdown.markdown(md_content, extensions=['extra', 'codehilite', 'tables', 'fenced_code'])

# Create a professional academic HTML template
html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CN7050 Coursework Report - JobMatchAI</title>
    <style>
        @page {{
            size: A4;
            margin: 2.5cm 2.5cm 3cm 2.5cm;
            @bottom-center {{
                content: counter(page);
                font-family: 'Times New Roman', serif;
                font-size: 11pt;
            }}
        }}
        
        body {{
            font-family: 'Times New Roman', Georgia, serif;
            font-size: 12pt;
            line-height: 1.6;
            color: #000;
            max-width: 210mm;
            margin: 0 auto;
            padding: 20px;
            background: white;
        }}
        
        h1 {{
            font-size: 18pt;
            font-weight: bold;
            margin-top: 24pt;
            margin-bottom: 12pt;
            page-break-after: avoid;
            color: #1a1a1a;
        }}
        
        h2 {{
            font-size: 16pt;
            font-weight: bold;
            margin-top: 20pt;
            margin-bottom: 10pt;
            page-break-after: avoid;
            color: #1a1a1a;
        }}
        
        h3 {{
            font-size: 14pt;
            font-weight: bold;
            margin-top: 16pt;
            margin-bottom: 8pt;
            page-break-after: avoid;
            color: #2a2a2a;
        }}
        
        h4 {{
            font-size: 12pt;
            font-weight: bold;
            margin-top: 12pt;
            margin-bottom: 6pt;
            page-break-after: avoid;
            font-style: italic;
        }}
        
        p {{
            margin: 0 0 12pt 0;
            text-align: justify;
        }}
        
        code {{
            font-family: 'Courier New', Consolas, monospace;
            font-size: 10pt;
            background: #f5f5f5;
            padding: 2px 4px;
            border-radius: 3px;
        }}
        
        pre {{
            background: #f8f8f8;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 12px;
            overflow-x: auto;
            font-family: 'Courier New', Consolas, monospace;
            font-size: 10pt;
            line-height: 1.4;
            margin: 12pt 0;
            page-break-inside: avoid;
        }}
        
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 12pt 0;
            page-break-inside: avoid;
        }}
        
        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}
        
        th {{
            background-color: #f2f2f2;
            font-weight: bold;
        }}
        
        ul, ol {{
            margin: 0 0 12pt 0;
            padding-left: 30pt;
        }}
        
        li {{
            margin-bottom: 6pt;
        }}
        
        blockquote {{
            margin: 12pt 20pt;
            padding-left: 15pt;
            border-left: 3px solid #ccc;
            color: #666;
            font-style: italic;
        }}
        
        .page-break {{
            page-break-after: always;
        }}
        
        .cover-page {{
            text-align: center;
            padding-top: 100pt;
        }}
        
        .cover-page h1 {{
            font-size: 24pt;
            margin-bottom: 40pt;
        }}
        
        .cover-page p {{
            font-size: 14pt;
            margin: 10pt 0;
        }}
        
        @media print {{
            body {{
                margin: 0;
                padding: 0;
            }}
            
            .no-print {{
                display: none;
            }}
        }}
    </style>
</head>
<body>
    {html_content}
</body>
</html>
"""

# Write HTML file
with open('CN7050_Final_Report.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print("HTML file created successfully: CN7050_Final_Report.html")
print("\nTo convert to PDF:")
print("1. Open CN7050_Final_Report.html in your browser")
print("2. Press Ctrl+P (print)")
print("3. Select 'Save as PDF' as the destination")
print("4. Click 'Save'")
