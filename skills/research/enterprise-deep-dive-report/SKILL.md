---
description: 生成投行级企业深度研究报告。八部结构，真实财务数据驱动，覆盖工商/股权/UBO/知识产权/STI五维/财务/风险/估值全维度。支持Doris DAAS+32类MCP API+上市公司对标+可比交易法。
name: enterprise-deep-dive-report
triggers:
- 企业分析报告
- 投行报告
- 企业尽调
- 深度研究报告
- 100页报告
- 投资研究报告
- 企业研究报告
version: 4.0.0
author: 凭安智能体
license: MIT
metadata:
  hermes:
    tags: [research, enterprise, investment-banking, due-diligence, doris-daas, pdf, financial-analysis]
    related_skills: [doris-daas-query, enterprise-risk-analysis-report]
    tags: [research, enterprise, investment-banking, due-diligence, doris-daas, pdf, comparable-transactions, real-financial-data]
    related_skills: [doris-daas-query, enterprise-risk-analysis-report]
---

# 企业深度研究报告生成

## 概述

为企业生成投行级深度分析报告（Markdown + PDF），支持 V1→V5 五级渐进升级。**V5.0 核心突破：`tb_annual_report_2` 表包含所有企业（含非上市）的真实年报财务数据**——营收、净利、总资产、净资产、负债、所得税、员工数全部可查。此前"非上市财务不公示"的假设彻底失效。

V5 报告以真实财务数据为中枢，包含：完整 P&L 趋势、资产负债表分析、ROE 杜邦分解、经营杠杆分析、盈亏平衡建模、烧钱率与现金跑道、真实数据驱动的三情景估值。

**触发关键词：** 企业分析、投行报告、尽调、深度研究、"分析 XX 公司"、对标分析、估值报告。

## 触发场景

- 用户要求"分析 XX 公司"
- 用户要求"生成 XX 公司的投行报告/尽调报告"
- 用户指定"不少于100页"等篇幅要求
- 用户要求同时分析多家企业并输出PDF

## 工作流

### Phase 1: 数据采集（两阶段并行）

**策略：** 对于 >1 家企业，使用两次 `delegate_task` 并行：
- **第一阶段（数据采集）**：3 个子智能体各负责一家企业的数据采集，每个调用 20-30 个 API，返回结构化 JSON 摘要（不做报告撰写，避免 600s 超时）。
- **第二阶段（报告撰写）**：3 个子智能体各负责一家企业的报告，接收全部数据后写出完整 Markdown。

**必查数据源（基础层 20 类 + 增强层 12 类 = 32 类 API）：**

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

**V3 增强：Doris DAAS 数据库深度查询**（需要投行级深度分析时）

```python
conn = pymysql.connect(host='10.9.17.20', port=9030, user='openapi',
    password='Ekaj3T4!', database='daas', charset='utf8mb4')
```

详见 `doris-daas-query` 技能。V3 报告必查的 DAAS 表（在基础 32 类 API 之外追加）：

| 表名 | 用途 | V3 报告对应章节 |
|------|------|------|
| `opt_company_intellectual_property_index` | IP 指数全景（163+指标：转让/许可/质押/被引/海外/PCT/有效比） | 知识产权深度分析 |
| `opt_government_award_subsidy` | 政府补贴明细（部门/金额/年度/类型） | 政府补贴与政策红利 |
| `tb_company_financing` | 融资事件（轮次/投资方/金额/日期） | 融资历程深度分析 |
| `tb_company_group` | 企业族群/集团归属 | 集团生态分析 |
| `opt_ent_scale_tag` | 企业规模年度标签（大/中/小/微） | 企业规模升级路径 |
| `opt_company_label_potential_01` | 潜力标签（专精特新/高企/创新等入库状态） | 企业资质标签 |
| `opt_ent_tax_status` | 税务状态（税务机关/地址） | 税务与合规 |
| `opt_company_label_base_10` | 基础标签（高新/SME等） | 企业画像 |

**注意：** label_id 字段需要解码。部分表的 label_name 列可能为空，需参考 `references/daas-deep-dive-tables.md` 中的标签字典。

## 报告最终结构（八部框架）

