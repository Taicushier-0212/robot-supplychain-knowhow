# 电子器件

**大类：** 供电、算力、驱动板、互连。电气会签 BOM；供应链跟交期、防静电和线束验收。

长周期器件在 G0 标红。线束禁止「看着能插」过检。

## 小类

| 小类 | 干什么 | 入口 |
|---|---|---|
| PCB / SMT | 裸板与贴片；层数、铜厚、表面处理 | [pcb.md](./pcb.md) |
| 线束 | 动力线、信号线、整机互联 | [harness.md](./harness.md)（[线材 / AWG](./wire/README.md)） |
| 接插件 | 可拆互连、防呆；XT30（2+2）、GMSL/FAKRA 等 | [connectors/](./connectors/README.md) |
| 算力 / 主控 | 规划、推理、全身调度；RK / RDK / Orin / AGX / Thor 对照 | [compute.md](./compute.md) |
| 电源模块 | 母线、DCDC、预充 | [power.md](./power.md) |

关节驱动器若做成模组内驱，主文档在 [关节模组 / 驱动器](../01-joint-modules/driver.md)；这里管板级电源和整机配电。
