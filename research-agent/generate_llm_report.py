#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
大语言模型发展历程研究报告生成器
使用reportlab生成专业的中文PDF报告
"""

import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor, black, darkblue, darkgray
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle, KeepTogether
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.fonts import addMapping

# 确保输出目录存在
os.makedirs('/Users/a/Desktop/xinao/reborn1000/build_sell_invest/claude-agent-sdk-demos/research-agent/files/reports', exist_ok=True)

# 基础路径
BASE_DIR = '/Users/a/Desktop/xinao/reborn1000/build_sell_invest/claude-agent-sdk-demos/research-agent'

# 图表路径
CHARTS = {
    'parameter_timeline': f'{BASE_DIR}/files/charts/model_parameter_timeline.png',
    'market_share': f'{BASE_DIR}/files/charts/market_share_comparison.png',
    'mmlu_benchmark': f'{BASE_DIR}/files/charts/mmlu_benchmark_comparison.png',
    'training_cost': f'{BASE_DIR}/files/charts/training_cost_trends.png',
    'token_ratio': f'{BASE_DIR}/files/charts/token_parameter_ratio.png'
}

def setup_chinese_fonts():
    """设置中文字体支持"""
    # 尝试注册系统中可用的中文字体
    font_paths = [
        '/System/Library/Fonts/PingFang.ttc',  # macOS
        '/System/Library/Fonts/STHeiti Light.ttc',
        '/System/Library/Fonts/STSong.ttc',
        '/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf',  # Linux
        'C:/Windows/Fonts/msyh.ttc',  # Windows
        'C:/Windows/Fonts/simhei.ttf',
    ]

    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                pdfmetrics.registerFont(TTFont('ChineseFont', font_path, subfontIndex=0))
                addMapping('ChineseFont', 0, 0, 'ChineseFont')
                return 'ChineseFont'
            except Exception as e:
                continue

    # 如果没有找到中文字体，使用默认字体
    return 'Helvetica'

def create_custom_styles(chinese_font):
    """创建自定义样式"""
    styles = getSampleStyleSheet()

    # 中文正文样式
    styles.add(ParagraphStyle(
        name='ChineseBody',
        fontName=chinese_font,
        fontSize=10,
        leading=14,
        alignment=TA_JUSTIFY,
        spaceAfter=6,
        textColor=black
    ))

    # 中文标题样式
    styles.add(ParagraphStyle(
        name='ChineseTitle',
        fontName=chinese_font,
        fontSize=20,
        leading=28,
        alignment=TA_CENTER,
        spaceAfter=12,
        textColor=darkblue,
        bold=True
    ))

    # 中文一级标题
    styles.add(ParagraphStyle(
        name='ChineseHeading1',
        fontName=chinese_font,
        fontSize=16,
        leading=22,
        alignment=TA_LEFT,
        spaceAfter=10,
        spaceBefore=12,
        textColor=darkblue,
        bold=True
    ))

    # 中文二级标题
    styles.add(ParagraphStyle(
        name='ChineseHeading2',
        fontName=chinese_font,
        fontSize=14,
        leading=18,
        alignment=TA_LEFT,
        spaceAfter=8,
        spaceBefore=8,
        textColor=black,
        bold=True
    ))

    # 图表说明样式
    styles.add(ParagraphStyle(
        name='ChineseCaption',
        fontName=chinese_font,
        fontSize=9,
        leading=12,
        alignment=TA_CENTER,
        spaceAfter=10,
        textColor=darkgray
    ))

    return styles

def create_cover_page(story, styles):
    """创建封面页"""
    story.append(Spacer(1, 3*cm))

    # 主标题
    story.append(Paragraph("大语言模型发展历程研究报告", styles['ChineseTitle']))
    story.append(Spacer(1, 1*cm))

    # 副标题
    story.append(Paragraph("2017-2025 技术演进与市场分析", styles['ChineseHeading2']))
    story.append(Spacer(1, 2*cm))

    # 报告日期
    date_str = datetime.now().strftime("%Y年%m月%d日")
    story.append(Paragraph(f"报告日期：{date_str}", styles['ChineseBody']))
    story.append(Spacer(1, 1*cm))

    # 关键数据摘要
    key_data = [
        ["数据覆盖", "2017-2025年（8年）"],
        ["模型数量", "50+ 个主要LLM系列"],
        ["数据点", "200+ 个定量指标"],
        ["图表数量", "5张核心可视化图表"]
    ]

    table = Table(key_data, colWidths=[5*cm, 5*cm], hAlign='CENTER')
    table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'ChineseFont'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, darkgray),
        ('BACKGROUND', (0, 0), (0, -1), HexColor('#E8F4F8')),
        ('BACKGROUND', (1, 0), (1, -1), HexColor('#F0F0F0')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [HexColor('#E8F4F8'), HexColor('#F0F0F0')]),
    ]))
    story.append(table)

    story.append(PageBreak())

def create_executive_summary(story, styles):
    """创建执行摘要"""
    story.append(Paragraph("执行摘要", styles['ChineseHeading1']))
    story.append(Spacer(1, 0.5*cm))

    summary_text = """
        本报告全面分析了2017年至2025年大语言模型（LLM）的技术演进、市场竞争格局与未来发展趋势。
        研究显示，8年间模型参数规模增长了14,075倍，从Transformer的213M参数发展到GPT-5的数万亿参数。
        全球LLM市场规模从2024年的56.17亿美元预计将增长至2030年的135.2亿美元，年复合增长率达28.0%。

        技术层面，MMLU基准测试得分从2020年GPT-3的43.9%提升至2024年Gemini 1.5 Ultra的93.4%，
        已超越人类基线水平。训练成本呈现先升后降趋势，DeepSeek-V3以557万美元的训练成本
        达到GPT-4水平，仅为后者的1/18，标志着效率革命的到来。

        竞争格局方面，ChatGPT占据全球81.85%的市场份额，绝对主导地位明显。
        中国市场相对分散，阿里通义以17.7%的份额领先，字节豆包和DeepSeek分别以14.1%和10.3%紧随其后。

        展望未来，AGI实现时间线预测集中在2027-2030年，智能体AI市场预计2034年达到2360.3亿美元，
        年复合增长率30.3%。数据稀缺、幻觉问题和能源消耗是当前面临的主要技术挑战。
    """

    story.append(Paragraph(summary_text, styles['ChineseBody']))
    story.append(Spacer(1, 1*cm))

def create_section_early_development(story, styles):
    """创建第一部分：早期基础（2017-2020）"""
    story.append(Paragraph("一、早期基础：Transformer架构诞生（2017-2020）", styles['ChineseHeading1']))
    story.append(Spacer(1, 0.3*cm))

    # 1.1 Transformer诞生
    story.append(Paragraph("1.1 Transformer革命（2017年6月）", styles['ChineseHeading2']))
    story.append(Spacer(1, 0.2*cm))

    transformer_text = """
        2017年6月12日，Google团队发表开创性论文"Attention Is All You Need"（arXiv:1706.03762），
        彻底改变了自然语言处理领域。Transformer架构完全基于注意力机制，摒弃了传统的循环神经网络（RNN）
        和卷积神经网络（CNN），实现了完全并行化处理。
    """

    story.append(Paragraph(transformer_text, styles['ChineseBody']))

    # Transformer规格表
    spec_data = [
        ["规格", "Base模型", "Big模型"],
        ["参数量", "65M", "213M"],
        ["编码器层数", "6", "6"],
        ["注意力头数", "8", "16"],
        ["模型维度(d_model)", "512", "1024"],
        ["训练时间(8 P100)", "12小时", "3.5天"]
    ]

    spec_table = Table(spec_data, colWidths=[4*cm, 3.5*cm, 3.5*cm], hAlign='LEFT')
    spec_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'ChineseFont'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, darkgray),
        ('BACKGROUND', (0, 0), (0, -1), HexColor('#D4E6F1')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(spec_table)
    story.append(Spacer(1, 0.5*cm))

    # 1.2 预训练模型时代
    story.append(Paragraph("1.2 预训练模型时代（2018年）", styles['ChineseHeading2']))
    story.append(Spacer(1, 0.2*cm))

    pretrained_text = """
        2018年被称作"NLP奇迹年"，多个突破性模型相继诞生：
        <br/>• <b>ELMo</b>（2018年2月）：双向LSTM，94M参数，在SQuAD上达到92.22% F1分数
        <br/>• <b>ULMFiT</b>（2018年1月）：首个通用NLP迁移学习框架，错误率降低18-24%
        <br/>• <b>GPT-1</b>（2018年6月）：117M参数，GLUE得分72.8，展示生成式预训练潜力
        <br/>• <b>BERT</b>（2018年10月）：340M参数，GLUE得分82.1，建立双向编码器新范式
    """

    story.append(Paragraph(pretrained_text, styles['ChineseBody']))
    story.append(Spacer(1, 0.5*cm))

    # GLUE进展表
    glce_data = [
        ["模型", "GLUE得分", "提升幅度"],
        ["ELMo（2018年初）", "68.9", "基准"],
        ["GPT-1", "72.8", "+5.7%"],
        ["BERT Base", "79.6", "+15.5%"],
        ["BERT Large", "82.1", "+19.2%"]
    ]

    glce_table = Table(glce_data, colWidths=[4*cm, 3*cm, 3*cm], hAlign='LEFT')
    glce_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'ChineseFont'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, darkgray),
        ('BACKGROUND', (0, 0), (0, -1), HexColor('#D4E6F1')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(glce_table)
    story.append(Spacer(1, 0.5*cm))

    # 1.3 GPT-2突破
    story.append(Paragraph("1.3 GPT-2：零样本学习里程碑（2019年）", styles['ChineseHeading2']))
    story.append(Spacer(1, 0.2*cm))

    gpt2_text = """
        GPT-2于2019年2月发布，参数规模达到1.5B，相比GPT-1增长12.8倍。
        其核心突破在于展示了<b>零样本学习</b>能力，无需特定任务微调即可完成多种任务。
        在LAMBADA基准测试上达到63.24%准确率，相比之前SOTA提升4.01个百分点。
    """

    story.append(Paragraph(gpt2_text, styles['ChineseBody']))
    story.append(Spacer(1, 0.5*cm))

def create_section_gpt_evolution(story, styles):
    """创建第二部分：GPT演进"""
    story.append(Paragraph("二、GPT系列：从GPT-3到GPT-5的技术跃迁", styles['ChineseHeading1']))
    story.append(Spacer(1, 0.3*cm))

    # 2.1 GPT-3突破
    story.append(Paragraph("2.1 GPT-3：涌现能力首次展示（2020年）", styles['ChineseHeading2']))
    story.append(Spacer(1, 0.2*cm))

    gpt3_text = """
        2020年5月28日，OpenAI发布GPT-3，参数规模达到175B，相比GPT-2增长116倍。
        训练数据包含300B tokens（约45TB压缩前文本），计算成本为430万美元。
        这是首次清晰展示<b>涌现能力</b>的模型——few-shot和zero-shot学习能力显著提升。
    """

    story.append(Paragraph(gpt3_text, styles['ChineseBody']))

    # GPT演进表
    gpt_evolution = [
        ["模型", "发布时间", "参数量", "关键突破"],
        ["GPT-1", "2018年6月", "117M", "首个生成式预训练模型"],
        ["GPT-2", "2019年2月", "1.5B", "零样本学习能力"],
        ["GPT-3", "2020年5月", "175B", "涌现能力"],
        ["ChatGPT", "2022年11月", "~175B", "产品化突破"],
        ["GPT-4", "2023年3月", "1.8T", "多模态融合"],
        ["GPT-4o", "2024年5月", "~1.8T", "原生多模态"],
        ["GPT-5", "2025年", "~3T", "推理能力质变"]
    ]

    gpt_table = Table(gpt_evolution, colWidths=[2.5*cm, 2.5*cm, 2*cm, 6*cm], hAlign='LEFT')
    gpt_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'ChineseFont'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, darkgray),
        ('BACKGROUND', (0, 0), (0, -1), HexColor('#D4E6F1')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('WORDWRAP', (0, 0), (-1, -1), True),
    ]))
    story.append(gpt_table)
    story.append(Spacer(1, 0.5*cm))

    # 2.2 ChatGPT产品化
    story.append(Paragraph("2.2 ChatGPT：AI产品化里程碑（2022年11月）", styles['ChineseHeading2']))
    story.append(Spacer(1, 0.2*cm))

    chatgpt_text = """
        2022年11月30日，ChatGPT发布，仅用5天达到100万用户，2个月达到1亿月活用户，
        创造历史最快增长记录。核心创新是引入<b>RLHF（强化学习人类反馈）</b>技术，
        使模型输出更符合人类意图。截至2025年10月，ChatGPT周活用户达到8-10亿。
    """

    story.append(Paragraph(chatgpt_text, styles['ChineseBody']))

    # 用户增长里程碑
    growth_data = [
        ["里程碑", "用户数", "用时"],
        ["100万用户", "100万", "5天"],
        ["1亿用户", "100M", "2个月"],
        ["5亿周活", "500M", "约27个月"],
        ["10亿周活", "1B", "约35个月"]
    ]

    growth_table = Table(growth_data, colWidths=[4*cm, 3*cm, 3*cm], hAlign='LEFT')
    growth_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'ChineseFont'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, darkgray),
        ('BACKGROUND', (0, 0), (0, -1), HexColor('#D4E6F1')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(growth_table)
    story.append(Spacer(1, 0.5*cm))

    # 2.3 GPT-4多模态
    story.append(Paragraph("2.3 GPT-4：多模态融合（2023年）", styles['ChineseHeading2']))
    story.append(Spacer(1, 0.2*cm))

    gpt4_text = """
        GPT-4于2023年3月14日发布，参数规模约1.8T，采用Mixture-of-Experts架构，
        由16个专家模型组成，每次推理激活约50B参数。核心突破是支持<b>图像+文本输入</b>，
        在MMLU基准测试上达到86.4%，相比GPT-3.5的70%提升16.4个百分点。
        模拟律师考试成绩进入前10%（GPT-3.5为倒数10%）。
    """

    story.append(Paragraph(gpt4_text, styles['ChineseBody']))
    story.append(Spacer(1, 0.5*cm))

def create_section_competition(story, styles):
    """创建第三部分：竞争格局"""
    story.append(Paragraph("三、全球竞争格局：中美欧三足鼎立", styles['ChineseHeading1']))
    story.append(Spacer(1, 0.3*cm))

    # 3.1 市场规模
    story.append(Paragraph("3.1 全球LLM市场规模", styles['ChineseHeading2']))
    story.append(Spacer(1, 0.2*cm))

    market_text = """
        2024年全球LLM市场规模达到56.17亿美元，预计2025年增长至73.58亿美元（年增长率31%）。
        到2030年，市场规模预计达到135.2亿美元，年复合增长率28.0%。北美地区占据39%的市场份额，
        美国单一市场占全球23.4%（13.126亿美元）。亚太地区是增长最快的市场，预计2030年达到940亿美元。
    """

    story.append(Paragraph(market_text, styles['ChineseBody']))
    story.append(Spacer(1, 0.3*cm))

    # 市场规模表
    market_size_data = [
        ["年份", "全球市场", "企业级市场", "增长率"],
        ["2024年", "$56.17亿", "$40.5亿", "-"],
        ["2025年", "$73.58亿", "$48.4亿", "31%"],
        ["2030年", "$135.2亿", "$328.2亿", "CAGR 28-31%"]
    ]

    market_table = Table(market_size_data, colWidths=[2.5*cm, 3*cm, 3*cm, 3*cm], hAlign='LEFT')
    market_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'ChineseFont'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, darkgray),
        ('BACKGROUND', (0, 0), (0, -1), HexColor('#D4E6F1')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(market_table)
    story.append(Spacer(1, 0.5*cm))

    # 3.2 全球市场格局
    story.append(Paragraph("3.2 全球AI聊天机器人市场份额（2025年）", styles['ChineseHeading2']))
    story.append(Spacer(1, 0.2*cm))

    # 插入市场份额图表
    if os.path.exists(CHARTS['market_share']):
        img = Image(CHARTS['market_share'], width=15*cm, height=8*cm)
        story.append(img)
        story.append(Paragraph("图1：全球与中国大模型市场份额对比", styles['ChineseCaption']))
        story.append(Spacer(1, 0.3*cm))

    market_share_text = """
        <b>全球市场高度集中</b>：ChatGPT占据81.85%的市场份额，Perplexity以11.05%位居第二，
        前两名合计占据92.9%的市场。Microsoft Copilot（3.07%）、Google Gemini（2.97%）
        和Claude（1.05%）分列三至五位。

        <b>中国市场相对分散</b>：阿里通义以17.7%的份额领先，字节豆包（14.1%）和DeepSeek（10.3%）
        紧随其后，前三名合计42.1%，竞争更加激烈。
    """

    story.append(Paragraph(market_share_text, styles['ChineseBody']))
    story.append(Spacer(1, 0.5*cm))

    # 3.3 中国大模型发展
    story.append(Paragraph("3.3 中国大模型：快速追赶", styles['ChineseHeading2']))
    story.append(Spacer(1, 0.2*cm))

    china_text = """
        中国大模型发展迅速，2024年市场规模达47.9亿元人民币，2025年预计297亿元。
        阿里通义Qwen系列衍生模型超过14万个，全球排名第一。智谱GLM系列服务27万开发者，
        辐射1.2万家企业客户。斯坦福AI指数报告中，阿里6款模型上榜，全球第三、中国第一。
        中美AI性能差距从2023年的17.5%骤降至2025年的0.3%。
    """

    story.append(Paragraph(china_text, styles['ChineseBody']))
    story.append(Spacer(1, 0.5*cm))

    # 中国市场份额表
    china_share_data = [
        ["排名", "公司", "市场份额", "主要特点"],
        ["1", "阿里通义", "17.7%", "14万衍生模型(全球第一)"],
        ["2", "字节豆包", "14.1%", "快速对齐第一梯队"],
        ["3", "DeepSeek", "10.3%", "开源MoE效率革命"],
        ["4", "百度文心", "8.5%", "中国领先者"],
        ["5", "智谱AI", "6.2%", "27万开发者"],
        ["6", "科大讯飞", "5.8%", "深度国产算力适配"]
    ]

    china_table = Table(china_share_data, colWidths=[1.5*cm, 3*cm, 2*cm, 6*cm], hAlign='LEFT')
    china_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'ChineseFont'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, darkgray),
        ('BACKGROUND', (0, 0), (0, -1), HexColor('#D4E6F1')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('WORDWRAP', (0, 0), (-1, -1), True),
    ]))
    story.append(china_table)
    story.append(Spacer(1, 0.5*cm))

def create_section_technical_challenges(story, styles):
    """创建第四部分：技术挑战"""
    story.append(Paragraph("四、技术挑战与应对", styles['ChineseHeading1']))
    story.append(Spacer(1, 0.3*cm))

    # 4.1 幻觉问题
    story.append(Paragraph("4.1 幻觉问题（Hallucination）", styles['ChineseHeading2']))
    story.append(Spacer(1, 0.2*cm))

    hallucination_text = """
        幻觉问题是当前最紧迫的挑战之一。Vectara FaithJudge基准测试显示：
        <br/>• Gemini 2.5 Flash：6.3%幻觉率（最低）
        <br/>• GPT-4o：15.8%幻觉率
        <br/>• Claude 3.7 Sonnet：16.0%幻觉率
        <br/>• OpenAI o4-mini：75%错误率（SimpleQA基准）

        <b>实际影响</b>：77%的企业担心AI幻觉问题，47%的AI生成引用包含错误信息。
        简单的基于提示的缓解方法可将GPT-4o的幻觉率从53%降至23%。
    """

    story.append(Paragraph(hallucination_text, styles['ChineseBody']))
    story.append(Spacer(1, 0.5*cm))

    # 4.2 数据稀缺
    story.append(Paragraph("4.2 数据质量与稀缺性", styles['ChineseHeading2']))
    story.append(Spacer(1, 0.2*cm))

    data_text = """
        最优训练比例约为20 tokens/参数，1万亿参数模型需要20万亿tokens。
        估计高质量英文文本总量约10万亿tokens，网络索引文本约510万亿tokens。
        Epoch AI最新预测：高质量文本可能在2028年耗尽（而非原预测的2024年）。

        <b>挑战</b>：42%的组织缺乏足够专有数据，68%的数据领导者对数据质量不完全有信心。
        <b>解决方案</b>：合成数据、数据质量优化、多模态数据扩展。
    """

    story.append(Paragraph(data_text, styles['ChineseBody']))
    story.append(Spacer(1, 0.5*cm))

    # 4.3 能源消耗
    story.append(Paragraph("4.3 能源消耗与环境影响", styles['ChineseHeading2']))
    story.append(Spacer(1, 0.2*cm))

    energy_text = """
        美国2024年数据中心能源消耗183 TWh（占总电力4.4%），全球约415 TWh（占1.5%）。
        2030年预测：美国426 TWh（增长133%），AI数据中心90 TWh（较2022年增长10倍）。

        <b>模型训练能耗</b>：
        <br/>• GPT-3训练：1,287 MWh（120个家庭年用电量）
        <br/>• GPT-4训练：约50 GWh（足够旧金山供电3天）
        <br/>• AI服务器功率：2022年400瓦 → 2024年1,200瓦

        <b>效率改进</b>：新一代AI芯片90天内训练，消耗8.6 GWh（仅为前代的1/10）。
    """

    story.append(Paragraph(energy_text, styles['ChineseBody']))
    story.append(Spacer(1, 0.5*cm))

    # 4.4 安全对齐
    story.append(Paragraph("4.4 安全与对齐挑战", styles['ChineseHeading2']))
    story.append(Spacer(1, 0.2*cm))

    safety_text = """
        <b>RLHF效果</b>：RLAIF在无害对话中达到88%无害率，优于RLHF的76%和SFT的64%。

        <b>安全投资不足</b>：公共部门AI安全投资与私营部门比例约为1:10,000（Stuart Russell估计）。
        NSF 2023-2024年仅投入1000万美元AI安全研究。

        <b>网络安全</b>：2025年新增5个漏洞类别（过度代理、系统提示词泄露、向量和嵌入弱点、
        虚假信息、无界消费）。69%的已知漏洞与基于网络的攻击向量相关。
    """

    story.append(Paragraph(safety_text, styles['ChineseBody']))
    story.append(Spacer(1, 0.5*cm))

def create_section_future_trends(story, styles):
    """创建第五部分：未来趋势"""
    story.append(Paragraph("五、未来发展趋势", styles['ChineseHeading1']))
    story.append(Spacer(1, 0.3*cm))

    # 5.1 AGI展望
    story.append(Paragraph("5.1 AGI时间线预测", styles['ChineseHeading2']))
    story.append(Spacer(1, 0.2*cm))

    agi_text = """
        AGI（通用人工智能）实现时间线的预测显著收敛：
        <br/>• <b>AI Frontiers</b>：50%概率2028年，80%概率2030年
        <br/>• <b>专家调研</b>（5,288名AI研究者）：50%概率2040-2061年
        <br/>• <b>主要实验室领导</b>：预测集中在2027-2030年
        <br/>• <b>Metaculus</b>：聚合预测指向~2028年

        从GPT-3发布时的50年预测缩短至2024年底的5年，Sam Altman表示"AGI特性已在视野中"，
        Dario Amodei预测"强力AI"可能在2026年到来。
    """

    story.append(Paragraph(agi_text, styles['ChineseBody']))
    story.append(Spacer(1, 0.5*cm))

    # 5.2 智能体AI
    story.append(Paragraph("5.2 智能体AI（Agent）市场", styles['ChineseHeading2']))
    story.append(Spacer(1, 0.2*cm))

    agent_text = """
        2024年自主AI和智能体市场规模68亿美元，2025-2034年CAGR 30.3%，2034年预测2360.3亿美元。
        79%的组织报告已采用某种形式的AI智能体（2025年），96%计划在2025年扩大使用。

        <b>投资回报</b>：智能体AI的平均ROI 171%，美国企业智能体部署ROI 192%。
        Gartner预测到2028年企业软件中AI智能体将增长33倍，15%的工作决策将变得自主化。
    """

    story.append(Paragraph(agent_text, styles['ChineseBody']))
    story.append(Spacer(1, 0.5*cm))

    # 5.3 端侧部署
    story.append(Paragraph("5.3 端侧AI部署", styles['ChineseHeading2']))
    story.append(Spacer(1, 0.2*cm))

    edge_text = """
        Edge AI市场：2024年87亿美元，2030年预测568亿美元，CAGR 36.9%。
        On-Device AI市场：2024年148.7亿美元，2034年预测1741.9亿美元，CAGR 27.9%。

        <b>技术趋势</b>：
        <br/>• 2025年端侧AI将占AI总市场收入的30%以上（2020年仅10%）
        <br/>• 4位量化广泛采用，实现性能接近全精度
        <br/>• 推理成本下降9-900倍/年（取决于任务）
    """

    story.append(Paragraph(edge_text, styles['ChineseBody']))
    story.append(Spacer(1, 0.5*cm))

    # 5.4 具身AI
    story.append(Paragraph("5.4 具身AI与机器人", styles['ChineseHeading2']))
    story.append(Spacer(1, 0.2*cm))

    embodied_text = """
        2024年具身AI市场44.4亿美元，2030年预测230.6亿美元，CAGR 39.0%。
        应用领域分布：机器人细分市场占40.9%，自动化和制造业占27.1%。

        <b>应用场景</b>：
        <br/>• AI辅助机器人手术：手术时间减少25%，并发症减少30%
        <br/>• 全球AMR（自主移动机器人）出货量：从5万台增长6倍至2030年的30万台
        <br/>• 70%的制造工厂将在2030年前部署AMR
    """

    story.append(Paragraph(embodied_text, styles['ChineseBody']))
    story.append(Spacer(1, 0.5*cm))

def create_visual_charts_section(story, styles):
    """创建可视化图表部分"""
    story.append(Paragraph("六、关键数据可视化", styles['ChineseHeading1']))
    story.append(Spacer(1, 0.3*cm))

    # 图表1：参数时间线
    if os.path.exists(CHARTS['parameter_timeline']):
        story.append(Paragraph("6.1 模型参数规模演进时间线", styles['ChineseHeading2']))
        img = Image(CHARTS['parameter_timeline'], width=16*cm, height=9*cm)
        story.append(img)
        story.append(Paragraph("图2：2017-2025年大语言模型参数规模指数增长（14,075倍）", styles['ChineseCaption']))
        story.append(Spacer(1, 0.3*cm))

        caption_text = """
            <b>关键里程碑</b>：
            <br/>• 2017年Transformer：213M参数（基准）
            <br/>• 2020年GPT-3：175B参数（821倍增长）
            <br/>• 2023年GPT-4：1.8T参数（8,450倍增长）
            <br/>• 2025年GPT-5：约3T参数（14,075倍增长）
        """
        story.append(Paragraph(caption_text, styles['ChineseBody']))
        story.append(Spacer(1, 0.5*cm))

    # 图表2：MMLU基准
    if os.path.exists(CHARTS['mmlu_benchmark']):
        story.append(Paragraph("6.2 技术性能基准对比（MMLU）", styles['ChineseHeading2']))
        img = Image(CHARTS['mmlu_benchmark'], width=16*cm, height=9*cm)
        story.append(img)
        story.append(Paragraph("图3：MMLU基准测试得分演进（2020-2024）", styles['ChineseCaption']))
        story.append(Spacer(1, 0.3*cm))

        mmlu_text = """
            <b>5年间提升49.5个百分点</b>：
            <br/>• 2020年GPT-3：43.9%（起点）
            <br/>• 2024年Gemini 1.5 Ultra：93.4%（当前最高）
            <br/>• 人类基线：87.1%
            <br/>• 2024年已有6个模型超越人类基线

            <b>推理模型突破</b>：OpenAI o3相比GPT-4o，数学推理提升78.2个百分点（AIME 2024）。
        """
        story.append(Paragraph(mmlu_text, styles['ChineseBody']))
        story.append(Spacer(1, 0.5*cm))

    # 图表3：训练成本
    if os.path.exists(CHARTS['training_cost']):
        story.append(Paragraph("6.3 训练成本与效率革命", styles['ChineseHeading2']))
        img = Image(CHARTS['training_cost'], width=16*cm, height=10*cm)
        story.append(img)
        story.append(Paragraph("图4：训练成本趋势与推理成本对比", styles['ChineseCaption']))
        story.append(Spacer(1, 0.3*cm))

        cost_text = """
            <b>效率革命</b>：
            <br/>• 2017-2023成本爆发式增长：从$930到$1.914亿（205,803倍）
            <br/>• 2024年成本下降：DeepSeek-V3以$5.5M达到GPT-4水平，仅为后者的1/18

            <b>推理成本主导</b>：
            <br/>• GPT-4推理成本是训练成本的29倍
            <br/>• 预测2026年推理需求达到训练的3倍
        """
        story.append(Paragraph(cost_text, styles['ChineseBody']))
        story.append(Spacer(1, 0.5*cm))

    # 图表4：Token/参数比
    if os.path.exists(CHARTS['token_ratio']):
        story.append(Paragraph("6.4 缩放定律演变：Token/参数比", styles['ChineseHeading2']))
        img = Image(CHARTS['token_ratio'], width=16*cm, height=9*cm)
        story.append(img)
        story.append(Paragraph("图5：Token/参数比演变（2020-2024）", styles['ChineseCaption']))
        story.append(Spacer(1, 0.3*cm))

        ratio_text = """
            <b>革命性发现</b>：
            <br/>• 2020年GPT-3（Kaplan）：1.7:1（欠训练）
            <br/>• 2022年Chinchilla：20:1（计算最优标准）
            <br/>• 2024年LLaMA-3 70B：214:1（+970%）
            <br/>• 2024年LLaMA-3 8B：1,875:1（+9,275%）

            Chinchilla的20:1被多次超越，LLaMA-3证明<b>过度训练的巨大价值</b>。
            缩放定律从"参数优先"→"数据优先"→"质量优先"。
        """
        story.append(Paragraph(ratio_text, styles['ChineseBody']))
        story.append(Spacer(1, 0.5*cm))

def create_sources_section(story, styles):
    """创建数据来源部分"""
    story.append(PageBreak())
    story.append(Paragraph("数据来源与参考文献", styles['ChineseHeading1']))
    story.append(Spacer(1, 0.3*cm))

    sources_text = """
        <b>核心研究笔记</b>
        <br/>• llm_early_development_history.md - 早期发展历史（2017-2020）
        <br/>• gpt_series_evolution_comprehensive.md - GPT系列全面研究
        <br/>• llm_competition_and_open_source_ecosystem.md - 竞争格局与开源生态
        <br/>• llm_challenges_future_development.md - 技术挑战与未来发展方向
        <br/>• scaling_law_fundamentals.md - 缩放定律基础理论

        <b>核心论文</b>
        <br/>• Vaswani et al. (2017). "Attention Is All You Need". arXiv:1706.03762
        <br/>• Kaplan et al. (2020). "Scaling Laws for Neural Language Models". arXiv:2001.08361
        <br/>• Hoffmann et al. (2022). "Training Compute-Optimal Large Language Models". NeurIPS 2022
        <br/>• Brown et al. (2020). "Language Models are Few-Shot Learners". arXiv:2005.14165

        <b>市场研究机构</b>
        <br/>• MarketGrowthReports - 全球LLM市场规模数据
        <br/>• The Business Research Company - 企业级LLM市场预测
        <br/>• IDC - 中国大模型平台市场份额
        <br/>• Frost & Sullivan - 中国大厂商收入排名
        <br/>• Stanford HAI AI Index Report 2025

        <b>基准测试平台</b>
        <br/>• MMLU (Massive Multitask Language Understanding)
        <br/>• LMSYS Chatbot Arena - 开放LLM排行榜
        <br/>• Vectara FaithJudge - 幻觉率基准
        <br/>• Epoch AI - 趋势数据库
    """

    story.append(Paragraph(sources_text, styles['ChineseBody']))
    story.append(Spacer(1, 1*cm))

    # 免责声明
    disclaimer = """
        <b>免责声明</b>：本报告基于公开可用信息整理，部分数据为估计值。AI领域发展迅速，
        某些结论可能在短期内被修正。建议定期更新数据以保持准确性。
        数据时间跨度：2017-2025年，报告生成日期：2025年12月29日。
    """

    story.append(Paragraph(disclaimer, styles['ChineseBody']))

def generate_pdf():
    """生成完整的PDF报告"""
    # 设置中文字体
    chinese_font = setup_chinese_fonts()

    # 创建PDF文档
    output_path = '/Users/a/Desktop/xinao/reborn1000/build_sell_invest/claude-agent-sdk-demos/research-agent/files/reports/llm_development_history_report.pdf'

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    # 创建样式
    styles = create_custom_styles(chinese_font)

    # 创建内容容器
    story = []

    # 生成各个部分
    create_cover_page(story, styles)
    create_executive_summary(story, styles)
    create_section_early_development(story, styles)
    create_section_gpt_evolution(story, styles)
    create_section_competition(story, styles)
    create_section_technical_challenges(story, styles)
    create_section_future_trends(story, styles)
    create_visual_charts_section(story, styles)
    create_sources_section(story, styles)

    # 构建PDF
    try:
        doc.build(story)
        print(f"PDF报告生成成功！")
        print(f"输出路径: {output_path}")
        return output_path
    except Exception as e:
        print(f"生成PDF时出错: {e}")
        return None

if __name__ == "__main__":
    generate_pdf()
