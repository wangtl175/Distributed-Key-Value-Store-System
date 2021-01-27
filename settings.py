# 配置文件
Chunk_List_File = 'chunk_list.json'  # 指定master服务器把chunk服务器的信息保存到那里
Directory_File = 'directory.json'  # 指定master服务器把映射表保存到那里
Table_File = 'table.json'  # 保存chunk服务器上的键值
Info_File = 'info.json'  # 保存服务器的信息

Persistence_Time = 5  # secs  每隔5秒就把服务器的数据持久化（输出到指定文件）
Detect_Heart_Time = 10  # secs  每隔10秒检测一下服务器的心跳（状态）
