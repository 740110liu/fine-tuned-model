"""数据预处理脚本 - 讯飞星辰MaaS平台适配"""
import json
import csv
import argparse
import random
from pathlib import Path


# 讯飞星辰MaaS平台 Alpaca 格式字段映射
FIELD_MAP = {
    "prompt": "instruction",
    "text": "input",
    "label": "output",
    "question": "instruction",
    "answer": "output",
    "context": "input",
}


def normalize_fields(item: dict) -> dict:
    """将常见字段名映射为 Alpaca 标准格式 (instruction/input/output)"""
    result = {}
    for key, value in item.items():
        mapped_key = FIELD_MAP.get(key, key)
        result[mapped_key] = value
    return result


def to_alpaca(item: dict) -> dict:
    """确保输出为标准 Alpaca 格式"""
    item = normalize_fields(item)
    return {
        "instruction": item.get("instruction", ""),
        "input": item.get("input", ""),
        "output": item.get("output", ""),
    }


def load_jsonl(path: str) -> list:
    data = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                data.append(json.loads(line))
    return data


def load_csv(path: str) -> list:
    data = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(dict(row))
    return data


def load_json(path: str) -> list:
    with open(path, "r", encoding="utf-8") as f:
        content = json.load(f)
        if isinstance(content, list):
            return content
        return [content]


def save_jsonl(data: list, path: str):
    with open(path, "w", encoding="utf-8") as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")


def split_dataset(data: list, train_ratio=0.7, eval_ratio=0.15, seed=42):
    """按比例划分训练集、验证集、测试集"""
    random.seed(seed)
    shuffled = data.copy()
    random.shuffle(shuffled)
    n = len(shuffled)
    train_end = int(n * train_ratio)
    eval_end = int(n * (train_ratio + eval_ratio))
    return shuffled[:train_end], shuffled[train_end:eval_end], shuffled[eval_end:]


def preprocess(input_path: str, output_dir: str, split: bool = False, seed: int = 42):
    """将原始数据转换为讯飞星辰MaaS平台标准 Alpaca 格式"""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 加载数据
    suffix = Path(input_path).suffix.lower()
    if suffix == ".csv":
        raw_data = load_csv(input_path)
    elif suffix == ".json":
        raw_data = load_json(input_path)
    else:
        raw_data = load_jsonl(input_path)

    # 转换为 Alpaca 格式
    alpaca_data = [to_alpaca(item) for item in raw_data]
    print(f"加载 {len(raw_data)} 条数据，已转换为 Alpaca 格式")

    if split:
        train, eval_data, test = split_dataset(alpaca_data, seed=seed)
        save_jsonl(train, str(output_dir / "train.jsonl"))
        save_jsonl(eval_data, str(output_dir / "eval.jsonl"))
        save_jsonl(test, str(output_dir / "test.jsonl"))
        print(f"已划分：训练集 {len(train)} / 验证集 {len(eval_data)} / 测试集 {len(test)}")
    else:
        save_jsonl(alpaca_data, str(output_dir / "train.jsonl"))
        print(f"已保存到 {output_dir / 'train.jsonl'}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="数据预处理 - 讯飞星辰MaaS平台")
    parser.add_argument("--input", type=str, required=True, help="输入文件路径 (jsonl/json/csv)")
    parser.add_argument("--output_dir", type=str, default="data", help="输出目录")
    parser.add_argument("--split", action="store_true", help="是否划分训练/验证/测试集")
    parser.add_argument("--seed", type=int, default=42, help="随机种子")
    args = parser.parse_args()
    preprocess(args.input, args.output_dir, args.split, args.seed)
