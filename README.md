# Qwen2-VL 肺炎 X 光片智能诊断助手

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![ModelScope Model](https://img.shields.io/badge/ModelScope-Model-orange)](https://modelscope.cn/models/lyeroq/Qwen2-VL-Pneumonia-Finetuned)

本项目基于 **Qwen2-VL-7B-Instruct** 多模态大语言模型，使用 **LoRA** 方法进行微调，使其能够对胸部 X 光片进行专业级分析，识别并描述肺炎征象（如大叶性实变、磨玻璃影、支气管充气征等）。微调后的模型已开源至 **ModelScope** 社区，本仓库包含完整的训练脚本、数据集及配置文件，用于模型的复现和二次开发。

> 🩺 **项目亮点**：一个可直接运行的肺炎 X 光片辅助诊断演示，展示了如何将通用多模态大模型适配到医疗影像领域。

---

## 📌 目录

- [模型链接](#模型链接)
- [数据集](#数据集)
- [训练方法](#训练方法)
- [使用方式](#使用方式)
- [效果示例](#效果示例)
- [项目结构](#项目结构)
- [局限性](#局限性)
- [致谢](#致谢)

---

## 🤗 模型链接

微调后的完整模型（包含合并后的权重）已上传至 **ModelScope**，可直接下载使用：

👉 [https://modelscope.cn/models/lyeroq/Qwen2-VL-Pneumonia-Finetuned](https://modelscope.cn/models/lyeroq/Qwen2-VL-Pneumonia-Finetuned)

你可以使用 ModelScope SDK 或 Git 直接下载模型。

---

## 📊 数据集

- **来源**：[Kaggle Chest X-Ray Images (Pneumonia)](https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia)
- **规模**：共 5856 张胸部 X 光片，包含肺炎阳性样本约 4000 张，正常样本约 1800 张。
- **预处理**：为每张图像配对了医生撰写的诊断描述，构建为指令微调对话数据（`human` 提问，`gpt` 回答）。最终指令数据集位于 `data/pneumonia_instructions.json`。

示例数据格式：
```json
{
  "conversations": [
    {
      "from": "human",
      "value": "请分析这张胸部X光片是否存在肺炎特征？ \\n \\n"
    },
    {
      "from": "gpt",
      "value": "影像显示右肺中叶大叶性实变，伴支气管充气征，符合细菌性肺炎。"
    }
  ],
  "images": ["path/to/xray.jpg"]
}
```
## 🛠️ 训练方法
基座模型：Qwen/Qwen2-VL-7B-Instruct

微调框架：LLaMA-Factory

微调方法：LoRA（秩 r=8, alpha=16）

训练参数：

学习率：1e-4

训练轮数：3

批处理大小：1（梯度累积步数 1）

精度：bfloat16

优化器：AdamW

最大序列长度：1024

保存步数：500（保留最近 2 个检查点）

硬件环境：单卡 NVIDIA GPU（显存约 24GB）

训练命令详见 chuli/one.sh。

## 🚀 使用方式
1. 直接加载合并后的完整模型（推荐）
```python
from transformers import AutoModelForCausalLM, AutoProcessor
import torch

model = AutoModelForCausalLM.from_pretrained(
    "lyeroq/Qwen2-VL-Pneumonia-Finetuned",
    trust_remote_code=True,
    torch_dtype=torch.bfloat16,
    device_map="auto"
)
processor = AutoProcessor.from_pretrained(
    "lyeroq/Qwen2-VL-Pneumonia-Finetuned",
    trust_remote_code=True
)

# 推理示例
from PIL import Image
image = Image.open("chest_xray.jpg")
prompt = "请分析这张胸部X光片是否存在肺炎特征？"
inputs = processor(text=prompt, images=image, return_tensors="pt")
output = model.generate(**inputs)
response = processor.decode(output[0], skip_special_tokens=True)
print(response)
```
2. 使用 ModelScope SDK 下载
```python
from modelscope import snapshot_download
model_dir = snapshot_download('lyeroq/Qwen2-VL-Pneumonia-Finetuned')
```
3. 使用 Git 下载
```bash
git clone https://www.modelscope.cn/lyeroq/Qwen2-VL-Pneumonia-Finetuned.git
```
## 🎯 效果示例
用户提问	                                                        模型回答
请分析这张胸部X光片是否存在肺炎特征？	影像显示右肺中叶大叶性实变，伴支气管充气征，符合细菌性肺炎。
请分析这张胸部X光片是否存在肺炎特征？	影像显示双肺多发斑片状、磨玻璃样密度增高影，符合病毒性肺炎。
请分析这张胸部X光片是否存在肺炎特征？	影像显示正常，未见明确的肺炎特征。
## 📂 项目结构
```text
.
├── chuli/                      # 训练脚本目录
│   └── one.sh                  # 主训练脚本
├── data/
│   ├── pneumonia_instructions.json   # 指令微调数据集
│   └── dataset_info.json             # 数据集注册配置
├── .gitignore                  # Git 忽略规则
├── upload_to_modelscope.py     # ModelScope 上传脚本
└── README.md                   # 项目说明
```
注：本仓库不包含原始 X 光图片及模型权重文件（已通过 .gitignore 忽略），图片请从 Kaggle 下载，模型权重请从 ModelScope 获取。

## ⚠️ 局限性
辅助诊断性质：模型输出仅为参考，不能替代专业医生的诊断。

数据来源单一：仅基于 Kaggle 公开数据集，泛化能力有限，不同医院/设备的影像可能效果下降。

仅限 X 光片：不适用于 CT、MRI 等其他医学影像模态。

## 🙏 致谢
QwenLM 开源多模态模型

LLaMA-Factory 高效微调框架

Kaggle Chest X-Ray Images (Pneumonia) 数据集

## 📜 许可证
本项目代码遵循 Apache License 2.0 开源协议。模型权重使用需遵守 Qwen 系列模型的许可协议。

## 📧 联系
如有问题或建议，欢迎提 Issue 或通过 GitHub 联系。

项目链接：https://github.com/LuKiovo/qwen2vl-pneumonia-detector
模型链接：https://modelscope.cn/models/lyeroq/Qwen2-VL-Pneumonia-Finetuned
