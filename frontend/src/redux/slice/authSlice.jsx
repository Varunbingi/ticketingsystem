import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import axiosInstance from "../../config/axiosInstance";

export const signup = createAsyncThunk("auth/signup",
  async (formData, { rejectWithValue }) => {
    try {
      const res = await axiosInstance.post("/auth/create", formData);
      return res.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || "Server error");
    }
  }
);

export const login = createAsyncThunk("auth/login",
  async (loginData, { rejectWithValue }) => {
    try {
      const form = new URLSearchParams();
      form.append("username", loginData.username);
      form.append("password", loginData.password);
      const res = await axiosInstance.post("/auth/token", form, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
      });
      return res.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || "Server error");
    }
  }
);

export const oauthgoogle = createAsyncThunk("auth/oauthgoogle",
  async (_, { rejectWithValue }) => {
    try {
      const res = await axiosInstance.get("/auth/google/login");
      return res.data; 
    } catch (error) {
      return rejectWithValue(error.response?.data || "Server error");
    }
  }
);

export const oauthgithub = createAsyncThunk("auth/oauthgithub",
  async (_, { rejectWithValue }) => {
    try {
      const res = await axiosInstance.get("/auth/github/login");
      return res.data; 
    } catch (error) {
      return rejectWithValue(error.response?.data || "Server error");
    }
  }
);


export const handleOAuthCallback = createAsyncThunk("auth/oauthCallback",
  async ({ provider, code }, { rejectWithValue }) => {
    try {
      const res = await axiosInstance.get(`/auth/${provider}/callback?code=${code}`);
      return res.data; 
    } catch (error) {
      return rejectWithValue(error.response?.data || "OAuth callback failed");
    }
  }
);

const authSlice = createSlice({
  name: "auth",
  initialState: {
    loading: false,
    oauthLoading: false,
    auth: null,
    isLogin: !!localStorage.getItem("token"),
    token: localStorage.getItem("token") || null,
    error: null,
  },
  reducers: {
    logout: (state) => {
      state.token = null;
      state.auth = null;
      state.isLogin = false;
      state.error = null;
      localStorage.removeItem("isLogin");
      localStorage.removeItem("token");
    },
    clearError: (state) => {
      state.error = null;
    },
    saveOAuthToken: (state, action) => {
      state.token = action.payload;
      state.isLogin = true;
      state.error = null;
      localStorage.setItem("token", action.payload);
      localStorage.setItem("isLogin", "true");
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(signup.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(signup.fulfilled, (state) => {
        state.loading = false;
      })
      .addCase(signup.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(login.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(login.fulfilled, (state, action) => {
        state.loading = false;
        state.isLogin = true;
        state.token = action.payload.access_token;
        localStorage.setItem("isLogin", "true");
        localStorage.setItem("token", action.payload.access_token);
      })
      .addCase(login.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })

      // ── OAuth Google ──
      .addCase(oauthgoogle.pending, (state) => {
        state.oauthLoading = true;
        state.error = null;
      })
      .addCase(oauthgoogle.fulfilled, (state) => {
        state.oauthLoading = false;
        // Redirect URL is handled in the component — no state needed
      })
      .addCase(oauthgoogle.rejected, (state, action) => {
        state.oauthLoading = false;
        state.error = action.payload;
      })

      // ── OAuth GitHub ──
      .addCase(oauthgithub.pending, (state) => {
        state.oauthLoading = true;
        state.error = null;
      })
      .addCase(oauthgithub.fulfilled, (state) => {
        state.oauthLoading = false;
      })
      .addCase(oauthgithub.rejected, (state, action) => {
        state.oauthLoading = false;
        state.error = action.payload;
      })
      .addCase(handleOAuthCallback.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(handleOAuthCallback.fulfilled, (state, action) => {
        state.loading = false;
        state.isLogin = true;
        state.token = action.payload.access_token;
        localStorage.setItem("isLogin", "true");
        localStorage.setItem("token", action.payload.access_token);
      })
      .addCase(handleOAuthCallback.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  },
});

export const { logout, clearError, saveOAuthToken } = authSlice.actions;
export default authSlice.reducer;