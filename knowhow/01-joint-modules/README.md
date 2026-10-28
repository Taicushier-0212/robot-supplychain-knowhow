# 关节模组

人形 BOM 里通常 **金额最高、交期最长、一致性最难手搓** 的一块。

可以买 **一体化关节**（电机 + 减速 + 编码 + 驱动，有时含抱闸/力觉），也可以按小类拆开自组。早期样机默认外购 ODM 模组、规格自控；拆开自组只在接口、成本或交期被卡死时做。

## 小类

| 小类 | 干什么 | 入口 |
|---|---|---|
| 减速机 | 把电机高速小扭变成关节低速大扭 | [reducer/](./reducer/README.md) |
| 无框力矩电机 | 电磁转矩；先分内转子 / 外转子 | [frameless-motor/](./frameless-motor/README.md) |
| 编码器 | 单编 / 双编 / 伪双编；磁编 / 电感编 / 光编 | [encoder/](./encoder/README.md) |
| 驱动器 | 电流环、总线、再生与抱闸时序 | [driver.md](./driver.md) |
| 制动器 | 断电保持、防坠落 | [brake.md](./brake.md) |
| 一体化关节 | 上述零件做成一个可采购单元 | [integrated-joint.md](./integrated-joint.md) |

减速机再往下分：[谐波](./reducer/harmonic/README.md)（[结构](./reducer/harmonic/structure.md) · [额定](./reducer/harmonic/ratings.md) · [装配](./reducer/harmonic/assembly.md)） · [行星](./reducer/planetary/README.md)（[NGW/NW](./reducer/planetary/types.md) · [齿轮](./reducer/planetary/gears.md) · [行星架](./reducer/planetary/carrier.md)） · [摆线 / RV](./reducer/cycloidal/README.md)（[结构](./reducer/cycloidal/structure.md) · [额定](./reducer/cycloidal/ratings.md) · [装配](./reducer/cycloidal/assembly.md)） · [其它路径](./reducer/other.md)（蜗轮 / 锥齿 / 带 / 直驱）。  
无框电机再往下分：[内转子](./frameless-motor/inner-rotor.md) · [外转子](./frameless-motor/outer-rotor.md)；[槽极](./frameless-motor/slot-pole.md) · [绕线](./frameless-motor/winding.md) · [磁钢](./frameless-motor/magnet.md) · [叠片 / 分瓣](./frameless-motor/core.md) · 装配 / 霍尔 / 温敏见 [frameless-motor/](./frameless-motor/README.md)。  
编码器再往下分：[单编 / 双编 / 伪双编](./encoder/count.md) · [磁编](./encoder/magnetic.md) · [电感编](./encoder/inductive.md) · [光编](./encoder/optical.md)。

## 大类必须一起冻的接口

不管买成套还是拆开买，下面这些对不上，零件各自合格也装不成轴：

- [ ] 电压平台（驱动、抱闸、编码器供电）
- [ ] 通信（CAN / EtherCAT / 厂商私有）与控制周期
- [ ] 法兰、定位销、中空孔径、出线方向
- [ ] 额定 / 峰值扭矩、持续温升、重量
- [ ] 关节侧是否要绝对式编码器、上电是否允许找零运动

供应链主责商务、交期、备份来源；规格与验收由关节 / 电控会签。

## 作业路径（成套模组）

```text
规格冻结 → 短名单（≥2）→ 样品 / 台架
  → 小批 PO → 来料通电抽检 → 寿命与一致性跟踪
```

## 大类已知坑

- 只比额定扭矩，峰值和持续温升上机才爆。
- 法兰能装，协议对不上，等于不能用。
- 独家 ODM 无备份，图纸一改全线停。
- 把减速机、电机、编码器三家拼，公差和驱动匹配全由自己扛。
