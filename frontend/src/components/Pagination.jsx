import { MdNavigateNext, MdNavigateBefore } from "react-icons/md";

const Pagination = ({page,totalPages,onPageChange}) => {
  if (totalPages < 1) return null;

  return (
    <div className="flex justify-center items-center gap-4 mt-auto pt-6">
      <button disabled={page === 1} onClick={() => onPageChange(page - 1)} className={`px-4 py-2 rounded ${page === 1 ? "bg-gray-300 cursor-not-allowed" : "bg-slate-700 text-white hover:bg-slate-800"}`}>
        <MdNavigateBefore />
      </button>
      {[...Array(totalPages)].map((_, index) => {
        const pageNumber = index + 1;

        return (
          <button  key={pageNumber} onClick={() => onPageChange(pageNumber)}
            className={`px-3 py-1 rounded 
              ${page === pageNumber
                ? "bg-slate-900 text-white"
                : "bg-gray-200 hover:bg-gray-300"
              }`}
          >
            {pageNumber}
          </button>
        );
      })}
      <button disabled={page === totalPages} onClick={() => onPageChange(page + 1)} className={`px-4 py-2 rounded 
      ${page === totalPages ? "bg-gray-300 cursor-not-allowed" : "bg-slate-700 text-white hover:bg-slate-800"}`}>
        <MdNavigateNext/>
      </button>
    </div>
  );
};

export default Pagination;
