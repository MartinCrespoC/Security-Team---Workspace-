#!/usr/bin/env python3
"""
🛡️ Security Team - Professional PDF Report Generator
Generates beautiful PDF reports from Markdown security assessments
"""

import sys
import os
import re
from datetime import datetime

try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch, mm
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
        PageBreak, Image, HRFlowable
    )
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
except ImportError:
    print("Installing required packages...")
    os.system("pip install reportlab markdown")
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch, mm
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
        PageBreak, Image, HRFlowable
    )
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY


# Color scheme
COLORS = {
    'primary': colors.HexColor('#1a1a2e'),
    'secondary': colors.HexColor('#16213e'),
    'accent': colors.HexColor('#e94560'),
    'success': colors.HexColor('#00bf63'),
    'warning': colors.HexColor('#ffc107'),
    'danger': colors.HexColor('#dc3545'),
    'info': colors.HexColor('#0dcaf0'),
    'light': colors.HexColor('#f8f9fa'),
    'dark': colors.HexColor('#212529'),
    'red_team': colors.HexColor('#dc3545'),
    'blue_team': colors.HexColor('#0d6efd'),
    'purple_team': colors.HexColor('#6f42c1'),
}


def create_styles():
    """Create custom paragraph styles"""
    styles = getSampleStyleSheet()
    
    # Title style
    styles.add(ParagraphStyle(
        name='ReportTitle',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=COLORS['primary'],
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    ))
    
    # Subtitle
    styles.add(ParagraphStyle(
        name='ReportSubtitle',
        parent=styles['Normal'],
        fontSize=14,
        textColor=COLORS['secondary'],
        spaceAfter=20,
        alignment=TA_CENTER
    ))
    
    # Section headers
    styles.add(ParagraphStyle(
        name='SectionHeader',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=COLORS['primary'],
        spaceBefore=20,
        spaceAfter=12,
        borderColor=COLORS['accent'],
        borderWidth=2,
        borderPadding=5,
        fontName='Helvetica-Bold'
    ))
    
    # Subsection
    styles.add(ParagraphStyle(
        name='SubSection',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=COLORS['secondary'],
        spaceBefore=15,
        spaceAfter=8,
        fontName='Helvetica-Bold'
    ))
    
    # Body text
    styles.add(ParagraphStyle(
        name='CustomBody',
        parent=styles['Normal'],
        fontSize=10,
        textColor=COLORS['dark'],
        spaceAfter=8,
        alignment=TA_JUSTIFY,
        leading=14
    ))
    
    # Code block
    styles.add(ParagraphStyle(
        name='CodeBlock',
        parent=styles['Normal'],
        fontSize=9,
        fontName='Courier',
        textColor=COLORS['dark'],
        backColor=COLORS['light'],
        borderColor=colors.grey,
        borderWidth=1,
        borderPadding=8,
        spaceAfter=10
    ))
    
    # Severity styles
    styles.add(ParagraphStyle(
        name='SeverityCritical',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.white,
        backColor=COLORS['danger'],
        borderPadding=5,
        fontName='Helvetica-Bold'
    ))
    
    styles.add(ParagraphStyle(
        name='SeverityHigh',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.white,
        backColor=COLORS['warning'],
        borderPadding=5,
        fontName='Helvetica-Bold'
    ))
    
    styles.add(ParagraphStyle(
        name='SeverityMedium',
        parent=styles['Normal'],
        fontSize=11,
        textColor=COLORS['dark'],
        backColor=colors.HexColor('#ffc107'),
        borderPadding=5
    ))
    
    styles.add(ParagraphStyle(
        name='SeverityLow',
        parent=styles['Normal'],
        fontSize=11,
        textColor=COLORS['dark'],
        backColor=COLORS['info'],
        borderPadding=5
    ))
    
    return styles


