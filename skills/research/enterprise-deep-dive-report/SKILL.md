---
description: 生成投行级企业深度研究报告。首发即深度（1200行以上50表格以上），Web搜索Doris DAAS可比交易法强制标配。7篇37章结构，真实财务数据驱动。
name: enterprise-deep-dive-report
triggers:
- 企业分析报告
- 投行报告
- 企业尽调
- 深度研究报告
- 100页报告
- 投资研究报告
- 企业研究报告
version: 5.1.0
author: 凭安智能体
license: MIT
metadata:
  hermes:
    tags: [research, enterprise, investment-banking, due-diligence, doris-daas, pdf, financial-analysis, comparable-transactions, real-financial-data]
    related_skills: [doris-daas-query, enterprise-risk-analysis-report]
---

# 企业深度研究报告生成

## 概述

为企业生成投行级深度分析报告（Markdown + PDF）。**🔴 首发即深度：不再存在"先薄后厚"模式。每份报告首次交付就必须达到凌度智能报告的深度级别（1,200+行表格式、50+表格、全维度覆盖）。**

**参考标杆：** `凌度智能_投资研究报告.pdf`（2,053行，全维度深度）。所有后续报告以此为最低标准。

**核心原则：** 真实财务数据为中枢，覆盖完整 P&L 趋势、资产负债表分析、ROE 杜邦分解、经营杠杆分析、盈亏平衡建模、烧钱率与现金跑道、真实数据驱动的三情景估值。Web 搜索 + Doris DAAS + 可比交易法是**标配，不是可选增强**。

**触发关键词：** 企业分析、投行报告、尽调、深度研究、"分析 XX 公司"、对标分析、估值报告。

## 触发场景

- 用户要求"分析 XX 公司"
- 用户要求"生成 XX 公司的投行报告/尽调报告"
- 用户指定"不少于100页"等篇幅要求
- 用户要求同时分析多家企业并输出PDF

## 工作流

### Phase 0: 触发深度检查（🔴 每次必执行）

在开始任何数据采集前，先确认本次报告必须达到的深度标准：

| 检查项 | 标准 | 不合规后果 |
|--------|------|------|
| 目标行数 | ≥1,800行（上市公司）/ ≥1,500行（非上市） | 禁止交付 |
| 数据表格数 | ≥50个 | 禁止交付 |
| "分析："段落数 | ≥30个（每表必配） | 禁止交付 |
| "关键发现："callout | ≥15个 | 警告 |
| Web搜索 | ≥5次 | 禁止进入Phase 3 |
| Doris DAAS | ≥5张表 | 禁止进入Phase 3 |
| 可比交易法 | 至少2个案例 | 禁止交付 |

> **行数说明：** 1,200行为表格式投行风格的最低标准。若采用叙事风格需1,800+行。表格式每行=1数据点，叙事式每行=1论点，密度不同。按内容完整性判断，非机械行数。

### Phase 1: 数据采集（三阶段🔴强制全部执行）

**⚠️ 废除"先薄后厚"模式。以下三个阶段全部为强制性，禁止只做第一阶段。**

#### Stage 1A: MCP API 全量采集（32类 + 上市公司专项）

