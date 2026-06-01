#!/usr/bin/env python3
"""
本地微调脚本 - 适用于 RTX 3050 4GB
使用 Qwen2.5-1.5B + LoRA 微调
"""

import json
import torch
from datasets import Dataset
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import LoraConfig
from trl import SFTTrainer, SFTConfig

# 检查 GPU
if not torch.cuda.is_available():
    print("错误: 未检测到 CUDA GPU")
    exit(1)

print(f"GPU: {torch.cuda.get_device_name(0)}")
print(f"GPU显存: {torch.cuda.get_device_properties(0).total_mem / 1e9:.1f}GB")

# 加载数据
data_path = "data/automation_advisor.jsonl"
print(f"\n加载数据: {data_path}")

data = []
with open(data_path, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line:
            data.append(json.loads(line))

print(f"加载 {len(data)} 条训练数据")

# 转换为对话格式
def format_to_chat(example):
    messages = []
    if example.get("system"):
        messages.append({"role": "system", "content": example["system"]})
    user_content = example["instruction"]
    if example.get("input"):
        user_content += "\n" + example["input"]
    messages.append({"role": "user", "content": user_content})
    messages.append({"role": "assistant", "content": example["output"]})
    return {"messages": messages}

chat_data = [format_to_chat(d) for d in data]
dataset = Dataset.from_list(chat_data)
print(f"数据集准备完成")

# 加载模型
model_name = "Qwen/Qwen2.5-1.5B-Instruct"
print(f"\n加载模型: {model_name}")

tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,  # 使用 float16 节省显存
    device_map="auto",
    trust_remote_code=True,
)

print(f"模型参数量: {model.num_parameters() / 1e9:.2f}B")

# LoRA 配置（针对 4GB 显存优化）
lora_config = LoraConfig(
    r=4,  # 降低 rank 节省显存
    lora_alpha=8,
    lora_dropout=0.05,
    target_modules=["q_proj", "v_proj"],  # 减少目标模块
    task_type="CAUSAL_LM",
)

# 训练配置（针对 4GB 显存优化）
training_config = SFTConfig(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=1,  # 减小 batch size
    gradient_accumulation_steps=8,  # 增加梯度累积
    learning_rate=2e-4,
    warmup_ratio=0.1,
    logging_steps=10,
    save_strategy="epoch",
    fp16=True,  # 使用 fp16
    max_seq_length=512,  # 减小序列长度
    report_to="none",
    gradient_checkpointing=True,  # 启用梯度检查点节省显存
)

# 创建训练器
trainer = SFTTrainer(
    model=model,
    args=training_config,
    train_dataset=dataset,
    processing_class=tokenizer,
    peft_config=lora_config,
)

print("\n开始训练...")
print(f"训练样本数: {len(dataset)}")
print(f"训练轮数: {training_config.num_train_epochs}")
print(f"学习率: {training_config.learning_rate}")
print(f"LoRA rank: {lora_config.r}")
print("-" * 50)

trainer.train()
print("\n训练完成！")

# 保存模型
save_path = "./automation_advisor_lora"
model.save_pretrained(save_path)
tokenizer.save_pretrained(save_path)
print(f"模型已保存到: {save_path}")

# 测试
def chat(question, system_prompt=None):
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": question})

    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(text, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=256,
            temperature=0.7,
            do_sample=True,
        )

    response = tokenizer.decode(outputs[0][inputs['input_ids'].shape[1]:], skip_special_tokens=True)
    return response

print("\n测试微调效果:")
system = "你是一位经验丰富的本科自动化专业指导导师。"
test_questions = [
    "自动化专业大一应该学好哪些课程？",
    "考研还是就业，很纠结怎么办？",
]

for q in test_questions:
    print(f"\n{'='*50}")
    print(f"问题: {q}")
    answer = chat(q, system)
    print(f"回答: {answer}")