def parse_markdown(md_content):
    """Parse markdown content into sections"""
    sections = []
    current_section = {'title': '', 'content': [], 'level': 0}
    
    lines = md_content.split('\n')
    in_code_block = False
    code_content = []
    in_table = False
    table_rows = []
    
    for line in lines:
        # Code blocks
        if line.startswith('```'):
            if in_code_block:
                current_section['content'].append({
                    'type': 'code',
                    'content': '\n'.join(code_content)
                })
                code_content = []
            in_code_block = not in_code_block
            continue
        
        if in_code_block:
            code_content.append(line)
            continue
        
        # Tables
        if '|' in line and not line.startswith('#'):
            if '---' in line:
                continue
            cells = [c.strip() for c in line.split('|')[1:-1]]
            if cells:
                if not in_table:
                    in_table = True
                    table_rows = []
                table_rows.append(cells)
            continue
        elif in_table:
            current_section['content'].append({
                'type': 'table',
                'content': table_rows
            })
            table_rows = []
            in_table = False
        
        # Headers
        if line.startswith('# '):
            if current_section['title'] or current_section['content']:
                sections.append(current_section)
            current_section = {
                'title': line[2:].strip(),
                'content': [],
                'level': 1
            }
        elif line.startswith('## '):
            if current_section['title'] or current_section['content']:
                sections.append(current_section)
            current_section = {
                'title': line[3:].strip(),
                'content': [],
                'level': 2
            }
        elif line.startswith('### '):
            current_section['content'].append({
                'type': 'subsection',
                'content': line[4:].strip()
            })
        elif line.startswith('#### '):
            current_section['content'].append({
                'type': 'subsubsection',
                'content': line[5:].strip()
            })
        elif line.startswith('- '):
            current_section['content'].append({
                'type': 'bullet',
                'content': line[2:].strip()
            })
        elif line.startswith('---'):
            current_section['content'].append({'type': 'hr'})
        elif line.strip():
            # Clean markdown formatting
            text = line.strip()
            text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
            text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
            text = re.sub(r'`(.+?)`', r'<font face="Courier">\1</font>', text)
            current_section['content'].append({
                'type': 'text',
                'content': text
            })
    
    # Add last table if exists
    if in_table and table_rows:
        current_section['content'].append({
            'type': 'table',
            'content': table_rows
        })
    
    if current_section['title'] or current_section['content']:
        sections.append(current_section)
    
    return sections


def create_cover_page(styles, target, date, classification):
    """Create a professional cover page"""
    elements = []
    
    # Logo placeholder (shield emoji as text)
    elements.append(Spacer(1, 1.5*inch))
    elements.append(Paragraph("🛡️", ParagraphStyle(
        'Logo', fontSize=72, alignment=TA_CENTER
    )))
    elements.append(Spacer(1, 0.3*inch))
    
    # Title
    elements.append(Paragraph(
        "SECURITY ASSESSMENT REPORT",
        styles['ReportTitle']
    ))
    
    # Target
    elements.append(Paragraph(
        f"<b>Target:</b> {target}",
        styles['ReportSubtitle']
    ))
    
    # Separator
    elements.append(Spacer(1, 0.5*inch))
    elements.append(HRFlowable(
        width="60%",
        thickness=2,
        color=COLORS['accent'],
        spaceBefore=10,
        spaceAfter=10,
        hAlign='CENTER'
    ))
    elements.append(Spacer(1, 0.5*inch))
    
    # Info table
    info_data = [
        ['Date:', date],
        ['Classification:', classification],
        ['Assessment Type:', 'Full Security Operation'],
        ['Generated By:', 'Security Team by ConcordIA / TITAN'],
    ]
    
    info_table = Table(info_data, colWidths=[2*inch, 3*inch])
    info_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('TEXTCOLOR', (0, 0), (-1, -1), COLORS['secondary']),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ]))
    elements.append(info_table)
    
    # Footer
    elements.append(Spacer(1, 2*inch))
    elements.append(Paragraph(
        "🔴 RED TEAM OPERATIONS",
        ParagraphStyle('Footer', fontSize=14, alignment=TA_CENTER, 
                      textColor=COLORS['red_team'], fontName='Helvetica-Bold')
    ))
    elements.append(Paragraph(
        "CONFIDENTIAL - FOR AUTHORIZED PERSONNEL ONLY",
        ParagraphStyle('Disclaimer', fontSize=10, alignment=TA_CENTER,
                      textColor=COLORS['danger'])
    ))
    
    elements.append(PageBreak())
    return elements


def create_table(data, styles):
    """Create a styled table"""
    if not data:
        return None
    
    table = Table(data, repeatRows=1)
    
    style = TableStyle([
        # Header
        ('BACKGROUND', (0, 0), (-1, 0), COLORS['primary']),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        
        # Body
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('TEXTCOLOR', (0, 1), (-1, -1), COLORS['dark']),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        
        # Grid
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        
        # Alternating rows
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, COLORS['light']]),
    ])
    
    table.setStyle(style)
    return table