| 层级 | 类别 | MCP 工具 | 说明 |
|------|------|------|------|
| **基础** | 工商信息 | `mcp_data_query_get_company_info` | 统一信用码、注册资本、法人、经营范围 |
| **基础** | 股东结构 | `mcp_data_query_get_company_partner` | 股东名称、出资比例、实缴情况 |
| **基础** | 高管团队 | `mcp_data_query_get_company_employee` | 董监高任职 |
| **基础** | 行业分类 | `mcp_data_query_get_company_industry` | 国民经济+战新产业分类 |
| **基础** | 变更记录 | `mcp_data_query_get_company_changes` | 历史变更全景 |
| **基础** | 资质证书 | `mcp_data_query_get_company_cert` | ISO、许可等 |
| **基础** | 荣誉资质 | `mcp_data_query_get_company_honor` | 高新、专精特新等 |
| **基础** | 对外投资 | `mcp_data_query_get_company_investment` | 子公司/参股 |
| **基础** | 实控人 | `mcp_data_query_get_company_controller` | 实际控制人 |
| **基础** | 受益所有人 | `mcp_data_query_get_company_beneficial_owner` | UBO，控制路径链路 |
| **基础** | 风险扫描 | `mcp_data_query_search_company_risk` | 自身/关联/历史风险 |
| **基础** | 新闻舆情 | `mcp_data_query_search_news` | 媒体报道 |
| **基础** | 科创总分 | `mcp_sti_evaluate_sti_capability` | STI评分+等级+排名 |
| **基础** | 专利 | `mcp_sti_search_patent` | 专利列表 |
| **基础** | 软著 | `mcp_sti_search_software_copyright` | 软件著作权 |
| **基础** | 商标 | `mcp_sti_search_trademark` | 商标信息 |
| **基础** | 年报 | `mcp_data_query_search_annual_report` | 社保人数、资产数据 |
| **基础** | 招投标 | `mcp_bid_search_company_winning_bid` | 中标记录 |
| **基础** | 融资记录 | `mcp_data_query_search_funding_record` | 融资轮次 |
| **基础** | 企业简介 | `mcp_data_query_get_company_introduction` | 官方介绍 |
| **增强** | 股权穿透(下) | `mcp_data_query_pierce_equity` (direction=0) | 向下子公司链 |
| **增强** | 股权穿透(上) | `mcp_data_query_pierce_equity` (direction=1) | 向上股东链（含国资穿透） |
| **增强** | STI创新投入 | `mcp_sti_get_sti_invest_score` | 发明人数量/融资/团队稳定性 |
| **增强** | STI创新产出 | `mcp_sti_get_sti_output_score` | 专利数/软著/高价值/战新 |
| **增强** | STI创新质量 | `mcp_sti_get_sti_quality_score` | 专利评分/估值/许可/质押 |
| **增强** | STI创新影响 | `mcp_sti_get_sti_influence_score` | 被引证/标准参与/PCT/海外 |
| **增强** | STI创新成长 | `mcp_sti_get_sti_develop_score` | 增速/奖项/活跃度趋势 |
| **增强** | 供应商 | `mcp_data_query_search_supplier` | 采购金额/占比/关联关系 |
| **增强** | 购地 | `mcp_data_query_search_land_purchase` | 固定资产规模 |
| **增强** | 招聘 | `mcp_data_query_search_recruitment` | 岗位类型→业务方向判断 |
| **增强** | 进出口信用 | `mcp_data_query_search_import_export_credit` | 海关信用/出海评估 |
| **增强** | 税务信用 | `mcp_data_query_search_tax_credit` | 纳税评级 |
| **增强** | 企业规模 | `mcp_data_query_get_company_scale` | 大/中/小/微 |
| **辅助** | 标准参与 | `mcp_sti_search_standard` | 行业标准话语权 |
| **辅助** | 网站备案 | `mcp_sti_search_website_icp` | 线上业务布局 |
| **辅助** | 业务信息 | `mcp_data_query_search_business_info` | 产品/品牌/融资轮次 |
| **辅助** | 发票抬头 | `mcp_data_query_search_invoice_title` | 开户行/资金流信息 |
| **辅助** | 推广记录 | `mcp_data_query_search_advertise_record` | 市场投放策略 |

**风险详查（高风险企业）：** 当风险扫描发现 >50 项风险时，追加逐类详查：
- 裁判文书: `mcp_data_risk_search_lawsuit`
- 被执行人: `mcp_data_risk_search_executed_person`
- 失信: `mcp_data_risk_search_dishonest_executed_person`
- 限高: `mcp_data_risk_search_high_consumption_restriction`
- 终本: `mcp_data_risk_search_end_execute_case`
- 行政处罚: `mcp_data_risk_search_punishment`
- 经营异常: `mcp_data_risk_search_abnormal_operation`
- 欠税: `mcp_data_risk_search_tax_arrears`
- 股权出质: `mcp_data_risk_search_equity_pledge`

**行业对标（并行查询）：** 确定可比上市公司后：
1. `mcp_query_onmarket_lookup_symbol` — 查股票代码
2. `mcp_query_onmarket_get_quote_snapshot` — 获取股价/市值快照
3. `mcp_query_onmarket_research_fundamentals` — 营收/利润/毛利率/ROE等完整财务
4. `mcp_data_listed_search_annual_stock_indicator` — 历年财务指标序列

#### Stage 1B: 🔴 Web 搜索（强制 — 每次必做，不可跳过）

使用 `mcp_baidu_web_search_mcp_server_webSearch` 至少执行以下 5 类搜索。**这些不是"增强章节"，是报告标配。**

