# 数据集说明
# 将你的训练数据放在此目录下

## 格式要求

### 标准指令微调格式 (JSONL)

```json
{"instruction": "你的指令", "input": "输入内容（可为空）", "output": "期望输出"}
```

### 对话格式 (JSONL)

```json
{"messages": [{"role": "system", "content": "系统提示"}, {"role": "user", "content": "用户输入"}, {"role": "assistant", "content": "助手回复"}]}
```

## 文件说明

- `train.jsonl` - 训练集
- `eval.jsonl` - 验证集
- `test.jsonl` - 测试集（可选）
- `raw.jsonl` - 原始数据（预处理前）
