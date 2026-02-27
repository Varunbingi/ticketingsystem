import { useEffect, useState } from "react";
import ClientForm from "../../components/ClientForm.jsx";
import { Link } from "react-router-dom";
import { MdDeleteOutline, MdEdit } from "react-icons/md";
import { BiDotsVerticalRounded } from "react-icons/bi";
import { FaPlus } from "react-icons/fa";
import { useDispatch, useSelector } from "react-redux";
import { addClient, getClients, updateClient, deleteClient } from "../../redux/slice/clientSlice.jsx";
import Pagination from "../../components/Pagination.jsx";
import Button from "../../components/UI/Button.jsx";



const Client=()=>{
  const dispatch = useDispatch();
  const { clients } = useSelector((state) => state.client);

  const [open, setOpen] = useState(false);
  const [editClient, setEditClient] = useState(null);
  const [page, setPage] = useState(1);
  const itemsPerPage = 6;

  const totalPages = Math.ceil(clients.length/itemsPerPage);
  const startIndex = (page-1)*itemsPerPage;
  const paginatedClients =clients.slice(startIndex,startIndex + itemsPerPage);

   const handlePageChange = (newPage) => {
    setPage(newPage);
  };

  useEffect(() => {
      dispatch(getClients());
  }, [dispatch]);

  const handleSave = (client) => {
    if (client.id) {
      dispatch(updateClient({ id: client.id, data: client }));
    } else {
      dispatch(addClient(client));
    }
    setOpen(false);
    setEditClient(null);
  };

  const handleEdit = (client) => {
    setEditClient(client);
    setOpen(true);
  };

  const handleDelete = (id) => {
    dispatch(deleteClient(id));
  };


  return (
    <div className="p-6 min-h-[90vh] w-full flex flex-col">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-xl font-bold text-gray-800">Clients</h1>
        <Button text={"Add"} icon={<FaPlus/>} onClick={() => {
            setEditClient(null);
            setOpen(true);
          }} design={"btn btn-secondary"}/>
      </div>
      {open && (
        <ClientForm  initialData={editClient}  onClose={() => {  setOpen(false); setEditClient(null);}}  onSave={handleSave}/>
      )}<div>
        
      </div>
      {clients.length === 0 ? (
        <>
          <p className="text-gray-500">No clients added yet.</p>
        </>
        
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {paginatedClients.map((client) => (
            <div  key={client.id}  className="bg-white border border-gray-200  shadow-md shadow-gray-500/50   transition overflow-hidden" >
              <div className="border-b border-gray-400 shadow-lg   p-2 flex justify-between items-center">
                <h2 className="text-xl font-semibold text-gray-800">{client.name}</h2>
                <div className="relative group">
                  <BiDotsVerticalRounded size={20} className="cursor-pointer" />
                  <div className="absolute right-0 mt-2 w-32 bg-white rounded-md shadow-lg opacity-0 group-hover:opacity-100 transition-opacity z-10">
                    <button onClick={() => handleEdit(client)} className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                      <MdEdit className="inline mr-2" />
                      Edit
                    </button>
                    <button onClick={() => handleDelete(client.id)} className="w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">
                      <MdDeleteOutline className="inline mr-2" />
                      Delete
                    </button>
                  </div>
                </div>
              </div>
              <div className="p-4">
                <p className="text-sm text-gray-600 mt-1">{client.email}</p>
                <p className="text-sm text-gray-600">{client.phone} </p>
                <p className="text-sm text-gray-500 mt-2">{client.address}</p>
                <div className="flex justify-end items-center mt-4">
                  <Link  to={`/client/${client.id}/contracts`}  className="text-white bg-[#009485] text-sm px-3 py-1 rounded-md ">
                  View 
                  </Link>
                </div>
              </div>  
            </div>
          ))}
        </div>
      )}
      <Pagination page={page} totalPages={totalPages} onPageChange={handlePageChange}/>
    </div>
  );
};

export default Client;
