# snort-ids-filter
讓腳本能順利執行的前置動作。
- 參考資料
	- [WRITING CUSTOM SNORT RULES](https://alparslanakyildiz.medium.com/writing-custom-snort-rules-e9abe10932e1)
	- [upcloud-How to install Snort on Ubuntu](https://upcloud.com/resources/tutorials/install-snort-ubuntu)
	- https://stackoverflow.com/questions/36215201/python-scapy-sniff-without-root
	- https://www.vultr.com/docs/working-with-linux-capabilities/
## Snort 安裝、客製化 Rules、配置與執行
- 看上面連結 WRITING CUSTOM SNORT RULES 這篇，照著做基本就沒啥大問題了。
## 建 snort 專用 user
- 如要使用已有的 user，跳過這步。
```
sudo groupadd snort_user
sudo useradd snort_user -r -s /bin/bash -c SNORT_IDS -g snort (如果需要)
```

## snort 配置文件與 rule 資料夾權限設定
- 若要使用已有的 user，注意 group 要修改為該 user 所屬的 group。
```
sudo chmod -R 5775 /etc/snort
sudo chmod -R 5775 /var/log/snort
sudo chown -R <user>:<group> /etc/snort
sudo chown -R <user>:<group> /var/log/snort
```
- 執行完這步已可以利用該 user 配置 snort。
- 但啟動 IDS mode 仍會 not permitted!，原因是 snort 需要開啟 socket 來做 filter，但linux kernel 下預設是 root 才能開，除非額外設定 capability。

## 修改 snort 的 Linux capability
- 修改 capability 才能讓 snort 有建立 socket 的權限。
- snort binary 若是用 apt-get install 的安裝方式，是在 /usr/sbin 下。
- scapy 也需要修改 capability，才能順利發送測試封包。
`setcap cap_net_raw=eip /usr/sbin/snort`
`setcap cap_net_raw=eip /usr/bin/pythonX.X`
