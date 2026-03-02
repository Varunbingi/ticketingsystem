import { IoMenu } from "react-icons/io5";
import { Link, useNavigate } from "react-router-dom";
import { logout } from "../redux/slice/authSlice.jsx";
import { useDispatch, useSelector } from "react-redux";
import { useEffect } from "react"; 
import NotificationIcon from './NotificationIcon';

import { fetchUnreadCount } from "../redux/slice/notificationSlice"; 

const NavBar = ({ toggleSidebar }) => {
  const navigate = useNavigate()
  const dispatch = useDispatch();
  const token = useSelector((state) => state.auth.token);
  const unreadCount = useSelector((state) => state.notifications.unreadCount);


useEffect(() => {
    if (token) {
      dispatch(fetchUnreadCount());

  
      const interval = setInterval(() => {
        dispatch(fetchUnreadCount());
      }, 30000);

      return () => clearInterval(interval); 
    }
  }, [token, dispatch]);
  const handleLogout = () => {
    dispatch(logout());
    navigate('/')
  };

  return (
    <div className="h-14 bg-[#009485] shadow flex items-center px-4 justify-between">
      <button onClick={toggleSidebar} className="p-2 rounded-md hover:bg-teal-700 md:hidden text-white">
        <IoMenu size={24} />
      </button>

      <div className="flex items-center gap-4 ml-auto">
        {token === null ? (
          <div className="flex gap-2 items-center">
            <Link to="/signup" className="px-4 py-2 rounded-md bg-white text-sm font-medium">
              SignUp
            </Link>
            <Link to="/login" className="px-4 py-2 rounded-md bg-white text-sm font-medium">
              Login
            </Link>
          </div>
        ) : (
          <div className="flex gap-4 items-center">
            <NotificationIcon unreadCount={unreadCount} />
            <button 
              className="px-3 py-1 bg-red-600 text-white rounded-md text-sm font-medium" 
              onClick={handleLogout}
            >
              Logout
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default NavBar;