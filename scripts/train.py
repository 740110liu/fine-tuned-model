"""模型微调训练脚本"""
import argparse
import yaml
from pathlib import Path

# TODO: 取消注释你需要的框架
# from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
# from peft import LoraConfig, get_peft_model, TaskType
# from trl import SFTTrainer
# from datasets import load_dataset


def load_config(config_path: str) -> dict:
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def train(config_path: str):
    config = load_config(config_path)
    print("训练配置:", config)
    # TODO: 实现训练逻辑
    # 1. 加载模型和 tokenizer
    # 2. 配置 LoRA / 全量微调
    # 3. 加载数据集
    # 4. 开始训练
    # 5. 保存模型
    raise NotImplementedError("请根据你的基座模型和微调方法实现训练逻辑")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default="configs/training_config.yaml")
    args = parser.parse_args()
    train(args.config)
