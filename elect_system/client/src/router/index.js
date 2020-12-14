import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import stuCore from '@/components/stu/stuCore'
import stuLogin from '@/components/stu/stuLogin'
import stuProgram from '@/components/stu/stuProgram'
import stuPersonal from '@/components/stu/stuPersonal'
import stuCourseSearch from '@/components/stu/stuCourseSearch'
import stuCourseDetail from '@/components/stu/stuCourseDetail'
import stuMain from '@/components/stu/stuMain'
import adminCore from '@/components/admin/adminCore'
import adminLogin from '@/components/admin/adminLogin'
import adminProgram from '@/components/admin/adminProgram'
import adminManual from '@/components/admin/adminManual'
import adminCourseEdit from '@/components/admin/adminCourseEdit'
import adminCourseSearch from '@/components/admin/adminCourseSearch'
import adminMain from '@/components/admin/adminMain'
import adminTime from '@/components/admin/adminTime'
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
    },
    // StuComponent
    {
      path: '/stu',
      name: 'stuCore',
      component: stuCore,
      children: [
        {
          path: '/stuProgram',
          name: 'stuProgram',
          component: stuProgram
        },
        {
          path: '/stuPersonal',
          name: 'stuPersonal',
          component: stuPersonal
        },
        {
          path: '/stuCourseSearch',
          name: 'stuCourseSearch',
          component: stuCourseSearch
        },
        {
          path: '/stuCourseDetail/:id',
          name: 'stuCourseDetail',
          component: stuCourseDetail
        },
        {
          path: '/stuMain',
          name: 'stuMain',
          component: stuMain
        }
      ]
    },
    {
      path: '/stuLogin',
      name: 'stuLogin',
      component: stuLogin
    },
    // AdminComponent
    {
      path: '/admin',
      name: 'adminCore',
      component: adminCore,
      children: [
        {
          path: '/adminProgram',
          name: 'adminProgram',
          component: adminProgram
        },
        {
          path: '/adminManual',
          name: 'adminManual',
          component: adminManual
        },
        {
          path: '/adminCourseSearch',
          name: 'adminCourseSearch',
          component: adminCourseSearch
        },
        {
          path: '/adminMain',
          name: 'adminMain',
          component: adminMain
        },
        {
          path: '/adminTime',
          name: 'adminTime',
          component: adminTime
        },
        {
          path: '/adminCourseEdit',
          name: 'adminCourseEdit',
          component: adminCourseEdit
        }
      ]
    },
    {
      path: '/adminLogin',
      name: 'adminLogin',
      component: adminLogin
    }
  ]
})
