# 工具运行位置

所有相对路径从项目根目录执行，完整源代码也收录在部署文档中。

| 工具 | 运行位置 | 用途 |
| --- | --- | --- |
| G6/restconf_ops.py | Python3管理机 | RESTCONF计划、修改、回读与native备份；密码交互输入 |
| G6/host31_restconf.py | Slax host31 Python2.7 | 从host31执行VTY修复实验 |
| G6/ribdump.py | IOS-XE Guest Shell | 按VRF与地址族动态查询路由 |
| G6/erp_lab.py | EVE对应namespace | HTTPS只读订单服务 |
| G6/business_probe.py | EVE对应namespace | 认证与证书校验后的业务请求 |
| deployment/setup_business.py | EVE root | 根据UNL或显式桥名准备namespace和服务；会改动本机网络与业务文件 |
| deployment/migrate_erp.py | EVE root | 复制订单、核对内容并切换DC入口后台 |
| deployment/diagnose_business.py | Python3管理机 | 只读采集网关与两个业务入口；实际端口通过参数指定 |
| g7_console.py | 被诊断脚本导入 | Telnet控制台协议处理；不单独使用其旧环境示例入口 |

故障关断步骤以部署文档中的手动操作为准，未打包带原环境端口与密码的批量故障脚本。原CA与设备身份恢复脚本也不打包；新环境记录自己的身份。
