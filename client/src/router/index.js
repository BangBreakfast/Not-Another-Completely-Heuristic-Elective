import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'

import ElementUi from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'

Vue.use(ElementUi)

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/test/hello',
      name: 'HelloWorld',
      component: HelloWorld
    }
  ]
})
