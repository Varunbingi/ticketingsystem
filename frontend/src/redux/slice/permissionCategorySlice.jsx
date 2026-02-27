import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import axiosInstance from "../../config/axiosInstance";

 export const addPermissionCategory=createAsyncThunk('/addPermission/',
  async (permissionCategoryData,{rejectWithValue})=>{
    try {
      const res = await axiosInstance.post("/permissioncategory/", permissionCategoryData);
      return res.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || "Server error");
    }
  }
)

export const getPermissionCategory=createAsyncThunk('/addPermissionCategrory/',
  async (_, { rejectWithValue }) => {
    try{
      const res = await axiosInstance.get('/permissioncategory/');
      return res.data;
    }
    catch (error){
      return rejectWithValue(error.response?.data||"Server error");
    }
  }
)

export const deletePermissionCategory=createAsyncThunk('/deletePermissionCategory',
  async (id,{rejectWithValue})=>{
    try{
      await axiosInstance.delete(`/permissioncategory/${id}`);
      return id;
    }
    catch(error){
      return rejectWithValue(error.response?.data||"Server error")
    }
  }
)

const permissionCategorySlice=createSlice({
  name:"permisionCategory",
  initialState:{
    permissionCategories:[],
  },
  reducers:{},
  extraReducers:(builder)=>{
    builder.addCase(addPermissionCategory.fulfilled,(state,action)=>{
      state.permissionCategories.push(action.payload)
    })
    .addCase(getPermissionCategory.fulfilled,(state,action)=>{
      state.permissionCategories=action.payload;
    })
    .addCase(deletePermissionCategory.fulfilled,(state,action)=>{
      state.permissionCategories = state.permissionCategories.filter((p) => p.id !== action.payload);
    })
  }
})

export default permissionCategorySlice.reducer;