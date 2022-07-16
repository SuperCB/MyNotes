# add_subdirectory

## add_subdirectory解决了什么问题？ 
add_subdirectory可以在原有的cmake项目的基础上加入子项目
一个大型的C++项目通常有很多个子项目组成.
子项目可以是自己写的代码，这样可以使代码的结构更加清晰。
子项目也可以是别人的代码，这样可以为自己的项目增添更多的功能。

子项目与父项目之间通过add_subdirectory来建立联系。
add_subdirectory可以在原有的cmake项目中加入子项目，从而使用子项目中代码。

## 使用流程
在父项目中的CMakeLists.txt中使用add_subdirectory(A)添加子项目A之后，父项目就可以使用子项目A中所生成的库、目标文件。


**注意事项**

+ 子项目通常是一个包含CMakeLists.txt的目录文件，没有CMakeLists.txt文件的目录不能被CMake视为是一个子项目。

+ 使用add_subdirectory之后，父项目就能够使用子项目中定义的变量，这些变量必须在子项目的CMakeLists.txt文件中有明确的声明。

[一个非常好的博客](https://www.bookstack.cn/read/CMake-Cookbook/content-chapter7-7.7-chinese.md)


对于一个这样的项目结构。

```sh
.
├── CMakeLists.txt
├── external
│    ├── CMakeLists.txt
│    ├── conversion.cpp
│    ├── conversion.hpp
│    └── README.md
├── src
│    ├── CMakeLists.txt
│    ├── evolution
│    │    ├── CMakeLists.txt
│    │    ├── evolution.cpp
│    │    └── evolution.hpp
│    ├── initial
│    │    ├── CMakeLists.txt
│    │    ├── initial.cpp
│    │    └── initial.hpp
│    ├── io
│    │    ├── CMakeLists.txt
│    │    ├── io.cpp
│    │    └── io.hpp
│    ├── main.cpp
│    └── parser
│        ├── CMakeLists.txt
│        ├── parser.cpp
│        └── parser.hpp
└── tests
    ├── catch.hpp
    ├── CMakeLists.txt
    └── test.cpp
```



src目录下的CMakeLists.txt内容如下：

```cmake
add_executable(automata main.cpp)
add_subdirectory(evolution)
add_subdirectory(initial)
add_subdirectory(io)
add_subdirectory(parser)
target_link_libraries(automata
  PRIVATE
    conversion
    evolution
    initial
    io
    parser
  )
```

以add_subdirectory(evolution)为例，当这条命令执行完之后，src中Cmake就能够使用evolution子项目中定义的库evolution.

子项目evolution中的CMakeLists.txt的内容如下。

```cmake
add_library(evolution "")
target_sources(evolution
  PRIVATE
      evolution.cpp
  PUBLIC
      ${CMAKE_CURRENT_LIST_DIR}/evolution.hpp
  )
target_include_directories(evolution
  PUBLIC
      ${CMAKE_CURRENT_LIST_DIR}
  )
```



**特别注意**：

+ 这个地方非常凑巧的是子项目的名称evolution与子项目所构建的库的名称evolution相同,这样会产生不必要的误会。

  在src目录中的CMakeLists.txt中，

  add_subdirectory(evolution)中的evolution是子项目的名称。

  target_link_libraries中的evolution是子项目中构建的库的名称。

  请特别注意这二者之间的区别。





## 有趣的事



CMake可以使用Graphviz图形可视化软件([http://www.graphviz.org](http://www.graphviz.org/) )生成项目的依赖关系图:

> 万物皆可Graphviz,我可太喜欢了

```shell
cd build
cmake --graphviz=example.dot ..
dot -T png example.dot -o example.png
```



生成的图表将显示不同目录下的目标之间的依赖关系:

![7.7 add_subdirectory的限定范围 - 图2](https://static.sitestack.cn/projects/CMake-Cookbook/images/chapter7/7-7-2.png)







