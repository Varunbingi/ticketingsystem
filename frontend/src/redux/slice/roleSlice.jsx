import { createAsyncThunk, createSlice } from "@reduxjs/toolkit"; 
import axiosInstance from "../../config/axiosInstance";

export const addRoles=createAsyncThunk("role/addRole",
  async (roleData,{rejectWithValue})=>{
    try {
      const res = await axiosInstance.post("/role/", roleData);
      return res.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || "Server error");
    }
  }
);
export const getRoles = createAsyncThunk("/role/getRole",
  async (_, { rejectWithValue }) => {
    try {
      const res = await axiosInstance.get("/role/");
      return res.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || "Server error");
    }
  }
);
export const updateRoles = createAsyncThunk("/role/updateRole",
  async ({ id, data }, { rejectWithValue }) => {
    try {
      const res = await axiosInstance.put(`/role/${id}`, data);
      return res.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || "Server error");
    }
  }
);


export const deleteRole = createAsyncThunk("/role/deleteRole",
  async (id, { rejectWithValue }) => {
    try {
      await axiosInstance.delete(`/role/${id}`); 
      return id;
    } catch (error) {
      return rejectWithValue(error.response?.data || "Server error");
    }
  }
);

const roleSlice=createSlice(
  {
    name:"roles",
    initialState: {
    roles: [],
    loading: false,
    error: null,
  },
  reducers:{},
  extraReducers: (builder) => {
      builder.addCase(addRoles.pending, (state) => {
          state.loading = true;
          state.error = null;
        })
        .addCase(addRoles.fulfilled, (state, action) => {
          state.loading = false;
          state.roles.push(action.payload);
        })
        .addCase(addRoles.rejected, (state, action) => {
          state.loading = false;
          state.error = action.payload;
        })
        .addCase(getRoles.pending, (state) => {
          state.loading = true;
          state.error = null;
        })
        .addCase(getRoles.fulfilled, (state, action) => {
          state.loading = false;
          state.roles = action.payload;
        })
        .addCase(getRoles.rejected, (state, action) => {
          state.loading = false;
          state.error = action.payload;
        })
        .addCase(updateRoles.pending, (state) => {
          state.loading = true;
        })
        .addCase(updateRoles.fulfilled, (state, action) => {
          state.loading = false;
          const index = state.roles.findIndex(
            (role) => role.id === action.payload.id
          );
          if (index !== -1) {
            state.roles[index] = action.payload;
          }
        })
        .addCase(updateRoles.rejected, (state, action) => {
          state.loading = false;
          state.error = action.payload;
        })
        .addCase(deleteRole.pending, (state) => {
          state.loading = true;
        })
        .addCase(deleteRole.fulfilled, (state, action) => {
          state.loading = false;
          state.roles = state.roles.filter(
            (role) => role.id !== action.payload
          );
        })
        .addCase(deleteRole.rejected, (state, action) => {
          state.loading = false;
          state.error = action.payload;
        });
    },
  }

)

export default roleSlice.reducer;