| # | 搜索主题 | 搜索关键词示例 | 对应报告章节 |
|:--:|------|------|------|
| 1 | **TAM/SAM/SOM 市场空间** | "{行业} 市场规模 2025 2026"、"{行业} 市场研究报告" | 行业市场规模 |
| 2 | **可比交易/并购案例** | "{赛道} 融资 并购 案例 2023 2024 2025" | 可比交易估值 |
| 3 | **国际竞争对手对标** | "{行业} 海外 公司 营收 估值"、"{英文赛道} market size" | 国际对标 |
| 4 | **产业链利润分配** | "{行业} 上游 中游 下游 毛利率"、"{上游关键词} 上市公司 毛利率" | 产业链利润分配 |
| 5 | **管理层背景** | "{创始人} {公司} 履历"、"{公司} 创始人 背景" | 管理层能力矩阵 |

**搜索量要求：** 每类至少 1 次搜索，合计 ≥5 次。上市公司额外搜索：
- "{股票代码} 研报 评级 目标价" — 获取券商覆盖
- "{行业} 可比公司 估值 PE PS" — 估值乘数对标
- "{行业} 政策 2025 2026" — 最新政策环境

#### Stage 1C: 🔴 Doris DAAS（强制 — 每次必做，不可跳过）

```python
conn = pymysql.connect(host='10.9.17.20', port=9030, user='openapi',
    password='Ekaj3T4!', database='daas', charset='utf8mb4')
```

**必查表（≥5张）：**

| 表名 | 用途 | 报告对应章节 |
|------|------|------|
| `opt_company_intellectual_property_index` | IP 指数全景（163+指标：转让/许可/质押/被引/海外/PCT/有效比） | 知识产权深度分析 |
| `opt_government_award_subsidy` | 政府补贴明细（部门/金额/年度/类型） | 政府补贴与政策红利 |
| `tb_company_financing` | 融资事件（轮次/投资方/金额/日期） | 融资历程深度分析 |
| `tb_company_group` | 企业族群/集团归属 | 集团生态分析 |
| `opt_ent_scale_tag` | 企业规模年度标签（大/中/小/微） | 企业规模升级路径 |
| `opt_company_label_potential_01` | 潜力标签（专精特新/高企/创新等入库状态） | 企业资质标签 |
| `ads_bid_win_candidate_out` | 中标金额汇总 | 中标金额交叉验证 |
| `ip_patent` | 专利IPC分类明细 | 专利IPC聚类分析 |

**⚠️ Doris 列名陷阱：** 技能文档中的列名可能与实际表结构不同。已在 `references/daas-column-mappings.md` 中记录实测列名（company_name→entName、year→publish_year、applicant→applicant_name、total_amount→amount 等）。查询前先参考该文件。

## 报告质量铁律（🔴 强制 — 违反将导致报告被拒）

### 格式严禁清单

| 禁止项 | 示例 | 为什么 |
|--------|------|--------|
| 字母编号章节 | `## A.1`、`## B.2`、`## D.1` | 破坏统一结构，目录不协调 |
| 版本标记 | `V4`、`v5`、`V3.0` | 报告是独立文档，不是 changelog |
| 迭代前缀 | `## 新增章节A`、`## 【新增】`、`## ★新增`、`## 【增强】` | 暴露后加痕迹 |
| 装饰分隔符 | `═══`、`███`、`# 模块（2026年更新）` | 非专业格式 |
| 日期重复 | 两处以上 `**报告日期：**` | 残留痕迹 |
| TOC 版本标记 | `-v4新增`、`★新增§34` | 目录也需清洁 |
| 空标题 | 孤立的 `#` 或 `##` 行 | 排版不整 |
| 元注释 | `本节为后续补充`、`初版→升级见第45章` | 读者不需要知道版本史 |

### 内容必须清单

| 要求 | 说明 |
|------|------|
| 财务数据标注来源 | `tb_annual_report_2`（企业自行申报的税务数据） |
| 财务异常注明 | empNum 与社保不一致时标注"数据矛盾" |
| 目录行间距一致 | 所有条目之间统一间距，无额外空行 |
| 章节编号连续 | 从 1 开始不间断递增 |
| 真实数据优先 | 已有实际数据时，禁止用行业均值替代 |
| 读起来像一次性成稿 | 无任何迭代痕迹 |

### 🔴 交付前自检

生成 PDF 前对 MD 文件执行以下检查：

