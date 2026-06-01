"""数据预处理脚本"""
import json
import argparse
from pathlib import Path


def preprocess(input_path: str, output_path: str, max_samples: int = None):
    """将原始数据转换为训练格式"""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    with open(input_path, "r", encoding="utf-8") as f_in, \
         open(output_path, "w", encoding="utf-8") as f_out:
        for i, line in enumerate(f_in):
            if max_samples and i >= max_samples:
                break
            item = json.loads(line)
            # TODO: 根据实际数据格式转换
            formatted = {
                "instruction": item.get("instruction", ""),
                "input": item.get("input", ""),
                "output": item.get("output", ""),
            }
            f_out.write(json.dumps(formatted, ensure_ascii=False) + "\n")

    print(f"预处理完成，输出到 {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default="data/raw.jsonl")
    parser.add_argument("--output", type=str, default="data/train.jsonl")
    parser.add_argument("--max_samples", type=int, default=None)
    args = parser.parse_args()
    preprocess(args.input, args.output, args.max_samples)
