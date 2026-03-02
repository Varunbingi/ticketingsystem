
import React, { useEffect, useState } from "react";
import { useDispatch } from "react-redux";
import axiosInstance from "../config/axiosInstance";
import { decrementCount } from "../redux/slice/notificationSlice";
import { 
  IoNotificationsOutline, 
  IoCheckmarkDoneOutline, 
  IoTimeOutline,
  IoMailOutline,
  IoPhonePortraitOutline,
  IoDesktopOutline
} from "react-icons/io5";

const Notifications = () => {
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const dispatch = useDispatch();


  const fetchNotifications = async () => {
    try {
      setLoading(true);
 
      const response = await axiosInstance.get("/notifications/");
      setNotifications(response.data);
      setError(null);
    } catch (err) {
      console.error("Failed to fetch notifications:", err);
      setError("Could not load notifications. Please try again later.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchNotifications();
  }, []);


  const markAsRead = async (id) => {
    try {

      await axiosInstance.patch(`/notifications/${id}/read`);
      
      setNotifications((prev) =>
        prev.map((n) => (n.id === id ? { ...n, read_status: true } : n))
      );
      
      dispatch(decrementCount());
    } catch (err) {
      console.error("Error marking notification as read:", err);
    }
  };

  const getChannelIcon = (channel) => {
    switch (channel?.toUpperCase()) {
      case 'EMAIL': return <IoMailOutline />;
      case 'SMS': return <IoPhonePortraitOutline />;
      default: return <IoDesktopOutline />;
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[#009485]"></div>
        <p className="mt-4 text-gray-600 font-medium">Loading your alerts...</p>
      </div>
    );
  }

  return (
    <div className="p-4 md:p-8 max-w-5xl mx-auto min-h-screen bg-gray-50">
      {/* Header Section */}
      <div className="flex flex-col md:flex-row md:items-center justify-between mb-8 gap-4 border-b border-gray-200 pb-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-800 flex items-center gap-3">
            <IoNotificationsOutline className="text-[#009485]" />
            Notifications
          </h1>
          <p className="text-gray-500 mt-1">Updates regarding your tickets and account security.</p>
        </div>
        <div className="flex items-center gap-2">
          <span className="bg-teal-100 text-[#009485] px-4 py-1.5 rounded-full text-sm font-semibold shadow-sm">
            {notifications.filter(n => !n.read_status).length} New
          </span>
        </div>
      </div>

      {error && (
        <div className="mb-6 p-4 bg-red-50 border-l-4 border-red-500 text-red-700 rounded">
          {error}
        </div>
      )}

      {/* Notifications List */}
      <div className="grid gap-4">
        {notifications.length > 0 ? (
          notifications.map((n) => (
            <div
              key={n.id}
              onClick={() => !n.read_status && markAsRead(n.id)}
              className={`group relative p-5 rounded-xl border transition-all duration-200 cursor-pointer shadow-sm hover:shadow-md ${
                n.read_status
                  ? "bg-gray-50 border-gray-200 opacity-75"
                  : "bg-white border-l-4 border-l-[#009485] border-gray-200"
              }`}
            >
              <div className="flex justify-between items-start gap-4">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <h3 className={`font-bold text-lg ${n.read_status ? "text-gray-600" : "text-gray-900"}`}>
                      {n.title}
                    </h3>
                    {!n.read_status && (
                      <span className="w-2.5 h-2.5 bg-[#009485] rounded-full animate-pulse"></span>
                    )}
                  </div>
                  <p className="text-gray-600 leading-relaxed text-sm md:text-base">
                    {n.message}
                  </p>
                  
                  <div className="flex items-center gap-4 mt-4 text-xs text-gray-400 font-medium">
                    <span className="flex items-center gap-1">
                      <IoTimeOutline size={14} />
                      {new Date(n.created_at).toLocaleString('en-US', {
                        month: 'short',
                        day: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit'
                      })}
                    </span>
                    <span className="flex items-center gap-1 uppercase tracking-wider">
                      {getChannelIcon(n.channel)}
                      {n.channel || 'INAPP'}
                    </span>
                  </div>
                </div>

                <div className="flex items-center">
                  {n.read_status ? (
                    <IoCheckmarkDoneOutline className="text-gray-400" size={24} />
                  ) : (
                    <button 
                      onClick={(e) => {
                        e.stopPropagation();
                        markAsRead(n.id);
                      }}
                      className="text-[#009485] hover:bg-teal-50 p-2 rounded-full transition-colors"
                      title="Mark as read"
                    >
                      <IoCheckmarkDoneOutline size={24} />
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="flex flex-col items-center justify-center py-24 bg-white rounded-2xl border-2 border-dashed border-gray-200">
            <div className="bg-gray-50 p-6 rounded-full mb-4">
              <IoNotificationsOutline size={48} className="text-gray-300" />
            </div>
            <p className="text-gray-500 text-lg font-medium">No notifications yet</p>
            <p className="text-gray-400 text-sm">We'll let you know when something happens.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Notifications;