import { useEffect, useState } from "react";
import { IoClose, IoDocumentAttach } from "react-icons/io5";
import Button from "./UI/Button.jsx";
const emptyForm = {
  id: null,
  client_id: "",
  startdate: "",
  enddate: "",
  hours: "",
  frequency: "",
  status: true,
  attachment:""
};

const ClientContractForm = ({ onClose, initialData, onSave }) => {
  const [form, setForm] = useState(emptyForm);

  useEffect(() => {
    setForm(initialData || emptyForm);
  }, [initialData]);

  const handleChange = (e) => {
    const { name, type, value, checked } = e.target;
    setForm((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave(form);
  };

  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50 h-full min-h-screen">
      <div className="bg-white w-full max-w-md rounded-xl ">
        <div className="h-14 bg-[#007a6c] text-white px-4 rounded-tl-xl rounded-tr-xl
        flex items-center justify-between">
          <h2 className="text-xl font-bold text-center">{form.id ? "Edit Contract" : "Add Contract"}</h2>
          <span className="cursor-pointer" onClick={onClose}>
            <IoClose className="text-white text-xl bg-white/20 rounded-full" />
          </span>
        </div>
        <form onSubmit={handleSubmit} className="bg-white p-6 rounded-xl shadow w-full max-w-md space-y-3">
          <label>Start Date</label>
          <input type="date" name="startdate" value={form.startdate} onChange={handleChange} placeholder="Start Date" className="w-full border-b border-blue-300 px-2 py-1 rounded-md focus:outline-transparent " required />
          <label >End Date</label>
          <input type="date" name="enddate" value={form.enddate}  onChange={handleChange} placeholder="End Date" className="w-full border-b border-blue-300 px-2 py-1 rounded-md focus:outline-transparent " required/>
          <label >Hours</label>
          <input type="number" name="hours" placeholder="Hours" value={form.hours} onChange={handleChange} className="w-full border-b border-blue-300 px-2 py-1 rounded-md focus:outline-transparent " required/>
          <label > Frequency</label>
          <select name="frequency" value={form.frequency} onChange={handleChange} required className="w-full border-b border-blue-300 px-2 py-1 rounded-md focus:outline-transparent">
            <option value={0}>NA</option>
            <option value={1}>Weekly</option>
            <option value={2}>Monthly</option>
            <option value={3}>Quarterly</option>
            <option value={4}>Half-Yearly</option>
            <option value={5}>Yearly</option>
          </select>
          <span>Attachment <IoDocumentAttach/></span>
          <input type="file" accept=".png" />
          <label className="flex items-center gap-2">
            <input type="checkbox" name="status" checked={form.status} onChange={handleChange}/>
            Active
          </label>
          
          <Button text={initialData ? "Update" : "Save"} onClick={handleSubmit} design={"btn btn-primary "}/>
          
      </form>
      </div>
      
    </div>
  );
};

export default ClientContractForm;