所有报告统一采用以下结构，确保专业性和一致性：

```
# 企业名称 投资研究报告

**报告日期：** YYYY年MM月  |  **机密等级：** 机密

## 目录

## 第一部分  投资概要
### 1.1 核心发现 · 1.2 投资亮点 · 1.3 关键风险 · 1.4 估值摘要

## 第二部分  公司概况  
### 2.1 工商登记 · 2.2 股权结构与穿透 · 2.3 实际控制人 · 2.4 管理层与治理
### 2.5 历史沿革 · 2.6 集团架构 · 2.7 政府补贴 · 2.8 企业规模演变

## 第三部分  业务与技术
### 3.1 主营业务 · 3.2 产品矩阵 · 3.3 商业模式 · 3.4 技术壁垒
### 3.5 知识产权全景 · 3.6 创新能力评估

## 第四部分  行业与市场
### 4.1 行业格局 · 4.2 市场规模 · 4.3 政策环境 · 4.4 竞争格局
### 4.5 可比公司分析 · 4.6 行业定位

## 第五部分  财务分析
### 5.1 财务数据概览（标注数据来源和可信度）
### 5.2 营收分析 · 5.3 盈利分析 · 5.4 资产负债 · 5.5 现金流与融资
### 5.6 财务预测 · 5.7 数据可信度评估

## 第六部分  风险分析
### 6.1 风险全景 · 6.2 财务风险 · 6.3 经营风险 · 6.4 行业风险 · 6.5 法律合规

## 第七部分  估值与建议
### 7.1 估值方法 · 7.2 可比公司估值 · 7.3 可比交易估值 · 7.4 DCF估值
### 7.5 三情景分析 · 7.6 投资评级 · 7.7 退出路径

## 第八部分  附录
### 附录A 核心专利清单 · 附录B 变更记录 · 附录C 财务详表 · 免责声明
```

## 报告质量铁律

### 严禁事项

1. **严禁字母编号**：不得出现 A.1、B.2、C.3 等字母前缀的章节标题
2. **严禁版本痕迹**：不得出现 "新增""补充""增强""升级""V4""v5" 等迭代标记
3. **严禁分隔装饰**：不得使用 ═══、███ 等 ASCII 装饰线分隔章节
4. **严禁日期重复**：报告只有一个报告日期
5. **严禁推测替代事实**：已有真实财务数据时，不得继续使用估算值

### 必须事项

1. **财务数据必须标注来源**：`tb_annual_report_2`（企业自行申报的税务数据）
2. **财务异常必须注明**：如 empNum=1 但社保48人的矛盾必须标注
3. **目录行间距一致**：所有目录条目之间等间距
4. **章节编号连续**：从1开始不间断递增，附录后用字母标识
5. **企业专有数据用真实值**：不得用行业均值替代已有实际数据

| 类别 | 章节 | 核心内容 |
|------|:--:|------|
| **封面与总览** | 1-2 | 封面、目录、执行摘要（投资亮点/风险/估值摘要表） |
| **公司基础** | 3-6 | 工商信息、行业分类、股权结构穿透（含国资分析）、UBO/实控人控制路径 |
| **治理与管理** | 7-8 | 管理层深度画像、历史沿革里程碑 |
| **业务与技术** | 9-11 | 商业模式、产品矩阵、知识产权全景（专利/软著/商标完整清单） |
| **STI 五维评分** | 12-16 | 投入（发明人/融资/稳定性）、产出（专利数/高价值）、质量（评分/估值/许可）、影响（被引/标准/PCT）、成长（增速/活跃度/奖项） |
| **资质与荣誉** | 17 | 资质认证体系+荣誉清单 |
| **行业分析** | 18-22 | 全球→全国→细分市场逐层分析、政策环境矩阵 |
| **竞争分析** | 23-24 | 竞争格局、可比上市公司财务对标（营收/毛利率/ROE/股价） |
| **战略分析** | 25-26 | SWOT、波特五力模型 |
| **风险分析** | 27 | 按类型/时间/金额/判决逐项展开、风险矩阵 |
| **财务与人力** | 28-29 | 社保趋势分析、招聘动态→业务方向判断 |
| **集团架构** | 30-32 | 子公司网络、供应链分析、国际化战略 |
| **ESG** | 33 | 环境/社会/治理三维评分 |
| **估值模型** | 34-36 | DCF三情景+可比法+敏感性分析 |
| **投资建议** | 37-38 | 投资评级（量化评分表）、退出路径（IPO/并购/转让×概率加权IRR） |
| **附录** | 39+ | 专利清单、变更记录汇总、社保表、股权演变图、免责声明 |