```python
import re
content = Path('report.md').read_text()
lines = len(content.split('\n'))
assert content.count('**报告日期') == 1, '日期重复'
assert not re.search(r'^## [A-Z]\.', content, re.MULTILINE), '字母编号残留'
assert not re.search(r'^#.*新增', content, re.MULTILINE), '标题含新增'
assert not re.search(r'【新增】|【增强】|★新增|补充章节|版本新增', content), '版本痕迹'
assert not re.search(r'V\d\.\d', content), '版本号残留'
assert not re.search(r'^#\s*$', content, re.MULTILINE), '空标题'

# 🔴 深度门禁
table_count = len(re.findall(r'^\\|[-|]+\\|$', content, re.MULTILINE)) // 2
analysis_count = len(re.findall(r'分析[：:]', content))
keyfinding_count = len(re.findall(r'关键发现', content))
assert lines >= 1800, f'行数不足: {lines} < 1800（禁止交付）'
assert table_count >= 50, f'表格不足: {table_count} < 50（禁止交付）'
assert analysis_count >= 30, f'"分析"段落不足: {analysis_count} < 30（禁止交付）'
assert '可比交易' in content, '缺失可比交易法（禁止交付）'
assert 'TAM' in content or '市场规模' in content, '缺失市场规模分析（禁止交付）'
assert '产业链' in content and '利润分配' in content, '缺失产业链分析（禁止交付）'
assert '管理层' in content and '矩阵' in content, '缺失管理层能力矩阵（禁止交付）'
print(f'✅ 深度门禁通过: {lines}行/{table_count}表/{analysis_count}分析段落/{keyfinding_count}关键发现')
```



### 🔴 全维度必备章节（15类 — 非可选，每次报告必含）

以下章节通过 Stage 1B Web搜索 + Stage 1C Doris DAAS 获取数据，**是报告标配，不是"增强"**：

| 必备章节 | 数据来源 | 核心内容 |
|------|------|------|
| **TAM/SAM/SOM 量化建模** | Web Search | 全球→中国→目标份额三层市场空间测算 |
| **可比交易法** | Web Search | 近2-3年同行业融资/并购案例→PS/PE/EV乘数→估值区间 |
| **国际竞争对手对标** | Web Search | 海外同赛道公司营收/估值/融资→估值锚 |
| **产业链利润分配** | Web Search | 上游→中游→下游利润率对比→议价能力定位 |
| **管理层能力矩阵** | Web Search | 创始人履历→技术/商业/管理/资本/合规5维评分 |
| **客户集中度分析** | Web Search | Top3/Top5客户占比→信用风险→单一客户依赖 |
| **政府补贴与政策红利** | `opt_government_award_subsidy` (Doris) | 补贴趋势/部门/金额/类型 |
| **IP 指数深度分析** | `opt_company_intellectual_property_index` (Doris) | 转让/许可/质押/被引/海外/PCT |
| **融资历程深度** | `tb_company_financing` (Doris) | 轮次/投资方/金额/估值 |
| **中标金额交叉验证** | `ads_bid_win_candidate_out` (Doris) | 中标金额→年化营收推演 |
| **专利 IPC 聚类分析** | `ip_patent` (Doris) + IPC字典 | IPC分类聚类→核心技术域→壁垒 |
| **企业规模升级路径** | `opt_ent_scale_tag` (Doris) | 微型→小型→中型追踪 |
| **行业密度与竞争位势** | Doris JOIN | 同城同行业大盘统计 |
| **企业族群/集团生态** | `tb_company_group` (Doris) | 集团归属/成员网络 |
| **IPO路径逐条对标** | Web Search | 科创板/北交所标准check→差距→时间表 |


**最终版报告结构（7篇37章，无版本痕迹）：**

**🔴 唯一报告结构。所有报告严格按此执行：**

