import { useEffect, useState } from "react";
import RolesForm from "../components/RolesForm.jsx";
import { MdDeleteOutline, MdEdit } from "react-icons/md";
import { FaPlus } from "react-icons/fa";
import { useSelector, useDispatch } from 'react-redux'
import { addRoles, deleteRole, getRoles, updateRoles } from "../redux/slice/roleSlice.jsx";
import { getPermissions } from "../redux/slice/permissionSlice.jsx";
import { getPermissionCategory} from "../redux/slice/permissionCategorySlice.jsx"
import Pagination from "../components/Pagination.jsx";
import Button from "../components/UI/Button.jsx";



const Roles = () => {
  const dispatch = useDispatch();
  const {roles}=useSelector((state)=>state.role)
  const [open, setOpen] = useState(false);
  const [editRole, setEditRole] = useState(null);
  
  const [page, setPage] = useState(1);
  const itemsPerPage = 10;

  const totalPages=Math.ceil(roles.length/itemsPerPage);
  const startIndex = (page-1)*itemsPerPage;
  const paginatedRoles=roles.slice(startIndex,startIndex + itemsPerPage);

  const handlePageChange=(newPage)=>{
    setPage(newPage);
  };

    useEffect(() => {
      dispatch(getRoles());
      dispatch(getPermissions());
      dispatch(getPermissionCategory())
    }, [dispatch]);

    const handleSave = (role) => {
      if (role.id) {
        dispatch(updateRoles({ id: role.id, data: role }));
      } else {
        dispatch(addRoles(role));
      }
      setOpen(false);
      setEditRole(null);
    };
  
    const handleEdit = (role) => {
      setEditRole(role);
      setOpen(true);
    };
  
    const handleDelete = (id) => {
      dispatch(deleteRole(id));
    };
    
  return (
    <div className="p-6 w-full space-y-6 min-h-[90vh] flex flex-col">
      <div className="flex justify-between items-center">
        <h1 className="text-xl font-bold">Roles</h1>
        <Button text={"Add"} icon={<FaPlus/>} onClick={() => {
            setEditRole(null);
            setOpen(true);
          }} design={"btn btn-secondary"}
          />
       
      </div>

      {open && (
        <RolesForm initialData={editRole} onSave={handleSave} onClose={() => setOpen(false)}/>
      )}

      <div className="bg-white rounded-xl shadow overflow-x-auto p-2">
        <table className="min-w-full border border-gray-200">
          <thead className="bg-slate-100">
            <tr>
              <th className="px-4 py-2 border border-gray-200">ID</th>
              <th className="text-start px-4 py-2 border border-gray-200">Role Name</th>
              <th className="text-start px-4 py-2 border border-gray-200">Short Name</th>
              <th className="text-start px-4 py-2 border border-gray-200">Description</th>
              <th className="px-4 py-2 border border-gray-200">Actions</th>
            </tr>
          </thead>
          <tbody>
            {paginatedRoles.map((role) => (
              <tr key={role.id} className="hover:bg-gray-50">
                <td className="text-center border border-gray-200 px-4 py-2">{role.id}</td>
                <td className="border border-gray-200 px-4 py-2">{role.name}</td>
                <td className="border border-gray-200 px-4 py-2">{role.shortname}</td>
                <td className="border border-gray-200 px-4 py-2">{role.description}</td>
                <td className="border border-gray-200 px-4 py-2">
                  <div className="flex justify-center items-center gap-2">
                    <button onClick={() => handleEdit(role)}  className="bg-green-500 text-white p-1 rounded-full text-sm">
                      <MdEdit size={15}/>
                    </button>
                    <button  onClick={() => handleDelete(role.id)}  className="bg-red-500 text-white p-1 rounded-full text-sm">
                      <MdDeleteOutline size={15} />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
            {roles.length === 0 && (
              <tr>
                <td colSpan="5" className="text-center py-6">No roles added</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
      <Pagination page={page} totalPages={totalPages} onPageChange={handlePageChange}/>
    </div>
  );
};

export default Roles;
