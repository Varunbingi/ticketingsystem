import { useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { getTicketById } from "../redux/slice/ticketSlice";
import { FaArrowLeftLong } from "react-icons/fa6";

const TicketDetails = () => {
  const { id } = useParams();
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const { selectedTicket, loading } = useSelector(
    (state) => state.ticket
  );

  useEffect(() => {
    dispatch(getTicketById(id));
  }, [dispatch, id]);

  if (loading) return <p className="p-6">Loading...</p>;
  if (!selectedTicket) return <p className="p-6">Ticket not found</p>;
  return (
    <div className="p-6  mx-auto space-y-4">
      <button onClick={() => navigate(-1)} className="">
        <FaArrowLeftLong />
      </button>

      <div className="bg-white rounded-xl shadow-md p-6 space-y-3">
        <h1 className="text-2xl font-bold">
          Ticket #{selectedTicket.id}
        </h1>
        <p><strong>Client ID:</strong> {selectedTicket.client_id}</p>
        <p><strong>Priority:</strong> {selectedTicket.priority}</p>
        <p><strong>Status:</strong> {selectedTicket.status}</p>
        <p><strong>Subject:</strong> {selectedTicket.subject}</p>
        <p><strong>Description:</strong> {selectedTicket.description}</p>
        {selectedTicket.files?.length > 0 && (
          <div>
            <p className="font-semibold">Attachments</p>
            <ul className="list-disc ml-5">
              {selectedTicket.files.map((file, i) => (
                <li key={i}>
                  <a  href={file} target="_blank" className="text-blue-600 underline">
                    File {i + 1}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};

export default TicketDetails;
