import { useEffect, useRef } from "react";
import { useParams, useSearchParams, useNavigate } from "react-router-dom";
import { useDispatch } from "react-redux";
import { saveOAuthToken } from "../redux/slice/authSlice.jsx";

const OAuthCallback = () => {
  const { provider } = useParams();
  const [searchParams] = useSearchParams();
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const called = useRef(false);

  useEffect(() => {
    if (called.current) return;
    called.current = true;

    const token = searchParams.get("token");
    const error = searchParams.get("error");

    // Handle OAuth error
    if (error) {
      navigate(`/login?oauth_error=${encodeURIComponent(error)}`);
      return;
    }

    // No token returned
    if (!token) {
      navigate("/login?oauth_error=no_token");
      return;
    }

    try {
      // Save token in Redux + localStorage
      dispatch(saveOAuthToken(token));

      // Redirect to home
      navigate("/");
    } catch (err) {
      console.error("OAuth callback error:", err);
      navigate("/login?oauth_error=callback_failed");
    }
  }, [dispatch, navigate, searchParams]);

  return (
    <div className="min-h-screen flex flex-col items-center justify-center gap-4">
      <div className="w-10 h-10 border-4 border-[#009485] border-t-transparent rounded-full animate-spin" />

      <p className="text-gray-500 text-sm capitalize">
        Signing you in with {provider || "OAuth"}…
      </p>
    </div>
  );
};

export default OAuthCallback;