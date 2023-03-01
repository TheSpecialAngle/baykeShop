# BaykeShop（拜客商城系统）

For full documentation visit [bayke.shop（拜客商城系统）](http://www.bayke.shop).

## 项目简介

- **曾用名**：[django-happy-shop](https://gitee.com/xingfugz/happy-shop)【不再维护】
- **现用名**：[baykeShop](https://gitee.com/bayke/bayke-shop/)
- **baykeShop(拜客商城系统)** 的由来：
> `django-happy-shop`诞生于2022年，作为django框架的一个包出现，但商城作为一个综合性和定制性很强的项目，
单纯已三方包的形式维护并实现更多的功能就会显得非常臃肿，部署也变得更加困难，另外`django-happy-shop`在开发之初缺乏合理的架构设计，
很多地方设计并不合理，也不利于后期扩展，于是便萌生了重构的念想，也就有了现在的**拜客商城系统**，英文名称直接已域名命名为：**baykeShop**。

## 项目特色
一款更符合国人使用和学习的Python django开源商城项目，没有复杂的语法和过渡的封装，
一切符合django的使用方式，全部采用django的cbv模式开发，便于代码复用及二开和学习！

1、后台定制默认admin,支持动态菜单，兼容三方皮肤（如：django-simpleui）

2、完整的多规格商品逻辑，支持商品SPU和SKU及规格关系

3、支持余额支付、微信支付（开发中）、支付宝支付，配置简单收款便捷

4、凭借django强大的加持，可轻松配置多数据库Mysql/Sqlite3等

5、独立配置文件，通过简单的配置修改可控制全局相关功能

6、PC端采用django的模板系统开发，移动端通过DRF框架将分离开放标准的RestFull api接口（开发中）


## 快速上手

1、克隆项目源码
```
git clone https://gitee.com/bayke/bayke-shop.git
```
2、创建虚拟环境
```
cd bayke-shop
python3 -m venv venv
```
3、激活虚拟环境
```
Windows: venv\Scripts\activate
Liunx: source venv/bin/activate
```
4、运行项目
```
python3 manage.py runserver
```
5、查看项目
```
前台：http://127.0.0.1:8000
后台：http://127.0.0.1:8000/baykeadmin/
后台账号：admin  密码：admin123qwe
```


项目默认配置了sqllite3数据库，项目中已包含，因此上无需再创建数据库迁移命令和数据库同步命令！

> 备注：如果你要配置Mysql或其他数据库命令，可使用django的导出数据库命令把除过contenttypes相关的数据全部导出，配置好其他数据库之后再自行导入！



