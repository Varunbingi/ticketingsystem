import { IoMenu } from "react-icons/io5";
import { Link, useNavigate } from "react-router-dom";
import { logout } from "../redux/slice/authSlice.jsx";
import { useDispatch, useSelector } from "react-redux";
import { useEffect } from "react";
import NotificationIcon from "./NotificationIcon";
import { useTranslation } from "react-i18next";

import { fetchUnreadCount } from "../redux/slice/notificationSlice";

const NavBar = ({ toggleSidebar }) => {

  const { t, i18n } = useTranslation();

  const navigate = useNavigate();
  const dispatch = useDispatch();
  const token = useSelector((state) => state.auth.token);
  const unreadCount = useSelector((state) => state.notifications.unreadCount);

  // 🔹 Sync language with localStorage on load
  useEffect(() => {
    const savedLang = localStorage.getItem("lang") || "en";
    if (i18n.language !== savedLang) {
      i18n.changeLanguage(savedLang);
    }
  }, [i18n]);

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
    navigate("/");
  };

  // LANGUAGE CHANGE FUNCTION
  const changeLanguage = (e) => {
    const lang = e.target.value;
    localStorage.setItem("lang", lang);
    i18n.changeLanguage(lang);
  };

  return (
    <div className="h-14 bg-[#009485] shadow flex items-center px-4 justify-between">

      <button
        onClick={toggleSidebar}
        className="p-2 rounded-md hover:bg-teal-700 md:hidden text-white"
      >
        <IoMenu size={24} />
      </button>

      <div className="flex items-center gap-4 ml-auto">

        <select
          onChange={changeLanguage}
          value={i18n.language}
          className="px-2 py-1 rounded text-sm"
        >
          <option value="en">English</option>
          <option value="te">తెలుగు</option>
        </select>

        {token === null ? (

          <div className="flex gap-2 items-center">

            <Link
              to="/signup"
              className="px-4 py-2 rounded-md bg-white text-sm font-medium"
            >
              {t("signup")}
            </Link>

            <Link
              to="/login"
              className="px-4 py-2 rounded-md bg-white text-sm font-medium"
            >
              {t("login")}
            </Link>

          </div>

        ) : (

          <div className="flex gap-4 items-center">

            <NotificationIcon unreadCount={unreadCount} />

            <button
              className="px-3 py-1 bg-red-600 text-white rounded-md text-sm font-medium"
              onClick={handleLogout}
            >
              {t("logout")}
            </button>

          </div>

        )}

      </div>

    </div>
  );
};

export default NavBar;