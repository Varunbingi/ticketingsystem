import { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { IoClose } from "react-icons/io5";
import Button from "./UI/Button.jsx";

const emptyRole={
  id:null,
  shortname:"",
  name:"",
  description:"",
  permissioncategory:[],
  permission:[]
};

const RolesForm=({ initialData, onSave, onClose }) => {
  const [role, setRole] = useState(emptyRole);
  const {permissionCategories }=useSelector((state)=>state.permissionCategory)
  const {permissions}=useSelector((state)=>state.permission)
  const toggleCheckbox = (name, value) => {
    setRole((prev) => ({
      ...prev,
      [name]: prev[name].includes(value)
        ? prev[name].filter((v) => v !== value)
        : [...prev[name], value]
    }));
  };
  useEffect(() => {
  if(initialData) {
    setRole({
      id: initialData.id ?? null,
      shortname: initialData.shortname ?? "",
      name: initialData.name ?? "",
      description: initialData.description ?? "",
      permissioncategory: Array.isArray(initialData.permissioncategory)
        ? initialData.permissioncategory
        : [],
      permission: Array.isArray(initialData.permission)
        ? initialData.permission
        : []
    });
  } else {
    setRole(emptyRole);
  }
}, [initialData]);

  const handleChange = (e) => {
    setRole({...role, [e.target.name]:e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave(role);
  };

  return (
    <div className="fixed inset-0 bg-black/40  flex items-center justify-center z-50 h-full min-h-screen">
      <form onSubmit={handleSubmit} className="bg-white  rounded-xl shadow w-full max-w-md space-y-3" >
        <div className="h-14 bg-[#007a6c] text-white px-4 rounded-tl-xl rounded-tr-xl 
        flex items-center justify-between">
          <h2 className="text-xl font-bold text-center">{initialData ? "Edit Role" : "Add Role"}</h2>
          <span className="cursor-pointer" onClick={onClose}>
            <IoClose className="text-white text-xl bg-white/20 rounded-full" />
          </span>
        </div>
        <div className="p-4 space-y-3">
          <input name="shortname" placeholder="Short Name" value={role.shortname} onChange={handleChange} className="w-full border-b border-blue-300 px-2 py-1 rounded-md focus:outline-transparent " required />
        <input name="name"  placeholder="Role Name"  value={role.name}  onChange={handleChange}   className="w-full border-b border-blue-300 px-2 py-1 rounded-md focus:outline-transparent " required />
        <textarea name="description"  placeholder="Description"  value={role.description}  onChange={handleChange}  className="w-full border-b border-blue-300 px-2 py-1 rounded-md focus:outline-transparent " required />
       <div className="p-3">
        <p className="font-semibold mb-2">Permission Categories</p>
        <div className="space-y-2 max-h-15  overflow-y-auto">
          {permissionCategories.map(pc => (
            <label key={pc.id} className="flex items-center gap-2">
              <input type="checkbox" checked={role.permissioncategory.includes(pc.id)}  onChange={() => toggleCheckbox("permissioncategory", pc.id)}/>
              <span>{pc.name}</span>
            </label>
          ))}
        </div>
        </div>

        <div className="p-3">
        <p className="font-semibold mb-2">Permissions</p>

        <div className="space-y-2 max-h-15 overflow-y-auto">
          {permissions.map(p => (
            <label key={p.id} className="flex items-center gap-2">
              <input type="checkbox" checked={role.permission.includes(p.id)} onChange={() => toggleCheckbox("permission", p.id)}/>
              <span>{p.name}</span>
            </label>
          ))}
        </div>
        </div>
      
        <Button text="Save" onClick={handleSubmit} design={"btn btn-primary "}/>
        
        </div>
        
      </form>
    </div>
  );
};

export default RolesForm;
