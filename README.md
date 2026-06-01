# 自动化专业导师模型 - 大模型微调项目

基于 Qwen2.5-1.5B + LoRA 的自动化专业导师模型微调实践项目，支持多种免费微调方案。

## 快速开始

### 推荐流程：讯飞平台 + 免费GPU 混合方案

**充分利用讯飞平台的免费数据处理工具 + 免费GPU进行微调**

#### 阶段1：数据准备（讯飞平台免费功能）

1. 登录 https://training.xfyun.cn/modelSquare
2. 使用"问答对抽取"从原始文档提取问答对
3. 使用"数据增强"扩充训练数据（推荐2-3倍）
4. 使用"Prompt工程"优化instruction格式
5. 导出 JSONL 格式

详见 [讯飞平台数据准备指南](docs/xfyun_data_prep_guide.md)

**本地数据增强（备用方案）：**
```bash
python scripts/enhance_data.py --input data/automation_advisor.jsonl --output data/enhanced.jsonl --factor 2
```

#### 阶段2：模型微调（免费GPU）

- Google Colab / Kaggle / 本地
- 使用 Qwen2.5-1.5B + LoRA

#### 阶段3：模型评估

- 本地测试 / 讯飞平台评估

详见 [平台集成指南](docs/platform_integration.md)

---

### 方案一：Google Colab（推荐）

**GPU：** T4 16GB（免费，无时间限制）

