"""本地推理测试脚本 - 用于快速测试微调效果"""
# 注意：主要训练和评估在讯飞星辰MaaS平台完成
# 此脚本仅用于本地快速验证，需要安装相关依赖

import argparse


def test_inference(model_path: str, prompt: str, input_text: str = ""):
    """
    本地推理测试
    需要根据使用的模型安装对应依赖（如 transformers, peft 等）
    """
    print(f"模型路径: {model_path}")
    print(f"指令: {prompt}")
    print(f"输入: {input_text}")
    print()
    # TODO: 实现本地推理逻辑
    # 示例（使用 transformers + peft）：
    # from transformers import AutoModelForCausalLM, AutoTokenizer
    # from peft import PeftModel
    #
    # tokenizer = AutoTokenizer.from_pretrained(model_path)
    # model = AutoModelForCausalLM.from_pretrained(model_path)
    # model = PeftModel.from_pretrained(model, adapter_path)
    #
    # full_prompt = f"{prompt}\n{input_text}" if input_text else prompt
    # inputs = tokenizer(full_prompt, return_tensors="pt")
    # outputs = model.generate(**inputs, max_new_tokens=256)
    # print(tokenizer.decode(outputs[0], skip_special_tokens=True))
    print("请根据你的模型实现推理逻辑，或直接在讯飞MaaS平台在线体验。")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="本地推理测试")
    parser.add_argument("--model", type=str, default="./results/final")
    parser.add_argument("--prompt", type=str, required=True, help="任务指令")
    parser.add_argument("--input", type=str, default="", help="输入内容")
    args = parser.parse_args()
    test_inference(args.model, args.prompt, args.input)
