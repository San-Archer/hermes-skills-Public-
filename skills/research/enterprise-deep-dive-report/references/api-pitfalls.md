# MCP API 数据陷阱实录

> 2026-06-09 会话实测，中科江南(301153.SZ)案例。

## 陷阱1：`research_industry` 返回不相关同业

**现象：** `mcp_query_onmarket_research_industry` 对中科江南(301153.SZ)自动选取的可比公司包含安徽凤凰(920000.BJ)，实际是汽车零部件企业，与财政IT完全不相关。

**根因：** 该 API 基于申万"软件和信息技术服务业"一级行业分类，该行业下有 5,525 家上市公司。自动 peers 选取未做子赛道过滤。

**正确做法：**
1. 不依赖该 API 的 `peers` 字段
2. 手动选择真正同赛道的可比公司（如财政IT：博思软件 300525、远光软件 002063）
3. 用 `get_quote_snapshot` + `research_fundamentals` 逐家查询
4. 可比公司选取优先级：同赛道已上市 > 同赛道新三板 > 同客户群

## 陷阱2：`research_fundamentals` BS/CF 数据在 compact 模式是同比变化率

**现象：** `mcp_query_onmarket_research_fundamentals` 在 `response_profile=compact` 下，资产负债表(BS)的 `total_assets: -1.095205` 被误读为"资产为-1.1亿"。

**实际含义：** compact 模式下 BS/CF 数值是**同比百分比变化率**。-1.095205 表示资产总额同比下降 1.1%，不是绝对金额。

**正确做法：**
| 数据类型 | compact 模式 | 可靠数据源 |
|----------|:--:|------|
| 利润表(IS) | ✅ 绝对值可用 | — |
| 比率(ratios) | ✅ 绝对值可用 | — |
| 估值(valuation) | ✅ 可用 | — |
| 资产负债表(BS) | ❌ 同比变化率 | 切换到 `standard`/`detail` 模式 |
| 现金流量表(CF) | ❌ 同比变化率 | 切换到 `standard`/`detail` 模式 |

**替代方案：** 使用 `mcp_data_listed_search_annual_stock_indicator` 获取历年财务指标——该接口始终返回绝对值。

## 陷阱3：中标数据返回量极大导致截断

**现象：** `mcp_bid_search_company_winning_bid` 对中科江南返回 3,667 条记录，响应体被截断为 3,460,248 字符。

**正确做法：**
- 仅取 `page_index=1` 的前几条确认活跃度
- 如需总量统计，用 `execute_code` 解析截断响应中的 `total` 字段
- 如需省份分布，同样从截断数据中提取（结果按省份排列）
- 不要尝试 `page_index=0`（返回全部）——会超时

## 陷阱4：`annual_report` 显示"企业选择不公示"但真实数据存在于 Doris

**现象：** `mcp_data_query_search_annual_report` 对非上市公司显示"企业选择不公示"。

**实际：** Doris DAAS 的 `tb_annual_report_2` 表包含所有企业完整年报数据，从税务申报端获取。

**做法：** 不依赖 MCP 年报接口获取财务数据。直接查 Doris `tb_annual_report_2`。

## 陷阱5：Doris `label_id` 字段需解码

**现象：** `opt_company_label_potential_01` 和 `opt_company_label_base_10` 表的 `label_name` 列可能为空。

**做法：** 需要 `label_id` → 标签名映射字典。详见 `references/daas-deep-dive-tables.md`。
