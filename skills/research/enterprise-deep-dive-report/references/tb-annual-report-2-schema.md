# tb_annual_report_2 完整 Schema

企业年度税务申报财务数据。即使企业公示系统显示"不公示"，此表仍可能包含完整数据。

## 字段清单

| 字段 | 类型 | 含义 | 用途 |
|------|------|------|------|
| `id` | bigint | 主键 | |
| `company_id` | varchar(32) | 企业ID | JOIN key |
| `anCheYear` | varchar | 年报年度 | 时间序列 |
| `anCheDate` | date | 年报提交日期 | |
| `entType` | varchar | 企业类型编码 | |
| `entName` | varchar | 企业名称 | 可能含曾用名 |
| `tel` | varchar | 联系电话 | |
| `addr` | varchar | 地址 | |
| `empNum` | int | 从业人数 | **⚠️ 可能与年报社保人数不一致** |
| `empNumDis` | varchar | 人数披露状态 | 0=不公示, 2=公示 |
| `vendInc` | decimal(38,6) | 营业总收入 | **P&L核心** |
| `vendIncEtl` | decimal(38,6) | 营业总收入(ETL) | 备用取值 |
| `vendIncDis` | varchar | 营收披露状态 | 0=不公示 |
| `maiBusInc` | decimal(38,6) | 主营业务收入 | 业务集中度 |
| `maiBusIncEtl` | decimal(38,6) | 主营业务收入(ETL) | |
| `netInc` | decimal(38,6) | 净利润 | **盈利核心** |
| `netIncEtl` | decimal(38,6) | 净利润(ETL) | |
| `proGro` | decimal(38,6) | 营业利润 | 经营效率 |
| `proGroEtl` | decimal(38,6) | 营业利润(ETL) | |
| `assGro` | decimal(38,6) | 资产总额 | **规模** |
| `assGroEtl` | decimal(38,6) | 资产总额(ETL) | |
| `totEqu` | decimal(38,6) | 所有者权益(净资产) | **偿付能力** |
| `totEquEtl` | decimal(38,6) | 所有者权益(ETL) | |
| `liaGro` | decimal(38,6) | 负债总额 | **杠杆率** |
| `liaGroEtl` | decimal(38,6) | 负债总额(ETL) | |
| `ratGro` | decimal(38,6) | 纳税总额 | 税务合规 |
| `ratGroEtl` | decimal(38,6) | 纳税总额(ETL) | |

## 查询模板

```sql
SELECT anCheYear, empNum,
       COALESCE(vendInc, vendIncEtl) AS revenue,
       COALESCE(netInc, netIncEtl) AS net_profit,
       COALESCE(assGro, assGroEtl) AS total_assets,
       COALESCE(totEqu, totEquEtl) AS equity,
       COALESCE(liaGro, liaGroEtl) AS liabilities,
       COALESCE(proGro, proGroEtl) AS operating_profit,
       COALESCE(ratGro, ratGroEtl) AS tax
FROM tb_annual_report_2
WHERE company_id = 'xxx'
ORDER BY anCheYear;
```

## 派生指标

```python
rev = COALESCE(vendInc, vendIncEtl)
net = COALESCE(netInc, netIncEtl)
assets = COALESCE(assGro, assGroEtl)
equity = COALESCE(totEqu, totEquEtl)
liab = COALESCE(liaGro, liaGroEtl)

margin = net / rev * 100                    # 净利率
roe = net / equity * 100                    # ROE
de_ratio = liab / assets * 100              # 资产负债率
burn_rate = abs(net) if net < 0 else 0      # 烧钱率(年)
runway_months = equity / (burn_rate / 12)   # 现金跑道(月)
per_capita = rev / empNum                   # 人均营收
breakeven = fixed_cost / (1 - var_cost_pct) # 盈亏平衡营收
operating_leverage = (rev_new - rev_old) / rev_old / ((net_new - net_old) / net_old)
```

## 已验证的数据覆盖

| 企业 | 可用年份 | 备注 |
|------|:--:|------|
| 凌度智能 | 2023 only | 2021-2022 empNum=1(空壳) |
| 联信高新 | 2013-2023 (11年) | 营收仅2020起披露 |
| 莱迪生物 | 2021-2023 | 2022 empNum缺失 |

## ⚠️ 数据质量警示

1. **empNum 可能与社保人数矛盾**：凌度2022 empNum=1 但社保48人
2. **需使用 COALESCE**：vendInc 和 vendIncEtl 可能一个为NULL
3. **dis=0 不代表无数据**：assGroDis=0 但 assGro 和 assGroEtl 可能仍有值
4. **未经审计**：数据为企业自行申报
