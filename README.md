# ToyLang

A python simple programming language，一个简单的python编程语言

# Python版本要求 Python version

- 最低 `Python >= 3.10`
- 推荐 `Python = 3.12`

- Least `Python >= 3.10`
- Use `Python = 3.12`

# 相关说明 About

- 令牌 tokens
    - "Hello World" -> 字符串 (string)
    - 114514 | 114514.191810 -> 数字 (number)
    - () -> 结构体 (structure)
    - [] -> 数组 (array)
    - {} -> 代码簇 (cluster)
    - () | [] | {} -> 包罗符 (including)

# 语法？Grammar?

|   关键字    |                                               用法                                               |
|:--------:|:----------------------------------------------------------------------------------------------:|
|   var    |                                 \<Variable> \= \<Expression*>                                  |
|    if    |                       (\<Condition*> \| \<Expression*>) {\<CodesCluster>}                        |
|  elseif  |                       (\<Condition*> \| \<Expression*>) {\<CodesCluster>}                        |
|   else   |                                       {\<CodesCluster>}                                        |
|   for    | \<Variable> from \<Expression*> to \<Expression*> (step \<Expression* -> 1>) {\<CodesCluster>} |
|  repeat  |                        (meet \| until)  \<Expression*> {\<CodesCluster>}                         |
| function |                               \<FunctionName> {\<CodesCluster>}                                |
|  delete  |                                          \<Variable>                                           |

- Variable : 变量名 varible name
- Condition : 条件表达式 condtion expr
- Expression : 普通表达式 normal expr
- CodesCluster : 执行代码 execute code
- {} : 表示填入代码  type code
- <> : 表示参数  param
- () : 表示非必选参数 unnessary
- (left | right) : 表示左边或右边的语法 left or right grammar
- (.*?) -> (.*?) : 表示默认值  default value
- | ： 表示"或"  'or'

## 三元表达式 Ternary Expression

用法

```
<Variable> ? <Expression> : <Expression>
     ^         ^      ^       ^      ^
     |         |      |       |      |
   变量名    触发符  真表达式 真|假  假表达式
```

示例

```
true ? "值为真" : "值为假"
```

## 变量别名 Use Variable as another name

用法

```
<Variable> -> <AnotherVaraibleName>
      ^         ^         ^
      |         |         |
被别名的变量    符号     别名变量
```

示例

```
true -> True
```
