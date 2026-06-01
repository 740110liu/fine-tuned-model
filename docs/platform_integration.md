# 讯飞星辰MaaS平台 + 免费GPU 微调完整流程

## 平台功能对比

| 功能 | 讯飞星辰MaaS | Google Colab | Kaggle |
|------|-------------|--------------|--------|
| 数据处理工具 | ✅ 免费 | ❌ 需自己实现 | ❌ 需自己实现 |
| 问答对抽取 | ✅ 免费（90%+准确率） | ❌ | ❌ |
| 数据增强 | ✅ 免费 | ❌ | ❌ |
| Prompt模板 | ✅ 50+模板 | ❌ | ❌ |
| 模型微调 | ⚠️ 可能需付费 | ✅ 免费 | ✅ 免费 |
| 模型评估 | ✅ 免费 | ✅ 需自己实现 | ✅ 需自己实现 |
| 模型部署 | ✅ 付费 | ❌ | ❌ |

## 推荐流程：混合方案

### 阶段1：数据准备（使用讯飞平台免费功能）

**1.1 问答对抽取**
- 登录 https://training.xfyun.cn/modelSquare
- 使用"问答对抽取"工具
- 从原始文本自动切分问答对
- 正确率90%+，覆盖率75%+

**1.2 数据增强**
- 使用"数据增强"工具
- 选择增强倍数（2x-5x）
- 自动扩展训练数据

**1.3 Prompt工程**
- 使用"Prompt工程"工具
- 选择50+预设模板
- 优化 instruction 格式

**1.4 数据导出**
- 导出为 JSONL 格式
- 确保符合 Alpaca 格式：
  ```json
  {"instruction": "...", "input": "...", "output": "..."}
  ```

### 阶段2：模型微调（使用免费GPU）

**方案A：Google Colab（推荐）**
1. 上传 `notebooks/fine_tune_colab.ipynb`
2. 上传从讯飞平台导出的数据
3. 运行时 → T4 GPU
4. 按顺序执行

**方案B：Kaggle**
1. 上传 `notebooks/fine_tune_kaggle.ipynb`
2. 上传从讯飞平台导出的数据
3. 设置 → GPU T4 x2
4. 按顺序执行

**方案C：本地（RTX 3050）**
1. 将数据放入 `data/` 目录
2. 运行 `run_local.bat`

### 阶段3：模型评估（可选：使用讯飞平台）

**3.1 本地评估**
```bash
python scripts/evaluate.py
```

**3.2 讯飞平台评估**
- 上传微调后的模型到讯飞平台
- 使用平台的评估工具：
  - 相似度打分
  - 裁判员打分
  - 多维度评测

## 数据处理脚本

### 从讯飞平台导出数据后，使用以下脚本验证格式：

```bash
python scripts/validate_data.py data/your_exported_data.jsonl
```

### 数据预处理（如需要）：

```bash
python scripts/preprocess.py --input data/raw/ --output data/processed/
```

## 完整工作流示例

```
1. 原始数据
   ↓
2. 讯飞平台 - 问答对抽取（免费）
   ↓
3. 讯飞平台 - 数据增强（免费）
   ↓
4. 讯飞平台 - Prompt优化（免费）
   ↓
5. 导出 JSONL 数据
   ↓
6. Google Colab - LoRA 微调（免费）
   ↓
7. 下载微调模型
   ↓
8. 本地测试 / 讯飞平台评估
   ↓
9. 部署（可选）
```

## 注意事项

1. **数据格式**：确保导出数据符合 Alpaca 格式
2. **模型大小**：免费GPU适合 1.5B-3B 参数的模型
3. **训练时间**：Colab 无时间限制，Kaggle 每周30小时
4. **保存模型**：训练完成后及时下载，避免丢失

## 参考链接

- [讯飞星辰MaaS平台](https://training.xfyun.cn/modelSquare)
- [Google Colab](https://colab.research.google.com/)
- [Kaggle](https://www.kaggle.com/)
- [Qwen2.5 模型](https://huggingface.co/Qwen)
