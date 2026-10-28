# 机器人供应链

> 记机器人供应链的判断口径：这颗料是什么、用在哪一轴、选型必须冻住哪些字段、到货怎么验、上次踩过什么坑。

[在线阅读](https://taicushier-0212.github.io/robot-supplychain-knowhow/) · [GitHub Actions](https://github.com/Taicushier-0212/robot-supplychain-knowhow/actions) · [仓库](https://github.com/Taicushier-0212/robot-supplychain-knowhow)

[![Deploy documentation site](https://github.com/Taicushier-0212/robot-supplychain-knowhow/actions/workflows/pages.yml/badge.svg)](https://github.com/Taicushier-0212/robot-supplychain-knowhow/actions/workflows/pages.yml)

做人形机器人时，买料这件事会反复卡在同一类问题上：这颗料到底是什么、用在哪一轴、选型必须冻住哪些字段、到货怎么验、上次踩过什么坑。

这个仓库就是用来记这些判断的。记的是**口径**，不是某一次买了谁。

## 先从这里开始

| 入口 | 适合先看什么 |
| --- | --- |
| [元器件分类](./knowhow/README.md) | 七个大类总览 |
| [关节模组](./knowhow/01-joint-modules/README.md) | 减速机、电机、编码、驱动 |
| [G0–G5 放行门](./docs/gates.md) | 买料时每一步怎么过门 |
| [作业手册](./playbooks/README.md) | 寻源、询价、准入、首件、来料和不合格闭环 |

在线站点支持目录导航和 `Ctrl+K` 搜索。离线环境可以打开 [knowhow.html](./knowhow.html)。

## 七个大类

| 编号 | 大类 | 覆盖范围 |
| --- | --- | --- |
| 01 | [关节模组](./knowhow/01-joint-modules/README.md) | 谐波、行星、RV；无框电机；编码、驱动、制动 |
| 02 | [结构件](./knowhow/02-structure/README.md) | 机加、钣金、压铸、表面处理 |
| 03 | [电子器件](./knowhow/03-electronics/README.md) | PCB、线束、线材、接插件、电源 |
| 04 | [传感器](./knowhow/04-sensors/README.md) | 力、触觉、IMU、视觉 |
| 05 | [能源](./knowhow/05-energy/README.md) | 电芯、PACK、BMS |
| 06 | [末端](./knowhow/06-end-effector/README.md) | 灵巧手、作业接口 |
| 07 | [标准件](./knowhow/07-standard-parts/README.md) | 轴承、紧固件 |

分类是 **大类 → 小类 → 细分**。一页通常按同一骨架写：是什么、用在哪、选型冻什么、和谁配套、怎么验、有什么坑。

## 放行门

所有大类都走同一组门，细节差在对应 knowhow 里，门本身不跳。

| Gate | 目的 |
| --- | --- |
| G0 | 需求与规格冻结 |
| G1 | 申购，图纸版本锁死 |
| G2 | 询价与首件 |
| G3 | 下单 |
| G4 | 来料检验入库 |
| G5 | 关单与复盘 |

完整条件和单据状态见 [G0–G5 放行门](./docs/gates.md)。询价、准入、首件、来料和不合格闭环见 [作业手册](./playbooks/README.md)。

## 仓库结构

- [docs/](./docs/)：原则、放行门、自制 vs 外购、质量与风险
- [playbooks/](./playbooks/)：询价、准入、首件、来料、不合格怎么走
- [templates/](./templates/)：新开一页、写复盘卡片用的模板
- [site/](./site/)：Markdown 生成器、样式和站点资源
- [knowhow.html](./knowhow.html)：离线单文件站点

几条底线（样机到小批都适用）：

> 无冻结图纸/规格不下正式单 · 无 IQC 不发料 · 无 NCR 不私下让步

## 什么该写、什么别写

**适合写进来**：选型口径、冻结清单、验收项、脱敏后的坑、流程和模板。

**别写进来**：合同扫描件、密钥、`.env`、对公账号、身份证、供应商完整电话或个人微信。

询价记录、PO、供应商名录放作业仓库；这里只留「下次怎么判」。细节见 [入库纪律](./docs/security.md)。

## 修改与发布

改完 Markdown 后重新生成站点：

```bash
python -m pip install markdown
python site/build.py
```

本地预览生成结果：

```bash
python -m http.server 8765 --directory site/dist
```

推送到 `main` 后，GitHub Actions 会执行 [发布 workflow](./.github/workflows/pages.yml)，生成 `site/dist` 并部署到 [GitHub Pages](https://taicushier-0212.github.io/robot-supplychain-knowhow/)。也可以在 Actions 页面手动运行 workflow。

## 往里加一页

1. 用 [templates/component.md](./templates/component.md) 开新页
2. 挂到对应大类的 README
3. 复盘追加到页末，可用 [templates/knowhow-card.md](./templates/knowhow-card.md)
4. 不写私人联系方式
