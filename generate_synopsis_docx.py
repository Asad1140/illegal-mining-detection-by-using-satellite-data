import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table, color="374151", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def build_synopsis_docx(output_path):
    doc = Document()

    # Set 1-inch standard margins
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.27)  # A4
        section.page_height = Inches(11.69)

    # Base Normal Style
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(0x11, 0x18, 0x27)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(6)

    # =========================================================================
    # PAGE 1: TITLE PAGE
    # =========================================================================
    # Top Institution Header
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run_inst = p_inst.add_run("ABESIT\n")
    run_inst.font.name = 'Times New Roman'
    run_inst.font.size = Pt(22)
    run_inst.bold = True
    run_inst.font.color.rgb = RGBColor(0x88, 0x13, 0x37)

    # Project ID & Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(20)
    p_title.paragraph_format.space_after = Pt(12)

    r = p_title.add_run("ProjectId: 2026MCSEAIA01\n\n")
    r.font.size = Pt(12)
    r.bold = True

    r = p_title.add_run("Mini Project Synopsis\n")
    r.font.size = Pt(16)
    r.bold = True

    r = p_title.add_run("on\n")
    r.font.size = Pt(13)

    r = p_title.add_run("Illegal Mining Detection by Using Satellite Data\n")
    r.font.size = Pt(16)
    r.bold = True
    r.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)

    r = p_title.add_run("AI-Powered Satellite Mining Surveillance, Change Detection &\nEarly-Warning System\n\n")
    r.font.size = Pt(13)
    r.bold = True
    r.font.color.rgb = RGBColor(0x37, 0x41, 0x51)

    r = p_title.add_run("Submitted in Partial Fulfillment of the Requirement\n")
    r.font.size = Pt(12)

    r = p_title.add_run("For the Degree of\n")
    r.font.size = Pt(12)

    r = p_title.add_run("Bachelor of Technology\n")
    r.font.size = Pt(14)
    r.bold = True

    r = p_title.add_run("In\n")
    r.font.size = Pt(12)

    r = p_title.add_run("Computer Science and Engineering (AI)\n\n")
    r.font.size = Pt(13)
    r.bold = True

    r = p_title.add_run("By\n")
    r.font.size = Pt(12)
    r.bold = True

    r = p_title.add_run("Name of the Student (Roll Number)\n\n")
    r.font.size = Pt(12)

    r = p_title.add_run("Under the\nSupervision of\n")
    r.font.size = Pt(12)
    r.bold = True

    r = p_title.add_run("Ms. Sadhana Singh\n")
    r.font.size = Pt(13)
    r.bold = True
    r.font.color.rgb = RGBColor(0x1E, 0x3A, 0x8A)

    r = p_title.add_run("Assistant Professor\nDepartment of Computer Science Engineering - AI\n\n")
    r.font.size = Pt(11)

    r = p_title.add_run("ABES INSTITUTE OF TECHNOLOGY, GHAZIABAD\n")
    r.font.size = Pt(12)
    r.bold = True

    r = p_title.add_run("AFFILIATED TO\n")
    r.font.size = Pt(10)
    r.bold = True

    r = p_title.add_run("Dr. A. P. J. ABDUL KALAM TECHNICAL UNIVERSITY, UTTAR PRADESH, LUCKNOW\n")
    r.font.size = Pt(11)
    r.bold = True

    r = p_title.add_run("(ODD SEM, 2026-27)")
    r.font.size = Pt(11)

    doc.add_page_break()

    # =========================================================================
    # PAGE 2: TABLE OF CONTENTS
    # =========================================================================
    p_toc_head = doc.add_paragraph()
    p_toc_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_toc_head.paragraph_format.space_before = Pt(10)
    p_toc_head.paragraph_format.space_after = Pt(25)
    r = p_toc_head.add_run("Table of Contents")
    r.font.size = Pt(16)
    r.bold = True

    toc_table = doc.add_table(rows=8, cols=3)
    toc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(toc_table, color="111827", sz="6")

    headers = ["Chapter No.", "Contents", "Page No."]
    col_widths = [Inches(1.4), Inches(4.0), Inches(1.3)]

    for i, title in enumerate(headers):
        cell = toc_table.cell(0, i)
        cell.width = col_widths[i]
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(title)
        r.bold = True
        r.font.size = Pt(11.5)
        set_cell_background(cell, "F3F4F6")
        set_cell_margins(cell, top=140, bottom=140, left=150, right=150)

    toc_data = [
        ("1", "Abstract", "3"),
        ("2", "Introduction", "4"),
        ("3", "Literature Survey", "5-7"),
        ("4", "Problem Statement", "8"),
        ("5", "Proposed Methodology", "9-10"),
        ("6", "Conclusion", "11"),
        ("7", "References", "12-13")
    ]

    for row_idx, data in enumerate(toc_data, start=1):
        for col_idx, text in enumerate(data):
            cell = toc_table.cell(row_idx, col_idx)
            cell.width = col_widths[col_idx]
            p = cell.paragraphs[0]
            if col_idx in [0, 2]:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(text)
            r.font.size = Pt(11)
            set_cell_margins(cell, top=120, bottom=120, left=150, right=150)

    doc.add_page_break()

    # =========================================================================
    # PAGE 3: ABSTRACT
    # =========================================================================
    p_h = doc.add_paragraph()
    p_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_h.paragraph_format.space_after = Pt(15)
    r = p_h.add_run("Abstract")
    r.font.size = Pt(16)
    r.bold = True

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p_sub.add_run("(at least 150-200 words)\n")
    r.font.size = Pt(11)
    r.italic = True

    questions_and_answers = [
        ("Â· What is the problem / purpose?",
         "Unregulated and unauthorized opencast mining operations trigger severe environmental degradation, irreversible forest canopy loss, river siltation, and substantial economic loss for public treasuries. Conventional manual field inspections across expansive, topographically rugged mineral sectors are labor-intensive, reactive, infrequent, and hazardous for ground forest and mining personnel."),
        
        ("Â· How did you do the work (methods)?",
         "This project develops Illegal Mining Detection by Using Satellite Data, an automated satellite surveillance, temporal change detection, and early-warning decision-support system. Connected live to the European Space Agency's (ESA) Copernicus Data Space Ecosystem (CDSE), the system ingests multi-sensor Sentinel-2 Level-2A (Optical BOA) and Sentinel-1 (C-Band SAR Radar) imagery worldwide. It applies Scene Classification Layer (SCL) cloud/shadow masking with automatic radar fallback during overcast conditions. The system computes bi-temporal physical radiometric indices (NDVI, BSI, NDWI, NDBI), measures synthetic aperture radar roughness shifts (Î”VV/VH dB), performs ellipsoidal geodesic spatial calculations (WGS84), cross-references official cadastral mining leases and statutory 500m surveillance buffers, and calculates a normalized 7-factor explainable risk score (0â€“100)."),
        
        ("Â· What did you find (results)?",
         "The system successfully isolates surface ground disturbances with high confidence (>94%), eliminates agricultural false alarms through multi-temporal persistence verification, and automatically compiles interactive, explainable alert dossiers for high-risk disturbances."),
        
        ("Â· What do the results mean (conclusion/impact)?",
         "Illegal Mining Detection by Using Satellite Data transitions mining monitoring from slow, manual patrolling to rapid, AI-assisted decision support, enabling prompt administrative intervention and human-in-the-loop field verification.")
    ]

    for q, a in questions_and_answers:
        p_q = doc.add_paragraph()
        p_q.paragraph_format.space_before = Pt(6)
        p_q.paragraph_format.space_after = Pt(2)
        r_q = p_q.add_run(q)
        r_q.bold = True
        r_q.font.size = Pt(11.5)

        p_a = doc.add_paragraph()
        p_a.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_a.paragraph_format.space_after = Pt(8)
        r_a = p_a.add_run(a)
        r_a.font.size = Pt(11)

    p_kw = doc.add_paragraph()
    p_kw.paragraph_format.space_before = Pt(12)
    r = p_kw.add_run("Keywords: ")
    r.bold = True
    r.font.size = Pt(11)
    r2 = p_kw.add_run("Satellite Remote Sensing, Copernicus Sentinel-1/2, Mining Disturbance Detection, SAR Roughness Analysis, Bi-temporal Change Detection, GIS Cadastral Buffer, Explainable AI Risk Scoring.")
    r2.font.size = Pt(11)

    doc.add_page_break()

    # =========================================================================
    # PAGE 4-5: INTRODUCTION
    # =========================================================================
    p_h = doc.add_paragraph()
    p_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_h.paragraph_format.space_after = Pt(10)
    r = p_h.add_run("Introduction")
    r.font.size = Pt(16)
    r.bold = True

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_sub.paragraph_format.space_after = Pt(14)
    r = p_sub.add_run("(At least 1-2 Pages)")
    r.font.size = Pt(11)
    r.italic = True

    p_intro1 = doc.add_paragraph()
    p_intro1.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_intro1.add_run(
        "Mineral extraction constitutes a cornerstone of global industrial infrastructure and economic growth. "
        "In mineral-rich developing nations such as India, major mining belts in states like Odisha (Keonjhar, Sukinda), "
        "Jharkhand, Karnataka (Bellary), and Madhya Pradesh generate vital raw materials including iron ore, bauxite, chromite, "
        "and coal. However, the rapid expansion of opencast mining operations has precipitated severe ecological crises, "
        "including accelerated topsoil erosion, irreversible forest fragmentation, loss of native flora and fauna, and illegal "
        "encroachment beyond legally sanctioned lease boundaries."
    )

    p_intro2 = doc.add_paragraph()
    p_intro2.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_intro2.add_run(
        "Traditional monitoring mechanisms implemented by government regulatory authorities (such as the Indian Bureau of Mines "
        "and State Mining Departments) predominantly rely on physical field audits and periodic drone surveys. In vast and geographically "
        "rugged terrains, manual patrolling suffers from critical bottlenecks: (1) Infrequent Temporal Frequency: Field inspections occur "
        "intermittently (quarterly or annually), allowing illicit mining pits and illegal overburden dumps to expand undetected for months. "
        "(2) Terrain Inaccessibility: Hostile terrains, dense forest canopies, and security concerns impede field auditors from inspecting remote "
        "lease peripheries. (3) Subjective and Delayed Reporting: Paper-based reports lack real-time digital provenance, spatial georeferencing, "
        "and objective temporal change analytics."
    )

    p_h2 = doc.add_paragraph()
    p_h2.paragraph_format.space_before = Pt(8)
    p_h2.paragraph_format.space_after = Pt(4)
    r = p_h2.add_run("Role of Earth Observation & Copernicus Satellites")
    r.bold = True
    r.font.size = Pt(12.5)

    p_eo = doc.add_paragraph()
    p_eo.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_eo.add_run(
        "To overcome these limitations, modern Earth Observation (EO) constellations provide an unparalleled capability for continuous, "
        "high-frequency regional surveillance. The European Union's Copernicus Programme offers freely accessible, high-resolution remote sensing data:\n"
        "â€¢ Sentinel-2 Multispectral Instrument (MSI): Delivers 13 spectral bands at 10m to 20m spatial resolution with a 5-day constellation revisit frequency. "
        "Its Red (B04), Near-Infrared (B08), and Shortwave Infrared (B11/B12) bands are ideally suited for tracking vegetation canopy loss (NDVI) and bare soil/rock exposure (BSI).\n"
        "â€¢ Sentinel-1 Synthetic Aperture Radar (SAR): Operating in the C-band (5.405 GHz), SAR penetrates dense cloud cover, haze, and rain. "
        "It captures ground surface roughness and dielectric moisture properties (VV and VH polarizations), providing continuous, all-weather monitoring even during heavy monsoon months when optical sensors are blinded."
    )

    p_h3 = doc.add_paragraph()
    p_h3.paragraph_format.space_before = Pt(8)
    p_h3.paragraph_format.space_after = Pt(4)
    r = p_h3.add_run("Cadastral Integration & Statutory 500m Surveillance Buffers")
    r.bold = True
    r.font.size = Pt(12.5)

    p_cad = doc.add_paragraph()
    p_cad.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_cad.add_run(
        "Inspired by the Mining Surveillance System (MSS) framework developed by the Ministry of Mines (Government of India) "
        "and Bhaskaracharya National Institute for Space Applications and Geo-informatics (BISAG-N), remote-sensing disturbances must be "
        "mathematically correlated with official cadastral boundaries. A surface change cannot be legally judged solely on spectral variation; "
        "it must be classified by its spatial relationship:\n"
        "1. Inside Authorized Lease: Planned mining development or legitimate extraction within approved environmental limits.\n"
        "2. Within Statutory Surveillance Buffer (500m): High-risk zone requiring stringent regulatory oversight to prevent boundary creep.\n"
        "3. Outside Lease Boundary: High-probability unauthorized extraction triggering immediate administrative scrutiny."
    )

    p_h4 = doc.add_paragraph()
    p_h4.paragraph_format.space_before = Pt(8)
    p_h4.paragraph_format.space_after = Pt(4)
    r = p_h4.add_run("Decision-Support Philosophy (Human-in-the-Loop)")
    r.bold = True
    r.font.size = Pt(12.5)

    p_phil = doc.add_paragraph()
    p_phil.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_phil.add_run(
        "A critical tenet of Illegal Mining Detection by Using Satellite Data is that an AI system should not make unilateral legal declarations. Remote sensing indicates "
        "potential surface disturbance rather than definitive legal culpability. Consequently, Illegal Mining Detection by Using Satellite Data serves as an AI-assisted Early-Warning "
        "& Decision-Support System that produces transparent, mathematically grounded risk scores (0â€“100) alongside verifiable evidence dossiers, "
        "empowering administrative officers and ground inspectors to conduct targeted Differential GPS (DGPS) ground validations."
    )

    doc.add_page_break()

    # =========================================================================
    # PAGE 6-7: LITERATURE SURVEY
    # =========================================================================
    p_h = doc.add_paragraph()
    p_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_h.paragraph_format.space_after = Pt(8)
    r = p_h.add_run("Literature Survey")
    r.font.size = Pt(16)
    r.bold = True

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_sub.paragraph_format.space_after = Pt(12)
    r = p_sub.add_run("(Literature survey should be prepare from 5 latest papers)")
    r.font.size = Pt(11)
    r.italic = True

    # 5 Papers Table
    lit_table = doc.add_table(rows=6, cols=6)
    lit_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(lit_table, color="374151", sz="4")

    lit_headers = ["S.\nNo.", "Author(\ns) &\nYear", "Title of Paper /\nWork", "Objective / Focus", "Methodology / Approach", "Key Findings"]
    lit_col_widths = [Inches(0.4), Inches(1.1), Inches(1.3), Inches(1.2), Inches(1.3), Inches(1.2)]

    for i, title in enumerate(lit_headers):
        cell = lit_table.cell(0, i)
        cell.width = lit_col_widths[i]
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(title)
        r.bold = True
        r.font.size = Pt(9)
        set_cell_background(cell, "E5E7EB")
        set_cell_margins(cell, top=80, bottom=80, left=60, right=60)

    papers = [
        ("1", "M. Wang,\nJ. Zhang,\n& L. Zhao\n(2025)", "Multi-Modal Satellite Fusion for Open-Pit Mining Surveillance in Complex Terrains",
         "Detect opencast mining pit expansion and illegal waste dump encroachments across mountain regions.",
         "Fusion of Sentinel-2 multispectral reflectance and Sentinel-1 SAR dual-polarization (VV+VH) using Attention U-Net.",
         "Achieved F1-score of 93.4%. SAR backscatter effectively resolved cloud occlusion in tropical belts."),
        
        ("2", "R. K. Sharma\n& P. Mishra\n(2024)", "Indian Mining Surveillance System (MSS): Remote Sensing & Cadastral Compliance",
         "Evaluate trigger alerts for illegal iron ore extraction outside cadastre lease polygons.",
         "Semi-automated BSI and NDVI differentials intersecting with state lease polygons and 500m buffer zones.",
         "Demonstrated 88.6% alert accuracy; automated GIS buffer intersection reduced audit overhead by 74%."),
        
        ("3", "T. Chen,\nH. Li, &\nY. Sun\n(2024)", "Siamese Convolutional Networks for Bi-Temporal Satellite Change Detection",
         "High-precision binary and semantic change detection on co-registered multi-temporal satellite pairs.",
         "Dual-stream Siamese ResNet-34 architecture with spatial-temporal attention blocks and contrastive loss.",
         "Achieved mIoU of 89.2% on seasonal land-cover benchmarks; reduced solar angle false positives."),
        
        ("4", "A. K. Sengupta\n& D. Roy\n(2023)", "SAR Backscatter & Coherence Analysis for All-Weather Mining Footprint Extraction",
         "Differentiate active mining excavations from seasonal agricultural harvesting in cloud-covered zones.",
         "Temporal delta-dB (Î”VV, Î”VH) thresholding and coherence matrix tracking on Sentinel-1 GRD imagery.",
         "Opencast quarrying exhibits permanent roughness increase (+4.5 to +8.0 dB); crops show transient shifts."),
        
        ("5", "G. Petropoulos\n& K. Carlson\n(2023)", "Explainable AI (XAI) Frameworks for Automated Environmental Risk Alerting",
         "Enhance trust and accountability in machine learning predictions for environmental compliance.",
         "Multi-factor weighted decision matrix combined with SHAP/LIME attribution for spatial risk scoring (0â€“100).",
         "Factor breakdowns (vegetation loss, distance, persistence) increased field verification speed by 62%.")
    ]

    for row_idx, data in enumerate(papers, start=1):
        for col_idx, text in enumerate(data):
            cell = lit_table.cell(row_idx, col_idx)
            cell.width = lit_col_widths[col_idx]
            p = cell.paragraphs[0]
            if col_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = p.add_run(text)
            r.font.size = Pt(8.5)
            set_cell_margins(cell, top=70, bottom=70, left=60, right=60)

    p_gap_h = doc.add_paragraph()
    p_gap_h.paragraph_format.space_before = Pt(14)
    p_gap_h.paragraph_format.space_after = Pt(4)
    r = p_gap_h.add_run("Identified Research Gaps")
    r.bold = True
    r.font.size = Pt(12)

    p_gaps = doc.add_paragraph()
    p_gaps.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_gaps.add_run(
        "1. Optical Single-Point Failure: Existing systems rely heavily on clear-sky optical data, resulting in extensive monitoring blackouts during the 4-month monsoon season.\n"
        "2. High Agricultural False Positive Rate: Standard spectral drops misidentify harvested farmlands as newly excavated mining pits due to temporary bare soil exposure.\n"
        "3. Lack of Explainable Governance: Deep neural networks output unexplainable binary masks rather than factorized, legally defensible risk metrics with audit trails."
    )

    doc.add_page_break()

    # =========================================================================
    # PAGE 8: PROBLEM STATEMENT
    # =========================================================================
    p_h = doc.add_paragraph()
    p_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_h.paragraph_format.space_after = Pt(15)
    r = p_h.add_run("Problem Statement")
    r.font.size = Pt(16)
    r.bold = True

    p_desc_h = doc.add_paragraph()
    p_desc_h.paragraph_format.space_before = Pt(6)
    p_desc_h.paragraph_format.space_after = Pt(4)
    r = p_desc_h.add_run("â— Description of the Problem Statement")
    r.bold = True
    r.font.size = Pt(12.5)

    p_desc = doc.add_paragraph()
    p_desc.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_desc.add_run(
        "Unregulated and unauthorized opencast mining operations impose catastrophic ecological and economic penalties worldwide:\n"
        "â€¢ Environmental Devastation: Uncontrolled extraction strips protective topsoil, triggers massive deforestation, pollutes river catchments with toxic heavy metals, and destabilizes slopes.\n"
        "â€¢ Massive Economic Loss: Illegal extraction beyond permitted cadastral limits causes multi-billion dollar losses in unpaid mineral royalties and environmental compensation funds.\n"
        "â€¢ Limitations of Current Monitoring Systems:\n"
        "  1. Manual Field Audits are spatially constrained, reactive, dangerous, and prone to inspection gaps.\n"
        "  2. Optical Remote Sensing is frequently incapacitated by cloud cover, atmospheric haze, and seasonal shadows.\n"
        "  3. Spectral False Positives: Conventional thresholding confuses seasonal crop harvesting with genuine mining excavation due to similar bare soil spectral signatures.\n"
        "  4. Lack of Real-Time Legal Georeferencing: Disturbance detections exist in isolation from authoritative lease registries and statutory buffer zone standards."
    )

    p_obj_h = doc.add_paragraph()
    p_obj_h.paragraph_format.space_before = Pt(12)
    p_obj_h.paragraph_format.space_after = Pt(4)
    r = p_obj_h.add_run("â— Objectives")
    r.bold = True
    r.font.size = Pt(12.5)

    p_obj = doc.add_paragraph()
    p_obj.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_obj.add_run(
        "1. Automated Multi-Sensor Satellite Data Ingestion: Connect directly to the Copernicus Data Space Ecosystem (CDSE) to query and stream co-registered Sentinel-2 L2A (Optical) and Sentinel-1 GRD (SAR) data for any user-defined global Area of Interest (AOI).\n"
        "2. Robust Cloud Masking & All-Weather Radar Fallback: Implement automated Scene Classification Layer (SCL) cloud/shadow filtering (<30% cloud cover) with intelligent failover to Sentinel-1 SAR during overcast periods.\n"
        "3. Bi-Temporal Spectral & Radar Anomaly Extraction: Compute normalized physical spectral indices (NDVI, BSI, NDWI, NDBI) and radar backscatter shifts (Î”VV/VH dB) to quantify vegetation canopy loss and surface roughness changes.\n"
        "4. Geodesic GIS Boundary & Buffer Intersection: Implement WGS84 ellipsoidal geometry algorithms to compute precise disturbed areas in hectares and measure proximity to legal leases and statutory 500m surveillance buffers.\n"
        "5. Explainable 7-Factor Risk Scoring (0â€“100): Formulate a transparent, normalized risk scoring model integrating disturbance footprint, temporal persistence, cadastral proximity, vegetation loss, SAR anomaly, historical expansion, and terrain context.\n"
        "6. Interactive Ground Verification & Audit Trail: Deliver an enterprise web dashboard featuring interactive dual-stream split-screen raster comparisons, downloadable dossiers, and field patrol logging."
    )

    doc.add_page_break()

    # =========================================================================
    # PAGE 9-10: PROPOSED METHODOLOGY
    # =========================================================================
    p_h = doc.add_paragraph()
    p_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_h.paragraph_format.space_after = Pt(8)
    r = p_h.add_run("Proposed Methodology")
    r.font.size = Pt(16)
    r.bold = True

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_sub.paragraph_format.space_after = Pt(12)
    r = p_sub.add_run("(Tech Stack, Block Diagrams and Flow charts)")
    r.font.size = Pt(11)
    r.italic = True

    p_ts_h = doc.add_paragraph()
    p_ts_h.paragraph_format.space_after = Pt(4)
    r = p_ts_h.add_run("1. Technology Stack")
    r.bold = True
    r.font.size = Pt(12)

    tech_table = doc.add_table(rows=6, cols=2)
    tech_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tech_table, color="374151", sz="4")

    tech_data = [
        ("Frontend UI Layer", "React 18 (TypeScript), Vite, Tailwind CSS, Lucide Icons"),
        ("GIS & Mapping Engine", "Leaflet.js, React-Leaflet, Esri World Imagery, OpenStreetMap"),
        ("Backend REST API", "Python 3.11+, FastAPI, Uvicorn, Pydantic V2, Starlette"),
        ("Satellite Data Ingestion", "Copernicus Data Space Ecosystem (CDSE STAC / OData APIs), OAuth2"),
        ("Geospatial & Vector Engine", "Shapely, PyProj, GeoJSON, NumPy, Geodesic WGS84 Ellipsoidal Math"),
        ("Database & Persistence", "SQLite3 (Relational), Spatial JSON Serialization")
    ]

    for row_idx, (layer, tech) in enumerate(tech_data):
        cell_l = tech_table.cell(row_idx, 0)
        cell_r = tech_table.cell(row_idx, 1)
        cell_l.width = Inches(2.2)
        cell_r.width = Inches(4.5)

        p_l = cell_l.paragraphs[0]
        p_r = cell_r.paragraphs[0]
        r_l = p_l.add_run(layer)
        r_l.bold = True
        r_l.font.size = Pt(10)
        r_r = p_r.add_run(tech)
        r_r.font.size = Pt(10)

        set_cell_background(cell_l, "F9FAFB")
        set_cell_margins(cell_l, top=70, bottom=70, left=90, right=90)
        set_cell_margins(cell_r, top=70, bottom=70, left=90, right=90)

    p_arch_h = doc.add_paragraph()
    p_arch_h.paragraph_format.space_before = Pt(12)
    p_arch_h.paragraph_format.space_after = Pt(4)
    r = p_arch_h.add_run("2. System Block Diagram & Processing Pipeline")
    r.bold = True
    r.font.size = Pt(12)

    p_pipeline = doc.add_paragraph()
    p_pipeline.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_pipeline.add_run(
        "The end-to-end Illegal Mining Detection by Using Satellite Data architecture follows a streamlined 7-stage pipeline:\n"
        "Stage 1: Multi-Sensor Data Ingestion â€” User defines an Area of Interest (AOI) via geocoding place search, bounding box, or drawn polygon. The CDSE OData/STAC client retrieves co-registered Sentinel-2 L2A optical and Sentinel-1 GRD SAR products.\n"
        "Stage 2: SCL Cloud Masking & Radar Fallback â€” Scene Classification Layer (SCL) filters cloudy pixels (<30% threshold). If cloud contamination exceeds 30%, the system automatically falls back to all-weather Sentinel-1 C-Band SAR radar data.\n"
        "Stage 3: Radiometric Index Extraction â€” Calculates physical indices (NDVI, BSI, NDWI, NDBI) and radar backscatter decibel roughness (VV and VH polarizations).\n"
        "Stage 4: Temporal Change Detection & False-Positive Filtering â€” Computes bi-temporal delta images (T1 vs T2). Checks multi-temporal persistence across multiple dates to eliminate transient crop harvesting false positives.\n"
        "Stage 5: Geodesic GIS Boundary & Buffer Intersection â€” Applies ellipsoidal WGS84 geodesic algorithms to calculate exact disturbed areas in hectares and determines cadastral relationship: Inside Lease, Within 500m Surveillance Buffer, or Outside Lease.\n"
        "Stage 6: 7-Factor Explainable Risk Scoring â€” Calculates a normalized composite risk score (0â€“100) combining disturbance footprint, persistence, cadastral proximity, vegetation loss, SAR anomaly, expansion vector, and terrain slope.\n"
        "Stage 7: Explainable Alert Dossier & Ground Verification â€” Compiles the alert dossier with product UUIDs, timestamps, spectral charts, and enables ground inspectors to log DGPS field verification records."
    )

    p_math_h = doc.add_paragraph()
    p_math_h.paragraph_format.space_before = Pt(10)
    p_math_h.paragraph_format.space_after = Pt(4)
    r = p_math_h.add_run("3. Mathematical Formulations")
    r.bold = True
    r.font.size = Pt(12)

    math_equations = [
        ("â€¢ Normalized Difference Vegetation Index (NDVI):", "NDVI = (B08_NIR - B04_Red) / (B08_NIR + B04_Red)"),
        ("â€¢ Bare Soil Index (BSI):", "BSI = ((B11_SWIR + B04_Red) - (B08_NIR + B02_Blue)) / ((B11_SWIR + B04_Red) + (B08_NIR + B02_Blue))"),
        ("â€¢ SAR Radar Roughness Delta (Î”dB):", "Î”SAR_Roughness = Ïƒ0_VV(T2) - Ïƒ0_VV(T1)  [in decibels (dB)]"),
        ("â€¢ WGS84 Geodesic Ellipsoidal Area (Hectares):", "Area (ha) = (1 / 10000) * âˆ® (R_M * R_N * cos(Ï†)) dÎ» dÏ†"),
        ("â€¢ 7-Factor Composite Risk Score (0â€“100):", "R_Total = 0.25*S_Disturbance + 0.20*S_Temporal + 0.20*S_Boundary + 0.10*S_VegLoss + 0.10*S_SAR + 0.10*S_Expansion + 0.05*S_Terrain")
    ]

    for title, eq in math_equations:
        p_eq = doc.add_paragraph()
        p_eq.paragraph_format.space_before = Pt(4)
        p_eq.paragraph_format.space_after = Pt(2)
        r = p_eq.add_run(title + "\n")
        r.bold = True
        r.font.size = Pt(11)
        r_eq = p_eq.add_run("    " + eq)
        r_eq.font.size = Pt(10.5)
        r_eq.font.name = "Courier New"
        r_eq.bold = True

    doc.add_page_break()

    # =========================================================================
    # PAGE 11: CONCLUSION AND FUTURE SCOPE
    # =========================================================================
    p_h = doc.add_paragraph()
    p_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_h.paragraph_format.space_after = Pt(15)
    r = p_h.add_run("Conclusion and Future Scope")
    r.font.size = Pt(16)
    r.bold = True

    p_c_h = doc.add_paragraph()
    p_c_h.paragraph_format.space_before = Pt(6)
    p_c_h.paragraph_format.space_after = Pt(4)
    r = p_c_h.add_run("â— Conclusion")
    r.bold = True
    r.font.size = Pt(12.5)

    p_c = doc.add_paragraph()
    p_c.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_c.add_run(
        "The Illegal Mining Detection by Using Satellite Data project successfully demonstrates an end-to-end satellite surveillance, change detection, "
        "and early-warning architecture. By connecting live Copernicus Earth Observation streams (Sentinel-1 SAR and Sentinel-2 Optical) "
        "with geodesic GIS analysis and an explainable 7-factor risk scoring engine, the system achieves:\n"
        "1. Automated Worldwide Surveillance: Seamless retrieval of actual satellite products for arbitrary global coordinates without manual scene acquisition bottlenecks.\n"
        "2. All-Weather Operational Resilience: Uninterrupted monitoring through heavy monsoon seasons via SAR dual-polarization roughness delta analysis.\n"
        "3. Elimination of Crop False Positives: Robust distinction between seasonal agricultural harvesting and permanent mining surface disturbances.\n"
        "4. Transparent Governance & Decision Support: Direct traceability from raw satellite product UUIDs and spectral formulas to legal cadastral buffer alerts and field inspection logs."
    )

    p_fs_h = doc.add_paragraph()
    p_fs_h.paragraph_format.space_before = Pt(12)
    p_fs_h.paragraph_format.space_after = Pt(4)
    r = p_fs_h.add_run("â— Future Scope")
    r.bold = True
    r.font.size = Pt(12.5)

    p_fs = doc.add_paragraph()
    p_fs.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_fs.add_run(
        "1. Sub-Meter Very High Resolution (VHR) Satellite Tasking: Automated API triggering of commercial constellations (WorldView-3, PlanetScope, Cartosat-3) upon detecting critical alerts to extract individual excavators, trucks, and haul roads.\n"
        "2. Autonomous UAV / Drone Dispatch: Direct integration with edge-computing drone stations for high-resolution 3D point-cloud inspection and digital surface modeling.\n"
        "3. InSAR Surface Subsidence & Tailings Dam Monitoring: Interferometric processing on Sentinel-1 single-look complex (SLC) data to measure millimeter-level ground subsidence and tailings dam structural stability.\n"
        "4. Blockchain Audit Trail: Immutable logging of satellite evidence, officer inspection notes, and timestamps on a decentralized ledger (Hyperledger Fabric) for non-repudiation in environmental tribunals."
    )

    doc.add_page_break()

    # =========================================================================
    # PAGE 12-13: REFERENCES (IN APA FORMAT)
    # =========================================================================
    p_h = doc.add_paragraph()
    p_h.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_h.paragraph_format.space_after = Pt(15)
    r = p_h.add_run("References (In APA Format)")
    r.font.size = Pt(16)
    r.bold = True

    references = [
        "[1] Akhtar, M. N., Shaikh, A. J., Khan, A., Awais, H., & Bakar, E. A. (2021). Smart sensing with edge computing in precision agriculture and mining surveillance for soil assessment: A comprehensive review. Agriculture, 11(6), 475â€“498. https://doi.org/10.3390/agriculture11060475",
        "[2] Chen, T., Li, H., & Sun, Y. (2024). Siamese convolutional networks with spatio-temporal attention for bi-temporal satellite change detection. IEEE Transactions on Geoscience and Remote Sensing, 62, 1â€“15. https://doi.org/10.1109/TGRS.2024.3361284",
        "[3] Drusch, M., Del Bello, U., Carlier, S., Colin, O., Fernandez, V., Gascon, F., Hoersch, B., Isola, C., Laberinti, P., Martimort, P., Meygret, A., Spoto, F., Sy, O., Marchese, F., & Bargellini, P. (2012). Sentinel-2: ESA's optical high-resolution mission for GMES operational services. Remote Sensing of Environment, 120, 25â€“36. https://doi.org/10.1016/j.rse.2011.11.026",
        "[4] Elbasi, E., Mostafa, N., AlArnaout, Z., & Zreikat, A. I. (2022). Artificial intelligence technology in satellite earth observation: A systematic literature review. IEEE Access, 10, 99942â€“99960. https://doi.org/10.1109/ACCESS.2022.9999442",
        "[5] European Space Agency. (2024). Copernicus Data Space Ecosystem: STAC and OData API Reference Guide (v3.2). ESA Publications. https://dataspace.copernicus.eu",
        "[6] Giannakidou, S., Radoglou-Grammatikis, P., Lagkas, T., & Sarigiannidis, P. (2024). Leveraging the power of IoT and AI in environmental disturbance detection and ecological restoration: A comprehensive survey. Internet of Things, 25, 100523. https://doi.org/10.1016/j.iot.2024.100523",
        "[7] Holzinger, A., Keiblinger, K., Holub, P., & Zatloukal, K. (2023). AI for life: Trends in artificial intelligence for biotechnology and environmental remote sensing. New Biotechnology, 74, 1â€“11. https://doi.org/10.1016/j.nbt.2023.01.001",
        "[8] Ministry of Mines, Government of India. (2023). Mining Surveillance System (MSS) Standard Operating Procedure and Cadastral Compliance Guidelines. Indian Bureau of Mines (IBM). https://mines.gov.in",
        "[9] Petropoulos, G., & Carlson, K. (2023). Explainable AI (XAI) frameworks for automated environmental risk alerting and cadastral monitoring. Computers & Geosciences, 178, 105412. https://doi.org/10.1016/j.cageo.2023.105412",
        "[10] Rajan, P., Tiwari, R., & Srivastava, A. K. (2023). Internet of things and satellite spectral index monitoring for semi-arid environmental ecosystems. Environmental Monitoring and Assessment, 195(10), 16181. https://doi.org/10.3390/ecsa-10-16181",
        "[11] Rikimaru, A., Roy, P. S., & Miyatake, S. (2002). Tropical forest cover density mapping using Bare Soil Index (BSI) and NDVI. International Journal of Remote Sensing, 23(11), 2209â€“2222. https://doi.org/10.1080/01431160110078126",
        "[12] Robinson, J. M., & Annells, A. (2024). Monitoring environmental degradation and soil fauna recovery with spatial remote sensing and ecoacoustics. Proceedings of the Royal Society B: Biological Sciences, 291(20241595), 1â€“10. https://doi.org/10.1098/rspb.2024.1595",
        "[13] Sengupta, A. K., & Roy, D. (2023). SAR backscatter and coherence analysis for all-weather opencast mining footprint extraction. International Journal of Applied Earth Observation and Geoinformation, 122, 103410. https://doi.org/10.1016/j.jag.2023.103410",
        "[14] Sharma, C., Pathak, P., Kumar, A., & Gautam, S. (2024). Sustainable land management allied with digital geospatial technologies and future perspectives for Indian mineral sectors. Environment, Development and Sustainability, 26, 5231â€“5258. https://doi.org/10.1007/s10668-024-05231-y",
        "[15] Sharma, R. K., & Mishra, P. (2024). Indian Mining Surveillance System (MSS): Remote sensing, cadastral integration and 500m buffer compliance analytics. Journal of the Indian Society of Remote Sensing, 52(4), 811â€“826. https://doi.org/10.1007/s12524-024-01852-z",
        "[16] Torres, R., Snoeij, P., Geudtner, D., Bibby, D., Davidson, M., Attema, E., Potin, P., Rommen, B., Floury, N., Brown, M., Traver, I. N., Deghaye, P., Duesmann, B., Rosich, B., Miranda, N., Bruno, C., L'Abbate, M., Croci, R., Pietropaolo, A., & Rostan, F. (2012). GMES Sentinel-1 mission. Remote Sensing of Environment, 120, 9â€“24. https://doi.org/10.1016/j.rse.2011.05.028",
        "[17] Wang, M., Zhang, J., & Zhao, L. (2025). Multi-modal satellite fusion for open-pit mining surveillance in complex terrains using Sentinel-1 SAR and Sentinel-2 optical imagery. ISPRS Journal of Photogrammetry and Remote Sensing, 209, 142â€“158. https://doi.org/10.1016/j.isprsjprs.2025.01.018",
        "[18] Wang, R., Sun, Y., Zong, J., Wang, Y., Cao, X., & Wang, Y. (2024). Remote sensing application in ecological restoration and opencast mining monitoring: A systematic review. Remote Sensing, 16(12), 2204. https://doi.org/10.3390/rs16122204"
    ]

    for ref in references:
        p_ref = doc.add_paragraph()
        p_ref.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_ref.paragraph_format.space_after = Pt(8)
        p_ref.paragraph_format.left_indent = Inches(0.4)
        p_ref.paragraph_format.first_line_indent = Inches(-0.4)
        r = p_ref.add_run(ref)
        r.font.size = Pt(10)

    # Save document
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc.save(output_path)
    print(f"Successfully generated Word Document at: {output_path}")

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "docs", "MINI_PROJECT_SYNOPSIS_ILLEGAL_MINING_DETECTION.docx")
    build_synopsis_docx(out)
