# 机器人供应链

做人形机器人时，买料这件事会反复卡在同一类问题上：这颗料到底是什么、用在哪一轴、选型必须冻住哪些字段、到货怎么验、上次踩过什么坑。

这个仓库就是用来记这些判断的。记的是**口径**，不是某一次买了谁。

双击 [knowhow.html](./knowhow.html) 就能看完整站点（用资源管理器打开，不要点 Cursor 里的链接）。Ctrl+K 可搜索。

---

## 在线站点

完整站点发布在 [GitHub Pages](https://taicushier-0212.github.io/robot-supplychain-knowhow/)。

每次推送到 `main`，GitHub Actions 会执行 [`.github/workflows/pages.yml`](./.github/workflows/pages.yml)：安装 Markdown 渲染器、运行 `site/build.py` 生成 `site/dist`，再发布到 GitHub Pages。也可以在 Actions 页面手动运行这个 workflow。

本地预览：

```bash
python -m pip install markdown
python site/build.py
python -m http.server 8765 --directory site/dist
```

然后打开 <http://localhost:8765/>。

---

## 怎么用

先看分类树，再往下钻具体料：

1. [元器件分类](./knowhow/README.md) — 七个大类总览  
2. [关节模组](./knowhow/01-joint-modules/README.md) — 减速机 / 电机 / 编码 / 驱动（最常先读）  
3. [G0–G5](./docs/gates.md) — 买的时候怎么过门  

改完 Markdown 后重新生成站点：

```bash
python -m pip install markdown
python site/build.py
```

---

## 七个大类

| | 大类 | 大致覆盖 |
|---|---|---|
| 01 | [关节模组](./knowhow/01-joint-modules/README.md) | 谐波、行星、RV；无框电机；编码、驱动、制动 |
| 02 | [结构件](./knowhow/02-structure/README.md) | 机加、钣金、压铸、表面处理 |
| 03 | [电子器件](./knowhow/03-electronics/README.md) | PCB、线束、线材、接插件、电源 |
| 04 | [传感器](./knowhow/04-sensors/README.md) | 力、触觉、IMU、视觉 |
| 05 | [能源](./knowhow/05-energy/README.md) | 电芯、PACK、BMS |
| 06 | [末端](./knowhow/06-end-effector/README.md) | 灵巧手、作业接口 |
| 07 | [标准件](./knowhow/07-standard-parts/README.md) | 轴承、紧固件 |

分类是 **大类 → 小类 → 细分**。一页通常按同一骨架写：是什么、用在哪、选型冻什么、和谁配套、怎么验、有什么坑。

---

## 仓库里还有什么

- [docs/](./docs/) — 原则、放行门、自制 vs 外购、质量与风险  
- [playbooks/](./playbooks/) — 询价、准入、首件、来料、不合格怎么走  
- [templates/](./templates/) — 新开一页、写复盘卡片用的模板  

几条底线（样机到小批都适用）：

> 无冻结图纸/规格不下正式单 · 无 IQC 不发料 · 无 NCR 不私下让步

---

## 什么该写、什么别写

**适合写进来**：选型口径、冻结清单、验收项、脱敏后的坑、流程和模板。

**别写进来**：合同扫描件、密钥、`.env`、对公账号、身份证、供应商完整电话或个人微信。

询价记录、PO、供应商名录放作业仓库；这里只留「下次怎么判」。细节见 [入库纪律](./docs/security.md)。

---

## 往里加一页

1. 用 [templates/component.md](./templates/component.md) 开新页  
2. 挂到对应大类的 README  
3. 复盘追加到页末，可用 [templates/knowhow-card.md](./templates/knowhow-card.md)  
4. 不写私人联系方式  
