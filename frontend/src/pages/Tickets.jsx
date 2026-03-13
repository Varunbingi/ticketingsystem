import { useEffect, useState } from "react";
import { FaPlus } from "react-icons/fa";
import TicketForm from "../components/TicketForm.jsx";
import { MdDeleteOutline, MdEdit } from "react-icons/md";
import { addTicket, deleteTicket, getTickets, updateTicket } from "../redux/slice/ticketSlice.jsx";
import { useSelector, useDispatch } from "react-redux";
import { useNavigate } from "react-router-dom";
import Button from "../components/UI/Button.jsx";
import { useTranslation } from "react-i18next";

const Tickets = () => {

  const { t } = useTranslation();

  const dispatch = useDispatch();
  const { tickets } = useSelector((state) => state.ticket);

  const [open, setOpen] = useState(false);
  const [editTicket, setEditTicket] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    dispatch(getTickets());
  }, [dispatch]);

  const handleSave = (newTicket) => {
    if (newTicket.id) {
      dispatch(updateTicket({ id: newTicket.id, data: newTicket }));
      setOpen(false);
      setEditTicket(null);
    } else {
      dispatch(addTicket(newTicket));
      setOpen(false);
    }
  };

  const handleEdit = (ticketToEdit) => {
    setEditTicket(ticketToEdit);
    setOpen(true);
  };

  const handleDelete = (ticketId) => {
    dispatch(deleteTicket(ticketId));
  };

  return (
    <div className="p-6 w-full space-y-6 min-h-[90vh] flex flex-col">

      <div className="flex justify-between items-center">
        <h1 className="text-xl font-bold">{t("tickets_page_title")}</h1>

        <Button
          text={t("add")}
          icon={<FaPlus />}
          onClick={() => {
            setEditTicket(null);
            setOpen(true);
          }}
          design={"btn btn-secondary"}
        />
      </div>

      {open && (
        <TicketForm
          initialData={editTicket}
          onClose={() => {
            setOpen(false);
            setEditTicket(null);
          }}
          onSave={handleSave}
        />
      )}

      <div className="flex flex-col gap-3">
        {tickets.map((tkt) => (
          <div
            key={tkt.id}
            onClick={() => navigate(`/tickets/${tkt.id}`)}
            className="grid grid-cols-2 md:grid-cols-4 justify-between items-center bg-white rounded-xl shadow-md p-5 hover:shadow-lg transition gap-3"
          >
            <p className="text-sm">
              {t("subject")}: {tkt.subject}
            </p>

            <p className="text-sm">
              {t("priority")} :
              <span
                className={`${
                  tkt.priority == 0
                    ? "bg-green-500"
                    : tkt.priority == 1
                    ? "bg-orange-500"
                    : "bg-red-500"
                } text-white px-2 py-1 rounded-full ml-2`}
              >
                {tkt.priority == 0
                  ? t("low")
                  : tkt.priority == 1
                  ? t("medium")
                  : t("high")}
              </span>
            </p>

            <p className="text-sm">
              {t("status")} :
              <span
                className={`${
                  tkt.status == 0
                    ? "bg-gray-500"
                    : tkt.status == 1
                    ? "bg-orange-500"
                    : "bg-green-500"
                } text-white p-1 rounded-full ml-2`}
              >
                {tkt.status == 0
                  ? t("todo")
                  : tkt.status == 1
                  ? t("in_progress")
                  : t("done")}
              </span>
            </p>

            <div className="flex justify-end items-center gap-2">

              <button
                onClick={(e) => {
                  e.stopPropagation();
                  handleEdit(tkt);
                }}
                className="p-1 bg-green-500 text-white rounded-full hover:bg-green-600 text-sm"
              >
                <MdEdit size={15} />
              </button>

              <button
                onClick={(e) => {
                  e.stopPropagation();
                  handleDelete(tkt.id);
                }}
                className="p-1 bg-red-500 hover:bg-red-600 text-white rounded-full text-sm"
              >
                <MdDeleteOutline size={15} />
              </button>

            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Tickets;