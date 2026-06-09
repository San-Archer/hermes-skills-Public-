# 技能审查方法论

> 2026-06-09 `enterprise-deep-dive-report` v4.0.0→v5.0.0 升级实录

## 三轮审查法

### 第一轮：执行对照（"跑一遍试试"）
- 用技能生成一份实际报告
- 对比标杆（凌度智能 2,053行）
- 标记缺失维度：Web搜索/Doris DAAS/可比交易/产业链/管理层矩阵

### 第二轮：结构审查（"找矛盾"）
检查项：
- [ ] 是否存在两套互斥的结构定义？
- [ ] Web搜索和Doris是否标记为"可选"而非"强制"？
- [ ] delegate_task 用于报告撰写 vs 禁止用delegate写报告是否矛盾？
- [ ] Phase编号是否连贯（0→1→2→3→4）？
- [ ] "渐进升级"模式是否与"首发即深度"矛盾？

### 第三轮：细节扫描（"逐行过"）
检查项：
- [ ] YAML description 是否与正文一致？
- [ ] 版本标记（V4/V5/V3.0）是否残留在非历史案例区域？
- [ ] 章节编号是否有两套并存？
- [ ] 是否存在空段落/空标题？
- [ ] 是否存在重复章节（同一H3出现两次）？
- [ ] 代码示例中的命名是否包含版本痕迹（如"企业A_v2"）？
- [ ] 表格列名是否包含过时标记（如"V4底版"）？
- [ ] 密码/Token是否暴露在公共文件中？

### Python 辅助检查脚本

```python
from pathlib import Path
import re

content = Path('SKILL.md').read_text()

# 结构冲突检测
conflicts = []
if content.count('篇') >= 2 and ('八部' in content or '8篇' in content) and '7篇' in content:
    conflicts.append('两套结构并存')
if '可选' in content and '强制' in content and 'Phase 1' in content:
    conflicts.append('可选/强制语气矛盾')
if 'delegate_task' in content and '撰写' in content and '禁止' in content:
    idx_w = content.find('delegate_task')
    idx_b = content.find('禁止')
    context = content[min(idx_w,idx_b)-200:max(idx_w,idx_b)+200]
    if '撰写报告' in context or '写报告' in context:
        conflicts.append('delegate写报告 vs 禁止delegate写报告')

# 重复章节
h3s = re.findall(r'^### (.+)$', content, re.MULTILINE)
from collections import Counter
dupes = [h for h, c in Counter(h3s).items() if c > 1]

# 版本标记残留（排除历史案例和质量规则）
v_markers = re.findall(r'\bV\d[\.\s]', content)
legit = sum(1 for m in v_markers if '版本标记' in content[max(0,content.find(m)-100):content.find(m)])
v_residual = len(v_markers) - legit

print(f"冲突: {conflicts}")
print(f"重复H3: {dupes}")
print(f"V标记残留: {v_residual}")
```

## 本次升级修复清单（18项）

| 轮次 | 修复项 | 类型 |
|:--:|------|------|
| 1 | 统一为7篇37章结构（删除八部框架） | 🔴 结构冲突 |
| 1 | Web搜索从可选→强制Stage 1B | 🔴 深度不足 |
| 1 | Doris DAAS从可选→强制Stage 1C | 🔴 深度不足 |
| 1 | 新增Phase 0深度门禁 | 🟡 缺失 |
| 1 | 新增Phase 2报告撰写 | 🟡 缺失 |
| 2 | 删除"报告撰写方式"delegate矛盾 | 🔴 内部矛盾 |
| 2 | 删除"渐进升级模式"（与首发深度矛盾） | 🔴 哲学矛盾 |
| 2 | 删除"V3报告迭代模式" | 🔴 过时 |
| 2 | 删除"两阶段delegate模式" | 🔴 过时 |
| 2 | V4增强→全维度必备章节(15类) | 🟡 语气修正 |
| 3 | YAML description八部结构→7篇37章 | 🟡 残留 |
| 3 | 删除空"报告最终结构"占位 | 🟡 空内容 |
| 3 | 删除冲突的扁平章节编号表 | 🔴 双结构 |
| 3 | 去除"升级/迭代终点"语言 | 🟡 残留 |
| 3 | Phase引用全部对齐(3→2) | 🟡 错位 |
| 3 | 去除V5版本标记3处 | 🟡 残留 |
| 3 | 删除过时"正确升级模式"操作步骤 | 🟡 残留 |
| 3 | 去除多企业"V4底版"标记 | 🟡 残留 |
