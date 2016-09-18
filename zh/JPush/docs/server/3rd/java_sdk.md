<h1>JPush API Java Library</h1>

<style>
img[alt=jpush_weblogic] { width: 800px; }
</style>

### 概述

这是 JPush REST API 的 Java 版本封装开发包，是由极光推送官方提供的，一般支持最新的 API 功能。

对应的 REST API 文档：[REST API - Push](../push/rest_api_v3_push/), [REST API - Report](../push/rest_api_v3_report/). 

本开发包 Javadoc：[API Docs](http://jpush.github.io/jpush-api-java-client/apidocs/)

版本更新：[Release页面](../../resources/#sdk_1)。下载更新请到这里。


### 安装

#### maven 方式

将下边的依赖条件放到你项目的 maven pom.xml 文件里。

```
<dependency>
    <groupId>cn.jpush.api</groupId>
    <artifactId>jpush-client</artifactId>
    <version>3.2.9</version>
</dependency>
```
#### jar 包方式

请到 [Release页面](https://github.com/jpush/jpush-api-java-client/releases)下载相应版本的发布包。

#### 依赖包
* [slf4j](http://www.slf4j.org/) / log4j (Logger)
* [gson](https://code.google.com/p/google-gson/) (Google JSON Utils)


其中 slf4j 可以与 logback, log4j, commons-logging 等日志框架一起工作，可根据你的需要配置使用。

如果使用 Maven 构建项目，则需要在你的项目 pom.xml 里增加：

```
		<dependency>
			<groupId>com.google.code.gson</groupId>
			<artifactId>gson</artifactId>
			<version>2.2.4</version>
		</dependency>
		<dependency>
			<groupId>org.slf4j</groupId>
			<artifactId>slf4j-api</artifactId>
			<version>1.7.5</version>
		</dependency>
		<dependency>
			<groupId>org.slf4j</groupId>
			<artifactId>slf4j-log4j12</artifactId>
			<version>1.7.5</version>
		</dependency>
		<dependency>
			<groupId>log4j</groupId>
			<artifactId>log4j</artifactId>
			<version>1.2.16</version>
		</dependency>
		<dependency>
			<groupId>junit</groupId>
			<artifactId>junit</artifactId>
			<version>4.11</version>
			<scope>test</scope>
		</dependency>
		<dependency>
			<groupId>com.google.guava</groupId>
			<artifactId>guava</artifactId>
			<version>17.0</version>
		</dependency>
		<dependency>
			<groupId>com.squareup.okhttp</groupId>
			<artifactId>mockwebserver</artifactId>
			<version>1.5.4</version>
			<scope>test</scope>
		</dependency>

```

如果不使用 Maven 构建项目，则项目 libs/ 目录下有依赖的 jar 可复制到你的项目里去。

#### 构建本项目

可以用 Eclipse 类 IDE 导出 jar 包。建议直接使用 maven，执行命令：

	maven package

#### 自动化测试

在项目目录下执行命令：

	mvn test

### 使用样例

#### 推送样例

以下片断来自项目代码里的文件：cn.jpush.api.examples.PushExample

```
        JPushClient jpushClient = new JPushClient(masterSecret, appKey, 3);
        
        // For push, all you need do is to build PushPayload object.
        PushPayload payload = buildPushObject_all_all_alert();
        
        try {
            PushResult result = jpushClient.sendPush(payload);
            LOG.info("Got result - " + result);
            
        } catch (APIConnectionException e) {
            // Connection error, should retry later
            LOG.error("Connection error, should retry later", e);
            
        } catch (APIRequestException e) {
            // Should review the error, and fix the request
            LOG.error("Should review the error, and fix the request", e);
            LOG.info("HTTP Status: " + e.getStatus());
            LOG.info("Error Code: " + e.getErrorCode());
            LOG.info("Error Message: " + e.getErrorMessage());
        }

```

进行推送的关键在于构建一个 PushPayload 对象。以下示例一般的构建对象的用法。

* 快捷地构建推送对象：所有平台，所有设备，内容为 ALERT 的通知。

```
	public static PushPayload buildPushObject_all_all_alert() {
	    return PushPayload.alertAll(ALERT);
	}
```

* 构建推送对象：所有平台，推送目标是别名为 "alias1"，通知内容为 ALERT。

```
    public static PushPayload buildPushObject_all_alias_alert() {
        return PushPayload.newBuilder()
                .setPlatform(Platform.all())
                .setAudience(Audience.alias("alias1"))
                .setNotification(Notification.alert(ALERT))
                .build();
    }
```

* 构建推送对象：平台是 Android，目标是 tag 为 "tag1" 的设备，内容是 Android 通知 ALERT，并且标题为 TITLE。

```
    public static PushPayload buildPushObject_android_tag_alertWithTitle() {
        return PushPayload.newBuilder()
                .setPlatform(Platform.android())
                .setAudience(Audience.tag("tag1"))
                .setNotification(Notification.android(ALERT, TITLE, null))
                .build();
    }
```

* 构建推送对象：平台是 iOS，推送目标是 "tag1", "tag_all" 的交集，推送内容同时包括通知与消息 - 通知信息是 ALERT，角标数字为 5，通知声音为 "happy"，并且附加字段 from = "JPush"；消息内容是 MSG_CONTENT。通知是 APNs 推送通道的，消息是 JPush 应用内消息通道的。APNs 的推送环境是“生产”（如果不显式设置的话，Library 会默认指定为开发）

```
    public static PushPayload buildPushObject_ios_tagAnd_alertWithExtrasAndMessage() {
        return PushPayload.newBuilder()
                .setPlatform(Platform.ios())
                .setAudience(Audience.tag_and("tag1", "tag_all"))
                .setNotification(Notification.newBuilder()
                        .addPlatformNotification(IosNotification.newBuilder()
                                .setAlert(ALERT)
                                .setBadge(5)
                                .setSound("happy.caf")
                                .addExtra("from", "JPush")
                                .build())
                        .build())
                 .setMessage(Message.content(MSG_CONTENT))
                 .setOptions(Options.newBuilder()
                         .setApnsProduction(true)
                         .build())
                 .build();
    }
```

* 构建推送对象：平台是 Andorid 与 iOS，推送目标是 （"tag1" 与 "tag2" 的并集）且（"alias1" 与 "alias2" 的并集），推送内容是 - 内容为 MSG_CONTENT 的消息，并且附加字段 from = JPush。

```
    public static PushPayload buildPushObject_ios_audienceMore_messageWithExtras() {
        return PushPayload.newBuilder()
                .setPlatform(Platform.android_ios())
                .setAudience(Audience.newBuilder()
                        .addAudienceTarget(AudienceTarget.tag("tag1", "tag2"))
                        .addAudienceTarget(AudienceTarget.alias("alias1", "alias2"))
                        .build())
                .setMessage(Message.newBuilder()
                        .setMsgContent(MSG_CONTENT)
                        .addExtra("from", "JPush")
                        .build())
                .build();
    }
```

#### 统计获取样例

以下片断来自项目代码里的文件：cn.jpush.api.examples.ReportsExample

```
        JPushClient jpushClient = new JPushClient(masterSecret, appKey);
		try {
            ReceivedsResult result = jpushClient.getReportReceiveds("1942377665");
            LOG.debug("Got result - " + result);
            
        } catch (APIConnectionException e) {
            // Connection error, should retry later
            LOG.error("Connection error, should retry later", e);
            
        } catch (APIRequestException e) {
            // Should review the error, and fix the request
            LOG.error("Should review the error, and fix the request", e);
            LOG.info("HTTP Status: " + e.getStatus());
            LOG.info("Error Code: " + e.getErrorCode());
            LOG.info("Error Message: " + e.getErrorMessage());
        }
```


### Weblogic 使用Java SDK

Weblogic在使用jpush-api-java-client时需要注意的一些事项。

#### 注意事项

本文档基于weblogic 10.3.6 版本，12版本请自己对应配置路径。

极个别时候，证书会有版本升级等情况，所以一定要验证当前使用的证书和官方证书的指纹是否一致。

**Weblogic console 设置**

+ 【主机名验证】设置为无，否则默认使用weblogic.security.SSL.HostnameVerifier进行主机名验证，导致Hostname验证失败
    + 配置路径 Weblogic Console > 服务器设置 > SSL > 高级 > 主机名验证
+ 选择【使用 JSSE SSL】，因为Weblogic默认的加密算法和Java标准的加密算法不一样
    + 配置路径 Weblogic Console > 服务器设置 > SSL > 高级 > 使用 JSSE SSL

**证书配置**

+ 检查Weblogic使用的信任密钥库的位置
    + 默认使用的文件是 JRE目录下面的  jre\lib\security\cacerts 文件
    + 有些开发者可能会改为自定义的信任密钥库
+ 检查对应的信任库是否包含了Geo Trust的根证书或者Geo Trust SSL二级 证书
    + 举例：keytool -list -keystore cacerts
    + 此过程需要信任库的密码（默认changeit）
    + 如果包含这两个证书中任意一个，调用JPush接口都可以调用通过
+ 如果信任库不包含上述证书，需要导入公钥到对应的信任库
    + 打开jpush.cn，导出公钥（可以是Geo Trust根证书、Geo Trust SSL 或者 *.jpush.cn 三个任意一个，具体导出方法请百度）
    + 将导出的公钥证书导入到步骤1对应的信任库
    + 举例：keytool -import -alias geotrustssl -keystore cacerts -file GeoTrustSSL.cer
    + 此过程需要信任库的密码（默认changeit）

**证书对比方式**

+ 执行 keytool -list -keystore mykey.jks  命令列出信任库里的所有公钥，观察对应证书的指纹
+ 检查官网证书，观察对应证书的指纹
+ 比较两个指纹是否一致，如下图所示
![jpush_weblogic](image/weblogic.png)

#### 异常记录
**证书错误异常**

```
Can not connect to JPush Server. Please ensure your internet connection is ok. 
If the problem persists, please let us know at support@jpush.cn.
javax.net.ssl.SSLHandshakeException: General SSLEngine problem
 at com.sun.net.ssl.internal.ssl.Handshaker.checkThrown(Handshaker.java:1015)
 at com.sun.net.ssl.internal.ssl.SSLEngineImpl.checkTaskThrown(SSLEngineImpl.java:485)
 at com.sun.net.ssl.internal.ssl.SSLEngineImpl.writeAppRecord(SSLEngineImpl.java:1128)
 at com.sun.net.ssl.internal.ssl.SSLEngineImpl.wrap(SSLEngineImpl.java:1100)
 at javax.net.ssl.SSLEngine.wrap(SSLEngine.java:452)
 at weblogic.security.SSL.jsseadapter.JaSSLEngine$1.run(JaSSLEngine.java:68)
 at weblogic.security.SSL.jsseadapter.JaSSLEngine.doAction(JaSSLEngine.java:732)
 at weblogic.security.SSL.jsseadapter.JaSSLEngine.wrap(JaSSLEngine.java:66)
 at weblogic.socket.JSSEFilterImpl.wrapAndWrite(JSSEFilterImpl.java:619)
 at weblogic.socket.JSSEFilterImpl.doHandshake(JSSEFilterImpl.java:91)
 at weblogic.socket.JSSEFilterImpl.doHandshake(JSSEFilterImpl.java:64)
 at weblogic.socket.JSSEFilterImpl.doHandshake(JSSEFilterImpl.java:59)
 at weblogic.socket.JSSEFilterImpl.write(JSSEFilterImpl.java:390)
 at weblogic.socket.JSSESocket$JSSEOutputStream.write(JSSESocket.java:78)
 at java.io.BufferedOutputStream.flushBuffer(BufferedOutputStream.java:65)
 at java.io.BufferedOutputStream.flush(BufferedOutputStream.java:123)
 at java.io.FilterOutputStream.flush(FilterOutputStream.java:123)
 at weblogic.net.http.HttpURLConnection.writeRequests(HttpURLConnection.java:186)
 at weblogic.net.http.HttpURLConnection.getOutputStream(HttpURLConnection.java:280)
 at cn.jpush.api.common.connection.NativeHttpClient._doRequest(NativeHttpClient.java:153)
 at cn.jpush.api.common.connection.NativeHttpClient.doRequest(NativeHttpClient.java:93)
 at cn.jpush.api.common.connection.NativeHttpClient.sendPost(NativeHttpClient.java:80)
 at cn.jpush.api.push.PushClient.sendPush(PushClient.java:119)
 at cn.jpush.api.JPushClient.sendMessageAll(JPushClient.java:362)
 at cn.liucy.hello.HelloPush.doPost(HelloPush.java:40)
 at cn.liucy.hello.HelloPush.doGet(HelloPush.java:29)
 at javax.servlet.http.HttpServlet.service(HttpServlet.java:707)
 at javax.servlet.http.HttpServlet.service(HttpServlet.java:820)
 at weblogic.servlet.internal.StubSecurityHelper$ServletServiceAction.run(StubSecurityHelper.java:227)
 at weblogic.servlet.internal.StubSecurityHelper.invokeServlet(StubSecurityHelper.java:125)
 at weblogic.servlet.internal.ServletStubImpl.execute(ServletStubImpl.java:301)
 at weblogic.servlet.internal.ServletStubImpl.execute(ServletStubImpl.java:184)
 at weblogic.servlet.internal.WebAppServletContext$ServletInvocationAction.wrapRun(WebAppServletContext.java:3732)
 at weblogic.servlet.internal.WebAppServletContext$ServletInvocationAction.run(WebAppServletContext.java:3696)
 at weblogic.security.acl.internal.AuthenticatedSubject.doAs(AuthenticatedSubject.java:321)
 at weblogic.security.service.SecurityManager.runAs(SecurityManager.java:120)
 at weblogic.servlet.internal.WebAppServletContext.securedExecute(WebAppServletContext.java:2273)
 at weblogic.servlet.internal.WebAppServletContext.execute(WebAppServletContext.java:2179)
 at weblogic.servlet.internal.ServletRequestImpl.run(ServletRequestImpl.java:1490)
 at weblogic.work.ExecuteThread.execute(ExecuteThread.java:256)
 at weblogic.work.ExecuteThread.run(ExecuteThread.java:221)
Caused by: javax.net.ssl.SSLHandshakeException: General SSLEngine problem
 at com.sun.net.ssl.internal.ssl.Alerts.getSSLException(Alerts.java:174)
 at com.sun.net.ssl.internal.ssl.SSLEngineImpl.fatal(SSLEngineImpl.java:1528)
 at com.sun.net.ssl.internal.ssl.Handshaker.fatalSE(Handshaker.java:243)
 at com.sun.net.ssl.internal.ssl.Handshaker.fatalSE(Handshaker.java:235)
 at com.sun.net.ssl.internal.ssl.ClientHandshaker.serverCertificate(ClientHandshaker.java:1206)
 at com.sun.net.ssl.internal.ssl.ClientHandshaker.processMessage(ClientHandshaker.java:136)
 at com.sun.net.ssl.internal.ssl.Handshaker.processLoop(Handshaker.java:593)
 at com.sun.net.ssl.internal.ssl.Handshaker$1.run(Handshaker.java:533)
 at java.security.AccessController.doPrivileged(Native Method)
 at com.sun.net.ssl.internal.ssl.Handshaker$DelegatedTask.run(Handshaker.java:952)
 at weblogic.socket.JSSEFilterImpl.doTasks(JSSEFilterImpl.java:186)
 at weblogic.socket.JSSEFilterImpl.doHandshake(JSSEFilterImpl.java:95)
 ... 31 more
Caused by: sun.security.validator.ValidatorException: PKIX path building failed: sun.security.provider.certpath.SunCertPathBuilderException: unable to find valid certification path to requested target
 at sun.security.validator.PKIXValidator.doBuild(PKIXValidator.java:323)
 at sun.security.validator.PKIXValidator.engineValidate(PKIXValidator.java:217)
 at sun.security.validator.Validator.validate(Validator.java:218)
 at com.sun.net.ssl.internal.ssl.X509TrustManagerImpl.validate(X509TrustManagerImpl.java:126)
 at com.sun.net.ssl.internal.ssl.X509TrustManagerImpl.checkServerTrusted(X509TrustManagerImpl.java:209)
 at weblogic.security.SSL.jsseadapter.JaTrustManager.checkServerTrusted(JaTrustManager.java:125)
 at com.sun.net.ssl.internal.ssl.ClientHandshaker.serverCertificate(ClientHandshaker.java:1198)
 ... 38 more
Caused by: sun.security.provider.certpath.SunCertPathBuilderException: unable to find valid certification path to requested target
 at sun.security.provider.certpath.SunCertPathBuilder.engineBuild(SunCertPathBuilder.java:174)
 at java.security.cert.CertPathBuilder.build(CertPathBuilder.java:238)
 at sun.security.validator.PKIXValidator.doBuild(PKIXValidator.java:318)
 ... 44 more
```

**未使用JSSE SSL异常**
```
Can not connect to JPush Server. Please ensure your internet connection is ok. 
If the problem persists, please let us know at support@jpush.cn.
javax.net.ssl.SSLKeyException: FATAL Alert:BAD_CERTIFICATE - A corrupt or unuseable certificate was received.
 at com.certicom.tls.interfaceimpl.TLSConnectionImpl.fireException(Unknown Source)
 at com.certicom.tls.interfaceimpl.TLSConnectionImpl.fireAlertSent(Unknown Source)
 at com.certicom.tls.record.handshake.HandshakeHandler.fireAlert(Unknown Source)
 at com.certicom.tls.record.handshake.HandshakeHandler.handleHandshakeMessages(Unknown Source)
 at com.certicom.tls.record.MessageInterpreter.interpretContent(Unknown Source)
 at com.certicom.tls.record.MessageInterpreter.decryptMessage(Unknown Source)
 at com.certicom.tls.record.ReadHandler.processRecord(Unknown Source)
 at com.certicom.tls.record.ReadHandler.readRecord(Unknown Source)
 at com.certicom.tls.record.ReadHandler.readUntilHandshakeComplete(Unknown Source)
 at com.certicom.tls.interfaceimpl.TLSConnectionImpl.completeHandshake(Unknown Source)
 at com.certicom.tls.record.WriteHandler.write(Unknown Source)
 at com.certicom.io.OutputSSLIOStreamWrapper.write(Unknown Source)
 at java.io.BufferedOutputStream.flushBuffer(BufferedOutputStream.java:65)
 at java.io.BufferedOutputStream.flush(BufferedOutputStream.java:123)
 at java.io.FilterOutputStream.flush(FilterOutputStream.java:123)
 at weblogic.net.http.HttpURLConnection.writeRequests(HttpURLConnection.java:186)
 at weblogic.net.http.HttpURLConnection.getOutputStream(HttpURLConnection.java:280)
 at cn.jpush.api.common.connection.NativeHttpClient._doRequest(NativeHttpClient.java:153)
 at cn.jpush.api.common.connection.NativeHttpClient.doRequest(NativeHttpClient.java:93)
 at cn.jpush.api.common.connection.NativeHttpClient.sendPost(NativeHttpClient.java:80)
 at cn.jpush.api.push.PushClient.sendPush(PushClient.java:119)
 at cn.jpush.api.JPushClient.sendMessageAll(JPushClient.java:362)
 at cn.liucy.hello.HelloPush.doPost(HelloPush.java:40)
 at cn.liucy.hello.HelloPush.doGet(HelloPush.java:29)
 at javax.servlet.http.HttpServlet.service(HttpServlet.java:707)
 at javax.servlet.http.HttpServlet.service(HttpServlet.java:820)
 at weblogic.servlet.internal.StubSecurityHelper$ServletServiceAction.run(StubSecurityHelper.java:227)
 at weblogic.servlet.internal.StubSecurityHelper.invokeServlet(StubSecurityHelper.java:125)
 at weblogic.servlet.internal.ServletStubImpl.execute(ServletStubImpl.java:301)
 at weblogic.servlet.internal.ServletStubImpl.execute(ServletStubImpl.java:184)
 at weblogic.servlet.internal.WebAppServletContext$ServletInvocationAction.wrapRun(WebAppServletContext.java:3732)
 at weblogic.servlet.internal.WebAppServletContext$ServletInvocationAction.run(WebAppServletContext.java:3696)
 at weblogic.security.acl.internal.AuthenticatedSubject.doAs(AuthenticatedSubject.java:321)
 at weblogic.security.service.SecurityManager.runAs(SecurityManager.java:120)
 at weblogic.servlet.internal.WebAppServletContext.securedExecute(WebAppServletContext.java:2273)
 at weblogic.servlet.internal.WebAppServletContext.execute(WebAppServletContext.java:2179)
 at weblogic.servlet.internal.ServletRequestImpl.run(ServletRequestImpl.java:1490)
 at weblogic.work.ExecuteThread.execute(ExecuteThread.java:256)
 at weblogic.work.ExecuteThread.run(ExecuteThread.java:221)
15/12/09 13:52:03 ERROR hello.HelloPush: Failed to server.
cn.jpush.api.common.resp.APIConnectionException: Connection IO error. 
Can not connect to JPush Server. Please ensure your internet connection is ok. 
If the problem persists, please let us know at support@jpush.cn.
 at cn.jpush.api.common.connection.NativeHttpClient._doRequest(NativeHttpClient.java:242)
 at cn.jpush.api.common.connection.NativeHttpClient.doRequest(NativeHttpClient.java:93)
 at cn.jpush.api.common.connection.NativeHttpClient.sendPost(NativeHttpClient.java:80)
 at cn.jpush.api.push.PushClient.sendPush(PushClient.java:119)
 at cn.jpush.api.JPushClient.sendMessageAll(JPushClient.java:362)
 at cn.liucy.hello.HelloPush.doPost(HelloPush.java:40)
 at cn.liucy.hello.HelloPush.doGet(HelloPush.java:29)
 at javax.servlet.http.HttpServlet.service(HttpServlet.java:707)
 at javax.servlet.http.HttpServlet.service(HttpServlet.java:820)
 at weblogic.servlet.internal.StubSecurityHelper$ServletServiceAction.run(StubSecurityHelper.java:227)
 at weblogic.servlet.internal.StubSecurityHelper.invokeServlet(StubSecurityHelper.java:125)
 at weblogic.servlet.internal.ServletStubImpl.execute(ServletStubImpl.java:301)
 at weblogic.servlet.internal.ServletStubImpl.execute(ServletStubImpl.java:184)
 at weblogic.servlet.internal.WebAppServletContext$ServletInvocationAction.wrapRun(WebAppServletContext.java:3732)
 at weblogic.servlet.internal.WebAppServletContext$ServletInvocationAction.run(WebAppServletContext.java:3696)
 at weblogic.security.acl.internal.AuthenticatedSubject.doAs(AuthenticatedSubject.java:321)
 at weblogic.security.service.SecurityManager.runAs(SecurityManager.java:120)
 at weblogic.servlet.internal.WebAppServletContext.securedExecute(WebAppServletContext.java:2273)
 at weblogic.servlet.internal.WebAppServletContext.execute(WebAppServletContext.java:2179)
 at weblogic.servlet.internal.ServletRequestImpl.run(ServletRequestImpl.java:1490)
 at weblogic.work.ExecuteThread.execute(ExecuteThread.java:256)
 at weblogic.work.ExecuteThread.run(ExecuteThread.java:221)
Caused by: javax.net.ssl.SSLKeyException: FATAL Alert:BAD_CERTIFICATE - A corrupt or unuseable certificate was received.
 at com.certicom.tls.interfaceimpl.TLSConnectionImpl.fireException(Unknown Source)
 at com.certicom.tls.interfaceimpl.TLSConnectionImpl.fireAlertSent(Unknown Source)
 at com.certicom.tls.record.handshake.HandshakeHandler.fireAlert(Unknown Source)
 at com.certicom.tls.record.handshake.HandshakeHandler.handleHandshakeMessages(Unknown Source)
 at com.certicom.tls.record.MessageInterpreter.interpretContent(Unknown Source)
 at com.certicom.tls.record.MessageInterpreter.decryptMessage(Unknown Source)
 at com.certicom.tls.record.ReadHandler.processRecord(Unknown Source)
 at com.certicom.tls.record.ReadHandler.readRecord(Unknown Source)
 at com.certicom.tls.record.ReadHandler.readUntilHandshakeComplete(Unknown Source)
 at com.certicom.tls.interfaceimpl.TLSConnectionImpl.completeHandshake(Unknown Source)
 at com.certicom.tls.record.WriteHandler.write(Unknown Source)
 at com.certicom.io.OutputSSLIOStreamWrapper.write(Unknown Source)
 at java.io.BufferedOutputStream.flushBuffer(BufferedOutputStream.java:65)
 at java.io.BufferedOutputStream.flush(BufferedOutputStream.java:123)
 at java.io.FilterOutputStream.flush(FilterOutputStream.java:123)
 at weblogic.net.http.HttpURLConnection.writeRequests(HttpURLConnection.java:186)
 at weblogic.net.http.HttpURLConnection.getOutputStream(HttpURLConnection.java:280)
 at cn.jpush.api.common.connection.NativeHttpClient._doRequest(NativeHttpClient.java:153)
 ... 21 more
```

**Hostname验证失败异常**

```
Can not connect to JPush Server. Please ensure your internet connection is ok. 
If the problem persists, please let us know at support@jpush.cn.
javax.net.ssl.SSLKeyException: Hostname verification failed: HostnameVerifier=weblogic.security.utils.SSLWLSHostnameVerifier, hostname=api.jpush.cn.
 at weblogic.security.SSL.jsseadapter.JaSSLEngine.doPostHandshake(JaSSLEngine.java:675)
 at weblogic.security.SSL.jsseadapter.JaSSLEngine.doAction(JaSSLEngine.java:746)
 at weblogic.security.SSL.jsseadapter.JaSSLEngine.unwrap(JaSSLEngine.java:132)
 at weblogic.socket.JSSEFilterImpl.unwrap(JSSEFilterImpl.java:505)
 at weblogic.socket.JSSEFilterImpl.unwrapAndHandleResults(JSSEFilterImpl.java:448)
 at weblogic.socket.JSSEFilterImpl.doHandshake(JSSEFilterImpl.java:80)
 at weblogic.socket.JSSEFilterImpl.doHandshake(JSSEFilterImpl.java:64)
 at weblogic.socket.JSSEFilterImpl.doHandshake(JSSEFilterImpl.java:59)
 at weblogic.socket.JSSEFilterImpl.write(JSSEFilterImpl.java:390)
 at weblogic.socket.JSSESocket$JSSEOutputStream.write(JSSESocket.java:78)
 at java.io.BufferedOutputStream.flushBuffer(BufferedOutputStream.java:65)
 at java.io.BufferedOutputStream.flush(BufferedOutputStream.java:123)
 at java.io.FilterOutputStream.flush(FilterOutputStream.java:123)
 at weblogic.net.http.HttpURLConnection.writeRequests(HttpURLConnection.java:186)
 at weblogic.net.http.HttpURLConnection.getOutputStream(HttpURLConnection.java:280)
 at cn.jpush.api.common.connection.NativeHttpClient._doRequest(NativeHttpClient.java:153)
 at cn.jpush.api.common.connection.NativeHttpClient.doRequest(NativeHttpClient.java:93)
 at cn.jpush.api.common.connection.NativeHttpClient.sendPost(NativeHttpClient.java:80)
 at cn.jpush.api.push.PushClient.sendPush(PushClient.java:119)
 at cn.jpush.api.JPushClient.sendMessageAll(JPushClient.java:362)
 at cn.liucy.hello.HelloPush.doPost(HelloPush.java:40)
 at cn.liucy.hello.HelloPush.doGet(HelloPush.java:29)
 at javax.servlet.http.HttpServlet.service(HttpServlet.java:707)
 at javax.servlet.http.HttpServlet.service(HttpServlet.java:820)
 at weblogic.servlet.internal.StubSecurityHelper$ServletServiceAction.run(StubSecurityHelper.java:227)
 at weblogic.servlet.internal.StubSecurityHelper.invokeServlet(StubSecurityHelper.java:125)
 at weblogic.servlet.internal.ServletStubImpl.execute(ServletStubImpl.java:301)
 at weblogic.servlet.internal.ServletStubImpl.execute(ServletStubImpl.java:184)
 at weblogic.servlet.internal.WebAppServletContext$ServletInvocationAction.wrapRun(WebAppServletContext.java:3732)
 at weblogic.servlet.internal.WebAppServletContext$ServletInvocationAction.run(WebAppServletContext.java:3696)
 at weblogic.security.acl.internal.AuthenticatedSubject.doAs(AuthenticatedSubject.java:321)
 at weblogic.security.service.SecurityManager.runAs(SecurityManager.java:120)
 at weblogic.servlet.internal.WebAppServletContext.securedExecute(WebAppServletContext.java:2273)
 at weblogic.servlet.internal.WebAppServletContext.execute(WebAppServletContext.java:2179)
 at weblogic.servlet.internal.ServletRequestImpl.run(ServletRequestImpl.java:1490)
 at weblogic.work.ExecuteThread.execute(ExecuteThread.java:256)
 at weblogic.work.ExecuteThread.run(ExecuteThread.java:221)
15/12/09 14:27:17 ERROR hello.HelloPush: Failed to server.
cn.jpush.api.common.resp.APIConnectionException: Connection IO error. 
Can not connect to JPush Server. Please ensure your internet connection is ok. 
If the problem persists, please let us know at support@jpush.cn.
 at cn.jpush.api.common.connection.NativeHttpClient._doRequest(NativeHttpClient.java:242)
 at cn.jpush.api.common.connection.NativeHttpClient.doRequest(NativeHttpClient.java:93)
 at cn.jpush.api.common.connection.NativeHttpClient.sendPost(NativeHttpClient.java:80)
 at cn.jpush.api.push.PushClient.sendPush(PushClient.java:119)
 at cn.jpush.api.JPushClient.sendMessageAll(JPushClient.java:362)
 at cn.liucy.hello.HelloPush.doPost(HelloPush.java:40)
 at cn.liucy.hello.HelloPush.doGet(HelloPush.java:29)
 at javax.servlet.http.HttpServlet.service(HttpServlet.java:707)
 at javax.servlet.http.HttpServlet.service(HttpServlet.java:820)
 at weblogic.servlet.internal.StubSecurityHelper$ServletServiceAction.run(StubSecurityHelper.java:227)
 at weblogic.servlet.internal.StubSecurityHelper.invokeServlet(StubSecurityHelper.java:125)
 at weblogic.servlet.internal.ServletStubImpl.execute(ServletStubImpl.java:301)
 at weblogic.servlet.internal.ServletStubImpl.execute(ServletStubImpl.java:184)
 at weblogic.servlet.internal.WebAppServletContext$ServletInvocationAction.wrapRun(WebAppServletContext.java:3732)
 at weblogic.servlet.internal.WebAppServletContext$ServletInvocationAction.run(WebAppServletContext.java:3696)
 at weblogic.security.acl.internal.AuthenticatedSubject.doAs(AuthenticatedSubject.java:321)
 at weblogic.security.service.SecurityManager.runAs(SecurityManager.java:120)
 at weblogic.servlet.internal.WebAppServletContext.securedExecute(WebAppServletContext.java:2273)
 at weblogic.servlet.internal.WebAppServletContext.execute(WebAppServletContext.java:2179)
 at weblogic.servlet.internal.ServletRequestImpl.run(ServletRequestImpl.java:1490)
 at weblogic.work.ExecuteThread.execute(ExecuteThread.java:256)
 at weblogic.work.ExecuteThread.run(ExecuteThread.java:221)
Caused by: javax.net.ssl.SSLKeyException: Hostname verification failed: HostnameVerifier=weblogic.security.utils.SSLWLSHostnameVerifier, hostname=api.jpush.cn.
 at weblogic.security.SSL.jsseadapter.JaSSLEngine.doPostHandshake(JaSSLEngine.java:675)
 at weblogic.security.SSL.jsseadapter.JaSSLEngine.doAction(JaSSLEngine.java:746)
 at weblogic.security.SSL.jsseadapter.JaSSLEngine.unwrap(JaSSLEngine.java:132)
 at weblogic.socket.JSSEFilterImpl.unwrap(JSSEFilterImpl.java:505)
 at weblogic.socket.JSSEFilterImpl.unwrapAndHandleResults(JSSEFilterImpl.java:448)
 at weblogic.socket.JSSEFilterImpl.doHandshake(JSSEFilterImpl.java:80)
 at weblogic.socket.JSSEFilterImpl.doHandshake(JSSEFilterImpl.java:64)
 at weblogic.socket.JSSEFilterImpl.doHandshake(JSSEFilterImpl.java:59)
 at weblogic.socket.JSSEFilterImpl.write(JSSEFilterImpl.java:390)
 at weblogic.socket.JSSESocket$JSSEOutputStream.write(JSSESocket.java:78)
 at java.io.BufferedOutputStream.flushBuffer(BufferedOutputStream.java:65)
 at java.io.BufferedOutputStream.flush(BufferedOutputStream.java:123)
 at java.io.FilterOutputStream.flush(FilterOutputStream.java:123)
 at weblogic.net.http.HttpURLConnection.writeRequests(HttpURLConnection.java:186)
 at weblogic.net.http.HttpURLConnection.getOutputStream(HttpURLConnection.java:280)
 at cn.jpush.api.common.connection.NativeHttpClient._doRequest(NativeHttpClient.java:153)
 ... 21 more
```


