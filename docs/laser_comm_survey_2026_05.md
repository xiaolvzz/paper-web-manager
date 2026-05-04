# 星地激光通信与高容量外场链路调研（截至 2026-05）

## 1. 调研范围与一句话结论

### 调研范围
- 只统计**实际做过**的在轨、空地、水平链路或其他外场试验。
- **不纳入**纯仿真、仅实验室台架、尚未在轨验证的指标。
- 速率统一写为 **Gbps / Tbps**；如果文献给的是累计数据量，则单独写 **Tb / TB**。

### 核心结论
1. **真正公开可核查的星地激光通信高码率记录仍然不多。**  
   目前公开资料里，星地链路的代表性高码率结果主要是：
   - 中国空天院体系：**10 Gbps（2023） -> 60 Gbps（2025，官方披露） -> 120 Gbps（2026）**
   - NASA TBIRD：**200 Gbps** 在轨下传
2. **100 Gbps 以上的“几百 G / Tbps”结果，目前主要还是水平链路、空地链路或近空间外场验证。**  
   它们验证了高容量体制可行，但并不等价于已经实现同等级的常态化星地业务。
3. 从公开案例看，**10-100 Gbps 星地工程应用已经进入可用阶段**，而 **400 Gbps+ 到 Tbps 级** 更像是为下一代星地/空天地一体链路做体制储备。

---

## 2. 星地/近星场景实际试验汇总

> 注：本表优先列真正“卫星-地面”链路；空地/近空间链路放在末行作为对比参考。

| 国家/机构 | 时间 | 场景 | 公开速率 | 已公开关键性能 | 关键技术点 | 备注 |
|---|---:|---|---:|---|---|---|
| 中国科学院空天院 + 长光卫星 | 2023 | 吉林一号 MF02A04 星地激光通信工程应用实验 | **10 Gbps** | 按业务化流程完成双向捕获、稳定建链、自适应光学校正、误码重传/断点续传；官方表述为“数据质量良好、满足高标准业务化应用需求” | 500 mm 口径激光通信地面系统、快速捕获建链、自适应光学校正、复杂大气下高可靠传输 | 中国公开资料中较明确的 10G 星地工程应用里程碑 [R1][R2] |
| 中国科学院空天院 + AIRSAT-02 | 2025 | 业务化星地下传实验 | **60 Gbps** | 本轮检索到的可核查公开信息主要来自 2026 年官方回顾，确认其为 120 G 之前一阶段里程碑；未找到同等细粒度公开指标 | 500 mm 口径星地激光通信系统、在轨软件/业务化验证路线延续 | 建议作为“公开披露里程碑”使用，不宜过度展开 [R3] |
| 中国科学院空天院 + AIRSAT-02 | 2026 | 超百 G 星地激光通信业务化应用实验 | **120 Gbps** | **秒级捕获建链**、**建链成功率 >93%**、**最大连续通信 108 s**、**累计下行 12.656 Tb**，并成功处理高质量遥感影像 | 在卫星硬件不变前提下进行**在轨软件重构**，把激光载荷能力从 60 G 提升到 120 G；高频实时校正 + 超高速基带处理 + 非稳态信道可靠传输 | 截至 2026-05，中国公开可核查的星地速率新纪录 [R3] |
| NASA + MIT Lincoln Laboratory + JPL（TBIRD/PTD-3） | 2023 | 低轨卫星到地面激光下传 | **200 Gbps** | 单次约 **5 min** 可下传 **4.8 TB**；NASA 官方称其为当时最高空间到地面光通信速率；任务中进行了多次在轨传输 | **相干收发机**、窄波束高精度指向、**ARQ 自动重传**、低轨短过站高吞吐设计 | 目前最有代表性的公开 200G 级在轨星地下传案例 [R4][R5] |
| 中国团队（宁波海岸空地试验） | 2026 | 飞艇-地面双向 FSO 外场链路 | **103.125 Gbps（双向同时）** | **216 min** 持续稳定通信；飞艇高度 **420 m**、斜距 **1395 m**；跟踪精度 **10 μrad**；BER **1E-8 ~ 1E-11** | **DP-QPSK**、空地双向跟踪、长时稳定保持 | 不是卫星链路，但非常接近“近空间/空地回传”应用形态 [R11] |