```
第一篇：执行摘要 (1-3章)
  1. 投资结论
  2. 核心指标卡
  3. 投资亮点与风险摘要

第二篇：公司基本面 (4-9章)
  4. 工商登记与基础信息
  5. 股权结构与穿透分析
  6. 实际控制人与受益所有人
  7. 管理层与治理结构
  8. 历史沿革
  9. 集团架构与子公司

第三篇：业务与市场 (10-17章)
  10. 主营业务与产品矩阵
  11. 商业模式
  12. 技术壁垒与知识产权
  13. 行业格局（全球→全国→细分三层）
  14. 竞争格局
  15. 可比公司分析
  16. 波特五力模型
  17. SWOT分析

第四篇：财务分析 (18-24章)
  18. 财务数据概览（完整历年P&L表）
  19. 营收与盈利分析（CAGR/净利率趋势/杜邦分解）
  20. 资产负债分析（D/E趋势/偿债能力）
  21. 现金流与融资分析（烧钱率/现金跑道）
  22. 财务数据可信度评估（⚠️ 必含）
  23. 财务异常标注与分析
  24. 盈亏平衡/产能模型

第五篇：创新与成长 (25-28章)
  25. 科创能力综合评估
  26. 创新投入与产出
  27. 创新质量与影响力
  28. 成长性与政策红利

第六篇：风险分析 (29-32章)
  29. 风险全景矩阵
  30. 财务风险（资不抵债/杠杆/流动性）
  31. 经营与法律风险
  32. 行业与竞争风险

第七篇：估值与建议 (33-37章)
  33. 估值方法论
  34. DCF估值（三情景）
  35. 可比公司/交易估值
  36. 综合估值区间与投资评级
  37. 退出路径与IPO可行性

附录 (A-D)
  A. 专利清单
  B. 工商变更记录
  C. 财务数据详表
  D. 免责声明
```

**🔒 必含章节：第22章「财务数据可信度评估」**

每份报告必须在财务分析篇中包含数据可信度评估，格式如下：

| 数据层级 | 来源 | 可信度 | 说明 |
|----------|------|:--:|------|
| 财务数据 | tb_annual_report_2 | ⚠️ 中 | 企业自行申报，未经审计 |
| 工商/股权 | 国家企业信用信息公示系统 | ✅ 高 | 官方登记 |
| IP | 国家知识产权局 | ✅ 高 | 官方授权 |
| 司法 | 裁判文书网 | ✅ 高 | 官方司法 |

异常标注要求：
- empNum=1但社保人数远超时 → 标注"空壳申报"
- empNum与社保人数差距>20%时 → 标注"数据矛盾"
- 净利年度波动>3倍时 → 标注"异常波动"并分析原因

### Phase 2: 报告撰写（主智能体定稿）

🔴 主智能体直接撰写完整 MD 文件，使用 `write_file` 或 `execute_code`。

**写作规则（🔴 强制 — 对标凌度标杆报告）：**

### 每表必配"分析"段落

**每张数据表格后，必须跟一段 100-300 字的"分析："段落。** 分析段落要求：
- 不能只是一句话点评（"从上表可以看出..."），必须展开推理链
- 必须解读数据背后的含义、趋势、异常
- 必须将数据与行业对标、公司战略、竞争格局关联
- 格式：`分析：[100-300字深度解读]`

**示例（凌度标杆风格）：**

> 分析：凌度智能的142件专利转出是极其罕见的数据。这暗示公司可能采取"研发-授权-转让"的IP商业化模式，通过专利许可形成第二收入曲线。6.75%的对外许可率在机器人初创企业中属于较高水平。对比同行业均值（<2%），凌度的IP运营能力显著领先。但大量专利转出也意味着核心技术的控制力下降——投资者需关注转出专利是否涉及核心算法。

### "关键发现"callout

**每 5-8 张表格，插入一个"关键发现："callout。** 整份报告至少 15 处关键发现。
- 格式：`**关键发现：** [一句话核心洞察]`
- 用于突出数据中最重要的发现，引导读者注意力

### 数据交叉验证

**多个数据源交集处，必须做交叉验证推演。** 示例：
- 中标金额 ÷ 平均单价 → 推算年化营收 → 与Doris财务数据交叉验证
- 招聘岗位类型 × 招聘数量 → 推算业务方向 → 与中标项目类型交叉验证
- 社保人数趋势 × 人均营收 → 推算营收区间 → 与财务数据交叉验证

### 禁止简短点评

| 禁止（我们之前的写法） | 要求（标杆写法） |
|------|------|
| "专利为纯防御性持有，未商业化运营。" (16字) | 展开为 100-200 字分析：对比行业均值、分析原因、推理商业影响 |
| "毛利率58.9%在软件同业中属于上等水平。" (18字) | 对比3家同业具体数字、分析高毛利来源、评估可持续性 |
| "资产负债率极低，几乎无银行借款。" (15字) | 量化分析负债结构、与IPO前后对比、评估财务弹性 |

### Phase 3: PDF 生成

**推荐方案：execute_code + subprocess 调用 Puppeteer**

当 MD 文件较大（>50KB）时，HTML 内容无法通过 `generate_pdf` 工具参数直接传递。使用 `execute_code` 中通过 subprocess 调用：

