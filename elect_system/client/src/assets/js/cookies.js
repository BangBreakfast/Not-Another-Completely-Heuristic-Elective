/* 用export把方法暴露出来 */
/* 设置cookie */
export function setCookie (Cname, value, expire) {
  var date = new Date()
  date.setSeconds(date.getSeconds() + expire)
  document.cookie = Cname + '=' + escape(value) + '; expires=' + date.toGMTString()
  console.log(document.cookie)
}

/* 获取cookie */
export function getCookie (Cname) {
  if (document.cookie.length > 0) {
    let Cstart = document.cookie.indexOf(Cname + '=')
    if (Cstart !== -1) {
      Cstart = Cstart + Cname.length + 1
      let Cend = document.cookie.indexOf(';', Cstart)
      if (Cend === -1) {
        Cend = document.cookie.length
      }
      return unescape(document.cookie.substring(Cstart, Cend))
    }
  }
  return ''
}

/* 删除cookie */
export function delCookie (Cname) {
  setCookie(Cname, '', -1)
}
