# L5 · 权重之上 / Beyond Weights

**保留来源、版本与决策依据，让规则可追溯。**

GROUNDSTATE 的来源与治理节点，记录代码、模型权重、数据集、服务和预期使用方式之间的关系。

当前状态：**v0.1 元数据清单检查器**。帮助发现缺失字段及未完成的复核，不输出商用许可结论。

## 先运行

Python 3.11+，仅标准库。

```bash
python inventory_check.py examples/component-inventory.json
python -m unittest discover -s tests -v
```

演示清单只记录本仓库原创工具及 MIT 文本，复核状态仍为 `pending`。加上 `--strict` 时，存在缺失项或待复核项会退出 1；普通模式打印报告并退出 0。`reviewed` 需要复核人、ISO 日期及说明，但依然不等于获得使用许可。

## 核查口径

每项填写名称、版本、类型、来源 URL、许可表达式、该版本的许可文本 URL 和预期用途。代码、权重、训练数据、输入素材和托管服务的条款分别核查；无法确认时保留缺失并待查。

SPDX 标识符可用于一致记录许可名称；本工具只检查该字段非空，不验证表达式语法、链接真实性、许可兼容性、隐私合规或适用法律。参见 [SPDX 的许可信息说明](https://spdx.dev/learn/handling-license-info/)。

使用 [复核记录模板](templates/review-note.md) 保存依据。不要将元数据完整改写为“可商用”，或用一张红绿灯图替代具体版本与用途的复核。

下一步：表达式解析、来源快照、变更追踪和人工复核流程。均待实现。

[总纲](https://github.com/nova-frontier/manifesto) · [提出问题](https://github.com/nova-frontier/agentic-order-spec/issues) · [贡献](CONTRIBUTING.md) · [MIT](LICENSE)
