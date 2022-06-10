[TOC]

#  塔杨算法

##   有向图强连通分量

> 如果一个有向图G，对于其中任意两个顶点v,u，都存在从v到u以及从u到v的有向路径，则称G为强连通图。而在一个不是强连通图的有向图G中，若其中两个顶点u、v在两个方向上都存在有向路径，则称u和v强连通。



###   受欢迎的牛

> 每一头牛的愿望就是变成一头最受欢迎的牛。
>
> 现在有 N 头牛，编号从 1 到 N，给你 M 对整数 (A,B)，表示牛 A 认为牛 B 受欢迎。
>
> 这种关系是具有传递性的，如果 A 认为 B 受欢迎，B 认为 C 受欢迎，那么牛 A 也认为牛 C 受欢迎。
>
> 你的任务是求出有多少头牛被除自己之外的所有牛认为是受欢迎的。



```c++
#include <cstdio>
#include <cstring>
#include <iostream>
#include <algorithm>

using namespace std;

const int N = 10010, M = 50010;

int n, m;
int h[N], e[M], ne[M], idx;
int dfn[N], low[N], timestamp;
int stk[N], top;
bool in_stk[N];
int id[N], scc_cnt, Size[N];
int dout[N];

void add(int a, int b)
{
    e[idx] = b, ne[idx] = h[a], h[a] = idx ++ ;
}

void tarjan(int u)
{
    dfn[u] = low[u] = ++ timestamp;
    stk[ ++ top] = u, in_stk[u] = true;
    for (int i = h[u]; i != -1; i = ne[i])
    {
        int j = e[i];
        if (!dfn[j])
        {
            tarjan(j);
            low[u] = min(low[u], low[j]);
        }
        else if (in_stk[j]) low[u] = min(low[u], dfn[j]);
    }

    if (dfn[u] == low[u])
    {
        ++ scc_cnt;
        int y;
        do {
            y = stk[top -- ];
            in_stk[y] = false;
            id[y] = scc_cnt;
            Size[scc_cnt] ++ ;
        } while (y != u);
    }
}

int main()
{
    scanf("%d%d", &n, &m);
    memset(h, -1, sizeof h);
    while (m -- )
    {
        int a, b;
        scanf("%d%d", &a, &b);
        add(a, b);
    }

    for (int i = 1; i <= n; i ++ )
        if (!dfn[i])
            tarjan(i);

    for (int i = 1; i <= n; i ++ )
        for (int j = h[i]; ~j; j = ne[j])
        {
            int k = e[j];
            int a = id[i], b = id[k];
            if (a != b) dout[a] ++ ;
        }

    int zeros = 0, sum = 0;
    for (int i = 1; i <= scc_cnt; i ++ )
        if (!dout[i])
        {
            zeros ++ ;
            sum += Size[i];
            if (zeros > 1)
            {
                sum = 0;
                break;
            }
        }

    printf("%d\n", sum);

    return 0;
}
```







##  边双连通分量

> *核心概念： 没有割边
> 割边只会把图分成两部分，对图中的点没有影响*

###   冗余路径

一边求割边，一边求边双联通分量。

```c++
#include <cstring>
#include <iostream>
#include <algorithm>

using namespace std;

const int N = 5010, M = 20010;

int n, m;
int h[N], e[M], ne[M], idx;
int dfn[N], low[N], timestamp;
int stk[N], top;
int id[N], dcc_cnt;
bool is_bridge[M];
int d[N];

void add(int a, int b)
{
    e[idx] = b, ne[idx] = h[a], h[a] = idx ++ ;
}

void tarjan(int u, int from)
{
    dfn[u] = low[u] = ++ timestamp;
    stk[ ++ top] = u;

    for (int i = h[u]; ~i; i = ne[i])
    {
        int j = e[i];
        if (!dfn[j])
        {
            tarjan(j, i);
            low[u] = min(low[u], low[j]);
            if (dfn[u] < low[j])
                is_bridge[i] = is_bridge[i ^ 1] = true;
        }
        else if (i != (from ^ 1))
            low[u] = min(low[u], dfn[j]);
    }

    if (dfn[u] == low[u])
    {
        ++ dcc_cnt;
        int y;
        do {
            y = stk[top -- ];
            id[y] = dcc_cnt;
        } while (y != u);
    }
}

int main()
{
    cin >> n >> m;
    memset(h, -1, sizeof h);
    while (m -- )
    {
        int a, b;
        cin >> a >> b;
        add(a, b), add(b, a);
    }

    tarjan(1, -1);

    for (int i = 0; i < idx; i ++ )
        if (is_bridge[i])
            d[id[e[i]]] ++ ;

    int cnt = 0;
    for (int i = 1; i <= dcc_cnt; i ++ )
        if (d[i] == 1)
            cnt ++ ;

    printf("%d\n", (cnt + 1) / 2);

    return 0;
}
```





