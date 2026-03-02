import React from "react";
import { IoNotificationsOutline } from "react-icons/io5";
import { useNavigate } from "react-router-dom";

const NotificationIcon = ({ unreadCount = 0 }) => {
  const navigate = useNavigate();

  return (
    <button 
      onClick={() => navigate('/notifications')}
      className="relative p-2 text-white hover:bg-white/10 rounded-full transition-colors focus:outline-none"
      aria-label="View Notifications"
    >
      <IoNotificationsOutline size={24} />
      {unreadCount > 0 && (
        <span className="absolute top-1 right-1 inline-flex items-center justify-center px-1.5 py-0.5 text-[10px] font-bold leading-none text-white transform translate-x-1/2 -translate-y-1/2 bg-red-600 rounded-full border border-white">
          {unreadCount}
        </span>
      )}
    </button>
  );
};

export default NotificationIcon;