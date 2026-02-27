import { useState, useEffect } from "react";
import { IoClose } from "react-icons/io5";
import Button from "./UI/Button.jsx";

const UserForm = ({ onClose, onSave, initialData }) => {
  const isEditMode = Boolean(initialData);

  const [form, setForm] = useState({
    id: null,
    username: "",
    firstname: "",
    lastname: "",
    email: "",
    password: "",
    phone: "",
    department_id: "",
    designation: "",
    reporting_to_id: "",
    suspended: false,
    deleted: false,
    is_client: false,
  });

  useEffect(() => {
    if (initialData) {
      setForm({ ...initialData }); 
    }
  }, [initialData]);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setForm({
      ...form,
      [name]: type === "checkbox" ? checked : value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    const formattedData = {
      ...form,
      department_id: Number(form.department_id),
      reporting_to_id: Number(form.reporting_to_id),
    };

    onSave(formattedData);
  };

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black/30 z-50">
      <div className="bg-white w-full max-w-3xl rounded-xl shadow-lg">
        <div className="h-14 bg-[#007a6c] text-white px-4 flex items-center justify-between rounded-t-xl">
          <h2 className="text-lg font-bold">
            {isEditMode ? "Edit User" : "Add User"}
          </h2>
          <IoClose  className="cursor-pointer text-white text-xl bg-white/20 rounded-full"  onClick={onClose}/>
        </div>
        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {!isEditMode && (
              <>
                <input  name="username"  value={form.username}  onChange={handleChange}placeholder="Username" required className="w-full border-b border-blue-300 px-2 py-1 rounded-md focus:outline-transparent " />
                <input type="password" name="password" value={form.password} onChange={handleChange} placeholder="Password" required className="w-full border-b border-blue-300 px-2 py-1 rounded-md focus:outline-transparent " />
              </>
            )}
            <input name="firstname" value={form.firstname} onChange={handleChange} placeholder="First Name" required className="w-full border-b border-blue-300 px-2 py-1 rounded-md focus:outline-transparent "/>
            <input name="lastname" value={form.lastname} onChange={handleChange} placeholder="Last Name" required className="w-full border-b border-blue-300 px-2 py-1 rounded-md focus:outline-transparent "/>
            <input type="email" name="email" value={form.email} onChange={handleChange} placeholder="Email" required className="w-full border-b border-blue-300 px-2 py-1 rounded-md focus:outline-transparent "/>
            <input name="phone" value={form.phone} onChange={handleChange} placeholder="Phone" className="w-full border-b border-blue-300 px-2 py-1 rounded-md focus:outline-transparent "/>
            <input type="number" name="department_id" value={form.department_id} onChange={handleChange} placeholder="Department ID" className="w-full border-b border-blue-300 px-2 py-1 rounded-md focus:outline-transparent "/>
            <input type="number" name="reporting_to_id" value={form.reporting_to_id} onChange={handleChange} placeholder="Reporting To (User ID)" className="w-full border-b border-blue-300 px-2 py-1 rounded-md focus:outline-transparent "/>
            <input name="designation" value={form.designation} onChange={handleChange} placeholder="Designation" className="w-full border-b border-blue-300 px-2 py-1 rounded-md focus:outline-transparent "/>
          </div>
          <div className="flex gap-6 pt-2">
            <label className="flex items-center gap-2">
              <input type="checkbox" name="suspended" checked={form.suspended} onChange={handleChange} />
              Suspended
            </label>
            <label className="flex items-center gap-2">
              <input type="checkbox" name="deleted" checked={form.deleted} onChange={handleChange}/>
              Deleted
            </label>
            <label className="flex items-center gap-2">
              <input type="checkbox" name="is_client" checked={form.is_client} onChange={handleChange}/>
              Client
            </label>
          </div>

          <Button text="Save" onClick={handleSubmit} design={"btn btn-primary "}/>
        </form>
      </div>
    </div>
  );
};

export default UserForm;
