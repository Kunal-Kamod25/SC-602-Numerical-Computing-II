import os
from pathlib import Path
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=80, bottom=80, left=110, right=110):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table, color="D0D5DD", sz="4"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:left w:val="none"/>'
        f'  <w:bottom w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:right w:val="none"/>'
        f'  <w:insideH w:val="single" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def build_doc():
    base_dir = Path("/home/kunal/Desktop/SC-602-Numerical-Computing-II/Assignment_9")
    output_dir = base_dir / "output"

    doc = docx.Document()

    for section in doc.sections:
        section.top_margin = Inches(0.85)
        section.bottom_margin = Inches(0.85)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
        # Running header matching sample style
        header = section.header
        header_p = header.paragraphs[0]
        header_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = header_p.add_run("Numerical Computing II — Assignment-IX | Kunal Kamod (MS2513)")
        hrun.font.name = "Calibri"
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(120, 120, 120)

    style_normal = doc.styles['Normal']
    font = style_normal.font
    font.name = 'Calibri'
    font.size = Pt(11)
    font.color.rgb = RGBColor(30, 30, 30)

    # Title matching sample
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(2)
    run_t1 = p_title.add_run("Numerical Computing II\n")
    run_t1.bold = True
    run_t1.font.size = Pt(14)
    run_t1.font.color.rgb = RGBColor(20, 30, 55)

    run_t2 = p_title.add_run("Assignment IX — Numerical Integration on Real Driving Cycles Dataset\n")
    run_t2.bold = True
    run_t2.font.size = Pt(12)
    run_t2.font.color.rgb = RGBColor(30, 30, 30)

    run_t3 = p_title.add_run("Date: Oct 12, 2026\n\n")
    run_t3.font.size = Pt(10)
    run_t3.font.color.rgb = RGBColor(80, 80, 80)

    run_name = p_title.add_run("Name: Kunal Kamod\nRoll No: MS2513")
    run_name.bold = True
    run_name.font.size = Pt(11)

    # Intro matching sample wording
    p_intro = doc.add_paragraph()
    p_intro.paragraph_format.space_before = Pt(8)
    p_intro.paragraph_format.space_after = Pt(6)
    p_intro.paragraph_format.line_spacing = 1.15
    p_intro.add_run(
        "For this assignment, I downloaded a real electric vehicle dataset from Kaggle: \"Battery and Heating Data in Real Driving Cycles\" "
        "(https://www.kaggle.com/datasets/atechnohazard/battery-and-heating-data-in-real-driving-cycles). "
        "The dataset contains actual road test measurements recorded from a BMW i3 (60 Ah) EV, specifically TripB01 in winter conditions.\n\n"
        "We evaluate the cabin and battery Heating Power P(t) [W] over a 12-minute trip (t = 0 to 720 seconds, step size h = 60s, n = 12 intervals). "
        "The physical goal is to compute the total thermal energy consumed by integrating the power curve: E = ∫₀⁷²⁰ P(t) dt. "
        "Because n = 12 is both an even number and divisible by 3, all three numerical integration methods can be evaluated directly on the complete dataset."
    )

    # 1. Full Dataset (Scatter Plot)
    h1 = doc.add_paragraph()
    h1.paragraph_format.space_before = Pt(8)
    h1.paragraph_format.space_after = Pt(2)
    rh1 = h1.add_run("1. Full Dataset (Scatter Plot)")
    rh1.bold = True
    rh1.font.size = Pt(12)
    rh1.font.color.rgb = RGBColor(30, 70, 140)

    p_scat_desc = doc.add_paragraph()
    p_scat_desc.paragraph_format.space_before = Pt(2)
    p_scat_desc.paragraph_format.space_after = Pt(4)
    p_scat_desc.add_run("First, here is a scatter plot showing all 13 sampled telemetry points of Heating Power [W] across the trip:")

    scat_img = output_dir / "scatter_dataset.png"
    if scat_img.exists():
        p_img = doc.add_paragraph()
        p_img.paragraph_format.space_before = Pt(4)
        p_img.paragraph_format.space_after = Pt(6)
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture(str(scat_img), width=Inches(5.4))

    # 2. Individual Graphs for the 3 Methods (Matching reference PDF progression)
    h2 = doc.add_paragraph()
    h2.paragraph_format.space_before = Pt(10)
    h2.paragraph_format.space_after = Pt(2)
    rh2 = h2.add_run("2. Individual Approximations by Each Method")
    rh2.bold = True
    rh2.font.size = Pt(12)
    rh2.font.color.rgb = RGBColor(30, 70, 140)

    # (a) Trapezoidal
    p_t_head = doc.add_paragraph()
    p_t_head.paragraph_format.space_before = Pt(6)
    p_t_head.paragraph_format.space_after = Pt(2)
    rt = p_t_head.add_run("Method 1: Trapezoidal Rule (Linear Chords)")
    rt.bold = True
    rt.font.size = Pt(11)
    rt.font.color.rgb = RGBColor(20, 40, 80)

    p_t_desc = doc.add_paragraph()
    p_t_desc.paragraph_format.space_before = Pt(2)
    p_t_desc.paragraph_format.space_after = Pt(4)
    p_t_desc.add_run(
        "This graph shows the trapezoidal approximation connecting points with straight chords. "
        "Total computed thermal energy = 939,000.00 Joules (0.26083 kWh)."
    )

    t_img = output_dir / "method_trapezoidal.png"
    if t_img.exists():
        p_img = doc.add_paragraph()
        p_img.paragraph_format.space_before = Pt(4)
        p_img.paragraph_format.space_after = Pt(6)
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture(str(t_img), width=Inches(5.4))

    # (b) Simpson 1/3
    p_s13_head = doc.add_paragraph()
    p_s13_head.paragraph_format.space_before = Pt(6)
    p_s13_head.paragraph_format.space_after = Pt(2)
    rs13 = p_s13_head.add_run("Method 2: Simpson's 1/3 Rule (Quadratic Parabolas)")
    rs13.bold = True
    rs13.font.size = Pt(11)
    rs13.font.color.rgb = RGBColor(20, 40, 80)

    p_s13_desc = doc.add_paragraph()
    p_s13_desc.paragraph_format.space_before = Pt(2)
    p_s13_desc.paragraph_format.space_after = Pt(4)
    p_s13_desc.add_run(
        "This graph shows Simpson's 1/3 rule fitting parabolic arcs across triplets of points (n = 12 is even). "
        "Total computed thermal energy = 942,400.00 Joules (0.26178 kWh)."
    )

    s13_img = output_dir / "method_simpson13.png"
    if s13_img.exists():
        p_img = doc.add_paragraph()
        p_img.paragraph_format.space_before = Pt(4)
        p_img.paragraph_format.space_after = Pt(6)
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture(str(s13_img), width=Inches(5.4))

    # (c) Simpson 3/8
    p_s38_head = doc.add_paragraph()
    p_s38_head.paragraph_format.space_before = Pt(6)
    p_s38_head.paragraph_format.space_after = Pt(2)
    rs38 = p_s38_head.add_run("Method 3: Simpson's 3/8 Rule (Cubic Polynomials)")
    rs38.bold = True
    rs38.font.size = Pt(11)
    rs38.font.color.rgb = RGBColor(20, 40, 80)

    p_s38_desc = doc.add_paragraph()
    p_s38_desc.paragraph_format.space_before = Pt(2)
    p_s38_desc.paragraph_format.space_after = Pt(4)
    p_s38_desc.add_run(
        "This graph shows Simpson's 3/8 rule fitting degree-3 cubic curves across groups of 4 points (n = 12 is divisible by 3). "
        "Total computed thermal energy = 946,125.00 Joules (0.26281 kWh)."
    )

    s38_img = output_dir / "method_simpson38.png"
    if s38_img.exists():
        p_img = doc.add_paragraph()
        p_img.paragraph_format.space_before = Pt(4)
        p_img.paragraph_format.space_after = Pt(6)
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture(str(s38_img), width=Inches(5.4))

    # 3. Comparison Section (Table + Combined Graph)
    h3 = doc.add_paragraph()
    h3.paragraph_format.space_before = Pt(10)
    h3.paragraph_format.space_after = Pt(2)
    rh3 = h3.add_run("3. Side-by-Side Comparison of the Three Methods")
    rh3.bold = True
    rh3.font.size = Pt(12)
    rh3.font.color.rgb = RGBColor(30, 70, 140)

    p_comp_desc = doc.add_paragraph()
    p_comp_desc.paragraph_format.space_before = Pt(2)
    p_comp_desc.paragraph_format.space_after = Pt(4)
    p_comp_desc.paragraph_format.line_spacing = 1.15
    p_comp_desc.add_run(
        "Below is the side-by-side comparison table of all three numerical integration methods on the Kaggle BMW i3 dataset:"
    )

    # Comparison Table
    table = doc.add_table(rows=4, cols=5)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table)

    headers = ["Method", "Polynomial Order", "Formula Applied", "Thermal Energy (Joules)", "Energy (kWh)"]
    for i, t in enumerate(headers):
        c = table.rows[0].cells[i]
        c.text = t
        set_cell_background(c, "EAEFF8")
        set_cell_margins(c, 70, 70, 90, 90)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.bold = True
            r.font.size = Pt(9)
            r.font.color.rgb = RGBColor(20, 40, 80)

    rows_data = [
        ["Trapezoidal Rule", "Linear O(h²)", "h · [ P₀/2 + ∑ P_i + P_n/2 ]", "939,000.00 J", "0.26083 kWh"],
        ["Simpson's 1/3 Rule", "Quadratic O(h⁴)", "(h/3) · [ P₀ + 4∑ P_odd + 2∑ P_even + P_n ]", "942,400.00 J", "0.26178 kWh"],
        ["Simpson's 3/8 Rule", "Cubic O(h⁴)", "(3h/8) · [ P₀ + 3P₁ + 3P₂ + 2P₃ + ... + P_n ]", "946,125.00 J", "0.26281 kWh"]
    ]

    for row_idx, rvals in enumerate(rows_data, start=1):
        for col_idx, val in enumerate(rvals):
            c = table.rows[row_idx].cells[col_idx]
            c.text = val
            set_cell_background(c, "F9FAFB" if row_idx % 2 == 1 else "FFFFFF")
            set_cell_margins(c, 60, 60, 90, 90)
            p = c.paragraphs[0]
            if col_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                p.runs[0].bold = True
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.font.size = Pt(8.5)

    # Combined Overlay Comparison Graph
    comp_img = output_dir / "three_methods_comparison_overlay.png"
    if comp_img.exists():
        p_img = doc.add_paragraph()
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(6)
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.add_run().add_picture(str(comp_img), width=Inches(5.4))

    # Short easy conclusion matching sample style
    p_conc = doc.add_paragraph()
    p_conc.paragraph_format.space_before = Pt(6)
    p_conc.paragraph_format.space_after = Pt(6)
    p_conc.paragraph_format.line_spacing = 1.15
    p_conc.add_run("Short Observations & Conclusion:\n").bold = True
    p_conc.add_run(
        "• Trapezoidal (939,000 J) connects points with straight chords, slightly cutting beneath the peak warming phase (1800 W at t = 240s).\n"
        "• Simpson 1/3 (942,400 J) fits quadratic parabolas across triplets of points, capturing the rounded thermal rise and plateau smoothly.\n"
        "• Simpson 3/8 (946,125 J) fits cubic splines across groups of 4 points, capturing higher-order rate changes during initial heater startup.\n"
        "• All three methods converge very tightly around 0.261 kWh of total cabin heating energy consumed, proving the reliability of numerical integration for battery vehicle management."
    )

    doc_path = base_dir / "Assignment_9_RealTime_Dataset_Comparison.docx"
    doc.save(str(doc_path))
    print(f"Updated document successfully at: {doc_path}")

if __name__ == "__main__":
    build_doc()
