import {createSlice,createAsyncThunk} from "@reduxjs/toolkit";
import axiosInstance from "../../config/axiosInstance.jsx";


export const addPermission=createAsyncThunk("permission/addPermission",async (permissionData,{rejectWithValue})=>{
    try {
      const res = await axiosInstance.post("/permission/", permissionData,);
      return res.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || "Server error");
    }
  }
);
export const getPermissions = createAsyncThunk("/permission/",
  async (_, { rejectWithValue }) => {
    try {
      const res = await axiosInstance.get("/permission/");
      return res.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || "Server error");
    }
  }
);
export const updatePermission = createAsyncThunk("permission/updatePermission",
  async ({ id, data }, { rejectWithValue }) => {
    try {
      const res = await axiosInstance.put(`/permission/${id}`, data);
      return res.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || "Server error");
    }
  }
);


export const deletePermission = createAsyncThunk("permissions/deletePermission",
  async (id, { rejectWithValue }) => {
    try {
      await axiosInstance.delete(`/permission/${id}`); 
      return id;
    } catch (error) {
      return rejectWithValue(error.response?.data || "Server error");
    }
  }
);

const permissionSlice = createSlice({
  name: "permissions",
  initialState: {
    permissions: [],
    loading: false,
    error: null,
  },
  reducers:{},
  extraReducers:(builder)=>{
    builder
      .addCase(addPermission.pending,(state)=>{
        state.loading = true;
        state.error = null;
      })
      .addCase(addPermission.fulfilled, (state, action) => {
        state.loading = false;
        state.permissions.push(action.payload);
      })
      .addCase(addPermission.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(getPermissions.pending,(state)=>{
        state.loading = true;
        state.error = null;
      })
      .addCase(getPermissions.fulfilled, (state, action) => {
        state.loading = false;
        state.permissions = action.payload;
      })
      .addCase(getPermissions.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(updatePermission.fulfilled, (state, action) => {
        const index = state.permissions.findIndex((c) => c.id === action.payload.id);
        if (index !== -1) {
          state.permissions[index] = action.payload;
        }
      })
      .addCase(deletePermission.fulfilled, (state, action) => {
        state.permissions = state.permissions.filter((c) => c.id !== action.payload);
      });
            
  },
});

export default permissionSlice.reducer;
