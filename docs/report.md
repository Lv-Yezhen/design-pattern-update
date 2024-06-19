采用了迭代器+访问者模式重写逻辑如下

改写 node.py,将原来的 traverse 方法去掉,转而定义了访问者接口(JSONVistor)以及各个节点中定义 accept 接口,然后依次实现了不同的访问者.

比如在具体 style 工厂中定义了一个渲染访问者(rendervistor)用迭代器实现具体的渲染
