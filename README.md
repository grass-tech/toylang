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

|   关键字    | 用法                                                                                             |                     用途                     |
|:--------:|:-----------------------------------------------------------------------------------------------|:------------------------------------------:|
|  global  | \<Variable>                                                                                    |          声明一个全局变量 Global variable          |
| private  | \<PrivatbleKeyWords> \<Expression*>                                                            |          数据私有化 Data to be private          |
|   var    | \<Variable> \= \<Expression*>                                                                  |           设置变量 Defined Variable            |
|    if    | (\<Condition*> \| \<Expression*>) {\<CodesCluster>}                                            |                 如果     if                  |
|  elseif  | (\<Condition*> \| \<Expression*>) {\<CodesCluster>}                                            |                 否则如果 then                  |
|   else   | {\<CodesCluster>}                                                                              |                 否则    else                 |
|   for    | \<Variable> from \<Expression*> to \<Expression*> (step \<Expression* -> 1>) {\<CodesCluster>} |             次数循环 repeat times              |
| foriter  | \<Variable> by (\<Variable> \| \[Array])                                                       |        迭代循环      iterate repeating         |
|  repeat  | (meet \| until)  \<Expression*> {\<CodesCluster>}                                              |         条件循环     condition repeat          |
| function | \<FunctionName> {\<CodesCluster>}                                                              |          构建函数     build function           |
|  delete  | \<Variable>                                                                                    |           删除变量   delete variable           |
|  return  | \<Expression*>                                                                                 |         函数返回 Function return value         |
| include  | \<Library> \| \<Module>                                                                        |   导入库或模块      import library or modules    |
|  break   | NULL                                                                                           |   跳出循环           jump out from repeating   |
| continue | NULL                                                                                           | 跳出本次循环          jump once out of repeating |

|   内置函数    |                             用法                             |      用途      |
|:---------:|:----------------------------------------------------------:|:------------:|
|  println  |                    <Expression*> -> Any                    |   输出信息到控制台   |
| readline  |                  <Expression*> -> String                   |    读取用户输入    |
|    int    |                    <Expression*> -> INT                    |   将值转换为整型    |
|  string   |                    <Expression*> -> Any                    |   将值转换为字符串   |
|  boolean  |                        <Condition*>                        |   将值转换为布尔值   |
|   array   |                  <Expression*> -> String                   |   将值转换为数组    |
|  length   |                  <Expression*> -> String                   |     获取长度     |
| timestamp | (Null \| [\<Time>, (\<TimeFormat> = "%Y-%m-%d %H:M%:%S")]) |  获取当前时间的时间戳  |
| calllist  |                      \<Object> -> Any                      | 获取对象所有可调用的列表 |
|   idle    |                            Null                            |    打开IDLE    |
|    run    |                     \<File> -> String                      |   运行tl源文件    |

- Time : 时间
- TimeFormat : 时间格式 time format
- PrivatableKeyWords : 可私有化关键字 private keyword
    - var 定义变量 or define variable
    - function 构建函数 or build function
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

---

【\*】 IDLE new add `idle_call_funciton_table` variable, this need upload a dict, dict's key is called builtin function
name, value is called execute function

【\*】 IDLE 新增`idle_call_function_table`的变量，该变量需传入一个字典；字典的键为调用的内置函数的名字，值为所对应的调用的执行函数

---

Default: {'println': print, 'readline': input}

默认：{'println': print, 'readline': input}

*IDLE*: {'println': self.println, 'readline': self.readline}

## 如何隔开代码簇 How to split cluster

**使用 *分号* 隔开代码簇的各个代码**

**Use *Semi* to separate codes in cluster**

### 三元表达式 Ternary Expression

用法 Useage

```js
<Variable> ? <Expression> : <Expression>
    ^      ^      ^       ^      ^
    |      |      |       |      |
   变量名 触发符 真表达式   真|假  假表达式
```

示例 Example

```js
true ? "值为真" : "值为假"
```

### 变量别名 Variable Alias

用法 Useage

```txt
<Variable> -> <AnotherVaraibleName>
    ^       ^         ^
    |       |         |
被别名的变量  符号     别名变量
```

示例 Example

```txt
true -> True
```

### 切片 Subscripts

用法 Useage

```txt
(<Variable> | [Array] | [String])[<Variable> | [Number]]
              ^                          ^
              |                          |
           被切片的                      索引
```

示例 Example

```txt
[1, 2, 3, 4, 5, 6][1]
[1, 2, 3, 4 ,5 ,6][0]
```

### 可选参数 Optional parameter

用法 Useage

```txt
function <FunctionName>(<Variable> = <Expression>) {<Expression>}
                                   ^
                                   |
                            参等于Param equal
```

示例 Example

```js
function test(a, b=1) {return a + b;}
test(1);
```

### 隐藏变量

> 隐藏变量是指无法被正常通过`Father.Child.Variable`的方式访问的变量（外部仍然可以通过`$`访问）

> Hiden variable means cannot normally access by `Father.Child.Varaible` (Outdoor still can access by `$`)

用法 Useage

```txt
var __<Variable>__ = <Expression*>
 ^       ^
 |       |
变量 开头末尾有"_"的变量
```

示例 Example

```js
var __test__ = '123'
```

调用 Call

```
$__test__
```

## 内置库 Builtin Libraries

### 随机数 random

> 采用梅森旋转算法生成伪随机数

> Use Mersenne Twister Algorithm to generate pseudo random number

