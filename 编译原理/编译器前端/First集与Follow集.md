# First集与Follow集
> + 要了命了，当时偷懒没有实现的First集与Follow集功能现在成了制约编译器开发的巨大瓶颈
> 

## First集

**计算方法**
+ 如果 $X$ 是终结符号，那么$FIRST(X)=X$

+ 如果 $X$ 是非终结符号，且 $X \rightarrow  Y_1Y_2Y_3 \cdots Y_k$ 是产生式:
 
  + 如果$\alpha$在$FIRST(Y_i)$中，且 $\epsilon$ 在$FIRST(Y_1)$，$FIRST(Y_2)$，…，$FIRST(Y_{i-1})$中，那么$\alpha$也在$FIRST(X)$中；
  + 如果$\epsilon$ 在$FIRST(Y_1)$，$FIRST(Y_2)$，…，$FIRST(Y_k)$中，那么$\epsilon$在$FIRST(X)$中

+ 如果$X$是非终结符号，且有$X\rightarrow \epsilon$，那么$\epsilon$在$FIRST(X)$中


**注意事项**：
这个方法虽然理解起来很简单，但是实现起来非常复杂。
具体编码方法可以参考我的编译器项目。
```cpp
std::set<std::string> CBCompiler::LALR::GetFirst(const CBCompiler::LRToken &token) {
    //对于终结符来说
    if (token.type == LRType::END || token.type == LRType::EMPTY) {
        return {token.str};
    }
    std::set<std::string> res;


    auto rexpres = expressions[token.str];
    for (auto &expre: rexpres) {
        uint loc = 0;
        while (loc < expre.expression.size()) {
            auto to = expre.expression[loc];
            bool stop = false;
            switch (to.type) {
                case LRType::EMPTY:
                    loc++;
                    break;
                case LRType::END:
                    res.insert(to.str);
                    stop = true;
                    break;
                case LRType::UNEND:
                    if (to.str == token.str) { loc++; }
                    else {
                        auto result = GetFirst(to);
                        assert(result.count("empty") <= 1);
                        if (result.count("empty") == 1) {

                            for (auto &first: result) {
                                if (first == "empty")continue;
                                res.insert(first);
                            }
                            loc++;
                        } else {
                            res.insert(result.begin(), result.end());
                        }
                    }
                    break;
                default:
                    break;
            }
            if (stop)
                break;
        }

        //这就说明所有的项都包含empty
        if(loc==expre.expression.size())
        {
            res.insert("empty");
        }

    }
    return res;
}
```
##  Follow 集
