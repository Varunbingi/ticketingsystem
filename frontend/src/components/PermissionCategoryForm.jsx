import { useEffect, useState } from "react"
import { IoClose } from "react-icons/io5";
import Button from "./UI/Button.jsx";
const emptyPermissioncategory={
    name:"",
    shortname:""
}
const PermissionCategoryForm = ({ initialData, onSave, onClose }) =>{
  const [permsissioncategoryData,setPermissionCategoryData]=useState(emptyPermissioncategory)

  
  useEffect(() => {
    initialData ? setPermissionCategoryData(initialData) : setPermissionCategoryData(emptyPermissioncategory);
  }, [initialData]);

  const handleChange =(e)=>{
    const {name,value}=e.target;
    setPermissionCategoryData({
      ...permsissioncategoryData,
      [name]:value
    })
  }

   const handleSubmit = (e) => {
    e.preventDefault();
    onSave(permsissioncategoryData);
  };
  return(
    <div className="fixed inset-0 bg-black/40  flex items-center justify-center z-50">
      <div className="bg-white w-full max-w-md rounded-xl ">
        <div className="h-14 bg-[#007a6c] text-white px-4 rounded-tl-xl rounded-tr-xl 
        flex items-center justify-between">
          <h2 className="text-xl font-bold text-center">{permsissioncategoryData.id ? "Edit Permission Category" : "Add Permission Category"}</h2>
          <span className="cursor-pointer" onClick={onClose}>
            <IoClose className="text-white text-xl bg-white/20 rounded-full" />
          </span>
        </div>
        <form onSubmit={handleSubmit} className="bg-white p-6 rounded-xl shadow w-full max-w-md space-y-3">
        <input name="name" placeholder="Permission Name" value={permsissioncategoryData.name} onChange={handleChange} className="w-full border-b border-blue-300 px-2 py-1 rounded-md focus:outline-transparent " required />
        <input name="shortname" placeholder="Permission short name" value={permsissioncategoryData.shortname} onChange={handleChange} className="w-full border-b border-blue-300 px-2 py-1 rounded-md focus:outline-transparent " required />
        
        <Button text={initialData ? "Update" : "Save"} onClick={handleSubmit} design={"btn btn-primary "}/>
      </form>
      </div>
      
    </div>
  )
}

export default PermissionCategoryForm;