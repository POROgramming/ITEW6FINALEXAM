import { reactive } from 'vue'

export const auth = reactive({
  isLoggedIn: !!localStorage.getItem('access'),
  isStaff: localStorage.getItem('is_staff') === 'true',
})
