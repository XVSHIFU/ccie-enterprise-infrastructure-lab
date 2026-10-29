# 设备配置

`.cli` 是按顺序输入的交互命令，包含进入配置模式、模式退出和保存。先替换 `<设备登录密码>`、`<对应实验密钥>`、`<DMVPN共享密钥>` 等参数，再在对应设备控制台输入。

这些文件不是 EVE Startup configuration 文件，不直接放进启动配置框；需要导入启动配置时，完成控制台配置并保存，再用 EVE Export CFG。证书与设备身份不在CLI中，按部署文档单独生成和登记。

| 设备 | 文件 |
| --- | --- |
| r1 | [r1.cli](ios/r1.cli) |
| r2 | [r2.cli](ios/r2.cli) |
| r3 | [r3.cli](ios/r3.cli) |
| r4 | [r4.cli](ios/r4.cli) |
| r5 | [r5.cli](ios/r5.cli) |
| r6 | [r6.cli](ios/r6.cli) |
| Internet_SP | [Internet_SP.cli](ios/Internet_SP.cli) |
| Global_SP2 | [Global_SP2.cli](ios/Global_SP2.cli) |
| sw201 | [sw201.cli](ios/sw201.cli) |
| sw202 | [sw202.cli](ios/sw202.cli) |
| sw211 | [sw211.cli](ios/sw211.cli) |
| sw212 | [sw212.cli](ios/sw212.cli) |
| r21 | [r21.cli](ios/r21.cli) |
| r22 | [r22.cli](ios/r22.cli) |
| r23 | [r23.cli](ios/r23.cli) |
| r24 | [r24.cli](ios/r24.cli) |
| sw110 | [sw110.cli](ios/sw110.cli) |
| sw101 | [sw101.cli](ios/sw101.cli) |
| sw102 | [sw102.cli](ios/sw102.cli) |
| r11 | [r11.cli](ios/r11.cli) |
| r12 | [r12.cli](ios/r12.cli) |
| r61 | [r61.cli](ios/r61.cli) |
| r62 | [r62.cli](ios/r62.cli) |
| r70 | [r70.cli](ios/r70.cli) |
| sw601 | [sw601.cli](ios/sw601.cli) |
| sw602 | [sw602.cli](ios/sw602.cli) |
| sw610 | [sw610.cli](ios/sw610.cli) |
| sw700 | [sw700.cli](ios/sw700.cli) |
| r30-IOL-IPv6 | [r30-IOL-IPv6.cli](ios/r30-IOL-IPv6.cli) |
| r30-CSR-G6 | [r30-CSR-G6.cli](ios/r30-CSR-G6.cli) |
| host12 | [host12.cli](ios/host12.cli) |
| vBond-Real | [vBond-Real.cli](sdwan/vBond-Real.cli) |
| vSmart-Real | [vSmart-Real.cli](sdwan/vSmart-Real.cli) |
| vManage-Real | [vManage-Real.cli](sdwan/vManage-Real.cli) |
| vEdge21-Real | [vEdge21-Real.cli](sdwan/vEdge21-Real.cli) |
| vEdge22-Real | [vEdge22-Real.cli](sdwan/vEdge22-Real.cli) |
| vEdge41-Real | [vEdge41-Real.cli](sdwan/vEdge41-Real.cli) |
| vEdge51-Real | [vEdge51-Real.cli](sdwan/vEdge51-Real.cli) |
| vEdge52-Real | [vEdge52-Real.cli](sdwan/vEdge52-Real.cli) |
| G5-Hybrid-GW | [G5-Hybrid-GW.cli](ios/G5-Hybrid-GW.cli) |