##  点双连通分量

求割点

##  电力

给定一个由 nn 个点 mm 条边构成的**无向**图，请你求出该图删除一个点之后，连通块最多有多少。

```c++
#include <cstdio>
#include <cstring>
#include <iostream>
#include <algorithm>

using namespace std;

const int N = 10010, M = 30010;
int n, m;
int h[N], e[M], ne[M], idx;
int dfn[N], low[N], timestamp;
int root, ans;

void add(int a, int b)
{
    e[idx] = b;
    ne[idx] = h[a];
    h[a] = idx ++ ;
}

void tarjan(int u)
{
    dfn[u] = low[u] = ++ timestamp;
    int cnt = 0;//当前块内 已经可以分出来的子树的个数
    for (int i = h[u]; ~i; i = ne[i])
    {
        int j = e[i];
        if (!dfn[j])//没有遍历过j
        {
            tarjan(j);
            low[u] = min(low[u], low[j]);//用j更新u
            if (low[j] >= dfn[u]) cnt ++ ;//j为割点 则多一个连通块
        }
        else low[u] = min(low[u], dfn[j]);
    }
    if (u != root) cnt ++ ;
    //如果不是根节点
    /*
             /
            x    删掉x后 除子节点yi外
           / \           还要要加上父节点部分+1
          o   o

    */
    ans = max(ans, cnt);
}
int main()
{
    while (cin >> n >> m, n || m)
    {
        memset(dfn, 0, sizeof dfn);
        memset(h, -1, sizeof h);
        idx = timestamp = 0;

        while (m -- )
        {
            int a, b;
            cin >> a >> b;
            add(a, b), add(b, a);
        }

        ans = 0;//把每个点删完后 最多能分为几块
        int cnt = 0;//连通块数量
        for (root = 0; root < n; root ++ )
            if (!dfn[root])//如果点root没搜索过 连通块数+1
            {
                cnt ++ ;
                tarjan(root);
            }

        cout << ans + cnt - 1 << endl;
    }

    return 0;
}

```



 





#  最短路

##  SPFA算法

```c++
#include <iostream>
#include <cstring>
#include <algorithm>

using namespace std;
const int N = 2600,M=13000;


int h[N], e[M], ne[M],w[M], idx;

int d[N],st[N],q[N];
void add(int a, int b,int c)  // 添加一条边a->b
{
    e[idx] = b,w[idx]=c, ne[idx] = h[a], h[a] = idx ++ ;
    e[idx]=a,w[idx]=c,   ne[idx]=h[b],h[b]=idx++;
    
}
int S,T;
void spfa()
{
    int hh=0,tt=0;//循环队列算法求最短路，最开始的时候队首和队尾在同样的位置上
    memset(d,0x3f,sizeof d);
    q[tt++]=S,d[S]=0,st[S]=true;
    while(hh!=tt)
    {
        int t=q[hh++];
        
        if(hh==N)
        hh=0;
        st[t]=false;
        for(int i=h[t];~i;i=ne[i])
        {
            int j=e[i];
            
            if(d[j]>d[t]+w[i])
            {
                d[j]=d[t]+w[i];
          //      cout<<d[j]<<endl;
                if(!st[j])
                {
                    q[tt++]=j;
                    if(tt==N)
                    tt=0;
                    st[j]=true;
                }
            }
        }
    }

}



int n,m;
int main()
{
    cin>>n>>m>>S>>T;
    memset(h,-1,sizeof h);
    for(int i=0;i<m;i++)
    {
        
        int a,b,c;
        cin>>a>>b>>c;
        add(a,b,c);
    }
    spfa();
    cout<<d[T]<<endl;
    return 0;
}

```









#  二分图

##  二分图相关知识点

+   最大匹配数 = 最小点覆盖 = 总点数 - 最大独立集 = 总点数 - 最小路径覆盖



