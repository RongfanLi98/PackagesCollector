# PackageSeeker
## 功能
包检查器  
本地版的爬虫，针对python包进行了优化
检查指定路径下的全部ipynb和py文件，自动生成requirements.txt(排除python标准库)

模块功能
1. seeker  
    * 找到指定的文件名，用正则表达式，返回路径列表
    * 用re在路径列表中找出目标内容，返回json格式
        ```json
        {
        "dirpath_one": ["math", "os"],
        "dirpath_tow": ["math", "os"]
        }
        ```
    * 无正则表达式则默认搜索python文件，查询中无正则则默认搜索python package

2. writer，按照给定的内容，比如json，写入requirement，并提供对应的删除方案

3. verifier
    * 到conda和pip上查询包是否存在，并且确认目前最新版本到requirements。如果有所冲突，保留原文件，判断后填入requirements_conda和requirements_pip，若都不存在则写一个失败文档
    * 查询本地包的版本和最新包的差距
    * 比较本地两个requirement的不同，见[pip-pop](https://github.com/heroku-python/pip-pop)的功能


## API
