# EVE 拓扑

`CCIE_EI_Rebuild.unl` 是50节点接线与布局，已移除嵌入配置和课程原页图片，并重新生成实验与QEMU节点UUID。导入后按部署文档配置，不包含已安装证书、设备授权、运行磁盘或已迁移的数据库。

通过 SFTP 放到 `/opt/unetlab/labs/CCIE-EI-Rebuild/CCIE_EI_Rebuild.unl`，然后在EVE执行 `/opt/unetlab/wrappers/unl_wrapper -a fixpermissions`，刷新文件管理器打开。镜像名必须与节点表一致；先确认资源再启动，不一键启动全部未知节点。

新UUID对应新设备身份。重新签发证书并登记实际chassis/serial，不复用原环境的手工身份脚本。Linux namespace 由部署脚本创建，不是UNL中的虚机。
