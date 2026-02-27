import {Navigate, Outlet,} from 'react-router-dom'
const RequireAuth=()=>{
    const isLogin=localStorage.getItem("isLogin");
    
    return isLogin?(<Outlet />):(<Navigate to='/login' />);
}

export default RequireAuth;