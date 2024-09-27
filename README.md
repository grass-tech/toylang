# ToyLang

网站 ： [ToyLang](https://toy.nekocode.top)

Website: [ToyLang](https://toy.nekocode.top)

A python simple programming language，一个简单的python编程语言

## Python版本要求 Python Version Required

- 最低 `Python >= 3.10`
- 推荐 `Python = 3.12`

- Least `Python >= 3.10`
- Recommended `Python = 3.12`

## 相关说明 About

- 令牌 tokens
  - "Hello World" -> 字符串 (string)
  - 114514 | 114514.191810 -> 数字 (number)
  - () -> 结构体 (structure)
  - [] -> 数组 (array)
  - {} -> 代码簇 (cluster)
  - () | [] | {} -> 包罗符 (including)

## 语法 Grammar

|   关键字    | 用法                                                                                             |   用途   |
|:--------:|:-----------------------------------------------------------------------------------------------|:------:|
|   var    | \<Variable> \= \<Expression*>                                                                  |  设置变量  |
|    if    | (\<Condition*> \| \<Expression*>) {\<CodesCluster>}                                            |   如果   |
|  elseif  | (\<Condition*> \| \<Expression*>) {\<CodesCluster>}                                            |  否则如果  |
|   else   | {\<CodesCluster>}                                                                              |   否则   |
|   for    | \<Variable> from \<Expression*> to \<Expression*> (step \<Expression* -> 1>) {\<CodesCluster>} |  迭代循环  |
|  repeat  | (meet \| until)  \<Expression*> {\<CodesCluster>}                                              |  条件循环  |
| function | \<FunctionName> {\<CodesCluster>}                                                              |  构建函数  |
|  delete  | \<Variable>                                                                                    |  删除变量  |
|  return  | \<Expression*>                                                                                 |  函数返回  |
| break    | NULL                                                                                           |  跳出循环  |
| continue | NULL                                                                                          | 跳出本次循环 |
| include  | \<Library> \| \<Module>                                                                       | 导入库或模块 |

|   内置函数   |           用法            |    用途    |
|:--------:|:-----------------------:|:--------:|
| println  |  <Expression*> -> Any   | 输出信息到控制台 |
| readline | <Expression*> -> String |  读取用户输入  |
|   int    |  <Expression*> -> INT   | 将值转换为整型  |
|  string  |  <Expression*> -> Any   | 将值转换为字符串 |
| boolean  |      <Condition*>       | 将值转换为布尔值 |
|  array   | <Expression*> -> String | 将值转换为数组  |
|  length  | <Expression*> -> String |   获取长度   |
|   run    |    \<File> -> String     |   运行tl源文件  |

- Variable : 变量名 variable name
- Condition : 条件表达式 condition expr
- Expression : 普通表达式 normal expr
- CodesCluster : 执行代码 execute code
- {} : 表示填入代码 type code
- <> : 表示参数 param
- () : 表示非必选参数
- (left | right) : 表示左边或右边的语法 left or right grammar
- (.*?) -> (.*?) : 表示默认值 default value
- | ： 表示"或"  'or'

### 如何隔开代码簇 How to split cluster

**使用 *分号* 隔开代码簇的各个代码**

**Use *Semi* to separate codes in cluster**

### 三元表达式 Ternary Expression

用法

```js
<Variable> ? <Expression> : <Expression>
    ^      ^      ^       ^      ^
    |      |      |       |      |
   变量名 触发符 真表达式   真|假  假表达式
```

示例

```js
true ? "值为真" : "值为假"
```

### 变量别名 Variable Alias

用法

```txt
<Variable> -> <AnotherVaraibleName>
    ^       ^         ^
    |       |         |
被别名的变量  符号     别名变量
```

示例

```txt
true -> True
```

## 代码示例 Code Example

- **奇偶数判断**

  Shell

  ```shell
  > function isEven(number) {if number % 2 == 0 {println('是偶数')} else {println('非偶数')}}
  > isEven(20)
  是偶数
  > isEven(19)
  非偶数
  ```

  File

  ```js
  function isEven(number) {
    if number % 2 == 0 {
      println('是偶数')
    } else {
      println('是奇数')
    }
  }

  println(isEven(19))
  println(isEven(20))
  ```

- **迭代奇偶数判断**

  Shell

  ```js
  > var maximum = int(readline('Type maximum number: '))
  > for i from 1 to maximum {if i % 2 == 0 {println(string(i) + " 是偶数")} else {println(string(i) + " 是奇数")}}
  ```

  File

  ```js
  var maximum = int(readline('Type maximum number: '))
  for i from 1 to maximum {
    if i % 2 == 0 {
      println(string(i) + " 是偶数")
    } else {
      println(string(i) + " 是奇数")
    }
  }
  ```

- **输出偶数**

  Shell
  
  ```js
  > var minimum = int(readline('Type minimum number: '))
  > var maximum = int(readline('Type maximum number: '))
  > if minimum % 2 == 0 {for i from minimum to maximum step 2 {println(i)}} else {println(string(minimum) + " 非偶数，请输入一个偶数")}
  ```
  
  File
  
  ```js
  var minimum = int(readline('Type minimum number: '))
  var maximum = int(readline('Type maximum number: '))
  if minimum % 2 == 0 {
    for i from minimum to maximum step 2 {
      println(i)
    } 
  } else {
    println(string(minimum) + " 非偶数，请输入一个偶数")
  }
  ```

- **斐波那契数列**

  Shell
  
  ```js
  > function fib(n) {function fn(i) {if i < 2 {return 1} else {return fn(i - 2) + fn(i - 1)}};for x from 0 to n {println(fn(x))}}
  > fib(int(readline('type maximum fibonachi: ')))
  ```
  
  File
  
  ```js
  function fib(n) {
    function fn(i) {
      if i < 2 {
        return 1
      } else {
        return fn(i - 2) + fn(i - 1)
      }
    };
    for x from 0 to n {
      println(fn(x))
    }
  }
  
  fib(int(readline('type maximum fibonachi: ')))
  ```

- **累加器**

  Shell

  ```js
  var start = int(readline('Type start number: '))
  var end = int(readline('Type end number: '))
  var counter = 0
  repeat until start == end {
    var counter = counter + 1;
    var start = start   + 1
  }
  println('从' + string(end - counter) + '加到' + string(end) + '需要加' +   string(counter) + '次')
  ```
  
  File
  
  ```js
  var start = int(readline('Type start number: '))
  var end = int(readline('Type end number: '))
  var counter = 0
  repeat until start == end {
    var counter = counter + 1;
    var start = start + 1
  }
  println('从' + string(end - counter) + '加到' + string(end) + '需要加' +   string(counter) + '次')
  ```

- **正确数据校验**

  ```js
  repeat meet true {
    var data = readline('Type a data: ');
      meet data == 'exit' {
      println('正确数据');
      var data = ''
    }
  }
  ```
