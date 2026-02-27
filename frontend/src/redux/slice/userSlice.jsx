import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import axiosInstance from "../../config/axiosInstance";


export const addUsers = createAsyncThunk("/users/addusers",
  async (userData, { rejectWithValue }) => {
    try {
      const res = await axiosInstance.post("/user/create",userData);
      return res.data.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || "Server error");
    }
  }
);

export const getUsers = createAsyncThunk("/users/getusers",
  async (_, { rejectWithValue }) => {
    try {
      const res = await axiosInstance.get("/user?skip=0&limit=20");
      return res.data.users ;
    } catch (error) {
      return rejectWithValue(error.response?.data || "Server error");
    }
  }
);


export const updateUser = createAsyncThunk("/users/updateuser",
  async ({ id, userData }, { rejectWithValue }) => {
    try {
      const res = await axiosInstance.put(`/user/${id}/update`, userData);
      return res.data.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || "Server error");
    }
  }
);

export const deletedUser = createAsyncThunk("/users/deleteUser",
  async (id, { rejectWithValue }) => {
    try {
      await axiosInstance.delete(`/user/${id}/delete`);
      return id;
    } catch (error) {
      return rejectWithValue(error.response?.data || "Server error");
    }
  }
);

const userSlice = createSlice({
  name: "users",
  initialState: {
    users: [],
    loading: false,
    error: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder.addCase(addUsers.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(addUsers.fulfilled, (state, action) => {
        state.loading = false;
        state.users.push(action.payload);
      })
      .addCase(addUsers.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(getUsers.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(getUsers.fulfilled, (state, action) => {
        state.loading = false;
        state.users = action.payload;
      })
      .addCase(getUsers.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(updateUser.pending, (state) => {
        state.loading = true;
      })
      .addCase(updateUser.fulfilled, (state, action) => {
        state.loading = false;
        const index = state.users.findIndex(
          (user) => user.id === action.payload.id
        );
        if (index !== -1) {
          state.users[index] = action.payload;
        }
      })
      .addCase(updateUser.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(deletedUser.pending, (state) => {
        state.loading = true;
      })
      .addCase(deletedUser.fulfilled, (state, action) => {
        state.loading = false;
        state.users = state.users.filter(
          (user) => user.id !== action.payload
        );
      })
      .addCase(deletedUser.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  },
});

export default userSlice.reducer;
