#  Pytorch源码阅读



> 阅读Pytorch源代码的想法起源于我对神经网络框架的疑惑。
>
> + 前端的Python语言是如何与后端算子交互的？
> + Pytorch是怎么构建出动态图的？
> + Pytorch怎么实现后端算子？
>
> 中文网络平台上少有文章能讲清楚Pytorch的运行机制。
>
> 很多博客的博主撰写文章时并没有遵循人类认知新事物的基本规律。即先从宏观-具体-宏观-具体，渐进深入的过程
>
> 而是过于专注技术的细节，一言不合就粘贴大量代码，而对些代码究竟解决了什么问题却，这种风格的文章很容易将读者置于巨大的混乱之中，所以与其阅读这些屎一样的博客，还不如自己上手探究一下。
>
> 



不得不说，阅读Pytorch代码是一件非常痛苦的事情。主要由以下原因：

+ Pytorch使用Python前端调用C++、Cuda构建的后端算子。因为Pythont特有的C extension 机制，函数调用关系经常会出现**凭空消失**的情况。
+ C、Cpp部分的代码中，函数的声明与函数的实现相隔非常遥远，原本相关的代码放在令人意想不到的文件中，让人无从下手。
+ 多种风格的语言以及多种风格的文件组织方式并存，源代码的组织非常混乱。
+ 有大量的代码逻辑不存在于源代码中，而是在编译阶段借助Python自动生成的