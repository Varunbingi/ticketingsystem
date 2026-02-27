import { useEffect, useState } from "react";
import { MdDeleteOutline, MdEdit } from "react-icons/md";
import { FaPlus } from "react-icons/fa";
import { useDispatch, useSelector } from "react-redux";
import { addUsers, getUsers, updateUser, deletedUser } from "../redux/slice/userSlice.jsx";
import Pagination from "../components/Pagination.jsx";
import UserForm from "../components/UserForm.jsx";
import Button from "../components/UI/Button.jsx";


const User=()=>{
  const dispatch = useDispatch();
  const { users } = useSelector((state) => state.user);
  const [open, setOpen] = useState(false);
  const [editUser, setEditUser] = useState(null);
  const [page, setPage] = useState(1);
  const itemsPerPage = 10;

  const totalPages = Math.ceil(users.length/itemsPerPage);
  const startIndex = (page-1)*itemsPerPage;
  const paginatedUsers =users.slice(startIndex,startIndex + itemsPerPage);

  const handlePageChange=(newPage)=>{
    setPage(newPage);
  }

  useEffect(() => {
    dispatch(getUsers());
  }, [dispatch]);

  const handleDelete = (id) => {
    dispatch(deletedUser(id));
  };

  const handleEdit = (user) => {
    setEditUser(user);
    setOpen(true);
  };

  const handleSave = (user) => {
    if (user.id) {
      dispatch(updateUser({ id: user.id, userData: user }));
    } else {
      dispatch(addUsers(user));
    }
    setOpen(false);
    setEditUser(null);
  };

  return (
    <div className="flex flex-col gap-4 p-6 w-full min-h-[90vh]">
      <div className="flex justify-between items-center">
        <h1 className="text-xl font-bold text-gray-800">Users</h1>
        <Button text={"Add"} icon={<FaPlus/>} onClick={() => {
            setEditUser(null);
            setOpen(true);
          }} design={"btn btn-secondary"}/>
      </div>
      {open && (
        <UserForm
          initialData={editUser}
          onSave={handleSave}
          onClose={() => {
            setOpen(false);
            setEditUser(null);
          }}
        />
      )}

        {users.length === 0 ? (  
            <p className="text-center py-6 text-gray-500">No users found</p>
              
          ) : (
          paginatedUsers.map((user) => (
            <div key={user.id} className="grid grid-cols-2 md:grid-cols-4 justify-between items-center p-4  rounded-md shadow-sm bg-white gap-2 text-sm">   
              <h2 >{user.firstname} {user.lastname}</h2>
              <h2 >{user.email}</h2>
            <div className="md:flex md:justify-end" >
              <span className={`px-2 py-1 rounded text-sm  ${user.is_client ? "bg-blue-100 text-blue-700" : "bg-green-100 text-green-700"}`}>
                {user.is_client ? "Client" : "Staff"}
              </span>
            </div>
            <div className="flex justify-end items-center gap-2">
              <button onClick={() => handleEdit(user)} className="p-1 bg-green-500 text-white rounded-full hover:bg-green-600 text-sm">
                <MdEdit size={15}/>
              </button>
              <button onClick={() => handleDelete(user.id)} className="p-1 bg-red-500 text-white rounded-full hover:bg-red-600 text-sm">
                <MdDeleteOutline size={15} />
              </button>
            </div>
          </div>         
        ))
      )}  
      <Pagination page={page} totalPages={totalPages} onPageChange={handlePageChange}/>
    </div>
  );
};

export default User;