**V4 增强章节（60+ 章，全维度投行级 + 国际对标 + 可比交易）：**

在 V3 50+ 章基础上，使用 Web 搜索 + Doris DAAS 追加数据后新增以下章节：

| V4 新增章节 | 数据来源 | 核心内容 |
|------------|------|------|
| 中标金额交叉验证 | `ads_bid_win_candidate_out` (Doris) | 中标金额汇总→年化营收推演→与招聘数据交叉验证 |
| 国际竞争对手对标 | Web Search | 海外同赛道公司（营收/估值/融资/产品线）→估值锚 |
| TAM/SAM/SOM 量化建模 | Web Search + 行业报告 | 全球→中国→目标份额三层市场空间测算 |
| 可比交易法 (Precedent Transactions) | Web Search | 近2-3年同行业融资/并购案例→PS/PE/EV乘数→估值区间 |
| 专利 IPC 聚类分析 | `ip_patent` (Doris) + IPC字典 | IPC分类聚类→核心技术域识别→壁垒评估 |
| 诉讼财务影响量化 | `risk_lawsuit` + `risk_lawsuit_list` (Doris) | 逐案判赔/标的金额→原告可回收/被告曝险值→三情景 |
| 风险时间线热力图 | 同上 + 综合 | 年×类型×角色×严重度矩阵→风险演化趋势 |
| 工厂产能利用率模型 | Web Search + 行业数据 | 厂房面积→产出率→产能→利用率→营收验证 |
| 管理层能力矩阵 | Web Search + `get_company_employee` | 创始人履历→技术/商业/管理/资本/合规5维评分 |
| 客户集中度分析 | Web Search + 行业数据 | Top3/Top5客户占比推算→信用风险→单一客户依赖 |
| 产业链利润分配 | Web Search (上下游上市公司毛利率) | 上游→中游→下游利润率对比→议价能力定位 |
| IPO 路径逐条对标 | Web Search + 上市公司规则 | 科创板/北交所标准逐条check→差距分析→时间表 |
| ENF/产线政策量化 | Web Search | 新国标/政策对营收的量化影响→资本开支需求

在 V2 35+ 章基础上，使用 Doris DAAS 追加数据后新增以下章节：

| V3 新增章节 | 数据来源 | 核心内容 |
|------------|------|------|
| 政府补贴与政策红利 | `opt_government_award_subsidy` | 补贴趋势表、部门/金额/类型分布、政策红利量化 |
| 企业规模升级路径 | `opt_ent_scale_tag` | 年份标签追踪（微型→小型→中型）、升级信号分析 |
| IP 指数深度分析 | `opt_company_intellectual_property_index` | 转让/许可/质押/被引/海外/PCT/有效比趋势、专利货币化模式 |
| 融资历程深度 | `tb_company_financing` | 轮次时间线、投资方质量矩阵、估值推算 |
| 行业密度与竞争位势 | Doris JOIN `opt_company_base` + `company_industry` | 同城同行业大盘统计（总数/存续/平均资本）、公司排名定位 |
| 企业族群/集团生态 | `tb_company_group` | 集团归属、成员企业网络、生态协同 |
| 企业标签画像 | `opt_company_label_potential_01` | 潜力标签（专精特新入库/备案/高新等）→发展信号 |

**V3 报告标志：** V3 报告标题应标注「V3.0」并注明升级内容，如：
> **升级内容：Doris DAAS × 政府补贴 × IP指数分析 × 融资历程 × 行业密度对比 × 企业规模升级路径**

### 报告撰写铁律（用户偏好）

**绝对禁止（违反将导致报告被拒）：**

