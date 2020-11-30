# API DOC
## JSON
### 登录

/user
	/user/login 
```json

发送
request.body = {
    "username": string,
    "password": string
}

返回
// 成功：
{
    "code": 200,
    "data": {
        "msg": "success"
    }
}
// 用户不存在
{
    "code": 404,
    "data": {
        "msg": "unknown"
    }
}
//失败
{
    "code": -200,
    "data": {
        "msg": "fail"
    }
}
```
### Response Body Fudanmental
``` json
// 通用：
{
    "code": xxx,
    "data": {
        "msg": string,
        xxx: xxx
    }
}


// 用户无权限
response.body = {
    "code": 400,
    "data": {
        "msg": "not authorized"
    }
}

// 用户未登录
response.body = {
    "code": 400,
    "data": {
        "msg": "user not logged in"
    }
}

// 方法错误：
{
    "code": 600,
    "data": {
        "msg": "wrong method"
    }
}

// 参数错误：
{
    "code": 700,
    "data": {
        "msg": "wrong parameter"
    }
}

```