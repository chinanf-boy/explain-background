# background

[![explain](http://llever.com/explain.svg)](https://github.com/chinanf-boy/Source-Explain)

版本 0.0.1

---

## 简述

入门级 python 库 由 requests 作者，创建的后台运行库

重点是，这个库只有四个文件，包括 README.rst 说明

也就是说，这是一个很好的入门例子，比如

- 上传pypi

- setup.py 的相关编写

- 后台运行 api

- rst 文档编写
...

---

## 目录

- [setup.py](#setup.py)

- [主文件，background.py](#background.py)

    - [配合用法解释-初级](#初级用法)

    - [配合用法解释-高级](#高级用法)
    
---

一般，我们看 python 可以从 setup.py 开始，和 node package.json 类似

不过，没那么清晰，在你第一次看的时候。

## setup.py

[代码1-12](./background/setup.py)

``` py
#!/usr/bin/env python 
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pip install twine

import io
import os
import sys
from shutil import rmtree

from setuptools import setup, Command
```

1. 无前缀执行 `#!/usr/bin/env python `


2. 编码规则统一 `# -*- coding: utf-8 -*-`

3. Note 这个时候引出了，`twine` 工具，这是一个上传到 pypi 的 工具，你需要安装它

- `# Note: To use the 'upload' functionality of this file, you must:`

- `#   $ pip install twine`

4. 各种导入，看下去再说。

next

[代码14-20](./background/setup.py#L14)

``` py
# Package meta-data.
NAME = 'background' # 包名字
DESCRIPTION = 'It does what it says it does.' # 包描述
URL = 'https://github.com/kennethreitz/background' # 包地址
EMAIL = 'me@kennethreitz.org' # 作者email
AUTHOR = 'Kenneth Reitz' # 作者名字
VERSION = '0.1.1' # 版本
```

next

[代码22-32](./background/setup.py#L22)

``` py
# 你的库包，需要依赖什么包
REQUIRED = [
    'futures'
    # 'requests', 'maya', 'records',
]

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!

# 本文件 setup.py 绝对路径的 目录
here = os.path.abspath(os.path.dirname(__file__)) 
```

next

[代码34-37](./background/setup.py#L34)

``` py
# Import the README and use it as the long-description.
# Note: this will only work if 'README.rst' is present in your MANIFEST.in file!
with io.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

# 导入 本文件 setup.py 目录下的 README.rst 文件，到变量 long_description 「详细描述」
```

next

[代码40-70](./background/setup.py#L40)

``` py
# 就 上传命令类，爸爸是 setuptools 的 Command
class PublishCommand(Command):
    """Support setup.py publish."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod # 静态方法，能被 类外 PublishCommand.status() 运行
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self): # 最重要，但也是基本不需要改,
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except FileNotFoundError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPi via Twine…')
        os.system('twine upload dist/*')

        sys.exit()
```

next

[代码73-110](./background/setup.py#L73)

``` py
# Where the magic happens: 终极命令
setup(
    name=NAME, # 包名字
    version=VERSION, # 包版本
    description=DESCRIPTION, # 包描述
    long_description=long_description, # pypi 库页面的详细描述，就像README.rst 不过pypi的格式基本是 rst
    author=AUTHOR, # 作者
    author_email=EMAIL, # 邮箱
    url=URL, # 库链接
    # If your package is a single module, use this instead of 'packages':
    py_modules=['background'],

    # entry_points={
    #     'console_scripts': ['mycli=mymodule:cli'],
    # },
    install_requires=REQUIRED, # 依赖库
    include_package_data=True, # 写入日期
    license='ISC', # 开源协议
    classifiers=[ 
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        # 'License :: OSI Approved :: MIT License',

        # 使用的python版本与类型
        
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    # $ setup.py publish support.
    cmdclass={
        'publish': PublishCommand,
    }, 
    
    # 上传支持 ，就是 运行上面 PublishCommand 类的命令
    # 终端使用
    # $ setup.py publish
    # Done!!!
)
```

[<div style="text-align:right">⬆️目录，目录是谁，我怎么知道</div>](#目录)

---

## background.py

``` py
python ./trybackground.py # 初级
```

or 

``` py
python trytopback.py # 高级用法
```

[background/background.py](./background/background.py)

``` py
#!/usr/bin/env python

import multiprocessing
import concurrent.futures


def default_n():
    return multiprocessing.cpu_count()

n = default_n()
pool = concurrent.futures.ThreadPoolExecutor(max_workers=n)
callbacks = []
results = []


def run(f, *args, **kwargs):

    pool._max_workers = n
    pool._adjust_thread_count()

    f = pool.submit(f, *args, **kwargs)
    results.append(f)

    return f


def task(f):
    def do_task(*args, **kwargs):
        result = run(f, *args, **kwargs)

        for cb in callbacks:
            result.add_done_callback(cb)

        return result
    return do_task


def callback(f):
    callbacks.append(f)

    def register_callback():
        f()

    return register_callback

```

好了，全在这里了

解释解释

[代码1-4]

``` py
#!/usr/bin/env python

import multiprocessing
import concurrent.futures
```

1. 运行

2. multiprocessing

3. concurrent.futures

next

## 初级用法

从初级使用方法入手，先 `@background.task` 先，那就看 task 先

- 任务列表函数

``` py
def task(f): # f 类型->函数
    def do_task(*args, **kwargs): # 
        result = run(f, *args, **kwargs) # run 函数

        for cb in callbacks: # callbacks 没使用过 == 看高级用法
            result.add_done_callback(cb)

        return result # 返回 run函数 结果， do_task() 的 返回结果
    return do_task # 初级中 work() 的函数运行

```

总得来说 ，

> => 是返回的意思

`task(f)` => `do_task` ,如果 `do_task()` => `run(f)`

那么看 `run`

- 运行函数

``` py
def run(f, *args, **kwargs): # f 一开始打进去的函数

    # n 默认 是 cpu 的 核数
    # pool = concurrent.futures.ThreadPoolExecutor(max_workers=n)
    # pool 是 线程池
    # 线程数
    pool._max_workers = n
    pool._adjust_thread_count()
    # 启动，返回结果
    f = pool.submit(f, *args, **kwargs)
    results.append(f) # 结果记录

    return f #结果
```

初级补充，有两个 全局变量

``` py
def default_n():
    return multiprocessing.cpu_count()

n = default_n() # 返回cpu 核数
# 线程池
pool = concurrent.futures.ThreadPoolExecutor(max_workers=n)
callbacks = [] # 1
results = [] # 2
```

`background` 主要是对 `concurrent.futures.ThreadPoolExecutor`进行封装

---

## 高级用法

[trytopback.py](trytopback.py)

``` py 
# Use 40 background threads.
background.n = 40 # 设置 线程数

@background.callback # 高级用法，最后那个函数 了
def work_callback(future):
    print(future)

```

看

``` py
def callback(f): # f == work_callback(future)
    callbacks.append(f) # 全局添加

    def register_callback(): # 注册函数
        f()

    return register_callback #返回
```

重新回到 task

``` py
def task(f): 
    def do_task(*args, **kwargs): 
        result = run(f, *args, **kwargs) # run 函数 返回 f 函数进入线程池运行完毕，的结果 返回

        for cb in callbacks: #
            result.add_done_callback(cb) # 添加 callback 到 f 的线程之旅-结果

            # cb 的 第一个变量 就是 线程状态
            # 高级用法中 print(future)
            # <Future at 0x10bd618d0 state=finished returned NoneType>

        return result 
    return do_task 

```

高级总结，加入 线程数 数量控制 `n` ，对线程结果的控制函数添加 `callback`

[<div style="text-align:right">⬆️目录，目录是谁，我怎么知道</div>](#目录)

---


## 其他参考

[有关 setup.py 的向导-kennethreitz](https://github.com/kennethreitz/setup.py)

[python 最佳实践-kennethreitz](https://github.com/kennethreitz/python-guide)

[最佳实践 代码示例-kennethreitz](https://github.com/kennethreitz/samplemod)

[推荐使用 `pipenv` 虚拟环境，也是由-kennethreitz](https://github.com/pypa/pipenv)