import { useState, useEffect } from "react";
import { IoClose } from "react-icons/io5";
import Button from  "./UI/Button.jsx"
const emptyForm = {
  idnumber: null,
  name: "",
  email: "",
  phone: "",
  address: "",
  startdate: "",
  enddate: "",
};

const ClientForm = ({ onClose, onSave, initialData }) => {
  const [form, setForm] = useState(emptyForm);

  useEffect(() => {
    if (initialData) setForm(initialData);
    else setForm(emptyForm);
  }, [initialData]);

  const handleChange = (e) => {
    const { name, value, type } = e.target;
    setForm({
      ...form,
      [name]: type === "number" ? Number(value) : value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave(form);
  };

  return (
    <div className="fixed inset-0 bg-black/40  flex justify-center items-center z-50">
      <div className="bg-white w-full max-w-md rounded-xl shadow-xl ">
        <div className="h-14 bg-[#007a6c] text-white px-4 rounded-tl-xl rounded-tr-xl 
        flex items-center justify-between">
          <h2 className="text-xl font-bold text-center">{initialData ? "Edit Client" : "Add Client"}</h2>
          <span className="cursor-pointer" onClick={onClose}>
            <IoClose className="text-white text-xl bg-white/20 rounded-full" />
          </span>
        </div>
        <form onSubmit={handleSubmit} className="space-y-3 p-4">
          <input name="idnumber" type="number" placeholder="ID Number" value={form.idnumber} onChange={handleChange} className="w-full border-b border-blue-300 px-2 py-1 rounded-md  focus:outline-transparent" required/>
          <input name="name" placeholder="Client Name" value={form.name} onChange={handleChange} className="w-full border-b border-blue-300 px-2 py-1 rounded-md focus:outline-transparent" required/>
          <input name="email" placeholder="Email" value={form.email} onChange={handleChange} className="w-full border-b border-blue-300 px-2 py-1 rounded-md focus:outline-transparent"  required/>
          <input name="phone" placeholder="Phone" value={form.phone} onChange={handleChange} className="w-full border-b border-blue-300 px-2 py-1 rounded-md focus:outline-transparent" required/>
          <textarea name="address" placeholder="Address" value={form.address} onChange={handleChange} className="w-full border-b border-blue-300 px-2 py-1 rounded-md focus:outline-transparent "  required/>
          <div className="flex gap-2">
            <input type="date" name="startdate" value={form.startdate} onChange={handleChange} placeholder="Start Date" className="w-full  border-b border-blue-300 px-2 py-1 rounded-md focus:outline-transparent" required/>
            <input type="date" name="enddate" value={form.enddate} onChange={handleChange} placeholder="End Date" className="w-full border-b border-blue-300 px-2 py-1 rounded-md focus:outline-transparent " required/>
          </div>
          <Button text={initialData ? "Update" : "Save"} onClick={handleSubmit} design={"btn btn-primary "}/>
        </form>
      </div>
    </div>
  );
};

export default ClientForm;
