#!/usr/bin/env python3
"""
数据增强脚本
用于扩充训练数据，提高微调效果
"""

import json
import random
import argparse
from pathlib import Path

def load_jsonl(file_path):
    """加载 JSONL 文件"""
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                data.append(json.loads(line))
    return data

def save_jsonl(data, file_path):
    """保存 JSONL 文件"""
    with open(file_path, 'w', encoding='utf-8') as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

def enhance_instruction_variations(item):
    """生成 instruction 变体"""
    variations = []

    # 原始数据
    variations.append(item)

    # 添加前缀变体
    prefixes = [
        "请问",
        "请告诉我",
        "我想了解",
        "能否解释一下",
        "帮我解答一下",
    ]

    for prefix in prefixes[:2]:  # 每条数据生成2个变体
        new_item = item.copy()
        if 'instruction' in new_item:
            new_item['instruction'] = prefix + new_item['instruction']
        variations.append(new_item)

    return variations

def enhance_with_system_prompt(item):
    """添加系统提示词变体"""
    variations = []

    # 原始数据
    variations.append(item)

    # 如果没有 system 字段，添加默认系统提示
    if 'system' not in item or not item['system']:
        new_item = item.copy()
        new_item['system'] = "你是一位经验丰富的本科自动化专业指导导师。"
        variations.append(new_item)

    return variations

def enhance_dataset(data, enhance_factor=2):
    """
    增强数据集

    Args:
        data: 原始数据列表
        enhance_factor: 增强倍数（1=不增强，2=翻倍，3=三倍）
    """
    enhanced_data = []

    for item in data:
        # 原始数据
        enhanced_data.append(item)

        # instruction 变体
        if enhance_factor >= 2:
            variations = enhance_instruction_variations(item)
            enhanced_data.extend(variations[1:])  # 排除原始数据

        # system prompt 变体
        if enhance_factor >= 3:
            variations = enhance_with_system_prompt(item)
            enhanced_data.extend(variations[1:])  # 排除原始数据

    # 如果需要更多数据，随机复制
    if enhance_factor > 3:
        while len(enhanced_data) < len(data) * enhance_factor:
            random_item = random.choice(data)
            enhanced_data.append(random_item.copy())

    return enhanced_data

def main():
    parser = argparse.ArgumentParser(description='数据增强脚本')
    parser.add_argument('--input', '-i', required=True, help='输入文件路径')
    parser.add_argument('--output', '-o', required=True, help='输出文件路径')
    parser.add_argument('--factor', '-f', type=int, default=2, help='增强倍数（默认2）')
    parser.add_argument('--seed', '-s', type=int, default=42, help='随机种子')

    args = parser.parse_args()

    # 设置随机种子
    random.seed(args.seed)

    # 加载数据
    print(f"加载数据: {args.input}")
    data = load_jsonl(args.input)
    print(f"原始数据量: {len(data)} 条")

    # 增强数据
    print(f"开始增强，倍数: {args.factor}x")
    enhanced_data = enhance_dataset(data, args.factor)
    print(f"增强后数据量: {len(enhanced_data)} 条")

    # 保存数据
    save_jsonl(enhanced_data, args.output)
    print(f"数据已保存到: {args.output}")

    # 统计信息
    print(f"\n统计信息:")
    print(f"  - 原始数据: {len(data)} 条")
    print(f"  - 增强后: {len(enhanced_data)} 条")
    print(f"  - 增强倍数: {len(enhanced_data) / len(data):.1f}x")

if __name__ == '__main__':
    main()