1. 打开 [Google Colab](https://colab.research.google.com/)
2. 上传 `notebooks/fine_tune_colab.ipynb`
3. 运行时 → 更改运行时类型 → 选择 **T4 GPU**
4. 按顺序运行每个单元格

### 方案二：Kaggle

**GPU：** T4 x2 16GB（每周30小时免费）

1. 打开 [Kaggle](https://www.kaggle.com/)
2. 创建新 Notebook
3. 上传 `notebooks/fine_tune_kaggle.ipynb`
4. 设置 → Accelerator → 选择 **GPU T4 x2**
5. 按顺序运行每个单元格

### 方案三：本地运行

**要求：** NVIDIA GPU（4GB+ 显存）

```bash
# Windows
双击运行 run_local.bat

# 或手动执行
pip install -q transformers peft datasets accelerate bitsandbytes trl
python scripts/local_finetune.py
```

**已测试配置：** RTX 3050 4GB（自动优化参数以适配小显存）

---

## 项目详情

## 平台简介

讯飞星辰MaaS微调平台以星火认知大模型和优质开源大模型为基础，提供数据管理、模型微调、评估、托管等全生命周期管理，支持零代码微调。

## 基座模型选择

| 模型 | 参数量 | 适用场景 | 显存需求 |
|------|--------|----------|----------|
| Qwen2.5-0.5B-Instruct | 0.5B | 超轻量级，适合极小显存 | 2GB |
| Qwen2.5-1.5B-Instruct | 1.5B | 轻量级，性能与资源平衡 | 4GB |
| Qwen2.5-3B-Instruct | 3B | 中等规模，效果更好 | 8GB |
| Qwen2.5-7B-Instruct | 7B | 高精度，需要较大显存 | 16GB |

本项目选用：**Qwen2.5-1.5B-Instruct**（适合 4GB 显存的 RTX 3050）

## 微调方法

- **LoRA**（低秩适配）：仅更新少量参数，资源需求低，训练快，减少过拟合风险
- **FFT**（全参数微调）：调整所有参数，充分利用模型表示能力，适合高精度需求

本项目使用：**LoRA**（低秩适配）

### LoRA 配置

```python
LoraConfig(
    r=4,                    # 秩（小显存用4，大显存可用8-16）
    lora_alpha=8,           # 缩放系数
    lora_dropout=0.05,      # 随机丢弃
    target_modules=["q_proj", "v_proj"],  # 目标模块
)
```

## 数据集

### 格式要求（Alpaca格式）

平台支持 JSON / JSONL / CSV 格式，标准字段如下：

```json
{
  "instruction": "任务指令（与input拼接形成模型输入）",
  "input": "输入内容",
  "output": "期望输出",
  "system": "系统提示词（可选）",
  "history": [["历史问题", "历史回答"]]  // 可选
}
```

### 示例（情感分类）

```json
{
  "instruction": "你是一个情感分析助手，目标是辨别推文的情感倾向，情感倾向分为积极和消极。接下来，我会给你推文的内容，请你告诉我情感分析的答案",
  "input": "一百多和三十的也看不出什么区别，包装精美，质量应该不错",
  "output": "积极"
}
```

### 数据集划分

推荐比例：70% 训练集 / 15% 验证集 / 15% 测试集

## 训练参数

| 参数 | 说明 | 影响 |
|------|------|------|
| 学习率 | 权重更新步长 | 较小更稳定但需更多迭代 |
| 训练次数 | 数据集迭代轮数 | 过多可能导致过拟合 |
| 分词最大长度 | 输入序列最大长度 | 超长需截断处理 |
| 数值精度 | 计算数据类型 | auto 自动选择 |
| LoRA秩 | 低秩矩阵复杂度 | 小→防过拟合，大→强表示 |
| LoRA随机丢弃 | 防过拟合概率 | 默认0.01（1%） |
| LoRA缩放系数 | 学习率缩放因子 | 过高过度微调，过低效果不足 |

## 工作流程

```
1. 构建数据集 → 2. 选择基座模型 → 3. 配置参数 → 4. 提交训练 → 5. 评估 → 6. 部署发布
```

### 在平台上的操作步骤

1. **构建数据集**：数据集管理 → 创建数据集 / 使用预置数据集
2. **创建模型**：模型管理 → 创建模型 → 选择基座模型
3. **数据配置**：选择训练集 → 配置字段映射（prompt→instruction, text→input, label→output）
4. **参数配置**：调整学习率、训练次数、LoRA参数等
5. **提交训练**：运行任务，等待状态变为"运行成功"，查看loss曲线
6. **发布服务**：发布为API/SDK → 在开放平台创建应用 → 授权发布
7. **在线评估**：体验中心测试 → 批量推理 → 模型评估（相似度打分/裁判员打分）

## 数据辅助工具

平台提供三种数据优化工具：
- **问答对抽取**：从文本/链接自动切分问答对，正确率90%+，覆盖率75%+
- **数据增强**：批量增强数据集，支持选择增强倍数和质量
- **Prompt工程**：50+常见prompt模板，满足多种数据需求

## 效果对比

| 指标 | 微调前 | 微调后 |
|------|--------|--------|
| [待填写] | - | - |

## 目录结构

```
├── README.md                    # 项目说明
├── run_local.bat                # Windows 一键运行脚本
├── requirements.txt             # Python 依赖
├── data/
│   ├── README.md                # 数据格式说明
│   ├── sample.jsonl             # 示例数据（5条）
│   └── automation_advisor.jsonl # 训练数据（151条）
├── notebooks/
│   ├── fine_tune_colab.ipynb    # Google Colab 微调 notebook
│   └── fine_tune_kaggle.ipynb   # Kaggle 微调 notebook
├── scripts/
│   ├── preprocess.py            # 数据预处理
│   ├── validate_data.py         # 数据验证
│   ├── evaluate.py              # 模型评估
│   ├── inference.py             # 模型推理
│   └── local_finetune.py        # 本地微调脚本
├── configs/
│   └── training_config.yaml     # 训练配置
└── results/                     # 评估结果
```

## 参考资料

### 免费 GPU 平台
- [Google Colab](https://colab.research.google.com/) - T4 16GB，免费无时间限制
- [Kaggle](https://www.kaggle.com/) - T4 x2 16GB，每周30小时免费

### 模型和文档
- [Qwen2.5 模型库](https://huggingface.co/Qwen) - 基座模型
- [PEFT 文档](https://huggingface.co/docs/peft) - LoRA 微调库
- [TRL 文档](https://huggingface.co/docs/trl) - 训练库

### 其他资源
- [讯飞星辰MaaS微调平台](https://training.xfyun.cn/modelSquare) - 付费平台（可选）
- [大模型微调学习笔记（CSDN）](https://blog.csdn.net/yang2330648064/article/details/149606413)
- [大模型微调基础入门](https://www.xfyun.cn/)
