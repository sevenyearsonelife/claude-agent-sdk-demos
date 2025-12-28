#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
勾股定理可视化证明方法综合研究报告生成器
Pythagorean Theorem Visual Proofs Comprehensive Research Report Generator
"""

import os
from datetime import datetime
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 设置中文字体支持 - 使用系统自带的中文字体
def setup_chinese_font():
    """设置中文字体"""
    try:
        # macOS 系统自带中文字体
        font_path = "/System/Library/Fonts/PingFang.ttc"
        if os.path.exists(font_path):
            pdfmetrics.registerFont(TTFont('ChineseFont', font_path))
            return 'ChineseFont'
    except:
        pass

    # 如果无法注册中文字体，使用Helvetica（中文可能显示为方块）
    return 'Helvetica'

# 创建输出目录
os.makedirs('files/reports', exist_ok=True)

# 获取当前日期
current_date = datetime.now()
date_str = current_date.strftime("%Y%m%d")
year_str = str(current_date.year)

# 输出文件路径
output_file = f"files/reports/pythagorean_theorem_visual_proofs_report_{date_str}.pdf"

# 创建PDF文档
doc = SimpleDocTemplate(
    output_file,
    pagesize=A4,
    rightMargin=72,
    leftMargin=72,
    topMargin=72,
    bottomMargin=72
)

# 设置字体
chinese_font = setup_chinese_font()

# 获取样式并创建自定义样式
styles = getSampleStyleSheet()

# 创建标题样式
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Title'],
    fontName=chinese_font,
    fontSize=20,
    alignment=TA_CENTER,
    spaceAfter=30,
    textColor=colors.darkblue
)

# 创建副标题样式
subtitle_style = ParagraphStyle(
    'CustomSubtitle',
    parent=styles['Heading2'],
    fontName=chinese_font,
    fontSize=14,
    alignment=TA_CENTER,
    spaceAfter=20,
    textColor=colors.darkgray
)

# 创建一级标题样式
heading1_style = ParagraphStyle(
    'CustomHeading1',
    parent=styles['Heading1'],
    fontName=chinese_font,
    fontSize=16,
    spaceAfter=12,
    spaceBefore=20,
    textColor=colors.darkblue,
    keepWithNext=True
)

# 创建二级标题样式
heading2_style = ParagraphStyle(
    'CustomHeading2',
    parent=styles['Heading2'],
    fontName=chinese_font,
    fontSize=14,
    spaceAfter=10,
    spaceBefore=15,
    textColor=colors.darkblue
)

# 创建三级标题样式
heading3_style = ParagraphStyle(
    'CustomHeading3',
    parent=styles['Heading3'],
    fontName=chinese_font,
    fontSize=12,
    spaceAfter=8,
    spaceBefore=10,
    textColor=colors.darkblue
)

# 创建正文样式
body_style = ParagraphStyle(
    'CustomBody',
    parent=styles['BodyText'],
    fontName=chinese_font,
    fontSize=10,
    leading=14,
    alignment=TA_JUSTIFY,
    spaceAfter=6
)

# 创建居中正文样式
center_body_style = ParagraphStyle(
    'CustomCenterBody',
    parent=body_style,
    alignment=TA_CENTER
)

# 创建引用样式
quote_style = ParagraphStyle(
    'CustomQuote',
    parent=body_style,
    leftIndent=20,
    rightIndent=20,
    textColor=colors.darkgray,
    backColor=colors.lightgrey
)

# 存储所有内容
story = []

# ============================================================================
# 封面页
# ============================================================================

story.append(Spacer(1, 1.5*inch))
story.append(Paragraph("勾股定理可视化证明方法综合研究报告", title_style))
story.append(Spacer(1, 0.3*inch))
story.append(Paragraph("Pythagorean Theorem Visual Proofs:", subtitle_style))
story.append(Paragraph("A Comprehensive Research Report", subtitle_style))
story.append(Spacer(1, 1*inch))
story.append(Paragraph(f"报告日期 / Report Date: {current_date.strftime('%Y年%m月%d日')}", body_style))
story.append(Spacer(1, 0.5*inch))
story.append(Paragraph("基于4份研究笔记、数据摘要及可视化图表的综合分析", body_style))
story.append(PageBreak())

# ============================================================================
# 目录页
# ============================================================================

story.append(Paragraph("目录 / Table of Contents", heading1_style))
story.append(Spacer(1, 0.2*inch))

toc_data = [
    ["1. 执行摘要", "3"],
    ["2. 勾股定理的五种可视化证明方法详解", "4"],
    ["3. 历史发展与文化背景", "6"],
    ["4. 现代可视化技术应用", "8"],
    ["5. 教育应用与效果分析", "10"],
    ["6. 数据可视化图表", "12"],
    ["7. 结论与建议", "13"],
    ["8. 参考文献", "14"]
]

toc_table = Table(toc_data, colWidths=[5*inch, 1*inch])
toc_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), chinese_font),
    ('FONTSIZE', (0, 0), (-1, -1), 11),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('LEFTPADDING', (0, 0), (0, -1), 20),
    ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
    ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
]))

story.append(toc_table)
story.append(PageBreak())

# ============================================================================
# 1. 执行摘要
# ============================================================================

story.append(Paragraph("1. 执行摘要 / Executive Summary", heading1_style))
story.append(Spacer(1, 0.15*inch))

story.append(Paragraph("本报告综合分析了勾股定理可视化证明方法的历史发展、教育应用效果和现代技术趋势。研究基于跨越约4000年的历史文献（公元前1900年至2025年）和涵盖15,000+名学生的现代教育研究数据。", body_style))

story.append(Spacer(1, 0.1*inch))

# 核心发现表格
story.append(Paragraph("核心发现 / Key Findings:", heading2_style))

key_findings_data = [
    ["发现项", "关键数据", "来源"],
    ["证明方法总数", "约400种", "Loomis 1940"],
    ["历史时间跨度", "约4000年", "多来源综合"],
    ["可视化教学效应值", "g = 0.504 (中等效应)", "41项研究元分析"],
    ["GeoGebra效应值", "g = 1.321 (超大效应)", "14项研究元分析"],
    ["AR几何学习效应值", "g = 0.99 (大效应)", "Cao 2023元分析"],
    ["知识保留率 (VR)", "75% vs 5% (传统讲座)", "National Training Lab"],
    ["学生高学习兴趣", "69.41%", "GeoGebra研究"],
    ["教育技术市场 (2029年预测)", "3952亿美元", "市场研究报告"],
    ["AR/VR教育市场 (2033年预测)", "750亿美元", "BCC Research 2024"]
]

key_findings_table = Table(key_findings_data, colWidths=[2.5*inch, 2*inch, 1.5*inch], repeatRows=1)
key_findings_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), chinese_font),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
]))

story.append(key_findings_table)
story.append(Spacer(1, 0.15*inch))

story.append(Paragraph("研究显示，可视化证明方法显著提升学生对勾股定理的理解和记忆。赵爽弦图证明法（公元3世纪）被80%的学生认为最直观，而现代动态几何软件如GeoGebra使课堂参与度从40%提升至75%。VR/AR技术的知识保留率是传统讲座的15倍（75% vs 5%）。", body_style))

story.append(PageBreak())

# ============================================================================
# 2. 勾股定理的五种可视化证明方法详解
# ============================================================================

story.append(Paragraph("2. 勾股定理的五种可视化证明方法详解 / Five Visual Proof Methods", heading1_style))
story.append(Spacer(1, 0.15*inch))

# 方法一：赵爽弦图
story.append(Paragraph("2.1 赵爽弦图证明法 (公元3世纪)", heading2_style))
story.append(Paragraph("<b>发明者：</b>赵爽（三国时期吴国数学家）", body_style))
story.append(Paragraph("<b>文献来源：</b>《周髀算经注》中的"勾股圆方图说"（约公元222年）", body_style))
story.append(Paragraph("<b>历史意义：</b>2002年第24届国际数学家大会会标采用赵爽弦图；比印度数学家婆什迦罗的类似证明早800多年", body_style))

story.append(Spacer(1, 0.1*inch))
story.append(Paragraph("<b>证明逻辑：</b>", heading3_style))
story.append(Paragraph("大正方形面积 = 4个三角形面积 + 中间小正方形面积", body_style))
story.append(Paragraph("c² = 4 × (1/2 × a × b) + (b - a)²", quote_style))
story.append(Paragraph("c² = 2ab + b² - 2ab + a² = a² + b²", quote_style))

story.append(Spacer(1, 0.1*inch))
story.append(Paragraph("<b>核心特点：</b>", heading3_style))
story.append(Paragraph("• 使用"出入相补"原理，体现中国古代形数结合思想", body_style))
story.append(Paragraph("• 80%的学生对此方法印象深刻", body_style))
story.append(Paragraph("• 直观性：★★★★★", body_style))
story.append(Paragraph("• 复杂度：★★☆☆☆", body_style))

story.append(Spacer(1, 0.2*inch))

# 方法二：毕达哥拉斯拼图
story.append(Paragraph("2.2 毕达哥拉斯拼图证明法 (公元前6世纪)", heading2_style))
story.append(Paragraph("<b>发明者：</b>毕达哥拉斯（Pythagoras，约公元前570-495年）", body_style))
story.append(Paragraph("<b>传说：</b>据说发现定理后宰杀百头牛庆祝（故称"百牛定理"）", body_style))
story.append(Paragraph("<b>特殊性：</b>原始证明方法已失传，现代版本是根据后人推测复原", body_style))

story.append(Spacer(1, 0.1*inch))
story.append(Paragraph("<b>证明逻辑：</b>", heading3_style))
story.append(Paragraph("通过重新排列图形中的三角形部分，保持总面积不变", body_style))
story.append(Paragraph("(a + b)² = c² + 2ab", quote_style))
story.append(Paragraph("a² + 2ab + b² = c² + 2ab", quote_style))
story.append(Paragraph("a² + b² = c²", quote_style))

story.append(Spacer(1, 0.1*inch))
story.append(Paragraph("<b>教育应用：</b>", heading3_style))
story.append(Paragraph("• 适合动画演示，现代有多个GIF动画版本", body_style))
story.append(Paragraph("• 维基百科提供动画版本", body_style))
story.append(Paragraph("• plus.maths.org提供交互式可视化", body_style))

story.append(Spacer(1, 0.2*inch))

# 方法三：欧几里得几何
story.append(Paragraph("2.3 欧几里得几何证明法 (公元前4世纪)", heading2_style))
story.append(Paragraph("<b>发明者：</b>欧几里得（Euclid，约公元前330-275年）", body_style))
story.append(Paragraph("<b>文献来源：</b>《几何原本》第一卷命题47（Book I, Proposition 47）", body_style))
story.append(Paragraph("<b>重要性：</b>这是《几何原本》第一卷的压轴命题，被称为该书的"高潮"", body_style))

story.append(Spacer(1, 0.1*inch))
story.append(Paragraph("<b>证明逻辑：</b>", heading3_style))
story.append(Paragraph("通过将两个直角边上的正方形转换为斜边正方形内的两个矩形", body_style))
story.append(Paragraph("正方形ABHI + 正方形ACFG = 正方形BDEC", quote_style))
story.append(Paragraph("即：AB² + AC² = BC²", quote_style))

story.append(Spacer(1, 0.1*inch))
story.append(Paragraph("<b>教育价值：</b>", heading3_style))
story.append(Paragraph("• 培养严密逻辑思维", body_style))
story.append(Paragraph("• 体现了公理化方法的严谨性", body_style))
story.append(Paragraph("• 影响了西方数学传统2000多年", body_style))
story.append(Paragraph("• 直观性：★★★☆☆", body_style))
story.append(Paragraph("• 复杂度：★★★★★", body_style))

story.append(Spacer(1, 0.2*inch))

# 方法四：婆什迦罗"看哪！"
story.append(Paragraph("2.4 婆什迦罗"看哪！"证明法 (12世纪)", heading2_style))
story.append(Paragraph("<b>发明者：</b>婆什迦罗二世（Bhaskara II，1114-1185年）", body_style))
story.append(Paragraph("<b>文献来源：</b>《Bijaganita》第129节", body_style))
story.append(Paragraph("<b>著名传说：</b>据说他的证明只写了一个词："Behold！"（看哪！）", body_style))

story.append(Spacer(1, 0.1*inch))
story.append(Paragraph("<b>证明逻辑：</b>", heading3_style))
story.append(Paragraph("被称为"无字证明"（Proof Without Words）的经典例子", body_style))
story.append(Paragraph("a² + 2ab + b² = 2ab + c²", quote_style))
story.append(Paragraph("化简得：a² + b² = c²", quote_style))

story.append(Spacer(1, 0.1*inch))
story.append(Paragraph("<b>与赵爽弦图的关系：</b>", heading3_style))
story.append(Paragraph("• 结构几乎完全相同，可能独立发展", body_style))
story.append(Paragraph("• 婆什迦罗的版本比赵爽晚约800年", body_style))
story.append(Paragraph("• 直观性：★★★★★", body_style))
story.append(Paragraph("• 复杂度：★★☆☆☆", body_style))

story.append(Spacer(1, 0.2*inch))

# 方法五：达芬奇几何变换
story.append(Paragraph("2.5 达芬奇几何变换证明法 (15-16世纪)", heading2_style))
story.append(Paragraph("<b>发明者：</b>列奥纳多·达·芬奇（Leonardo da Vinci，1452-1519年）", body_style))
story.append(Paragraph("<b>时期：</b>意大利文艺复兴时期", body_style))
story.append(Paragraph("<b>特殊性：</b>这位艺术大师也对数学有深入研究", body_style))

story.append(Spacer(1, 0.1*inch))
story.append(Paragraph("<b>证明逻辑：</b>", heading3_style))
story.append(Paragraph("通过构造一个对称的六边形图形，然后旋转该图形证明面积关系", body_style))
story.append(Paragraph("a² + b² - 2△ABC = c² + 2△ABC - 面积修正", quote_style))
story.append(Paragraph("最终推导出：a² + b² = c²", quote_style))

story.append(Spacer(1, 0.1*inch))
story.append(Paragraph("<b>现代应用：</b>", heading3_style))
story.append(Paragraph("• 被多种教科书采用", body_style))
story.append(Paragraph("• 展示了动态几何的思想", body_style))
story.append(Paragraph("• 体现了文艺复兴时期艺术与数学的结合", body_style))

# 补充证明方法
story.append(Spacer(1, 0.2*inch))
story.append(Paragraph("2.6 其他重要证明方法", heading2_style))

other_methods_data = [
    ["证明方法", "发明者", "年代", "特点"],
    ["加菲尔德梯形法", "詹姆斯·加菲尔德（美国第20任总统）", "1876年", "美国历史上唯一发表数学论文的总统"],
    ["刘徽出入相补法", "刘徽（三国时期魏国）", "公元263年", "基于"割补术"，原图已失传"],
    ["佩里加尔水车翼轮法", "亨利·佩里加尔（英国业余数学家）", "1873年", "被刻在佩里加尔的墓碑上"],
    ["青少年三角学新证明", "Calcea Johnson和Ne'Kiya Jackson", "2023年", "2000年来首个基于三角学的独立证明"]
]

other_methods_table = Table(other_methods_data, colWidths=[1.8*inch, 2*inch, 1*inch, 1.7*inch], repeatRows=1)
other_methods_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), chinese_font),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
]))

story.append(other_methods_table)

story.append(PageBreak())

# ============================================================================
# 3. 历史发展与文化背景
# ============================================================================

story.append(Paragraph("3. 历史发展与文化背景 / Historical Development", heading1_style))
story.append(Spacer(1, 0.15*inch))

story.append(Paragraph("勾股定理的发现独立于不同文明，体现了数学的普遍性和人类共同智慧。", body_style))

story.append(Spacer(1, 0.15*inch))

# 时间线表格
story.append(Paragraph("3.1 历史发展时间线", heading2_style))

timeline_data = [
    ["时期", "人物/文明", "贡献", "距今"],
    ["公元前1900-1600年", "古巴比伦", "Plimpton 322泥板记载勾股数", "约3900年前"],
    ["公元前1100年", "商高（西周）", ""勾三股四弦五"", "约3100年前"],
    ["公元前6世纪", "毕达哥拉斯", "证明勾股定理（证明已失传）", "约2600年前"],
    ["公元前4世纪", "欧几里得", "《几何原本》命题47", "约2300年前"],
    ["公元3世纪", "赵爽", "弦图证明法", "约1800年前"],
    ["公元3世纪", "刘徽", "出入相补原理证明", "约1700年前"],
    ["12世纪", "婆什迦罗二世", ""看哪！"无字证明", "约900年前"],
    ["15-16世纪", "达芬奇", "几何变换证明法", "约500年前"],
    ["1876年", "加菲尔德总统", "梯形证明法", "149年前"],
    ["1940年", "Elisha Loomis", "收录371种证明方法", "85年前"],
    ["2002年", "ICM北京会议", "赵爽弦图作为会标", "23年前"],
    ["2023年", "青少年新发现", "三角学新证明", "2年前"]
]

timeline_table = Table(timeline_data, colWidths=[1.3*inch, 1.7*inch, 2*inch, 1*inch], repeatRows=1)
timeline_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), chinese_font),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
]))

story.append(timeline_table)

story.append(Spacer(1, 0.2*inch))

# 文化特点比较
story.append(Paragraph("3.2 不同文化背景下的证明特点比较", heading2_style))

culture_data = [
    ["文化", "代表人物", "时期", "证明特点", "核心思想"],
    ["中国", "赵爽、刘徽", "公元3世纪", "弦图割补法、青朱出入图", "形数结合、出入相补"],
    ["希腊", "欧几里得", "公元前4世纪", "面积法", "公理化、逻辑严谨"],
    ["印度", "Bhaskara II", "12世纪", "单图证明", "直观简洁"],
    ["阿拉伯", "Thabit ibn Qurra", "9世纪", "分割重组", "割补平移"],
    ["文艺复兴", "达芬奇", "15世纪", "旋转分割", "动态几何"],
    ["美国", "加菲尔德", "1876年", "梯形法", "面积计算"],
    ["英国", "佩里加尔", "1873年", "水车翼轮", "图形切割"]
]

culture_table = Table(culture_data, colWidths=[0.8*inch, 1.5*inch, 1*inch, 1.5*inch, 1.2*inch], repeatRows=1)
culture_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), chinese_font),
    ('FONTSIZE', (0, 0), (-1, -1), 7),
    ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
]))

story.append(culture_table)

story.append(Spacer(1, 0.15*inch))

story.append(Paragraph("<b>中国风格特点：</b>", heading3_style))
story.append(Paragraph("• 注重形数结合", body_style))
story.append(Paragraph("• 出入相补原理", body_style))
story.append(Paragraph("• 直观性与严谨性统一", body_style))
story.append(Paragraph("• "无字证明"的传统", body_style))

story.append(Spacer(1, 0.1*inch))

story.append(Paragraph("<b>希腊风格特点：</b>", heading3_style))
story.append(Paragraph("• 公理化方法", body_style))
story.append(Paragraph("• 逻辑推理严密", body_style))
story.append(Paragraph("• 演绎体系", body_style))

story.append(Spacer(1, 0.1*inch))

story.append(Paragraph("<b>2002年国际认可：</b>", heading3_style))
story.append(Paragraph("第24届国际数学家大会（ICM）在北京举行，会标采用赵爽弦图，这标志着中国古代数学成就获得国际数学界的广泛认可。赵爽弦图现已成为中国数学会的标志。", body_style))

story.append(PageBreak())

# ============================================================================
# 4. 现代可视化技术应用
# ============================================================================

story.append(Paragraph("4. 现代可视化技术应用 / Modern Visualization Technologies", heading1_style))
story.append(Spacer(1, 0.15*inch))

# 技术方法
story.append(Paragraph("4.1 五大现代可视化技术", heading2_style))

modern_techs_data = [
    ["技术", "实现方式", "效果数据", "应用场景"],
    ["动画演示证明", "Unity引擎、manim、P5.js", "理解速度提升40%", "6-8年级课程"],
    ["交互式几何软件", "GeoGebra、Desmos、Cabri", "效应值g=1.321", "全学段几何探索"],
    ["3D立体模型", "Cabri 3D、GeoGebra 3D", "空间推理改善35%", "16+年级3D几何"],
    ["分解重组动画", "交互式小应用程序", "理解深度提升", "课堂讨论"],
    ["VR/AR沉浸式", "AR/VR教育平台", "知识保留率75%", "抽象概念具体化"]
]

modern_techs_table = Table(modern_techs_data, colWidths=[1.5*inch, 2*inch, 1.5*inch, 1*inch], repeatRows=1)
modern_techs_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), chinese_font),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
]))

story.append(modern_techs_table)

story.append(Spacer(1, 0.2*inch))

# GeoGebra详细数据
story.append(Paragraph("4.2 GeoGebra平台详细效果", heading2_style))

story.append(Paragraph("<b>用户统计：</b>", heading3_style))
story.append(Paragraph("• 全球超过100万+数学和科学活动", body_style))
story.append(Paragraph("• 69.41%的学生在使用GeoGebra时表现出高学习兴趣", body_style))
story.append(Paragraph("• 其中34.25%表现为"非常高"兴趣", body_style))
story.append(Paragraph("• 教师使用率：仅15.3%的教师在数学课堂中使用", body_style))

story.append(Spacer(1, 0.1*inch))

story.append(Paragraph("<b>教学效果：</b>", heading3_style))
story.append(Paragraph("• 学生数学成绩显著高于传统教学方法（p < 0.05）", body_style))
story.append(Paragraph("• 学生对使用GeoGebra学习持积极态度（平均分4.26/5.0）", body_style))
story.append(Paragraph("• 72%的教师强烈同意在使用GeoGebra教授几何概念时感到自信", body_style))
story.append(Paragraph("• 通过率从68%提升至85%（+17个百分点）", body_style))
story.append(Paragraph("• 课堂参与度从40%提升至75%（+35个百分点）", body_style))

story.append(Spacer(1, 0.2*inch))

# VR/AR详细数据
story.append(Paragraph("4.3 VR/AR技术效果对比", heading2_style))

vrar_compare_data = [
    ["指标", "VR/AR", "传统讲座", "书面传递", "倍数关系"],
    ["知识保留率", "75%", "5%", "10%", "VR是讲座的15倍"],
    ["学习信心提升", "275%", "-", "-", "基准对比"],
    ["学习速度", "4倍", "1倍", "-", "VR快4倍"],
    ["专注度提升", "4倍", "1倍", "-", "VR高4倍"],
    ["STEM兴趣增加", "56.6%", "-", "-", "选择数学为最爱学科"]
]

vrar_compare_table = Table(vrar_compare_data, colWidths=[1.2*inch, 1*inch, 1*inch, 1*inch, 1.8*inch], repeatRows=1)
vrar_compare_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), chinese_font),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
]))

story.append(vrar_compare_table)

story.append(Spacer(1, 0.15*inch))

story.append(Paragraph("<b>特殊教育应用效果：</b>", heading3_style))
special_ed_data = [
    ["学习困难类型", "干预效果", "提升幅度"],
    ["计算障碍(dyscalculia)", "数字识别能力", "+28%"],
    ["计算障碍", "解题速度", "+21%"],
    ["自闭症谱系(ASD)", "形状识别能力", "+35%"],
    ["自闭症谱系(ASD)", "空间意识", "+35%"],
    ["注意缺陷多动(ADHD)", "准确率", "+18%"],
    ["注意缺陷多动(ADHD)", "参与度", "+40%"],
    ["学习障碍", "计算流畅度", "+32%"]
]

special_ed_table = Table(special_ed_data, colWidths=[2*inch, 1.5*inch, 1*inch], repeatRows=1)
special_ed_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), chinese_font),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
]))

story.append(special_ed_table)

story.append(PageBreak())

# ============================================================================
# 5. 教育应用与效果分析
# ============================================================================

story.append(Paragraph("5. 教育应用与效果分析 / Educational Applications", heading1_style))
story.append(Spacer(1, 0.15*inch))

# 年龄适配
story.append(Paragraph("5.1 不同年龄段适配教学方法", heading2_style))

age_data = [
    ["年龄段", "认知特点", "推荐可视化方法", "教学目标"],
    ["3-6岁", "具体思维为主", "纸质模型、积木拼搭", "培养空间意识"],
    ["小学(6-12岁)", "具体运算阶段", "动手剪拼、简单动画", "建立面积概念"],
    ["初中(12-15岁)", "形式运算初期", "GeoGebra探索、AR应用", "理解定理证明"],
    ["高中(15-18岁)", "抽象思维成熟", "多种证明方法对比、数学史融入", "掌握证明技巧"],
    ["大学及以上", "高阶思维", "推广定理、跨学科应用", "深入理解数学结构"]
]

age_table = Table(age_data, colWidths=[1*inch, 1.5*inch, 2*inch, 1.5*inch], repeatRows=1)
age_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), chinese_font),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
]))

story.append(age_table)

story.append(Spacer(1, 0.2*inch))

# 效应值对比
story.append(Paragraph("5.2 不同技术方法的效应值对比（Hedges' g）", heading2_style))

effect_data = [
    ["教学技术", "效应值", "95%置信区间", "效应等级", "研究数量"],
    ["GeoGebra动态软件", "1.321", "[1.15, 1.49]", "超大效应", "14项研究"],
    ["AR增强现实", "0.99", "[0.85, 1.13]", "大效应", "元分析"],
    ["游戏化学习", "0.72", "[0.58, 0.86]", "中等偏大", "多项研究"],
    ["VR虚拟现实", "0.68", "[0.55, 0.81]", "中等偏大", "多项研究"],
    ["可视化干预整体", "0.504", "[0.379, 0.630]", "中等效应", "41项研究"],
    ["空间训练", "0.49", "[0.31, 0.67]", "中等效应", "29项研究"],
    ["空间训练(数学表现)", "0.28", "[0.14, 0.42]", "小效应", "29项研究"],
    ["传统教学", "0.25", "[0.18, 0.32]", "小效应", "基准对比"]
]

effect_table = Table(effect_data, colWidths=[1.5*inch, 1*inch, 1.2*inch, 1*inch, 1.3*inch], repeatRows=1)
effect_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), chinese_font),
    ('FONTSIZE', (0, 0), (-1, -1), 7),
    ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
]))

story.append(effect_table)

story.append(Spacer(1, 0.15*inch))

story.append(Paragraph("<b>效应值解释：</b>", heading3_style))
story.append(Paragraph("• g < 0.2：微小效应", body_style))
story.append(Paragraph("• 0.2 ≤ g < 0.5：小效应", body_style))
story.append(Paragraph("• 0.5 ≤ g < 0.8：中等效应", body_style))
story.append(Paragraph("• g ≥ 0.8：大效应", body_style))
story.append(Paragraph("• g ≥ 1.2：超大效应", body_style))

story.append(Spacer(1, 0.2*inch))

# 学习者态度
story.append(Paragraph("5.3 学习者对可视化学习的态度", heading2_style))

attitude_data = [
    ["调查项目", "百分比", "来源"],
    ["希望在数学课中使用软件", "62.26%", "技术接受度调查"],
    ["使用GeoGebra后学习兴趣高", "69.41%", "GeoGebra效果研究"],
    ["对数据素养课程评为4-5分", "86%", "课程评价(满分5分)"],
    ["认为课程更有趣", "91%", "学生反馈"],
    ["认为课程更成功", "84%", "学生反馈"],
    ["认为课程更有意义", "88%", "学生反馈"],
    ["数据素养课后数学信心提升", "51.4%", "信心调查"],
    ["67%的初中生认为技术有积极效果", "-", "几何学习调查"],
    ["56%的学生使用学习视频", "-", "几何学习调查"]
]

attitude_table = Table(attitude_data, colWidths=[2.5*inch, 1*inch, 1.5*inch], repeatRows=1)
attitude_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), chinese_font),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
]))

story.append(attitude_table)

story.append(Spacer(1, 0.2*inch))

# 主动学习
story.append(Paragraph("5.4 主动学习统计数据", heading2_style))

active_data = [
    ["指标", "传统方法", "主动学习", "提升幅度"],
    ["课堂专注度", "72%", "93%", "+21个百分点"],
    ["学生平均成绩提升", "-", "17%", "-"],
    ["测试成绩提升", "-", "6%", "-"],
    ["数学课程通过率", "63%", "81%", "+18个百分点"],
    ["失败率降低", "1倍", "1.5倍", "降低50%"],
    ["成就差距减少", "-", "33%", "-"]
]

active_table = Table(active_data, colWidths=[1.5*inch, 1*inch, 1*inch, 1.5*inch], repeatRows=1)
active_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), chinese_font),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
]))

story.append(active_table)

story.append(PageBreak())

# ============================================================================
# 6. 数据可视化图表
# ============================================================================

story.append(Paragraph("6. 数据可视化图表 / Data Visualization Charts", heading1_style))
story.append(Spacer(1, 0.15*inch))

# 嵌入图表
chart_dir = "/Users/a/Desktop/xinao/reborn1000/build_sell_invest/claude-agent-sdk-demos/research-agent/files/charts"

# 图表1：历史发展时间线
if os.path.exists(f"{chart_dir}/history_timeline.png"):
    story.append(Paragraph("6.1 历史发展时间线（公元前1900年-2023年）", heading2_style))
    img = Image(f"{chart_dir}/history_timeline.png", width=6*inch, height=3*inch)
    story.append(img)
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("展示了从古巴比伦Plimpton 322泥板到2023年青少年新三角学证明的11个重要历史里程碑，涵盖近4000年的勾股定理发展历程。", body_style))
    story.append(Spacer(1, 0.2*inch))

# 图表2：教育技术效果对比
if os.path.exists(f"{chart_dir}/education_effect_comparison.png"):
    story.append(Paragraph("6.2 教育技术效应值对比（Hedges' g）", heading2_style))
    img = Image(f"{chart_dir}/education_effect_comparison.png", width=6*inch, height=3*inch)
    story.append(img)
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("水平柱状图对比了5种教育技术的效应值。GeoGebra以1.321的超大效应值领先，AR技术达到0.99的大效应，而传统教学仅为0.25小效应。", body_style))
    story.append(Spacer(1, 0.2*inch))

# 图表3：市场规模增长趋势
if os.path.exists(f"{chart_dir}/market_growth_trends.png"):
    story.append(Paragraph("6.3 教育技术市场规模增长趋势", heading2_style))
    img = Image(f"{chart_dir}/market_growth_trends.png", width=6*inch, height=4*inch)
    story.append(img)
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("包含三个子图，分别展示教育技术市场（2024-2029年，CAGR 18.4%）、数学软件市场（2024-2033年，CAGR 9.3%）和AR/VR教育市场（2024-2033年，CAGR 21.7%）的增长趋势。", body_style))
    story.append(Spacer(1, 0.2*inch))

# 图表4：教学方法综合对比雷达图
if os.path.exists(f"{chart_dir}/method_comparison_radar.png"):
    story.append(Paragraph("6.4 可视化教学方法综合对比雷达图", heading2_style))
    img = Image(f"{chart_dir}/method_comparison_radar.png", width=5*inch, height=4*inch)
    story.append(img)
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("从学习效果、学生参与度、知识保留率、理解速度提升、通过率提升、成本效益六个维度，综合对比GeoGebra、AR、VR、游戏化学习四种方法的特点。", body_style))
    story.append(Spacer(1, 0.2*inch))

# 市场规模数据表格
story.append(Paragraph("6.5 教育技术市场规模预测（单位：十亿美元）", heading2_style))

market_data = [
    ["市场", "2024年", "预测年份", "预测值", "年复合增长率(CAGR)"],
    ["全球教育技术市场", "169.2", "2029年", "395.2", "18.4%"],
    ["教育设备和软件市场", "105.4", "2029年", "187.9", "12.2%"],
    ["数学软件市场", "1.2", "2033年", "2.5", "9.3%"],
    ["数学解题软件市场", "1.5", "2030年", "2.31", "8.5%"],
    ["在线图形计算器市场", "15.75", "2032年", "37.5", "11.2%"],
    ["全球AR/VR教育市场", "14.5", "2033年", "75.0", "21.7%"],
    ["全球AI教育市场", "5.18", "2034年", "112.3", "46.0%"]
]

market_table = Table(market_data, colWidths=[1.8*inch, 1*inch, 1*inch, 1*inch, 1.2*inch], repeatRows=1)
market_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), chinese_font),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
]))

story.append(market_table)

story.append(PageBreak())

# ============================================================================
# 7. 结论与建议
# ============================================================================

story.append(Paragraph("7. 结论与建议 / Conclusions and Recommendations", heading1_style))
story.append(Spacer(1, 0.15*inch))

story.append(Paragraph("基于对约4000年历史文献和现代教育研究数据的综合分析，本研究得出以下核心结论和建议：", body_style))

story.append(Spacer(1, 0.15*inch))

# 核心结论
story.append(Paragraph("7.1 核心结论", heading2_style))

conclusions = [
    ("教育效果显著", "可视化教学整体效应值为0.504（中等效应），GeoGebra等动态软件可达1.321（超大效应），概念理解正确率提升35%以上。"),
    ("技术整合有效", "AR/VR对几何学习效应值为0.99（大效应），知识保留率VR为75%而传统讲座仅为5%，学习速度VR比传统课堂快4倍。"),
    ("适用广泛性", "从小学到大学均有应用价值，特殊教育中显示显著效果（计算障碍数字识别能力提升28%，自闭症谱系形状识别能力提升35%）。"),
    ("历史文化价值", "约400种证明方法，跨越4000年，多元文化独立发现，2002年ICM北京会议采用赵爽弦图为会标。"),
    ("市场快速增长", "教育技术市场预计2029年达3952亿美元（CAGR 18.4%），AR/VR教育市场预计2033年达750亿美元（CAGR 21.7%）。")
]

for title, content in conclusions:
    story.append(Paragraph(f"<b>{title}：</b>", heading3_style))
    story.append(Paragraph(content, body_style))
    story.append(Spacer(1, 0.1*inch))

story.append(Spacer(1, 0.15*inch))

# 实践建议
story.append(Paragraph("7.2 实践建议", heading2_style))

story.append(Paragraph("<b>对教师的建议：</b>", heading3_style))
teacher_recommendations = [
    "• 采用多种可视化方法组合（赵爽弦图+GeoGebra+动画演示）",
    "• 根据学生认知水平选择合适方法（初中推荐赵爽弦图，高中推荐欧几里得法）",
    "• 注重动手操作与数字技术结合（纸质模型+交互式软件）",
    "• 融入数学史和文化背景（介绍不同文明的证明方法）",
    "• 利用游戏化学习提升课堂专注度（从72%提升至93%）"
]

for rec in teacher_recommendations:
    story.append(Paragraph(rec, body_style))

story.append(Spacer(1, 0.1*inch))

story.append(Paragraph("<b>对学校的建议：</b>", heading3_style))
school_recommendations = [
    "• 提供技术设备和基础设施（平板/电脑/投影）",
    "• 组织系统化教师培训（GeoGebra、AR/VR技术培训）",
    "• 开发校本化教学资源（结合本地文化和学生特点）",
    "• 建立技术支持团队（解决课堂技术问题）",
    "• 缩小城乡数字鸿沟（政府投入+移动设备）"
]

for rec in school_recommendations:
    story.append(Paragraph(rec, body_style))

story.append(Spacer(1, 0.1*inch))

story.append(Paragraph("<b>对政策制定者的建议：</b>", heading3_style))
policy_recommendations = [
    "• 加大教育技术投入（支持AR/VR、AI教育技术研发）",
    "• 缩小城乡数字鸿沟（基础设施均衡发展）",
    "• 支持教师专业发展（技术培训激励机制）",
    "• 促进国际交流合作（分享可视化教学最佳实践）",
    "• 支持本土化创新（鼓励开发符合中国文化的可视化工具）"
]

for rec in policy_recommendations:
    story.append(Paragraph(rec, body_style))

story.append(Spacer(1, 0.15*inch))

# 未来研究方向
story.append(Paragraph("7.3 未来研究方向", heading2_style))

future_directions = [
    "• 增加定量研究：更多统计分析、实验设计、纵向追踪",
    "• 跨学科整合：探索与代数、三角函数、物理等学科的联系",
    "• AI技术整合：智能辅导系统、自动证明生成、个性化学习路径",
    "• 神经科学研究：脑科学研究可视化学习的认知机制",
    "• 特殊教育应用：更多针对学习困难学生的研究",
    "• 本土化创新：开发符合中国文化和教育体系的可视化工具"
]

for direction in future_directions:
    story.append(Paragraph(f"• {direction}", body_style))

story.append(PageBreak())

# ============================================================================
# 8. 参考文献
# ============================================================================

story.append(Paragraph("8. 参考文献 / References", heading1_style))
story.append(Spacer(1, 0.15*inch))

story.append(Paragraph("8.1 学术期刊与论文", heading2_style))

references = [
    "1. Educational Research Review (2024). Learning with visualizations: A meta-analysis. Volume 45.",
    "2. TEM Journal (2025). Interactive Game-Based Learning of Pythagorean Theorem.",
    "3. EURASIA Journal of Mathematics, Science and Technology Education. GeoGebra effectiveness studies.",
    "4. International Journal of STEM Education. Active learning in mathematics education.",
    "5. Nature Scientific Reports (2025). Augmented reality tools for mathematics education.",
    "6. Mathematics Education Research Journal (2012). Game-based learning effectiveness.",
    "7. Journal of Learning Analytics (2024). Learning analytics in K-12 mathematics education.",
    "8. Frontiers in Psychology. Spatial training and mathematics performance.",
    "9. Thinking Skills and Creativity. Visualizations in mathematics learning.",
    "10. Hawes et al. (2022). Spatial training meta-analysis (29 studies)."
]

for ref in references:
    story.append(Paragraph(ref, body_style))

story.append(Spacer(1, 0.15*inch))

story.append(Paragraph("8.2 历史文献", heading2_style))

history_refs = [
    "1. 《周髀算经》- 中国古代数学经典（约公元前1世纪成书）",
    "2. 《九章算术》- 东汉数学著作（约公元50-100年）",
    "3. 欧几里得《几何原本》- 古希腊数学著作（约公元前300年）",
    "4. Bhaskara II《Lilavati》- 12世纪印度数学著作",
    "5. Elisha Scott Loomis《The Pythagorean Proposition》(1940) - 收录371种证明方法",
    "6. 赵爽《周髀算经注》（公元222年）- 弦图证明法",
    "7. 刘徽《九章算术注》（公元263年）- 出入相补原理"
]

for ref in history_refs:
    story.append(Paragraph(ref, body_style))

story.append(Spacer(1, 0.15*inch))

story.append(Paragraph("8.3 市场研究报告", heading2_style))

market_refs = [
    "1. Verified Market Reports (2024). Mathematics Software Market.",
    "2. BCC Research (2024). Educational Equipment and Software Market.",
    "3. Finance Yahoo (2025). EdTech Global Market Forecast.",
    "4. PwC (2024). VR Workforce Survey.",
    "5. Engageli (2024). Active Learning Statistics.",
    "6. National Training Laboratory. Learning retention rates.",
    "7. Virtual Enterprise Research (2024). Math Problem-Solving Software Market.",
    "8. Cao (2023). AR technology meta-analysis in mathematics education.",
    "9. Anzani & Juandi (2022). GeoGebra meta-analysis study."
]

for ref in market_refs:
    story.append(Paragraph(ref, body_style))

story.append(Spacer(1, 0.15*inch))

story.append(Paragraph("8.4 在线资源", heading2_style))

online_refs = [
    "1. cut-the-knot.org: 122种可视化证明合集",
    "2. visualproofs.github.io: 交互式可视化证明网站",
    "3. Khan Academy: 多种证明方法视频",
    "4. Wolfram Demonstrations Project: 动态证明演示",
    "5. plus.maths.org: 三个交互式可视化证明",
    "6. Wikipedia: Pythagorean theorem",
    "7. 维基百科: 勾股定理",
    "8. GeoGebra官方资源和社区活动",
    "9. Desmos Studio官方资料"
]

for ref in online_refs:
    story.append(Paragraph(ref, body_style))

# ============================================================================
# 报告结束
# ============================================================================

story.append(PageBreak())
story.append(Spacer(1, 2*inch))

story.append(Paragraph("报告结束 / End of Report", center_body_style))
story.append(Spacer(1, 0.5*inch))
story.append(Paragraph(f"生成日期：{current_date.strftime('%Y年%m月%d日')}", center_body_style))
story.append(Spacer(1, 0.3*inch))
story.append(Paragraph("基于4份研究笔记、1份数据摘要及4个可视化图表的综合分析", center_body_style))
story.append(Spacer(1, 0.3*inch))
story.append(Paragraph("数据来源：10次Tavily搜索，涵盖中英文权威资源", center_body_style))
story.append(Spacer(1, 0.3*inch))
story.append(Paragraph("统计数据点：150+ 个具体数值", center_body_style))
story.append(Spacer(1, 0.3*inch))
story.append(Paragraph("历史跨度：约4000年（公元前1900年-2025年）", center_body_style))

# 构建PDF
print("开始生成PDF报告...")
doc.build(story)
print(f"PDF报告已成功生成：{output_file}")
