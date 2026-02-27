import { createAsyncThunk, createSlice } from "@reduxjs/toolkit"; 
import axiosInstance from "../../config/axiosInstance";

export const addRolePermission=createAsyncThunk("/addRolePermission",
  async (rolePermissionData,{rejectWithValue})=>{
    try {
      const res = await axiosInstance.post("/rolepermission/", rolePermissionData);
      return res.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || "Server error");
    }
  }
);
export const getRolePermission = createAsyncThunk("/getRolePermission",
  async (_, { rejectWithValue }) => {
    try {
      const res = await axiosInstance.get("/rolePermission/");
      return res.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || "Server error");
    }
  }
);
export const updateRolePermission = createAsyncThunk("/updateRolePermission",
  async ({ id, data }, { rejectWithValue }) => {
    try {
      const res = await axiosInstance.put(`/rolePermission/${id}`, data);
      return res.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || "Server error");
    }
  }
);


export const deleteRolePermission = createAsyncThunk("/deleteRolePermission",
  async (id, { rejectWithValue }) => {
    try {
      await axiosInstance.delete(`/rolePermission/${id}`); 
      return id;
    } catch (error) {
      return rejectWithValue(error.response?.data || "Server error");
    }
  }
);

const rolePermissionSlice=createSlice(
  {
    name:"rolePermission",
    initialState: {
    rolePermission: [],
    loading: false,
    error: null,
  },
  reducers:{},
  extraReducers: (builder) => {
      builder.addCase(addRolePermission.pending, (state) => {
          state.loading = true;
          state.error = null;
        })
        .addCase(addRolePermission.fulfilled, (state, action) => {
          state.loading = false;
          state.rolePermission.push(action.payload);
        })
        .addCase(addRolePermission.rejected, (state, action) => {
          state.loading = false;
          state.error = action.payload;
        })
        .addCase(getRolePermission.pending, (state) => {
          state.loading = true;
          state.error = null;
        })
        .addCase(getRolePermission.fulfilled, (state, action) => {
          state.loading = false;
          state.rolePermission = action.payload;
        })
        .addCase(getRolePermission.rejected, (state, action) => {
          state.loading = false;
          state.error = action.payload;
        })
        .addCase(updateRolePermission.pending, (state) => {
          state.loading = true;
        })
        .addCase(updateRolePermission.fulfilled, (state, action) => {
          state.loading = false;
          const index = state.rolePermission.findIndex(
            (rolepermission) => rolepermission.id === action.payload.id
          );
          if (index !== -1) {
            state.roles[index] = action.payload;
          }
        })
        .addCase(updateRolePermission.rejected, (state, action) => {
          state.loading = false;
          state.error = action.payload;
        })
        .addCase(deleteRolePermission.pending, (state) => {
          state.loading = true;
        })
        .addCase(deleteRolePermission.fulfilled, (state, action) => {
          state.loading = false;
          state.rolePermission = state.rolePermission.filter(
            (rolepermission) => rolepermission.id !== action.payload
          );
        })
        .addCase(deleteRolePermission.rejected, (state, action) => {
          state.loading = false;
          state.error = action.payload;
        });
    },
  }

)

export default rolePermissionSlice.reducer;