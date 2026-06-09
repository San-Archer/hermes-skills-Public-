# Doris DAAS 实际列名映射（2026-06 实测）

技能文件中使用的列名与实际表结构存在差异。以下为已验证的正确列名：

## opt_government_award_subsidy

| 技能文档列名 | 实际列名 | 说明 |
|------|------|------|
| `year` | `publish_year` | 发布日期 |
| — | `department` | 补贴部门 ✅ |
| — | `amount` | 金额 ✅ |
| — | `company_name` | 公司名 ✅ |

正确查询：
```sql
SELECT publish_year, department, SUM(amount) as total_amt
FROM opt_government_award_subsidy
WHERE company_name LIKE '%公司名%'
GROUP BY publish_year, department
ORDER BY publish_year DESC
```

## opt_company_label_potential_01

此表不包含 `company_name` 列。通过 `company_id` 关联。主要字段：`label_id`, `label_value`, `attributes`。

正确用法：不做直接查询，通过 JOIN `company_id` 获取。

## ads_bid_win_candidate_out

| 技能文档列名 | 实际列名 | 说明 |
|------|------|------|
| `total_amount` | `amount` | 中标金额 |
| — | `company_name` | 公司名 ✅ |
| — | `project_name` | 项目名 |
| — | `ranking` | 排名 |

正确查询：
```sql
SELECT SUM(amount) as total_bid, COUNT(*) as cnt
FROM ads_bid_win_candidate_out
WHERE company_name LIKE '%公司名%'
```

## ip_patent

| 技能文档列名 | 实际列名 | 说明 |
|------|------|------|
| `applicant` | `applicant_name` | 申请人 |
| — | `main_ipc` | 主分类号 ✅ |
| — | `title` | 专利名称 |

正确查询：
```sql
SELECT main_ipc, COUNT(*) as cnt
FROM ip_patent
WHERE applicant_name LIKE '%公司名%'
GROUP BY main_ipc ORDER BY cnt DESC
```

## tb_annual_report_2

| 技能文档列名 | 实际列名 | 说明 |
|------|------|------|
| `company_name` | `entName` | 企业名称 |
| — | `anCheYear` | 年报年度 ✅ |
| — | `empNum` | 从业人数 ✅ |
| — | `vendInc` / `vendIncEtl` | 营收 ✅ |
| — | `netInc` / `netIncEtl` | 净利润 ✅ |
| — | `assGro` / `assGroEtl` | 资产总额 ✅ |
| — | `totEqu` / `totEquEtl` | 净资产 ✅ |
| — | `liaGro` / `liaGroEtl` | 负债总额 ✅ |

正确查询：
```sql
SELECT anCheYear,
  COALESCE(vendInc, vendIncEtl) as revenue,
  COALESCE(netInc, netIncEtl) as net_income,
  empNum,
  COALESCE(assGro, assGroEtl) as total_assets,
  COALESCE(totEqu, totEquEtl) as equity,
  COALESCE(liaGro, liaGroEtl) as liabilities
FROM tb_annual_report_2
WHERE entName LIKE '%公司名%'
ORDER BY anCheYear DESC
```

## opt_company_intellectual_property_index

此表通过 `credit_no`（统一信用码）关联，不使用 `company_name`。

## tb_company_financing / tb_company_group / opt_ent_scale_tag

这三个表使用 `company_name` ✅，列名正确。
