# Funny JSON Explorer

Funny JSON Explorer (FJE)，是一个JSON文件可视化的命令行界面小工具

## 安装

本项目基于 python 编写，最低支持版本为 3.8，不依赖任何外部库，在项目根目录下运行以下命令安装：

```shell
pip install -e .
```

卸载方式如下：

```shell
pip uninstall fje
```

## 使用

在使用 pip 安装 fje 后，你可以直接在命令行中使用 `fje` 命令打开 Funny JSON Explorer：

```shell
fje -f <json_file_path>
```

完整的命令说明如下：

```
usage: fje [-h] -f FILE [-s STYLE] [-i ICON_FAMILY] [-c CONFIG] [-v]

Funny JSON Explorer

options:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  JSON file path
  -s STYLE, --style STYLE
                        style
  -i ICON_FAMILY, --icon-family ICON_FAMILY
                        icon family
  -c CONFIG, --config CONFIG
                        icon family file
  -v, --verbose         print availavle icon families and styles
```

自定义的 icon family 文件为 JSON 格式，示例如下；

```json
{
    "marker": {
        "composite": "+",
        "leaf": "*"
    },
    "emoji": {
        "composite": "📦",
        "leaf": "🧸"
    }
}
```

## 开发

项目通过 setuptools 进行打包，源码位于 fje 目录下。

如果需要添加样式，只需实现 `style.style` 的抽象产品类和的抽象工厂类，然后在 `style.__init__.py` 中注册即可。

详细请参考 docs 目录的设计文档。

## 测试

时间有限没有做单元测试，不过 test 目录提供了集成测试，可以在安装后自己看一下效果：

```shell
test> fje -f test.json -c config.json -s rect -i marker
```