```python
from pathlib import Path
import subprocess, sys, markdown

base = Path('/home/pingan/.hermes/profiles/0ipkw091isket7zlis540eqtwieie/workspace')

template = '''<!DOCTYPE html><html lang="zh-CN">
<head><meta charset="utf-8">
<style>
  @page {{ size: A4; margin: 16mm; }}
  body {{ font-family: 'AlibabaPuHuiTi-3-55-Regular', 'SimSun', serif; font-size: 10pt; line-height: 1.7; color: #222; }}
  h1 {{ font-size: 19pt; text-align: center; border-bottom: 3px solid #1a5276; padding-bottom: 10px; margin-top: 28px; }}
  h2 {{ font-size: 14pt; color: #1a5276; border-bottom: 1.5px solid #ccc; padding-bottom: 5px; margin-top: 22px; }}
  h3 {{ font-size: 12pt; color: #2c3e50; margin-top: 16px; }}
  table {{ border-collapse: collapse; width: 100%; margin: 10px 0; font-size: 8pt; page-break-inside: avoid; }}
  th {{ background-color: #1a5276; color: white; padding: 6px 5px; text-align: center; }}
  td {{ border: 1px solid #ddd; padding: 4px 5px; }}
  tr:nth-child(even) {{ background-color: #f2f6fa; }}
  strong {{ color: #1a5276; }}
  blockquote {{ border-left: 4px solid #1a5276; padding: 6px 14px; background: #f0f4f8; margin: 10px 0; }}
  pre {{ font-size: 7.5pt; line-height: 1.35; background: #f5f5f5; padding: 8px; border-radius: 3px; overflow-x: auto; }}
  hr {{ border: 1px solid #1a5276; margin: 18px 0; }}
  p {{ margin: 5px 0; text-align: justify; }}
  ul, ol {{ margin: 4px 0; padding-left: 20px; }}
  li {{ margin: 2px 0; }}
</style></head><body>{body}</body></html>'''

for name in ['企业A', '企业B', '企业C']:
    md_path = base / f'report_{name}.md'
    content = md_path.read_text(encoding='utf-8')
    
    # 1. Markdown → HTML
    html_body = markdown.markdown(content, extensions=['tables', 'fenced_code'])
    html_doc = template.replace('{body}', html_body)
    
    pdf_path = base / f'report_{name}.pdf'
    
    # 2. HTML → PDF via puppeteer (subprocess to avoid parameter size limits)
    script = '''
import sys
sys.path.insert(0, '/home/pingan/hermes-agent')
from tools.pdf_tool import generate_pdf_with_puppeteer
import json
html_content = sys.stdin.read()
result = generate_pdf_with_puppeteer(html_content, sys.argv[1])
print(json.dumps(result))
'''
    proc = subprocess.run(
        [sys.executable, '-c', script, str(pdf_path)],
        input=html_doc,
        capture_output=True,
        text=True,
        timeout=120
    )
    print(f"{name}: {'✅' if proc.returncode == 0 else '❌'} {pdf_path.stat().st_size/1024/1024:.1f}MB")
```

**备选方案：** 如果 MD 文件较小（<30KB），可直接使用 `generate_pdf` 工具传入 HTML 字符串。

**前置条件：** `pip install markdown`（Python markdown 库，支持 `tables` 和 `fenced_code` 扩展）

### Phase 4: 文件交付

- MD 文件保存在 `workspace/report_{企业简称}.md`
- PDF 文件保存在 `workspace/report_{企业简称}.pdf`
- 使用 `MEDIA:` 路径在消息中发送文件

### 用户偏好

用户徐生偏好直接、精简的交付方式。报告完成后简短汇总核心发现，直接发送 MEDIA 文件。不主动推销。

**⚡ 批量执行模式**：当用户问"还可以做什么优化"时，列出优化项后直接全部执行——不要逐一询问确认。用户会回复"都做"/"全部一起"/"做"。（🔴 强制）

**教训：** 子智能体重写报告会丢失已完成版本的深度和细节。用户实测反馈子智能体的"终极版"只有 V4 一半的深度。

| 做法 | 结果 | 评价 |
|------|------|:--:|
| 用 `delegate_task` 让子智能体从零写报告 | 958行 vs 原版2053行 | ❌ 丢失深度 |
| 用 Python `str.replace` 向已有报告插入新章节 | 保留全部深度+追加新数据 | ✅ 推荐 |

**⚠️ 为什么不能用 delegate_task 写最终版报告**

