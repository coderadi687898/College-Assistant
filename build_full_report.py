import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

TEMPLATE_PATH = r"C:/Users/Aditya/.gemini/antigravity/brain/baeb5cba-9fd3-4e2b-b1a8-7cf9e21fdddd/.user_uploaded/media_1792635115471_0399c95c.docx"
OUTPUT_PATH = r"d:\Projects\Minor Project\College Assistant\IIIT_Bhopal_Minor_Project_Report_DocuVideo_RAG.docx"
OUTPUT_COPY = r"d:\Projects\Minor Project\College Assistant\Minor_Project_Report_DocuVideo_RAG.docx"
FIG_DIR = r"d:\Projects\Minor Project\College Assistant\report_assets\figures"

def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=180, right=180):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def set_table_borders(table, color="D1D5DB", sz="4", val="single"):
    tblPr = table._element.xpath('w:tblPr')
    if tblPr:
        borders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>'
            f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'</w:tblBorders>'
        )
        tblPr[0].append(borders)

def add_p(doc, text="", font_size=12, bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=4, line_spacing=1.15):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    if text:
        r = p.add_run(text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(font_size)
        r.font.bold = bold
        r.font.italic = italic
    return p

def add_h1(doc, text, center=True):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER if center else WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(16)
    r.font.bold = True
    return p

def add_h2(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(13)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(14)
    r.font.bold = True
    return p

def add_h3(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(9)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.bold = True
    return p

def add_bullet(doc, bold_prefix, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.left_indent = Inches(0.25)
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    
    r_sym = p.add_run("•  ")
    r_sym.font.name = "Times New Roman"
    r_sym.font.size = Pt(12)
    r_sym.font.bold = True
    
    if bold_prefix:
        r_pre = p.add_run(bold_prefix + ": ")
        r_pre.font.name = "Times New Roman"
        r_pre.font.size = Pt(12)
        r_pre.font.bold = True
        
    r_txt = p.add_run(text)
    r_txt.font.name = "Times New Roman"
    r_txt.font.size = Pt(12)
    return p

def add_fig_cap(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(12)
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.italic = True
    return p

def add_tbl_cap(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.bold = True
    return p

def add_figure(doc, img_name, caption_text, width=Inches(6.0)):
    img_path = os.path.join(FIG_DIR, img_name)
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(2)
        p_img.paragraph_format.keep_with_next = True
        p_img.add_run().add_picture(img_path, width=width)
        add_fig_cap(doc, caption_text)
    else:
        print(f"Warning: Missing figure: {img_path}")

def add_page_break(doc):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.add_run().add_break(WD_BREAK.PAGE)

def add_algorithm_box(doc, algo_num, title, inputs, outputs, steps):
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_cap.paragraph_format.space_before = Pt(10)
    p_cap.paragraph_format.space_after = Pt(4)
    p_cap.paragraph_format.keep_with_next = True
    r = p_cap.add_run(f"Algorithm {algo_num}: {title}")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)
    r.font.bold = True
    
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.rows[0].cells[0]
    set_cell_background(cell, "F8FAFC")
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    set_table_borders(tbl, color="94A3B8", sz="6")
    
    cp = cell.paragraphs[0]
    cp.paragraph_format.space_before = Pt(0)
    cp.paragraph_format.space_after = Pt(2)
    cp.paragraph_format.line_spacing = 1.15
    
    r_in = cp.add_run("Input: ")
    r_in.font.name = "Times New Roman"; r_in.font.size = Pt(11); r_in.font.bold = True
    r_in_val = cp.add_run(inputs + "\n")
    r_in_val.font.name = "Times New Roman"; r_in_val.font.size = Pt(11)
    
    r_out = cp.add_run("Output: ")
    r_out.font.name = "Times New Roman"; r_out.font.size = Pt(11); r_out.font.bold = True
    r_out_val = cp.add_run(outputs + "\n")
    r_out_val.font.name = "Times New Roman"; r_out_val.font.size = Pt(11)
    
    r_div = cp.add_run("―" * 60 + "\n")
    r_div.font.name = "Times New Roman"; r_div.font.size = Pt(10); r_div.font.bold = True
    
    for s_idx, s in enumerate(steps, 1):
        r_step_num = cp.add_run(f"{s_idx:02d}: ")
        r_step_num.font.name = "Courier New"; r_step_num.font.size = Pt(10); r_step_num.font.bold = True
        r_step_txt = cp.add_run(s + "\n")
        r_step_txt.font.name = "Times New Roman"; r_step_txt.font.size = Pt(11)
        
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

def create_table_from_data(doc, caption_text, headers, rows_data, col_widths=None):
    add_tbl_cap(doc, caption_text)
    tbl = doc.add_table(rows=len(rows_data) + 1, cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl, color="94A3B8", sz="4")
    
    # Header row
    hdr_row = tbl.rows[0]
    for c_idx, h_text in enumerate(headers):
        c = hdr_row.cells[c_idx]
        set_cell_background(c, "1E293B")
        set_cell_margins(c, top=140, bottom=140, left=180, right=180)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h_text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        
    # Data rows
    for r_idx, row_items in enumerate(rows_data):
        row = tbl.rows[r_idx + 1]
        bg_col = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_items):
            c = row.cells[c_idx]
            set_cell_background(c, bg_col)
            set_cell_margins(c, top=100, bottom=100, left=150, right=150)
            p = c.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.15
            # Center if short or number
            if len(str(val)) <= 15 or c_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(str(val))
            r.font.name = "Times New Roman"
            r.font.size = Pt(10.5)
            if c_idx == 0 and len(str(val)) <= 5:
                r.font.bold = True
                
    if col_widths:
        for r in tbl.rows:
            for c_idx, w in enumerate(col_widths):
                r.cells[c_idx].width = Inches(w)
                
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

print("Report generator framework loaded.")
