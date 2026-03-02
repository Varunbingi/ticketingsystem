import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import axiosInstance from "../../config/axiosInstance";


export const fetchUnreadCount = createAsyncThunk(
  "notifications/fetchUnreadCount",
  async (_, { rejectWithValue }) => {
    try {
      const response = await axiosInstance.get("/notifications/");

      const unread = response.data.filter((n) => !n.read_status).length;
      return unread;
    } catch (err) {
      return rejectWithValue(err.response.data);
    }
  }
);

const notificationSlice = createSlice({
  name: "notifications",
  initialState: {
    unreadCount: 0,
    status: "idle",
  },
  reducers: {

    decrementCount: (state) => {
      state.unreadCount = Math.max(0, state.unreadCount - 1);
    }
  },
  extraReducers: (builder) => {
    builder.addCase(fetchUnreadCount.fulfilled, (state, action) => {
      state.unreadCount = action.payload;
      state.status = "succeeded";
    });
  },
});

export const { decrementCount } = notificationSlice.actions;
export default notificationSlice.reducer;