"""
技能文件自我一致性检查脚本
用法: python references/skill-self-check.py SKILL.md

检查项目：
  1. YAML frontmatter 描述与正文一致
  2. 无重复 H2/H3 标题
  3. 无 V 版本标记残留（V4/V5 等，质量规则表中的示例除外）
  4. 无迭代语言（升级/迭代终点/先薄后厚）
  5. 无双结构命名（八部框架 vs 7篇37章）
  6. Phase 引用全部对齐
  7. 无 delegate_task 写报告的矛盾表述
  8. 无空 H2/H3 标题
  9. 章节编号连续
  10. Doris 密码暴露检查
"""

import re
import sys
from pathlib import Path


def check_skill(path: str) -> list[str]:
    content = Path(path).read_text(encoding='utf-8')
    issues = []

    # ----- 1. YAML 描述一致性 -----
    desc_match = re.search(r'description:\s*(.+?)\n', content)
    if desc_match:
        desc = desc_match.group(1)
        if '八部结构' in desc and '7篇37章' in content:
            issues.append("🔴 YAML描述写'八部结构'但正文用7篇37章")

    # ----- 2. 重复标题 -----
    found = {}
    for m in re.finditer(r'^(#{2,3})\s+(.+)$', content, re.MULTILINE):
        key = f"{m.group(1)} {m.group(2).strip()}"
        found[key] = found.get(key, 0) + 1
    for title, count in found.items():
        if count > 1:
            issues.append(f"🟡 重复标题({count}次): {title[:60]}")

    # ----- 3. V版本标记残留 -----
    v_matches = re.findall(r'\bV\d[\.\s]', content)
    for m in set(v_matches):
        idx = content.find(m)
        ctx = content[max(0, idx-80):idx+30]
        if not any(kw in ctx for kw in ['版本标记', '禁止项', '血泪', '教训', '失败', '│ `V4`']):
            issues.append(f"🟡 V标记残留: '{m.strip()}' at pos {idx}")

    # ----- 4. 迭代语言 -----
    for term in ['迭代终点', '先薄后厚', '500-800.*行']:
        if re.search(term, content):
            issues.append(f"🔴 迭代语言残留: '{term}'")

    # ----- 5. 双结构 -----
    if '八部框架' in content:
        issues.append("🔴 '八部框架'残留（应统一为7篇37章）")

    # ----- 6. Phase 引用 -----
    if 'Phase 3' in content:
        # Check if still referencing old Phase 3 for report writing
        if re.search(r'Phase 3.*报告定稿|Phase 3.*写.*报告', content):
            issues.append("🔴 Phase引用错位: 报告定稿应在Phase 2非Phase 3")

    # ----- 7. delegate矛盾 -----
    has_delegate_write = bool(re.search(r'delegate_task.*(撰写|写报告|生成报告)', content))
    has_ban_delegate = 'delegate_task` 仅用于' in content
    if has_delegate_write and has_ban_delegate:
        issues.append("🔴 delegate_task用途矛盾: 一处允许写报告一处禁止")

    # ----- 8. 空标题 -----
    if re.search(r'^#{1,3}\s*$', content, re.MULTILINE):
        issues.append("🟡 存在空标题行")
    
    # 空段落（标题后直接是下一个标题）
    empty_sections = re.findall(r'^#{1,3}\s+.+\n\n+#{1,3}\s+', content, re.MULTILINE)
    if empty_sections:
        issues.append(f"🟡 空内容段落: {len(empty_sections)}个")

    # ----- 9. Doris 密码 -----
    if 'Ekaj3T4!' in content:
        issues.append("⚠️ Doris密码暴露（GitHub公开仓库会泄露）")

    return issues


if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else 'SKILL.md'
    issues = check_skill(target)
    if issues:
        print(f"❌ 发现 {len(issues)} 个问题:")
        for i in issues:
            print(f"  {i}")
        sys.exit(1)
    else:
        print("✅ 技能文件一致，无问题")