**二分图的最小顶点覆盖**

定义：假如选了一个点就相当于覆盖了以它为端点的所有边。最小顶点覆盖就是选择最少的点来覆盖所有的边。

方法：最小顶点覆盖等于二分图的最大匹配。

**二分图的最大独立集**

定义：选出一些顶点使得这些顶点两两不相邻*相互之间不连边的意思*，则这些点构成的集合称为独立集。找出一个包含顶点数最多的独立集称为最大独立集。

方法：最大独立集=所有顶点数-最小顶点覆盖

![img](https://images2015.cnblogs.com/blog/361759/201611/361759-20161106185133846-1899337148.png)

















#  最大流算法

## $Dinic$算法模板

```c++
#include <iostream>
#include <cstring>
#include <algorithm>

using namespace std;

const int N = 10010, M = 200010, INF = 1e8;

int n, m, S, T;
int h[N], e[M], f[M], ne[M], idx;
int q[N], d[N], cur[N];

void add(int a, int b, int c)
{
    e[idx] = b, f[idx] = c, ne[idx] = h[a], h[a] = idx ++ ;
    e[idx] = a, f[idx] = 0, ne[idx] = h[b], h[b] = idx ++ ;
}

bool bfs()
{
    int hh = 0, tt = 0;
    memset(d, -1, sizeof d);
    q[0] = S, d[S] = 0, cur[S] = h[S];
    while (hh <= tt)
    {
        int t = q[hh ++ ];
        for (int i = h[t]; ~i; i = ne[i])
        {
            int ver = e[i];
            if (d[ver] == -1 && f[i])
            {
                d[ver] = d[t] + 1;
                cur[ver] = h[ver];
                if (ver == T)  return true;
                q[ ++ tt] = ver;
            }
        }
    }
    return false;
}

int find(int u, int limit)
{
    if (u == T) return limit;
    int flow = 0;
    for (int i = cur[u]; ~i && flow < limit; i = ne[i])
    {
        cur[u] = i;  // 当前弧优化
        int ver = e[i];
        if (d[ver] == d[u] + 1 && f[i])
        {
            int t = find(ver, min(f[i], limit - flow));
            if (!t) d[ver] = -1;
            f[i] -= t, f[i ^ 1] += t, flow += t;
        }
    }
    return flow;
}

int dinic()
{
    int r = 0, flow;
    while (bfs()) while (flow = find(S, INF)) r += flow;
    return r;
}

int main()
{
    scanf("%d%d%d%d", &n, &m, &S, &T);
    memset(h, -1, sizeof h);
    while (m -- )
    {
        int a, b, c;
        scanf("%d%d%d", &a, &b, &c);
        add(a, b, c);
    }

    printf("%d\n", dinic());

    return 0;
}
```

### 无源汇上下界可行流

```c++
#include <iostream>
#include <cstring>
#include <algorithm>

using namespace std;

const int N = 210, M = (10200 + N) * 2, INF = 1e8;

int n, m, S, T;
int h[N], e[M], f[M], l[M], ne[M], idx;
int q[N], d[N], cur[N], A[N];

void add(int a, int b, int c, int d)
{
    e[idx] = b, f[idx] = d - c, l[idx] = c, ne[idx] = h[a], h[a] = idx ++ ;
    e[idx] = a, f[idx] = 0, ne[idx] = h[b], h[b] = idx ++ ;
}

bool bfs()
{
    int hh = 0, tt = 0;
    memset(d, -1, sizeof d);
    q[0] = S, d[S] = 0, cur[S] = h[S];
    while (hh <= tt)
    {
        int t = q[hh ++ ];
        for (int i = h[t]; ~i; i = ne[i])
        {
            int ver = e[i];
            if (d[ver] == -1 && f[i])
            {
                d[ver] = d[t] + 1;
                cur[ver] = h[ver];
                if (ver == T) return true;
                q[ ++ tt] = ver;
            }
        }
    }
    return false;
}

int find(int u, int limit)
{
    if (u == T) return limit;
    int flow = 0;
    for (int i = cur[u]; ~i && flow < limit; i = ne[i])
    {
        cur[u] = i;
        int ver = e[i];
        if (d[ver] == d[u] + 1 && f[i])
        {
            int t = find(ver, min(f[i], limit - flow));
            if (!t) d[ver] = -1;
            f[i] -= t, f[i ^ 1] += t, flow += t;
        }
    }
    return flow;
}

int dinic()
{
    int r = 0, flow;
    while (bfs()) while (flow = find(S, INF)) r += flow;
    return r;
}

int main()
{
    scanf("%d%d", &n, &m);
    S = 0, T = n + 1;
    memset(h, -1, sizeof h);
    for (int i = 0; i < m; i ++ )
    {
        int a, b, c, d;
        scanf("%d%d%d%d", &a, &b, &c, &d);
        add(a, b, c, d);
        A[a] -= c, A[b] += c;
    }

    int tot = 0;
    for (int i = 1; i <= n; i ++ )
        if (A[i] > 0) add(S, i, 0, A[i]), tot += A[i];
        else if (A[i] < 0) add(i, T, 0, -A[i]);

    if (dinic() != tot) puts("NO");
    else
    {
        puts("YES");
        for (int i = 0; i < m * 2; i += 2)
            printf("%d\n", f[i ^ 1] + l[i]);
    }
    return 0;
}
```



###  有源汇上下界最大流

```c++
#include <iostream>
#include <cstring>
#include <algorithm>

using namespace std;

const int N = 210, M = (N + 10000) * 2, INF = 1e8;

int n, m, S, T;
int h[N], e[M], f[M], ne[M], idx;
int q[N], d[N], cur[N], A[N];

void add(int a, int b, int c)
{
    e[idx] = b, f[idx] = c, ne[idx] = h[a], h[a] = idx ++ ;
    e[idx] = a, f[idx] = 0, ne[idx] = h[b], h[b] = idx ++ ;
}

bool bfs()
{
    int hh = 0, tt = 0;
    memset(d, -1, sizeof d);
    q[0] = S, d[S] = 0, cur[S] = h[S];
    while (hh <= tt)
    {
        int t = q[hh ++ ];
        for (int i = h[t]; ~i; i = ne[i])
        {
            int ver = e[i];
            if (d[ver] == -1 && f[i])
            {
                d[ver] = d[t] + 1;
                cur[ver] = h[ver];
                if (ver == T) return true;
                q[ ++ tt] = ver;
            }
        }
    }
    return false;
}

int find(int u, int limit)
{
    if (u == T) return limit;
    int flow = 0;
    for (int i = cur[u]; ~i && flow < limit; i = ne[i])
    {
        cur[u] = i;
        int ver = e[i];
        if (d[ver] == d[u] + 1 && f[i])
        {
            int t = find(ver, min(f[i], limit - flow));
            if (!t) d[ver] = -1;
            f[i] -= t, f[i ^ 1] += t, flow += t;
        }
    }
    return flow;
}

int dinic()
{
    int r = 0, flow;
    while (bfs()) while (flow = find(S, INF)) r += flow;
    return r;
}

int main()
{
    int s, t;
    scanf("%d%d%d%d", &n, &m, &s, &t);
    S = 0, T = n + 1;
    memset(h, -1, sizeof h);
    while (m -- )
    {
        int a, b, c, d;
        scanf("%d%d%d%d", &a, &b, &c, &d);
        add(a, b, d - c);
        A[a] -= c, A[b] += c;
    }

    int tot = 0;
    for (int i = 1; i <= n; i ++ )
        if (A[i] > 0) add(S, i, A[i]), tot += A[i];
        else if (A[i] < 0) add(i, T, -A[i]);

    add(t, s, INF);
    if (dinic() < tot) puts("No Solution");
    else
    {
        int res = f[idx - 1];
        S = s, T = t;
        f[idx - 1] = f[idx - 2] = 0;
        printf("%d\n", res + dinic());
    }

    return 0;
}

```



###  有源汇上下界最小流













#  最小割的应用

## 最大权闭合子图

+ [思想最精辟的一篇博客](https://blog.csdn.net/winter2121/article/details/80076806)



**重点**

+ 为什么会与最小割模型有关？ **最小割割出来的图正好是最大权闭合子图**

```c++
#include <iostream>
#include <cstring>
#include <algorithm>

using namespace std;

const int N = 55010, M = (50000 * 3 + 5000) * 2 + 10, INF = 1e8;

int n, m, S, T;
int h[N], e[M], f[M], ne[M], idx;
int q[N], d[N], cur[N];

void add(int a, int b, int c)
{
    e[idx] = b, f[idx] = c, ne[idx] = h[a], h[a] = idx ++ ;
    e[idx] = a, f[idx] = 0, ne[idx] = h[b], h[b] = idx ++ ;
}

bool bfs()
{
    int hh = 0, tt = 0;
    memset(d, -1, sizeof d);
    q[0] = S, d[S] = 0, cur[S] = h[S];
    while (hh <= tt)
    {
        int t = q[hh ++ ];
        for (int i = h[t]; ~i; i = ne[i])
        {
            int ver = e[i];
            if (d[ver] == -1 && f[i])
            {
                d[ver] = d[t] + 1;
                cur[ver] = h[ver];
                if (ver == T) return true;
                q[ ++ tt] = ver;
            }
        }
    }
    return false;
}

int find(int u, int limit)
{
    if (u == T) return limit;
    int flow = 0;
    for (int i = cur[u]; ~i && flow < limit; i = ne[i])
    {
        cur[u] = i;
        int ver = e[i];
        if (d[ver] == d[u] + 1 && f[i])
        {
            int t = find(ver, min(f[i], limit - flow));
            if (!t) d[ver] = -1;
            f[i] -= t, f[i ^ 1] += t, flow += t;
        }
    }
    return flow;
}

int dinic()
{
    int r = 0, flow;
    while (bfs()) while (flow = find(S, INF)) r += flow;
    return r;
}

int main()
{
    scanf("%d%d", &n, &m);
    S = 0, T = n + m + 1;
    memset(h, -1, sizeof h);
    for (int i = 1; i <= n; i ++ )
    {
        int p;
        scanf("%d", &p);
        add(m + i, T, p);
    }

    int tot = 0;
    for (int i = 1; i <= m; i ++ )
    {
        int a, b, c;
        scanf("%d%d%d", &a, &b, &c);
        add(S, i, c);
        add(i, m + a, INF);
        add(i, m + b, INF);
        tot += c;
    }

    printf("%d\n", tot - dinic());

    return 0;
}

```















##  最小点权覆盖集和最大点权独立集

### 最小点权覆盖

给出一个二分图，每个点有一个非负点权

要求选出一些点构成一个覆盖，问点权最小是多少

 

#### 建模：

S到左部点，容量为点权

右部点到T，容量为点权

左部点到右部点的边，容量inf

求最小割即可。

 

#### 证明：

> 每一个割集，对应选择一些点，对应一个覆盖。
>
> 每个覆盖有不同的代价，选择最小的就是最小点覆盖
>
> 每个割集有不同的代价，选择最小的就是最小割
>
> 由于割集和覆盖一一对应
>
> 所以，这个新图的最小割，就对应原图的最小点覆盖。

#####  代码实现

```c++
#include<cstdio>
#include <iostream>
#include <cstring>
#include <algorithm>

using namespace std;


const int N = 210,M=12000,INF=1e9;

int h[N],ne[M],e[M],f[M],idx;
int q[N],d[N],cur[N];
int S,T;
void add(int a,int b,int c)
{
    e[idx]=b,f[idx]=c,ne[idx]=h[a],h[a]=idx++;
    e[idx]=a,f[idx]=0,ne[idx]=h[b],h[b]=idx++;
}
bool bfs()
{
    int hh=0,tt=0;
    memset(d,-1,sizeof(d));
    q[0]=S,d[S]=0,cur[S]=h[S];

    while(hh<=tt)
    {
        int t=q[hh++];

        for(int i=h[t];~i;i=ne[i])
        {
            int ver=e[i];
            if(f[i]&&d[ver]==-1)
            {
                d[ver]=d[t]+1;
                cur[ver]=h[ver];
                if(ver==T)
                return true;
                q[++tt]=ver;


            }


        }






    }


    return false;
}
int find(int u,int limit)
{
    if(u==T)return limit;

    int flow=0;
    for(int i=cur[u];~i&&flow<limit;i=ne[i])
    {
        cur[u]=i;
        int ver=e[i];

        if(d[ver]==d[u]+1&&f[i])
        {
            int t=find(ver,min(f[i],limit-flow));
            if(!t)d[ver]=-1;
            f[i]-=t,f[i^1]+=t,flow+=t;

        }
    }

    return flow;

}


int dinic()
{
    int r=0,flow;
    while(bfs())
    while(flow=find(S,INF))
    r+=flow;
    return r;

}


int n,m;
int st[N];

void dfs(int u)
{
    st[u]=true;
    for(int i=h[u];~i;i=ne[i])
    {
        int ver=e[i];
        if(!st[ver]&&f[i])
        dfs(ver);
        
        
    }
    
    
}
int main(){
    
    scanf("%d%d", &n, &m);
    memset(h, -1, sizeof h);
    S=0,T=2*n+1;
    for (int i = 1; i <=n; i ++ )
    {
        int t;
        scanf("%d",&t);
        add(S, i,t);
        
        
    }
    for (int i = 1; i <=n; i ++ )
    {
        
        int t;
        scanf("%d",&t);
        add(i+n, T,t);
    }
    
    for (int i = 0; i < m; i ++ )
    {
        int a,b;
        scanf("%d%d", &a, &b);
        
        add(b, a+n,INF);
        
        
    }
    
    printf("%d\n",dinic());
    
    int cnt=0;
    
    dfs(S);
    
    for(int i=0;i<idx;i+=2)
    {
        int a=e[i^1],b=e[i];
        if(st[a]&&!st[b])
        cnt++;
        
        
    }
    printf("%d\n",cnt);
    for(int i=0;i<idx;i+=2)
    {
        int a=e[i^1],b=e[i];
        if(st[a]&&!st[b])
      if(a==S)
      printf("%d +\n",b);
        
        
    }
    for(int i=0;i<idx;i+=2)
    {
        int a=e[i^1],b=e[i];
        if(st[a]&&!st[b])
      if(b==T)
      printf("%d -\n",a-n);
        
        
    }
    
    return 0;
}
```









### 最大点权独立集

给出一个二分图，每个点有一个非负点权

要求选出一些点构成一个独立集，问点权最大是多少

 

建模：

等于：总权值-最小点权覆盖

 

证明：

扔掉覆盖的点的剩余点一定是一个独立集

而且，根据覆盖=点数-独立集

对于一个固定的点覆盖，独立集已经不能更大。

所以，一个固定的点覆盖下，最大独立集是确定的。两者呈现一一对应的关系。

而总权值不变，所以选择扔掉的覆盖集总权值最小即可。

所以，最大点权独立集=总权值-最小点权覆盖





#  01分数规划

##  [观光奶牛](https://www.acwing.com/problem/content/description/363/)

###  原题

给定一张 $L$个点、$P$条边的有向图，每个点都有一个权值 $f[i]$，每条边都有一个权值 $t[i]$。

求图中的一个环，使**环上各点的权值之和除以环上各边的权值之和**最大。

输出这个最大值。

**注意**：数据保证至少存在一个环。



###  题解

01分数规划

设答案为 ansans。

二分答案，设当前二分值为 midmid。

设一个环 $S$ 的边权为 $t1,t2,t3…$，点权为 $f1,f2,f3…$

+ 若 mid<=ansmid<=ans，即存在一个环SS使得 $mid\le \frac{\sum f_i}{\sum t_i}$，变换一下：$\sum(mid∗t_i−f_i)<=0$

+ 否则，则 mid>ans

每次 check 的时候，一条 u 指向 v，边权为 w 的边权变为：w∗mid−fuw∗mid−fu。我们只需检查这个图是否存在负环即可。

时间复杂度
最坏情况存在长度为 LL 的环， ∑ti=L,∑fi=1000L∑ti=L,∑fi=1000L。故答案最大可能是 1000。

$Log_210^7≈24$
$O(24∗LP)$。判负环的时间一般情况下低于 $O(LP)$。





#  最近公共祖先

##  模板

```c++

#include <cstdio>
#include <cstring>
#include <iostream>
#include <algorithm>

using namespace std;

const int N = 40010, M = N * 2;

int n, m;
int h[N], e[M], ne[M], idx;
int depth[N], fa[N][16];
int q[N];

void add(int a, int b)
{
    e[idx] = b, ne[idx] = h[a], h[a] = idx ++ ;
}

void bfs(int root)
{
    memset(depth, 0x3f, sizeof depth);
    depth[0] = 0, depth[root] = 1;
    int hh = 0, tt = 0;
    q[0] = root;
    while (hh <= tt)
    {
        int t = q[hh ++ ];
        for (int i = h[t]; ~i; i = ne[i])
        {
            int j = e[i];
            if (depth[j] > depth[t] + 1)
            {
                depth[j] = depth[t] + 1;
                q[ ++ tt] = j;
                fa[j][0] = t;
                for (int k = 1; k <= 15; k ++ )
                    fa[j][k] = fa[fa[j][k - 1]][k - 1];
            }
        }
    }
}

int lca(int a, int b)
{
    if (depth[a] < depth[b]) swap(a, b);
    for (int k = 15; k >= 0; k -- )
        if (depth[fa[a][k]] >= depth[b])
            a = fa[a][k];
    if (a == b) return a;
    for (int k = 15; k >= 0; k -- )
        if (fa[a][k] != fa[b][k])
        {
            a = fa[a][k];
            b = fa[b][k];
        }
    return fa[a][0];
}

int main()
{
    scanf("%d", &n);
    int root = 0;
    memset(h, -1, sizeof h);

    for (int i = 0; i < n; i ++ )
    {
        int a, b;
        scanf("%d%d", &a, &b);
        if (b == -1) root = a;
        else add(a, b), add(b, a);
    }

    bfs(root);

    scanf("%d", &m);
    while (m -- )
    {
        int a, b;
        scanf("%d%d", &a, &b);
        int p = lca(a, b);
        if (p == a) puts("1");
        else if (p == b) puts("2");
        else puts("0");
    }

    return 0;
}

```





#  费用流

##  模板

```c++
#include <iostream>
#include <cstring>
#include <algorithm>

using namespace std;

const int N = 5010, M = 100010, INF = 1e8;

int n, m, S, T;
int h[N], e[M], f[M], w[M], ne[M], idx;
int q[N], d[N], pre[N], incf[N];
bool st[N];

void add(int a, int b, int c, int d)
{
    e[idx] = b, f[idx] = c, w[idx] = d, ne[idx] = h[a], h[a] = idx ++ ;
    e[idx] = a, f[idx] = 0, w[idx] = -d, ne[idx] = h[b], h[b] = idx ++ ;
}

bool spfa()
{
    int hh = 0, tt = 1;
    memset(d, 0x3f, sizeof d);
    memset(incf, 0, sizeof incf);
    q[0] = S, d[S] = 0, incf[S] = INF;
    while (hh != tt)
    {
        int t = q[hh ++ ];
        if (hh == N) hh = 0;
        st[t] = false;

        for (int i = h[t]; ~i; i = ne[i])
        {
            int ver = e[i];
            if (f[i] && d[ver] > d[t] + w[i])
            {
                d[ver] = d[t] + w[i];
                pre[ver] = i;
                incf[ver] = min(f[i], incf[t]);
                if (!st[ver])
                {
                    q[tt ++ ] = ver;
                    if (tt == N) tt = 0;
                    st[ver] = true;
                }
            }
        }
    }

    return incf[T] > 0;
}

void EK(int& flow, int& cost)
{
    flow = cost = 0;
    while (spfa())
    {
        int t = incf[T];
        flow += t, cost += t * d[T];
        for (int i = T; i != S; i = e[pre[i] ^ 1])
        {
            f[pre[i]] -= t;
            f[pre[i] ^ 1] += t;
        }
    }
}

int main()
{
    scanf("%d%d%d%d", &n, &m, &S, &T);
    memset(h, -1, sizeof h);
    while (m -- )
    {
        int a, b, c, d;
        scanf("%d%d%d%d", &a, &b, &c, &d);
        add(a, b, c, d);
    }

    int flow, cost;
    EK(flow, cost);
    printf("%d %d\n", flow, cost);

    return 0;
}

```

#  离散化

```c++
//离散化预处理
inline void discrete()
{
    //排序
    sort(a + 1,a + n + 1);
    //去重
    for(int i = 1;i <= n;++i)
    {
        if(i == 1 || a[i] != a[i-1])
            b[++m] = a[i];
    }
}

//二分查找 x映射为那个1~m之间的整数
inline int query(int x)
{
    return lower_bound(b + 1,b + m + 1,x) - b;
}
```





#  Ac自动机

```c++
#include <cstdio>
#include <cstring>
#include <iostream>
#include <algorithm>

using namespace std;

const int N = 10010, S = 55, M = 1000010;

int n;
int tr[N * S][26], cnt[N * S], idx;
char str[M];
int q[N * S], ne[N * S];

void insert()
{
    int p = 0;
    for (int i = 0; str[i]; i ++ )
    {
        int t = str[i] - 'a';
        if (!tr[p][t]) tr[p][t] = ++ idx;
        p = tr[p][t];
    }
    cnt[p] ++ ;
}

void build()
{
    int hh = 0, tt = -1;
    for (int i = 0; i < 26; i ++ )
        if (tr[0][i])
            q[ ++ tt] = tr[0][i];

    while (hh <= tt)
    {
        int t = q[hh ++ ];
        for (int i = 0; i < 26; i ++ )
        {
            int p = tr[t][i];
            if (!p) tr[t][i] = tr[ne[t]][i];
            else
            {
                ne[p] = tr[ne[t]][i];
                q[ ++ tt] = p;
            }
        }
    }
}

int main()
{
    int T;
    scanf("%d", &T);
    while (T -- )
    {
        memset(tr, 0, sizeof tr);
        memset(cnt, 0, sizeof cnt);
        memset(ne, 0, sizeof ne);
        idx = 0;

        scanf("%d", &n);
        for (int i = 0; i < n; i ++ )
        {
            scanf("%s", str);
            insert();
        }

        build();

        scanf("%s", str);

        int res = 0;
        for (int i = 0, j = 0; str[i]; i ++ )
        {
            int t = str[i] - 'a';
            j = tr[j][t];

            int p = j;
            while (p)
            {
                res += cnt[p];
                cnt[p] = 0;
                p = ne[p];
            }
        }

        printf("%d\n", res);
    }

    return 0;
}
```



#  线段树

##  一个简单的整数问题

> 给定一个长度为 NN 的数列 AA，以及 MM 条指令，每条指令可能是以下两种之一：
>
> 1. `C l r d`，表示把 A[l],A[l+1],…,A[r]A[l],A[l+1],…,A[r] 都加上 dd。
> 2. `Q l r`，表示询问数列中第 l∼rl∼r 个数的和。
>
> 对于每个询问，输出一个整数表示答案。

```c++
#include <cstdio>
#include <cstring>
#include <iostream>
#include <algorithm>

using namespace std;

typedef long long LL;

const int N = 100010;

int n, m;
int w[N];
struct Node
{
    int l, r;
    LL sum, add;
}tr[N * 4];

void pushup(int u)
{
    tr[u].sum = tr[u << 1].sum + tr[u << 1 | 1].sum;
}

void pushdown(int u)
{
    auto &root = tr[u], &left = tr[u << 1], &right = tr[u << 1 | 1];
    if (root.add)
    {
        left.add += root.add, left.sum += (LL)(left.r - left.l + 1) * root.add;
        right.add += root.add, right.sum += (LL)(right.r - right.l + 1) * root.add;
        root.add = 0;
    }
}

void build(int u, int l, int r)
{
    if (l == r) tr[u] = {l, r, w[r], 0};
    else
    {
        tr[u] = {l, r};
        int mid = l + r >> 1;
        build(u << 1, l, mid), build(u << 1 | 1, mid + 1, r);
        pushup(u);
    }
}

void modify(int u, int l, int r, int d)
{
    if (tr[u].l >= l && tr[u].r <= r)
    {
        tr[u].sum += (LL)(tr[u].r - tr[u].l + 1) * d;
        tr[u].add += d;
    }
    else    // 一定要分裂
    {
        pushdown(u);
        int mid = tr[u].l + tr[u].r >> 1;
        if (l <= mid) modify(u << 1, l, r, d);
        if (r > mid) modify(u << 1 | 1, l, r, d);
        pushup(u);
    }
}

LL query(int u, int l, int r)
{
    if (tr[u].l >= l && tr[u].r <= r) return tr[u].sum;

    pushdown(u);
    int mid = tr[u].l + tr[u].r >> 1;
    LL sum = 0;
    if (l <= mid) sum = query(u << 1, l, r);
    if (r > mid) sum += query(u << 1 | 1, l, r);
    return sum;
}


int main()
{
    scanf("%d%d", &n, &m);

    for (int i = 1; i <= n; i ++ ) scanf("%d", &w[i]);

    build(1, 1, n);

    char op[2];
    int l, r, d;

    while (m -- )
    {
        scanf("%s%d%d", op, &l, &r);
        if (*op == 'C')
        {
            scanf("%d", &d);
            modify(1, l, r, d);
        }
        else printf("%lld\n", query(1, l, r));
    }

    return 0;
}

```