### 对星地现状的判断
- **10-120 Gbps：** 已经能看到工程化、业务化、重复验证的迹象，尤其是中国空天院路线。
- **200 Gbps：** 已被 NASA TBIRD 在轨证明可行，但仍高度依赖精密指向、天气窗口和专用地面站能力。
- **>200 Gbps 真正星地：** 公开、可核查、已在轨的案例仍然很少；现阶段更多还是地面/空地外场先行。

---

## 3. 水平链路、海面链路和其他外场试验（重点看 100 G / 400 G / Tbps）

| 国家/机构 | 时间 | 场景 | 公开速率 | 关键性能指标 | 关键技术点 | 备注 |
|---|---:|---|---:|---|---|---|
| 澳大利亚 UWA/ICRAR | 2022 | 无人机反射器 + 地面终端，模拟 LEO 跟踪速率的相干 FSO | **100 Gbps** | 在湍流大气下实现**不中断 100 Gbps**；可在 **1.5 deg/s** 角速率下维持单模光纤耦合；折叠链路最长约 **1.4 km** | **1550 nm 相干链路**、**10 Hz 机器视觉跟踪**、**200 Hz tip/tilt 自适应稳定**、单模光纤耦合 | 这类试验对“把 100G 相干体制真正搬到星地链路”很有参考价值 [R6] |
| 葡萄牙 IT/合作方 | 2024 | 1.8 km 室外 FSO 场试 | **100 Gbps** | 在约 **10 dB** 慢衰落、**16 h** 观测内，平均接收机动态范围最多降低 **5 dB**，链路可靠性平均提升 **7%** | **LoRa 反馈信道** + 发射功率自适应预补偿 + 相干 FSO | 强调“工程可用性”，不是单纯追峰值速率 [R7] |
| 中国团队 | 2022 | 1 km 外场自由空间链路 | **150 Gbit/s** | 基于 **60 × 2.5 Gbit/s 16-PPM** 并行传输；最佳单梳齿接收灵敏度可达 **-52.62 dBm**（BER = **1e-3**, 无 FEC） | **soliton microcomb**、多波长并行、PPM 高灵敏度传输 | 属于国内较早公开的百 G 以上外场验证 [R14] |
| 葡萄牙 IT/合作方 | 2022 | 室外 FSO 场试 | **400 Gbps** | 基于 **3 h BER** 测试，传输可靠性 **>99%** | **ANN 信道估计**、慢衰落预测与补偿 | 400G 级室外链路已经不只是短时打点，而是开始考察可靠性 [R8] |
| 葡萄牙 IT/合作方 | 2024 | 1.8 km 室外 FSO 场试 | **4 Tbps+** | 通过 APC 光预放稳定接收功率，使感知 **Rytov 方差降低约 10 倍**；并通过 FEC 开销优化提升净吞吐和可靠性 | **相干 WDM**、**APC 光预放**、**FEC 优化** | 代表当前“多 Tbps 室外链路”的工程路线 [R9] |
| UCLA 等 | 2025 | 160 m 混合室内/室外自由空间链路 | **8.21 Tbps** | 在湍流条件下保持稳定，**稳定运行超过 10 h**；BER 低于 **FEC 门限 4.5e-3** | **platicon 微梳**、55 个以上光载波、WDM + PDM、**16-QAM / 20 Gbaud**、主动稳束、相位恢复 | 是很强的 Tbps 级体制验证，但距离和场景与真正星地仍有差距 [R10] |
| 中国团队（青海湖） | 2025 | 水平大气链路外场试验 | **112 Gbit/s** | 题名明确给出 **104.8 km** 水平大气链路；本轮检索未拿到同等详细公开摘要指标 | **单波长高速 FSO** | 这是很值得关注的国内 100G 级长距离外场案例，但公开可核查细节暂不如上面几项丰富 [R12] |
| 南开大学 + 长春理工 | 2025（公开报道） | 海岛间/近海面长距离激光通信 | **10 Gbps（双向）** | 海面 29 km；四路分集 + 孔径平均下，误码率可达 **1E-6** 量级以下；24 h 测试中 **94.05%** 时间 BER < **1E-6**，**99.912%** 时间 BER < **1E-3** | 多孔径分集发射、大口径接收、光斑跟踪、FPGA 实时处理、波分/多模光纤 | 对“海面/低空/强湍流”这种难信道很有代表性 [R13] |
| 中国团队 | 2025 | 29 km 近海面岛间 FSO 场试 | **40 Gbps** | 在闪烁指数 **0.21** 条件下，可获得 **BER = 1e-3**、平均接收光功率 **-19 dBm** | 商用 **2.5/10 Gbps SFP+** 光模块 + **4 波 DWDM**、高功率发射、大口径接收 | 可视为国内海面长距离链路从 10G 向更高速率迈进的代表 [R15] |