本会话实测教训：让子智能体按"全新结构"重写已有报告，输出行数从 2000+ 腰斩到 900-1200 行。原因：
- 子智能体有 token 和 context 限制，无法持有一份 2000 行报告的完整上下文
- 子智能体倾向于"总结"而非"展开"，丢失深度分析
- 子智能体写作风格不稳定，可能偏离投行风格

**结论**：`delegate_task` 仅用于 Phase 1 数据采集和 Phase 2 Web 研究搜索。Phase 2 报告定稿 + Phase 3 PDF 生成始终由主智能体完成。

## 注意事项

### 🔴 报告撰写原则：主智能体定稿，子智能体只采集

**已在本会话实测验证**：`delegate_task` 子智能体写的最终版报告行数只有主智能体累积版的 35-50%。

| 角色 | 负责 | 禁止 |
|------|------|------|
| `delegate_task` 子智能体 | Stage 1A MCP采集 + Stage 1B Web搜索 | ❌ 写最终版报告 |
| 主智能体（你） | Phase 2 报告定稿 + Phase 3 PDF生成 | ❌ 串行采集20+API |

操作模式：用 `execute_code` 读入已有MD → Python清理/注入数据 → `write_file` 写回。

详见 `references/anti-pattern-delegate-for-finals.md`。


### 数据质量陷阱

> ⚠️ 完整陷阱实录见 `references/api-pitfalls.md`（5个陷阱：不相关同业/BS数据误解/中标截断/年报空值/label解码）

**陷阱1：`research_industry` 返回不相关同业（2026-06 实测）**

`mcp_query_onmarket_research_industry` 基于申万行业分类选取可比公司。对于垂直赛道（如财政IT、政务软件），申万"软件和信息技术服务业"一级行业下有5,525家上市公司——自动返回的"peers"可能完全不相关。中科江南实测案例：返回了安徽凤凰（920000.BJ，汽车零部件企业）。

**正确做法：** 不依赖该 API 的 peers 字段。手动选择真正同赛道的可比公司（如博思软件300525、远光软件002063），然后用 `get_quote_snapshot` + `research_fundamentals` 逐家查询。

**陷阱2：`research_fundamentals` BS/CF 数据在 compact 模式为同比变化率**

`mcp_query_onmarket_research_fundamentals` 在 compact 响应模式下，资产负债表(BS)和现金流量表(CF)的数值是**同比百分比变化**而非绝对金额。例如 `total_assets: -1.095205` 表示资产总额同比下降1.1%，不是资产为-1.1亿。

**正确做法：** 利润表(IS)和比率(ratios)在 compact 模式下是绝对值，可直接使用。BS/CF 数据需切换到 standard 或 detail 模式获取绝对值，或使用 `mcp_data_listed_search_annual_stock_indicator` 获取历年财务指标（该接口返回绝对值）。

**陷阱3：中标数据返回量极大**

`mcp_bid_search_company_winning_bid` 对活跃企业可能返回数千条记录（中科江南3,667条），compact 响应会被截断（本次会话返回被截断为3,460,248字符）。

**正确做法：** 只取 `page_index=1` 的前几条中标记录确认活跃度即可，或使用 `execute_code` 解析截断数据中的总量和省份分布统计。

### 数据限制

**🚨 关键发现：不要相信"企业选择不公示"**

MCP `mcp_data_query_search_annual_report` 接口对非上市公司的财务数据显示为"企业选择不公示"。但这**不代表数据不存在**。

Doris DAAS 的 **`tb_annual_report_2`** 表包含所有企业的完整年报财务数据，字段如下：

| 字段 | 含义 | 用途 |
|------|------|------|
| `anCheYear` | 年报年度 | 时间序列 |
| `empNum` | 从业人数 | 人均产值计算 |
| `vendInc` / `vendIncEtl` | 营业总收入 | P&L核心 |
| `maiBusInc` / `maiBusIncEtl` | 主营业务收入 | 业务集中度 |
| `netInc` / `netIncEtl` | 净利润 | 盈利能力 |
| `proGro` / `proGroEtl` | 营业利润 | 经营效率 |
| `assGro` / `assGroEtl` | 资产总额 | 规模 |
| `totEqu` / `totEquEtl` | 净资产（所有者权益） | 偿付能力 |
| `liaGro` / `liaGroEtl` | 负债总额 | 杠杆率 |
| `ratGro` / `ratGroEtl` | 纳税总额 | 税务合规 |

