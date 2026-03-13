import { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { Link, useNavigate } from "react-router-dom";
import { signup, oauthgoogle, oauthgithub, clearError } from "../redux/slice/authSlice.jsx";
import { FaArrowLeftLong } from "react-icons/fa6";
import { FaGoogle, FaGithub } from "react-icons/fa";
import { useTranslation } from "react-i18next";

const SignUp = () => {

  const { t } = useTranslation();

  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { loading, oauthLoading, error } = useSelector((state) => state.auth);

  const [form, setForm] = useState({
    username: "",
    password: "",
    firstname: "",
    lastname: "",
    email: "",
    phone: "",
    department_id: "",
    designation: "",
    reporting_to: "",
    suspended: false,
    deleted: false,
    is_client: false,
  });

  const handleChange = (e) => {
    dispatch(clearError());
    const { name, value, type, checked } = e.target;
    setForm({ ...form, [name]: type === "checkbox" ? checked : value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await dispatch(signup(form)).unwrap();
      navigate("/login");
    } catch (err) {
      console.error("Signup error:", err);
    }
  };

  const handleGoogle = async () => {
    const result = await dispatch(oauthgoogle());
    if (result.meta.requestStatus === "fulfilled") {
      const url = result.payload;
      if (url) window.location.href = url;
    }
  };

  const handleGithub = async () => {
    const result = await dispatch(oauthgithub());
    if (result.meta.requestStatus === "fulfilled") {
      const url = result.payload;
      if (url) window.location.href = url;
    }
  };

  const errorMessage =
    typeof error === "string"
      ? error
      : error?.detail || error?.message || null;

  return (
    <div className="min-h-screen flex items-center justify-center bg-black/10 p-4">
      <div className="bg-white shadow-lg rounded-xl p-8 w-full max-w-lg">

        <Link to="/">
          <FaArrowLeftLong />
        </Link>

        <h1 className="text-3xl font-bold text-center mb-6">
          {t("signup")}
        </h1>

        {errorMessage && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 text-red-600 text-sm rounded-md">
            {errorMessage}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">

            <input
              type="text"
              name="username"
              value={form.username}
              onChange={handleChange}
              placeholder={t("username")}
              required
              className="border-b border-blue-300 px-2 py-1 rounded-md focus:border-slate-100 focus:outline"
            />

            <input
              type="password"
              name="password"
              value={form.password}
              onChange={handleChange}
              placeholder={t("password")}
              required
              className="border-b border-blue-300 px-2 py-1 rounded-md focus:border-slate-100 focus:outline"
            />

            <input
              type="text"
              name="firstname"
              value={form.firstname}
              onChange={handleChange}
              placeholder={t("firstname")}
              required
              className="border-b border-blue-300 px-2 py-1 rounded-md focus:border-slate-100 focus:outline"
            />

            <input
              type="text"
              name="lastname"
              value={form.lastname}
              onChange={handleChange}
              placeholder={t("lastname")}
              required
              className="border-b border-blue-300 px-2 py-1 rounded-md focus:border-slate-100 focus:outline"
            />

            <input
              type="email"
              name="email"
              value={form.email}
              onChange={handleChange}
              placeholder={t("email")}
              required
              className="border-b border-blue-300 px-2 py-1 rounded-md focus:border-slate-100 focus:outline"
            />

            <input
              type="text"
              name="phone"
              value={form.phone}
              onChange={handleChange}
              placeholder={t("phone")}
              required
              className="border-b border-blue-300 px-2 py-1 rounded-md focus:border-slate-100 focus:outline"
            />

            <input
              type="number"
              name="department_id"
              min={0}
              value={form.department_id}
              onChange={handleChange}
              placeholder={t("department")}
              className="border-b border-blue-300 px-2 py-1 rounded-md focus:border-slate-100 focus:outline"
            />

            <input
              type="number"
              name="reporting_to"
              min={0}
              value={form.reporting_to}
              onChange={handleChange}
              placeholder={t("reporting_to")}
              className="border-b border-blue-300 px-2 py-1 rounded-md focus:border-slate-100 focus:outline"
            />

          </div>

          <div className="flex gap-4 items-center">

            <label className="flex items-center gap-2">
              <input type="checkbox" name="suspended" checked={form.suspended} onChange={handleChange}/>
              {t("suspended")}
            </label>

            <label className="flex items-center gap-2">
              <input type="checkbox" name="deleted" checked={form.deleted} onChange={handleChange}/>
              {t("deleted")}
            </label>

            <label className="flex items-center gap-2">
              <input type="checkbox" name="is_client" checked={form.is_client} onChange={handleChange}/>
              {t("client")}
            </label>

          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-[#009485] hover:bg-[#0d7065] disabled:opacity-60 text-white py-2 rounded-md transition"
          >
            {loading ? t("creating_account") : t("signup")}
          </button>

        </form>

        <div className="flex items-center gap-3 my-6">
          <span className="flex-1 h-px bg-gray-200" />
          <span className="text-xs tracking-widest text-gray-400">
            {t("or_signup_with")}
          </span>
          <span className="flex-1 h-px bg-gray-200" />
        </div>

        <div className="grid grid-cols-2 gap-3">

          <button
            onClick={handleGoogle}
            disabled={oauthLoading}
            className="flex items-center justify-center gap-2 py-3 border-gray-300 border-2 rounded-xl text-sm font-medium transition-all duration-200 disabled:opacity-60"
          >
            <FaGoogle size={13}/>
            {oauthLoading ? "…" : "Google"}
          </button>

          <button
            onClick={handleGithub}
            disabled={oauthLoading}
            className="flex items-center justify-center gap-2 py-3 border-gray-300 border-2 rounded-xl text-sm font-medium transition-all duration-200 disabled:opacity-60"
          >
            <FaGithub size={13}/>
            {oauthLoading ? "…" : "GitHub"}
          </button>

        </div>

        <p className="text-center mt-6 text-xs font-light">
          {t("already_have_account")}{" "}
          <Link to="/login" className="font-medium">
            {t("login")}
          </Link>
        </p>

      </div>
    </div>
  );
};

export default SignUp;