---

## 4. 速率、技术路线和关键指标怎么比较

### 4.1 从公开结果看，速率提升大致沿着这条路线走
1. **10 G 级星地工程应用**  
   核心是先把链路“建起来、稳住、能反复用”。  
   关键词：快速捕获建链、粗精跟踪、自适应光学校正、误码重传、业务流程闭环。

2. **100 G 级星地/空地/水平链路**  
   开始明显转向**相干体制**，并且更依赖高精度跟踪与单模耦合。  
   关键词：DP-QPSK/相干检测、单模光纤耦合、tip/tilt 稳束、非稳态大气补偿。

3. **400 G 到 Tbps 级外场链路**  
   单载波已经不够，通常要靠**WDM、多载波、微梳、联合 FEC 优化、功率预补偿**。  
   关键词：coherent WDM、APC、FEC overhead optimization、AI/ANN 信道估计、microcomb。

### 4.2 真正决定“能不能工程化”的指标，不只是峰值速率
- **建链成功率 / 可用时长**：如中国 120G 星地建链成功率 >93%、最大连续 108 s。
- **单次过站可传数据量**：如 TBIRD 单次 5 min 约 4.8 TB。
- **BER / FEC 门限**：很多高码率论文更看重是否长期低于 FEC 阈值，而不只是某一时刻跑到多快。
- **跟踪能力**：例如 LEO 等效场景下的 **1.5 deg/s** 跟踪速率、空地链路的 **10 μrad** 跟踪精度。
- **信道鲁棒性**：慢衰落、海面强湍流、烟尘、风致抖动等，往往比“实验室极限速率”更关键。

### 4.3 一个实用判断
- 如果目标是**近几年可落地的星地工程系统**，重点应关注 **10-120 Gbps** 这一级别的稳定性、可重复性和业务流程。
- 如果目标是**下一代超高速星地体制储备**，重点应关注 **100G 相干化、400G+ WDM 化、Tbps 微梳/多载波化**。
- **几百 G / Tbps 外场成功** 不等于 **同等级星地业务已成熟**；两者之间仍隔着大气窗口、云层覆盖、卫星平台微振动、姿轨控精度、地面站网规模等工程门槛。

---

## 5. 可直接引用的简短结论

可以直接这样概括：

> 截至 2026 年 5 月，公开可核查的实际星地激光通信试验已从 10 Gbps 工程应用推进到 120 Gbps 业务化验证，中国空天院体系形成了 10G、60G、120G 的连续爬升路线；国际上 NASA TBIRD 已完成 200 Gbps 在轨星地下传，并实现单过站 TB 级数据回传。  
> 与此同时，100 Gbps、400 Gbps 乃至 Tbps 级的高容量能力，当前更多由水平链路、空地链路和其他外场试验来验证，其代表性技术路线是相干检测、精密跟踪、自适应稳束、WDM/多载波和 FEC/功率联合优化。换句话说，**星地激光通信的工程可用速率已进入 10-100G 乃至超百 G 阶段，而几百 G 到 Tbps 仍主要处于外场体制验证向星地迁移的阶段。**

---

## 6. 参考文献与资料来源

### 星地与业务化应用
- [R1] Li, Y., Zhang, H., Huang, P., et al. **Demonstration of 10 Gbps satellite-to-ground laser communications in engineering**. *The Innovation*, 5(1), 2024. DOI: 10.1016/j.xinn.2023.100557.
- [R2] 中国科学院空天信息创新研究院. **我国星地激光高速通信业务化应用实验取得成功**. 2023-06-28.  
  http://www.aircas.cas.cn/dtxw/tpxw/202306/t20230628_6792105.html
