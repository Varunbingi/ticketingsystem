import { useEffect, useState } from "react";
import PermissionsForm from "../components/PermissionsForm.jsx";
import { MdDeleteOutline, MdEdit } from "react-icons/md";
import { FaPlus } from "react-icons/fa";
import {useSelector,useDispatch} from 'react-redux'
import { addPermission, getPermissions, updatePermission, deletePermission } from "../redux/slice/permissionSlice.jsx";
import {addPermissionCategory, getPermissionCategory} from "../redux/slice/permissionCategorySlice.jsx"
import PermissionCategoryForm from "../components/PermissionCategoryForm.jsx";
import Pagination from "../components/Pagination.jsx";
import Button from "../components/UI/Button.jsx";


const Permissions = () => {
  const dispatch = useDispatch();
  const {permissions}=useSelector((state)=>state.permission)
  const {permissionCategories}=useSelector((satate)=>satate.permissionCategory)
  
  const [openPermission, setOpenPermission] = useState(false);
  const [openPermissionCategory, setOpenPermissionCategory] = useState(false);
  const [editPermission, setEditPermission] = useState(null);
  const [editPermissionCategory, setEditPermissionCategory] =useState(null);
  const [page, setPage] = useState(1);
  const itemsPerPage = 10;

  const totalPages = Math.ceil(permissions.length/itemsPerPage);
  const startIndex = (page-1)*itemsPerPage;
  const paginatedPermissions =permissions.slice(startIndex,startIndex + itemsPerPage);

  const handlePageChange =(newPage)=>{
    setPage(newPage);
  }
  
  useEffect(() => {
    dispatch(getPermissions());
    dispatch(getPermissionCategory());
  }, [dispatch]);
  
  const handleSave = (permission) => {
    if (permission.id) {
      dispatch(updatePermission({ id: permission.id, data: permission }));
    } else {
      dispatch(addPermission(permission));
    }
    setOpenPermission(false);
    setEditPermission(null);
  };

  const permissionCategorySave=(data)=>{
    dispatch(addPermissionCategory(data))
  }
  
  const handleEdit = (permission) => {
    setEditPermission(permission);
    setOpenPermission(true);
  };

  const handleDelete = (id) => {
    dispatch(deletePermission(id));
  }; 

  return (
    <div className="p-6 w-full space-y-6 min-h-[90vh] flex flex-col">
      <div className="flex justify-between items-center">
        <h1 className="text-xl font-bold">Permissions</h1>
        <div className="flex gap-3">
          <Button text={"Add Permission Category"} icon={<FaPlus/>} onClick={() => {
            setEditPermissionCategory(null);
            setOpenPermissionCategory(true);
          }}design={"btn btn-secondary"}/>
          <Button text={"Add Permission"} icon={<FaPlus/>} onClick={() => {
            setEditPermission(null);
            setOpenPermission(true);
          }} design={"btn btn-secondary"}/>
        </div>
      </div>

      {openPermission && (
        <PermissionsForm initialData={editPermission}  onSave={handleSave}  onClose={() => setOpenPermission(false)}/>
      )}
      {openPermissionCategory && (
        <PermissionCategoryForm initialData={editPermissionCategory} onSave={permissionCategorySave} 
        onClose={()=>setOpenPermissionCategory(false)}/>
      )}

      <div className="bg-white rounded-xl shadow overflow-x-auto p-2">
        <table className="min-w-full border border-gray-200">
          <thead className="bg-slate-100">
            <tr>
              <th className="border border-gray-200 px-4 py-2">ID</th>
              <th className="border border-gray-200 px-4 py-2 text-start">Name</th>
              <th className="border border-gray-200 px-4 py-2 text-start">Description</th>
              <th className="border border-gray-200 px-4 py-2">Actions</th>
            </tr>
          </thead>
          <tbody>
            {paginatedPermissions.map((p) => (
              <tr key={p.id} className="hover:bg-gray-50">
                <td className="text-center border border-gray-200 px-4 py-2">{p.id}</td>
                <td className="border border-gray-200 px-4 py-2">{p.name}</td>
                <td className="border border-gray-200 px-4 py-2">{p.description}</td>
                <td className="border border-gray-200 px-4 py-2">
                  <div className="flex justify-center items-center gap-2">
                    <button  onClick={() => handleEdit(p)}  className="bg-green-500 text-white p-1 rounded-full text-sm">
                      <MdEdit size={15} />
                    </button>
                    <button  onClick={() => handleDelete(p.id)}  className="bg-red-500 text-white p-1 rounded-full text-sm">
                      <MdDeleteOutline size={15} />
                    </button>
                  </div>
                </td>
              </tr>
            ))}

            {permissions.length === 0 && (
              <tr>
                <td colSpan="4" className="text-center py-6"> No permissions added</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
      <Pagination page={page} totalPages={totalPages} onPageChange={handlePageChange}/>
    </div>
  );
};

export default Permissions;
