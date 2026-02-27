import { createAsyncThunk, createSlice } from "@reduxjs/toolkit"
import axiosInstance from "../../config/axiosInstance"
import { buildTicketFormData } from "../../utils/ticketFormData.js";


export const addTicket=createAsyncThunk("ticket/addticket",
  async(data,{rejectWithValue})=>{
    try{
      const formData = buildTicketFormData(data);
      const res = await axiosInstance.post("/ticket/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      return res.data;
    } catch (error) {
      return rejectWithValue(error.response?.data || "Server error");
    }

  }
)

export const getTickets=createAsyncThunk("tickets/getalltickets",
  async(_,{rejectWithValue})=>{
    try{
      const res=await axiosInstance.get('/ticket/')
      return res.data;
    }
    catch (error) {
      return rejectWithValue(error.response?.data || "Server error");
    }
  }
)
export const getTicketById=createAsyncThunk("tickets/getticketbyid",
  async(id,{rejectWithValue})=>{
    try{
      const res=await axiosInstance.get(`/ticket/${id}`)
      return res.data;
    }
    catch (error) {
      return rejectWithValue(error.response?.data || "Server error");
    }
  }
)

export const updateTicket= createAsyncThunk("tickets/updateticket",
  async({ id, data },{rejectWithValue})=>{
    try{
      const formData = buildTicketFormData(data);
      const res = await axiosInstance.put(`/ticket/${id}`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      return res.data
    }
    catch (error) {
      return rejectWithValue(error.response?.data || "Server error");
    }

  }

)
export const deleteTicket= createAsyncThunk("tickets/deleteticket",
  async(id,{rejectWithValue})=>{
    try{
      const res=await axiosInstance.delete(`/ticket/${id}`)
      return res.data;
    }
      catch (error) {
      return rejectWithValue(error.response?.data || "Server error");
    }
  }
)
const ticketSlice=createSlice(
   {
      name:"tickets",
      initialState: {
      tickets: [],
      selectedTicket: null,
      loading: false,
      error: null,
    },
    reducers:{},
    extraReducers: (builder) => {
      builder.addCase(addTicket.pending,(state,action)=>{
        state.loading=true;
      })
      .addCase(addTicket.fulfilled,(state,action)=>{
        state.loading=false;
        state.tickets.push(action.payload);
      })
      .addCase(addTicket.rejected,(state,action)=>{
        state.error=action.payload;
        state.loading=false;
      })
      .addCase(getTickets.fulfilled,(state,action)=>{
        state.tickets=action.payload;
      })
      .addCase(getTicketById.fulfilled,(state,action)=>{
        state.selectedTicket=action.payload;
      })
      .addCase(updateTicket.fulfilled,(state,action)=>{
        state.loading = false;
        const index = state.tickets.findIndex(
          (ticket) => ticket.id === action.payload.id
        );
        if (index !== -1) {
          state.tickets[index] = action.payload;
        }
      })
      .addCase(deleteTicket.fulfilled,(state, action)=>{
        state.loading = false;
        state.tickets = state.tickets.filter(
          (ticket) => ticket.id !== action.payload
        );
      })
    }
    }
)


export default ticketSlice.reducer;