| 禁止项 | 示例 | 原因 |
|--------|------|------|
| 版本号 | V1/V2/V4/V5 | 报告应是独立完整体 |
| "新增/补充/增强/升级" | "新增章节A"、"增强模块" | 暴露迭代痕迹 |
| 字母编号章节 | A.1/B.2/C.3/D.1 | 破坏统一结构 |
| 日期重复 | 两处"报告日期" | 残留痕迹 |
| 装饰性分隔符 | "═══"、"模块（更新）" | 非专业格式 |
| TOC含版本标记 | "-v4新增"、"★新增§34" | 目录也需清洁 |
| 更新说明/元注释 | "本节为V3新增" | 读者不需要知道版本史 |
| 子智能体轻量报告 | <1000行的"八部结构"版 | 深度不足，用户会要求恢复旧版 |

**必须做到：**

| 要求 | 说明 |
|------|------|
| 报告读起来像一次性写成的完整作品 | 无任何迭代痕迹 |
| 目录、标题、正文三者一致 | 统一使用数字编号（## 1. / ## 2. ...） |
| 所有内容深度均匀 | 没有"有些章节5页、有些章节2行"的断层 |
| 使用用户V4基底而非子智能体重写 | V4是深度最丰富的版本（2000+行） |

**报告最终呈现标准：**
- 章节连续编号（1→51），中间无跳跃
- 无"第一部分/第二部分"中文篇章（子智能体版过于简略）
- 深度优先于结构整洁（用户明确表示"内容不如V4"）
- 用户指出"新增章节A"等问题后，应直接用脚本批量替换清理，而非用子智能体重写（重写会丢失深度）
- 中文，专业严谨，投行风格
- 大量使用表格展示数据（每章至少 2-3 个表格）
- 每个表格下必须有「分析解读」段落
- 估值部分必须有量化模型（非仅定性判断）
- 附录放置原始数据
- **禁止使用版本号**：最终版报告不得出现"V1发现"/"V3修正为"等版本对比语言。只呈现最终结论

**最终版报告结构（7篇37章，无版本痕迹）：**

这是所有报告升级的**终极目标结构**。无论从哪个版本起步，迭代终点都应收敛到此结构：

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

**报告撰写方式：** 使用 `delegate_task` 将每家企业分配给独立子智能体撰写。子智能体 context 中必须包含：
1. 所有第一阶段采集的结构化数据
2. 行业对标数据
3. 完整的章节结构要求（35+ 章）
4. 写作风格指南（投行中文、表格密集、每表必解读）

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

for name in ['企业A_v2', '企业B_v2', '企业C_v2']:
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

## 报告定稿：禁止版本痕迹（🔴 强制）

最终版报告必须是**干净的一次性成品**，读者不应感知到任何迭代过程。

### 🔴 报告交付前自检清单

生成 PDF 前，**必须**对 MD 文件执行以下检查（用 `grep` 或 Python）：

1. **重复日期**：`grep -c '报告日期' report.md` → 必须 = 1
2. **字母编号残留**：`grep -E '^## [A-Z]\.' report.md` → 必须为空
3. **"新增"在标题**：`grep -E '^#.*新增' report.md` → 必须为空（业务含义的"新增"如"新增装机"除外）
4. **"补充"/"增强"/"升级"**：`grep -E '补充章节|新增模块|【新增】|【增强】|升级内容|★新增' report.md` → 必须为空
5. **版本号残留**：`grep -E 'V[0-9]' report.md` → 必须为空
6. **空标题**：`grep -n '^#\s*$' report.md` → 必须为空
7. **章节跳跃**：主章节从第一、二、三...连续排到第八部分（或1-37连续），无跳跃
8. **小节编号一致**：同一父章节下的小节使用统一的 `### X.Y` 格式

**清理脚本模板：**
```python
import re
content = Path('report.md').read_text()
content = re.sub(r'新增章节\w[：:]?\s*', '', content)
content = re.sub(r'【新增】|【增强】|★新增|（新增）', '', content)
content = re.sub(r'V\d[\.\d]*', '', content)
content = re.sub(r'\*\*升级内容[：:].*?\*\*\n', '', content)
content = re.sub(r'\n{4,}', '\n\n\n', content)
```

