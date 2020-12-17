import Vue from 'vue'

import stuLogin from '@/components/stu/stuLogin'
import {setCookie, getCookie} from '../../../src/assets/js/cookies.js'
import axios from 'axios'

jest.mock('axios')
jest.mock('../../../src/assets/js/cookies.js')
axios.post.mockResolvedValue({
  succes: true,
  msg: 'None'
})
// stuLogin.StuLogin
describe('stu.AssertStuLogin', () => {
  it('模拟用户登录', () => {
    const Constructor = Vue.extend(stuLogin)
    const vm = new Constructor().$mount()
    vm.find('button').trigger('click')
    test('getUserInfo 有且只 call 了一次', () => {
      expect(axios.post.mock.calls.length).toBe(1);
    });
    expect(vm.$el.querySelector('.hello h1').textContent)
      .toEqual('Welcome to Your Vue.js App')
  })
})
