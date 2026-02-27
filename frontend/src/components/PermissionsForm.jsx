import { useEffect, useState } from "react";
import { IoClose } from "react-icons/io5";
import { useSelector } from "react-redux";
import Button from "./UI/Button.jsx";

const emptyPermission = {
  permission_category_id: "",
  name: "",
  shortname: "",
  description: "",
};

const PermissionsForm = ({ initialData, onSave, onClose }) => {
  const [form, setForm] = useState(emptyPermission);
  const {permissionCategories }=useSelector((state)=>state.permissionCategory)

  useEffect(() => {
    initialData ? setForm(initialData) : setForm(emptyPermission);
  }, [initialData]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({...prev,
      [name]:name === "permission_category_id"?value === "" ? "" : Number(value): value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave({...form,permission_category_id: Number(form.permission_category_id),});
  };

  return (
    <div className="fixed inset-0 bg-black/40  flex items-center justify-center z-50">
      <div className="bg-white w-full max-w-md rounded-xl ">
        <div className="h-14 bg-[#007a6c] text-white px-4 rounded-tl-xl rounded-tr-xl 
        flex items-center justify-between">
          <h2 className="text-xl font-bold text-center">{form.id ? "Edit Permission" : "Add Permission"}</h2>
          <span className="cursor-pointer" onClick={onClose}>
            <IoClose className="text-white text-xl bg-white/20 rounded-full" />
          </span>
        </div>
        <form onSubmit={handleSubmit} className="bg-white p-6 rounded-xl shadow w-full max-w-md space-y-3">
       
       <select name="permission_category_id" id="permission_category_id" onChange={handleChange} className="w-full border-b border-blue-300 px-2 py-1 rounded-md focus:outline-transparent " value={form.permission_category_id} > 
          <option value="" disabled>
            Select Permission Category
          </option>
          {permissionCategories.map((p)=>(
              <option key={p.id} value={p.id}>{p.name}</option>
          ))}
        </select>
        <input name="name" placeholder="Permission Name" value={form.name} onChange={handleChange} className="w-full border-b border-blue-300 px-2 py-1 rounded-md focus:outline-transparent " required />
        <input name="shortname" placeholder="Permission short name" value={form.shortname} onChange={handleChange} className="w-full border-b border-blue-300 px-2 py-1 rounded-md focus:outline-transparent " required />
        <textarea name="description" placeholder="Description" value={form.description} onChange={handleChange} className="w-full border-b border-blue-300 px-2 py-1 rounded-md focus:outline-transparent " required/>
        
        <Button text={initialData ? "Update" : "Save"} onClick={handleSubmit} design={"btn btn-primary "}/>
        
      </form>
      </div>
      
    </div>
  );
};

export default PermissionsForm;
