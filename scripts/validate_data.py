"""数据格式校验脚本 - 讯飞星辰MaaS平台"""
import json
import argparse


REQUIRED_FIELDS = {"instruction", "output"}
OPTIONAL_FIELDS = {"input", "system", "history"}


def validate(filepath: str) -> bool:
    """校验数据集是否符合讯飞星辰MaaS平台 Alpaca 格式要求"""
    errors = []
    count = 0

    with open(filepath, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            count += 1
            try:
                item = json.loads(line)
            except json.JSONDecodeError as e:
                errors.append(f"第{i}行: JSON解析失败 - {e}")
                continue

            # 检查必填字段
            for field in REQUIRED_FIELDS:
                if field not in item:
                    errors.append(f"第{i}行: 缺少必填字段 '{field}'")

            # 检查是否有错误的字段名（常见错误）
            known_fields = REQUIRED_FIELDS | OPTIONAL_FIELDS
            for key in item:
                if key not in known_fields:
                    if key in ("prompt", "text", "label", "question", "answer"):
                        errors.append(f"第{i}行: 字段 '{key}' 应改为 '{({'prompt':'instruction','text':'input','label':'output','question':'instruction','answer':'output'}).get(key, key)}'")

    if errors:
        print(f"校验失败，发现 {len(errors)} 个问题：")
        for e in errors[:20]:
            print(f"  - {e}")
        if len(errors) > 20:
            print(f"  ... 还有 {len(errors) - 20} 个问题")
        return False

    print(f"校验通过！共 {count} 条数据，格式符合要求。")
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="校验数据集是否符合讯飞MaaS平台格式")
    parser.add_argument("file", type=str, help="数据集文件路径 (jsonl)")
    args = parser.parse_args()
    validate(args.file)
