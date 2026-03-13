import { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import axiosInstance from "../config/axiosInstance";

const Home = () => {

  const [message, setMessage] = useState("");
  const token = useSelector((state) => state.auth.token);

  useEffect(() => {

    // only run when user logged in
    if (!token) return;

    axiosInstance.get("/auth/test-i18n")
      .then((res) => {
        setMessage(res.data.message);
      })
      .catch((err) => {
        console.error(err);
      });

  }, [token]);

  return(
    <div className="flex flex-col w-full p-4">

      {token ? (
        <h1 className="text-2xl font-bold">{message}</h1>
      ) : (
        <h1 className="text-2xl font-bold">Welcome</h1>
      )}

    </div>
  )
}

export default Home;