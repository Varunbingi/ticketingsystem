import { Link, NavLink, useNavigate } from "react-router-dom";
import { IoHomeOutline } from "react-icons/io5";
import { FaRegHandshake, FaUsers, FaTicket } from "react-icons/fa6";
import { FaUserLock } from "react-icons/fa";
import { TbUserSquareRounded } from "react-icons/tb";
import { useDispatch, useSelector } from "react-redux";
import { logout } from "../redux/slice/authSlice.jsx";

const menuItemClasses = ({ isActive }) =>
  `flex items-center gap-3 px-4 py-2 rounded-md transition-all ${isActive ? "bg-[#007a6c] text-white" : "text-gray-200 hover:bg-[#26a699] hover:text-white"}`;

const SideBar = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const token = useSelector((state) => state.auth.token);

  const handleLogout = () => {
    dispatch(logout());
    navigate('/')
  };
  return (
    <nav className="group  px-2 h-full flex flex-col md:hover:w-40 md:transition-all md:duration-300">
      <div className="flex items-center justify-center h-14 gap-1">
        <h1>CMDX</h1>
      </div>
      <ul className="space-y-1">
        <li>
          <NavLink to="/" className={menuItemClasses}>
            <IoHomeOutline size={20} />
            <span className="whitespace-nowrap overflow-hidden md:w-0 md:opacity-0 md:group-hover:w-auto md:group-hover:opacity-100 md:transition-all md:duration-300">Home</span>
          </NavLink>
        </li>
        <li>
          <NavLink to="/users" className={menuItemClasses}>
            <TbUserSquareRounded size={20} />
            <span className="whitespace-nowrap overflow-hidden md:w-0 md:opacity-0 group-hover:w-auto group-hover:opacity-100 transition-all duration-300">Users</span>
          </NavLink>
        </li>
        <li>
          <NavLink to="/client" className={menuItemClasses}>
            <FaRegHandshake size={20} />
            <span  className="whitespace-nowrap overflow-hidden md:w-0 md:opacity-0 group-hover:w-auto group-hover:opacity-100 transition-all duration-300">Client</span>
          </NavLink>
        </li>
        <li>
          <NavLink to="/roles" className={menuItemClasses}>
            <FaUsers size={20} />
            <span  className="whitespace-nowrap overflow-hidden md:w-0 md:opacity-0 group-hover:w-auto group-hover:opacity-100 transition-all duration-300">Roles</span>
          </NavLink>
        </li>
        <li>
          <NavLink to="/permissions" className={menuItemClasses}>
            <FaUserLock size={20} />
            <span  className="whitespace-nowrap overflow-hidden md:w-0 md:opacity-0 group-hover:w-auto group-hover:opacity-100 transition-all duration-300">Permissions</span>
          </NavLink>
        </li>
        <li>
          <NavLink to="/tickets" className={menuItemClasses}>
            <FaTicket size={20} />
            <span  className="whitespace-nowrap overflow-hidden md:w-0 md:opacity-0 group-hover:w-auto group-hover:opacity-100 transition-all duration-300">Tickets</span>
          </NavLink>
        </li>
      </ul>
      <div className="mt-auto mb-10 flex justify-center gap-2 md:hidden">
       {token === null ? (
        <div className="flex gap-2 md:hidden w-full justify-center items-center">
          <Link to="/signup" className="px-4 py-2 rounded-md bg-slate-800">
            SignUp
          </Link>
          <Link to="/login" className="px-4 py-2 rounded-md bg-slate-800 ">
            Login
          </Link>
        </div>
      ) : (
        <div className="flex  md:hidden w-full justify-center items-center">
          <button className="px-3 py-1 bg-red-600 text-white rounded-md" onClick={handleLogout}>
            Logout
          </button>
        </div>
      )}
      </div>
    </nav>
  );
};

export default SideBar;
