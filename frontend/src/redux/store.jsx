import { configureStore } from "@reduxjs/toolkit";
import clientReducer from "./slice/clientSlice.jsx";
import clientContractReducer from "./slice/clientContractSlice.jsx"
import authReducer from './slice/authSlice.jsx'
import userReducer from "./slice/userSlice.jsx"
import roleReducer from "./slice/roleSlice.jsx"
import permissionReducer from './slice/permissionSlice.jsx'
import permissionCategoryReducer from './slice/permissionCategorySlice.jsx'
import rolePermissionReducer from './slice/rolePermissionSlice.jsx'
import ticketReducer from './slice/ticketSlice.jsx'



const store=configureStore({
    reducer:{
        client:clientReducer,
        clientContract:clientContractReducer,
        user:userReducer,
        auth:authReducer,
        role:roleReducer,
        permission:permissionReducer,
        permissionCategory:permissionCategoryReducer,
        rolePermission:rolePermissionReducer,
        ticket:ticketReducer,
        
    }
})

export default store;