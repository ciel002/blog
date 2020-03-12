# blog — 个人博客
#### 导语：
>本练手项目的功能包含了博客最基本的一些功能，且在不断的搬码和完善中。
<br/>在本项目中，前端使用了Bootstrap框架，尽可能的做到响应式布局，使得PC端和移动端能够有一样的使用体验；
后端采用Flask框架，处理由前端传来的数据，完成博客的各项功能。
<br/>本人才疏学浅，所写代码仍有很多不足，希望能供大家参考的同时，也能得到一些指点和收获。

### 一、如何运行本项目
1. 将本项目下载到本地
2. 创建python虚拟环境，将项目中requirement.txt中的包下载
3. 在mysql中新建dev-database数据库，用于存放项目数据，并根据app/config.py中的数据库配置项进行配置，保持能够正常连接mysql
4. 运行python虚拟环境，在命令行中依次输入
<br> python manager.py db migrate 
<br> python manager.py db upgrade 
<br> python manager.py init_database
<br> python manager.py runserver
<br>python manager.py db init 
5. 成功运行（如有问题请联系作者，方式在下方）

### 二、项目结构说明
1. manager.py 为项目的入口文件
1. app/\_\_init\_\_.py 为项目的工厂函数
2. app/config.py 为项目app的配置项
3. app/data.py 为项目app的初始化数据
4. app/common 为项目的常量
5. app/form 为项目中生态HTML中form表单的表单目录
6. app/function 为项目中的一些功能函数目录
7. app/model 为项目中的数据库模型目录（MVC中的M）
8. app/static 为项目中的静态文件目录
9. app/templates 为项目中的模板文件目录（MVC中的V）
10. app/view为项目中的视图函数目录（MVC中的C）

### 三、测试项目
本项目测试地址：[mingchen.xyz](http://39.107.25.30/ "Blog")

### 四、联系作者
* QQ：1102839480
* 微信：ccnc320