import { useState } from "react";
import { useSelector } from "react-redux";
import Button from "./UI/Button.jsx";

const RolePermisionsForm = () =>{
    const [data,setData]=useState({
        id:null,
        role:0,
        permission_category:0,
        permissions:0
    }) 
    const handleChange = (e) => {
        setData({...data, [e.target.name]:e.target.value });
    };
    
    const {roles}=useSelector((state)=>state.role)
    const {permissions}=useSelector((state)=>state.permission)
    

    const handleSubmit=(e)=>{
        e.preventDefault();
    }
    return(
        <div className="fixed inset-0 bg-black/40  flex items-center justify-center z-50">
            <form onSubmit={handleSubmit} className="bg-white p-6 rounded-xl shadow w-full max-w-md space-y-3">
                <h2 className="text-xl font-bold text-center">Roles Permission Form</h2>
                <label>Roles</label>
                <select name="role" id="role" onChange={handleChange} className="border p-2 rounded w-full" >
                    {roles.map((role)=>(
                        <option key={role.id} value={role.id}>{role.name}</option>
                    ))}
                </select>
                <label >Permission category</label>
                <select name="permission_category" id="permission_category" onChange={handleChange} className="border p-2 rounded w-full">
                    <option value="no">NA</option>
                </select>
                <label >Permissions</label>
                <select name="permission" id="permission" onChange={handleChange} className="border p-2 rounded w-full">
                    {permissions.map((permission)=>(
                        <option key={permission.id} value={permission.id}>{permission.name}</option>
                    ))}
                </select>
                <div className="flex justify-end gap-3 pt-3">
                    <button  type="button" className="bg-gray-300 px-4 py-1 rounded">
                        Cancel
                    </button>
                    <Button text="Save" onClick={handleSubmit} design={"btn btn-primary "}/>
                </div>
            </form>
        </div>
    )
}

export default RolePermisionsForm; 