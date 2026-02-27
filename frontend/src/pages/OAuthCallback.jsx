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

    if (error) {
      navigate(`/login?oauth_error=${encodeURIComponent(error)}`);
      return;
    }

    if (!token) {
      navigate("/login?oauth_error=no_token");
      return;
    }

    // Save token to Redux + localStorage and go home
    dispatch(saveOAuthToken(token));
    navigate("/");
  }, []);

  return (
    <div className="min-h-screen flex flex-col items-center justify-center gap-4">
      <div className="w-10 h-10 border-4 border-[#009485] border-t-transparent rounded-full animate-spin" />
      <p className="text-gray-500 text-sm capitalize">
        Signing you in with {provider}…
      </p>
    </div>
  );
};

export default OAuthCallback;