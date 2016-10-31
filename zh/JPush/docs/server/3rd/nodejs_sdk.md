<<<<<<< HEAD
[![Build Status](https://travis-ci.org/jpush/jpush-api-nodejs-client.svg?branch=master)](https://travis-ci.org/jpush/jpush-api-nodejs-client)

# JPush API client library for Node.js

本 SDK 提供 JPush 服务端接口的 Node 封装，与 JPush Rest API 组件通信。使用时引用该模块即可，可参考附带 Demo 学习使用方法。

[REST API 文档](http://docs.jiguang.cn/server/rest_api_v3_push/)

[NodeJS API 文档][2]


## Install
=======
<h1>JPush API client library for Node.js</h1>

###概述

<div style="font-size:13px;background: #E0EFFE;border: 1px solid #ACBFD7;border-radius: 3px;padding: 8px 16px;">
<p>温馨提示：</p>
<p>详细API介绍文档地址   <a href="https://github.com/jpush/jpush-api-nodejs-client/blob/master/doc/api.md">NodeJS API DOC</a></p>
</div>

<br>

本SDK提供JPush服务端接口的Node封装，与 JPush Rest API 组件通信。使用时引用该模块即可，可参考附带Demo学习使用方法。

[REST API 文档](../server/rest_api_v3_push/)


版本更新：[Release页面](../../resources/#sdk_1)。下载更新请到这里。

###Install

>>>>>>> e8ebb19e891ee41f300ee8854a1e907b07df85b2
```
npm install jpush-sdk
#or
{
    "dependencies": {
        "jpush-sdk": "*"
    }
}
```

<<<<<<< HEAD

## Example
### Quick start
此 Demo 展示如何使用 Node lib 向所有用户推送通知。
``` js
var JPush = require("../lib/JPush/JPush.js")
var client = JPush.buildClient('your appKey', 'your masterSecret')
=======
### Example

#### Quick start

此Demo展示如何使用Node lib向所有用户推送通知。

```
var JPush = require("../lib/JPush/JPush.js");
var client = JPush.buildClient('your appKey', 'your masterSecret');
>>>>>>> e8ebb19e891ee41f300ee8854a1e907b07df85b2

//easy push
client.push().setPlatform(JPush.ALL)
    .setAudience(JPush.ALL)
<<<<<<< HEAD
    .setNotification('Hi, JPush', JPush.ios('ios alert', 'happy', 5))
    .send(function(err, res) {
        if (err) {
            console.log(err.message)
        } else {
            console.log('Sendno: ' + res.sendno)
            console.log('Msg_id: ' + res.msg_id)
=======
    .setNotification('Hi, JPush', JPush.ios('ios alert', 'happy.caf', 5))
    .send(function(err, res) {
        if (err) {
            console.log(err.message);
        } else {
            console.log('Sendno: ' + res.sendno);
            console.log('Msg_id: ' + res.msg_id);
>>>>>>> e8ebb19e891ee41f300ee8854a1e907b07df85b2
        }
    });
```

<<<<<<< HEAD
### Expert mode（高级版）

``` js
=======
#### Expert mode(高级版)

```
>>>>>>> e8ebb19e891ee41f300ee8854a1e907b07df85b2
client.push().setPlatform('ios', 'android')
    .setAudience(JPush.tag('555', '666'), JPush.alias('666,777'))
    .setNotification('Hi, JPush', JPush.ios('ios alert'), JPush.android('android alert', null, 1))
    .setMessage('msg content')
    .setOptions(null, 60)
    .send(function(err, res) {
        if (err) {
<<<<<<< HEAD
            console.log(err.message)
        } else {
            console.log('Sendno: ' + res.sendno)
            console.log('Msg_id: ' + res.msg_id)
        }
    });

```

关于 Payload 对象的方法，参考[详细 API 文档][4]。

### 获取统计信息
本 Node lib 简易封装获取统计信息的接口，传入推送 API 返回的 msg_id 列表，多个 msg_id 用逗号隔开，最多支持 100 个 msg_id。  
更多详细要求，请参考 [Report API 文档][5]。

```js
=======
            console.log(err.message);
        } else {
            console.log('Sendno: ' + res.sendno);
            console.log('Msg_id: ' + res.msg_id);
        }
    });
```


 关于Payload对象的方法，参考 [详细API文档](https://github.com/jpush/jpush-api-nodejs-client/blob/master/doc/api.md)

#### 获取统计信息

本Node lib简易封装获取统计信息的接口，传入推送API返回的 msg_id 列表，多个 msg_id 用逗号隔开，最多支持100个msg_id。
更多详细要求，请参考 [Report API 文档](../server/rest_api_v3_report/)

```
>>>>>>> e8ebb19e891ee41f300ee8854a1e907b07df85b2
var JPush = require("../lib/JPush/JPush.js");
var client = JPush.buildClient('your appKey', 'your masterSecret');

client.getReportReceiveds('746522674,344076897', function(err, res) {
    if (err) {
<<<<<<< HEAD
        console.log(err.message)
    } else {
        for (var i = 0; i < res.length; i++) {
            console.log(res[i].android_received)
            console.log(res[i].ios_apns_sent)
            console.log(res[i].msg_id)
            console.log('------------')
=======
        console.log(err.message);
    } else {
        for (var i=0; i<res.length; i++) {
            console.log(res[i].android_received);
            console.log(res[i].ios_apns_sent);
            console.log(res[i].msg_id);
            console.log('------------');
>>>>>>> e8ebb19e891ee41f300ee8854a1e907b07df85b2
        }
    }
});
```

<<<<<<< HEAD
### 关闭 Log

```js
// 在构建 JPushClient 对象的时候, 指定 isDebug 参数。
var client = JPush.buildClient({
    appKey:'47a3ddda34b2602fa9e17c01',
    masterSecret:'d94f733358cca97b18b2cb98',
    isDebug:false
});
// or
var client = JPush.buildClient('47a3ddda34b2602fa9e17c01', 'd94f733358cca97b18b2cb98', null, false);
```

### 单元测试

在程序根目录下执行.
```
mocha test
```


  [2]: doc/api.md
  [3]: http://docs.jpush.cn/display/dev/Push-API-v3#Push-API-v3-%E6%8E%A8%E9%80%81%E5%AF%B9%E8%B1%A1
  [4]: doc/api.md
  [5]: http://docs.jiguang.cn/server/rest_api_v3_report/
=======
####单元测试

在程序根目录下执行

```
mocha test
``` 
>>>>>>> e8ebb19e891ee41f300ee8854a1e907b07df85b2