- [R3] 中国科学院空天信息创新研究院 / 人民网转载. **我国超百G星地激光通信业务化应用实验取得成功**. 2026-01-30.  
  https://aircas.cas.cn/dtxw/cmsm/202601/t20260130_8121030.html
- [R4] NASA. **NASA, Partners Achieve Fastest Space-to-Ground Laser Comms Link**. 2023-05-11.  
  https://www.nasa.gov/centers-and-facilities/goddard/nasa-partners-achieve-fastest-space-to-ground-laser-comms-link/
- [R5] Riesing, K., Schieler, C., Bilyeu, B., et al. **Operations and Results from the 200 Gbps TBIRD Laser Communication Mission**. 37th Annual Small Satellite Conference, 2023. DOI: 10.26077/aggw-e480.  
  https://ntrs.nasa.gov/citations/20230007959

### 100 G / 400 G / Tbps 外场与水平链路
- [R6] Karpathakis, S. F. E., McCann, A. S., Dix-Matthews, B. P., et al. **Demonstration of 100 Gbps coherent free-space optical communications at LEO tracking rates**. *Scientific Reports*, 12, 18345, 2022. DOI: 10.1038/s41598-022-22027-0.
- [R7] Fernandes, M., Fernandes, G., Brandao, B., et al. **100G FSO field trial with transmitter power adaptability using a LoRa feedback channel**. *Journal of Optical Communications and Networking*, 16(3), 270-277, 2024. DOI: 10.1364/JOCN.505781.
- [R8] Fernandes, M., Nascimento, J., Monteiro, P., Guiomar, F. P. **Highly Reliable Outdoor 400G FSO Transmission Enabled by ANN Channel Estimation**. *OFC 2022*, Paper W3I.4.
- [R9] Fernandes, M., Fernandes, G., Brandao, B., et al. **4 Tbps+ FSO Field Trial Over 1.8 km With Turbulence Mitigation and FEC Optimization**. *Journal of Lightwave Technology*, 42(11), 4060-4067, 2024. DOI: 10.1109/JLT.2024.3358488.
- [R10] Wang, W., Liu, H., Wu, J., et al. **Free-space terabit/s coherent optical links via platicon frequency microcombs**. *eLight*, 5, 8, 2025. DOI: 10.1186/s43593-025-00082-0.

### 国内空地/海面/长距离水平链路
- [R11] Bai, Z., Bian, Y., Wang, X., et al. **Sustained 103.125 Gbps simultaneously bidirectional FSO communication in a 1395-m airship-to-ground link over 216 min**. *Optics Letters*, 51(8), 2096-2099, 2026. DOI: 10.1364/OL.587688.
- [R12] Bai, Z., Bian, Y., Wang, X., et al. **112 Gbit/s single-wavelength FSO communication with 104.8 km horizontal atmospheric link over Qinghai Lake**. *Optics Express*, 33(9), 19966-19979, 2025. DOI: 10.1364/OE.33.019966.
- [R13] 南开大学现代光学研究所. **光纤光子学团队完成低海拔海面29km 10Gbps高速激光通信外场试验**.  
  https://imo.nankai.edu.cn/info/1054/1555.htm
- [R14] Jia, S., et al. **150 Gbit/s 1 km high-sensitivity FSO communication outfield demonstration based on a soliton microcomb**. *Optics Express*, 2022. DOI: 10.1364/OE.465803.
- [R15] Guo, M., et al. **40 Gbps High-Speed Free-Space Inter-Island Optical Communication Over 29 Kilometers Under Turbulent Near-Sea Surface Environment**. *Journal of Lightwave Technology*, 2025. DOI: 10.1109/JLT.2024.3510783.

---

## 7. 使用这份调研时需要注意的两点

1. **不要把“星间链路”当成“星地链路”。**  
   例如国内公开的 100 Gbps 星间激光通信非常亮眼，但它不等价于 100 Gbps 星地链路已经全面成熟。

2. **不要把“峰值速率”直接当成“可业务化能力”。**  
   对真实系统来说，更重要的是：建链成功率、连续通信时长、误码率/FEC 裕量、天气适应性、单次过站回传量、地面站网络规模。