```js
/* random generator by Mersenne Twister Arguments */

var N = 624
var M = 397
var MATRIX_A = 0x9908B0DF
var UPPER_MASK = 0x80000000
var LOWER_MASK = 0x7FFFFFFF

var state = [0] * N
var index = N + 1

/* private twist function */
private function twist() {
    global state
    global index
    for i from 0 to N - 1 {
        var x = (state[i] & UPPER_MASK) + (state[(i + 1) % N] & LOWER_MASK)
        var xA = x >> 1;
        if (x % 2 == 1) {
            var xA = xA ^ MATRIX_A;
        }
        var state[i] = state[(i + M) % N] ^ xA;
    }
    var index = 0;
}

/* seed generator */
function seed(seed_value=0) {
    if seed_value == null {
        var seed_value = int(timestamp(), true)
    }
    global state
    global index
    var state[0] = seed_value;
    for i from 1 to N - 1 {
        var state[i] = (1812433253 * (state[i - 1] ^ (state[i - 1] >> 30)) + i) & 0xFFFFFFFF
    }
    var index = N
}

/* relay random generator */
function retrack() {
    global state
    global index
    seed()

    if index >= N {
        twist()
    }
    var y = state[index]
    var y = y ^  ((y >> 11) & 0xFFFFFFFF)
    var y = y ^ ((y << 7) & 0x9D2C5680)
    var y = y ^ ((y << 15) & 0xEFC60000)
    var y = y ^ (y >> 18)
    var index = index + 1
    return y & 0xFFFFFFFF
}

/* choose a random in range */
function rand(min, max) {
    var range = max - min + 1
    return (retrack() % range) + min
}
```

- random.seed() 随机数种子 random seed
- random.retrack() 重置随机数 reset
- random.rand(x, y) 随机数生成(范围) random generator (range)

### 单元库 Utils

> 封装一些常用函数

> Wrap some common functions

```js
/* Multiple Function Package File 多函数包文件 */

/* fibonacci with factorial 递归斐波那契数列 */
function factorial_fib(n=10) {
    var result = [];
    function factor(i) {
        if i < 2 {
            return 1;
        } else {
            return factor(i - 2) + factor(i - 1);
        }
    }

    for x from 0 to n {
        var result = result + factor(x);
    }
    return result
}

/* fibonacci with Repeat 循环斐波那契数列 */
function repeat_fib(n=20) {
    var result = [];
    for i from 0 to n {
        if i <= 1 {
            var result = result + [1];
        } else {
            var result = result + (result[i-2] + result[i-1]);
        }
    }
    return result;
}

/* mapping function */
function map(func, ld) {
    var result = [];
    for x from 0 to length(ld) - 1 {
        var result = result + func(ld[x]);
    }
    return result;
}

/* access array element(s) */
function access(ld, i) {
    return ld[i];
}

/* Compute Running Time */
function timer(func) {
    var starttime = timestamp();
    func();
    return timestamp() - starttime;
}
```

- factorial_fib(n=10) 递归斐波那契数列 factorial fibonacci
- repeat_fib(n=20) 循环斐波那契数列 repeat fibonacci
- map(func, ld) 映射函数 map function
- access(ld, i) 访问数组元素 access array element
- timer(func) 计算运行时间 compute running time

### 非标准数学库 Non-Standard Math

> 封装一些数学函数，注意：此数学库为  **非标准** 数学库，不支持所有数学函数，仅支持部分数学函数且计算可能不正确

> Wrap some math functions, note: This math library is **non-standard** math library, does not support all math
> functions, only supports some math functions and the calculation may be incorrect.

```js
/* non-Standard Math Libray */

/* Some normal constants */
var pi = 3.141592653589793
var e = 2.718281828459045
var tau = 6.283185307179586

/* Power */
function pow(n, p) {
    return n ** p;
}

/* Absolute value */
function abs(n) {
    if n < 0 {
        return -n;
    } else {
        return n;
    }
}

/* factorial */
function factorial(n) {
    var result = 1;
    for x from 1 to n {
        var result = result * x;
    }
    return result;
}

/* Special factorial to compute trigonometric functions */
private function _factorial(n) {
    if n == 0 or n == 1 {
        return 1;
    }
    var result = 1;
    for x from 2 to n {
        var result = result * x;
    }
    return result
}

/* Square root */
function sqrt(n) {
    return n ** 0.5;
}

/* Trigonometric 'cos' by Taylor series */
function cos(n, terms = 10) {
    var result = 0;
    for x from 0 to terms - 1 {
        var term = ((-1) ** x) * (n ** (2 * x)) / _factorial(2 * x);
        var result = result + term;
    }
    return result;
}

/* Trigonometric 'sin' by Taylor series */
function sin(n, terms = 10) {
    var result = 0;
    for x from 0 to terms - 1 {
        var term = ((-1) ** x) * (n ** (2 * x + 1)) / _factorial(2 * x + 1);
        var result = result + term;
    }
    return result;
}

/* Test each math function 'test' */
function test() {
    var result = [];
    var result = result + pow(2, 2);
    var result = result + factorial(5);
    var result = result + abs(5);
    var result = result + abs(-5)
    println(['math.pow(2, 2)', 'math.factorial(5)', 'math.abs(5)', 'math.abs(-5)']);
    println(result)
    var result = [];
    var result = result + cos(pi / 2);
    var result = result + sin(pi / 2);
    println(['math.cos(pi / 2)', 'math.sin(pi / 2)']);
    println(result)

    println('Function end successfully')

    return null;
}
```

- pow(n, p) 幂运算 pow
- abs(n) 绝对值 abs
- factorial(n) 阶乘 factorial
- sqrt(n) 平方根 sqrt
- cos(n, terms = 10) 余弦 cos
- sin(n, terms = 10) 正弦 sin

---

- test() 测试函数 test
