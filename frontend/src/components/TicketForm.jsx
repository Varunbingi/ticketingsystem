import { useEffect, useState } from "react";
import { IoClose, IoDocumentAttach } from "react-icons/io5";
import Button from "./UI/Button.jsx";

const emptyForm = {
  id: "",
  priority: "",
  subject: "",
  description: "",
  files: [],
};

const TicketForm = ({ onClose, onSave, initialData }) => {
  const [form, setForm] = useState(emptyForm);

  useEffect(() => {
    if (initialData) {
      setForm({ ...initialData, files: [] }); 
    } else {
      setForm(emptyForm);
    }
  }, [initialData]);

  const handleChange = (e) => {
    const { name, value, files } = e.target;
    if (name === "files") {
      setForm((prev) => ({ ...prev, files: Array.from(files) }));
    } else {
      setForm((prev) => ({ ...prev, [name]: value }));
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave(form);
  };

  return (
    <div className="fixed inset-0 bg-black/40 flex justify-center items-center z-50">
      <div className="bg-white w-full max-w-md rounded-xl ">
        <div className="h-14 bg-[#007a6c] text-white px-4 rounded-tl-xl rounded-tr-xl 
        flex items-center justify-between">
          <h2 className="text-xl font-bold text-center">{initialData ? "Edit Ticket" : "Add Ticket"}</h2>
          <span className="cursor-pointer" onClick={onClose}>
            <IoClose className="text-white text-xl bg-white/20 rounded-full" />
          </span>
        </div>
        <form onSubmit={handleSubmit} className="space-y-3 p-4">
          <select name="priority" value={form.priority} onChange={handleChange} className="w-full border-b border-blue-300 px-2 py-1 rounded-md focus:outline-transparent " required>
            <option value="" disabled>Select Priority</option>
            <option value={0}>Low</option>
            <option value={1}>Medium</option>
            <option value={2}>High</option>
          </select>
          <input type="text" name="subject" placeholder="Subject" value={form.subject} onChange={handleChange} className="w-full border-b border-blue-300 px-2 py-1 rounded-md focus:outline-transparent " required/>
          <input type="text" name="description" placeholder="Description" value={form.description} onChange={handleChange} className="w-full border-b border-blue-300 px-2 py-1 rounded-md focus:outline-transparent "/>
          <label className="flex items-center gap-2">
            <IoDocumentAttach />
            <input type="file" name="files" multiple onChange={handleChange} />
          </label>
          {initialData?.files?.length > 0 && (
            <div className="text-sm text-gray-600">
              Existing files:
              <ul className="list-disc ml-4">
                {initialData.files.map((f, i) => (
                  <li key={i}>
                    <a href={f} target="_blank" rel="noreferrer" className="text-blue-500">
                      File {i + 1}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          )}
          
          <Button text={initialData ? "Update" : "Save"} onClick={handleSubmit} design={"btn btn-primary "}/>
        </form>
      </div>
    </div>
  );
};

export default TicketForm;
