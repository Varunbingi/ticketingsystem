import { useState } from "react";
import { FaArrowLeftLong } from "react-icons/fa6";
import { FaGoogle, FaGithub } from "react-icons/fa";
import { Link, useNavigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { login, oauthgoogle, oauthgithub, clearError } from "../redux/slice/authSlice.jsx";

const Login = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { loading, oauthLoading, error } = useSelector((state) => state.auth);

  const [data, setData] = useState({ username: "", password: "" });

  const handleChange = (e) => {
    dispatch(clearError());
    setData({ ...data, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const result = await dispatch(login(data));
    if (result.meta.requestStatus === "fulfilled") {
      navigate("/");
    }
  };


  const handleGoogle = async () => {
    const result = await dispatch(oauthgoogle());
    if (result.meta.requestStatus === "fulfilled") {
      const url = result.payload; 
      if (url) {
        window.location.href = url;
      }
    }
  };

  
  const handleGithub = async () => {
    const result = await dispatch(oauthgithub());
    if (result.meta.requestStatus === "fulfilled") {
      const url = result.payload; 
      if (url) {
        window.location.href = url;
      }
    }
  };
  const errorMessage = typeof error === "string"
    ? error
    : error?.detail || error?.message || null;

  return (
    <div className="min-h-screen flex items-center justify-center bg-black/10 p-4">
      <div className="bg-white shadow-lg rounded-xl p-8 w-full max-w-md">
        <Link to="/">
          <FaArrowLeftLong />
        </Link>
        <h1 className="text-2xl font-bold text-center mb-6">Login</h1>

        {errorMessage && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 text-red-600 text-sm rounded-md">
            {errorMessage}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="flex flex-col">
            <label htmlFor="username" className="font-medium mb-1">Username</label>
            <input
              type="text" id="username" name="username"
              value={data.username} onChange={handleChange}
              required
              className="border-b border-blue-300 px-2 py-1 rounded-md focus:border-slate-100 focus:outline"
              placeholder="Enter username"
            />
          </div>
          <div className="flex flex-col">
            <label htmlFor="password" className="font-medium mb-1">Password</label>
            <input
              type="password" id="password" name="password"
              value={data.password} onChange={handleChange}
              required
              className="border-b border-blue-300 px-2 py-1 rounded-md focus:border-slate-100 focus:outline"
              placeholder="Enter password"
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-[#009485] hover:bg-[#0d7065] disabled:opacity-60 text-white py-2 rounded-md transition"
          >
            {loading ? "Logging in…" : "Login"}
          </button>
        </form>

        <div className="flex items-center gap-3 my-6">
          <span className="flex-1 h-px bg-gray-200" />
          <span className="text-xs tracking-widest text-gray-400">OR LOGIN WITH</span>
          <span className="flex-1 h-px bg-gray-200" />
        </div>

        <div className="grid grid-cols-2 gap-3">
          <button
            onClick={handleGoogle}
            disabled={oauthLoading}
            className="flex items-center justify-center gap-2 py-3 border-gray-300 border-2 rounded-xl text-sm font-medium transition-all duration-200 disabled:opacity-60"
          >
            <FaGoogle size={13} />
            {oauthLoading ? "…" : "Google"}
          </button>
          <button
            onClick={handleGithub}
            disabled={oauthLoading}
            className="flex items-center justify-center gap-2 py-3 border-gray-300 border-2 rounded-xl text-sm font-medium transition-all duration-200 disabled:opacity-60"
          >
            <FaGithub size={13} />
            {oauthLoading ? "…" : "GitHub"}
          </button>
        </div>

        <p className="text-center mt-6 text-xs font-light">
          Create new account?{" "}
          <Link to="/signup" className="font-medium">Sign up</Link>
        </p>
      </div>
    </div>
  );
};

export default Login;