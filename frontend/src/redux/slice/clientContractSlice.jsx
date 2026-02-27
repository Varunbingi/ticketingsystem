import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import axiosInstance from "../../config/axiosInstance.jsx";

export const addClientContract = createAsyncThunk("/client/addClientContract",
  async(contractData, { rejectWithValue }) => {
    try{
      const res = await axiosInstance.post("/contract/",contractData);
      return res.data;
    }catch (error) {
      return rejectWithValue(error.response?.data || "Server error");
    }
  }
);

export const getClientContract = createAsyncThunk("/client/getClientContracts",
  async (id, { rejectWithValue }) => {
    try {
      const res = await axiosInstance.get(`/contract/${id}`);
      return res.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || "Server error");
    }
  }
);


export const updateClientContract = createAsyncThunk("/clients/updateClientContract",
  async ({ id, data }, { rejectWithValue }) => {
    try {
      const res = await axiosInstance.put(`/contract/${id}`, data);
      return res.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || "Server error");
    }
  }
);


export const deleteClientContrcact = createAsyncThunk("/clients/deleteClient",
  async (id, { rejectWithValue }) => {
    try {
      await axiosInstance.delete(`/contract/${id}`); 
      return id;
    } catch (error) {
      return rejectWithValue(error.response?.data || "Server error");
    }
  }
);

const clientContractSlice = createSlice({
  name: "clientContracts",
  initialState: {
    clientContracts: [],
    loading: false,
    error: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(addClientContract.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(addClientContract.fulfilled, (state, action) => {
        state.loading = false;
        state.clientContracts.push(action.payload);
      })
      .addCase(addClientContract.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(getClientContract.pending,(state)=>{
        state.loading = true;
        state.error = null;
      })
      .addCase(getClientContract.fulfilled, (state, action) => {
        state.loading = false;
        state.clientContracts = action.payload;
      })
      .addCase(getClientContract.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(updateClientContract.fulfilled, (state, action) => {
        const index = state.clientContracts.findIndex((c) => c.id === action.payload.id);
        if (index !== -1) {
          state.clientContracts[index] = action.payload;
        }
      })
      .addCase(deleteClientContrcact.fulfilled, (state, action) => {
        state.clientContracts = state.clientContracts.filter((c) => c.id !== action.payload);
      });
  },
});

export default clientContractSlice.reducer;