### 禁止的表述清单

| 禁止的表述 | 示例 | 为什么不行 |
|-----------|------|------|
| "新增章节X" | `# 新增章节A：政府补贴分析` | 暴露了该章节是后加的 |
| "补充模块" | `## 新增模块：可比交易法` | 同上 |
| "【新增】"标记 | `## 第10章 【新增】三家工厂产能模型` | 同上 |
| 版本号 | `此次V4升级重点为...` | 报告是独立文档，不是changelog |
| 版本对比 | `V1-V4估营收2000万，V5实为1005万` | 直接说"营收1005万"即可 |
| "升级内容" | `**升级内容：Doris DAAS × 政府补贴**` | 同上 |
| 任何带"原"/"旧"/"新"的对比 | `原来的估值是X，现在修正为Y` | 只呈现最终结论 |

**正确的做法：** 章节标题直接用业务名称，不加任何"新增/补充/升级"前缀。如 `## 政府补贴与政策红利分析`。

**清理方法：** 定稿时用 Python 正则批量清除：`re.sub(r'新增章节|补充模块|【新增】|V\d\.\d|\*\*升级.*?\*\*\n', '', content)`

## 报告升级：Patch 优于 Rewrite（🔴 强制）

**教训：** 子智能体重写报告会丢失已完成版本的深度和细节。用户实测反馈子智能体的"终极版"只有 V4 一半的深度。

| 做法 | 结果 | 评价 |
|------|------|:--:|
| 用 `delegate_task` 让子智能体从零写报告 | 958行 vs 原版2053行 | ❌ 丢失深度 |
| 用 Python `str.replace` 向已有报告插入新章节 | 保留全部深度+追加新数据 | ✅ 推荐 |

**正确的升级模式：**
1. `read_file` 读入当前最佳版本的 MD（已经是 V4/V5 深度级别）
2. 用 Python `re.sub` 清理版本标记
3. 用 `str.replace` 在合适位置插入新章节内容
4. 所有操作在 `execute_code` 中一次完成
5. 子智能体只用于**数据采集**和**研究搜索**，不用于报告撰写

**⚠️ 为什么不能用 delegate_task 写最终版报告**

本会话实测教训：让子智能体按"全新结构"重写已有报告，输出行数从 2000+ 腰斩到 900-1200 行。原因：
- 子智能体有 token 和 context 限制，无法持有一份 2000 行报告的完整上下文
- 子智能体倾向于"总结"而非"展开"，丢失深度分析
- 子智能体写作风格不稳定，可能偏离投行风格

**结论**：`delegate_task` 仅用于 Phase 1 数据采集和 Phase 2 Web 研究搜索。Phase 3 报告定稿始终由主智能体通过 `execute_code` + `patch` 完成。

## 注意事项

### 两阶段 delegate 模式（防超时）

**关键洞察：** 子智能体 600s 超时常见于同时做数据采集+报告撰写。解决方案：

**标准流程（>1家企业）：**
1. **第一阶段（并行数据采集）**：3 个子智能体仅做 API 调用，返回结构化 JSON。context 中给明确 API 调用清单（含参数）。每个约 2-3 分钟。
2. **第二阶段（并行报告撰写）**：3 个子智能体使用采集数据撰写完整报告。context 中包含全部数据 + 行业对标数据 + 章节结构要求。每个约 5-7 分钟。
3. **主智能体做 PDF 生成**：接收报告后统一转换。

**单家企业模式：** 跳过 delegate，主智能体直接串行调用所有 API 后写报告。

### 超时处理

如果子智能体仍然超时：
- 将数据采集拆分为两个子智能体（如：基础20API + 增强12API）
- 报告撰写阶段提示子智能体优先写核心章节（1-28），附录可后续补充
- 主智能体在接收不完整报告后补齐缺失章节

### 数据限制

**🚨 关键发现（V5）：不要相信"企业选择不公示"**

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

**V5 财务分析核心指标：**
- 营收 CAGR / 净利率趋势 / ROE 杜邦分解
- 负债率变化 + 经营杠杆系数
- 盈亏平衡点 = 固定成本 / (1 - 变动成本率)
- 现金跑道(月) = 净资产 / (|年均烧钱率| / 12)
- 人均产值 = 营收 / 员工数

