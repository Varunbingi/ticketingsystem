import { useEffect, useState } from "react";
import ClientContractForm from "../../components/ClientContractForm.jsx";
import { useParams } from "react-router-dom";
import { MdDeleteOutline, MdEdit } from "react-icons/md";
import { FaPlus } from "react-icons/fa";
import { useDispatch, useSelector } from "react-redux";
import { addClientContract, deleteClientContrcact, getClientContract, updateClientContract } from "../../redux/slice/clientContractSlice.jsx";
import { Link } from "react-router-dom";
import Pagination from "../../components/Pagination.jsx";
import Button from "../../components/UI/Button.jsx";

const Contract = () => {
  const { client_id } = useParams();
  const dispatch=useDispatch();
  const { clientContracts } = useSelector((state) => state.clientContract);
 
  const  frequencyOptions = ["Weekly", "Monthly", "Quarterly", "Half-Yearly", "Yearly"];
  const [open, setOpen] = useState(false);
  const [editData, setEditData] = useState(null);
  const [page, setPage] = useState(1);
  const itemsPerPage = 10;

  const totalPages = Math.ceil(clientContracts.length/itemsPerPage);
  const startIndex = (page-1)*itemsPerPage;
  const paginatedContract =clientContracts.slice(startIndex,startIndex + itemsPerPage);

   const handlePageChange = (newPage) => {
    setPage(newPage);
  };


  useEffect(() => {
    dispatch(getClientContract(client_id));
  }, [dispatch, client_id]);

  
  const handleSave = (contract) => {
    if (contract.id) { 
      dispatch(updateClientContract({ id: contract.id, data: contract }));
    } else {
      dispatch(addClientContract({...contract,client_id:client_id})); 
    }
    setOpen(false); 
    setEditData(null);
  };
  
  const handleEdit = (contract) => {
    setEditData(contract);
    setOpen(true);
  };
  
  const handleDelete = (id) => {
    dispatch(deleteClientContrcact(id));
  };

  return (
    <div className="p-6 w-full space-y-6 min-h-[90vh] flex flex-col">
      <div className="flex justify-between items-center">
        <div>
            <h1 className="text-xl font-bold text-gray-800">Contracts</h1>
            <h1 className="text-sm text-gray-800 mt-4" ><Link to='/client'>client</Link> {">"} contract</h1>
        </div>
        
        <Button text={"Add"} icon={<FaPlus/>} onClick={() => {
            setEditData(null);
            setOpen(true);
          }} design={"btn btn-secondary"}/>
      </div>
      {open && (
        <ClientContractForm
          initialData={editData}
          onClose={() => {
            setEditData(null);
            setOpen(false);
          }}
          onSave={handleSave}
        />
      )}
      {paginatedContract.length === 0 ? (
        <p className="text-gray-500">No contracts for this client</p>
      ) : (
        <div className="flex flex-col gap-3">
          {clientContracts.map((c, index) => (
            <div key={c.id} className="flex justify-between items-center bg-white rounded-xl shadow-md p-5 hover:shadow-lg transition flex-wrap gap-3">
              <h2 className="text-lg font-semibold">Contract #{index + 1}</h2>

              <p className="text-sm ">
                Start Date : {c.startdate} 
              </p>
              <p className="text-sm">
                End Date : {c.startdate} 
              </p>  
              <p className="text-sm">
                Hours : {c.hours}
              </p> 
              <p className="text-sm">
                Frequency : {c.frequency? frequencyOptions[c.frequency-1] : "NA"}
              </p>
              <h2 className={`text-sm font-semibold ${ c.status ? "text-green-600" : "text-red-600"}`}>
                {c.status ? "Active" : "Inactive"}
              </h2>
              <div className="flex  gap-2">
                <button onClick={() => handleEdit(c)} className="p-1 bg-green-500 text-white rounded-full hover:bg-green-600 text-sm">
                  <MdEdit size={15} />
                </button>
                <button onClick={() => handleDelete(c.id)} className="p-1 bg-red-500 hover:bg-red-600 text-white rounded-full text-sm">
                  <MdDeleteOutline size={15} />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
      <Pagination page={page} totalPages={totalPages} onPageChange={handlePageChange}/>
    </div>
  );
};

export default Contract;
