# API DOC

## JSON

### stu, dean 登录

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

### stu, dean 退出

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
### stu 修改密码

#### Get Verification Code

- Method: __GET__
- Path: /stu/chpasswd?stuId=1600013239
- Request body: null

#### Send Verification Code

- Method: __POST__
- Path: /stu/chpasswd
- Request body:

```json
{
	"stuId": "1600013239",
	"password": "123456",	// new password
	"vcode": "1234"
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