"""模型评估脚本"""
import argparse

# TODO: 取消注释你需要的
# from transformers import AutoModelForCausalLM, AutoTokenizer
# import evaluate


def evaluate(model_path: str, eval_data: str):
    print(f"评估模型: {model_path}")
    print(f"评估数据: {eval_data}")
    # TODO: 实现评估逻辑
    # 1. 加载微调后的模型
    # 2. 在测试集上推理
    # 3. 计算指标（accuracy / rouge / BLEU 等）
    # 4. 输出结果
    raise NotImplementedError("请实现评估逻辑")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="./results/final")
    parser.add_argument("--eval_data", type=str, default="data/eval.jsonl")
    args = parser.parse_args()
    evaluate(args.model, args.eval_data)