def add_header_footer(canvas, doc):
    """Add header and footer to each page"""
    canvas.saveState()
    
    # Header
    canvas.setFillColor(COLORS['primary'])
    canvas.rect(0, A4[1] - 40, A4[0], 40, fill=True, stroke=False)
    canvas.setFillColor(colors.white)
    canvas.setFont('Helvetica-Bold', 10)
    canvas.drawString(30, A4[1] - 25, "🛡️ SECURITY ASSESSMENT REPORT")
    canvas.drawRightString(A4[0] - 30, A4[1] - 25, "CONFIDENTIAL")
    
    # Footer
    canvas.setFillColor(COLORS['light'])
    canvas.rect(0, 0, A4[0], 30, fill=True, stroke=False)
    canvas.setFillColor(COLORS['secondary'])
    canvas.setFont('Helvetica', 8)
    canvas.drawString(30, 12, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    canvas.drawCentredString(A4[0]/2, 12, "Security Team by ConcordIA / TITAN")
    canvas.drawRightString(A4[0] - 30, 12, f"Page {doc.page}")
    
    canvas.restoreState()


def generate_pdf(md_file, output_file=None):
    """Generate PDF from markdown file"""
    
    # Read markdown
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Parse metadata
    target = "Unknown"
    date = datetime.now().strftime('%Y-%m-%d')
    classification = "CONFIDENTIAL"
    
    # Extract target from content
    target_match = re.search(r'\*\*Target:\*\*\s*(.+)', md_content)
    if target_match:
        target = target_match.group(1).strip()
    
    date_match = re.search(r'\*\*Date:\*\*\s*(.+)', md_content)
    if date_match:
        date = date_match.group(1).strip()
    
    # Output file
    if not output_file:
        output_file = md_file.replace('.md', '.pdf')
    
    # Create document
    doc = SimpleDocTemplate(
        output_file,
        pagesize=A4,
        rightMargin=30,
        leftMargin=30,
        topMargin=50,
        bottomMargin=40
    )
    
    styles = create_styles()
    elements = []
    
    # Cover page
    elements.extend(create_cover_page(styles, target, date, classification))
    
    # Parse content
    sections = parse_markdown(md_content)
    
    # Build content
    for section in sections:
        # Section title
        if section['title']:
            # Remove emojis for cleaner look (optional)
            title = re.sub(r'[^\w\s\-\.]', '', section['title']).strip()
            if section['level'] == 1:
                elements.append(Paragraph(title, styles['ReportTitle']))
            else:
                elements.append(Paragraph(title, styles['SectionHeader']))
        
        # Section content
        for item in section['content']:
            if item['type'] == 'text':
                elements.append(Paragraph(item['content'], styles['CustomBody']))
            
            elif item['type'] == 'subsection':
                title = re.sub(r'[^\w\s\-\.\:]', '', item['content']).strip()
                elements.append(Paragraph(title, styles['SubSection']))
            
            elif item['type'] == 'subsubsection':
                title = item['content']
                # Check for severity
                if 'CRITICAL' in title.upper() or 'HIGH' in title.upper():
                    elements.append(Spacer(1, 10))
                    elements.append(Paragraph(f"⚠️ {title}", styles['SubSection']))
                else:
                    elements.append(Paragraph(title, styles['SubSection']))
            
            elif item['type'] == 'bullet':
                elements.append(Paragraph(f"• {item['content']}", styles['CustomBody']))
            
            elif item['type'] == 'code':
                # Split long code blocks
                code_lines = item['content'].split('\n')
                code_text = '<br/>'.join(code_lines[:20])  # Limit lines
                elements.append(Paragraph(code_text, styles['CodeBlock']))
            
            elif item['type'] == 'table':
                table = create_table(item['content'], styles)
                if table:
                    elements.append(Spacer(1, 10))
                    elements.append(table)
                    elements.append(Spacer(1, 10))
            
            elif item['type'] == 'hr':
                elements.append(Spacer(1, 10))
                elements.append(HRFlowable(
                    width="100%",
                    thickness=1,
                    color=COLORS['accent'],
                    spaceBefore=5,
                    spaceAfter=5
                ))
    
    # Build PDF
    doc.build(elements, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
    
    print(f"✅ PDF generated: {output_file}")
    return output_file


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_pdf_report.py <markdown_file> [output_pdf]")
        print("Example: python generate_pdf_report.py report.md report.pdf")
        sys.exit(1)
    
    md_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(md_file):
        print(f"Error: File not found: {md_file}")
        sys.exit(1)
    
    generate_pdf(md_file, output_file)
