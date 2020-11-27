// This middleware will prevent a non admin user from accessing a page
export default ({ $auth, redirect }) => {
  if (!$auth.user || !$auth.user.is_admin) {
    return redirect('/')
  }
}
