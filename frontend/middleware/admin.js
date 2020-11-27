export default ({ $auth, redirect }) => {
  console.log('ADMINS')
  // If the user is not and admin
  if (!$auth.user || !$auth.user.is_admin) {
    return redirect('/')
  }
}
