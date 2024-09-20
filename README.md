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
| 关键字 | 用法 |
| :----: | :----: |
| var    | <VariableName> = <Expression*> |
| if     | <Condition*> \| <Expression*> {<CodesCluster>} |
| elseif | <Condition*> \| <Expression*> {<CodesCluster>} |
| else   | {<CodesCluster>} |
| for    | <VariableName> from <Expression*> to <Expression*> (step <Expression* -> 1>) {<CodesCluster>} |
| repeat | meet \| until  <Expression*> {<CodesCluster>}|
| function | <FunctionName> {<CodesCluster>} |
| delete | <Variable> |

- VariableName : 变量名
- Condition : 条件表达式
- Expression : 普通表达式
- CodesCluster : 执行代码
- () : 表示非必选参数
- (.*?) -> (.*?) : 表示默认值
- | ： 表示"或"

## 三元表达式 Ternary Expression

用法
```
<VariableName> ? <Expression> : <Expression>
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
<VariableName> -> <AnotherVaraibleName>
      ^         ^         ^
      |         |         |
被别名的变量    符号     别名变量
```

示例
```
true as True
```
