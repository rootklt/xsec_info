## 零组安全资料库爬虫

---

​    这几天看了一些零组安全的资料，觉得很不错，资料也比较全面，为了方便离线时能查阅，写了一个简单的爬虫把资料爬下来。

### 依赖

---

1. requests
2. bs4
3. lxml

### 例子

```bash
python3 0sec_info.py
```

![avatar](/Users/rootk1t/Softwares/01-tools/0sec1/运行截图.png)

+ 页面效果

![avatar](/Users/rootk1t/Softwares/01-tools/0sec1/页面截图.png)

### TODO

---

目前只是把整个html页面保存下来，若0组资料库有更新，则需要重新爬一次；应该做一个模板，爬到的文章部分在浏览时动态加载导航模板，这样就算更新了，只要爬导航部分和新增文章就可以，。







