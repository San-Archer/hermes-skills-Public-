# 交付前自检清单

生成 PDF 前对 MD 文件执行以下检查。任一未通过 → 拒绝交付。

## 自动化检查 (Python)

```python
import re
from pathlib import Path

def validate_report(path: str) -> list[str]:
    c = Path(path).read_text(encoding='utf-8')
    lines = len(c.split('\n'))
    issues = []
    
    # === 格式检查 ===
    if c.count('**报告日期') > 1:
        issues.append('报告日期重复')
    if re.search(r'^## [A-Z]\.', c, re.MULTILINE):
        issues.append('字母编号残留 (A.1/B.2等)')
    bad = ['新增章节','新增模块','补充章节','升级内容','版本新增','【新增】','【增强】','★新增','v4新增']
    for t in bad:
        if t in c:
            issues.append(f'版本痕迹: {t}')
    if re.search(r'V\d\.\d', c):
        issues.append('版本号残留')
    if re.search(r'^#\s*$', c, re.MULTILINE):
        issues.append('空标题 (孤立的#)')
    if re.search(r'═|█', c):
        issues.append('ASCII装饰符')
    
    # === 🔴 深度门禁 (v5.1.0) ===
    if lines < 1800:
        issues.append(f'行数不足: {lines} < 1800')
    
    # 表格计数
    table_sep = len(re.findall(r'^\\|[-|]+\\|$', c, re.MULTILINE))
    table_count = table_sep // 2
    if table_count < 50:
        issues.append(f'表格不足: {table_count} < 50')
    
    # 🔴 v5.1.0 写作风格门禁
    analysis_count = len(re.findall(r'分析[：:]', c))
    if analysis_count < 30:
        issues.append(f'"分析:"段落不足: {analysis_count} < 30（每表必配分析段落）')
    
    keyfinding_count = len(re.findall(r'关键发现', c))
    if keyfinding_count < 15:
        issues.append(f'"关键发现:"不足: {keyfinding_count} < 15（每5-8表一处）')
    
    # 必备章节
    required = {
        '可比交易': '缺失可比交易法',
        '产业链': '缺失产业链分析',
        'TAM': '缺失TAM市场规模',
        '管理层.*矩阵': '缺失管理层能力矩阵',
        'IPO.*对标|退出路径': '缺失IPO/退出路径',
    }
    for pattern, msg in required.items():
        if not re.search(pattern, c):
            issues.append(msg)
    
    # TOC间距一致
    toc = re.search(r'## 目录\n(.*?)\n## \d', c, re.DOTALL)
    if toc and '\n\n\n' in toc.group(1):
        issues.append('TOC有双空行')
    
    return issues

# 使用
errors = validate_report('report.md')
assert not errors, f'质检未通过: {errors}'
print('✅ 全部通过')
```

## 人工检查

- [ ] 行数 ≥ 1,800（上市公司）/ 1,500（非上市公司）
- [ ] 数据表格 ≥ 50 个
- [ ] 🔴 "分析："段落 ≥ 30 个（每表必配100-300字分析）
- [ ] 🔴 "关键发现："callout ≥ 15 处
- [ ] 可比交易法章节存在且包含 ≥2 个案例
- [ ] TAM/SAM/SOM 市场规模三层测算存在
- [ ] 产业链利润分配分析存在
- [ ] 管理层能力矩阵（5维评分）存在
- [ ] 真实财务数据已标注来源（上市公司→审计年报，非上市→tb_annual_report_2）
- [ ] 财务异常已标注（empNum≠社保 / 年度波动>3x）
- [ ] 多企业报告间行数差 < 25%
- [ ] 报告标题不含版本号
- [ ] 🔴 无一句话点评——每个表格的分析必须展开100-300字推理链

## 修复脚本

```python
# 清理版本痕迹
content = re.sub(r'V\d[\.\d]*', '', content)
content = re.sub(r'【新增】|【增强】|★新增|（★新增）', '', content)
content = re.sub(r'新增章节|新增模块|补充章节|升级内容|版本新增', '', content)
content = re.sub(r'\n{4,}', '\n\n\n', content)
```

## 关联文档

- 首发深度强制令: `references/deep-first-pass-mandate.md`
- 反模式-子智能体写最终版: `references/anti-pattern-delegate-for-finals.md`