> **注意：** 部分年份 `vendInc` 可能为 NULL 但 `vendIncEtl` 有值（或反之）。查询时使用 `COALESCE(vendInc, vendIncEtl)` 取非空值。`assGroDis=0` 表示企业选择不公示，但 `assGro` 和 `assGroEtl` 字段仍可能有数据——Doris 从税务申报端获取了数据。

**财务分析核心指标：**
- 营收 CAGR / 净利率趋势 / ROE 杜邦分解
- 负债率变化 + 经营杠杆系数
- 盈亏平衡点 = 固定成本 / (1 - 变动成本率)
- 现金跑道(月) = 净资产 / (|年均烧钱率| / 12)
- 人均产值 = 营收 / 员工数

详见 `references/tb-annual-report-2-schema.md`。

**其他限制：**
- 供应商/购地/发票等辅助数据对非上市中小企业通常为空，不影响报告质量
- 零司法风险本身是重要积极信号
- STI 五维评分 + 专利数 + 标签（专精特新/高新） + **真实财务数据** = 核心评估维度

### PDF 生成陷阱

- `generate_pdf` 工具参数的 content 字段有大小限制（~30KB），大报告（>50KB MD）需通过 `execute_code` + subprocess 方式渲染
- `execute_code` 中的 `read_file` 返回 dict（不是直接字符串），用 `Path.read_text()` 代替
- Python `markdown` 库的 `content` key 问题：`read_file(path)['content']` 在某些版本不可靠，直接用 `pathlib` 更稳定
- `markdown.markdown()` 必须显式传 `extensions=['tables', 'fenced_code']`，否则表格和代码块渲染异常
- `font-family` 必须包含中文字体 fallback：`'AlibabaPuHuiTi-3-55-Regular', 'SimSun', serif`，否则 PDF 中文显示为方块
- ```` @page { size: A4; margin: 16mm; } ```` 中的双花括号是 CSS 语法，写入 Python f-string 时不需要转义
- 渲染前确认 `pip install markdown` 已完成（通常已安装），无 matplotlib 不影响 PDF 渲染

### 🔴 首发深度铁律（2026-06 血泪教训）

**旧模式（已废除）：** 首发 500-800 行薄报告 → 用户问"还可以优化" → 迭代到 2000+ 行

**新模式（🔴 强制）：** 首发即 1,800+ 行，包含 Web 搜索、Doris DAAS、可比交易法全部章节。

**中科江南失败案例（2026-06-09）：**
- 按旧模式首发：857行，缺失 Web 搜索（可比交易/TAM/国际对标）、Doris DAAS（IP指数/补贴/融资/标签）、产业链分析、管理层矩阵
- 用户反馈：不如凌度报告（2,053行）
- 根因：技能文件把 Web 搜索和 Doris 写成"可选增强"，执行时全部跳过
- 详见 `references/deep-first-pass-mandate.md`

**🔴 新标准：**
- 最小行数：1,200行（表格式）/ 1,800行（叙事式）
- 必含章节：Web搜索≥5次产生的章节 + Doris≥5张表产生的章节 + 可比交易法
- 交付前：行数不达标 → 拒绝交付，补全数据后重写

### 🔴 多企业报告一致性（本次会话血泪教训）

当并行处理多家企业时，不同子智能体生成的报告质量和结构差异极大。本次会话中：

| 企业 | 首次子智能体版 | 深度版 | 差异 |
|------|:--:|:--:|:--:|
| 凌度 | 958行 | 2,053行 | 主智能体深度打磨 |
| 联信 | 731行 | 1,882行 | 子智能体基底薄弱 |
| 莱迪 | 672行 | 1,563行 | 子智能体基底薄弱 |

**根因**：凌度的深度版由主智能体迭代了 N 轮达到极致深度，而联信和莱迪的深度版由不同子智能体生成，深度先天不足。

**修复方法**：
1. 生成三份报告后，对比行数/H2数/表格数/维度覆盖
2. 如果某份报告行数比最厚的少 20% 以上，**重建它**（用最厚报告的 delegate_task context 模板 + 该企业的完整数据）
3. 重建时在 context 中明确：`"匹配凌度报告的深度，目标 2000+ 行、50+ 章节"`
4. 交付前统一验证三份报告的维度完整性

**验证脚本**（见 `references/report-quality-checklist.md`）。修改技能文件后，运行 `python references/skill-self-check.py SKILL.md` 进行自动化一致性检查。
