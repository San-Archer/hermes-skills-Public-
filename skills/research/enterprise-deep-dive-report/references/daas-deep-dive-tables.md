# Doris DAAS 深度查询参考

## tb_annual_report_2 — 真实财务数据 ⭐⭐⭐⭐⭐

**这是本技能最重要的数据发现。** 该表包含企业自行向税务机关申报的年度财务数据，即使企业在工商年报中选择"不公示"，数据仍可能出现在此表中。

### 表结构关键字段

| 字段 | 类型 | 说明 |
|------|------|------|
| `anCheYear` | varchar | 申报年度 |
| `empNum` | int | 员工人数 |
| `assGro` / `assGroEtl` | decimal | 总资产 / 总资产(折算) |
| `totEqu` / `totEquEtl` | decimal | 净资产 / 净资产(折算) |
| `liaGro` / `liaGroEtl` | decimal | 总负债 / 总负债(折算) |
| `vendInc` / `vendIncEtl` | decimal | 营业收入 / 营业收入(折算) |
| `proGro` / `proGroEtl` | decimal | 营业利润 / 营业利润(折算) |
| `netInc` / `netIncEtl` | decimal | 净利润 / 净利润(折算) |
| `ratGro` / `ratGroEtl` | decimal | 所得税 / 所得税(折算) |
| `maiBusInc` / `maiBusIncEtl` | decimal | 主营业务收入 |

**注意**：`assGro` 和 `assGroEtl` 通常至少有一个有值。建议 COALESCE 取非空值。字段名含 `Dis` 后缀（如 `assGroDis`）表示是否公示，0=不公示，2=公示。

### 数据可信度

- 数据为**企业自行申报**，未经第三方审计
- 部分企业早期年份存在 empNum=1 等异常（可能是空壳申报）
- 数据完整度因企业而异：联信有11年完整数据(2013-2023)，凌度仅有2023年
- **必须与年报社保人数交叉验证**：如果 empNum 与 employee_no 差异悬殊，标记为可信度警告

### 查询示例

```sql
SELECT anCheYear, empNum, 
       COALESCE(assGro, assGroEtl) assets,
       COALESCE(totEqu, totEquEtl) equity,
       COALESCE(vendInc, vendIncEtl) revenue,
       COALESCE(netInc, netIncEtl) net_profit
FROM tb_annual_report_2 
WHERE company_id = 'xxx' 
ORDER BY anCheYear;
```

## 其他关键表速查

| 表名 | 用途 |
|------|------|
| `opt_company_intellectual_property_index` | IP指数(163+指标) |
| `opt_government_award_subsidy` | 政府补贴明细 |
| `tb_company_financing` | 融资事件 |
| `tb_company_group` | 企业族群 |
| `opt_ent_scale_tag` | 企业规模年度标签 |
| `company_chattel` | 动产抵押 |
| `risk_zhixing` | 被执行人(含exec_money金额) |

本文档记录在企业深度报告 V3 实践中验证的高价值表，是对 `doris-daas-query` 技能核心表速查的补充。

## 企业评估与标签

### opt_company_label_base_10 — 基础标签
```sql
SELECT * FROM opt_company_label_base_10 WHERE company_id = 'xxx';
```
- `label_id`: 标签编码（如 `BASE_10_002`），解码需查字典
- 常见标签：`BASE_10_002` = 高新/SME

### opt_company_label_potential_01 — 潜力标签（V3 高价值）
```sql
SELECT * FROM opt_company_label_potential_01 WHERE company_id = 'xxx';
```
- `label_id` 解码：
  - `POTENTIAL_01_001` = 专精特新
  - `POTENTIAL_01_001_001` = 专精特新入库（`attributes` 含 `in_storage_status: 入库`）
  - `POTENTIAL_01_002` = 备案
  - `POTENTIAL_01_002_001` = 备案（`attributes` 含 `filing_status: 备案`）
  - `POTENTIAL_01_003` = 高新技术企业
  - `POTENTIAL_01_016` = 创新型企业
  - `POTENTIAL_01_017` = 其他潜力

### opt_ent_scale_tag — 企业规模标签
```sql
SELECT * FROM opt_ent_scale_tag WHERE company_id = 'xxx' ORDER BY year;
```
- `year`: 年份, `scale`: 大/中/小/微
- 用途：追踪企业规模升级路径

### opt_company_intellectual_property_index — IP 指数全景
```sql
SELECT * FROM opt_company_intellectual_property_index WHERE company_id = 'xxx' ORDER BY summary_month DESC;
```
- 核心指标：专利总数/发明/实用/外观、授权/有效/有效比、转让进出、许可率、质押次数、被引用、海外/PCT、平均评分/剩余寿命、商标/软著/标准数
- 注意：月度快照，取最新 `summary_month`

### tb_company_financing — 融资事件
```sql
SELECT * FROM tb_company_financing WHERE company_id = 'xxx' ORDER BY financing_date;
```
- `financing_date`, `round`, `std_round`, `amount`, `investor_names`

### opt_government_award_subsidy — 政府补贴
```sql
SELECT * FROM opt_government_award_subsidy WHERE company_name LIKE '%企业名%' ORDER BY publish_year DESC;
```
- `amount`(万元, 0=荣誉性), `department`, `title`, `partition_name`

### tb_company_group — 企业族群
```sql
SELECT * FROM tb_company_group WHERE company_id = 'xxx';
```
- `group_name`, `member_type`(0=核心/2=成员)

### opt_ent_tax_status — 税务登记
```sql
SELECT * FROM opt_ent_tax_status WHERE company_id = 'xxx';
```
- `tax_status`, `tax_authority`, `operate_address`

### 行业密度统计
```sql
SELECT COUNT(*) total,
  SUM(CASE WHEN b.company_status LIKE '%存续%' THEN 1 ELSE 0 END) active,
  AVG(CAST(b.capital_num AS DECIMAL(20,2))) avg_capital
FROM opt_company_base b
JOIN company_industry i ON b.company_id = i.company_id
WHERE i.industry_l3_name LIKE '%行业%' AND b.city = '城市';
```

## 已验证的坑

| 问题 | 详情 |
|------|------|
| label_name 可能为空 | label_id 需从已知样本推断 |
| IP Index 为月度快照 | 取最新 summary_month |
| capital_num 可能 NULL | AVG/MAX 需 CAST 并处理 NULL |
| tb_investment_event 列名不确定 | 先 DESCRIBE 确认 |