详见 `references/tb-annual-report-2-schema.md`。

**其他限制：**
- 供应商/购地/发票等辅助数据对非上市中小企业通常为空，不影响报告质量
- 零司法风险本身是重要积极信号
- STI 五维评分 + 专利数 + 标签（专精特新/高新） + **真实财务数据** = V5 核心评估维度

### 用户偏好

用户徐生偏好直接、精简的交付方式。报告完成后：
- 简短汇总核心发现（一句话+一个核心指标表）
- 直接发送 MEDIA 文件
- 不主动推销，等用户追问再展开

**⚡ 批量执行模式（关键）：** 当用户问"还可以做什么优化"时，列出优化项后**不要逐一询问是否执行**——直接全部做完。用户会回复"都做"/"全部一起"/"做"。这是标准模式：列清单→不等确认→do everything at once。

此偏好同样适用于：
- 数据补全：一次列出所有缺失维度→不等确认→全部执行
- 报告升级：列出版本升级项→不等确认→全部升级
- 多企业并行：3家企业同时处理，不串行

### 渐进升级模式

本技能支持同一批企业的多轮迭代升级：
- **V1 → V2**：补充 STI 五维、UBO、股权穿透、可比上市公司财务对标（+15章）
- **V2 → V3**：补充 Doris DAAS（IP指数/政府补贴/融资历程/行业密度/标签/规模升级）（+12章）
- **V3 → V4**：补充国际对标、可比交易法、TAM/SAM/SOM、IPC聚类、诉讼量化、产能模型、管理层矩阵、产业链利润、IPO对标（+13章）
- **V4 → V5**：`tb_annual_report_2` 真实财务数据→完整 P&L/BS/ROE杜邦/经营杠杆/盈亏平衡/烧钱率/现金跑道/真实数据估值（财务章节从估算全部重写为实际）(+8章)

⛔ **V4→V5 警告：** 真实财务数据可能彻底翻转投资叙事。凌度案例：V1-V4 估营收 2000-6000万/零风险 → V5 实为 1005万/资不抵债-480万/净亏707万。必须准备接受**任何方向**的叙事翻转。

每轮升级的策略是**在上一版基础上追加新章节**，而非从零重写。使用 `read_file` 读入已有报告→`str.replace` 或 `patch` 在关键位置插入新章节→打新版标记。

详见 `references/tb-annual-report-2-schema.md`。

### PDF 生成陷阱

- `generate_pdf` 工具参数的 content 字段有大小限制（~30KB），大报告（>50KB MD）需通过 `execute_code` + subprocess 方式渲染
- `execute_code` 中的 `read_file` 返回 dict（不是直接字符串），用 `Path.read_text()` 代替
- Python `markdown` 库的 `content` key 问题：`read_file(path)['content']` 在某些版本不可靠，直接用 `pathlib` 更稳定
- `markdown.markdown()` 必须显式传 `extensions=['tables', 'fenced_code']`，否则表格和代码块渲染异常
- `font-family` 必须包含中文字体 fallback：`'AlibabaPuHuiTi-3-55-Regular', 'SimSun', serif`，否则 PDF 中文显示为方块
- ```` @page { size: A4; margin: 16mm; } ```` 中的双花括号是 CSS 语法，写入 Python f-string 时不需要转义
- 渲染前确认 `pip install markdown` 已完成（通常已安装），无 matplotlib 不影响 PDF 渲染

### V3 报告迭代模式（复用已有报告）

当用户要求对已有报告进行全维度升级时，不要从零开始。策略：

1. **保留 V2 报告为基底**：读取已有 MD 文件
2. **追加新章节**：在 V2 报告结构的关键位置（执行摘要后、附录前）插入 V3 新增章节
3. **打 V3 标记**：在报告标题中标注「V3.0」和升级内容
4. **使用 patch 而非 rewrite**：用 `patch` 工具或 Python `str.replace` 插章节，而非让子智能体从头写

这样可以避免子智能体 600s 超时（常见于凌度这种数据密集型企业），同时保证报告连续性。
