"""
把 hasu_dictionary.json 轉成 VideoLingo 的 custom_terms.xlsx
在 VideoLingo 環境內執行：uv run python hasu_to_custom_terms.py
"""
import json
import pandas as pd

with open("hasu_dictionary.json", encoding="utf-8") as f:
    d = json.load(f)

rows = []

def parse_rule(rule_str, note_prefix=""):
    """把 'A -> B (說明)' 解析成 (src, tgt, note)"""
    left, right = rule_str.split("->", 1)
    src = left.strip()
    right = right.strip()
    if "(" in right:
        tgt = right[:right.index("(")].strip()
        note = right[right.index("(")+1:right.rindex(")")].strip()
    else:
        tgt = right.strip()
        note = note_prefix
    return src, tgt, note

# 1. 企劃/活動名稱 → 保留原文
for rule in d["translation_rules"]:
    src, tgt, note = parse_rule(rule, "固有名詞・原文のまま")
    rows.append({"src": src, "tgt": tgt, "note": note})

# 2. 角色稱謂關係 (先輩/ちゃん)
for rule in d["character_relations"]:
    src, tgt, note = parse_rule(rule, "キャラクター呼称")
    rows.append({"src": src, "tgt": tgt, "note": "角色稱謂，" + note if note == "キャラクター呼称" else note})

# 3. 聲優暱稱 → 保留原文
for rule in d["cast_nicknames"]:
    src, tgt, note = parse_rule(rule, "聲優暱稱・原文のまま")
    rows.append({"src": src, "tgt": tgt, "note": note})

df = pd.DataFrame(rows, columns=["src", "tgt", "note"])
df.to_excel("custom_terms.xlsx", index=False)

print(f"✅ 寫入 custom_terms.xlsx 完成，共 {len(df)} 筆詞條")
print(df.to_string())
