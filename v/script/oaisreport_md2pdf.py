"""Markdown to PDF converter"""
import subprocess
import sys
import argparse
from pathlib import Path


def convert_md_to_pdf(input_path: str, output_path: str):
    """Convert markdown to PDF using markdown + weasyprint"""
    try:
        import markdown
        from weasyprint import HTML, CSS
    except ImportError:
        print('weasyprint가 설치되어 있지 않습니다.')
        print('설치: uv pip install weasyprint')
        sys.exit(1)

    # Read markdown file
    with open(input_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Convert markdown to HTML
    html_content = markdown.markdown(
        md_content,
        extensions=['tables', 'fenced_code', 'codehilite']
    )

    # Wrap with HTML template
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{
                font-family: 'Malgun Gothic', sans-serif;
                font-size: 11pt;
                line-height: 1.6;
                margin: 2cm;
            }}
            h1 {{ font-size: 18pt; margin-top: 1em; }}
            h2 {{ font-size: 14pt; margin-top: 0.8em; }}
            h3 {{ font-size: 12pt; margin-top: 0.6em; }}
            code {{
                font-family: Consolas, monospace;
                font-size: 9pt;
                background-color: #f4f4f4;
                padding: 2px 4px;
            }}
            pre {{
                background-color: #f4f4f4;
                padding: 10px;
                overflow-x: auto;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                margin: 1em 0;
            }}
            th, td {{
                border: 1px solid #000;
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #f0f0f0;
                font-weight: bold;
            }}
            blockquote {{
                margin-left: 1em;
                padding-left: 1em;
                border-left: 3px solid #ccc;
                color: #666;
            }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """

    # Convert HTML to PDF
    HTML(string=full_html).write_pdf(output_path)
    print(f'PDF 문서 생성 완료: {output_path}')


def convert_with_pandoc(input_path: str, output_path: str):
    """Convert markdown to PDF using pandoc (supports LaTeX math)"""
    import os

    # Try different PDF engines in order of preference
    engines = ['xelatex', 'pdflatex', 'lualatex', 'wkhtmltopdf']

    for engine in engines:
        cmd = ['pandoc', input_path, '-o', output_path, f'--pdf-engine={engine}']
        if engine == 'xelatex':
            cmd.extend(['-V', 'mainfont=Malgun Gothic'])
        cmd.extend(['-V', 'geometry:margin=2cm'])

        result = subprocess.run(cmd, capture_output=True)
        if result.returncode == 0 and os.path.exists(output_path):
            print(f'PDF 문서 생성 완료 (pandoc/{engine}): {output_path}')
            return

    print('PDF 엔진을 찾을 수 없습니다.')
    print('다음 중 하나를 설치해주세요: xelatex, pdflatex, wkhtmltopdf')
    sys.exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Markdown to PDF converter')
    parser.add_argument('input_file', nargs='?', default='doc/d0102_가상논문.md',
                        help='Input markdown file')
    parser.add_argument('--pandoc', action='store_true',
                        help='Use pandoc for conversion (supports LaTeX math)')
    args = parser.parse_args()

    input_file = args.input_file
    output_file = input_file.rsplit('.', 1)[0] + '.pdf'

    if args.pandoc:
        convert_with_pandoc(input_file, output_file)
    else:
        convert_md_to_pdf(input_file, output_file)
