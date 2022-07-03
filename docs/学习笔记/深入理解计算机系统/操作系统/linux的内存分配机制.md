#  Linux的内存分配机制

> 见过不少文章描述Linux内部的内存分配算法，slab与buddy算法，但是这些文章却很少提及是内核中的哪个部分以及哪个函数调用了这些算法，这个问题也成了我长久以来的一个疑惑。

## malloc、kmalloc与vmalloc

首先我们需要先了解三个函数malloc、kmalloc与vmalloc。
+ kmalloc和vmalloc是分配内核的内存，malloc分配的是用户空间的内存。
+ kmalloc 保证分配的内存在物理上是连续的，vmalloc保证的是在虚拟地址空间上的连续，malloc申请的内存不一定连续（用户空间存储以空间链表的方式组织（地址递增），每一个链表块包含一个长度、一个指向下一个链表块的指针以及一个指向自身的存储空间指针。）
+ kmalloc能分配的大小有限，vmalloc与malloc能分配的空间大小相对较大。
+ 内存只有在要被DMA访问的时候才需要物理上连续。
vmalloc要不kmalloc要慢。

Linux系统在内核态与用户态有着不同的内存分配机制。



### 内核态内存分配 kmalloc 和vmalloc
Buddy伙伴算法与slab分配器是内核态中实现**kmalloc**与**vmalloc**分配机制的算法。

在内核中进行内存分配有特殊的要求，相比于用户态程序，内核程序更加注重效率，因此往往需要使用连续的物理地址来提高内存读写的速度。

Buddy算法就是一个基于连续地址空间分配内存的高效算法。



### 用户态内存分配 malloc
Buddy和slab在理论上也能用与用户进程的内存分配函数malloc中，但是实际应用中不会采用这种方式为用户进程分配内存。这是因为用户进程运行在 **虚拟地址空间**
，其物理内存空间通常情况下都是不连续的，并且其分配的内存的大小通常是非常不规则的，这就失去了应用Buddy与slab算法的意义了。

用户态的内存管理有很多不同的算法，包括
+ dlmalloc (General purpose allocator)通用分配器
+ ptmalloc2 (标准glibc)
+ tcmalloc (Google) 


用户态内存分配还必须充分考虑线程之间的同步以及并发的问题。

# Buddy 算法




