# API DOC

## JSON

### 登录

- Method: POST
- Paths: /stu/login, /dean/login
- Request body

```json
request.body = {
    "username": string,
    "password": string
}
```

- Response body

```json
// Login success
{
	"success": true,
	"msg": "Successfully login"
}
// Auth fail
{
    "success": false,
    "msg": "Incorrect password or nonexist user"
}
// Json format error
{
    "success": false,
    "msg": "Json format error"
}
// Parameter error
{
    "success": false,
    "msg": "Wrong parameter"
}
// Wrong method
{
    "success": false,
    "msg": "Wrong method"
}
```

### 退出

- Method: POST
- Paths: /stu/logout, /dean/logout
- Request body: (empty)
- Response body:
```json
// ok
{
    "success": true,
    "msg": "Successfully logout"
}
// Wrong method
{
	"success": false,
	"msg": "Wrong method"
}
```
### 获取时间信息
- Method: Get
- Paths: time/timetable.json
- Request body: (empty)
- Response body:
```json 
[
    // 具体的时间
    {
    "date":string, 
    // 时间的内容：选课节点等
    "detail":string,
    // 备注信息：开放跨院系选课等
    "info":string
    },
    {
    "date":string, 
    // 时间的内容：选课节点等
    "detail":string,
    // 备注信息：开放跨院系选课等
    "info":string
    },
    ...
]
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