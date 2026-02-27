import {createSlice,createAsyncThunk} from "@reduxjs/toolkit";
import axiosInstance from "../../config/axiosInstance.jsx";


export const addClient=createAsyncThunk("/clients/addClient",async (clientData,{rejectWithValue})=>{
    try {
      const res = await axiosInstance.post("/clients/", clientData);
      return res.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || "Server error");
    }
  }
);
export const getClients = createAsyncThunk("/clients/getclients",
  async (_, { rejectWithValue }) => {
    try {
      const res = await axiosInstance.get("/clients/");
      return res.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || "Server error");
    }
  }
);
export const updateClient = createAsyncThunk("/clients/updateClient",
  async ({ id, data }, { rejectWithValue }) => {
    try {
      const res = await axiosInstance.put(`/clients/${id}`, data);
      return res.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || "Server error");
    }
  }
);


export const deleteClient = createAsyncThunk("/clients/deleteClient",
  async (id, { rejectWithValue }) => {
    try {
      await axiosInstance.delete(`/clients/${id}`); 
      return id;
    } catch (error) {
      return rejectWithValue(error.response?.data || "Server error");
    }
  }
);

const clientSlice = createSlice({
  name: "clients",
  initialState: {
    clients: [],
    loading: false,
    error: null,
  },
  reducers:{},
  extraReducers:(builder)=>{
    builder
      .addCase(addClient.pending,(state)=>{
        state.loading = true;
        state.error = null;
      })
      .addCase(addClient.fulfilled, (state, action) => {
        state.loading = false;
        state.clients.unshift(action.payload);
      })
      .addCase(addClient.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(getClients.pending,(state)=>{
        state.loading = true;
        state.error = null;
      })
      .addCase(getClients.fulfilled, (state, action) => {
        state.loading = false;
        state.clients = action.payload;
      })
      .addCase(getClients.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(updateClient.fulfilled, (state, action) => {
        const index = state.clients.findIndex((c) => c.id === action.payload.id);
        if (index !== -1) {
          state.clients[index] = action.payload;
        }
      })
      .addCase(deleteClient.fulfilled, (state, action) => {
        state.clients = state.clients.filter((c) => c.id !== action.payload);
      });
            
  },
});

export default clientSlice.reducer;
