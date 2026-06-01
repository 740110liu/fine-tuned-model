"""模型评估脚本 - 基于讯飞星辰MaaS平台批量推理结果"""
import json
import argparse
from collections import Counter


def load_jsonl(path: str) -> list:
    data = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                data.append(json.loads(line))
    return data


def exact_match_eval(predictions: list, references: list) -> dict:
    """精确匹配评估（适用于分类任务）"""
    correct = sum(1 for p, r in zip(predictions, references) if p.strip() == r.strip())
    total = len(predictions)
    return {
        "total": total,
        "correct": correct,
        "accuracy": correct / total if total > 0 else 0,
    }


def eval_from_files(pred_path: str, ref_path: str, pred_field="output", ref_field="output"):
    """对比预测结果与参考答案"""
    preds = load_jsonl(pred_path)
    refs = load_jsonl(ref_path)

    pred_outputs = [item.get(pred_field, "") for item in preds]
    ref_outputs = [item.get(ref_field, "") for item in refs]

    if len(pred_outputs) != len(ref_outputs):
        print(f"警告：预测结果({len(pred_outputs)})与参考答案({len(ref_outputs)})数量不一致")

    results = exact_match_eval(pred_outputs, ref_outputs)

    print("=" * 50)
    print("评估结果")
    print("=" * 50)
    print(f"总样本数: {results['total']}")
    print(f"正确数:   {results['correct']}")
    print(f"准确率:   {results['accuracy']:.2%}")
    print("=" * 50)

    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="评估模型预测结果")
    parser.add_argument("--pred", type=str, required=True, help="预测结果文件 (jsonl)")
    parser.add_argument("--ref", type=str, required=True, help="参考答案文件 (jsonl)")
    parser.add_argument("--pred_field", type=str, default="output", help="预测结果字段名")
    parser.add_argument("--ref_field", type=str, default="output", help="参考答案字段名")
    args = parser.parse_args()
    eval_from_files(args.pred, args.ref, args.pred_field, args.ref_field)
