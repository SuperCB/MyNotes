
# variant

> 一种非常神奇的C++模板类，源自C++17标准


可变值
C++17引入了一个新模板类。variant,它可以说是一个智能union,可以聚合任意类型，同时用起来又和union几乎一样了。它像只能容纳一个元素的"异质"容器，想知道当前哪种元素可以调用成员函数index()

```cpp
variant<int, float, double> v; //可以容纳3种不同的整数
v = 42;
assert(v.index() == 0);  //索引是0
v = 3.14f;  //直接赋值float
assert(v.index() == 1);  //索引是1
v = 2.718;
assert(v.index() == 2);  //索引是2
```





##  get 函数
variant不能用成员变量的形式来访问内部的值，必须用外部的模板函数get()来获取值，模板参数可以是类型名或者是索引。

如果用get()访问了不存在的值就会出错，以抛出异常的方式告知用户。

```cpp
v = 42;
assert(get<0>(v) == 42); //取索引值为0的值，即int
 
v = 2.718;
auto x = get<double>(v);  //取double得值，即索引为2
 
get<int>(v);  //当前是double,所以出错，抛出异常
```


## get_if

**注意事项**：
+ get_if的输入是指针，输出也是指针
+ get_if的尖括号中存放的是类型名称
```cpp
auto p = get_if<int>(&v);   //取int得值，不存在就返回空指针
assert(p == nullptr);
```

