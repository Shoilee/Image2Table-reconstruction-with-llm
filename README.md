# NGTR  [![IJCAI 2025 Accepted](https://img.shields.io/badge/IJCAI-2025-blue)](https://2025.ijcai.org/)

Official implementation of the paper:
**Enhancing Table Recognition with Vision LLMs: A Benchmark and Neighbor-Guided Toolchain Reasoner**

🔗 [Paper on arXiv](https://arxiv.org/abs/2412.20662)

📌 Accepted at *IJCAI 2025*



## 🌟 Introduction

We present **NGTR** (Neighbor-Guided Toolchain Reasoner), a novel framework that enhances table recognition in document images by integrating **Vision Large Language Models (VLLMs)** with **lightweight visual tools** and **retrieval-augmented planning** strategies.

Despite the recent progress of VLLMs, their performance on table recognition tasks—particularly in **low-quality image** settings—remains under-explored. NGTR fills this gap through a modular reasoning pipeline and sets a new benchmark standard for structured data extraction from tables.

<div align="center">
  <img src="assets/model.png" width="100%" alt="NGTR Framework Architecture"/>
</div>

### 🚀 Key Contributions

* **Pioneering VLLM-based Table Recognition**: We introduce the first **comprehensive benchmark** that evaluates VLLMs in training-free table recognition tasks with **hierarchical evaluation** design.
* **Neighbor-Guided Reasoning Framework**: NGTR introduces a reflection-driven, modular toolchain system to **improve input quality and guide recognition** effectively.
* **Extensive Evaluation**: Demonstrated state-of-the-art performance across **SciTSR**, **PubTabNet**, and **WTW** datasets, showcasing robustness in both clean and noisy table environments.



## 🛠️ Setup & Environment

This repo is built and tested under `Python 3.9.19`.
To set up the environment:

```bash
conda create -n NGTR python=3.9 -y
conda activate NGTR
pip install -r requirements.txt
```

---

## 📦 Running the Project

To run the main pipeline, execute:

```bash
python main.py
```

Please refer to the `main.py` file for detailed arguments and configuration instructions.

---

## 📚 Citation

---
>
> 🙋 Please let us know if you find out a mistake or have any suggestions!
> 
> 🌟 If you find this resource helpful, please consider to star this repository and cite our research:


```bibtex
@article{zhou2024enhancing,
  title={Enhancing Table Recognition with Vision LLMs: A Benchmark and Neighbor-Guided Toolchain Reasoner},
  author={Zhou, Yitong and Cheng, Mingyue and Mao, Qingyang and Liu, Qi and Xu, Feiyang and Li, Xin and Chen, Enhong},
  journal={arXiv preprint arXiv:2412.20662},
  year={2024}
}
```

---

## 🙏 Acknowledgements

This work builds on prior contributions and datasets from the following repositories:

* [SciTSR](https://github.com/Academic-Hammer/SciTSR)
* [PubTabNet](https://github.com/ibm-aur-nlp/PubTabNet)
* [WTW-Dataset](https://github.com/wangwen-whu/WTW-Dataset)
* [YOLOv10](https://github.com/THU-MIG/yolov10)
* [Upscayl](https://github.com/upscayl/upscayl)
