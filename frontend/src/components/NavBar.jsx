import { IoMenu } from "react-icons/io5";
import { Link, useNavigate } from "react-router-dom";
import { logout } from "../redux/slice/authSlice.jsx";
import { useDispatch, useSelector } from "react-redux";

const NavBar = ({ toggleSidebar }) => {
  const navigate = useNavigate()
  const dispatch = useDispatch();
  const token = useSelector((state) => state.auth.token);

  const handleLogout = () => {
    dispatch(logout());
    navigate('/')
  };

  return (
    <div className="h-14 bg-[#009485] shadow flex items-center px-4">
      <button onClick={toggleSidebar} className="p-2 rounded-md hover:bg-gray-200 md:hidden">
        <IoMenu size={24} />
      </button>
      {token === null ? (
        <div className="md:flex gap-2 hidden w-full justify-end items-center">
          <Link to="/signup" className="px-4 py-2 rounded-md bg-white">
            SignUp
          </Link>
          <Link to="/login" className="px-4 py-2 rounded-md bg-white ">
            Login
          </Link>
        </div>
      ) : (
        <div className="md:flex gap-2 hidden w-full justify-end items-center">
          <button className="px-3 py-1 bg-red-600 text-white rounded-md" onClick={handleLogout}>
            Logout
          </button>
        </div>
      )}
    </div>
  );
};

export default NavBar;
